#!/usr/bin/env python2
from PySide.QtGui import QApplication
import sys

from pycollect import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
