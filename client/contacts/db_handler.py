import requests # TEMP
IP = "" # TEMP


def get_info(contact_pk: int) -> dict:
    """ Gets contact info from a contact_fk variable to lookup in the db
    
    Parameters:
    (int)contact_pk: A primary key that will retrieve contact info
    
    Returns:
    (dict): The contact info with a name, email, phone, and address field
    
    """
    response = requests.get("%s/api/contact/%s/" % (IP, contact_pk))
    return response.json()

def create(payload: dict) -> int:
    """ Creates a contact give a payload with a name, phone, email, and address
    
    Parameters:
    (dict)payload: The payload to send to the server
    
    Returns:
    (int): An integer with the id of the contact
    
    """
    response = requests.post("%s/api/contact/" % IP, json=payload)
    return response.json()['id']

def get_all_data() -> list[dict]:
    """ Gets all the contact data from the db 
    
    Returns:
    (list[dict]): A list of contact items from the database
    
    """
    response = requests.get("%s/api/contact/" % IP)
    return response.json()

def update_value(contact_id: int, key: str, value: str) -> None:
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