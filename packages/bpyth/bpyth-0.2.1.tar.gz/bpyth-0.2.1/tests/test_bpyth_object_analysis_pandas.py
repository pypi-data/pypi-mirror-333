import pytest
from bpyth.bpyth_object_analysis import stype, rtype, shape, has_shape

try:
    import pandas as pd
    pandas_not_installed = False
except ImportError:
    pandas_not_installed = True

@pytest.mark.skipif(pandas_not_installed, reason="Pandas is not installed")
class TestRtypePandas:

    def test_rtype_with_empty_series(self):
        # Teste, ob rtype mit einer leeren Pandas Series korrekt funktioniert
        data = pd.Series()
        assert rtype(data) == ("Series",)

    def test_rtype_with_empty_dataframe(self):
        # Teste, ob rtype mit einem leeren Pandas DataFrame korrekt funktioniert
        data = pd.DataFrame()
        assert rtype(data) == ("DataFrame",)


    def test_rtype_with_series(self):
        data = pd.Series([1, 2, 3])
        assert rtype(data) == ("Series", "int")
        assert True

    def test_rtype_with_dataframe_int(self):
        # Teste, ob rtype mit einem Pandas DataFrame korrekt funktioniert
        data = pd.DataFrame([[1, 2], [3, 4]])
        assert rtype(data) == ("DataFrame", "Series", "int")

    def test_rtype_with_dataframe_str(self):
        # Teste, ob rtype mit einem Pandas DataFrame, dessen Elemente Listen von Strings sind, korrekt funktioniert
        data = pd.DataFrame([["a", "b"], ["c", "d"]])
        assert rtype(data) == ("DataFrame", "Series", "str")

    def test_rtype_with_heterogeneous_dataframe(self):
        # Teste, ob rtype mit einem heterogenen Pandas DataFrame korrekt funktioniert
        data = pd.DataFrame([["a", 1, 2.0], ["b", 3, 4.0]])
        assert rtype(data) == ("DataFrame", "Series", "str")

    def test_rtype_with_dataframe_of_dictionaries(self):
        # Teste, ob rtype mit einem Pandas DataFrame, dessen Elemente Dictionaries sind, korrekt funktioniert
        data = pd.DataFrame([[{"a": 1, "b": 2}, {"c": 3, "d": 4}], [{"e": 5, "f": 6}, {"g": 7, "h": 8}]])
        assert rtype(data) == ("DataFrame", "Series", "dict", "int")

    def test_rtype_with_dataframe_of_lists(self):
        # Teste, ob rtype mit einem Pandas DataFrame, dessen Elemente Listen sind, korrekt funktioniert
        data = pd.DataFrame([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        assert rtype(data) == ("DataFrame", "Series", "list", "int")


