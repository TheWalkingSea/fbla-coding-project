import re
import requests

def search_function(query: str, searchList: list[str]) -> list[str]:
    """ Implements a search function using a search list and query.
    
    Parameters:
    (str)query: The string to search/query for.
    (list[str])searchList: A list of strings that will be searched through
    
    Returns:
    (list[str]): List of filtered words

    """
    return list(filter(lambda x: re.search(query, x, re.IGNORECASE), searchList))


def check_wifi(ip: str="https://google.com") -> bool:
    """ Checks wifi availability 
    
    Parameters:
    (str)ip: The IP to test; Defaults to google

    Returns:
    (bool): A boolean that represents the wifi availability 
    
    """
    try:
        response = requests.get(ip, timeout=3)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False