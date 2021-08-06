import logging
import sqlite3
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class Reply:
    """Class for keeping track of an item in inventory."""

    chat_id: int
    user_id: int = 0
    ts: int = 0

    @property
    def none(self) -> bool:
        return self.ts == 0

    @property
    def timeout(self):
        return int(time.time()) - self.ts


class Database:
    __connections = {}

    def __init__(self, db_url="db.sqlite"):
        self.__db_url = db_url
        self.__create_table()

    def __str__(self):
        return f"SQLite3({self.__db_url!r})"

    def get_reply_for_chat_id(self, chat_id):
        chat_id = int(chat_id)
        with self.cursor(commit=False) as cur:
            row = cur.execute(
                f"SELECT user_id, ts FROM reply_data WHERE chat_id={chat_id}"
            ).fetchone()
            reply = Reply(chat_id=chat_id)
            if row:
                reply.user_id = row[0]
                reply.ts = row[1]
            return reply

    def update_reply(self, chat_id, user_id):
        with self.cursor() as cur:
            cur.executemany(
                "INSERT OR REPLACE INTO reply_data VALUES (?, ?, ?)",
                ((chat_id, user_id, int(time.time())),),
            )

    @property
    def connection(self):
        thread_id = threading.get_ident()
        if thread_id not in self.__connections:
            self.__connections[thread_id] = sqlite3.connect(self.__db_url)
        if len(self.__connections) > 5:
            logging.warning("To many db connections: %s", len(self.__connections))
        return self.__connections[thread_id]

    @contextmanager
    def cursor(self, commit=True):
        yield self.connection.cursor()
        if commit:
            self.connection.commit()

    def __create_table(self):
        with self.cursor() as cur:
            sql = """
                CREATE TABLE IF NOT EXISTS reply_data (
                    chat_id INTEGER PRIMARY KEY
                    , user_id INTEGER NOT NULL
                    , ts INTEGER NOT NULL
                );
            """
            cur.execute(sql)
