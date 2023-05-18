from pathlib import Path

from lintel import Configuration, discover_files


def test_file_discovery(discovery_dir: Path) -> None:
    top_level_file = discovery_dir / "top_level.py"
    first_file = discovery_dir / "first_folder" / "first_file.py"
    second_file = discovery_dir / "second_folder" / "second_file.py"
    hidden_file = discovery_dir / ".hidden" / "hidden.py"

    config = Configuration()
    files = discover_files([discovery_dir], config)

    assert len(files) == 3
    assert top_level_file in files
    assert first_file in files
    assert second_file in files

    # CLI takes precedence
    files = discover_files([discovery_dir, hidden_file], config)

    assert len(files) == 4
    assert hidden_file in files

    # Can match files
    config = Configuration(match=".*file.py$")
    files = discover_files([discovery_dir], config)

    assert len(files) == 2
    assert first_file in files
    assert second_file in files

    # Can match folders
    config = Configuration(match_dir=".*folder$")
    files = discover_files([discovery_dir], config)

    assert len(files) == 3
    assert top_level_file in files
    assert first_file in files
    assert second_file in files
