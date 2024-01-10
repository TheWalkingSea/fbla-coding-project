import inquirer
import sys
import os
import requests
from typing import Callable
from utils import validator
from openpyxl import Workbook
import re

IP = "http://127.0.0.1:8000"

def cls() -> None:
    """ Clears the cli menu when the user chooses to go to a new menu"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_contact_names(data: list[dict]) -> list[str]:
    """ Extracts all the contact names from contact data
     
    Parameters:
    (list[dict])data: A variable that represents contactdata
    
    Returns:
    (list[str]): A list of names extracted from the contactdata
    
    """
    return [contact['name'] for contact in data]

def get_contact_info(contact_pk: int) -> dict:
    """ Gets contact info from a contact_fk variable to lookup in the db
    
    Parameters:
    (int)contact_pk: A primary key that will retrieve contact info
    
    Returns:
    (dict): The contact info with a name, email, phone, and address field
    
    """
    response = requests.get("%s/api/contact/%s/" % (IP, contact_pk))
    return response.json()

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
        ret.append(get_contact_info(fk))
    return ret

def create_contact(payload: dict) -> int:
    """ Creates a contact give a payload with a name, phone, email, and address
    
    Parameters:
    (dict)payload: The payload to send to the server
    
    Returns:
    (int): An integer with the id of the contact
    
    """
    response = requests.post("%s/api/contact/" % IP, json=payload)
    return response.json()['id']

def get_all_contact_data() -> list[dict]:
    """ Gets all the contact data from the db 
    
    Returns:
    (list[dict]): A list of contact items from the database
    
    """
    response = requests.get("%s/api/contact/" % IP)
    return response.json()

def get_all_organization_data() -> list[dict]:
    """ Gets all the organization data from the db 
    
    Returns:
    (list[dict]): A list of organization items from the database
    
    """
    response = requests.get("%s/api/organization/" % IP)
    return response.json()

def update_value_contact(contact_id: int, key: str, value: str) -> None:
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


def contact_value_menu(contact_id: int, key: str, validator: Callable=None) -> None:
    """ Represents the cli menu for a value of an contact
     
    Parameters:
    (int)contact_id: The contact id in the database to edit
    (str)key: The value being updated
    (Callable)validator: A validation function that is optional but can be used to validate input
    
    """
    cls()
    q = [
        inquirer.Text(name="key", message=key.capitalize(), validate=True if not validator else lambda _, current: validator(current)),
        inquirer.Confirm("confirmation", message="Name: {key}?")
    ]
    answers = inquirer.prompt(q)
    if (answers['confirmation']):
        update_value_contact(contact_id, key, answers['key'])


# Organization

def organization_menu() -> None:
    """ Represents the organization interactive cli menu """
    cls()
    orgdata = get_all_organization_data()
    contactdata = get_contacts_info(orgdata)
    contactNames = get_contact_names(contactdata)
    
    q = [
        inquirer.List("organizations", message="Choose an organization to view", choices=[
            "Search"
            *contactNames,
            "Create Organization...",
            "Back"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['organizations']
    if (answer == "Search"):
        pass
    elif (answer == "Create Organization..."):
        create_organization_menu()
        organization_menu()
    elif (answer == "Back"):
        main() # Go back to main menu
    else:
        # This uses a sneaky trick with zip to make the contactNames as a key to the organization and contact data.
        # The contactName can be extracted from the prompt and we can extract the orgdata and contactdata to pass into show_organization
        orgdata, contactdata = dict(zip(contactNames, zip(orgdata, contactdata)))[answer]
        show_organization(answer, orgdata, contactdata)

def create_organization(payload: dict) -> None:
    """ Creates an organization object with a payload
    
    Parameters:
    (dict)payload: A payload with a description, type, url, and contact_fk
    
    """
    requests.post("%s/api/organization/" % IP, json=payload)

def create_organization_menu():
    """ Creates an organization with a prompt """
    cls()
    q = [
        inquirer.Text("name", "Name", validate=lambda _, x: validator.isNotNull(x)),
        inquirer.Text("type", "Type", validate=lambda _, x: validator.isNotNull(x)),
        inquirer.Text("description", "Description", validate=lambda _, x: validator.isNotNull(x)),
        inquirer.Text("url", "Website URL", validate=lambda _, x: validator.validate_url(x)),
        inquirer.Text("phone", "Phone", validate=lambda _, x: validator.validate_phone(x)),
        inquirer.Text("email", "Email", validate=lambda _, x: validator.validate_email(x)),
        inquirer.Text("address", "Address", validate=lambda _, x: validator.isNotNull(x))
    ]
    answers = inquirer.prompt(q)
    contact_payload = {
        "name": answers['name'],
        "phone": answers['phone'],
        "email": answers['email'],
        "address": answers['address']
    }
    contact_fk = create_contact(contact_payload)
    organization_payload = {
        "description": answers['description'],
        "type": answers['type'],
        "url": answers['url'],
        "contact_fk": contact_fk
    }
    create_organization(organization_payload)
    
def get_organization_data(organization_id: int) -> dict:
    """ Gets all organization data for a specific id 
    
    Parameters:
    (int)organization_id: The primary key for the organization
    
    Returns:
    (dict): The payload of the organization
    
    """
    response = requests.get("%s/api/organization/%s/" % (IP, organization_id))
    return response.json()

def delete_organization(organization_id: int) -> None:
    """ Deletes an organization from the database 
    
    Parameters:
    (int)organization_id: The id needed for the request
    
    """
    requests.delete("%s/api/organization/%s/" % (IP, organization_id))


def update_value_organization(organization_id: int, key: str, value: str) -> None:
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


def organization_value_menu(organization_id: int, key: str, validator: Callable=None) -> None:
    """ Represents the cli menu for a value of an organization
     
    Parameters:
    (int)organization_id: The organization id in the database to edit
    (str)key: The value being updated
    (Callable)validator: A validation function that is optional but can be used to validate input
    
    """
    cls()
    q = [
        inquirer.Text(name="key", message=key.capitalize(), validate=True if not validator else lambda _, current: validator(current)),
        inquirer.Confirm("confirmation", message="Name: {key}?")
    ]
    answers = inquirer.prompt(q)
    if (answers['confirmation']):
        update_value_organization(organization_id, key, answers['key'])

def show_organization(organization: str, orgdata: dict, contactdata: dict, back: Callable=organization_menu) -> None:
    """ Represents the cli menu for an organization
    
    Parameters:
    (str)organization: The name of the organization
    (dict)orgdata: The data of the organization from the db
    (dict)contactdata: The contact information data of the organization from the db
    (Callable)back: A function representing where the program should go if the user selects back; Default: organization_menu
    
    """
    cls()
    q = [
        inquirer.List("organization", message=organization, choices=[
            "Name: %s" % contactdata['name'],
            "Type: %s" % orgdata['type'],
            "Description: %s" % orgdata['description'],
            "Website URL: %s" % orgdata['url'],
            "Phone: %s" % contactdata['phone'],
            "Email: %s" % contactdata['email'],
            "Address: %s" % contactdata['address'],
            "Delete",
            "Back"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['organization']
    if (answer == "Back"):
        back()
        return
    elif (answer == "Delete"):
        delete_organization(orgdata['id'])
        back()
        return
    key = answer.split(":")[0]
    match key:
        case "Type" | "Description":
            organization_value_menu(orgdata['id'], key.lower(), validator=validator.isNotNull)
        case "Name" | "Address":
            contact_value_menu(orgdata['contact_fk'], key.lower(), validator=validator.isNotNull)
        case "Phone":
            contact_value_menu(orgdata['contact_fk'], key.lower(), validator=validator.validate_phone)
        case "Email":
            contact_value_menu(orgdata['contact_fk'], key.lower(), validator=validator.validate_email)
        case "Website URL":
            organization_value_menu(orgdata['id'], 'url', validator=validator.validate_url)
    organization_menu()

# PARTNERS
    

def get_all_partner_data() -> list[dict]:
    """ Gets all the partner data from the db 

    Returns:
    (list[dict]): A list of partner items from the database

    """
    response = requests.get("%s/api/partner/" % IP)
    return response.json()

def partner_menu() -> None:
    """ Represents the partner interactive cli menu """
    cls()
    partnerdata = get_all_partner_data()
    contactdata = get_contacts_info(partnerdata)
    contactNames = get_contact_names(contactdata)
    
    q = [
        inquirer.List("partners", message="Choose a partner to view", choices=[
            *contactNames,
            "Create Partner...",
            "Back"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['partners']
    if (answer == "Create Partner..."):
        create_partner_menu()
        partner_menu()
    elif (answer == "Back"):
        main() # Go back to main menu
    else:
        # This uses a sneaky trick with zip to make the contactNames as a key to the partner and contact data.
        # The contactName can be extracted from the prompt and we can extract the orgdata and contactdata to pass into show_partner
        partnerdata, contactdata = dict(zip(contactNames, zip(partnerdata, contactdata)))[answer]
        show_partner(answer, partnerdata, contactdata)

def create_partner(payload: dict) -> None:
    """ Creates an partner object with a payload
    
    Parameters:
    (dict)payload: A payload with a role, description, expertise, organization_fk, and contact_fk
    
    """
    requests.post("%s/api/partner/" % IP, json=payload)

def create_partner_menu():
    """ Creates an partner with a prompt """
    cls()

    orgdata = get_all_organization_data()
    contactdata = get_contacts_info(orgdata)
    contactNames = get_contact_names(contactdata) # All the names for the organizations

    q = [
        inquirer.Text("name", "Name", validate=lambda _, x: validator.isNotNull(x)),
        inquirer.Text("expertise", "Expertise", validate=lambda _, x: validator.isNotNull(x)),
        inquirer.Text("role", "Role", validate=lambda _, x: validator.isNotNull(x)),
        inquirer.Text("description", "Description", validate=lambda _, x: validator.isNotNull(x)),
        inquirer.Text("phone", "Phone", validate=lambda _, x: validator.validate_phone(x)),
        inquirer.Text("email", "Email", validate=lambda _, x: validator.validate_email(x)),
        inquirer.Text("address", "Address", validate=lambda _, x: validator.isNotNull(x)),
        inquirer.List(name="organizations", message="Organization", choices=contactNames)
    ]


    answers = inquirer.prompt(q)

    # Gets the organization_fk usign a trick with zip that maps the contact names as a key (output from prompt) to a list of organization id's
    # The organization ids are found by getting the 'id' field from every item in contactdata
    organization_fk = dict(zip(contactNames, list(map(lambda x:x['id'], contactdata))))[answers['organizations']]

    contact_payload = {
        "name": answers['name'],
        "phone": answers['phone'],
        "email": answers['email'],
        "address": answers['address']
    }
    contact_fk = create_contact(contact_payload)
    partner_payload = {
        "description": answers['description'],
        "role": answers['role'],
        "expertise": answers['expertise'],
        "contact_fk": contact_fk,
        "organization_fk": organization_fk
    }
    create_partner(partner_payload)
    


def delete_partner(partner_id: int) -> None:
    """ Deletes an partner from the database 
    
    Parameters:
    (int)partner_id: The id needed for the request
    
    """
    requests.delete("%s/api/partner/%s/" % (IP, partner_id))


def update_value_partner(partner_id: int, key: str, value: str) -> None:
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


def partner_value_menu(partner_id: int, key: str, validator: Callable=None) -> None:
    """ Represents the cli menu for a value of an partner
     
    Parameters:
    (int)partner_id: The partner id in the database to edit
    (str)key: The value being updated
    (Callable)validator: A validation function that is optional but can be used to validate input
    
    """
    cls()
    q = [
        inquirer.Text(name="key", message=key.capitalize(), validate=True if not validator else lambda _, current: validator(current)),
        inquirer.Confirm("confirmation", message="Name: {key}?")
    ]
    answers = inquirer.prompt(q)
    if (answers['confirmation']):
        update_value_partner(partner_id, key, answers['key'])

def partner_organization_value_menu(partner_id: int) -> None:
    """ Represents the cli for editing a partner's organization which requires a multiselect 
    
    Parameters:
    (int)partner_id: The partners id to edit
    
    """
    cls()

    orgdata = get_all_organization_data()
    contactdata = get_contacts_info(orgdata)
    contactNames = get_contact_names(contactdata) # All the names for the organizations

    q = [
        inquirer.List(name="organizations", message="Organization",
        choices=[
            *contactNames,
            "Back"
        ]
        )
    ]
    answers = inquirer.prompt(q)
    answer = answers['organizations']
    if (answer == "Back"):
        return
    else:
        # Gets the organization_fk usign a trick with zip that maps the contact names as a key (output from prompt) to a list of organization id's
        # The organization ids are found by getting the 'id' field from every item in contactdata
        organization_fk = dict(zip(contactNames, list(map(lambda x:x['id'], orgdata))))[answer]
        update_value_partner(partner_id, "organization_fk", organization_fk)




def show_partner(partner: str, partnerdata: dict, contactdata: dict, back: Callable=partner_menu) -> None:
    """ Represents the cli menu for a partner
    
    Parameters:
    (str)partner: The name of the partner
    (dict)partnerdata: The data of the partner from the db
    (dict)contactdata: The contact information data of the partner from the db
    (Callable)back: A function representing where the program should go if the user selects back; Default: partner_menu
    
    """
    cls()
    organization_contact_id = get_organization_data(partnerdata['organization_fk'])['contact_fk']
    q = [
        inquirer.List("partner", message=partner, choices=[
            "Name: %s" % contactdata['name'],
            "Role: %s" % partnerdata['role'],
            "Description: %s" % partnerdata['description'],
            "Expertise: %s" % partnerdata['expertise'],
            "Organization: %s" % get_contact_info(organization_contact_id)['name'],
            "Phone: %s" % contactdata['phone'],
            "Email: %s" % contactdata['email'],
            "Address: %s" % contactdata['address'],
            "Delete",
            "Back"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['partner']
    if (answer == "Back"):
        back()
        return
    elif (answer == "Delete"):
        delete_partner(partnerdata['id'])
        back()
        return
    key = answer.split(":")[0]
    match key:
        case "Organization":
            partner_organization_value_menu(partnerdata['id'])
        case "Description" | "Expertise":
            partner_value_menu(partnerdata['id'], key.lower(), validator=validator.isNotNull)
        case "Name" | "Address":
            contact_value_menu(partnerdata['contact_fk'], key.lower(), validator=validator.isNotNull)
        case "Phone":
            contact_value_menu(partnerdata['contact_fk'], key.lower(), validator=validator.validate_phone)
        case "Email":
            contact_value_menu(partnerdata['contact_fk'], key.lower(), validator=validator.validate_email)
    partner_menu()

def create_report() -> None:
    """ Creates a full Excel report and exports to export.xlsx """
    wb = Workbook()
    ws = wb.active
    orgdata = get_all_organization_data()
    partnerdata = get_all_partner_data()
    contactdata = get_all_contact_data()

    def get_contact(contact_id: int) -> dict:
        """ Gets contact data for a certain partner_id using the contact data above 
        
        Parameters:
        (int)contact_id: The id of the partner
        
        Returns:
        (dict): The data from the db
        
        """
        return list(filter(lambda x:x['id'] == contact_id, contactdata))[0]
    
    ws.append(['Type', 'Name', 'Description', 'Email', 'Address', 'Phone', "Expertise", 'Role', 'Type', 'URL'])
    for organization in orgdata:
        orgcontact = get_contact(organization['contact_fk'])
        ws.append([
            'Organization',
            orgcontact['name'], 
            organization['description'], 
            orgcontact['email'], 
            orgcontact['address'], 
            orgcontact['phone'], 
            '', 
            '', 
            organization['type'], 
            organization['url']
        ])
        for partner in filter(lambda x: x['organization_fk'] == organization['id'], partnerdata):
            partnercontact = get_contact(partner['contact_fk'])
            ws.append([
                'Partner', 
                partnercontact['name'], 
                partner['description'], 
                partnercontact['email'], 
                partnercontact['address'], 
                partnercontact['phone'], 
                partner['expertise'],
                partner['role'],
                '',
                ''
            ])
        ws.append(['']*10)




    wb.save("export.xlsx")


def main() -> None:
    """ Represents the main menu for the cli """
    cls()
    q = [
        inquirer.List("main", message="Welcome to EduVision Collaborator Platform", choices=[
            "Organizations",
            "Partners",
            "Create Report",
            "Exit"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['main']
    
    match answer:
        case "Organizations":
            cls()
            organization_menu()
        case "Partners":
            cls()
            partner_menu()
        case "Create Report":
            create_report()
            print("Report exported to export.xlsx...")
        case "Exit":
            sys.exit(0)
        



if __name__ == "__main__":
    main()