"""
viewer.py  –  Standalone webview window launcher (called as subprocess).

Commands:
  python viewer.py story            -> today's story
  python viewer.py story <index>    -> story by 0-based index
  python viewer.py browse           -> browse all stories gallery
  python viewer.py settings         -> settings window
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.config import ConfigManager
from src.story_manager import get_today_story, get_all_stories, get_story_by_index
from src.popup import show_story_popup, show_settings_window, show_browse_window


def main():
    config = ConfigManager()
    args   = sys.argv[1:]

    mode = args[0] if args else "story"

    if mode == "story":
        if len(args) > 1:
            story = get_story_by_index(int(args[1]))
        else:
            story = get_today_story()
        show_story_popup(story, config)

    elif mode == "browse":
        show_browse_window(config)

    elif mode == "settings":
        from src.autostart import AutoStartHelper
        show_settings_window(config, AutoStartHelper())

    else:
        print(f"Unknown command: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
