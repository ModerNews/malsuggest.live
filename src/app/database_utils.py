import datetime
from typing import Collection


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
        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM cache WHERE timestamp < %s", (timestamp, ))
            return cur.fetchall()

    def create_cache_data(self, all_results, primary_result):
        assert (isinstance(primary_result, int) or isinstance(primary_result, str))
        assert isinstance(all_results, Collection)
        with self._conn.cursor() as cur:
            cur.execute("INSERT INTO cache VALUES (default, %s, %s, default) RETURNING id", (primary_result, all_results, ))
            return cur.fetchone()[0]
        if self.autocommit:
            self._conn.commit()

    def create_task(self, task_id):
        with self._conn.cursor() as cur:
            cur.execute("INSERT INTO task_state VALUES (default, %s, default)", (task_id, ))
        if self.autocommit:
            self._conn.commit()

    def bind_cache_to_task(self, task_id, cache_id):
        with self._conn.cursor() as cur:
            cur.execute("UPDATE task_state SET cache_id = %s WHERE task_id = %s", (cache_id, task_id, ))
        if self.autocommit:
            self._conn.commit()

    def get_session_by_token(self, token):
        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM sessions WHERE token = %s", (token, ))
            return cur.fetchone()

    def create_session(self, user_id, token, expires_in):
        with self._conn.cursor() as cur:
            cur.execute("INSERT INTO sessions VALUES (default, %s, %s, %s)", (expires_in, token, user_id,))
        if self.autocommit:
            self._conn.commit()

    def create_mal_tokens(self, user_id, access_token, refresh_token):
        # TODO ensure that tokens are unique psycopg2.errors.UniqueViolation
        with self._conn.cursor() as cur:
            cur.execute("INSERT INTO mal_tokens VALUES (%s, %s, %s)", (user_id, access_token, refresh_token,))
        if self.autocommit:
            self._conn.commit()

    def get_mal_tokens(self, user_id):
        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM mal_tokens WHERE user_id = %s", (user_id, ))
            return cur.fetchone()

    def get_mal_tokens_for_session(self, session_token):
        with self._conn.cursor() as cur:
            cur.execute("SELECT mal.* FROM mal_tokens mal INNER JOIN sessions s ON mal.user_id = s.user_id WHERE s.token = %s", (session_token, ))
            return cur.fetchone()

    def delete_mal_tokens_with_user_id(self, user_id):
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM mal_tokens WHERE user_id = %s", (user_id, ))
        if self.autocommit:
            self._conn.commit()

    def delete_session_token(self, session_token):
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM sessions WHERE user_id = %s", (session_token, ))
        if self.autocommit:
            self._conn.commit()