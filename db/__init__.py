import sqlite3
from typing import List, Tuple

class Connection:
    def __init__(self, fd: str) -> None:
        self.con = sqlite3.connect(fd)
        self.__create_brands_table()
        self.__create_tools_table()

    def get_brands(self) -> List[str]:
        cur = self.con.cursor()
        cur.execute('''
            SELECT name FROM brands;
        ''')
        brands = [brand[0] for brand in cur.fetchall()]
        cur.close()
        return brands

    def list_tables(self) -> List[str]:
        cur = self.con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cur.fetchall()]
        cur.close()
        return tables
    
    def add_brand(self, brand) -> None:
        brands = self.get_brands()

        cur = self.con.cursor()
        if brand in brands:
            cur.execute(f'''
                DELETE FROM brands
                WHERE name = {brand};
            ''')
        self.con.execute(
            f"INSERT INTO brands(name) VALUES(?);",
            (brand,)
        )
        self.con.commit()
        cur.close()


    def __create_brands_table(self):
        cur = self.con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS brands (
                name TEXT UNIQUE,
                id INTEGER PRIMARY KEY
            );
        ''')
        self.con.commit()
        cur.close()

    def __create_tools_table(self):
        cur = self.con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tools (
                name TEXT,
                model TEXT,
                brand TEXT,
                "brand-model" TEXT UNIQUE PRIMARY KEY
            );
        ''')

    def get_brand_tools(self, brand) -> List[Tuple[str, str, str]]:
        brands = self.get_brands()
        if brand not in brands:
            self.add_brand(brand)

        cur = self.con.cursor()
        cur.execute(f'''
            SELECT name, model, "brand-model" FROM tools
            WHERE brand = ?
        ''', (brand,))
        tools = [(e[0], e[1], e[2]) for e in cur.fetchall()]
        cur.close()
        return tools

    
    def add_tool(self, brand, name, model):
        tools = self.get_brand_tools(brand)

        cur = self.con.cursor()
        if f"{brand}-{model}" in [e[2] for e in tools]:
            cur.execute(f'''
                DELETE FROM tools
                WHERE "brand-model" = "{brand}-{model}"
            ''')
        
        cur.execute(
            f'''
            INSERT INTO tools (brand, name, model, "brand-model")
            VALUES (?, ?, ?, ?)
            ''',
            (brand, name, model, f"{brand}-{model}")
        )
        self.con.commit()
        cur.close() 

    # def store()
