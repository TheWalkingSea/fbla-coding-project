import re
from . import regex_patterns
from django.core.validators import validate_email as emailValidator
from django.core.exceptions import ValidationError

def validate_email(email: str) -> bool:
    """ Checks if the email is valid using djangos representation of the email validator because it is also checked server side
    
    Parameters:
    (str)email: The email to validate

    Returns:
    (bool): A boolean that represents whether the input is valid or not
    
    """
    try:
        emailValidator(email)
        return True
    except ValidationError:
        return False
    

def validate_url(url: str) -> bool:
    """ 
    Checks if the url is valud using a regex pattern from https://www.freecodecamp.org/news/how-to-write-a-regular-expression-for-a-url/
        
    Parameters:
    (str)email: The url to validate

    Returns:
    (bool): A boolean that represents whether the input is valid or not
    
    """
    return bool(re.fullmatch(regex_patterns.URL_REGEX_PATTERN, url))

def validate_phone(phone: str) -> bool:
    """ 
    Checks if the phone number is valud using a regex pattern from https://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number
        
    Parameters:
    (str)email: The phone number to validate

    Returns:
    (bool): A boolean that represents whether the input is valid or not
    
    """
    return bool(re.fullmatch(regex_patterns.PHONE_REGEX_PATTERN, phone))


def isNotNull(text: str) -> bool:
    """ 
    Checks if the value is null or not
    
    Parameters:
    (str)text: The text to check
    
    Returns:
    (bool): A boolean representing whether its empty or not
    
    """
    return bool(text)