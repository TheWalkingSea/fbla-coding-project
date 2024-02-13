from . import conn
from datetime import datetime
import sqlite3
import os

def backup() -> None:
    """ Backs up the database """
    if not os.path.exists("backups"):
        os.makedirs("backups")
    timestamp = datetime.now().strftime("%Y%m%d")
    backup_conn = sqlite3.connect(f"backups/backup_{timestamp}.db")
    conn.backup(backup_conn)
    backup_conn.close()