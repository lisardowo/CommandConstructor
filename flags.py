NOT_DEFINED_REPETITIONS = 1

class flagsMixin: 
    
    @staticmethod
    def _buildFlagsString(selectedFlags: list) -> str:
        parts = []
        for f in selectedFlags:
            count = f.get("count", 1)
            flag = f.get("flag", "")
            if count > 1:
                parts.append(f"{flag}{count}")
            else:
                parts.append(flag) # This WILL duplicate the flag
        return " ".join(parts)

    @staticmethod
    def _isRepeatable(flagData: dict) -> bool: # specific flag
        if not flagData.get("repeatable", False):
            return False
        return flagData.get("max_repeats", NOT_DEFINED_REPETITIONS) > 1 # comparing it to 1 prevents misconfigurations (P.E: the flag set as repeatable but it allows only 1 repeats (by definition is not repeatable)) 
    
    @staticmethod
    def _maxRepeats(flagData: dict) -> int:
        if not flagData.get("repeatable", False):
            return 1
        return flagData.get("max_repeats", NOT_DEFINED_REPETITIONS)
    @staticmethod
    
    def _flattenFlags(commandData: dict):
        flags = []
        for category in commandData.get("categories", []):
            flags.extend(category.get("flags", []))
        return flags
    
    
if __name__ == '__main__':
    flags = [
        {"flag": "--verbose", "count": 2},
        {"flag": "--retry", "count": 0}
    ]
    test = flagsMixin()
    
    print(test._buildFlagsString(flags)) 