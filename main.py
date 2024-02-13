import inquirer
import sys
from help.cli_interface import help_menu
from utils import util, report
import organization
import partner
from database.backup import backup # Also initialized database connection
import schedule

def main() -> None:
    """ Represents the main menu for the cli """

    schedule.every(1).days.do(backup) # Backups the database daily (Dynamic Backup feature) to /backups/

    util.cls()
    q = [
        inquirer.List("main", message="Welcome to EduVision Collaborator Platform", choices=[
            "Organizations",
            "Partners",
            "Create Report",
            "Help",
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
            report.report_menu()
            print("Report exported to export.xlsx...")
        case "Help":
            help_menu()
        case "Exit":
            sys.exit(0)
        



if __name__ == "__main__":
    main()