import datetime


class CRUD:
    def get_cache_data(self):
        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM cache")
            return cur.fetchall()

    def get_cache_by_task_id(self, task_id):
        with self._conn.cursor() as cur:
            cur.execute("SELECT c.* FROM task_state INNER JOIN cache AS c ON task_state.cache_id = c.id WHERE task_state.task_id = %s", (task_id, ))
            return cur.fetchall()

    def get_cache_before_date(self, timestamp: datetime.datetime | datetime.date):
        if isinstance(timestamp, datetime.date):
            timestamp = datetime.datetime.combine(timestamp, datetime.time.min)