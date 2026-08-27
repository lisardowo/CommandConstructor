from typing import Callable, Optional
from .msg import Msg, QuitMsg

Cmd = Callable[[], Optional[Msg]]

def quit() -> Cmd:
    return lambda: QuitMsg