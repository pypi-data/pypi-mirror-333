#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from itertools import combinations
from typing import Dict, FrozenSet, Iterable, List, Optional

from conformer.systems import System
from conformer_core.stages import FilterStack, ModStack, Stack, Stage, StageOptions
from scipy.special import binom

from fragment.core.quickPIE import compress_up
from fragment.db.models import DBView
from fragment.views import Key, KeySet, View


class FragmenterOptions(StageOptions):
    clean_zeros: bool = True # NOTE: Only implemented for aux fragmenters


class Fragmenter(Stage):
    Options = FragmenterOptions

    subsystem_mods = Stack()
    pre_mods = ModStack()
    post_mods = ModStack()


class PrimaryFragmenter(Fragmenter):
    def new_view(self, sys: System, primaries: Iterable[FrozenSet[int]]) -> View:
        sys_name = f"{self.name}({sys.name})"
        view = View.new_primary(self, primaries, name=sys_name)
        view.bind_system(sys)
        return view

    def view_from_db(self, sys: System) -> View | None:
        if not self._use_db:
            return
        if self._saved:  # Only query if this Fragmenter has been saved
            return DBView.get_view_by_originator(
                self,
                sys,
                0,  # Primary Views have order == 0
                WORLD=self._world,  # Share the Fragmenter World
                REGISTRY={
                    self.__class__.__name__: self.__class__
                },  # This shouldn't need to be accessed
            )
        return None

    def view_to_db(self, view: View) -> View:
        if not self._use_db:
            return
        DBView.add_views([view])

    def __call__(self, sys: System) -> View:
        if not sys.is_canonized:
            sys = sys.canonize()
        # Check if we have a copy in the database
        view = self.view_from_db(sys)
        if view is not None:  # Add force flag
            return view

        # sys = self.pre_mods(sys)
        view = self.fragment(sys)
        # view = self.post_mods(view)

        self.view_to_db(view)
        return view

    def fragment(self, sys: System) -> View: ...


class AuxFragmenter(Fragmenter):
    filters = FilterStack()

    def view_name(self, view: View, order: int) -> View:
        return f"{view.name}--{self.name}({order})"

    def view_from_db(self, p_view: View, order: int) -> View | None:
        if not self._use_db:
            return
        if self._saved:  # Only query if this Fragmenter has been saved
            return DBView.get_view_by_originator(
                self,
                p_view.supersystem,
                order,  # Primary Views have order == 0
                WORLD=self._world,  # Share the Fragmenter World
                REGISTRY={
                    self.__class__.__name__: self.__class__
                },  # This shouldn't need to be accessed
            )
        return None

    def view_to_db(self, view: View) -> str:
        if not self._use_db:
            return
        DBView.add_views([view])

    def combinate(self, p_view: View, order: int) -> View: ...

    def __call__(self, p_view: View, order: int) -> View:
        if p_view.supersystem is not None:
            assert p_view.supersystem.is_canonized
        view = self.view_from_db(p_view, order)
        if view:
            return view

        # p_view, order = self.pre_mods(p_view, order)
        view = self.combinate(p_view, order)
        # view = self.post_mods(view)

        if self.opts.clean_zeros:
            view.tree.clean_zeros()
        if not view.tree.is_complete():
            raise ValueError(
                f"Fragmentation scheme does not reproduce the supersystem:\n  {view.tree.count_members()}"
            )

        self.view_to_db(view)
        return view


class FullFragmenter(AuxFragmenter):
    filters = None  # There is no filtering allowed for this puppy

    def combinate(self, p_view: View, order: int) -> View:
        # Quicklky do non-overlapping fragments
        if p_view.primaries == p_view.primitives:
            view = View.new_MBE_auxiliary(
                self, p_view, order, name=self.view_name(p_view, order)
            )

        # Spend more time brute-forcing overlapping fragments :(
        else:
            view = View.new_auxiliary(
                self, p_view, order, name=self.view_name(p_view, order)
            )
            for comb in combinations(view.primaries, order):
                view.add(Key.union(*comb))

        return view


