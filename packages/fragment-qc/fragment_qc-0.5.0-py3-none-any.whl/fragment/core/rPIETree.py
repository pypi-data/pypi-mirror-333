#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from __future__ import annotations

from copy import copy
from itertools import combinations, product
from math import isclose
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    TypeVar,
)

import rustworkx as rx
from scipy.special import comb

from fragment.core.quickPIE import (
    add_cd,
    collect_primitives,
    roots_overlap,
)

# The set Type
SetT = TypeVar("SetT", frozenset[int], set[int])


def get_order(data: SetT, parents: Iterable[SetT]) -> int:
    return sum((1 for p in parents if p.issubset(data)))


def tree_equal(
    t1: rx.PyDiGraph, t2: rx.PyDiGraph, check_coefs=False, debug=False
) -> bool:
    nd1 = {n.data: n for n in t1.nodes()}
    nd2 = {n.data: n for n in t2.nodes()}

    if set(nd1.keys()) != set(nd2.keys()):
        return False

    for n1, d1 in nd1.items():
        d2 = nd2[n1]

        if not isclose(d1.coef, d2.coef, rel_tol=1e-6):
            return False
        if {s.data for s in t1.successors(d1.id)} != {
            s.data for s in t2.successors(d2.id)
        }:
            return False
        if {s.data for s in t1.predecessors(d1.id)} != {
            s.data for s in t2.predecessors(d2.id)
        }:
            return False
    return True


def deltas_equal(delta1, delta2) -> bool:
    """Testing function to confirm that two sets of deltas are equivalent"""
    d1_keys = frozenset((k for k, d in delta1.items() if d != 0))
    d2_keys = frozenset((k for k, d in delta2.items() if d != 0))

    if d1_keys != d2_keys:
        return False

    for k1 in d1_keys:
        if delta1[k1] != delta2[k1]:
            return False

    return True


def MBE_delta_coef(n: int, k: int) -> float:
    """
    Returns coef deltas for a standard MBE fragment
    n is the expansion order
    k is the expansion level
    """
    return (-1.0) ** (n - k)


class Node(Generic[SetT]):
    __slots__ = ("id", "_saved", "data", "coef", "primary_order", "primitive_order")

    def __init__(
        self,
        id: int,
        data: SetT,
        coef: int,
        primary_order: int,
        primitive_order: int,
        _saved: int = 0,
    ):
        self.id: int = id
        self._saved: int = _saved
        self.data: frozenset[int] = data
        self.coef: float = coef
        self.primary_order: int = primary_order
        self.primitive_order: int = primitive_order

    # For backwards Compatibility. Used to be dict
    def __getitem__(self, key: str) -> Any:
        return self.__getattribute__(key)

    def __setitem__(self, name: str, value: Any) -> None:
        return self.__setattr__(name, value)


