from database import conn

def get_all_data() -> list[dict]:
    """ Gets all the partner data from the db 

    Returns:
    (list[dict]): A list of partner items from the database

    """
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM partner")
    if (not result): return None
    return [dict(row) for row in result]

def create(payload: dict) -> None:
    """ Creates an partner object with a payload
    
    Parameters:
    (dict)payload: A payload with a role, description, expertise, organization_fk, and contact_fk
    
    """
    cursor = conn.cursor()

    cursor.execute("INSERT INTO partner (role, description, expertise, organization_fk, contact_fk) VALUES (?, ?, ?, ?, ?)", (
        payload['role'],
        payload['description'],
        payload['expertise'],
        payload['organization_fk'],
        payload['contact_fk']
    ))
    conn.commit()

def get_data(partner_id: int) -> dict:
    """ Gets all partner data for a specific id 
    
    Parameters:
    (int)partner_id: The primary key for the partner
    
    Returns:
    (dict): The payload of the partner
    
    """
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM partner WHERE id=?", (partner_id,))
    return None if not result else dict(result.fetchone())

def delete(partner_id: int) -> None:
    """ Deletes an partner from the database 
    
    Parameters:
    (int)partner_id: The pk for the partner
    
    """
    contact_id = get_data(partner_id)['contact_fk']
    cursor = conn.cursor()

    cursor.execute("DELETE FROM partner WHERE id=?", (partner_id,))
    cursor.execute("DELETE FROM contact WHERE id=?", (contact_id,))

    conn.commit()


def update_value(partner_id: int, key: str, value: str) -> None:
    """ Updates a value in an partner object in the database 
    
    Parameters:
    (int)partner_id: The partner to update
    (str)key: The key to update
    (str)value: The value for the key 
    
    """
    query = f"UPDATE partner SET {key}=? WHERE id=?" # Safe since key is not managed by user
    cursor = conn.cursor()
    cursor.execute(query, (value, partner_id))
    conn.commit()