class TopDownFragmenter(AuxFragmenter):
    def combinate(self, p_view: View, order: int) -> View:
        # TODO: Implement without complete combos.
        # May be simpler and cheaper to check if fragment is in tree
        # Do the old reliable way :)
        view = View.new_auxiliary(
            self, p_view, order, name=self.view_name(p_view, order)
        )

        root_fragments = self.complete_combos(view.primaries, view, order)
        for k in compress_up(root_fragments):
            view.add(k)

        return view

    def complete_combos(
        self,
        to_add: KeySet,
        view: View,
        order: int,
        fragments: Optional[KeySet] = None,
        checked: Optional[KeySet] = None,
    ) -> KeySet:
        if fragments is None:
            fragments = KeySet()
        if checked is None:
            checked = KeySet()  # Maybe just build the view?

        # TODO: Parallelize with accessors
        for frags in combinations(to_add, order):
            key = Key.union(*frags)
            if key in checked:
                continue  # Skip. It's already there
            else:
                checked.add(key)  # Skip next time

            if order == 1:  # All first order fragments get added
                fragments.add(key)  # TODO: Why not just add it to the view?
            elif self.filters(view, frags, order)[1]:  # Filtering
                fragments.add(key)
            else:
                self.complete_combos(frags, view, order - 1, fragments, checked)

        return fragments

    # def add_fragments(self, view: View, *frags: Key) -> KeySet:
    #     order = len(frags)
    #     key = frozenset.union(*frags)

    #     if order == 1:
    #         return set(frags)

    #     # TODO: Parallelize this with accessors
    #     if filter(view, frags):  # Keep if True
    #         return set((key,))

    #     return self.complete_combos(fags, order - 1, filter)


# class BottomUpFragmenter(AuxFragmenter):
class BottomUpFragmenterLegacy(AuxFragmenter):
    """Legacy bottom up fragmenter

    Kept for reference until the new on is established.
    """

    class Options(FragmenterOptions):
        M: int = 1

    def combinate(self, p_view: View, order: int) -> View:
        """Adds nodes layer by layer.

        Only fragments with N - M parents in the tree are allowed to be added.
        For example ab + ac + bc -> abc is allowed but ab + ac -!> abc for M = 0
        """
        view = View.new_auxiliary(
            self, p_view, order=order, name=self.view_name(p_view, order)
        )
        # Congratulations! We have level one completed!
        for f in p_view.primaries:
            view.add(f)

        if order != 1:
            # Add remaining levels
            self.add_bottom_up_level(view, order, 2)
        return view

    def add_bottom_up_level(
        self,
        view: View,
        o: int,  # Target order
        m: int,  # The current level
    ) -> None:
        # TODO: Find a more efficient way to do this
        _new_hl: KeySet = set()
        new_ll_nodes = 1  # New low-level nodes
        new_hl_nodes = 1  # New high-level nodes
        MAX_ITER = 1
        _M = self.opts.M
        itr = 1

        while new_ll_nodes and new_hl_nodes and MAX_ITER >= itr:
            to_add: KeySet = set()
            to_add_missing: KeySet = set()

            # This is a brute force check. We can probably do this much more
            # efficiently with the Tree (finally, a use!)
            for com in combinations(view.primaries, m):
                # Check that all parents exist in the tree. They don't have to have
                # non-zero coefs (?) but should be there
                mc = 0
                missing = set()
                hl_key = frozenset.union(*(com))
                if hl_key in _new_hl:
                    continue  # Don't duplicate work

                skip = False
                for children in combinations(com, m - 1):
                    pk = frozenset.union(*(children))
                    if pk not in view:
                        mc += 1
                        missing.add(pk)
                        if mc > _M:
                            skip = True
                            # break

                if not skip and self.filters(view, com, m)[1]:
                    to_add_missing.update(missing)
                    to_add.add(hl_key)

            # Add the missing high-level terms and new keys
            prev_nodes = len(view)

            for k in to_add:
                view.add(k)

            new_hl_nodes = len(to_add)
            new_ll_nodes = len(view) - prev_nodes - new_hl_nodes
            _new_hl.update(to_add)  # Keep track of which HL nodes exist
            itr += 1

        # Just keep going until we have nothing left to add
        if m == o or len(_new_hl) == 0:
            return view
        else:
            return self.add_bottom_up_level(view, o, m + 1)


