


import sys
import termios
import tty
import commandConstructor

def printInRaw(currentString: str):
    strlen = len(currentString)
    i = 0
    while i < strlen:
        print(f"\r\033[K{currentString}", end="", flush=True)
        i+=1

def readTerminal():
  
    fd = sys.stdin.fileno() # save fd of stdin
    
    
    previousSettings = termios.tcgetattr(fd)
    
    
      
    tty.setraw(fd) # Switch the terminal to raw mode
    
    print("Raw mode active. Press any key (or 'q' to quit)...", end="", flush=True)
    reconstructedString = ""
    while True:
        
        char = sys.stdin.read(1)
        match char:
            case _ if char == '\x11':
                break 
            case _:
                reconstructedString += char 
        print(f"/r/n{char}", end = "", flush = True)
        printInRaw(reconstructedString)
        
        
        match reconstructedString:
            case _ if "nmap" in reconstructedString:
                commandConstructor.constructNmap()
    
    # Restore previous settings
    termios.tcsetattr(fd, termios.TCSADRAIN, previousSettings)