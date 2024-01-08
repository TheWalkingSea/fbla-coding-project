import logging
from .adapter import DatabaseAdapter
from typing import Any
from psycopg2 import sql

logger = logging.getLogger(__name__)

class PkAdapter(DatabaseAdapter):
    """ Helps modify and retrieve data from a table with a primary key identifier """
    def __init__(self, pk: str, table: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pk = pk
        self.table = table
    
    def getField(self, fieldName: str) -> Any:
        """ Gets a field from the record specified by the pk 
        
        Parameters:
        (str)fieldName: A name for the column to select
        
        Returns:
        (Any): The data in that cell; Can be any data type depending on what is stored in the cell"""


        return self.fetchone("SELECT %s FROM %s WHERE %s_pk=%s", (fieldName, self.table, self.table, self.pk))

    def getFields(self) -> Any:
        """ Gets all fields for a row
        
        Returns:
        (Any): All the data in the row
        
        """
        keys = self.get_column_names(self.table)
        # values = self.fetchone(sql.SQL("SELECT * FROM {table} WHERE {tablepk}=%s").format(
        #         table=sql.Identifier(self.table),
        #         tablepk=sql.Identifier(self.table + "_pk")
        #     ), (self.pk,))
        values = [2]
        # return dict(zip(keys, list(values)))
        return {2: 3}
    
    def deleteRecord(self) -> None:
        """ Deletes the record with self.pk """
        logger.info("Deleting row with pk %s in table %s" % (self.pk, self.table))
        self.execute_query(sql.SQL("DELETE FROM {table} WHERE {tablepk}=%s").format(
                table=sql.Identifier(self.table), 
                tablepk=sql.Identifier(self.table + "_pk")
            ), (self.pk,))
    
    def updateRecord(self, fieldName: str, value: Any) -> None:
        """ Updates a record with a new value. This only updates one value 
        
        Parameters:
        (str)fieldName: The column which determines the cell to update the value with
        (Any)value: The value to update the cell with

        """
        self.execute_query("UPDATE %s SET %s=%s WHERE %s_pk=%s", (self.table, fieldName, value, self.table))
    
    def updateMultipleRecordValues(self, data: list[tuple]) -> None:
        """ Updates multiple cells with data. This function is similar to updateRecord but updates multiple values
        
        Parameters:
        (list[tuple])data: A list of tuples consisting of a fieldName and a value
        
        """
        for fieldName, value in data:
            self.execute_query("UPDATE %s SET %s=%s WHERE %s_pk=%s", (self.table, fieldName, value, self.table), commit=False)
        self.conn.commit()
    


