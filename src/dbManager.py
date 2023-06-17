from os import path
from sqlite3 import connect


class DatabaseManager:
    def __init__(self, db_file_path="../db/database_file.db"):
        self.database_file = db_file_path
        self.conn = None

    def connect_to_db(self):
        if not path.exists(self.database_file):
            self.create_database()

        self.conn = connect(self.database_file)

    def create_database(self):
        conn = connect(self.database_file)
        cursor = conn.cursor()

        # Create the Users table
        cursor.execute('''CREATE TABLE Users (
                               id INTEGER PRIMARY KEY,
                               name TEXT,
                               email TEXT,
                               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )''')

        # Create the Uploads table
        cursor.execute('''CREATE TABLE Uploads (
                               id INTEGER PRIMARY KEY,
                               user_id INTEGER,
                               filename TEXT,
                               metadata TEXT,
                               uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               FOREIGN KEY (user_id) REFERENCES Users(id)
                           )''')

        conn.commit()
        conn.close()

    def close(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query):
        if self.conn is None:
            self.connect_to_db()
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        return cursor.fetchall()

    def insert_user(self, name, email):
        query = f"INSERT INTO Users (name, email) VALUES ('{name}', '{email}')"
        self.execute_query(query)

    def insert_upload(self, user_id, filename, metadata):
        query = f"INSERT INTO Uploads (user_id, filename, metadata) VALUES ({user_id}, '{filename}', '{metadata}')"
        self.execute_query(query)

    def get_users(self):
        query = "SELECT * FROM Users"
        return self.execute_query(query)

    def get_uploads(self):
        query = "SELECT * FROM Uploads"
        return self.execute_query(query)
