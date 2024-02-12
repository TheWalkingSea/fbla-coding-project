import re
import requests
import os
import inquirer
from typing import Callable

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

def cls() -> None:
    """ Clears the cli menu when the user chooses to go to a new menu"""
    os.system('cls' if os.name == 'nt' else 'clear')


def search_menu(filterList: list[str], callback: Callable) -> None:
    """ Presents a search menu where the user enters a query, in which it is filtered and callback is called with the list as an argument
    
    Parameters:
    (list[str])filterList: The complete list of queries that will be filtered through
    (Callable)callback: A function with one argument being the filtered list
    
    """
    q = [
        inquirer.Text("search", "Enter A Search Query...")
    ]
    answers = inquirer.prompt(q)
    answer = answers['search']
    if (answer == ""):
        callback(filterList)
        return
    filteredList = search_function(answer, filterList)
    callback(filteredList)