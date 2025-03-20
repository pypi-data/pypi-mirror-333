import pytest
from collections import Counter
from bpyth.bpyth_iterable import (
    minivenn,
    flatten,
    remove_dups,
    sort_by_priority_list,
    cut_counter,
    ranking_from_counter,
)


class TestFlatten:
    def test_flatten_normal(self):
        assert list(flatten([[1, 2], [3, 4]])) == [1, 2, 3, 4]
        assert list(flatten([1, [2, [3, 4]]])) == [1, 2, 3, 4]
        assert list(flatten([1, 2, 3])) == [1, 2, 3]
        assert list(flatten([])) == []
        assert list(flatten([[1, 2], [3, [4, 5]]])) == [1, 2, 3, 4, 5]

    def test_flatten_mixed(self):
        assert list(flatten([1, [2, 3], "abc", [4, 5]])) == [1, 2, 3, "abc", 4, 5]

    def test_flatten_more_types(self):
        assert list(flatten([(1, 2), [3, 4]])) == [1, 2, 3, 4]  # Tupel
        assert list(flatten([{1, 2}, {3, 4}])) == [1, 2, 3, 4]  # Sets
        assert list(flatten([{1: 2}, {3: 4}])) == [1, 3]  # Dictionaries (nur Keys)
        assert list(flatten([b"abc", b"def"])) == [b"abc", b"def"]  # Bytes
        assert list(flatten([1, (2, [3, {4, 5}]), "abc", b"def"])) == [1, 2, 3, 4, 5, "abc", b"def"] # Alles gemischt
        assert list(flatten([1, (2, [3, {4, 5}]), "abc", b"def", {6:7}])) == [1, 2, 3, 4, 5, "abc", b"def", 6] # Alles gemischt mit Dictionary

    def test_flatten_none(self):
        assert list(flatten([None])) == [None]
        assert list(flatten([[None]])) == [None]
        assert list(flatten([1, [2, None]])) == [1, 2, None]






class TestRemoveDups:
    def test_remove_dups_normal(self):
        assert remove_dups([1, 2, 2, 3, 4, 4, 4, 5]) == [1, 2, 3, 4, 5]
        assert remove_dups([1, 1, 1, 1]) == [1]
        assert remove_dups([]) == []
        assert remove_dups([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
        assert remove_dups([1, 2, 3, 2, 1, 4, 5, 4]) == [1, 2, 3, 4, 5]

    def test_remove_dups_mixed(self):
        assert remove_dups([1, "a", 2, "a", 3, 1]) == [1, "a", 2, 3]

    def test_remove_dups_more_types(self):
        assert remove_dups([1, 1.0, 1.0, "1", "1", True, True, False, False, None, None]) == [1, 1.0, "1", True, False, None]
        assert remove_dups([1, (1,2), (1,2), [1,2], [1,2], {1,2}, {1,2}]) == [1, (1,2), [1,2], {1,2}]

    def test_remove_dups_none(self):
        assert remove_dups([None, None, None]) == [None]
        assert remove_dups([1, None, None, 2]) == [1, None, 2]
        assert remove_dups([None, 1, 2, None]) == [None, 1, 2]




class TestSortByPriorityList:
    def test_sort_by_priority_list_normal(self):
        assert sort_by_priority_list([1, 2, 3, 4, 5], [3, 1]) == [3, 1, 2, 4, 5]
        assert sort_by_priority_list([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == [5, 4, 3, 2, 1]
        assert sort_by_priority_list([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
        assert sort_by_priority_list([1, 2, 3, 4, 5], []) == [1, 2, 3, 4, 5]
        assert sort_by_priority_list([], [1, 2, 3]) == []
        assert sort_by_priority_list([1, 2, 3, 4, 5], [6, 7]) == [1, 2, 3, 4, 5]

    def test_sort_by_priority_list_mixed(self):
        assert sort_by_priority_list([1, "a", 2, "b", 3], ["b", 1]) == ["b", 1, "a", 2, 3]
        assert sort_by_priority_list([1, "a", 2, "b", 3], ["b", 1, 2]) == ["b", 1, 2, "a", 3]
        assert ''.join(sort_by_priority_list(list(' Lorem ipsum dolor sit amet'), list('aeiou'))) == 'aeeiiooou Lrm psm dlr st mt'






class TestCutCounter:
    def test_cut_counter_normal(self):
        assert cut_counter(Counter([1, 1, 1, 2, 2, 3, 4, 4, 4, 4]), 10) == Counter({4: 4, 1: 3, 2: 2})
        assert cut_counter(Counter([1, 1, 1, 2, 2, 3, 4, 4, 4, 4]), 20) == Counter({4: 4, 1: 3 })
        assert cut_counter(Counter([1, 1, 1, 2, 2, 3, 4, 4, 4, 4]), 30) == Counter({4: 4 })



class TestRankingFromCounter:
    def test_ranking_from_counter_normal(self):
        c = Counter('Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.')
        assert ranking_from_counter(c) == {' ': 0,
                                            'e': 1,
                                            'o': 2,
                                            't': 3,
                                            'a': 4,
                                            'r': 5,
                                            'm': 6,
                                            'u': 7,
                                            'i': 8,
                                            's': 9,
                                            'd': 10,
                                            'l': 11,
                                            'n': 12,
                                            'p': 13,
                                            'c': 14,
                                            ',': 15,
                                            'v': 16,
                                            'g': 17,
                                            'y': 18,
                                            'b': 19,
                                            '.': 20,
                                            'L': 21,
                                            'q': 22,
                                            'A': 23,
                                            'j': 24}

    def test_ranking_from_counter_empty(self):
        assert ranking_from_counter(Counter()) == {}

    def test_ranking_from_counter_single(self):
        assert ranking_from_counter(Counter([1])) == {1: 0}

    def test_ranking_from_counter_mixed(self):
        assert ranking_from_counter(Counter([1, 1, 1, "a", "a", "b", "c", "c", "c", "c"])) == {"c": 0, 1: 1, "a": 2, "b": 3}