import pytest
import string
from bpyth.bpyth_string import superstrip, remove_words, remove_dupwords, longest_substr, random_str


@pytest.mark.jetzt
class TestString:


    def test_superstrip(self):
        assert superstrip("  abc  ") == "abc"
        assert superstrip("abc\tdef") == "abc def"
        assert superstrip("abc   def") == "abc def"
        assert superstrip("  \u00A0abc\u00A0  ") == "abc"
        assert superstrip("abc") == "abc"
        assert superstrip("") == ""
        assert superstrip("   ") == ""
        assert superstrip("\t\n") == ""
        assert superstrip(" \u00A0 \u00A0 ") == ""
        assert superstrip(" \u00A0 \u00A0 abc \u00A0 \u00A0 ") == "abc"
        assert superstrip(" \t abc \n def \r ") == "abc def"
        assert superstrip("  \u2003abc\u2003  ") == "abc"  # En quad
        assert superstrip("  \u2009abc\u2009  ") == "abc"  # Thin space


    def test_remove_words(self):
        assert remove_words("Dies ist ein Test", ["ist", "ein"]) == "Dies Test"
        assert remove_words("Dies ist ein Test.", ["ist", "ein"]) == "Dies Test."
        assert remove_words("Dies ist ein Test.", ["ist", "ein", "."]) == "Dies Test."
        assert remove_words("ist Dies ist ein Test.", ["ist", "ein", "."]) == "Dies Test."
        assert remove_words("Dies ist ein Test.", []) == "Dies ist ein Test."
        assert remove_words("", ["ist", "ein"]) == ""
        assert remove_words("   ", ["ist", "ein"]) == "   "
        assert remove_words("Dies ist ein Test.", ["ist", "ein", "Test"]) == "Dies ."


    def test_remove_dupwords(self):
        assert remove_dupwords("abc def abc ghi") == "abc def ghi"
        assert remove_dupwords("abc def abc ghi abc", sep=" ") == "abc def ghi"
        assert remove_dupwords("abc,def,abc,ghi", sep=",") == "abc,def,ghi"
        assert remove_dupwords("abc def abc def", sep=" ") == "abc def"
        assert remove_dupwords("abc", sep=" ") == "abc"
        assert remove_dupwords("", sep=" ") == ""
        assert remove_dupwords("   ", sep=" ") == ""
        assert remove_dupwords("abc def abc def abc", sep=" ") == "abc def"
        assert remove_dupwords("abc def abc def abc ", sep=" ") == "abc def "

        assert remove_dupwords("abc def abc def abc def", sep=" ") == "abc def"
        assert remove_dupwords("abc,def,abc,def,abc,def", sep=",") == "abc,def"
        assert remove_dupwords("abc def ghi jkl abc def ghi jkl", sep=" ") == "abc def ghi jkl"
        assert remove_dupwords("abc_def_ghi_jkl_abc_def_ghi_jkl", sep="_") == "abc_def_ghi_jkl"


    def test_longest_substr(self):
        assert longest_substr(["abcdef", "abcghi", "abcklm"]) == "abc"
        assert longest_substr(["qabcdef", "rabcghi", "sabcklm"]) == "abc"
        assert longest_substr(["abcdef", "xyz"]) == ""
        assert longest_substr(["abcdef"]) == ""
        assert longest_substr([]) == ""
        assert longest_substr(["abc", "abcd", "abcde"]) == "abc"
        assert longest_substr(["abc", "xyz", "def"]) == ""
        assert longest_substr(["", "abc", "def"]) == ""
        assert longest_substr(["abc", "", "def"]) == ""
        assert longest_substr(["abc", "def", ""]) == ""
        assert longest_substr(["abc", "abc", "abc"]) == "abc"

        assert longest_substr(["abcdefg", "abcghi", "abcklm"]) == "abc"
        assert longest_substr(["abcdefg", "abcghi", "abcklm", "abc"]) == "abc"
        assert longest_substr(["abcdefg", "abcghi", "abcklm", "abcd"]) == "abc"
        assert longest_substr(["abcdefg", "abcghi", "abcklm", "ab"]) == "ab"
        assert longest_substr(["abcdefg", "abcghi", "abcklm", "a"]) == "a"
        assert longest_substr(["abcdefg", "abcghi", "abcklm", ""]) == ""
        assert longest_substr(["abcdefg", "abcghi", "abcklm", "xyz"]) == ""
        assert longest_substr(["abcdefg", "abcghi", "abcklm", "abcxyz"]) == "abc"


    def test_random_str(self):
        # Standardfall: size=10, keine size_min/size_max
        assert len(random_str()) == 10
        assert all(c in string.ascii_letters for c in random_str())

        # size angegeben
        assert len(random_str(size=5)) == 5
        assert all(c in string.ascii_letters for c in random_str(size=5))

        # mix angegeben
        assert all(c in "01" for c in random_str(mix="01"))
        assert all(c in string.ascii_lowercase for c in random_str(mix=string.ascii_lowercase))
        assert all(c in string.digits for c in random_str(mix=string.digits))
        assert all(c in string.punctuation for c in random_str(mix=string.punctuation))
        assert all(
            c in string.ascii_letters + string.digits for c in random_str(mix=string.ascii_letters + string.digits))

        # size_min und size_max angegeben
        assert len(random_str(size_min=3, size_max=7)) >= 3
        assert len(random_str(size_min=3, size_max=7)) <= 7
        assert all(c in string.ascii_letters for c in random_str(size_min=3, size_max=7))
        assert all(c in "01" for c in random_str(size_min=3, size_max=7, mix="01"))

        # size_min und size_max gleich
        assert len(random_str(size_min=3, size_max=3)) == 3
        assert len(random_str(size_min=1, size_max=1)) == 1

        # size_max = 0
        assert len(random_str(size_min=0, size_max=0)) == 0
        assert len(random_str(size_min=-2)) == 0
        assert len(random_str(size_max=-2)) == 0
        assert len(random_str(size=-2)) == 0
        assert random_str(size_min=0, size_max=0) == ""

        # size_min und size_max, size wird ignoriert
        assert len(random_str(size=100, size_min=3, size_max=7)) >= 3
        assert len(random_str(size=100, size_min=3, size_max=7)) <= 7

        # nur size_min angegeben
        assert len(random_str(size_min=5)) == 5
        assert all(c in string.ascii_letters for c in random_str(size_min=5))

        # nur size_max angegeben
        assert len(random_str(size_max=5)) == 5
        assert all(c in string.ascii_letters for c in random_str(size_max=5))

