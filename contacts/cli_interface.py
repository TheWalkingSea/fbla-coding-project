from utils.util import cls
from typing import Callable
import inquirer
from . import db_handler

def value_menu(contact_id: int, key: str, validator: Callable=None) -> None:
    """ Represents the cli menu for a value of an contact
     
    Parameters:
    (int)contact_id: The contact id in the database to edit
    (str)key: The value being updated
    (Callable)validator: A validation function that is optional but can be used to validate input
    
    """
    cls()
    q = [
        inquirer.Text(name="key", message=key.capitalize(), validate=True if not validator else lambda _, current: validator(current)),
        inquirer.Confirm("confirmation", message="Name: {key}?")
    ]
    answers = inquirer.prompt(q)
    if (answers['confirmation']):
        db_handler.update_value(contact_id, key, answers['key'])