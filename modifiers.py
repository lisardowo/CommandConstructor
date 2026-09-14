
from enum import Enum
 
 
TRIGGER_CHAR = "&"
 
 
class ViewMode(str, Enum):
    DEFAULT = "default"
    EXPLANATION = "explanation"
    USE_CASE = "use_case"
 
 
class ModifierResult:
 
    def __init__(self, viewMode: ViewMode | None = None, message: str = "", isError: bool = False):
        self.viewMode = viewMode
        self.message = message
        self.isError = isError
 
 
class ModifierEngine:

    _REGISTRY = {
        "e": {"viewMode": ViewMode.EXPLANATION, "help": "brief explanation of the flags"},
        "u": {"viewMode": ViewMode.USE_CASE, "help": "Use cases for each flag"},
    }
 
    HELP_COMMAND = "?"
 
    def __init__(self):
        self.isActive = False
        self.buffer = ""
        self.viewMode = ViewMode.DEFAULT
        self.lastMessage = ""
        self.lastWasError = False
 

    def activate(self):
        
        self.isActive = True
        self.buffer = ""
 
    def cancel(self):
       
        self.isActive = False
        self.buffer = ""
 
    def feedChar(self, char: str):
        if self.isActive:
            self.buffer += char
 
    def backspace(self):
        if not self.isActive:
            return
        if self.buffer:
            self.buffer = self.buffer[:-1]
        else:
            self.cancel()
 
    def execute(self) -> ModifierResult:
        if not self.isActive:
            return ModifierResult()
 
        command = self.buffer.strip().lower()
        self.isActive = False
        self.buffer = ""
 
        if command == self.HELP_COMMAND:
            result = ModifierResult(message=self.helpText())
            self._remember(result)
            return result
 
        entry = self._REGISTRY.get(command)
        if entry is None:
            message = (
                f"Unknown command: '{TRIGGER_CHAR}{command}' "
                f"(try {TRIGGER_CHAR}{self.HELP_COMMAND} for more help)"
            )
            result = ModifierResult(message=message, isError=True)
            self._remember(result)
            return result
 
        self.viewMode = entry["viewMode"]
        message = f"View: {entry['viewMode'].value} ({entry['help']})"
        result = ModifierResult(viewMode=entry["viewMode"], message=message)
        self._remember(result)
        return result
 
    def _remember(self, result: ModifierResult):
        self.lastMessage = result.message
        self.lastWasError = result.isError

    def helpText(self) -> str:
        lines = [
            f"{TRIGGER_CHAR}{key}  ->  {meta['help']}"
            for key, meta in self._REGISTRY.items()
        ]
        lines.append(f"{TRIGGER_CHAR}{self.HELP_COMMAND}  ->  shows this menu")
        return "\n".join(lines)
 
    def inputLineSuffix(self) -> str:
        if not self.isActive:
            return ""
        return f" {TRIGGER_CHAR}{self.buffer}"
        
    def renderPopup(self) -> str:

        typed = self.buffer
        title = f" Modifiers mode ({TRIGGER_CHAR}{typed}) "
        
        rows = []
        for key, meta in self._REGISTRY.items():
            matches = bool(typed) and key.startswith(typed)
            pointer = "→ " if matches else "  "
            rows.append(f"{pointer}{TRIGGER_CHAR}{key}   {meta['help']}")
        rows.append(f"  {TRIGGER_CHAR}{self.HELP_COMMAND}   shows this menu")
        rows.append("")
        rows.append("[Enter] confirm   [Backspace on empty] cancel")
        
        width = max(len(title), max(len(r) for r in rows)) + 2
        top = "┌" + "─" * width + "┐"
        titleLine = "│" + title.center(width) + "│"
        sep = "├" + "─" * width + "┤"
        body = [f"│ {r.ljust(width - 1)}│" for r in rows]
        bottom = "└" + "─" * width + "┘"
        
        return "\n".join([top, titleLine, sep, *body, bottom])

    @staticmethod
    def isTrigger(char: str) -> bool:
        return char == TRIGGER_CHAR
