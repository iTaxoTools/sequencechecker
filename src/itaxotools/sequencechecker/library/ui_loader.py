#!/usr/bin/env python3

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QMetaObject


class UiLoader(QUiLoader):
    def __init__(self, base_instance):
        QUiLoader.__init__(self, base_instance)
        self.base_instance = base_instance

    def createWidget(self, className, parent=None, name=""):
        if parent is None and self.base_instance:
            return self.base_instance
        else:
            widget = QUiLoader.createWidget(self, className, parent, name)
            if self.base_instance:
                setattr(self.base_instance, name, widget)
            return widget


def load_ui(ui_file, base_instance=None):
    loader = UiLoader(base_instance)
    widget = loader.load(ui_file)
    QMetaObject.connectSlotsByName(widget)
    return widget
