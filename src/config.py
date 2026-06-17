import json
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class AppSettings:
    save_directory: str = str(Path.home() / "FIFA_Inspirational_Stories")
    output_format: str = "both"
    auto_start: bool = False
    show_on_startup: bool = True
    last_story_date: str = ""
    current_story_index: int = 0


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".fifa_inspirational"
        self.config_file = self.config_dir / "settings.json"
        self.config_dir.mkdir(exist_ok=True)
        self.settings = self.load()

    def load(self) -> AppSettings:
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                return AppSettings(**data)
            except Exception:
                pass
        return AppSettings()

    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(asdict(self.settings), f, indent=2)

    def get(self) -> AppSettings:
        return self.settings

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        self.save()