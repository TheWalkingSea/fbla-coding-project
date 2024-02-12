import requests
IP = "http://GYD76GBCM7J0JFIEH2P46JD843HDC.asuscomm.com:8000"

def create(payload: dict) -> None:
    """ Creates an organization object with a payload
    
    Parameters:
    (dict)payload: A payload with a description, type, url, and contact_fk
    
    """
    requests.post("%s/api/organization/" % IP, json=payload)

def get_all_data() -> list[dict]:
    """ Gets all the organization data from the db 
    
    Returns:
    (list[dict]): A list of organization items from the database
    
    """
    response = requests.get("%s/api/organization/" % IP)
    return response.json()

def get_data(organization_id: int) -> dict:
    """ Gets all organization data for a specific id 
    
    Parameters:
    (int)organization_id: The primary key for the organization
    
    Returns:
    (dict): The payload of the organization
    
    """
    response = requests.get("%s/api/organization/%s/" % (IP, organization_id))
    return response.json()

def delete(organization_id: int) -> None:
    """ Deletes an organization from the database 
    
    Parameters:
    (int)organization_id: The id needed for the request
    
    """
    requests.delete("%s/api/organization/%s/" % (IP, organization_id))


def update_value(organization_id: int, key: str, value: str) -> None:
    """ Updates a value in an organization object in the database 
    
    Parameters:
    (int)organization_id: The organization to update
    (str)key: The key to update
    (str)value: The value for the key 
    
    """
    json_data = {
        key: value
    }
    requests.patch("%s/api/organization/%s/" % (IP, organization_id), data=json_data)
