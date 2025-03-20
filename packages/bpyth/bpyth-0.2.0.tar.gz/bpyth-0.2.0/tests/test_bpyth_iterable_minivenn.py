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


class TestMinivenn:
    def test_minivenn_normal_dict(self):
        assert minivenn({1, 2, 3}, {3, 4, 5}) == {
            'left_only': {1, 2},
            'both': {3},
            'right_only': {4, 5},
        }
        assert minivenn({1, 2, 3}, {4, 5, 6}) == {
            'left_only': {1, 2, 3},
            'both': set(),
            'right_only': {4, 5, 6},
        }
        assert minivenn({1, 2, 3}, {1, 2, 3}) == {
            'left_only': set(),
            'both': {1, 2, 3},
            'right_only': set(),
        }
        assert minivenn(set(), set()) == {
            'left_only': set(),
            'both': set(),
            'right_only': set(),
        }

    def test_minivenn_empty_dict(self):
        assert minivenn({1, 2, 3}, set()) == {
            'left_only': {1, 2, 3},
            'both': set(),
            'right_only': set(),
        }
        assert minivenn(set(), {1, 2, 3}) == {
            'left_only': set(),
            'both': set(),
            'right_only': {1, 2, 3},
        }

    def test_minivenn_normal_count(self):
        assert minivenn({1, 2, 3}, {3, 4, 5}, format='count') == {
            'left_only': 2,
            'both': 1,
            'right_only': 2,
        }
        assert minivenn({1, 2, 3}, {4, 5, 6}, format='count') == {
            'left_only': 3,
            'both': 0,
            'right_only': 3,
        }
        assert minivenn({1, 2, 3}, {1, 2, 3}, format='count') == {
            'left_only': 0,
            'both': 3,
            'right_only': 0,
        }
        assert minivenn(set(), set(), format='count') == {
            'left_only': 0,
            'both': 0,
            'right_only': 0,
        }

    def test_minivenn_empty_count(self):
        assert minivenn({1, 2, 3}, set(), format='count') == {
            'left_only': 3,
            'both': 0,
            'right_only': 0,
        }
        assert minivenn(set(), {1, 2, 3}, format='count') == {
            'left_only': 0,
            'both': 0,
            'right_only': 3,
        }

    def test_minivenn_normal_list(self):
        assert minivenn({1, 2, 3}, {3, 4, 5}, format='list') == [
            {1, 2},
            {3},
            {4, 5},
        ]
        assert minivenn({1, 2, 3}, {4, 5, 6}, format='list') == [
            {1, 2, 3},
            set(),
            {4, 5, 6},
        ]
        assert minivenn({1, 2, 3}, {1, 2, 3}, format='list') == [
            set(),
            {1, 2, 3},
            set(),
        ]
        assert minivenn(set(), set(), format='list') == [
            set(),
            set(),
            set(),
        ]

    def test_minivenn_empty_list(self):
        assert minivenn({1, 2, 3}, set(), format='list') == [
            {1, 2, 3},
            set(),
            set(),
        ]
        assert minivenn(set(), {1, 2, 3}, format='list') == [
            set(),
            set(),
            {1, 2, 3},
        ]

    def test_minivenn_print(self, capsys):
        minivenn({1, 2, 3}, {3, 4, 5}, format='print')
        captured = capsys.readouterr()
        assert captured.out == "left_only:  {1, 2}\nboth:       {3}\nright_only: {4, 5}\n\n"
        assert minivenn({1, 2, 3}, {3, 4, 5}, format='print') is None


    def test_minivenn_invalid_format(self):
        with pytest.raises(ValueError):
            minivenn({1, 2, 3}, {3, 4, 5}, format='invalid')




