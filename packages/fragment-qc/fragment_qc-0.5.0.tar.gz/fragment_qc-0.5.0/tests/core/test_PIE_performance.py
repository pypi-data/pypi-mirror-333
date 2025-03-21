#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#

# Test Stuite to Benchmark PIE Implementations against each other.
# Only modest correctness tests will be done (quick_PIE will be used for this)
#
# PIE_v1: QuickPIE (dictionaty based)
# PIE_v2: PIELegacy (QuickPIE + Manual tree)
# PIE_v3: PIETree (NetworkX-based implementation)
# PIE_v4: rPIETree (RustworkX-based implementation)
# PIE_v5: rPIETree_graph (uses graph intersections method)
# PIE_v6: rPIETree_descendents (uses primitive descendants method)

import gc
import unittest
from itertools import combinations, product
from os import environ
from random import randint, seed
from time import process_time
from typing import Iterable

from fragment.core.legacy_PIE import PIEPlan
from fragment.core.legacy_PIETree import make_PIETree
from fragment.core.PIETree import PIETree
from fragment.core.quickPIE import mk_quickPlan
from fragment.core.rPIETree import PIETree as rPIETree


def stress_test_V1(
    primaries: Iterable[set[int]], aux: Iterable[set[int]]
) -> tuple[set[tuple[frozenset[int], int]], float]:
    """Creates a quickPlan dictionary

    This is our reference implementation; however additionas are quadratic
    """
    gc.collect()
    start_time = process_time()

    # primaries is ignored
    plan = mk_quickPlan(aux)

    time = process_time() - start_time

    return {(k, c) for k, c in plan.items() if c != 0}, time


def stress_test_V2(
    primaries: Iterable[set[int]], aux: Iterable[set[int]]
) -> tuple[set[tuple[frozenset[int], int]], float]:
    """
    Creates a PIEPlan and then creates a classic PIETree


    """
    gc.collect()
    start_time = process_time()

    # primaries is ignored
    plan = PIEPlan(aux)
    G = make_PIETree(plan, primaries)

    time = process_time() - start_time

    return {
        (frozenset(n), d["coef"])
        for n, d in G.nodes(data=True)
        if n != 0 and d["coef"] != 0
    }, time


def stress_test_V3(
    primaries: Iterable[set[int]], aux: Iterable[set[int]]
) -> tuple[set[tuple[frozenset[int], int]], float]:
    """Test using PIETree (NetworkX)"""
    gc.collect()
    start_time = process_time()

    tree = PIETree.from_primaries(primaries=primaries)
    for a in aux:
        tree.expand(a)

    time = process_time() - start_time
    return {(n, d["coef"]) for n, d in tree if d["coef"] != 0}, time


def stress_test_V4(
    primaries: Iterable[set[int]], aux: Iterable[set[int]]
) -> tuple[set[tuple[frozenset[int], int]], float]:
    """Test with the rPIETree code (Rust)"""
    gc.collect()
    start_time = process_time()

    tree = rPIETree(primaries=primaries)
    for a in aux:
        tree.expand(a)

    time = process_time() - start_time
    return {(n, d["coef"]) for n, d in tree if d["coef"] != 0}, time


def stress_test_V5(
    primaries: Iterable[set[int]], aux: Iterable[set[int]]
) -> tuple[set[tuple[frozenset[int], int]], float]:
    """Test with the rPIETree code (Rust)"""
    gc.collect()
    start_time = process_time()

    tree = rPIETree(primaries=primaries)
    for a in aux:
        tree.expand(a, method="descendants")

    time = process_time() - start_time
    return {(n, d["coef"]) for n, d in tree if d["coef"] != 0}, time


def stress_test_V6(
    primaries: Iterable[set[int]], aux: Iterable[set[int]]
) -> tuple[set[tuple[frozenset[int], int]], float]:
    """Test with the rPIETree code (Rust)"""
    gc.collect()
    start_time = process_time()

    tree = rPIETree(primaries=primaries)
    for a in aux:
        tree.expand(a, method="graph")

    time = process_time() - start_time
    return {(n, d["coef"]) for n, d in tree if d["coef"] != 0}, time


def stress_test_V7(
    primaries: Iterable[set[int]], aux: Iterable[set[int]]
) -> tuple[set[tuple[frozenset[int], int]], float]:
    """Test with the rPIETree code (Rust)"""
    gc.collect()
    start_time = process_time()

    tree = rPIETree(primaries=primaries)
    for a in aux:
        tree.expand(a, method="mbe")

    time = process_time() - start_time
    return {(n, d["coef"]) for n, d in tree if d["coef"] != 0}, time


# TODO: Make this consistent with other optional tests
class PIETestCases(unittest.TestCase):
    test_methods = [
        ("quickPIE", stress_test_V1),
        # ("PIELegacy", stress_test_V2),
        ("PIETree", stress_test_V3),
        ("rPIETree", stress_test_V4),
        ("rPIETree_desc", stress_test_V5),
        ("rPIETree_graph", stress_test_V6),
        # ("rPIETree_mbe", stress_test_V7),
    ]

    def MBE_frags(self, N_f: int, n: int, r=0):
        """
        Creates array of primary non-overlapping fragments

        Creates higher order combinations with an optional screening procedure
        """
        # Create primary fragments
        primary = [frozenset({i}) for i in range(N_f)]

        # Create auxiliary fragments
        aux = [frozenset.union(*i) for i in combinations(primary, n)]

        # Create screened or unscreened auxiliary fragments
        if r:
            # Screening checks if the min index or max index are within r of each other
            # Default is r = 7
            def keeper(i: frozenset[int]) -> bool:
                return (max(i) - min(i)) <= r

            aux = [a for a in aux if keeper(a)]

        return primary, aux

    def GMBE_frags(self, N_f: int, n: int):
        """
        Creates rondomly overlapping primary fragments

        Generates higher-order fragments and compresses up to ensure these fragments don't
        contain subsets of each other
        """
        primary = [frozenset({randint(0, N_f) for i in range(3)}) for i in range(N_f)]

        aux = [frozenset.union(*i) for i in combinations(primary, n)]
        return primary, aux

    def perf_test(self, method: str, N_f: int, n: int, r: int = 0):
        if method == "GMBE":
            primary, aux = self.GMBE_frags(N_f, n)
        else:
            primary, aux = self.MBE_frags(N_f, n, r=r)

        ref = None

        for name, test_fn in self.test_methods:
            data, time = test_fn(primary, aux)
            if ref is None:
                ref = data
            else:
                self.assertSetEqual(ref, data)

            print(name, method, n, r, N_f, len(data), time, sep=", ", flush=True)

    @unittest.skipIf("PERF_TEST" not in environ, "Not running performance check")
    def test_performance_quick(self):
        seed(314)
        self.perf_test("GMBE", 16, 4, r=0)

    @unittest.skipIf("PERF_TEST" not in environ, "Not running performance check")
    def test_performance(self):
        print("method", "test", "n", "r", "N_f", "fragments", "time", sep=", ")

        # Test raw MBE
        for n, N_f in product(range(4, 7), range(6, 16, 1)):
            if N_f <= n:
                continue
            self.perf_test("MBE", N_f, n, r=0)

        # Test screened MBE
        for r, n, N_f in product(range(8, 12, 2), range(5, 8), range(10, 35, 5)):
            if N_f <= n:
                continue
            self.perf_test("MBE", N_f, n, r=r)

        # Test GMBE
        seed(314)
        for n, N_f in product(range(3, 5), range(10, 18, 2)):
            if N_f <= n:
                continue
            self.perf_test("GMBE", N_f, n, r=0)
