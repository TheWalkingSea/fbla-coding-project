import requests # TEMP
IP = "" # TEMP
import db_handler

def get_names(data: list[dict]) -> list[str]:
    """ Extracts all the contact names from contact data
     
    Parameters:
    (list[dict])data: A variable that represents contactdata
    
    Returns:
    (list[str]): A list of names extracted from the contactdata
    
    """
    return [contact['name'] for contact in data]

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
        ret.append(db_handler.get_info(fk))
    return ret