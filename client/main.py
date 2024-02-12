import inquirer
import sys
import utils
from utils import util, report
import organization
import partner


IP = "http://GYD76GBCM7J0JFIEH2P46JD843HDC.asuscomm.com:8000"

def main() -> None:
    """ Represents the main menu for the cli """
    if (not utils.check_wifi(IP)):
        input("Wifi is not available. Please connect and try again.")
        sys.exit(-1)

    util.cls()
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
            util.cls()
            organization.organization_menu()
        case "Partners":
            util.cls()
            partner.partners_menu()
        case "Create Report":
            report.create_report()
            print("Report exported to export.xlsx...")
        case "Exit":
            sys.exit(0)
        



if __name__ == "__main__":
    main()