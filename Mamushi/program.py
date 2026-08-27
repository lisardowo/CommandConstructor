import sys 
import tty
import termios

from .render import Renderer
from .msg import Msg, KeyMsg, QuitMsg
from .model import Model

class Program:
    
    def __init__(self, model: Model, useProgramScreen: bool = True):
        self.model = model
        self.renderer = Renderer(useProgramScreen=useProgramScreen)
    
    def _dispatch(self, msg: Msg) -> bool:
        
        if isinstance(msg, QuitMsg):
            return False # if receives a quit msg returns a signal to terminate the program
        
        cmd = self.model.update(msg)
        
        if cmd is not None:
            result = cmd()
            if result is not None:
                return self._dispatch(result)
            # commands can be concadenated with other msgs
            # if the command does not end, it recursively acts on it
        return True
    
    # =============== Actual program
    
    def run(self):
        fd = sys.stdin.fileno()
        previousSettings = termios.tcgetattr(fd)
        
        self.renderer.start()
        
        try:
            tty.setraw(fd)
            
            startCmd = self.model.init()
            if startCmd is not None:
                result = startCmd()
                if result is not None:
                    self._dispatch(result) # the fuck this does
            
            self.renderer.render(self.model.view())
            
            while True:
                char = sys.stdin.read(1)
                shouldContinue = self._dispatch(KeyMsg(char))
                
                self.renderer.render(self.model.view())
                
                if not shouldContinue:
                    break
        
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, previousSettings) # restart settings
            self.renderer.stop()
