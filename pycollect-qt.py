#!/usr/bin/env python2
from PySide.QtGui import QApplication
import sys

from pycollect import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        window = MainWindow(sys.argv[1])
    except KeyError:
        window = MainWindow()
    sys.exit(app.exec_())
