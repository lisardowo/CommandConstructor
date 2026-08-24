


import sys
import termios
import tty

def read_single_key():
  
    fd = sys.stdin.fileno() # save fd of stdin
    
    
    previousSettings = termios.tcgetattr(fd)
    
    
      
    tty.setraw(fd) # Switch the terminal to raw mode
    
    print("Raw mode active. Press any key (or 'q' to quit)...", end="", flush=True)
    reconstructedString = []
    while True:
        
        char = sys.stdin.read(1)
        if char == 'q':
         #   print("\r\nExiting raw mode...")
            break
        if char == '\r':
            #print("space!", end="", flush=True)
            continue
            reconstructedString += char 
        #print(f"\r\n You pressed: {repr(char)}", end="", flush=True)
        reconstructedString += char
        print(f"\r\n{"".join(reconstructedString)}", end = "", flush = True)
    # Restore previous settings
    termios.tcsetattr(fd, termios.TCSADRAIN, previousSettings)

if __name__ == "__main__":

    read_single_key()
