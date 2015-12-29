from PySide.QtGui import *
from PySide.QtCore import Qt

from pycollect.plugins import VgCollectApi
from pycollect.models import SearchModel

class SearchRemoteDialog(QDialog):
    def __init__(self, parent):
        "docstring"
        super(SearchRemoteDialog, self).__init__(parent)
        self.api = VgCollectApi()
        self.initUI()
        self.parent = parent


    def initUI(self):
        self.setWindowTitle('Search remote database')
        self.setMinimumSize(900, 600)

        layout = QGridLayout()
        self.setLayout(layout)

        self.search_box = QLineEdit(self)
        search_label = QLabel('Search by name:')
        search_button = QPushButton('Search')
        self.condition_combo = QComboBox(self)
        self.condition_combo.addItems(['Loose', 'CIB', 'New'])
        add_button = QPushButton('Add')
        quit_button = QPushButton('Close')
        self.search_result_table = QTableView()
        self.search_result_table.setSortingEnabled(True)
        self.search_result_table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.search_result_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        layout.addWidget(search_label, 1, 1)
        layout.addWidget(self.search_box, 1, 2, 1, 2)
        layout.addWidget(search_button, 1, 4)
        layout.addWidget(self.search_result_table, 2, 1 , 4, 4)
        layout.addWidget(self.condition_combo, 6, 2)
        layout.addWidget(add_button, 6, 3)
        layout.addWidget(quit_button, 6, 4)

        search_button.clicked.connect(self.search_vgcollect)
        add_button.clicked.connect(self.add_items)
        quit_button.clicked.connect(self.close)

        self.updateGeometry()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter:
            self.search_vgcollect()
        if e.key() == Qt.Key_Escape:
            self.close()

    def search_vgcollect(self):
        data = []
        self.api_results = self.api.search_games(self.search_box.text().split(' '))
        for g in self.api_results:
            data.append((g['game_id'], g['name'], g['category_name']))
        self.search_result_table.setModel(SearchModel(self, data))
        self.search_result_table.resizeColumnsToContents()

    def add_items(self):
        for r in self.search_result_table.selectedIndexes():
            if r.data().isdigit():
                item =  self.api.get_item(r.data())
                item['condition'] = self.condition_combo.currentText().lower()
                self.parent.db.add_game(item)
        self.parent.updated_game_list.emit(self.parent.current_platform)
