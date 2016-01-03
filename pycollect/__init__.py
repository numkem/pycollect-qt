#!/usr/bin/env python2
from PySide.QtGui import *
from PySide.QtCore import *
from tinydb import TinyDB, where
import sys

from views import *
from models import GameListModel
from pycollectapi import PycollectApi

class MainWindow(QMainWindow):
    updated_game_list = Signal(str)

    def __init__(self, database_filename=None, parent=None):
        super(MainWindow, self).__init__(parent)

        self.updated_game_list.connect(self.update_game_list)
        self.db = PycollectApi()

        self.initUI()

        if database_filename is not None:
            self._open_tinydb(database_filename)

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        openFileAction = QAction(QIcon('open.png'), '&Open', self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.setStatusTip('Open existing database')
        openFileAction.triggered.connect(self.open_database)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(exitAction)

        self.find_button = QPushButton('F&ind')
        grid.addWidget(self.find_button, 1, 0)
        self.search_button = QPushButton('&Search', parent=self)
        grid.addWidget(self.search_button, 1, 1)
        self.search_button.clicked.connect(self.open_search_dialog)

        self.platform_list_combo = QComboBox(self)
        grid.addWidget(self.platform_list_combo, 2, 0, 1, 2)
        self.platform_list_combo.addItem('Select a platform')
        self.platform_list_combo.activated[str].connect(self.update_game_list)

        self.game_list_view = QListView(self)
        self.game_list_view.doubleClicked.connect(self.show_game)
        grid.addWidget(self.game_list_view, 3, 0, 1, 2)

        self.setWindowTitle('Pycollect')
        self.show()

    def open_database(self):
        filename = QFileDialog.getOpenFileName(self,
                                                "Open existing database",
                                                directory=".",
                                                filter="Database (*.db)")[0]
        self._open_tinydb(filename)

    def _open_tinydb(self, filename):
        try:
            self.db = PycollectApi(filename)
            self.statusBar().showMessage('Game total: {}'.format(self.db.game_count()))
            self.update_platform_list()
            self.setWindowTitle('Pycollect ({})'.format(filename))
        except IOError as e:
            pass

    def update_platform_list(self):
        self.platform_list = sorted(self.db.games_platforms())
        for i in range(0, self.platform_list_combo.count()):
            self.platform_list_combo.removeItem(i)

        self.platform_list_combo.addItem('Select a platform')
        self.platform_list_combo.addItems(self.platform_list)

    @Slot(str)
    def update_game_list(self, platform):
        self.current_platform = platform
        self.game_list = self.db.games_platform(platform)
        model = GameListModel(self, self.game_list)
        self.game_list_view.setModel(model)

    def open_search_dialog(self):
        search_dialog = SearchRemoteDialog(self)
        search_dialog.show()

    def show_game(self, game):
        detail_dialog = DetailDialog(self, game.data())
        detail_dialog.show()

