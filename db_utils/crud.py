import sqlite3


class DatabaseClient(object):
    def __init__(self, *args, **kwargs):
        self._parameters = kwargs
        self.client = sqlite3.connect(*args, **kwargs)

    def __enter__(self):
        return self.client.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_genres(self, mal_id: int):
        with self as cursor:
            return cursor.execute("SELECT * FROM genres WHERE mal_id = ?", (mal_id,))
