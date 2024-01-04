from . import regex_patterns
import re

def validate_email(email: str) -> bool:
    """ 
    Checks if the email is valid using a regex pattern in Perl's Mail::RFC822::Address module
    
    Parameters:
    (str)email: The email to validate

    Returns:
    (bool): A boolean that represents whether the input is valid or not
    
    """
    return bool(re.fullmatch(email, regex_patterns.EMAIL_REGEX_PATTERN))
    