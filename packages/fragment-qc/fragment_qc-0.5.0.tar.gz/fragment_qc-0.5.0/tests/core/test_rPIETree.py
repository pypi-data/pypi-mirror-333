#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from itertools import combinations
from typing import List, Set

from scipy.special import comb

from fragment.core.legacy_PIE import mk_key
from fragment.core.legacy_PIETree import Key
from fragment.core.quickPIE import compress_up, mk_quickPlan, quickNode
from fragment.core.rPIETree import PIETree, collect_primitives
from tests._util import QNList, QNSet

t1 = QNList({1}, {3}, {1, 2}, {1, 3, 4})  # 3,4 is not a parent of 1,2,3
t2 = QNList({1}, {2}, {3}, {4}, {1, 2}, {2, 3}, {1, 3}, {1, 2, 3, 4})
t3 = QNList({1}, {2}, {1, 3}, {1, 4})
t4 = QNList({1, 2, 4}, {1}, {2}, {3}, {4})
t5 = QNList({1, 2, 3}, {1, 2, 4}, {1}, {2})
t6 = QNList({1, 2, 3}, {1}, {2})
t7 = QNList(
    {0, 1, 3, 4},
    {0, 1},
    {2},
    {0, 1, 4},
    {0, 1, 2},
    {0, 1, 3},
    {0, 1, 2, 4},
    {4},
    {1},
    {0, 2, 3, 4},
    {0, 1, 2, 3},
    {0},
    {3},
)
t8 = QNList({0, 1, 2, 3}, {0, 1, 2}, {0, 3}, {0}, {1})
t9 = QNList(
    {0, 5, 7, 9, 12, 14},
    {1, 3, 5, 6, 12, 14, 17, 18},
    {1, 3, 5, 6, 12, 14, 18},
    {0, 1, 5, 6, 7, 9, 12, 14, 18},
    {1, 3, 5, 6, 7, 12, 14, 17},
    {0, 3, 5, 7, 9, 12, 14, 17},
    {0, 1, 5, 6, 7, 9, 12, 14},
    {1, 3, 5, 6, 7, 12, 14, 20},
    {1, 3, 5, 6, 7, 12, 14, 17, 20},
    {5, 7, 12, 14},
    {1, 3, 5, 6, 12, 14},
    {3, 5, 7, 12, 14, 17, 20},
    {1, 5, 6, 7, 12, 14},
    {1, 3, 5, 6, 12, 14, 17},
    {0, 3, 5, 7, 9, 12, 14, 17, 20},
    {1, 3, 5, 6, 7, 12, 14},
    {3},
    {1, 3, 5, 6, 7, 12, 14, 18, 20},
    {3, 5, 7, 12, 14, 17},
    {0, 1, 3, 5, 6, 7, 9, 12, 14, 17},
    {1, 5, 6, 7, 12, 14, 18},
    {3},
    {5, 7, 12, 14},
    {20},
)

d1 = QNList({0}, {0, 1}, {0, 2}, {0, 1, 2})


class ConsolidateTestCases(unittest.TestCase):
    def test_primitives(self):
        primary_nodes = QNList({1, 2}, {2, 3})
        primitives = QNSet((1,), (2,), (3,))

        p1 = collect_primitives(primary_nodes)
        self.assertSetEqual(p1, primitives)

        # Case from fuzzing
        primary_nodes = QNList(
            {8, 18, 20, 13},
            {0, 6, 7},
            {1, 13, 17},
            {16, 17, 20, 1},
            {8, 17, 3},
            {0, 9, 12, 5},
            {1, 2, 12, 17},
            {8, 0, 13, 15},
            {2, 4, 6},
            {16, 1, 10, 9},
        )
        primitives = QNSet(
            (1,),
            (16,),
            (6,),
            (12,),
            (18,),
            (2,),
            (15,),
            (5,),
            (8,),
            (4,),
            (17,),
            (7,),
            (20,),
            (10,),
            (0,),
            (13,),
            (3,),
            (9,),
        )

        p2 = collect_primitives(primary_nodes)
        self.assertSetEqual(p2, primitives)

    def test_compress_up(self):
        roots = QNList({1, 2}, {2, 3}, {3})
        compressed = compress_up(roots)
        self.assertListEqual(list(compressed), QNList({1, 2}, {2, 3}))

        roots.reverse()
        compressed = compress_up(roots)
        self.assertListEqual(list(compressed), QNList({2, 3}, {1, 2}))


