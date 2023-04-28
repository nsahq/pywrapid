#!/usr/bin/python3
"""Pywrapid filesystem tools tests"""

import os

import pytest

import pywrapid.utils as module_0

# pylint: disable=redefined-outer-name, protected-access, no-member


@pytest.fixture()
def filesystem_fixture_0(tmp_path: str) -> str:
    """Fixture for producing file and directory structure"""
    # Top level
    path_0 = tmp_path / "test_dir_0" / "test_file_0_0"  # type: ignore
    path_0.parent.mkdir()
    path_0.touch()
    path_0.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    path_1 = tmp_path / "test_dir_1" / "test_file_1_0"  # type: ignore
    path_1.parent.mkdir()
    path_1.touch()
    path_1.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    single_file_0 = tmp_path / "test_file_0"  # type: ignore
    single_file_0.touch()
    single_file_0.write_text(
        "sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    )

    single_file_1 = tmp_path / "test_file_1"  # type: ignore
    single_file_1.touch()
    single_file_1.write_text(
        "sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    )

    # Second level
    path_2 = tmp_path / "test_dir_0" / "test_dir_0_0" / "test_file_0_0_0"  # type: ignore
    path_2.parent.mkdir()
    path_2.touch()
    path_2.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    # Third level
    path_3 = tmp_path / "test_dir_0" / "test_dir_0_0" / "test_dir_0_0_0" / "test_file_0_0_0_0"  # type: ignore
    path_3.parent.mkdir()
    path_3.touch()
    path_3.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    # Fourth level
    path_4 = (
        tmp_path  # type: ignore
        / "test_dir_0"
        / "test_dir_0_0"
        / "test_dir_0_0_0"
        / "test_dir_0_0_0_0"
        / "test_file_0_0_0_0_0"
    )
    path_4.parent.mkdir()
    path_4.touch()
    path_4.write_text("sample text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    sym_dir = tmp_path / "test_dir_1" / "test_symlink_dir"  # type: ignore
    sym_file = tmp_path / "test_dir_1" / "test_file_1_0" / "test_symlink_file"  # type: ignore
    if not os.path.exists(sym_dir):
        os.symlink(tmp_path / "test_dir_1", tmp_path / "test_symlink_dir")  # type: ignore
    if not os.path.exists(sym_file):
        os.symlink(tmp_path / "test_dir_1" / "test_file_1_0", tmp_path / "test_symlink_file")  # type: ignore

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


# pylint: disable=too-many-statements
def test_get_metadata(filesystem_fixture_0: str) -> None:
    """Test get_metadata function"""
    # Generate file structure
    path_0 = filesystem_fixture_0 / "test_dir_0" / "test_file_0_0"  # type: ignore

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
        filesystem_fixture_0 / "test_dir_0", depth=1, exclude_directories=True  # type: ignore
    )
    assert len(files) == 1
    assert files[0]["name"] == "test_file_0_0"
    assert files[0]["type"] == "file"


def test_find_directory_content_1(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for directories"""
    # Find directories
    files = module_0.find_directory_content(
        filesystem_fixture_0 / "test_dir_0", depth=1, exclude_files=True  # type: ignore
    )
    assert len(files) == 1
    assert files[0]["name"] == "test_dir_0_0"
    assert files[0]["type"] == "directory"

    # Find nothing
    files = module_0.find_directory_content(
        filesystem_fixture_0 / "test_dir_0", depth=1, exclude_files=True, exclude_directories=True  # type: ignore
    )
    assert len(files) == 0


def test_find_directory_content_2(filesystem_fixture_0: str) -> None:
    """Test find_directory_content for files and directories"""
    files = module_0.find_directory_content(filesystem_fixture_0 / "test_dir_0", depth=1)  # type: ignore
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


# Test find_directory_content order by name, size, and type
def test_find_directory_content_9(filesystem_fixture_0: str) -> None:
    """Test find_directory_content order by name"""
    files = module_0.find_directory_content(
        filesystem_fixture_0, depth=1, order_by="name", order="asc"
    )

    assert len(files) == 6
    assert files[0]["name"] == "test_dir_0"
    assert files[1]["name"] == "test_dir_1"
    assert files[2]["name"] == "test_file_0"
    assert files[3]["name"] == "test_file_1"
    assert files[4]["name"] == "test_symlink_dir"
    assert files[5]["name"] == "test_symlink_file"


def test_find_directory_content_10(filesystem_fixture_0: str) -> None:
    """Test find_directory_content order by name, ascending"""
    files = module_0.find_directory_content(
        filesystem_fixture_0, depth=1, order_by="path", order="asc"
    )

    assert len(files) == 6
    assert files[0]["name"] == "test_dir_0"
    assert files[1]["name"] == "test_dir_1"
    assert files[2]["name"] == "test_file_0"
    assert files[3]["name"] == "test_file_1"
    assert files[4]["name"] == "test_symlink_dir"
    assert files[5]["name"] == "test_symlink_file"


def test_find_directory_content_exceptions_0() -> None:
    """Test find_directory_content exceptions"""
    with pytest.raises(OSError):
        module_0.find_directory_content("not_real_path")


def test_filesystem_tools__special_sort_0() -> None:
    """Test _special_sort function."""
    data = [
        {
            "name": "file_1",
            "path": "/tmp/dir1/file_1",
            "size": 100,
            "type": "file",
        },
        {
            "name": "file_2",
            "path": "/tmp/dir1/dir2/file_2",
            "size": 200,
            "type": "file",
        },
        {
            "name": "file_3",
            "path": "/tmp/dir1/dir2/dir3/file_3",
            "size": 300,
            "type": "file",
        },
    ]
    keys = ["name", "path", "size", "type"]

    for key in keys:
        result = module_0.filesystem_tools._special_sort(data, key, "asc")
        assert result == data if key not in ["path", "type"] else list(reversed(data))

        result = module_0.filesystem_tools._special_sort(data, key, "desc")
        assert result == list(reversed(data)) if key not in ["path", "type"] else data

    # Test for invalid key
    with pytest.raises(ValueError):
        module_0.filesystem_tools._special_sort(data, "invalid_key", "asc")

    # Test for invalid order
    with pytest.raises(ValueError):
        module_0.filesystem_tools._special_sort(data, "name", "invalid_order")


def test_filesystem_tools__special_sort_1() -> None:
    """Test _special_sort function."""
    data = [
        {
            "name": "file_1",
            "path": "/tmp/dir1/file_1",
            "size": 100,
            "type": "file",
        },
        {
            "name": "dir_1",
            "path": "/tmp/dir1",
            "type": "file",
            "mount_point": False,
        },
        {
            "name": "symlink_1",
            "path": "/tmp/dir1/symlink_1",
            "size": 300,
            "type": "file",
            "symlink": "/tmp/dir1/file_1",
        },
    ]

    keys = ["name", "path", "type"]

    for key in keys:
        result = module_0.filesystem_tools._special_sort(data, key, "asc")
        assert result == data

        result = module_0.filesystem_tools._special_sort(data, key, "desc")
        assert result == list(reversed(data))

    # Test for invalid key
    with pytest.raises(ValueError):
        module_0.filesystem_tools._special_sort(data, "invalid_key", "asc")

    # Test for invalid order
    with pytest.raises(ValueError):
        module_0.filesystem_tools._special_sort(data, "name", "invalid_order")
