

from Mamushi import terminal
from Mamushi.msg import keyType
import itertools

from Mamushi.colors import Colors
from Mamushi.msg import keyMsg
from Mamushi import commands
from getMenu import loadCommands

COLUMN_WIDTH = 60

class constructorModel:
   
    def __init__(self): # constructor of the object
        self.userinput = ""
        self.cursorPosition = 0
        self.matchedCommands = None
        self.selectedFlags = []
        self.commandDatabase = {}
        self.savedCommands = []
        
    def init(self): # loads the DB to memory
        self.commandDatabase = loadCommands()
        return None
    
    def update(self, msg):
        if not isinstance(msg, keyMsg):
            return None
        
        if msg.is_ctrl('q'):
            return commands.quit()
      
        match msg.type:
            case keyType.BACKSPACE:
                if self.cursorPosition > 0:
                    self.userinput = (self.userinput[:self.cursorPosition - 1] + self.userinput[self.cursorPosition:]) 
                    self.cursorPosition -=1
            case keyType.SPACE: 
                self.insertInCursor(' ')
            case keyType.RUNES:
                self.insertInCursor(msg.runes)
            case keyType.ENTER:
                if self.matchedCommands:
                    self.saveCommand() #TODO create func to save command
            case keyType.LEFT:
                self.cursorPosition = max(0, self.cursorPosition - 1)
                return None
            case keyType.RIGHT:
                self.cursorPosition = min(len(self.userinput), self.cursorPosition + 1)
                return None
            
        self._recompute()
        return None
    
    def view(self) -> str:
        lines = [f"> {self.userinput}", ""]
        
        if not self.matchedCommands:
            
            lines.append(Colors.applyColor("Command not recognized !", Colors.BRIGHT_RED))
            
            return "\n".join(lines)
        
        commandData = self.commandDatabase[self.matchedCommands]
        categories = commandData.get("categories", [])
        
        for flag in self.selectedFlags:
            selectedFlagKeys = {flag.get("flag", "")}
        
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
                lines.append(f"{leftLine.ljust(COLUMN_WIDTH)}{rightLine}") # todo update this to render sum colors
            lines.append("")
        
        if self.selectedFlags:
            
            flagsStr = " ".join(f.get("flag", "") for f in self.selectedFlags)
            lines.append(f"> {self.matchedCommands} {flagsStr} ") #Construct the output command
        
        if self.savedCommands:
            lines.append(" -- Saved Commands --")
            for saved in self.savedCommands:
                lines.append(f" {saved['command']}")
                if saved.get("description"):
                    lines.append(f" {saved['description']}")
        return "\n".join(lines)
    
    def _renderInputLine(self) -> str:
        before = self.userinput[: self.cursorPosition]
        underCursor = self.userinput[self.cursorPosition : self.cursorPosition + 1] or " "
        after = self.userinput[self.cursorPosition + 1:]
        return f"> {before}{terminal.reverseCursor(underCursor)}{after}"
    
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
        seenIndices = set()
        
        for token in tokens[1:]: #from 2nd element on because 0 is the command
            if token.isdigit():
                idx = int(token) - 1
                if 0 <= idx < len(allFlags):
                    selected.append(allFlags[idx]) # n from input should be an n in the range of all the flags of the command
                    seenIndices.add(idx)
        self.selectedFlags = selected
    
    def saveCommand(self):
        flagsStr = " ".join(f.get("flag", "") for f in self.selectedFlags)
        commandStr = f"{self.matchedCommands} {flagsStr}".strip()
        
        description = self.commandDatabase.get(self.matchedCommands, {}).get("description", "")
        
        self.savedCommands.append({"command": commandStr, "description": description,})
    
    def insertInCursor(self, toInsert:str):
        self.userinput = self.userinput[: self.cursorPosition] + toInsert + self.userinput[self.cursorPosition :]
        self.cursorPosition += len(toInsert)

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
            flag = flag.get("flag", "")
            lines.append(f"{idx}) {tag} - ({flag})")
            idx += 1
        return lines, idx