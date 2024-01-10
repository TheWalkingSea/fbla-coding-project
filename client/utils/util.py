import re

def search_function(query: str, searchList: list[str]) -> list[str]:
    """ Implements a search function using a search list and query.
    
    Parameters:
    (str)query: The string to search/query for.
    (list[str])searchList: A list of strings that will be searched through
    
    Returns:
    (list[str]): List of filtered words
    
    """
    return list(filter(lambda x: re.search(query, x, re.IGNORECASE), searchList))