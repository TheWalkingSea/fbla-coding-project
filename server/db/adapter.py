import psycopg2 as pgdriver
import logging
from datetime import datetime
import subprocess
from psycopg2.extensions import connection

logger = logging.getLogger(__name__)

class DatabaseAdapter:
    """ A database adapter used to make code more robust and supports dynamic backups to the database so data is preserved """
    def __init__(self, conn: connection=None, **kwargs) -> None:
        self.db_params = kwargs
        self.conn = conn
        self._latest_checksum = None
    
    def connect(self) -> None:
        """ Establishs a connection with the database using db_params passed during initialization """
        self.conn = pgdriver.connect(**self.db_params)
        # self._latest_checksum = self._calculate_db_checksum() # Sets the checksum 
    
    def execute_query(self, query: str, params: tuple=None, commit: bool=True) -> None:
        """ 
        Executes a query with params. Logs an error if anything goes wrong
        
        Parameters:
        (str)query: The query to execute
        (tuple)params: Params that are substituted in the query to prevent SQL injection
        (bool)commit: Whether or not the change is committed to the db. This is useful when stacking queries
        
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, vars=params)
                if (commit): self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                logging.error("Rolling back because something went executing query; Query: %s; Params: %s; Exception: %s" % (query, params, e))

    def fetchall(self, query: str, params: tuple=None) -> list:
        """ 
        Fetches all rows from the query. Logs an error if anything goes wrong
        
        Parameters:
        (str)query: The query to execute
        (tuple)params: Params that are substituted in the query to prevent SQL injection
        
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query=query, vars=params)
                return cursor.fetchall()
            except Exception as e:
                logging.error("Something went wrong retrieving data; Query: %s; Params: %s; Exception: %s" % (query, params, e))
                return None
    
    def fetchone(self, query: str, params: tuple=None) -> list:
        """ 
        Fetches one row from the query. Useful for when a primary key is used. Logs an error if anything goes wrong
        
        Parameters:
        (str)query: The query to execute
        (tuple)params: Params that are substituted in the query to prevent SQL injection
        
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query=query, vars=params)
                return cursor.fetchone()
            except Exception as e:
                logging.error("Something went wrong retrieving data; Query: %s; Params: %s; Exception: %s" % (query, params, e))
                return None
    
    def get_column_names(self, table_name: str) -> list[str]:
        """ Gets the column names for the table and returns it as a list of strings 
        
        Parameters:
        (str)table_name: The name of the table to extract column names from
        
        Returns:
        (list[str]): A list of strings that represents the column names in the order as show in the db
        
        """
        return [i[0] for i in self.fetchall("SELECT column_name FROM information_schema.columns WHERE table_name=%s ORDER BY ordinal_position", (table_name,))]


    def _calculate_db_checksum(self) -> str:
        """ Calculates a checksum on the database's data using MD5, a common algorithm for calculating signatures 
         
        Returns:
        (str): The checksum value of the database as a 32 character string
         
        """
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT MD5(pg_dump())")
            checksum = cursor.fetchone()[0]
            logging.info("Checksum for current db: %s" % checksum)
            return checksum

    def get_backup_filename(self) -> str:
        """ Gets a filename for the backup in the format backup_YYMMDD_HHMMSS.sql
        
        Returns:
        (str): A filename for the db
        
        """
        dt = datetime.now()
        return "backup_%s.sql" % dt.strftime("%Y%m%d_%H%M%S")

    def backup(self) -> None:
        """ Performs a full backup to the database if any changes were made """
        # If the checksums are the same, nothing has changed
        if (self._latest_checksum == self._calculate_db_checksum()):
            logging.info("No changes have been made to the database since the last backup")
        else:
            logging.info("Backing up database...")
            # https://www.postgresql.org/docs/current/app-pgdump.html
            command = [
                "pg_dump",
                "--file", f"./backups/{self.get_backup_filename()}",
                "--dbname", self.conn.dsn # Can be a connection string according to the docs
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            stdout, stderr = process.communicate()
            logging.info(stdout.decode('utf-8'))
            if (process.returncode == 0):
                logging.info("Backup completed successfully")
            else:
                logging.error(f"Something went wrong updating the database; {stderr.decode('utf-8')}")

    def close(self) -> None:
        """ Closes the connections to the class """
        self.conn.close()
