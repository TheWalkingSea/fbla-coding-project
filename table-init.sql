CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS partner
(
    partner_pk UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    role TEXT,
    description TEXT,
    expertise TEXT,
    organization_fk UUID,
    contact_fk UUID
);

CREATE TABLE IF NOT EXISTS organization
(
    organization_pk UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    description TEXT,
    type TEXT,
    url TEXT,
    contact_fk UUID
);

CREATE TABLE IF NOT EXISTS contact
(
    contact_pk UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT,
    phone VARCHAR(15),
    email TEXT,
    address TEXT
);

CREATE TABLE IF NOT EXISTS partner_tag
(
    partner_pk UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    tagname TEXT,
    tagcolor VARCHAR(6)
);

CREATE TABLE IF NOT EXISTS organization_tag
(
    organization_pk UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    tagname TEXT,
    tagcolor VARCHAR(6)
);

