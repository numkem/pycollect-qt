from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage
import os


class GameAlreadyExistException(Exception):
    def __init__(self, game_id):
        "docstring"
        self.game_id = game_id
    def message():
        return "Game #{} already exits in database".format(self.game_id)


class PycollectApi(object):
    def __init__(self, filename=None):
        "docstring"
        if filename is None:
            self.db = TinyDB(storage=MemoryStorage)
            self.games = self.db.table('games')
        else:
            if os.path.isfile(filename):
                self.db = TinyDB(filename)
                self.games = self.db.table('games')
            else:
                raise IOError("{} is not a valid Pycollect database filename".format(filename))

    def _games_by_attr(self, attr, value):
        return self.games.search(where(attr) == value)

    def all_games(self):
        return self.games.all()

    def add_game(self, game):
        # Check that the game doesn't already exists by it's id
        games = self._games_by_attr('id', game['id'])
        if not len(games):
            self.games.insert(game)
        else:
            raise GameAlreadyExistException(game['id'])

    def games_platform(self, platform):
        return self._games_by_attr('platform', platform)

    def games_platforms(self):
        return set(g['platform'] for g in self.games.all())

    def game_count(self):
        return len(self.games)
