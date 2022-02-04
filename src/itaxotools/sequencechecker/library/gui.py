#!/usr/bin/env python3

from typing import Dict
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QLabel, QToolButton, QCheckBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QFile, Slot, QSize

import itaxotools.common as common
import itaxotools.common.resources

from .ui_loader import load_ui
from .options import Option


class SequenceCheckerMainWindow(QMainWindow):
    def __init__(self):
        super(SequenceCheckerMainWindow, self).__init__()
        self.load_ui()
        self.set_logos_and_icons()
        self.collect_options_checkboxes()
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
