import inquirer
import getpass
from utils import util

def print_instructions() -> None:
    """ Prints instructions using getpass. It will show an input box (except they can't type) and when they click enter it will return to the main menu """
    util.cls()
    getpass.getpass("EduVision is a command line interface that stores information about business and community partners. \
You can navigate to the organizations page which will show businesses in our area and selecting a business will show you information regarding the business such as contact info and their website name. \
You can also navigate to the partners page which will show partners that work for businesses. You can select a partner to show contact info, the business they are associated with, \
and information about their role in the business. Finally, you can create a full customizable report about businesses and partners that will export to an excel file.\nPress enter to exit.")

def q_and_a_menu() -> None:
    """ Represents the Q&A menu to help the user navigate the site """
    
    q_a = {
        "What is the purpose of this program?": "The purpose of this program is to help the school's Career and Technical Education Department collect, store, and organize information safely about business and community partners with a stylish command line interface.",
        "How do I add an organization to the list?": "You can navigate to the Organizations page and use the down arrow to navigate to the 'Create Organization' option",
        "How do I add a partner to the list?": "You can navigate to the Partner page and use the down arrow to navigate to the 'Create Partner' option",
        "How do I see information regarding an organization or partner?": "You can navigate to the Organizations/Partners page and select on an item to view specifying info describing that particular partner or organization.",
        "How do I print out a report?": "Select 'Create Report' from the main menu!",
        "Where is the exported report?": "It will be a Excel file named export.xlsx in the same folder as the program.",
        "Why does the program say that my input is invalid?": "Some inputs are validated by the program to ensure that all information is accurately inputted into the program. For example, phone numbers must be a valid international number without any exceptions or the number will not be accepted.",
        "How do I search through items?": "Select the 'Search' option and enter text to filter through and click enter. The results will be filtered through by name.",
        "How do I delete an organization/partner?": "Select the organization or partner from their respective menu and scroll down using the down arrow until you get the the 'Delete' option and click enter.",
        "Is my information shared with EduVision?": "All your information is stored safely in the program and is never shared with any of our servers. Your data is securely stored on your local computer and never makes contact with any of EduVision's servers.",
        "How often is my data backed up?": "Your data is backed up every 24 hours of the program's uptime.",
        "How do I backup my data?": "Your data is dynamically backed up by EduVision on your computer, so if any of your data was corrupted, then you can back it up with earlier versions of the database.",
        "Where are my backups located?": "Backups are located at /backups/ in the same folder as the program. This is to ensure that your backups are easily accessible at all times.",
        "How do I rollback my database from a backup?": "Delete the old database and move the backup the same folder as the program and rename it to db.sqlite3. This is the file that EduVision pulls from.",
        "Why does the CLI duplicate when I scroll": "Unfortunately due some problems with Windows, the CLI can bug out and cause duplicated lines when scrolling."
    }
    util.cls()
    q = [
        inquirer.List("q_a", message="Choose a question", choices=[
            *(q_a.keys()),
            "Back"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['q_a']
    if (answer == "Back"):
        help_menu() # Go back to the help menu
    else:
        util.cls()
        # Uses the getpass trick to show the text and have the enter to exit feature, but preventing the user from typing junk in the terminal
        getpass.getpass(q_a[answer] + "\nPress enter to exit.")
    help_menu()


def help_menu() -> None:
    """ Represents the help menu with instructions and Q&A options """

    util.cls()

    q = [
        inquirer.List("help", message="Choose a help option", choices=[
            "Instructions",
            "Q&A",
            "Back"
        ])
    ]
    answers = inquirer.prompt(q)
    answer = answers['help']
    if (answer == "Instructions"):
        print_instructions()
    elif (answer == "Q&A"):
        q_and_a_menu()

    # For every option they will go back to the main menu so I removed the if block for the BACK option as it was redundant
    from main import main # To prevent import looping errors
    main() # Go back to main menu