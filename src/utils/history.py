import json
from pathlib import Path

HISTORY_FILE = Path("data/history.json")

HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

if not HISTORY_FILE.exists():
    HISTORY_FILE.write_text("[]")


def load_history():

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(record):

    history = load_history()

    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def clear_history():

    with open(HISTORY_FILE, "w") as file:
        json.dump([], file)


def latest_records(limit=10):

    history = load_history()

    return history[-limit:]