class PIETree(Generic[SetT]):
    # The tree and supporting info!
    # G: rx.PyDiGraph[Node[SetT], None]
    G: rx.PyDiGraph
    set_class: type[SetT]
    node_lookup: dict[SetT, int]
    expand_counter: int
    clean_interval: int
    mbe_primaries: bool

    # Internal structural data
    primaries: set[SetT]  # Smallest blocks which may overlap
    primitives: set[SetT]  # Smallest blocks of the fragmentation
    target: SetT  # Target this tree should reproduce

    # Generic definitons for set-theoretic methods
    union: Callable[[SetT, ...], SetT]
    insersection: Callable[[SetT, SetT], SetT]
    issubset = Callable[[SetT, SetT], bool]
    issuperset = Callable[[SetT, SetT], bool]

    def __init__(
        self,
        primaries: set[SetT],
        primitives: set[SetT]
        | None = None,  # Allow caching for performance (primay -> aux)
        G: rx.PyDiGraph | None = None,
        coef: int = 0.0,  # Primay initalization coef
        clean_interval: int = 500,
    ) -> None:
        # Link to set-theoretic methods
        self.set_class = next(iter(primaries)).__class__
        self.union = self.set_class.union
        self.intersection = self.set_class.intersection
        self.issubset = self.set_class.issubset
        self.issuperset = self.set_class.issuperset
        self.expand_counter = 0
        self.clean_interval = clean_interval

        # Add graph-data
        if primitives:
            self.primitives = frozenset(primitives)
        else:
            self.primitives = frozenset(collect_primitives(primaries))
        self.primaries = frozenset(primaries)
        self.target = self.union(*self.primaries)

        # Adds some protection against MBE additions to GMBE fragments
        self.mbe_primaries = self.primitives == self.primaries

        if G is None:
            self.G = rx.PyDiGraph()
            self.node_lookup = {}

            # Add primitives, the base layer of the graph
            for p in self.primitives:
                self.add_node(p, coef=0.0, link=False)
            # Add higher order primaries
            for p in self.primaries:
                self.expand(p, coef)
        else:
            # Caller is repsobisible for a reasonable G
            self.G = G
            self.node_lookup = {n.data: n.id for n in G.nodes()}

    def __iter__(self) -> Iterator[tuple[SetT, Node[SetT]]]:
        return ((i.data, i) for i in self.G.nodes())

    def __getitem__(self, k: SetT | int) -> Node[SetT]:
        # Handle direct indexing
        if isinstance(k, int):
            return self.G[k]

        # Handle key indexing
        return self.G[self.node_lookup[k]]

    def __contains__(self, k: Any) -> bool:
        if isinstance(k, int):
            return self.G[k]
        return k in self.node_lookup

    def __len__(self) -> int:
        return len(self.G)

    def copy(self) -> "PIETree[SetT]":
        """Create copy of graph and all it's nodes"""
        G = self.G.copy()

        # Copy each node. This is not done automatically
        for nid in self.G.node_indices():
            G[nid] = copy(G[nid])

        # Don't worry about edge data
        return self.__class__(primaries=self.primaries, primitives=self.primitives, G=G)

    def NIDs(self, node_keys: Iterable[SetT]) -> set[int]:
        """Get the node IDs for a given iterable of keys"""
        return {self.node_lookup[i] for i in node_keys}

    @classmethod
    def brute_force(cls, nodes: Iterable[SetT]) -> "PIETree[SetT]":
        """Start with a collection and build a PIE tree by brute force.

        .. NOTE ::
            Method is only for testing
        """
        primitives = collect_primitives(nodes)
        tree = cls(primitives, primitives)

        # Add primitives
        for n in nodes + [frozenset(p) for p in primitives]:
            # Quick and dirty node addition
            tree.add_node(n, 0.0, link=False)

        # Add cross linkages to ALL nodes (SLOW)
        for a, b in combinations(tree.G.nodes(), 2):
            if a.data.issubset(b.data):
                tree.G.add_edge(a.id, b.id, None)
            elif a.data.issuperset(b.data):
                tree.G.add_edge(b.id, a.id, None)

        for k in tree.NIDs(tree.primaries):
            tree._brute_force_clean_edges(k)

        return tree

    def _brute_force_clean_edges(self, k: int) -> None:
        """Removes edges from indirect descendents"""
        for a, b in combinations(self.G.successors(k), 2):
            try:
                if a.data.issubset(b.data):
                    self.G.remove_edge(k, b.id)
                elif a.data.issuperset(b.data):
                    self.G.remove_edge(k, a.id)
            except rx.NoEdgeBetweenNodes:
                pass

        # Go through and do the same for all children
        for n in self.G.successor_indices(k):
            self._brute_force_clean_edges(n)

    @classmethod
    def from_primitives(
        cls, primitives: set[SetT], primaries: list[SetT] | None = None
    ) -> "PIETree":
        """Creates PIE tree from primitaves and primaries.
        NOTE: This method is depricated and is only present for backwards compatibility
        """
        if primaries:
            return cls(primaries, primitives=primitives)
        else:
            return cls(primitives)

    @classmethod
    def from_primaries(cls, primaries: list[SetT], add=False, add_coef=1) -> "PIETree":
        """Creates PIETree from primary fragments.

        Primitives are generated

        Depricated
        """
        return cls(primaries, coef=add_coef)

    @classmethod
    def from_roots(
        cls, roots: list[SetT], primitives: set[SetT] | None = None
    ) -> "PIETree":
        """Creats PIETree from a collection of roots."""
        _primitives = collect_primitives(roots) if primitives is None else primitives
        tree = cls.from_primitives(_primitives)
        for r in roots:
            tree.expand(r)
        return tree

    @classmethod
    def from_MBE_primary_frags(
        cls, primaries: Iterable[SetT], order: int
    ) -> "PIETree[SetT]":
        """Creates PIETree for complete MBE(n)"""
        if not primaries:
            raise ValueError("Primaries cannot be empty")

        if roots_overlap(primaries):
            raise Exception("Cannot perform MBE with overlapping fragments (yet).")

        # TODO: Exploid node and edge_count_hint

        if len(primaries) <= order:
            tree = cls(primaries, primitives=primaries)
            tree.expand(tree.union(*primaries), 1.0)
        else:
            tree = cls(primaries, primitives=primaries, G=rx.PyDiGraph())
            tree.add_MBE_levels(primaries, order)
        return tree

    def add_MBE_levels(self, primaries: list[SetT], order: int, m: int = 0):
        """
        Adds an MBE level and links to to the previous level

        See "Understanding the Many-Body Expansion: Part I" for this formula
        """
        N = len(primaries)
        coef = comb(N - order - 1 + m, m) * (-1) ** m
        make_links = m < order - 1

        # Add lower levels first so we can efficiently link to them
        if make_links:
            self.add_MBE_levels(primaries, order, m + 1)

        # Add the proper number of coefficients to the node dict
        for prims in combinations(primaries, order - m):
            frag = frozenset.union(*prims)
            k = self.add_node(frag, float(coef), link=False)

            if make_links:
                for children in combinations(prims, len(prims) - 1):
                    ck = frozenset.union(*children)
                    self.G.add_edge(self.node_lookup[ck], k, None)

    # CONSTRUCTION METHODS
    def add_node(self, data: SetT, coef: float, link=True) -> int:
        """Adds a node to the tree

        .. NOTE ::
            The node is not linked (no parentage information!)
        """
        if data in self.node_lookup:
            # Don't double-add nodes. RustworkX doesn't catch this
            return self.node_lookup[data]

        # Create new node
        node_data = Node(
            -1,
            data,
            coef,
            primary_order=get_order(data, self.primaries),
            primitive_order=get_order(data, self.primitives),
        )

        nid = self.G.add_node(node_data)  # Add to graph
        node_data.id = nid  # Add the back reference
        self.node_lookup[data] = nid  # Allow key-lookup

        # Optionally add parent-child information
        if link:
            self.link_node(node_data)

        return nid

    def link_node(self, node: Node) -> None:
        """
        Creates edges between any parents/children in the graph for new a node

        Method removes edges from other parents and children to ensure the graph's
        ingegrity
        """
        nid = node.id
        data = node.data
        if self.G.in_degree(nid) or self.G.out_degree(nid):
            raise AttributeError(f"Node {nid} is already linked")

        # Find spot in DiGraph
        parents = self.find_parents(data)
        children = self.find_children(data, parents)

        # NOTE: This throws a NoEdgeBetweenNodes error
        # self.G.remove_edges_from([(p, c) for p, c in product(parents, children)])
        for p, c in product(parents, children):
            # NOTE: Not particularly efficient...
            try:
                self.G.remove_edge(p, c)
            except rx.NoEdgeBetweenNodes:
                pass

        # Create edges
        self.G.add_edges_from_no_data([(p, nid) for p in parents])
        self.G.add_edges_from_no_data([(nid, c) for c in children])

    def update_coef(self, n: SetT, delta: float) -> None:
        """Update the node coefficient

        Adds the node if it does not exist
        """
        try:
            self[n].coef += delta
        except KeyError:
            self.add_node(n, delta)

    # QUERY METHODS

    ################# FIND PARENTS #################
    def find_parents(self, key: SetT) -> set[int]:
        """FOR USE WITH KEY NOT IN TREE
        Finds parents for a node which isn't in the tree

        Returns:
            List of node indexes which should be `key`'s parents
        """
        parents: set[int] = set()
        visited: set[int] = set()

        for n in self.primitives:
            if not n.issubset(key):
                continue
            self._find_parents(self.node_lookup[n], key, parents, visited)

        return parents

    def _find_parents(
        self, nid: int, key: SetT, parents: set[SetT], visited: set[int]
    ) -> None:
        # Skip if we have already visited
        visited.add(nid)

        # If we are here, node *could* be parent. Must check children
        is_parent = True

        # Check if nodes children are also children
        for p_node in self.G.successors(nid):
            if p_node.data.issubset(key):
                is_parent = False

                # Don't look any further if node is visited
                if p_node.id not in visited:
                    self._find_parents(p_node.id, key, parents, visited)

        if is_parent:
            parents.add(nid)

    ################# FIND PARENTS #################
    def find_children(self, key: SetT, start: set[SetT]) -> set[SetT]:
        """Returns children of this node

        These nodes are the smallest nodes which are supersets of this nodes.

        start: a list of parents (could also be primitives, but this is slow)
        """
        children: set[int] = set()
        visited: set[int] = set()

        # Assumes start are all children of `key`
        for k in start:
            self._find_children(k, key, visited, children)

        return {self.node_lookup[c] for c in children}

    def _find_children(
        self, nid: int, d: SetT, visited: set[int], children: set[int]
    ) -> None:
        visited.add(nid)

        for c in self.G.successors(nid):
            # This is a child node
            if c.data.issuperset(d):
                add_cd(children, c.data)
                if c.id not in visited:
                    self._visit_all_successors(c.id, visited)
                continue
            # This nodes has an indirect child
            if c.id not in visited:
                self._find_children(c.id, d, visited, children)

    def _visit_all_successors(self, nid: int, visited: set[int]):
        """Marks all succeeding nodes as visited"""
        visited.add(nid)
        visited.update(self.G.successor_indices(nid))

    def accessible_from(
        self, n: SetT, accessible: set[SetT] | None = None
    ) -> set[SetT]:
        """Returns which nodes this node is accessable from"""
        _accessible = set() if accessible is None else accessible

        for c in self.tree.successors(n):
            # We don't visit it or it's already visited
            if c in _accessible:
                continue
            _accessible.add(c)
            self.accessible_from(c, accessible=_accessible)
        return _accessible

    # BUILDING METHODS
    def remove_node(self, n: SetT) -> None:
        """Removes a node from the PIETree"""
        nid = self.node_lookup[n]
        children = set(self.G.successor_indices(nid))
        parents = set(self.G.predecessor_indices(nid))
        del self.node_lookup[n]
        self.G.remove_node(nid)
        for p in parents:
            accessible_children = rx.descendants(self.G, p)
            for c in children:
                if c in accessible_children:
                    continue
                self.G.add_edge(p, c, None)

    def expand(self, n: SetT, coef: int = 1.0, method: str | None = None) -> None:
        # Remove zero nodes. Usually not an issue but can become a bottle neck when the
        # tree gets large
        if self.expand_counter % self.clean_interval == 0:
            self.clean_zeros()
        self.expand_counter += 1

        # Calculate the primary components here. Will help determine which
        # delta strategy to use
        prims = [p for p in self.primitives if p.issubset(n)]

        # Make a decision on which delta strategy to use

        # For testing, do all three/four, but only apply the last one
        # graph_size = len(self.G)

        if method is None:
            # Automatically choose the best delta method
            if len(prims) > 5:
                deltas = self._calculate_deltas_descendants(n, coef, prims)
            else:
                deltas = self._calculate_deltas_graph(n, coef, prims)
        elif method == "descendants":
            deltas = self._calculate_deltas_descendants(n, coef, prims)
        elif method == "graph":
            deltas = self._calculate_deltas_graph(n, coef, prims)
        elif method == "mbe":
            # Do MBE-style addition. Use with CAUTION
            deltas = self._calculate_deltas_mbe(n, coef, prims)
        else:
            raise ValueError(
                f"Unknown expand method '{method}'. Options are None (automatic), 'descendants', 'graph' and 'mbe'"
            )

        # Update deltas and add any new nodes
        # Add the new node!
        self.update_coef(n, deltas[n])
        del deltas[n]

        # Update the rest. Exclude coef = 0
        for k, d_coef in deltas.items():
            if d_coef == 0:
                continue
            self.update_coef(k, d_coef)

    def _calculate_deltas_mbe(
        self, n: SetT, coef: int, primitives: list[SetT]
    ) -> dict[SetT, float]:
        """Use caution"""
        if not self.mbe_primaries:
            print("Actually, doing desc")
            return self._calculate_deltas_descendants(n, coef, primitives)

        num_frags = len(primitives)
        deltas: dict[SetT, float] = {}
        for k in range(1, num_frags + 1):
            delta = coef * MBE_delta_coef(num_frags, k)
            for combs in combinations(primitives, k):
                key = self.union(*combs)
                deltas[key] = delta

        # Let's test this just to make sure...
        # assert deltas_equal(deltas, self._calculate_deltas_graph(n, coef, primitives))

        return deltas

    def _calculate_deltas_graph(
        self, n: SetT, coef: int, primitives: list[SetT]
    ) -> dict[SetT, float]:
        """Calculates all overlaps with `n` and update coefficients"""
        overlaps: dict[SetT, set[int]] = {}
        # This step could get expensive. But should be less than THOUSANDS of intersections...

        for p in primitives:
            pid = self.node_lookup[p]
            desc = rx.descendants(self.G, pid)
            desc.add(pid)
            overlaps[p] = desc

        # Check for nodes which overlap everything
        # Work from the largest to smallest!
        changes: dict[SetT, float] = {}
        for n_overlaps in reversed(range(1, len(overlaps) + 1)):
            for combs in combinations(overlaps.items(), n_overlaps):
                overlapping_nodes = set.intersection(*(c[1] for c in combs))
                if not overlapping_nodes:
                    continue
                # Remove these nodes from the subsets
                for c in combs:
                    c[1].difference_update(overlapping_nodes)
                key = self.union(*(c[0] for c in combs))

                changes[key] = -coef * sum((self.G[i].coef for i in overlapping_nodes))

        try:
            changes[n] += coef
        except KeyError:
            changes[n] = coef
        return changes

    def _calculate_deltas_descendants(
        self, n: SetT, coef: int, primitives: list[SetT]
    ) -> dict[SetT, float]:
        """Traverse the tree, starting with the primitive nodes
        and accumulate changes on the fly!
        """
        # Find all decendents of whichever primary nodes are subsets of p
        try:
            probe = self.G.add_node("PROBE")
            for p in primitives:
                self.G.add_edge(probe, self.node_lookup[p], None)
            overlaps = rx.descendants(self.G, probe)
        finally:
            self.G.remove_node(probe)

        # Calculate coef deltas for overlaps with existing nodes
        changes: dict[SetT, int] = {n: coef}

        for o in overlaps:
            od = self.G[o]
            od_key = od.data
            key = self.intersection(n, od_key)

            # Update coefficient
            try:
                changes[key] += -coef * od.coef
            except KeyError:
                changes[key] = -coef * od.coef
        return changes

    def clean_zeros(self):
        """Remove nodes where the coef == 0

        This method will not remove primitive nodes
        """
        zeros: set[SetT] = set()

        for n in self.G.nodes():
            if n.coef == 0 and n.primitive_order != 1:
                zeros.add(n.data)

        for z in zeros:
            self.remove_node(z)

    def update_target(self):
        self.target = {k for k in self.count_members().keys()}

    # VALIDATION METHODS
    def count_members(self) -> dict[int, int]:
        """Counts the net times each key in self.targe occures"""
        counts: dict[int, int] = {}
        coef_key = "coef"
        for _, d in self:
            for i in d.data:
                try:
                    counts[i] += d[coef_key]
                except KeyError:
                    counts[i] = d[coef_key]
        return counts

    def is_complete(self) -> bool:
        """Checks that the coefficients of each term in self.target equal 1"""
        counts = self.count_members()
        for c in counts.values():
            if c != 1:
                return False

        if self.target != {s for s in counts.keys()}:
            return False

        return True

    @staticmethod
    def is_equal(t1: "PIETree", t2: "PIETree", check_coef=False, debug=False) -> bool:
        return tree_equal(t1.G, t2.G, check_coefs=check_coef, debug=debug)

    def to_quickPIE(self) -> dict[SetT, float]:
        return {
            d.data: d.coef for n, d in self if not isclose(d.coef, 0.0, rel_tol=1e-6)
        }

    def visualize(self, display=False):
        from rustworkx.visualization import graphviz_draw

        def label_fn(n: Node) -> dict[str, str]:
            key = ",".join(str(s) for s in sorted(n.data))
            coef = f"c = {n.coef}"
            primary_order = f"po = {n.primary_order}"
            return {"label": "\n".join([key, coef, primary_order])}

        img = graphviz_draw(
            self.G,
            node_attr_fn=label_fn,
        )
        img.show()
