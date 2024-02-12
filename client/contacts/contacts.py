import requests # TEMP
IP = "" # TEMP

from typing import Callable
import inquirer
from ..utils.util import cls

def get_contact_names(data: list[dict]) -> list[str]:
    """ Extracts all the contact names from contact data
     
    Parameters:
    (list[dict])data: A variable that represents contactdata
    
    Returns:
    (list[str]): A list of names extracted from the contactdata
    
    """
    return [contact['name'] for contact in data]

def get_contact_info(contact_pk: int) -> dict:
    """ Gets contact info from a contact_fk variable to lookup in the db
    
    Parameters:
    (int)contact_pk: A primary key that will retrieve contact info
    
    Returns:
    (dict): The contact info with a name, email, phone, and address field
    
    """
    response = requests.get("%s/api/contact/%s/" % (IP, contact_pk))
    return response.json()

def get_contacts_info(data: list) -> list:
    """ Gets contact info for every item in the list of data
     
    Parameters:
    (list)data: Data that has contact_fk field (organization or partner data)
     
    Returns:
    (list): A list of contact info with a name, email, phone, and address fields
    
    """
    ret = []
    for item in data:
        fk = item['contact_fk']
        ret.append(get_contact_info(fk))
    return ret

def create_contact(payload: dict) -> int:
    """ Creates a contact give a payload with a name, phone, email, and address
    
    Parameters:
    (dict)payload: The payload to send to the server
    
    Returns:
    (int): An integer with the id of the contact
    
    """
    response = requests.post("%s/api/contact/" % IP, json=payload)
    return response.json()['id']

def get_all_contact_data() -> list[dict]:
    """ Gets all the contact data from the db 
    
    Returns:
    (list[dict]): A list of contact items from the database
    
    """
    response = requests.get("%s/api/contact/" % IP)
    return response.json()


def update_value_contact(contact_id: int, key: str, value: str) -> None:
    """ Updates a value in an contact object in the database 
    
    Parameters:
    (int)contact_id: The contact to update
    (str)key: The key to update
    (str)value: The value for the key 
    
    """
    json_data = {
        key: value
    }
    requests.patch("%s/api/contact/%s/" % (IP, contact_id), data=json_data)


def contact_value_menu(contact_id: int, key: str, validator: Callable=None) -> None:
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
        update_value_contact(contact_id, key, answers['key'])