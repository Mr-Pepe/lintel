import os
import re
from pathlib import Path
from typing import List, Set

from lintel import Configuration


def discover_files(paths: List[Path], config: Configuration) -> Set[Path]:
    discovered_files: Set[Path] = set()

    for path in paths:
        if path.is_file() and re.compile(config.match).match(path.name):
            discovered_files.add(path)

        if path.is_dir():
            for dirpath, dirnames, filenames in os.walk(path):
                # Do not recurse into folders that don't match the regex
                dirnames[:] = [n for n in dirnames if re.compile(config.match_dir).match(n)]

                for filename in filenames:
                    if re.compile(config.match).match(filename):
                        discovered_files.add(Path(dirpath) / filename)

    return discovered_files
