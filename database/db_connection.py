import sqlite3

def create_connection(database_file):
    try:
        connection = sqlite3.connect(database_file)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return None