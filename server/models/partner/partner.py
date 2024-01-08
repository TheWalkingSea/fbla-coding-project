from db.pk import PkAdapter
import db
import uuid
from typing import Type
from psycopg2.extensions import connection

class Partner(PkAdapter):
    """ A model that represents a partner.
        partner_pk UUID,
        role TEXT,
        description TEXT,
        expertise TEXT,
        organization_fk UUID,
        contact_fk UUID
    """
    def __init__(self, pk: str=None, *args, **kwargs):
        super().__init__(pk, db.PARTNER, *args, **kwargs)
    
    @classmethod
    def build_partner(cls: Type["Partner"],
        conn: connection,
        role: str, 
        description: str, 
        expertise: str, 
        organization_fk: uuid.UUID, 
        contact_fk: uuid.UUID, 
        partner_pk: uuid.UUID=uuid.uuid4()
        ) -> "Partner":
        adapter = db.adapter.DatabaseAdapter(conn)
        adapter.execute_query("INSERT INTO partner VALUES (%s, %s, %s, %s, %s, %s)", 
            (partner_pk, 
            role, 
            description, 
            expertise, 
            organization_fk, 
            contact_fk))
        return cls(partner_pk, conn)


