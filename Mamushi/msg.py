class Msg:
    #I guess saying that this defines the "type" is the best
    #Every message inherits this base structure
    pass

class KeyMsg(Msg):
    #Reads 1 byte from stdIn
    
    def __init__(self, char:str):
        self.char = char
        
    def __repr__(self):
        return f"KeyMsg({self.char!r})" # !r forces python to return the value as text

class QuitMsg(Msg):
    
    #when receiving this message the program does a clean stop()
    pass