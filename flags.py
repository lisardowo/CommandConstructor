NOT_DEFINED_REPETITIONS = 1

class flagsMixin: 
    
    @staticmethod
    def _buildFlagsString(selectedFlags: list) -> str:
        parts = []
        for f in selectedFlags:
            count = f.get("count", 1)
            parts.extend([f.get("flag", "")] * max(count, 1))
        return " ".join(parts)
    @staticmethod
    def _hasRepeatableFlags(commandData: dict) -> bool: # whole commmand
        for category in commandData.get("categories", []):
                for flag in category.get("flags", []):
                    if flag.get("repeatable", False) and flag.get("max_repeats", 1 ) > 1:
                        return True
        return False
    @staticmethod
    def _isRepeatable(flagData: dict) -> bool: # specific flag
        if not flagData.get("repeatabla", False):
            return False
        return flagData.get("max_repeats", NOT_DEFINED_REPETITIONS) > 1 # comparing it to 1 prevents misconfigurations (P.E: the flag set as repeatable but it allows only 1 repeats (by definition is not repeatable)) 
    
    @staticmethod
    def _maxReapeats(flagData: dict) -> int:
        if not flagData.get("repeatable", False):
            return 1
        return flagData.get("max_repeats", NOT_DEFINED_REPETITIONS)
    @staticmethod
    
    def _flattenFlags(commandData: dict):
        flags = []
        for category in commandData.get("categories", []):
            flags.extend(category.get("flags", []))
        return flags