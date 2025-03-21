#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import enum
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from datetime import datetime
from itertools import combinations
from typing import (
    Any,
    Generator,
    Optional,
)
from uuid import UUID, uuid4

import rustworkx as rx
from conformer.records import SystemRecord
from conformer.systems import NamedSystem, System
from conformer_core.stages import Stage
from conformer_core.util import ind, summarize
from lru import LRU

# from fragment.core.PIETree import ROOT, PIETree
from fragment.core.rPIETree import Node, PIETree


class ViewType(enum.IntEnum):
    PRIMARY = 0
    AUXILIARY = 1
    PRIMITIVE = 2


class Key(frozenset[int]): ...


class KeySet(set[Key]): ...


Keyable = Key | System | Iterable[int]


@dataclass
class View:
    tree: PIETree[frozenset[int]]
    order: int
    type: ViewType
    fragmenter: Stage  # NOTE: Not a Fragmenter to avoid circular dep.

    parent: "View | None" = None
    supersystem: System | None = None

    id: UUID = field(default_factory=uuid4)
    name: str = field(default_factory=str)
    created: datetime = field(default_factory=datetime.now)
    meta: dict[str, Any] = field(default_factory=dict)
    system_cache: LRU = field(default_factory=lambda: LRU(5000))
    # system_cache: LRU[System, SystemRecord] = field(default_factory=lambda: LRU(500))
    _saved: int = 0

    #####     CONSTUCTORS     #####
    def __post_init__(self) -> None:
        if self.supersystem:  # Clean the supersystem and make sure it's propertly bound
            self.bind_system(self.supersystem)

    @classmethod
    def new_primary(cls, fragmenter: Stage, primaries: KeySet, **kwargs):
        # Can't use the _key function because view isn' initilized

        tree = PIETree.from_primaries(primaries, add=True, add_coef=0)
        return cls(
            tree=tree, order=0, type=ViewType.PRIMARY, fragmenter=fragmenter, **kwargs
        )

    @classmethod
    def new_auxiliary(
        cls, fragmenter: Stage, primary_view: "View", order: int, **kwargs
    ):
        # Quick than deep copying?
        tree = PIETree.from_primaries(primary_view.tree.primaries, add=True, add_coef=0)
        return cls(
            tree=tree,
            order=order,
            type=ViewType.AUXILIARY,
            parent=primary_view,
            supersystem=primary_view.supersystem,
            fragmenter=fragmenter,
            **kwargs,
        )

    @classmethod
    def new_MBE_auxiliary(
        cls, fragmenter: Stage, primary_view: "View", order: int, **kwargs
    ):
        tree = PIETree.from_MBE_primary_frags(primary_view.primaries, order)
        return cls(
            tree=tree,
            order=order,
            type=ViewType.AUXILIARY,
            parent=primary_view,
            supersystem=primary_view.supersystem,
            fragmenter=fragmenter,
            **kwargs,
        )

    def add(self, value: Keyable, coef=1, method: str | None = None) -> None:
        k = self._key(value)  # This could probably be replaced with decorator
        self.tree.expand(k, coef=coef, method=method)

    @property
    def primaries(self):
        return self.tree.primaries

    @property
    def primitives(self):
        return self.tree.primitives

    #####     KEYS     #####

    def _system_to_key(self, sys: System) -> Key:
        # Be strict since equality checks for systems are expensive
        raise Exception("_system_to_key is deprecated. It's unreleable")
        if sys.supersystem != self.supersystem:
            raise ValueError(
                f"System is not a subsystem of the view's supersystem.\n\tSystem: {sys}\n\tParents: {sys.supersystem} != {self.supersystem}"
            )
        return Key((m[0] for m in self.supersystem.join_map(sys)))

    @classmethod
    def primaries_from_subsystems(self, systems: list[System]) -> KeySet:
        return {s.supersystem_idxs for s in systems}

    def _key(self, k: Keyable) -> Key:
        if isinstance(k, frozenset):  # Allow any frozen set
            return k
        elif isinstance(k, System):
            return self._system_to_key(k)
        else:
            return Key(k)

    #####  CONSTRUCTION METHODS  #####

    def __contains__(self, value: Keyable) -> bool:
        return self._key(value) in self.tree

    def __iter__(self) -> Iterator[Key]:
        return self.iter_data()

    def __getitem__(self, value: Keyable) -> Node:
        return self.tree[self._key(value)]

    def __len__(self) -> int:
        return len(self.tree)

    def __eq__(self, other: "View") -> bool:
        """Equality doesn't check for which stage created it"""
        if not isinstance(other, self.__class__):
            return False
        if self is other:
            return True
        return all(
            [
                self.type == other.type,
                self.order == other.order,
                self.tree.is_equal(self.tree, other.tree),
            ]
        )

    def __hash__(self) -> int:
        return self.id.__hash__()

    #####  GETTER_METHODS  #####

    def bind_system(self, sys: System, keep_order=False) -> None:
        """Associates system to view"""
        self.system_cache.clear()
        if sys.is_canonized or keep_order:
            self.supersystem = sys
        else:
            self.supersystem = sys.canonize()

    def get_primaries(self, value: Keyable) -> KeySet:
        """Returns primary keys which are subsets of `value`"""
        k = self._key(value)
        return {p for p in self.tree.primaries if p.issubset(k)}

    def get_primitives(self, value: Keyable) -> KeySet:
        """Returns primitive keys which are subsets of `value`"""
        k = self._key(value)
        return {p for p in self.tree.primitives if p.issubset(k)}
    

    def get_aux_parents_from_primaries(self, primaries: list[frozenset[int]], order: int) -> KeySet:
        """Generates auxiliary parents of order `order` for given `value`"""
        if len(primaries) < order:
            raise ValueError(f"Cannot generate aux of order {order} for value consisting of {len(primaries)} primaries")

        return {frozenset.union(*c) for c in combinations(primaries, order)}
    

    def get_aux_parents_from_aux(self, value: Keyable, order: int) -> KeySet:
        """Generates lower-order combinatoric aux parents for a given Keyable"""
        primaries = self.get_primaries(value)
        return self.get_aux_parents_from_primaries(primaries, order)


    def get_system(self, value: Keyable, use_mods: bool = True) -> System:
        """Returns a subsystem of the bound supersystem"""
        # TODO: Allow disabling mods
        if self.supersystem is None:
            raise AttributeError("View does not have a bound supersystem")
        k = self._key(value)

        if not use_mods:
            return self.supersystem.subsystem(k)  # This is usually pretty fast

        if k in self.system_cache:  # Check for cached version!
            return self.system_cache[k]
        else:  # Mod system and add it to the cache
            sys = self.supersystem.subsystem(k, self.fragmenter.subsystem_mods)
            self.system_cache[k] = sys
            return sys

    #####  ITERATION METHODS  #####
    def size(self, include_zeros=False) -> int:
        if include_zeros:
            return self.__len__()
        else:
            return sum((1 for _ in self.iter_keys()))

    def iter_systems(
        self, include_zeros=False, use_mods=True
    ) -> Generator[tuple[System, dict], None, None]:
        """Iterates all systems which exist in the view and their node data"""
        for k, d in self.iter_data(include_zeros):
            yield self.get_system(k, use_mods), d

    def iter_data(self, include_zeros=False) -> Generator[tuple[Key, Node], None, None]:
        """Iterates all node keys and data for the view"""
        for k, d in self.tree:
            if d["coef"] == 0 and not include_zeros:
                continue
            yield k, d

    def iter_keys(self, include_zeros=False) -> Generator[Key, None, None]:
        for n, d in self.iter_data(include_zeros):
            yield n

    #####  RELATIONSHIPS  ####

    def get_parents(self, value: Keyable) -> KeySet:
        """Returns the direct parents of node  `value`

        ..NOTE::
            NetworkX call this function sucessors but that is a mouthful
        """
        k = self._key(value)
        return {n.data for n in self.tree.G.predecessors(self.tree.node_lookup[k])}

    def get_ancestors(self, value: Keyable) -> KeySet:
        """Returns all parents (direct and indirect) of node  `value`"""
        k = self._key(value)
        nid = self.tree.node_lookup[k]
        return {self.tree.G[n].data for n in rx.ancestors(self.tree.G, nid)}

    def get_children(self, value: Keyable) -> KeySet:
        """Returns the direct children of node  `value`

        ..NOTE::
            NetworkX call this function predacessors but that is a mouthful
        """
        k = self._key(value)
        return {n.data for n in self.tree.G.successors(self.tree.node_lookup[k])}

    def get_descendents(self, value: Keyable) -> KeySet:
        """Returns all children (direct and indirect) of node  `value`"""
        k = self._key(value)
        nid = self.tree.node_lookup[k]
        return {self.tree.G[n].data for n in rx.descendants(self.tree.G, nid)}

    def active_edge(self) -> set[Key]:
        """Returns notes which don't have children (the working edge of the view)"""
        edge_n = self.tree.G.filter_nodes(lambda n: self.tree.G.out_degree(n.id) == 0)
        return {self.tree.G[n].data for n in edge_n}


