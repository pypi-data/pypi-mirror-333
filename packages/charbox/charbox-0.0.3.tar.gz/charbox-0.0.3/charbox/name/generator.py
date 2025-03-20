from .dict import names
import random
import os
import inspect

can_use = False

def init() -> None:
    """
    Initializes the names package.
    """
    global can_use
    
    from .. import initializer
    AUTHORIZED_CALLERS = [f"{os.path.abspath(__file__)}", f"{initializer.__file__}"]
    
    stack = inspect.stack()
    caller_frame = stack[1]  # The direct caller
    caller_filename = caller_frame.filename.split("/")[-1]  # Extract file name only
    
    if caller_filename not in AUTHORIZED_CALLERS:
        raise PermissionError("You are not authorized to initialize this module. Please use the 'charbox.init()' function to initialize the package.")
    
    can_use = True
    return can_use

def generate_first_name(gender: str = "male", origin: str = "American") -> str:
    """
    Generates a random first name.
    
    Args:
        gender (str, optional): The gender of the name. Defaults to "male". Can be "male" or "female".
        origin (str, optional): The origin of the name. Defaults to "American". Can be "American", "Japanese", "Korean", "German", or "Russain".
        
    Returns:
        str: The generated first name.
    """
    
    if not can_use:
        raise ModuleNotFoundError("No module named 'charbox.names'")
    
    assert gender in ["male", "female"], "Gender must be either 'male' or 'female'."
    assert origin in names, "Origin must be one of the following: American, Japanese, Korean, German, or Russian."
    return random.choice(names[origin]["first"][gender])

def generate_last_name(origin: str = "American") -> str:
    """
    Generates a random last name.

    Args:
        origin (str, optional): The origin of the name. Defaults to "American". Can be "American", "Japanese", "Korean", "German", or "Russain".
    
    Returns:
    str: The generated last name.
    """
    
    if not can_use:
        raise ModuleNotFoundError("No module named 'charbox.names'")
    
    assert origin in names, "Origin must be one of the following: American, Japanese, Korean, German, or Russian."
    return random.choice(names[origin]["last"])

def generate_name(gender: str = "male", origin: str = "American") -> str:
    """
    Generates a random name.
    
    Args:
        gender (str, optional): The gender of the name. Defaults to "male". Can be "male" or "female"
        origin (str, optional): The origin of the name. Defaults to "American". Can be "American", "Japanese", "Korean", "German", or "Russain".
        
    Returns:
        str: The generated name.
    """
    
    if not can_use:
        raise ModuleNotFoundError("No module named 'charbox.names'")
    
    assert gender in ["male", "female"], "Gender must be either 'male' or 'female'."
    assert origin in names, "Origin must be one of the following: American, Japanese, Korean, German, or Russian."
    return f"{generate_first_name(gender, origin)} {generate_last_name(origin)}"