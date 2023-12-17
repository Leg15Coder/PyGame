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
        res = tuple({names[i]: e[i] for i in range(len(names))} for e in res)
        return res

    def get_quest(self, i: int):
        res = self.cur.execute(f"SELECT * FROM quests WHERE id={i}").fetchone()[0]
        names = ['id', 'opinion']
        res = ({names[i]: e[i] for i in range(len(names))} for e in res)
        return res


db = Database()
