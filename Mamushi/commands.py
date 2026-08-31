from typing import Callable, Optional
from .msg import Msg, quitMsg

Cmd = Callable[[], Optional[Msg]]

def quit() -> Cmd:
    return lambda: quitMsg()