from database import conn

def get_info(contact_pk: int) -> dict:
    """ Gets contact info from a contact_fk variable to lookup in the db
    
    Parameters:
    (int)contact_pk: A primary key that will retrieve contact info
    
    Returns:
    (dict): The contact info with a name, email, phone, and address field
    
    """
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM contact WHERE id=?", (contact_pk,))
    return None if not result else dict(result.fetchone())

def create(payload: dict) -> int:
    """ Creates a contact give a payload with a name, phone, email, and address
    
    Parameters:
    (dict)payload: The payload to send to the server
    
    Returns:
    (int): An integer with the id of the contact
    
    """
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contact (name, phone, email, address) VALUES (?, ?, ?, ?) RETURNING id", (
        payload['name'],
        payload['phone'],
        payload['email'],
        payload['address']
    ))
    contact_id = cursor.fetchone()[0]
    conn.commit()

    return contact_id

def get_all_data() -> list[dict]:
    """ Gets all the contact data from the db 
    
    Returns:
    (list[dict]): A list of contact items from the database
    
    """
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM contact")
    if (not result): return None
    return [dict(row) for row in result]

def update_value(contact_id: int, key: str, value: str) -> None:
    """ Updates a value in an contact object in the database 
    
    Parameters:
    (int)contact_id: The contact to update
    (str)key: The key to update
    (str)value: The value for the key 
    
    """
    query = f"UPDATE contact SET {key}=? WHERE id=?" # Safe since key is not managed by user
    cursor = conn.cursor()
    cursor.execute(query, (value, contact_id))
    conn.commit()