class TreeCreateTestCases(unittest.TestCase):
    def assertAdd(self, d: Set[int], t_ref: List[Set[int]]):
        _d = frozenset(d)
        _t_ref = QNList(*t_ref)

        # Create reference tree
        t = PIETree.brute_force(_t_ref)

        # Identify parents/children for testing
        parents = t.find_parents(_d)
        children = t.find_children(_d, parents)

        # Add node
        # t.visualize(display=True)
        t.add_node(_d, 0)

        # Compair to brute-forced version
        ref = PIETree.brute_force(_t_ref + [_d])
        # ref.visualize(display=True)
        self.assertTrue(PIETree.is_equal(t, ref))
        return {t[n].data for n in parents}, {t[n].data for n in children}

    def assertRemove(self, d, t_ref: Set[Key]):
        # Create reference graph
        _d = frozenset(d)
        _t_ref = QNList(*t_ref)
        t = PIETree.brute_force(_t_ref)

        # Remvoe node
        t.remove_node(_d)

        # Compare to brute-forced version
        ref = PIETree.brute_force([i for i in _t_ref if i != _d])
        self.assertTrue(PIETree.is_equal(t, ref))

    def test_t1(self):
        parents, children = self.assertAdd({1, 2, 3}, t1)
        self.assertSetEqual(
            QNSet((1, 2), (3,)),
            parents,
        )
        self.assertSetEqual(set(), children)

    def test_t2(self):
        parents, children = self.assertAdd({1, 2, 3}, t2)
        self.assertSetEqual(
            QNSet((1, 2), (2, 3), (1, 3)),
            parents,
        )
        self.assertSetEqual(
            QNSet((1, 2, 3, 4)),
            children,
        )

    def test_t3(self):
        parents, children = self.assertAdd({1, 2}, t3)
        self.assertSetEqual(QNSet((1,), (2,)), parents)
        self.assertSetEqual(set(), children)

    def test_t4(self):
        parents, children = self.assertAdd({1, 2, 3}, t4)
        self.assertSetEqual(QNSet((1,), (2,), (3,)), parents)
        self.assertSetEqual(set(), children)

    def test_t5(self):
        parents, children = self.assertAdd({1, 2}, t5)
        self.assertSetEqual(QNSet((1,), (2,)), parents)
        self.assertSetEqual(QNSet((1, 2, 3), (1, 2, 4)), children)

    def test_t6(self):
        parents, children = self.assertAdd({1, 2}, t6)
        self.assertSetEqual(QNSet((1,), (2,)), parents)
        self.assertSetEqual(QNSet((1, 2, 3)), children)

    def test_t7(self):
        parents, children = self.assertAdd({0, 2}, t7)
        self.assertSetEqual(QNSet((0,), (2,)), parents)
        self.assertSetEqual(QNSet((0, 1, 2), (0, 2, 3, 4)), children)

    def test_t8(self):
        parents, children = self.assertAdd({0, 1}, t8)
        self.assertSetEqual(QNSet((0,), (1,)), parents)
        self.assertSetEqual(QNSet((0, 1, 2)), children)

    def test_t9(self):
        parents, children = self.assertAdd({3, 5, 7, 12, 14, 20}, t9)
        self.assertSetEqual(QNSet((3,), (20,), (5, 7, 12, 14)), parents)
        self.assertSetEqual(
            QNSet((1, 3, 5, 6, 7, 12, 14, 20), (3, 5, 7, 12, 14, 17, 20)), children
        )

    def test_d1(self):
        self.assertRemove({0, 1}, d1)

    def test_from_roots(self):
        """Check that from_roots works.

        Does not check coefficients
        """
        t = PIETree.from_roots(t1)
        self.assertTrue(t.is_complete)

        t = PIETree.from_roots(t2)
        self.assertTrue(t.is_complete)

        t = PIETree.from_roots(t3)
        self.assertTrue(t.is_complete)

    def test_MBE(self):
        order = 4
        for n in range(5, 8):
            frags = QNSet(*((i,) for i in range(n)))
            MBETree = PIETree.from_MBE_primary_frags(frags, order)
            nodes_in_graph = int(
                comb(len(frags), 4)
                + comb(len(frags), 3)
                + comb(len(frags), 2)
                + comb(len(frags), 1)
            )
            self.assertEqual(nodes_in_graph, len(MBETree.G))
            self.assertTrue(MBETree.is_complete())

            GMBETree = PIETree.from_primitives(set(frags))
            for f in combinations(frags, order):
                GMBETree.expand(frozenset.union(*f))

            # Check that all nodes are accessible and have right number of children
            self.assertTrue(PIETree.is_equal(MBETree, GMBETree, check_coef=True))

    def test_idempotence(self):
        SIZE = 6
        prims = QNSet(*((i,) for i in range(SIZE)))
        big_to_small = (
            [frozenset(i) for i in combinations(range(SIZE), 4)]
            + [frozenset(i) for i in combinations(range(SIZE), 3)]
            + [frozenset(i) for i in combinations(range(SIZE), 2)]
            + [frozenset(i) for i in combinations(range(SIZE), 1)]
        )

        bs_tree = PIETree.from_primitives(prims)
        for i in big_to_small:
            bs_tree.expand(i)
        self.assertTrue(bs_tree.is_complete())

        sb_tree = PIETree.from_primitives(prims)
        for i in reversed(big_to_small):
            sb_tree.expand(i)
        self.assertTrue(sb_tree.is_complete())

        self.assertTrue(PIETree.is_equal(bs_tree, sb_tree, check_coef=True))

        # Let's try to re-add a node to the tree
        bs_tree.expand(frozenset({0, 1, 2, 3}))

        self.assertTrue(PIETree.is_equal(bs_tree, sb_tree, check_coef=True))


