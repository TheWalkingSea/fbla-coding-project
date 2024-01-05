import logging
from .adapter import DatabaseAdapter
from typing import Any

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
    
    def deleteRecord(self) -> None:
        """ Deletes the record with self.pk """
        logger.info("Deleting row with pk %s in table %s" % (self.pk, self.table))
        self.execute_query("DELETE FROM %s WHERE %s_pk=%s", (self.table, self.table, self.pk))
    
    def updateRecord(self, fieldName: str, value: Any) -> None:
        """ Updates a record with a new value. This only updates one value """
        self.execute_query("UPDATE %s SET %s=%s WHERE %s_pk=%s", (self.table, fieldName, value, self.table))
    
    def updateMultipleRecordValues(self, list)


    def createRecord(self) -> None: # Abstract method
        raise NotImplementedError
    
    


