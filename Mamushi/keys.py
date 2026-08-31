from sys import stdin
import select
from .msg import keyMsg, keyType
import os

escapeSequences = {
    "\r": keyType.ENTER,
    "\n": keyType.ENTER,
    "\x7f": keyType.BACKSPACE,
    "\x08": keyType.BACKSPACE, # sum terminals use this variation
    "\t": keyType.TAB,
    " ": keyType.SPACE
}

arrowsDirection = {
    "A": keyType.UP,
    "B": keyType.DOWN,
    "C": keyType.RIGHT,
    "D": keyType.LEFT,
}

ESCAPECODE = "\x1b"

def _read_byte(fd: int) -> str:
    data = os.read(fd, 1)
    return data.decode(errors="replace")

def read_key() -> keyMsg:
    fd = stdin.fileno()
    char = _read_byte(fd)
    
    if char in escapeSequences:
        return keyMsg(escapeSequences[char])

    if char == ESCAPECODE:

        return _read_escape_sequence(fd)

    if char and ord(char) < 0x20: # CTRL + A = 0x01.. CTRL+Z = 0x1A
        char = chr(ord(char) + 0x60) # +60 Gets lower case
        return keyMsg(keyType.CTRL, char=char)
    if char.isprintable():
        return keyMsg(keyType.RUNES, runes=char)
    
    return keyMsg(keyType.UNDEFINED, runes=char)

def _read_escape_sequence(fd: int) -> keyMsg:
    ready, _, _ = select.select([fd], [], [], 0.01)
    if not ready:
        return keyMsg(keyType.ESCAPE)
 
    next_byte = _read_byte(fd)
    if next_byte != "[":
        return keyMsg(keyType.UNDEFINED, runes=f"\x1b{next_byte}")
 
    code = _read_byte(fd)
    if code in arrowsDirection:
        return keyMsg(arrowsDirection[code])
 
    return keyMsg(keyType.UNDEFINED, runes=f"\x1b[{code}")

