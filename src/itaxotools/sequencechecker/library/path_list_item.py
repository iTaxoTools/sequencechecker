#!/usr/bin/env python3

from typing import Optional
from pathlib import Path

from PySide6.QtWidgets import QListWidgetItem, QListWidget


class PathListItem(QListWidgetItem):
    def __init__(self, path: Path, parent: Optional[QListWidget] = None):
        super().__init__(path.name, parent, 1001)
        self.path = path
