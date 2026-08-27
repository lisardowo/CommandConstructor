"""

claude is CLAVE

"""
 
from .model import BaseModel
from .msg import KeyMsg
from . import commands
from .program import Program
 
 
class CounterModel(BaseModel):
    def __init__(self):
        self.contador = 0
 
    def update(self, msg):
        if isinstance(msg, KeyMsg):
            if msg.char == "q":
                return commands.quit()
            elif msg.char == "j":
                self.contador -= 1
            elif msg.char == "k":
                self.contador += 1
        return None
 
    def view(self) -> str:
        return (
            "=== Demo mamushi.Program ===\n"
            "\n"
            f"Counter: {self.contador}\n"
            "\n"
            "j = substract   k = add   q = quit"
        )
 
 
def main():
    program = Program(CounterModel())
    program.run()
 
 
if __name__ == "__main__":
    main()
 