@dataclass
class ViewRecord(SystemRecord):
    view: Optional[View] = None

    def summarize(self, padding=2, level=0) -> str:
        rec_str = f"View Record {self.id}:\n"
        level += 1
        if self.view.name:
            rec_str += ind(padding, level, f"View Name: {self.view.name}\n")
        rec_str += ind(padding, level, f"Driver: {self.stage.name}\n")
        rec_str += ind(padding, level, f"Fragmenter: {self.view.fragmenter.name}\n")
        rec_str += ind(padding, level, f"Order: {self.view.order}\n")

        if isinstance(self.system, NamedSystem):
            rec_str += ind(padding, level, f"System: {self.system.name}\n")
        else:
            rec_str += ind(padding, level, f"System: {self.system}\n")

        rec_str += ind(
            padding,
            level,
            f"Created: {self.start_time.isoformat(timespec='minutes')}\n",
        )
        rec_str += ind(padding, level, f"Num Fragments: {self.view.size()}\n")
        self.view
        rec_str += ind(padding, level, f"Status: {self.status.name}\n")

        if self.meta:
            rec_str += summarize("Meta", self.meta)

        if self.properties:
            rec_str += ind(padding, level, "Properties:\n")
            rec_str += self.properties.summarize(padding=padding, level=level + 1)
        return rec_str
