import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor(dictionary=True)

    # Pobierz wszystkie rekordy z tabeli
    def fetch_all(self, table):
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Pobierz jeden rekord (np. po ID)
    def fetch_one(self, table, condition, params=None):
        query = f"SELECT * FROM {table} WHERE {condition} LIMIT 1"
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()
    
    # Pobierz n rekordów
    def fetch_last_n(self, table, n):
        query = f"SELECT * FROM {table} ORDER BY id DESC LIMIT %s"
        self.cursor.execute(query, (n,))
        return self.cursor.fetchall()

    # Pobierz najnowszy rekord
    def fetch_latest(self, table):
        query = f"SELECT * FROM {table} ORDER BY id DESC LIMIT 1"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # Własne zapytanie SELECT
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    # INSERT / UPDATE / DELETE
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        self.conn.commit()

    # Zamknięcie połączenia
    def close(self):
        self.cursor.close()
        self.conn.close()