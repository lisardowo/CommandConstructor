import sys

ESC = "\x1b"

def hideCursor():
    sys.stdout.write(f"{ESC}[?25l")

def showCursor():
    sys.stdout.write(f"{ESC}[?25h")

def moveCursor(row: int, column: int = 1) -> str:
    return f"{ESC}[{row};{column}H"

def clearLine() -> str:
    return f"{ESC}[2K"

def clearScreen():
    sys.stdout.write(f"{ESC}[2J{ESC}[H")
    
def enterProgramScreen():
    #something real nice I learn why doing this is that vim and programs like that use an alternate screen buffer to keep the terminal as it was
    sys.stdout.write(f"{ESC}[?1049h")
    
def exitProgramScreen():
    sys.stdout.write(f"{ESC}[?1049l")

def reverseCursor(text: str):
    return f"{ESC}[7m{text}{ESC}[0m"