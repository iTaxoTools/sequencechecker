#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from .library.gui import SequenceCheckerMainWindow


def main() -> None:
    app = QApplication(sys.argv)
    win = SequenceCheckerMainWindow()
    win.show()
    print(win.options())
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
