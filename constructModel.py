
import itertools

from Mamushi.msg import KeyMsg
from Mamushi import commands
from getMenu import loadCommands

COLUMN_WIDTH = 40

class constructorModel:
   
    def __init__(self): # constructor of the object
        self.userinput = ""
        self.matchedCommands = None
        self.selectedFlags = []
        self.commandDatabase = {}
    
    def init(self): # loads the DB to memory
        self.commandDatabase = loadCommands()
        return None
    
    def update(self, msg):
        if not isinstance(msg, KeyMsg):
            return None
        
        char = msg.char
        
        if char == "\x11":
            return commands.quit()
        
        if char in ("\r", "\n"):
            
            if self.matchedCommands:
                self.saveCommand() #TODO create func to save command
            
            return None
        if char == "\x7f":
            self.userinput = self.userinput[:-1]
        elif char.isprintable():
            self.userinput += char
            
        self._recompute()
        return None
    
    def view(self) -> str:
        lines = [f"> {self.userinput}", ""]
        
        if not self.matchedCommands:
            lines.append("Command not recognized !")
            
            return "\n".join(lines)
        
        commandData = self.commandDatabase[self.matchedCommands]
        categories = commandData.get("categories", [])
        
        globalIndex = 1
        blocks = []
        for category in categories: 
            
            block, globalIndex = self._renderCategoryBlock(category, globalIndex)
            blocks.append(block)
            
        left = blocks[0::2]
        right = blocks[1::2]
        
        for categoryLeft, categoryRight in itertools.zip_longest(left,right, fillvalue = []):
            maxRows = max(len(categoryLeft), len(categoryRight))
            for i in range(maxRows):
                if i < len(categoryLeft):
                    leftLine = categoryLeft[i]
                else:
                    leftLine = ""
                if i < len(categoryRight):
                    rightLine = categoryRight[i]
                else:
                    rightLine = ""
                lines.append(f"{leftLine.ljust(COLUMN_WIDTH)}{rightLine}")
            lines.append("")
        
        if self.selectedFlags:
            for f in self.selectedFlags:
                flagsStr = " ".join(f.get("flag", ""))
                lines.append(f"{self.matchedCommands} {flagsStr}")
        
        return "\n".join(lines)
    
    def _reset(self):
        
        self.userinput = ""
        self.matchedCommands = None
        self.selectedFlags = []
        
    def _recompute(self):
        
        tokens = self.userinput.split()
        if not tokens:
            
            self.matchedCommands = None
            self.selectedFlags = []
            
            return
        
        commandName = tokens[0]
        if commandName in self.commandDatabase:
            self.matchedCommands = commandName
        else:
            self.matchedCommands = None
        
        if self.matchedCommands is None:
            self.selectedFlags = []
            return
        
        allFlags = self._flattenFlags(self.commandDatabase[self.matchedCommands])
        
        selected = []
        
        for token in tokens[1:]: #from 2nd element on because 0 is the command
            if token.isdigit():
                idx = int(token) - 1
                if 0 <= idx < len(allFlags):
                    selected.append(allFlags[idx]) # n from input should be an n in the range of all the flags of the command
        
        self.selectedFlags = selected
    
    @staticmethod
    
    def _flattenFlags(commandData: dict):
        flags = []
        for category in commandData.get("categories", []):
            flags.extend(category.get("flags", []))
        return flags
    
    @staticmethod
    
    def _renderCategoryBlock(category: dict, startIndex: int):
        lines = [f"-- {category.get('name', "unable to find name")} --"]
        idx = startIndex
        for flag in category.get("flags", []):
            tag = flag.get("name", "")
            #flag = flag.get("flag", "")
            lines.append(f"{idx}) {tag}")
            idx += 1
        return lines, idx