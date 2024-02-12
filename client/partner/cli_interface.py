from utils import util, validator
import inquirer
from . import db_handler
from typing import Callable
import contacts
import organization


def partners_menu(back: Callable, contactNames: list[str]=None) -> None:
    """ Represents the partner interactive cli menu. (Shows ALL partners)
           
    Parameters:
    (Callable)back: A callback to the main function
    (list[str])contactNames: A list of contact names; Defaults to None and is retrieved from the server 
    
    """
    util.cls()
    partnerdata = db_handler.get_all_data()
    contactdata = contacts.get_contacts_info(partnerdata)
    contactNames = contactNames or contacts.get_names(contactdata)
    
    q = [
        inquirer.List("partners", message="Choose a partner to view", choices=[
            "Search",
            *contactNames,
            "Create Partner...",
            "Back"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['partners']
    if (answer == "Search"):
        util.search_menu(filterList=contactNames, callback=partners_menu)
    elif (answer == "Create Partner..."):
        create_partners_menu()
        partners_menu()
    elif (answer == "Back"):
        back() # Go back to main menu
    else:
        # This uses a sneaky trick with zip to make the contactNames as a key to the partner and contact data.
        # The contactName can be extracted from the prompt and we can extract the orgdata and contactdata to pass into show_partner
        partnerdata, contactdata = dict(zip(contactNames, zip(partnerdata, contactdata)))[answer]
        show_partner(answer, partnerdata, contactdata)


def create_partners_menu():
    """ Creates an partner with a prompt """
    util.cls()

    orgdata = organization.get_all_data()
    contactdata = contacts.get_contacts_info(orgdata)
    contactNames = contacts.get_names(contactdata) # All the names for the organizations

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
    contact_fk = contacts.create(contact_payload)
    partner_payload = {
        "description": answers['description'],
        "role": answers['role'],
        "expertise": answers['expertise'],
        "contact_fk": contact_fk,
        "organization_fk": organization_fk
    }
    db_handler.create(partner_payload)

def partner_value_menu(partner_id: int, key: str, validator: Callable=None) -> None:
    """ Represents the cli menu for a value of an partner
     
    Parameters:
    (int)partner_id: The partner id in the database to edit
    (str)key: The value being updated
    (Callable)validator: A validation function that is optional but can be used to validate input
    
    """
    util.cls()
    q = [
        inquirer.Text(name="key", message=key.capitalize(), validate=True if not validator else lambda _, current: validator(current)),
        inquirer.Confirm("confirmation", message="Name: {key}?")
    ]
    answers = inquirer.prompt(q)
    if (answers['confirmation']):
        db_handler.update_value(partner_id, key, answers['key'])

def partner_organization_value_menu(partner_id: int) -> None:
    """ Represents the cli for editing a partner's organization which requires a multiselect 
    
    Parameters:
    (int)partner_id: The partners id to edit
    
    """
    util.cls()

    orgdata = organization.get_all_data()
    contactdata = contacts.get_contacts_info(orgdata)
    contactNames = contacts.get_names(contactdata) # All the names for the organizations

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
        db_handler.update_value(partner_id, "organization_fk", organization_fk)




def show_partner(partner: str, partnerdata: dict, contactdata: dict, back: Callable=partners_menu) -> None:
    """ Represents the cli menu for ONE partner.
    
    Parameters:
    (str)partner: The name of the partner
    (dict)partnerdata: The data of the partner from the db
    (dict)contactdata: The contact information data of the partner from the db
    (Callable)back: A function representing where the program should go if the user selects back; Default: partners_menu
    
    """
    util.cls()
    organization_contact_id = organization.get_data(partnerdata['organization_fk'])['contact_fk']
    organization_name = contacts.get_info(organization_contact_id)['name']
    q = [
        inquirer.List("partner", message=partner, choices=[
            "Name: %s" % contactdata['name'],
            "Role: %s" % partnerdata['role'],
            "Description: %s" % partnerdata['description'],
            "Expertise: %s" % partnerdata['expertise'],
            "Organization: %s" % organization_name,
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
        db_handler.delete(partnerdata['id'])
        back()
        return
    key = answer.split(":")[0]
    match key:
        case "Organization":
            partner_organization_value_menu(partnerdata['id'])
        case "Description" | "Expertise":
            partner_value_menu(partnerdata['id'], key.lower(), validator=validator.isNotNull)
        case "Name" | "Address":
            contacts.value_menu(partnerdata['contact_fk'], key.lower(), validator=validator.isNotNull)
        case "Phone":
            contacts.value_menu(partnerdata['contact_fk'], key.lower(), validator=validator.validate_phone)
        case "Email":
            contacts.value_menu(partnerdata['contact_fk'], key.lower(), validator=validator.validate_email)
    partners_menu()
