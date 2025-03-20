import pytest
from pathlib import Path
from prettree import list_directory

def test_basic_directory_listing(tmp_path):
    # Create a test directory structure
    dir1 = tmp_path / "dir1"
    dir1.mkdir()
    (dir1 / "file1.txt").touch()
    (dir1 / "file2.txt").touch()
    
    dir2 = tmp_path / "dir2"
    dir2.mkdir()
    (dir2 / "file3.txt").touch()
    
    result = list(list_directory(tmp_path))
    
    assert len(result) > 0
    assert str(tmp_path.absolute()) == result[0]
    assert any("dir1" in line for line in result)
    assert any("dir2" in line for line in result)
    assert any("file1.txt" in line for line in result)

def test_hidden_files(tmp_path):
    (tmp_path / ".hidden").touch()
    
    # Test without showing hidden files
    result = list(list_directory(tmp_path))
    assert not any(".hidden" in line for line in result)
    
    # Test with showing hidden files
    result = list(list_directory(tmp_path, show_hidden=True))
    assert any(".hidden" in line for line in result)

def test_max_depth(tmp_path):
    dir1 = tmp_path / "dir1"
    dir1.mkdir()
    dir2 = dir1 / "dir2"
    dir2.mkdir()
    dir3 = dir2 / "dir3"
    dir3.mkdir()
    
    result = list(list_directory(tmp_path, max_depth=1))
    assert any("dir1" in line for line in result)
    assert not any("dir3" in line for line in result) 