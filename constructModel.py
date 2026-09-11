
from flags import flagsMixin

from Mamushi import terminal
from Mamushi.msg import keyType
import itertools
import re
from Mamushi.colors import Colors
from Mamushi.msg import keyMsg
from Mamushi import commands
from getMenu import loadCommands

REPEAT_MARKER = " \u27f3"
NOT_DEFINED_REPETITIONS = 1
COLUMN_WIDTH = 60
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")

def _visibleLength(text: str) -> int:
    return len(ANSI_ESCAPE_RE.sub("",text))
    
    
def _visualLjust(text: str, width: int) -> str:
    padding = width - _visibleLength(text)
    if padding > 0 :
        return text + (" " * padding)
    return text

class constructorModel(flagsMixin): # Uses inheritance of the mixin to use the helpers methods for parsing and understanding the flags while keeping a cleaner code base 
   
    def __init__(self): # constructor of the object
        self.userinput = ""
        self.cursorPosition = 0
        self.matchedCommands = None
        self.selectedFlags = []
        self.commandDatabase = {}
        self.savedCommands = []
        
        
    def init(self): # loads the DB to memory
                    #TODO on init the program should read history file and construct the history
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
                    #self._reset()
            case keyType.LEFT:
                self.cursorPosition = max(0, self.cursorPosition - 1)
                return None
            case keyType.RIGHT:
                self.cursorPosition = min(len(self.userinput), self.cursorPosition + 1)
                return None
            
        self._recompute()
        return None
    
    def view(self) -> str:
        lines = [self._renderInputLine(), ""]
        
        if not self.matchedCommands:
            
            lines.append(Colors.applyColor("Command not recognized !", Colors.BRIGHT_RED))
            
            return "\n".join(lines)
        
        commandData = self.commandDatabase[self.matchedCommands]
        categories = commandData.get("categories", [])
        
        selectedCounts = {
            flag.get("flag", ""): flag.get("count", 1) for flag in self.selectedFlags
        }
        
        repeatHint = self._repeatableHint()
        
        if repeatHint:
            lines.append(Colors.applyColor(repeatHint, Colors.YELLOW))
            lines.append("")
        
        #selectedFlagKeys = {flag.get("flag", ""):flag.get("count", NOT_DEFINED_REPETITIONS) for flag in self.selectedFlags} # 1 as a fallback for no specified number of repetitions 
        
        globalIndex = 1
        blocks = []
        for category in categories: 
            
            block, globalIndex = self._renderCategoryBlock(category, globalIndex, selectedCounts)
            blocks.append(block)
            
        left = blocks[0::2] # this truncates to two columns
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
                lines.append(f"{_visualLjust(leftLine, 70)}{rightLine}")
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
        self.cursorPosition = 0
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
        
        order = []
        counts = {}
        
        for token in tokens[1:]: #from 2nd element on because 0 is the command
            if token.isdigit():
                idx = int(token) - 1
                if 0 <= idx < len(allFlags):
                    flagData = allFlags[idx] # n from input should be an n in the range of all the flags of the command
                    isRepeatable = self._isRepeatable(flagData)
                    maxRepeats = self._maxReapeats(flagData)
                
                    if idx not in counts:
                        counts[idx] = 0 
                        order.append(idx) 
                
                    if isRepeatable:
                        if counts[idx] < maxRepeats: #TODO < or <=
                            counts[idx] += 1
            elif ";" in token:
                parts = token.split(";")
                idx = int(parts[0]) - 1
                if 0 <= idx < len(allFlags):
                    
                    flagData = allFlags[idx]
                    maxRepeats = self._maxReapeats(flagData)
                    
                    if idx not in counts:
                        counts[idx] = 0 
                        order.append(idx)
                    parts[1] = 3#TODO debug parts value
                    if self._isRepeatable(flagData):
                        if counts[idx] + int(parts[1]) <= maxRepeats: #TODO Less or less equal?
                            counts[idx] += int(parts[1])
        
        selected = []
        for idx in order:
            flagData = dict(allFlags[idx])
            flagData["count"] = counts[idx]
            selected.append(flagData)

                            
        self.selectedFlags = selected
    
    def saveCommand(self):
        #TODO implement save to history file
        flagsStr = " ".join(f.get("flag", "") for f in self.selectedFlags)
        commandStr = f"{self.matchedCommands} {flagsStr}".strip()
        
        description = self.commandDatabase.get(self.matchedCommands, {}).get("description", "")
        displayString = f"command: {commandStr}, description: {description},"
        
        self.savedCommands.append(displayString)
    
        with open(".commandsHist.txt", "a") as history:
            history.write(displayString) #TODO read the history in the file when the tool start
    
    def insertInCursor(self, toInsert:str):
        self.userinput = self.userinput[: self.cursorPosition] + toInsert + self.userinput[self.cursorPosition :]
        self.cursorPosition += len(toInsert)


    @staticmethod
    
    def _renderCategoryBlock(category: dict, startIndex: int, selectedCounts: set):
        lines = [f"-- {category.get('name', 'name not found')} --"]
        idx = startIndex
        for flag in category.get("flags", []):
            tag = flag.get("name", "")
            
            flagKey = flag.get("flag", "")
            maxRepeats = flag.get("max_repeats", 1)
            isRepeatable = flag.get("repeatable", False) and maxRepeats > 1
            
            marker = f"{REPEAT_MARKER}(max {maxRepeats})" if isRepeatable else ""
            label = f"{idx}) {tag} - ({flagKey}){marker}"
            
            count = selectedCounts.get(flagKey, 0)
            if count > 0:
                if isRepeatable:
                    
                    isMaxed = count >= maxRepeats
                    suffix = f" x{count}/{maxRepeats}"
                    label = Colors.applyColor(f"{label}{suffix}", Colors.GREEN)
                    
                    if isMaxed:
                        suffix += " (Max reached)"
                        label = Colors.applyColor(label, Colors.RED)
                        label = Colors.strikethrough(label)
                else:
                    label = Colors.strikethrough(Colors.applyColor(label, Colors.RED))
                
            lines.append(label)
            idx += 1
        return lines, idx

    def _repeatableHint(self) -> str:
        repeatableSelected = [f for f in self.selectedFlags if self._isRepeatable(f)]
        if not repeatableSelected:
            return ""
        examples = []
        for f in repeatableSelected:
            examples.append(
                f" {f.get('max_repeats', NOT_DEFINED_REPETITIONS)} times"
            )#TODO show how to repeat (syntax) 
        return "Selected flag is repeatable =>" + " | ".join(examples)