class PIETestCases(unittest.TestCase):
    def assert_MBE_methods(self, n: int, o: int, r=0):
        primary_legacy = [{i} for i in range(n)]

        if r:

            def keeper(i: quickNode, r=7) -> bool:
                i_s = set.union(*i)
                return (max(i_s) - min(i_s)) <= r

            aux_legacy = [
                set.union(*i) for i in combinations(primary_legacy, o) if keeper(i, r)
            ]
        else:
            aux_legacy = [set.union(*i) for i in combinations(primary_legacy, o)]

        primary = [frozenset(i) for i in primary_legacy]
        aux = [frozenset(i) for i in aux_legacy]

        self.compare_methods(aux, primary, n, o)

    def compare_methods(self, aux, primaries, n, o):
        plan = mk_quickPlan(aux)

        tree_graph = PIETree(primaries)
        tree_desc = PIETree(primaries)
        tree_mbe = PIETree(primaries)
        for a in aux:
            tree_graph.expand(a, method="graph")
            tree_desc.expand(a, method="descendants")
            tree_mbe.expand(a, method="mbe")

        self.assertTrue(tree_graph.mbe_primaries)
        self.assertSetEqual(tree_graph.primaries, set(primaries))
        self.assertEqual(tree_graph.primitives, collect_primitives(primaries))

        for tree in [tree_graph, tree_desc]:
            tree_plan = tree_graph.to_quickPIE()
            # Remove zero items keys
            plan = {n: c for n, c in plan.items() if c != 0}

            self.assertSetEqual(set(plan.keys()), set(tree_plan.keys()))
            for n in plan.keys():
                self.assertEqual(plan[n], tree_plan[n])

    def test_MBE_higher_order(self):
        """
        Tests the case where the number of primary fragment is less
        than the requested order.

        The chosen behavior is to merge all all nodes into a single supernode instead
        of throwing an error. For example, if there are two primary nodes and the order
        is three, these two nerds will be merged
        """
        tree = PIETree.from_MBE_primary_frags(QNList({0}, {1}), 3)
        self.assertSetEqual(
            {(mk_key(n), d["coef"]) for n, d in tree},
            {((0,), 0), ((1,), 0), ((0, 1), 1)},
        )

        tree = PIETree.from_MBE_primary_frags(QNList({0}, {1}, {2}), 3)
        self.assertSetEqual(
            {(mk_key(n), d["coef"]) for n, d in tree},
            {((0,), 0), ((1,), 0), ((2,), 0), ((0, 1, 2), 1)},
        )

    def test_MBE_aux_nodes(self):
        for i in range(4, 9):
            self.assert_MBE_methods(i, 3)
        for i in range(5, 8):
            self.assert_MBE_methods(i, 4)
        for i in range(10, 12):
            self.assert_MBE_methods(i, 4, 6)
