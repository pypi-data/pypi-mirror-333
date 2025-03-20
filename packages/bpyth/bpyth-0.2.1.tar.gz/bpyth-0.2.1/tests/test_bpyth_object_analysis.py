import pytest
from bpyth.bpyth_object_analysis import stype, rtype, shape, has_shape, memory_consumption

class TestStype:
    def test_stype_normal(self):
        assert stype(1) == "int"
        assert stype("abc") == "str"
        assert stype([1, 2, 3]) == "list"
        assert stype((1, 2, 3)) == "tuple"
        assert stype({1, 2, 3}) == "set"
        assert stype({"a": 1, "b": 2}) == "dict"
        assert stype(1.0) == "float"
        assert stype(True) == "bool"
        assert stype(None) == "NoneType"
        assert stype(b"abc") == "bytes"



class TestRtype:
    def test_rtype_normal(self):
        assert rtype(1) == ("int",)
        assert rtype("abc") == ("str",)
        assert rtype([1, 2, 3]) == ("list", "int")
        assert rtype([[1, 2], [3, 4]]) == ("list", "list", "int")
        assert rtype((1, 2, 3)) == ("tuple", "int")
        assert rtype(((1, 2), (3, 4))) == ("tuple", "tuple", "int")
        assert rtype({1, 2, 3}) == ("set", "int")
        assert rtype({1: 2, 3: 4}) == ("dict", "int")
        assert rtype(1.0) == ("float",)
        assert rtype(True) == ("bool",)
        assert rtype(None) == ("NoneType",)
        assert rtype(b"abc") == ("bytes",)
        assert rtype({b"abc", b"ac", }) == ("set","bytes")

    def test_rtype_mixed(self):
        assert rtype([1, "a", 2]) == ("list", "int")
        assert rtype([[1, "a"], [2, "b"]]) == ("list", "list", "int")
        assert rtype([1, [2, "a"]]) == ("list", "int")
        assert rtype([1, [2, "a"], 3]) == ("list", "int")


    def test_rtype_more_types(self):
        assert rtype([1, (2, 3)]) == ("list", "int")
        assert rtype([1, {2, 3}]) == ("list", "int")
        assert rtype([1, {2: 3}]) == ("list", "int")
        assert rtype([1, b"abc"]) == ("list", "int")
        assert rtype([1, [2, b"abc"]]) == ("list", "int")
        assert rtype([1, [2, {3: 4}]]) == ("list", "int")
        assert rtype([1, [2, {3, 4}]]) == ("list", "int")
        assert rtype([1, [2, (3, 4)]]) == ("list", "int")

    def test_rtype_dict(self):
        assert rtype({"a": 1, "b": 2}) == ("dict", "int")
        assert rtype({}) == ("dict",)
        assert rtype({"a": [1, 2], "b": [3, 4]}) == ("dict", "list", "int")

    def test_rtype_notebook_cases(self):
        # 1 Dimension
        obj_4 = ('abcde', 'grfer', 'btjqw', 'bqwer')
        assert rtype(obj_4) == ('tuple', 'str')

        # shit
        obj_shit = [[]]
        assert rtype(obj_shit) == ('list', 'list')

        # shit
        obj_shit = [[1]]
        assert rtype(obj_shit) == ('list', 'list', 'int')

        # 1 Dimension, heterogener Inhalt: Nur das erste Element wird untersucht!
        obj_3 = ('ICH WERDE UNTERSUCHT', -77, -99)
        assert rtype(obj_3) == ('tuple', 'str')

        # 2 Dimensionen
        obj_43 = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        assert rtype(obj_43) == ('list', 'list', 'int')
        assert rtype(tuple(obj_43)) == ('tuple', 'list', 'int')

        # 3 Dimensionen
        obj_533 = [
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
        ]
        assert rtype(obj_533) == ('list', 'list', 'list', 'int')

        # Anderer Datentyp
        obj_45 = [list('abcde'), list('grfer'), list('btjqw'), list('bqwer')]
        assert rtype(obj_45) == ('list', 'list', 'str')

        # 2 Dimensionen mit leeren Listen
        obj_53 = [
            [[], [], []],
            [[], [], []],
            [[], [], []],
            [[], [], []],
            [[], [], []],
        ]
        assert rtype(obj_53) == ('list', 'list', 'list')

        dict_3 = {'A': 1,
                  'B': 2,
                  'C': 3,
                  }

        assert rtype(dict_3) == ('dict', 'int')

        dict_54 = {'A': [1, 4, 5, 6],
                   'B': [2, 4, 5, 6],
                   'C': [3, 4, 0, 9],
                   'D': [4, 4, 5, 9],
                   'E': [5, 4, 5, 6],
                   }
        assert rtype(dict_54) == ('dict', 'list', 'int')

        dict_54b = {'A': (1, 4, 5, 6),
                    'B': (2, 4, 5, 6),
                    'C': (3, 4, 0, 9),
                    'D': (4, 4, 5, 9),
                    'E': (5, 4, 5, 6),
                    }
        assert rtype(dict_54b) == ('dict', 'tuple', 'int')

        dict_32 = {'A': ((), (),),
                   'B': ((), (),),
                   'C': ((), (),),
                   }
        assert rtype(dict_32) == ('dict', 'tuple', 'tuple')





