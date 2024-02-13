from database import conn
import partner

def create(payload: dict) -> None:
    """ Creates an organization object with a payload
    
    Parameters:
    (dict)payload: A payload with a description, type, url, and contact_fk
    
    """
    cursor = conn.cursor()
    cursor.execute("INSERT INTO organization (description, type, url, contact_fk) VALUES (?, ?, ?, ?)", (
        payload['description'],
        payload['type'],
        payload['url'],
        payload['contact_fk']
    ))
    conn.commit()

def get_all_data() -> list[dict]:
    """ Gets all the organization data from the db 
    
    Returns:
    (list[dict]): A list of organization items from the database
    
    """
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM organization")
    if (not result): return None
    return [dict(row) for row in result]

def get_data(organization_id: int) -> dict:
    """ Gets all organization data for a specific id 
    
    Parameters:
    (int)organization_id: The primary key for the organization
    
    Returns:
    (dict): The payload of the organization
    
    """
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM organization WHERE id=?", (organization_id,))
    return None if not result else dict(result.fetchone())

def delete(organization_id: int) -> None:
    """ Deletes an organization from the database 
    
    Parameters:
    (int)organization_id: The id needed for the request
    
    """
    contact_id = get_data(organization_id)['contact_fk']

    cursor = conn.cursor()

    cursor.execute("DELETE FROM organization WHERE id=?", (organization_id,))
    cursor.execute("DELETE FROM contact WHERE id=?", (contact_id,))
    
    result = cursor.execute("SELECT id FROM partner WHERE organization_fk=?", (organization_id,))
    if (not result): 
        conn.commit()
        return # Nothing is connected to the organization so return
    for row in result.fetchall():
        partner_id = dict(row)['id']

        contact_id = partner.get_data(partner_id)['contact_fk']
        cursor = conn.cursor()

        cursor.execute("DELETE FROM partner WHERE id=?", (partner_id,))
        cursor.execute("DELETE FROM contact WHERE id=?", (contact_id,))

    conn.commit()


def update_value(organization_id: int, key: str, value: str) -> None:
    """ Updates a value in an organization object in the database 
    
    Parameters:
    (int)organization_id: The organization to update
    (str)key: The key to update
    (str)value: The value for the key 
    
    """
    query = f"UPDATE organization SET {key}=? WHERE id=?" # Safe since key is not managed by user
    cursor = conn.cursor()
    cursor.execute(query, (value, organization_id))
    conn.commit()