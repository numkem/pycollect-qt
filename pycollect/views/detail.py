from PySide.QtGui import *
from PySide.QtCore import Qt
import requests

class DetailDialog(QDialog):
    def __init__(self, parent, game_name):
        "docstring"
        super(DetailDialog, self).__init__(parent)
        self.parent = parent
        self.game_title = game_name
        self.game = self.parent.db.game_by_name(game_name)
        self._details = {
            'ID': {
                'key': 'id',
                'type': QLineEdit,
                'read-only': True
            },
            'Name': {
                'key': 'name',
                'type': QLineEdit,
            },
            'Condition': {
                'key': 'condition',
                'type': QLineEdit,
            },
            'Genre': {
                'key': 'genre',
                'type': QLineEdit,
            },
            'Platform': {
                'key': 'platform',
                'type': QLineEdit,
                'read-only': True
            },
            'Box Text': {
                'key': 'box_text',
                'type': QTextEdit,
            }
        }
        self._details_controls = {}
        self._details_order = ['ID', 'Name', 'Condition', 'Genre', 'Platform', 'Box Text']

        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)


        # Get the image from remote site
        image = None
        if 'image' in self.game:
            try:
                r = requests.get(self.game['image'], stream=True)
                if r.status_code == 200:
                    data = r.raw.read()
                    pixmap = QPixmap()
                    pixmap.loadFromData(data)
            except requests.exceptions.ConnectionError:
                pass

        image_label = QLabel(self)
        if pixmap is not None:
            image_label.setPixmap(pixmap)
        self.layout.addWidget(image_label, 1, 1, 10, 1)

        self.setWindowTitle('Details for {}'.format(self.game['name']))

        layout_row_id = 1
        for label_name in self._details_order:
            detail = self._details[label_name]
            key = detail['key']

            label = QLabel(label_name)
            self.layout.addWidget(label, layout_row_id, 2)

            self._details_controls[key] = detail['type']()
            self.layout.addWidget(self._details_controls[key], layout_row_id, 3, 1, 2)

            layout_row_id += 1

        close_button = QPushButton('&Close')
        close_button.clicked.connect(self.close)
        self.layout.addWidget(close_button, layout_row_id, 4)

        self.load_game_details()

    def load_game_details(self):
        for key, control in self._details_controls.iteritems():
            try:
                control.setText(self.game[key])
            except KeyError:
                pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
