import requests
IP = ""

def get_all_data() -> list[dict]:
    """ Gets all the partner data from the db 

    Returns:
    (list[dict]): A list of partner items from the database

    """
    response = requests.get("%s/api/partner/" % IP)
    return response.json()

def create(payload: dict) -> None:
    """ Creates an partner object with a payload
    
    Parameters:
    (dict)payload: A payload with a role, description, expertise, organization_fk, and contact_fk
    
    """
    requests.post("%s/api/partner/" % IP, json=payload)


def delete(partner_id: int) -> None:
    """ Deletes an partner from the database 
    
    Parameters:
    (int)partner_id: The id needed for the request
    
    """
    requests.delete("%s/api/partner/%s/" % (IP, partner_id))


def update_value(partner_id: int, key: str, value: str) -> None:
    """ Updates a value in an partner object in the database 
    
    Parameters:
    (int)partner_id: The partner to update
    (str)key: The key to update
    (str)value: The value for the key 
    
    """
    json_data = {
        key: value
    }
    requests.patch("%s/api/partner/%s/" % (IP, partner_id), data=json_data)