class TestShape:
    def test_shape_normal(self):
        assert shape(1) == ()
        assert shape("abc") == ()
        assert shape(b"abc") == (3,)
        assert shape([1, 2, 3]) == (3,)
        assert shape([[1, 2], [3, 4]]) == (2, 2)
        assert shape([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]) == (2, 2, 2)
        assert shape((1, 2, 3)) == (3,)
        assert shape({1, 2, 3}) == (3,)
        assert shape({1: 2, 3: 4}) == (2,)
        assert shape({None, True, False, True}) == (3,)
        assert shape(((1, 2), (3, 4))) == (2, 2)
        assert shape(1.0) == ()
        assert shape(True) == ()
        assert shape(None) == ()

    def test_shape_dict(self):
        assert shape({"a": 1, "b": 2}) == (2,)
        assert shape({}) == ()
        assert shape({"a": [1, 2], "b": [3, 4]}) == (2,2)

    def test_shape_mixed(self):
        assert shape([1, "a", 2]) == (3,)
        assert shape([[1, "a"], [2, "b"]]) == (2, 2)
        with pytest.raises(ValueError):
            shape([1, [2, "a"]])
        with pytest.raises(ValueError):
            shape([1, [2, "a"], 3])

    def test_shape_notebook_cases(self):
        # 0 Dimensionen
        assert shape('jjj') == tuple()
        assert shape(123) == tuple()
        assert shape(None) == tuple()
        assert shape([]) == tuple()
        assert shape({}) == tuple()

        # 1 Dimension
        obj_4 = ('abcde', 'grfer', 'btjqw', 'bqwer')
        assert shape(obj_4) == (4,)

        # shit
        obj_shit = [[]]
        assert shape(obj_shit) == (1,)

        # shit
        obj_shit = [[1]]
        assert shape(obj_shit) == (1, 1)

        # 1 Dimension, heterogener Inhalt: Nur das erste Element wird untersucht!
        obj_3 = ('ICH WERDE UNTERSUCHT', -77, -99)
        assert shape(obj_3) == (3,)

        # 2 Dimensionen
        obj_43 = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        assert shape(obj_43) == (4, 3)
        assert shape(tuple(obj_43)) == (4, 3)

        # 3 Dimensionen
        obj_533 = [
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
        ]
        assert shape(obj_533) == (5, 3, 3)

        # Anderer Datentyp
        obj_45 = [list('abcde'), list('grfer'), list('btjqw'), list('bqwer')]
        assert shape(obj_45) == (4, 5)

        # 2 Dimensionen mit leeren Listen
        obj_53 = [
            [[], [], []],
            [[], [], []],
            [[], [], []],
            [[], [], []],
            [[], [], []],
        ]
        assert shape(obj_53) == (5, 3)

        dict_3 = {'A': 1,
                  'B': 2,
                  'C': 3,
                  }

        assert shape(dict_3) == (3,)

        dict_54 = {'A': [1, 4, 5, 6],
                   'B': [2, 4, 5, 6],
                   'C': [3, 4, 0, 9],
                   'D': [4, 4, 5, 9],
                   'E': [5, 4, 5, 6],
                   }
        assert shape(dict_54) == (5,4)

        dict_54b = {'A': (1, 4, 5, 6),
                    'B': (2, 4, 5, 6),
                    'C': (3, 4, 0, 9),
                    'D': (4, 4, 5, 9),
                    'E': (5, 4, 5, 6),
                    }
        assert shape(dict_54b) == (5,4)

        dict_32 = {'A': ((), (),),
                   'B': ((), (),),
                   'C': ((), (),),
                   }
        assert shape(dict_32) == (3,2)





class TestHasShape:
    def test_has_shape_normal(self):
        assert has_shape(1) == False
        assert has_shape("abc") == False
        assert has_shape([1, 2, 3]) == True
        assert has_shape([[1, 2], [3, 4]]) == True
        assert has_shape((1, 2, 3)) == True
        assert has_shape(((1, 2), (3, 4))) == True
        assert has_shape({1, 2, 3}) == True
        assert has_shape({1: 2, 3: 4}) == True
        assert has_shape(1.0) == False
        assert has_shape(True) == False
        assert has_shape(None) == False
        assert has_shape(b"abc") == True


    def test_has_shape_mixed(self):
        assert has_shape([1, "a", 2]) == True
        assert has_shape([[1, "a"], [2, "b"]]) == True
        assert has_shape([1, [2, "a"]]) == True
        assert has_shape([1, [2, "a"], 3]) == True

    def test_has_shape_more_types(self):
        assert has_shape([1, (2, 3)]) == True
        assert has_shape([1, {2, 3}]) == True
        assert has_shape([1, {2: 3}]) == True
        assert has_shape([1, b"abc"]) == True
        assert has_shape([1, [2, b"abc"]]) == True
        assert has_shape([1, [2, {3: 4}]]) == True
        assert has_shape([1, [2, {3, 4}]]) == True
        assert has_shape([1, [2, (3, 4)]]) == True

    def test_has_shape_dict(self):
        assert has_shape({"a": 1, "b": 2}) == True
        assert has_shape({}) == False
        assert has_shape({"a": [1, 2], "b": [3, 4]}) == True
        assert has_shape({"a": [1, 2], "b": 3}) == True





