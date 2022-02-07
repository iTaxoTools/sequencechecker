#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication
import tempfile
from pathlib import Path
import shutil

from .library.gui import SequenceCheckerMainWindow


def main() -> None:
    app = QApplication(sys.argv)
    preview_dir = Path(tempfile.mkdtemp())
    app.aboutToQuit.connect(lambda: shutil.rmtree(preview_dir, ignore_errors=True))
    win = SequenceCheckerMainWindow(preview_dir)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
