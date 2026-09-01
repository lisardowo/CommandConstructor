import sys
from . import terminal

class Renderer:
    def __init__(self, useProgramScreen: bool = True):
        #Creates instance
        self._useProgramScreen = useProgramScreen
        self._previousLines: list[str] = []
        self._isStarted = False
        #private elements just for usage in the scope of the renderer

    def start(self):
        #setup the screen for drawing
        if self._useProgramScreen:
            terminal.enterProgramScreen()
        #TODO cursor buggg terminal.hideCursor()
        terminal.clearScreen()
        sys.stdout.flush() 
        
        self._isStarted = True
        self._previousLines = []
    
    def stop(self):
        #Returns terminal to std configuration
        terminal.showCursor()
        if self._useProgramScreen:
            terminal.exitProgramScreen()
        sys.stdout.flush()
        self._isStarted = False
        
    def render(self, frame: str):
        if not self._isStarted:
            sys.stdout.write("[WARNING] You must call .start() before first call to render")
            sys.stdout.flush() #TODO turn this into a proper error message/exception
            
        newLines = frame.split("\n")
        previousLines = self._previousLines
        
        buffer = []
        totalLines = max(len(newLines), len(previousLines))
        
        for i in range(totalLines):
            newLine = newLines[i] if i < len(newLines) else None
            previousLine = previousLines[i] if i < len(previousLines) else None
            
            if newLine == previousLine:
                continue # ignore lines without change
            
            row = i + 1 #ANSI is 1 indexed (1,1 is top left of the screen)
            buffer.append(terminal.moveCursor(row, 1)) #TODO harcorded one (column) may cause some problems
            buffer.append(terminal.clearLine())
            
            if newLine is not None:
                buffer.append(newLine)
        
        if buffer:
            sys.stdout.write("".join(buffer))
            sys.stdout.flush()
            
        self._previousLines = newLines
    
    def forceFullRedraw(self):
        #pretty self explanatory
        self._previousLines = []
        terminal.clearScreen()
        sys.stdout.flush() 