def primary_descendents(view: View, N: Key, k: int) -> set[frozenset[int]]:
    """Given a grandparent `N`, returns it's children (parents) which
    may be of interest for combinating
    """
    primary_order = view[N].primary_order

    # Defulat case for non-overlapping fragments
    if primary_order == k - 2:
        return {c for c in view.get_children(N) if view[c].primary_order >= k - 1}
    # With overlaps, you might spontaniously generate higher-order fragments
    elif primary_order >= (k - 1):
        return set.union(
            *(primary_descendents(view, i, k) for i in view.get_parents(N))
        )
    # Don't return low-level fragments (grand parents etc)
    else:
        # Don't consider lower-level nodes. Need to return all nodes at the k-1 level!
        return set()


class BottomUpFragmenter(AuxFragmenter):
    class Options(FragmenterOptions):
        M: int = 1

    opts: Options

    def combinate(self, p_view: View, order: int) -> View:
        """Adds nodes layer by layer.

        Only fragments with N - M parents in the tree are allowed to be added.
        For example ab + ac + bc -> abc is allowed but ab + ac -!> abc for M = 0
        """
        view = View.new_auxiliary(
            self, p_view, order=order, name=self.view_name(p_view, order)
        )
        # Congratulations! We have level one completed!
        for f in p_view.primaries:
            view.add(f)

        if order != 1:
            # Add remaining levels
            self.add_bottom_up_level(view, order, 2, [p_view.primaries])
        return view

    def add_bottom_up_level(
        self,
        view: View,
        n: int,  # Target order
        k: int,  # The current level,
        levels: List[KeySet],
    ) -> None:
        # TODO: Find a more efficient way to do this
        _M = self.opts.M
        needed = k - _M

        to_add = {}
        added = set()
        do_mbe_adds = view.tree.mbe_primaries
        for com in self.propose_bu_combs(view, n, k, levels):
            # Check that all parents exist in the tree. They don't have to have
            # non-zero coefs (?) but should be there
            num_parents = 0
            mc = 0
            hl_key = frozenset.union(*(com))

            # This block may not be necessary if propose_bu_combos is doing it's jobs
            for children in combinations(com, k - 1):
                if frozenset.union(*(children)) not in view:
                    mc += 1
                else:
                    num_parents += 1

            if num_parents >= needed:
                self.filters.submit(view, com, k)
                to_add[hl_key] = num_parents

        # Add the missing high-level terms and new keys
        for ((_v, primaries, _k), keep) in self.filters.as_completed():
            if not keep:
                continue

            x = frozenset.union(*primaries)
            added.add(x)
            if do_mbe_adds and to_add[x] == k:
                view.add(
                    x, method="mbe"
                )  # Do a quick MBE add since we know the parents exist and have coef = 1
            else:
                view.add(x)

        # Just keep going until we have nothing left to add
        if n == k or len(added) == 0:
            return
        else:
            levels.append(added)
            return self.add_bottom_up_level(view, n, k + 1, levels)

    def propose_bu_combs(
        self,
        view: View,
        n: int,  # Target order
        k: int,  # The current level
        levels: list[KeySet],  # List of fragments which have been explicitly added
    ) -> Iterable[frozenset[int]]:
        parents = levels[k - 2]  # Levels are 0-based index.
        parents_needed = k - self.opts.M

        if parents_needed <= 0:
            # No parent requirements means you just have to add combinations
            return combinations(view.primaries, k)
        elif parents_needed == 1 or k == 2:
            # NOTE: Three are no grandparents at the k=2 level!
            # If only one parent is needed, you just need extend by 1 primary!
            aux = set()  # Add to set to prevent double adding
            i = 0
            for p in parents:
                for primary in view.primaries:
                    if not primary.issubset(p):  # Extend by one primary!
                        i += 1
                        aux.add(primary.union(p))
            for x in aux:
                yield view.get_primaries(x)
        else:
            # Use parent information to whittle down the combination space.
            # NOTE: In some cases it might make more sense to use option 1 of this loop.
            counts: Dict[FrozenSet[int], int] = {}

            # Collect grand parents
            grandparents = set()
            for p in parents:
                grandparents.update(view.get_parents(p))

            # Collect pairs of parents
            for gp in grandparents:
                # for p1, p2 in combinations(view.get_children(gp), 2):
                for p1, p2 in combinations(primary_descendents(view, gp, k), 2):
                    key = p1.union(p2)

                    # COLLECT TERMS!
                    try:
                        counts[key] += 1
                    except KeyError:
                        counts[key] = 1

            # Return ones that meet our criteria
            thresh = int(binom(parents_needed, 2))
            for key, parents in counts.items():
                if parents >= thresh:
                    yield {s for s in view.get_primaries(key)}
