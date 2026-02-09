import sqlite3
from datetime import datetime

class FortressDB:
    def __init__(self, db_path="fortress_index.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS storage_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            importance TEXT,
            timestamp TEXT,
            encrypted_content BLOB
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_entry(self, filename, importance, content):
        query = "INSERT INTO storage_index (filename, importance, timestamp, encrypted_content) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (filename, importance, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content))
        self.conn.commit()

    def get_all_files(self):
        return self.conn.execute("SELECT id, filename, importance, timestamp FROM storage_index ORDER BY id DESC").fetchall()

    def get_file_content(self, file_id):
        return self.conn.execute("SELECT encrypted_content FROM storage_index WHERE id = ?", (file_id,)).fetchone()
