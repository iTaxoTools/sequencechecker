#!/usr/bin/env python3

import sys
from pathlib import Path
from PySide6.QtCore import Qt, QFile, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


@Slot()
def say_hello() -> None:
    print("hello")


def main() -> None:
    app = QApplication(sys.argv)
    loader = QUiLoader()
    ui_file = QFile(str(Path(__file__).with_name("sequencechecker.ui")))
    ui_file.open(QFile.ReadOnly)
    win = loader.load(ui_file)
    ui_file.close()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
