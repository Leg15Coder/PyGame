from config import config
import sqlite3 as sql


class Database(object):
    def __init__(self):
        self.db = sql.connect(config.db.get_secret_value())
        self.cur = self.db.cursor()

    def __del__(self):
        self.db.commit()
        self.db.close()

    def get_dialog(self, i: int):
        res = self.cur.execute(f"SELECT * FROM dialogs WHERE id={i}").fetchone()[0]
        names = ['id', 'text', 'order', 'events', 'dialog_id', 'next_step', 'start']
        res = self.cur.execute(f"SELECT * FROM frases WHERE dialog_id={res}").fetchall()
        return tuple({names[i]: e[i] for i in range(7)} for e in res)


db = Database()
