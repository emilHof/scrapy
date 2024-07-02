import sqlite3
from typing import List

class Connection:
    def __init__(self, fd: str) -> None:
        self.con = sqlite3.connect(fd)

    def get_brands(self) -> List[str]:
        cur = self.con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS brands (
                name TEXT UNIQUE,
                id INTEGER PRIMARY KEY
            );
        ''')
        cur.execute('''
            SELECT name FROM brands;
        ''')
        return [brand[0] for brand in cur.fetchall()]

    def get_available_tools(self, brand) -> List[str]:
        cur = self.con.cursor()


    def list_tables(self) -> List[str]:
        cur = self.con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in cur.fetchall()]
    # def store()