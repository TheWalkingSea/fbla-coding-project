import sqlite3
import sys
import os




def create_connection(database_file: str) -> None:
    """ Creates a database connections
    
    Parameters:
    (str)database_file: A file path for the database

    """
    try:
        connection = sqlite3.connect(database_file)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        input(f"Error connecting to SQLite database: {e}")
        return None