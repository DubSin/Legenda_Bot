import sqlite3


class BoT_DB:
    def __init__(self, db):
        self.db = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.db.cursor()

    def get_yuan(self):
        result = self.cursor.execute("SELECT yuan FROM `exchange_rates`")
        return result.fetchone()

    def get_dollar(self):
        result = self.cursor.execute("SELECT dollar FROM `exchange_rates`")
        return result.fetchone()

    def get_euro(self):
        result = self.cursor.execute("SELECT euro FROM `exchange_rates`")
        return result.fetchone()

    def update_yuan(self, new_cur):
        self.cursor.execute("UPDATE `exchange_rates` SET `yuan` = ? WHERE `id` = 1", (new_cur,))
        return self.db.commit()

    def update_dollar(self, new_cur):
        self.cursor.execute("UPDATE `exchange_rates` SET `dollar` = ? WHERE `id` = 1", (new_cur,))
        return self.db.commit()

    def update_euro(self, new_cur):
        self.cursor.execute("UPDATE `exchange_rates` SET `euro` = ? WHERE `id` = 1", (new_cur,))
        return self.db.commit()

    def get_current(self):
        result = self.cursor.execute("SELECT * FROM `exchange_rates`")
        return result.fetchone()
