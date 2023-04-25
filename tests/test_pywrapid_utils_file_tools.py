#!/usr/bin/python3
"""Pywrapid config tests"""

import os

import pytest

import pywrapid.utils.file_tools as module_0

# pylint: disable=redefined-outer-name, protected-access


@pytest.fixture()
def filesystem_fixture_0(tmp_path) -> str:
    """Fixture for producing file and directory structure"""
    # Top level
    path_0 = tmp_path / "test_dir_0" / "test_file_0_0"
    path_0.parent.mkdir()
    path_0.touch()
    path_0.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    path_1 = tmp_path / "test_dir_1" / "test_file_1_0"
    path_1.parent.mkdir()
    path_1.touch()
    path_1.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    single_file_0 = tmp_path / "test_file_0"
    single_file_0.touch()
    single_file_0.write_text(
        "sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    )

    single_file_1 = tmp_path / "test_file_1"
    single_file_1.touch()
    single_file_1.write_text(
        "sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    )

    # Second level
    path_2 = tmp_path / "test_dir_0" / "test_dir_0_0" / "test_file_0_0_0"
    path_2.parent.mkdir()
    path_2.touch()
    path_2.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    # Third level
    path_3 = tmp_path / "test_dir_0" / "test_dir_0_0" / "test_dir_0_0_0" / "test_file_0_0_0_0"
    path_3.parent.mkdir()
    path_3.touch()
    path_3.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    # Fourth level
    path_4 = (
        tmp_path
        / "test_dir_0"
        / "test_dir_0_0"
        / "test_dir_0_0_0"
        / "test_dir_0_0_0_0"
        / "test_file_0_0_0_0_0"
    )
    path_4.parent.mkdir()
    path_4.touch()
    path_4.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    sym_dir = tmp_path / "test_dir_1" / "test_symlink_dir"
    sym_file = tmp_path / "test_dir_1" / "test_file_1_0" / "test_symlink_file"
    if not os.path.exists(sym_dir):
        os.symlink(tmp_path / "test_dir_1", tmp_path / "test_symlink_dir")
    if not os.path.exists(sym_file):
        os.symlink(tmp_path / "test_dir_1" / "test_file_1_0", tmp_path / "test_symlink_file")

    return tmp_path


def test_is_file_readable_0() -> None:
    """Test is_file_readable function"""
    assert module_0.is_file_readable("tests/test_conf_ok.yml") is True
    assert module_0.is_file_readable("not_real_file") is False


def test_is_file_writable_0() -> None:
    """Test is_file_writable function"""
    assert module_0.is_file_writable("tests/test_conf_ok.yml") is True
    assert module_0.is_file_writable("not_real_file") is False


def test_is_directory_readable_0() -> None:
    """Test is_directory_readable function"""
    assert module_0.is_directory_readable("tests") is True
    assert module_0.is_directory_readable("not_real_directory") is False


def test_is_directory_writable_0() -> None:
    """Test is_directory_writable function"""
    assert module_0.is_directory_writable("tests") is True
    assert module_0.is_directory_writable("not_real_directory") is False


def test_is_directory_writable_1(tmp_path: pytest.TempPathFactory) -> None:
    """Test is_directory_writable function"""
    assert module_0.is_directory_writable(tmp_path) is True


def test_get_metadata(filesystem_fixture_0: str) -> None:
    """Test get_metadata function"""
    # Generate file structure
    path_0 = filesystem_fixture_0 / "test_dir_0" / "test_file_0_0"

    # Set path variables
    file_name = os.path.basename(path_0)
    file_path = os.path.realpath(path_0)
    dir_path = os.path.dirname(file_path)
    dir_name = os.path.basename(dir_path)
    sym_dir_path = os.path.join(filesystem_fixture_0, "test_symlink_dir")
    sym_file_path = os.path.join(filesystem_fixture_0, "test_symlink_file")

    # Test directory
    metadata = module_0.get_metadata(dir_path)
    assert metadata["type"] == "directory"
    assert metadata["name"] == dir_name
    assert metadata["path"] == dir_path
    assert metadata["access_time"] > 0
    assert metadata["create_time"] > 0
    assert metadata["modify_time"] > 0
    # assert metadata["group"] == os.getgid()
    # assert metadata["owner"] == os.getuid()
    assert metadata["permissions"] > 0
    assert metadata["inode"] > 0
    assert metadata["mount_point"] is False
    assert "symlink" not in metadata
    assert "size" not in metadata

    # Test file
    metadata = module_0.get_metadata(file_path)
    assert metadata["type"] == "file"
    assert metadata["name"] == file_name
    assert metadata["path"] == file_path
    assert metadata["size"] == 70
    assert metadata["access_time"] > 0
    assert metadata["create_time"] > 0
    assert metadata["modify_time"] > 0
    # assert metadata["group"] == os.getgid()
    # assert metadata["owner"] == os.getuid()
    assert metadata["permissions"] > 0
    assert metadata["inode"] > 0
    assert "mount_point" not in metadata
    assert "symlink" not in metadata

    # Test symlink to directory
    metadata = module_0.get_metadata(sym_dir_path)
    assert metadata["type"] == "symlink"
    assert metadata["name"] == "test_symlink_dir"
    assert metadata["path"] == sym_dir_path
    assert metadata["access_time"] > 0
    assert metadata["create_time"] > 0
    assert metadata["modify_time"] > 0
    # assert metadata["group"] == os.getgid()
    # assert metadata["owner"] == os.getuid()
    assert metadata["permissions"] > 0
    assert metadata["inode"] > 0
    assert metadata["symlink"] == os.path.join(filesystem_fixture_0, "test_dir_1")
    assert metadata["mount_point"] is False
    assert "size" not in metadata

    # Test symlink to file
    metadata = module_0.get_metadata(sym_file_path)
    assert metadata["type"] == "symlink"
    assert metadata["name"] == "test_symlink_file"
    assert metadata["path"] == sym_file_path
    assert metadata["size"] == 70
    assert metadata["access_time"] > 0
    assert metadata["create_time"] > 0
    assert metadata["modify_time"] > 0
    # assert metadata["group"] == os.getgid()
    # assert metadata["owner"] == os.getuid()
    assert metadata["permissions"] > 0
    assert metadata["inode"] > 0
    assert metadata["symlink"] == os.path.join(filesystem_fixture_0, "test_dir_1", "test_file_1_0")
    assert "mount_point" not in metadata


def testget_metadata_exceptions_0() -> None:
    """Test get_metadata exceptions"""
    with pytest.raises(FileNotFoundError):
        module_0.get_metadata("not_real_path")


def test_find_directory_content_0(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for files"""
    # Find files
    files = module_0.find_directory_content(
        filesystem_fixture_0 / "test_dir_0", depth=1, exclude_directories=True
    )
    assert len(files) == 1
    assert files[0]["name"] == "test_file_0_0"
    assert files[0]["type"] == "file"


def test_find_directory_content_1(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for directories"""
    # Find directories
    files = module_0.find_directory_content(
        filesystem_fixture_0 / "test_dir_0", depth=1, exclude_files=True
    )
    assert len(files) == 1
    assert files[0]["name"] == "test_dir_0_0"
    assert files[0]["type"] == "directory"

    # Find nothing
    files = module_0.find_directory_content(
        filesystem_fixture_0 / "test_dir_0", depth=1, exclude_files=True, exclude_directories=True
    )
    assert len(files) == 0


def test_find_directory_content_2(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for files and directories"""
    files = module_0.find_directory_content(filesystem_fixture_0 / "test_dir_0", depth=1)
    assert len(files) == 2
    assert files[0]["name"] != files[1]["name"]
    for file in files:
        assert file["name"] == "test_dir_0_0" or file["name"] == "test_file_0_0"
        if "test_dir" in file["name"]:
            assert file["type"] == "directory"
        if "test_file" in file["name"]:
            assert file["type"] == "file"


def test_find_directory_content_3(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for all files"""
    files = module_0.find_directory_content(
        filesystem_fixture_0, depth=0, exclude_directories=True, exclude_symlinks=True
    )
    assert len(files) == 7
    for file in files:
        assert "file" in file["name"]
        assert file["type"] == "file"
        assert "size" in file
        assert "symlink" not in file
        assert "mount_point" not in file


def test_find_directory_content_4(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for all directories"""
    files = module_0.find_directory_content(
        filesystem_fixture_0, depth=0, exclude_files=True, exclude_symlinks=True
    )
    assert len(files) == 5
    for file in files:
        assert "dir" in file["name"]
        assert file["type"] == "directory"
        assert "size" not in file
        assert "symlink" not in file
        assert file["mount_point"] is False


def test_find_directory_content_5(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for all files and directories to depth 3"""
    files = module_0.find_directory_content(filesystem_fixture_0, depth=3, exclude_symlinks=True)
    assert len(files) == 9
    for file in files:
        if "test_dir" in file["name"]:
            assert file["type"] == "directory"
            assert "size" not in file
            assert "symlink" not in file
            assert file["mount_point"] is False
        elif "test_file" in file["name"]:
            assert file["type"] == "file"
            assert "size" in file
            assert "symlink" not in file
            assert "mount_point" not in file


def test_find_directory_content_6(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for all symlinks"""
    files = module_0.find_directory_content(
        filesystem_fixture_0, depth=0, exclude_files=True, exclude_directories=True
    )
    assert len(files) == 2
    for file in files:
        assert "symlink" in file["name"]
        assert file["type"] == "symlink"

    # TODO: Add tests to find all but exclude pattern


def test_find_directory_content_7(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for all except a certain match"""
    files = module_0.find_directory_content(filesystem_fixture_0, exclude_patterns=["0_0_0"])
    assert len(files) == 9
    for file in files:
        if "test_dir" in file["name"]:
            assert file["type"] == "directory"
            assert "size" not in file
            assert "symlink" not in file
            assert file["mount_point"] is False
        elif "test_file" in file["name"]:
            assert file["type"] == "file"
            assert "size" in file
            assert "symlink" not in file
            assert "mount_point" not in file
        elif "symlink" in file["name"]:
            assert file["type"] == "symlink"
            assert "symlink" in file


def test_find_directory_content_8(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for all files, directories, and symlinks"""
    files = module_0.find_directory_content(filesystem_fixture_0, depth=0)
    assert len(files) == 14
    for file in files:
        if "test_dir" in file["name"]:
            assert file["type"] == "directory"
            assert "size" not in file
            assert "symlink" not in file
            assert file["mount_point"] is False
        elif "test_file" in file["name"]:
            assert file["type"] == "file"
            assert "size" in file
            assert "symlink" not in file
            assert "mount_point" not in file
        elif "symlink" in file["name"]:
            assert file["type"] == "symlink"
            assert "symlink" in file


def test_find_directory_content_exceptions_0() -> None:
    """Test find_directory_content exceptions"""
    with pytest.raises(OSError):
        module_0.find_directory_content("not_real_path")
