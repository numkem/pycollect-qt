from PySide.QtCore import QAbstractTableModel, QAbstractListModel, Qt, SIGNAL
import operator


class SearchModel(QAbstractTableModel):
    def __init__(self, parent, data, *args):
        "docstring"
        super(SearchModel, self).__init__(parent, *args)
        self._data = data
        self.headers = ['ID', 'Name', 'Platform']

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self._data[index.row()][index.column()]

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        try:
            return len(self._data[0])
        except IndexError:
            return 0

    def sort(self, col, order):
        "Sort table by given column number"
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self._data = sorted(self._data,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.emit(SIGNAL("layoutChanged()"))


class GameListModel(QAbstractListModel):
    def __init__(self, parent, games, *args):
        "docstring"
        super(GameListModel, self).__init__(parent, *args)
        self.games = sorted([g['name'] for g in games])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.games[index.row()]

    def rowCount(self, parent):
        return len(self.games)
