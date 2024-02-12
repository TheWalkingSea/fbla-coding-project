import sys
import organization
import partner
import contacts
from openpyxl import Workbook

def create_report() -> None:
    """ Creates a full Excel report and exports to export.xlsx """
    wb = Workbook()
    ws = wb.active
    orgdata = organization.get_all_data()
    partnerdata = partner.get_all_data()
    contactdata = contacts.get_all_data()

    def get_contact(contact_id: int) -> dict:
        """ Gets contact data for a certain partner_id using the contact data above 
        
        Parameters:
        (int)contact_id: The id of the partner
        
        Returns:
        (dict): The data from the db
        
        """
        return list(filter(lambda x:x['id'] == contact_id, contactdata))[0]
    
    ws.append(['Type', 'Name', 'Description', 'Email', 'Address', 'Phone', "Expertise", 'Role', 'Type', 'URL'])
    for org in orgdata:
        orgcontact = get_contact(org['contact_fk'])
        ws.append([
            'Organization',
            orgcontact['name'], 
            org['description'], 
            orgcontact['email'], 
            orgcontact['address'], 
            orgcontact['phone'], 
            '', 
            '', 
            org['type'], 
            org['url']
        ])
        for ptnr in filter(lambda x: x['organization_fk'] == org['id'], partnerdata):
            partnercontact = get_contact(ptnr['contact_fk'])
            ws.append([
                'Partner', 
                partnercontact['name'], 
                ptnr['description'], 
                partnercontact['email'], 
                partnercontact['address'], 
                partnercontact['phone'], 
                ptnr['expertise'],
                ptnr['role'],
                '',
                ''
            ])
        ws.append(['']*10)



    try:
        wb.save("export.xlsx")
    except PermissionError:
        input("Something went wrong when trying to access the export file. Please delete the file and try again.")
        sys.exit(-1)