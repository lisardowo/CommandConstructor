import json
import os
import sys

def loadCommands():
    dataDir="data"
    commandDatabase = {} 

    if not os.path.exists(dataDir):
        print(f"[ERROR] Unable to find {dataDir} ")
        sys.exit(1)
        
    for filename in os.listdir(dataDir):
        if filename.endswith(".json"):
            filepath = os.path.join(dataDir, filename)
            file = open(filepath, 'r', encoding='utf-8')
            data = json.load(file)
            
            if "command" in data:
                commandName = data["command"]
                commandDatabase[commandName] = data
    
    return commandDatabase

if __name__ == "__main__":
    
    print("[DEBUG] db: \n")
    db = loadCommands()
    
    print(f"commands: {list(db["nmap"].values())}")
    