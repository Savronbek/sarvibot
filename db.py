import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                referrer_id INTEGER
            )
            """)

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, referrer_id=None):
        if not self.user_exists(user_id):
            with self.connection:
                try:
                    if referrer_id is not None:
                        self.cursor.execute("INSERT INTO users (user_id, referrer_id) VALUES (?, ?)", (user_id, referrer_id))
                    else:
                        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
                except sqlite3.IntegrityError as e:
                    print(f"Error adding user: {e}")
                    return False
        return True

    def count_referrals(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT COUNT(id) as count FROM users WHERE referrer_id = ?", (user_id,)).fetchone()
            return result[0] if result else 0
