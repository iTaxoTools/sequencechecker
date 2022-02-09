#!/usr/bin/env python3

from typing import Optional, Iterator
from pathlib import Path

from PySide6.QtWidgets import QListWidgetItem, QListWidget


class PathListItem(QListWidgetItem):
    def __init__(self, path: Path, parent: Optional[QListWidget] = None):
        super().__init__(path.name, parent, 1001)
        self.path = path

    def paths(self) -> Iterator[Path]:
        """
        If self contains a file path, yield it.
        If self contains a directory path, yield paths to files in it.
        """
        if self.path.is_file():
            yield self.path
            return
        if not self.path.is_dir():
            return
        for path in self.path.iterdir():
            if path.is_file():
                yield path
