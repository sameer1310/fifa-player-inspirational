import json
import os
from datetime import date
from pathlib import Path


def get_stories_path():
    # Works both when run from source and from PyInstaller bundle
    base = Path(getattr(__import__('sys'), '_MEIPASS', Path(__file__).parent.parent))
    return base / "stories" / "players.json"


def load_stories():
    with open(get_stories_path(), "r", encoding="utf-8") as f:
        return json.load(f)


def get_today_story():
    stories = load_stories()
    today = date.today().isoformat()
    for story in stories:
        if story["date"] == today:
            return story
    # Fallback: cycle by day-of-year index if no exact date match
    day_index = date.today().timetuple().tm_yday % len(stories)
    return stories[day_index]


def get_story_by_index(index):
    stories = load_stories()
    return stories[index % len(stories)]


def get_all_stories():
    return load_stories()
