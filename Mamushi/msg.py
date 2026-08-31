
from decimal import ROUND_DOWN
from os import EX_CANTCREAT
from enum import Enum, auto


class Msg:
    #I guess saying that this defines the "type" is the best
    #Every message inherits this base structure
    pass

class keyType(Enum):
    RUNES   = auto()
    ENTER   = auto()
    BACKSPACE = auto()
    TAB   = auto()
    SPACE   = auto()
    ESCAPE   = auto()
    CTRL   = auto()
    UP   = auto()
    DOWN = auto()
    LEFT   = auto()
    RIGHT   = auto()
    UNDEFINED   = auto()

class keyMsg(Msg):
    #Reads 1 byte from stdIn
    
    def __init__(self, type: keyType, char:str=None, runes: str=None):
        self.char = char
        self.type = type
        self.runes = runes
        
    def is_ctrl(self, key: str) -> bool:
        return self.type == keyType.CTRL and self.char == key.lower()
        
        
    def __repr__(self):
        if self.type == keyType.RUNES:
            return f"keyMsg({self.runes!r})" # !r forces python to return the value as text
        if self.type == keyType.CTRL:
            return f"keyMsg(CTRL + {self.char!r})"
        return f"keyMsg({self.type.name!r})"
    
class quitMsg(Msg):
    
    #when receiving this message the program does a clean stop()
    pass