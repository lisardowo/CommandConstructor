class Colors:
    #AI GENERATED ESCAPE CODES
    BLACK = "\033[38;5;0m"
    RED = "\033[38;5;1m"
    GREEN = "\033[38;5;2m"
    YELLOW = "\033[38;5;3m"
    BLUE = "\033[38;5;4m"
    MAGENTA = "\033[38;5;5m"
    CYAN = "\033[38;5;6m"
    WHITE = "\033[38;5;7m"
    
    BRIGHT_BLACK = "\033[38;5;8m"
    BRIGHT_RED = "\033[38;5;9m"
    BRIGHT_GREEN = "\033[38;5;10m"
    BRIGHT_YELLOW = "\033[38;5;11m"
    BRIGHT_BLUE = "\033[38;5;12m"
    BRIGHT_MAGENTA = "\033[38;5;13m"
    BRIGHT_CYAN = "\033[38;5;14m"
    BRIGHT_WHITE = "\033[38;5;15m"

  
    RESET = "\033[0m"

   
    # Dictionary to dinamically generate an specific color (by index)
    TEXT = {i: f"\033[38;5;{i}m" for i in range(256)}
    BG = {i: f"\033[48;5;{i}m" for i in range(256)}

    # Popular Colors
    ORANGE = TEXT[208]
    DARK_ORANGE = TEXT[166]
    PINK = TEXT[205]
    HOT_PINK = TEXT[198]
    PURPLE = TEXT[93]
    VIOLET = TEXT[129]
    TEAL = TEXT[30]
    TURQUOISE = TEXT[45]
    LIME = TEXT[118]
    GOLD = TEXT[220]
    BROWN = TEXT[94]
    
    CHARCOAL = TEXT[235]
    DARK_GRAY = TEXT[240]
    MID_GRAY = TEXT[245]
    LIGHT_GRAY = TEXT[250]
    SILVER = TEXT[252]

    #Text Modifiers
    STRIKETHROUGH = "\033[9m"
    
    @staticmethod
    def applyColor(string:str, color:str):
        return f"{color}{string}{Colors.RESET}"
    
    @staticmethod
    def strikethrough(string: str):
        return f"{Colors.STRIKETHROUGH}{string}{Colors.RESET}"
    
    