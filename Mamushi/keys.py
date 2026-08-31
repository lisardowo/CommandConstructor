import select
from .msg import keyMsg, keyType

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

def read_key(stdinFd) -> keyMsg:
    
    char = stdinFd.read(1) 
    
    if char in escapeSequences:
        return keyMsg(escapeSequences[char])
    
    if char == "\x1b":
        return _read_escape_sequence(stdinFd)
    
    if char and ord(char) < 0x20: # CTRL + A = 0x01.. CTRL+Z = 0x1A
        char = chr(ord(char) + 0x60) # +60 Gets lower case
        return keyMsg(keyType.CTRL, char=char)
    if char.isprintable():
        return keyMsg(keyType.RUNES, runes=char)
    
    return keyMsg(keyType.UNDEFINED, runes=char)

def _read_escape_sequence(stdinFD) -> keyMsg:
    ready, _, _ = select.select([stdinFD], [], [], 0.01)
    if not ready:
        return keyMsg(keyType.ESCAPE)
    nextByte = stdinFD.read(1)
    if nextByte != "[":
        return keyMsg(keyType.UNDEFINED, runes=f"\x1b{nextByte}")

    code = stdinFD.read(1)
    if code in arrowsDirection:
        return keyMsg(arrowsDirection[code])
    
    return keyMsg(keyType.UNDEFINED, runes="\x1b{nextByte}")
