from typing import Dict, List

# List of common natural eye colors
eyecolors: List[str] = [
    "Amber",
    "Blue",
    "Brown",
    "Gray",
    "Green",
    "Hazel",
    "Red",
    "Violet",
    "Black"
]

# List of fancy or uncommon eye colors
eyecolors_fancy: List[str] = [
    "Amber",
    "Blue",
    "Brown",
    "Gray",
    "Green",
    "Hazel",
    "Red",
    "Violet",
    "Black",
    "Sapphire",  # Deep Blue
    "Emerald",  # Bright Green
    "Amethyst",  # Purple
    "Rose Quartz",  # Pink
    "Golden",  # Intense Yellow
    "Aquamarine",  # Cyan
    "Cerulean",  # Aqua Blue
    "Azure",  # Sky Blue
    "Lavender",  # Soft Purple
    "Crimson",  # Deep Red
    "Turquoise",  # Blue-Green
    "Chartreuse",  # Yellow-Green
    "Periwinkle",  # Blue-Lavender
    "Indigo",  # Deep Blue-Violet
    "Obsidian",  # Pure Black
    "Silver",  # Metallic Gray
    "Opal",  # Iridescent Multicolor
]

# Dictionary for mapping fancy names to basic eye colors
translations: Dict[str, str] = {
    "Amber": "Golden Brown",
    "Blue": "Blue",
    "Brown": "Brown",
    "Gray": "Gray",
    "Green": "Green",
    "Hazel": "Brown-Green",
    "Red": "Red",
    "Violet": "Purple",
    "Black": "Black",
    "Sapphire": "Deep Blue",
    "Emerald": "Bright Green",
    "Amethyst": "Purple",
    "Rose Quartz": "Pink",
    "Golden": "Yellow",
    "Aquamarine": "Cyan",
    "Cerulean": "Aqua Blue",
    "Azure": "Sky Blue",
    "Lavender": "Soft Purple",
    "Crimson": "Deep Red",
    "Turquoise": "Blue-Green",
    "Chartreuse": "Yellow-Green",
    "Periwinkle": "Blue-Lavender",
    "Indigo": "Deep Blue-Violet",
    "Obsidian": "Pure Black",
    "Silver": "Metallic Gray",
    "Opal": "Iridescent Multicolor",
}