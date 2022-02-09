#!/usr/bin/env python3

from typing import Dict, Iterator, List
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QToolButton,
    QPushButton,
    QCheckBox,
    QListWidget,
    QListView,
    QTreeView,
    QFileDialog,
    QFileSystemModel,
    QTextBrowser,
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QFile, Slot, QModelIndex, QUrl, Qt

import itaxotools.common as common
import itaxotools.common.resources

from .ui_loader import load_ui
from .options import Option
from .path_list_item import PathListItem


class SequenceCheckerMainWindow(QMainWindow):
    def __init__(self, prewiev_dir: Path):
        super(SequenceCheckerMainWindow, self).__init__()
        self.preview_dir = prewiev_dir
        self.load_ui()
        self.set_logos_and_icons()
        self.collect_options_checkboxes()
        self.connect_filelist_buttons()
        self.connect_preview()
        for checkbox in self._options.values():
            checkbox.stateChanged.connect(self.show_options)

    @Slot()
    def show_options(self) -> None:
        print(self.options())

    def load_ui(self) -> None:
        ui_file = QFile(
            common.resources.get("itaxotools.sequencechecker", "ui/sequencechecker.ui")
        )
        ui_file.open(QFile.ReadOnly)
        load_ui(ui_file, self)
        ui_file.close()

    def set_logos_and_icons(self):
        logo_label = self.findChild(QLabel, "Logo")
        logo_pixmap = QPixmap(
            common.resources.get("logos/itaxotools-micrologo.png")
        ).scaledToHeight(80)
        logo_label.setPixmap(logo_pixmap)

        save_btn = self.findChild(QToolButton, "save_btn")
        save_icon = QIcon(common.resources.get("icons/svg/save.svg"))
        save_btn.setIcon(save_icon)

        save_all_btn = self.findChild(QToolButton, "save_all_btn")
        save_all_icon = QIcon(common.resources.get("icons/svg/save_all.svg"))
        save_all_btn.setIcon(save_all_icon)

    def collect_options_checkboxes(self) -> None:
        self._options: Dict[Option, QCheckBox] = {}
        for option in Option:
            self._options[option] = self.findChild(QCheckBox, option._name_)

    def options(self) -> Dict[Option, bool]:
        return {option: self._options[option].isChecked() for option in Option}

    def connect_filelist_buttons(self) -> None:
        self.filelist = self.findChild(QListWidget, "filelist_widget")
        self.findChild(QPushButton, "file_btn").clicked.connect(self.add_file_path)
        self.findChild(QPushButton, "dir_btn").clicked.connect(self.add_dir_path)
        self.findChild(QPushButton, "file_rm_btn").clicked.connect(
            self.clear_selected_paths
        )
        self.findChild(QPushButton, "files_clear_btn").clicked.connect(self.clear_paths)

    def add_path(self, path: Path) -> None:
        PathListItem(path, self.filelist)

    @Slot()
    def add_file_path(self) -> None:
        file_names, _ = QFileDialog.getOpenFileNames(self)
        for file_name in file_names:
            self.add_path(Path(file_name))

    @Slot()
    def add_dir_path(self) -> None:
        dir_name = QFileDialog.getExistingDirectory()
        if dir_name:
            self.add_path(Path(dir_name))

    @Slot()
    def clear_selected_paths(self) -> None:
        for item in self.filelist.selectedItems():
            self.filelist.takeItem(self.filelist.row(item))

    @Slot()
    def clear_paths(self) -> None:
        self.filelist.clear()

    def connect_preview(self) -> None:
        self.preview_model = QFileSystemModel(self)
        self.text_browser = self.findChild(QTextBrowser, "preview_box")
        self.preview_model.setRootPath(str(self.preview_dir))
        files_view = self.findChild(QListView, "files_view")
        files_view.setModel(self.preview_model)
        files_view.setRootIndex(self.preview_model.index(str(self.preview_dir)))
        files_view.selectionModel().currentChanged.connect(self.test_model_connect)

    @Slot(QModelIndex)
    def test_model_connect(self, index: QModelIndex) -> None:
        self.text_browser.setSource(
            QUrl.fromLocalFile(self.preview_model.filePath(index))
        )

    def input_paths(self) -> Iterator[Path]:
        for item in self.filelist.findItems("*", Qt.MatchWildcard):
            yield from item.paths()
