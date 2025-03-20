from .list import haircolors, haircolors_fancy, translations
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

def generate_hair_color(wording: str = "standard") -> str:
    """
    Generates a random hair color based on the specified type.
    
    Args:
        wording (str, optional): The wording type for the hair color. Defaults to "standard". Can be "standard" or "fancy".
    
    Returns:
    str: The generated hair color.
    """
    
    if not can_use:
        raise ModuleNotFoundError("No module named 'charbox.haircolor'")
    
    assert wording in ["standard", "fancy"], "Invalid wording type. Use 'standard' or 'fancy'."
    
    if wording == "standard":
        return random.choice(haircolors)
    elif wording == "fancy":
        return random.choice(haircolors_fancy)
    else:
        raise ValueError("Invalid wording type. Use 'standard' or 'fancy'.")

def translate(hair_color: str) -> str:
    """
    Translates a hair color to a more readable format.

    Args:
        hair_color (str): The hair color to translate.

    Returns:
        str: The translated hair color.
    """
    
    if not can_use:
        raise ModuleNotFoundError("No module named 'charbox.haircolor'")

    assert hair_color in translations, "Invalid hair color. Use a valid hair color from the [list](https://pypi.org/project/charbox/)."

    translation = translations.get(hair_color, None)

    if translation is not None:
        return translation
    else:
        raise ValueError("Invalid hair color. Use a valid hair color from the [list](https://pypi.org/project/charbox/).")