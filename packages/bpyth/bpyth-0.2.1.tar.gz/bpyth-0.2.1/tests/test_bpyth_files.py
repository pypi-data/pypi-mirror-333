import os
import pytest
import tempfile
import shutil  # for removing directories
from bpyth.bpyth_files import (
    dump_pickle,
    load_pickle,
    StreamFiles,
    StreamLines,
    path_join,
)


class TestDumpLoadPickle:
    def test_dump_load_pickle(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            filename = tmpfile.name
        try:
            # Test mit einem Dictionary
            data_to_dump = {"key1": "value1", "key2": 123, "key3": [1, 2, 3]}
            dump_pickle(data_to_dump, filename)
            loaded_data = load_pickle(filename)
            assert loaded_data == data_to_dump

            # Test mit einer Liste
            data_to_dump = [1, 2, 3, 4, 5]
            dump_pickle(data_to_dump, filename)
            loaded_data = load_pickle(filename)
            assert loaded_data == data_to_dump

            # Test mit einer Zahl
            data_to_dump = 123456
            dump_pickle(data_to_dump, filename)
            loaded_data = load_pickle(filename)
            assert loaded_data == data_to_dump
        finally:
            os.remove(filename)

    def test_load_pickle_file_not_found(self):
        loaded_data = load_pickle("nonexistent_file.pkl")
        assert loaded_data is None


class TestStreamFiles:
    def test_stream_files(self):
        # Erstelle ein temporäres Verzeichnis und einige Dateien
        temp_dir = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(temp_dir, "subdir"))
            with open(os.path.join(temp_dir, "file1.txt"), "w") as f:
                f.write("Test")
            with open(os.path.join(temp_dir, "subdir", "file2.txt"), "w") as f:
                f.write("Test")
            with open(os.path.join(temp_dir, "subdir", "file3.csv"), "w") as f:
                f.write("Test")

            # Teste StreamFiles
            files = list(StreamFiles(temp_dir, ".txt"))
            assert len(files) == 2
            assert os.path.join(temp_dir, "file1.txt") in files
            assert os.path.join(temp_dir, "subdir", "file2.txt") in files

        finally:
            # Räume das temporäre Verzeichnis auf
            shutil.rmtree(temp_dir)


class TestStreamLines:
    def test_stream_lines(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmpfile:
            filename = tmpfile.name
            tmpfile.write("Line 1\nLine 2\nLine 3\n")
        try:
            lines = list(StreamLines(filename))
            assert lines == ["Line 1\n", "Line 2\n", "Line 3\n"]
        finally:
            os.remove(filename)


class TestPathJoin:
    def test_path_join_normal(self):
        result = os.path.normpath(os.sep + "base" + os.sep + "path" + os.sep + "to" + os.sep + "file")
        assert path_join(os.sep + "base",                   "path" + os.sep + "to" + os.sep + "file")                    == result
        assert path_join(os.sep + "base" + os.sep,          "path" + os.sep + "to" + os.sep + "file")                    == result
        assert path_join(os.sep + "base",                   os.sep + "path" + os.sep + "to" + os.sep + "file")           == result
        assert path_join(os.sep + "base" + os.sep,          os.sep + "path" + os.sep + "to" + os.sep + "file")           == result
        assert path_join(os.sep + "base" + os.sep,          os.sep + "path" + os.sep + "to" + os.sep + "file" + os.sep ) == result
        assert path_join(os.sep + "base" + os.sep,          os.sep + "path" + os.sep + "to" + os.sep + "file" + os.sep)  == result
        assert path_join(os.sep + "base",                   "path" + os.sep + "to" + os.sep) == os.path.normpath(os.sep + "base" + os.sep + "path" + os.sep + "to")
        assert path_join(os.sep + "base",                   "path" + os.sep + ".." + os.sep + "to" + os.sep) == os.path.normpath(os.sep + "base" + os.sep + "to")
        assert path_join("C:" + os.sep + "base",            "path" + os.sep + "to" + os.sep + "file") == os.path.normpath("C:" + os.sep + "base" + os.sep + "path" + os.sep + "to" + os.sep + "file")
        assert path_join("C:" + os.sep + "base" + os.sep,   "path" + os.sep + "to" + os.sep + "file") == os.path.normpath("C:" + os.sep + "base" + os.sep + "path" + os.sep + "to" + os.sep + "file")

    def test_path_join_warn(self):
        with pytest.warns(UserWarning):
            path_join("/does/not/exist", "file.txt", test="warn")
        with pytest.warns(UserWarning):
            path_join("/base/", "/does/not/exist/file.txt", test="warn")
        with pytest.warns(UserWarning):
            path_join("does/not/exist", "file.txt", test="warn")
        with pytest.warns(UserWarning):
            path_join("does/not/exist", "/file.txt", test="warn")

    def test_path_join_raise(self):
        with pytest.raises(Exception):
            path_join("/does/not/exist", "file.txt", test="raise")
        with pytest.raises(Exception):
            path_join("/base/", "/does/not/exist/file.txt", test="raise")
        with pytest.raises(Exception):
            path_join("does/not/exist", "file.txt", test="raise")
        with pytest.raises(Exception):
            path_join("does/not/exist", "/file.txt", test="raise")
