from .list import eyecolors, eyecolors_fancy, translations
import random
import os
import inspect

can_use = False

def init() -> None:
    """
    Initializes the name package.
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

def generate_eye_color(wording: str = "standard") -> str:
    """
    Generates a random eye color based on the specified type.
    
    Args:
        wording (str, optional): The wording type for the eye color. Defaults to "standard". Can be "standard" or "fancy".
    
    Returns:
    str: The generated eye color.
    """
    
    if not can_use:
        raise ModuleNotFoundError("No module named 'charbox.eyecolor'")
    
    assert wording in ["standard", "fancy"], "Invalid wording type. Use 'standard' or 'fancy'."
    
    if wording == "standard":
        return random.choice(eyecolors)
    elif wording == "fancy":
        return random.choice(eyecolors_fancy)

def translate(eye_color: str) -> str:
    """
    Translates a eye color to a more readable format.

    Args:
        eye_color (str): The eye color to translate.

    Returns:
        str: The translated eye color.
    """
    
    if not can_use:
        raise ModuleNotFoundError("No module named 'charbox.eyecolor'")
    
    assert eye_color in translations, "Invalid eye color. Use a valid eye color from the [list](https://pypi.org/project/charbox/)."

    translation = translations.get(eye_color, None)

    if translation is not None:
        return translation
    else:
        raise ValueError("Invalid eye color. Use a valid eye color from the [list](https://pypi.org/project/charbox/).")