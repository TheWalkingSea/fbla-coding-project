from utils import util, validator
from . import db_handler
import inquirer
import contacts
from typing import Callable

def organization_menu(back: Callable, contactNames: list[str]=None) -> None:
    """ Represents the organization interactive cli menu
     
    Parameters:
    (Callable)back: A callback to the main function
    (list[str])contactNames: A list of contact names; Defaults to None and is retrieved from the server
      
    """
    util.cls()
    orgdata = db_handler.get_all_data()
    contactdata = contacts.get_contacts_info(orgdata)
    contactNames = contactNames or contacts.get_names(contactdata)

    
    q = [
        inquirer.List("organizations", message="Choose an organization to view", choices=[
            "Search",
            *contactNames,
            "Create Organization...",
            "Back"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['organizations']
    if (answer == "Search"):
        util.search_menu(filterList=contactNames, callback=organization_menu)
    elif (answer == "Create Organization..."):
        create_organization_menu()
        organization_menu()
    elif (answer == "Back"):
        back() # Go back to main menu
    else:
        # This uses a sneaky trick with zip to make the contactNames as a key to the organization and contact data.
        # The contactName can be extracted from the prompt and we can extract the orgdata and contactdata to pass into show_organization
        orgdata, contactdata = dict(zip(contactNames, zip(orgdata, contactdata)))[answer]
        show_organization(answer, orgdata, contactdata)


def create_organization_menu():
    """ Creates an organization with a prompt """
    util.cls()
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
    contact_fk = contacts.create(contact_payload)
    organization_payload = {
        "description": answers['description'],
        "type": answers['type'],
        "url": answers['url'],
        "contact_fk": contact_fk
    }
    db_handler.create(organization_payload)

    

def organization_value_menu(organization_id: int, key: str, validator: Callable=None) -> None:
    """ Represents the cli menu for a value of an organization
     
    Parameters:
    (int)organization_id: The organization id in the database to edit
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
        db_handler.update_value(organization_id, key, answers['key'])

def show_organization(organization: str, orgdata: dict, contactdata: dict, back: Callable=organization_menu) -> None:
    """ Represents the cli menu for an organization
    
    Parameters:
    (str)organization: The name of the organization
    (dict)orgdata: The data of the organization from the db
    (dict)contactdata: The contact information data of the organization from the db
    (Callable)back: A function representing where the program should go if the user selects back; Default: organization_menu
    
    """
    util.cls()
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
        db_handler.delete(orgdata['id'])
        back()
        return
    key = answer.split(":")[0]
    match key:
        case "Type" | "Description":
            organization_value_menu(orgdata['id'], key.lower(), validator=validator.isNotNull)
        case "Name" | "Address":
            contacts.value_menu(orgdata['contact_fk'], key.lower(), validator=validator.isNotNull)
        case "Phone":
            contacts.value_menu(orgdata['contact_fk'], key.lower(), validator=validator.validate_phone)
        case "Email":
            contacts.value_menu(orgdata['contact_fk'], key.lower(), validator=validator.validate_email)
        case "Website URL":
            organization_value_menu(orgdata['id'], 'url', validator=validator.validate_url)
    organization_menu()