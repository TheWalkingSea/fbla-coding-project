import psycopg2 as pgdriver
import logging

logger = logging.getLogger(__name__)

class DatabaseAdapter:
    """ A Database adapter used to make code more robust """
    def __init__(self, conn: pgdriver.connection=None, **kwargs) -> None:
        self.db_params = kwargs
        self.conn = conn
        self.cursor = None if not self.conn else self.conn.cursor() # Set the cursor if self.conn exists
    
    def connect(self) -> None:
        """ Establishs a connection with the database using db_params passed during initialization """
        self.conn = pgdriver.connect(self.kwargs)
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query: str, params: tuple=None, commit: bool=True) -> None:
        """ 
        Executes a query with params. Logs an error if anything goes wrong
        
        Parameters:
        (str)query: The query to execute
        (tuple)params: Params that are substituted in the query to prevent SQL injection
        (bool)commit: Whether or not the change is committed to the db. This is useful when stacking queries
        
        """
        try:
            self.cursor.execute(query, vars=params)
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
        try:
            self.cursor.execute(query=query, vars=params)
            return self.cursor.fetchall()
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
        try:
            self.cursor.execute(query=query, vars=params)
            return self.cursor.fetchone()
        except Exception as e:
            logging.error("Something went wrong retrieving data; Query: %s; Params: %s; Exception: %s" % (query, params, e))
            return None

    def __del__(self) -> None:
        """ Closes the connections before deleting the class to prevent memory leaks """
        self.conn.close()
        self.cursor.close()

    def close(self) -> None:
        """ Closes the connections to the class """
        self.__del__()
