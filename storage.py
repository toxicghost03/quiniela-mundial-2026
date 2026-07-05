import json, os, pathlib

DATA_FILE = pathlib.Path("data.json")

def load():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except:
            pass
    return {"users": {}, "results": {}}

def save(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
