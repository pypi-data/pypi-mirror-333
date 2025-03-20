"""Transformer model."""

from ..name import generator as name
from ..haircolor import generator as haircolor
from ..eyecolor import generator as eyecolor
from ..initializer import init

class CharBox:
    @staticmethod
    def init(show_credits: bool = True) -> None:
        """
        Initializes the CharBox library.
        """
        init(show_credits=show_credits)

class Name:
    """
    The Name module of CharBox library.
    """
    @staticmethod
    def generate_first_name(gender: str = "male", origin: str = "American") -> str:
        """
        Generates a random first name.
        
        Args:
            gender (str, optional): The gender of the name. Defaults to "male". Can be "male" or "female".
            origin (str, optional): The origin of the name. Defaults to "American". Can be "American", "Japanese", "Korean", "German", or "Russain".
            
        Returns:
            str: The generated first name.
        """
        return name.generate_first_name(gender=gender, origin=origin)
    
    @staticmethod
    def generate_last_name(origin: str = "American") -> str:
        """
        Generates a random last name.

        Args:
            origin (str, optional): The origin of the name. Defaults to "American". Can be "American", "Japanese", "Korean", "German", or "Russain".
        
        Returns:
        str: The generated last name.
        """
        return name.generate_last_name(origin=origin)

    @staticmethod
    def generate_name(gender: str = "male", origin: str = "American") -> str:
        """
        Generates a random name.
        
        Args:
            gender (str, optional): The gender of the name. Defaults to "male". Can be "male" or "female"
            origin (str, optional): The origin of the name. Defaults to "American". Can be "American", "Japanese", "Korean", "German", or "Russain".
            
        Returns:
            str: The generated name.
        """
        return name.generate_name(gender=gender, origin=origin)

class HairColor:
    """
    The HairColor module of CharBox library.
    """
    @staticmethod
    def generate_hair_color(wording: str = "standard") -> str:
        """
        Generates a random hair color based on the specified type.
        
        Args:
            wording (str, optional): The wording type for the hair color. Defaults to "standard". Can be "standard" or "fancy".
        
        Returns:
        str: The generated hair color.
        """
        return haircolor.generate_hair_color(wording=wording)

    @staticmethod
    def translate(hair_color: str) -> str:
        """
        Translates a hair color to a more readable format.

        Args:
            hair_color (str): The hair color to translate.

        Returns:
            str: The translated hair color.
        """
        return haircolor.translate(hair_color)

class EyeColor:
    """
    The EyeColor module of CharBox library.
    """
    @staticmethod
    def generate_eye_color(wording: str = "standard") -> str:
        """
        Generates a random eye color based on the specified type.

        Args:
            wording (str, optional): The wording type for the eye color. Defaults to "standard". Can be "standard" or "fancy".

        Returns:
        str: The generated eye color.
        """
        return eyecolor.generate_eye_color(wording=wording)

    @staticmethod
    def translate(eye_color: str) -> str:
        """
        Translates a eye color to a more readable format.

        Args:
            eye_color (str): The eye color to translate.

        Returns:
            str: The translated eye color.
        """
        return eyecolor.translate(eye_color)