import db
import uuid
import psycopg2 as pgdriver
from typing import Type

class Organization(db.pk.PkAdapter):
    """ A model that represents an organization.
        organization_pk UUID,
        description TEXT,
        type TEXT,
        url TEXT,
        contact_fk UUID
    """
    def __init__(self, pk: str=None, *args, **kwargs):
        super().__init__(pk, db.ORGANIZATION, *args, **kwargs)
    
    @classmethod
    def build_partner(cls: Type["Organization"],
        conn: pgdriver.connection,
        description: str,
        type: str,
        url: str,
        contact_fk: uuid.UUID,
        organization_pk: uuid.UUID=uuid.UUID4()
        ) -> "Organization":
        adapter = db.adapter.DatabaseAdapter(conn)
        adapter.execute_query("INSERT INTO organization VALUES (%s %s %s %s %s)", 
            (organization_pk,
            description,
            type,
            url,
            contact_fk))
        return cls(organization_pk, conn)