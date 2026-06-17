"""
main.py  –  macOS menu bar (rumps) + subprocess viewer windows.
Each popup runs in its own process so a crash never kills the tray.
"""
import sys
import os
import subprocess
from pathlib import Path

ROOT   = Path(__file__).resolve().parent
PYTHON = sys.executable
VIEWER = str(ROOT / "viewer.py")

sys.path.insert(0, str(ROOT))


def _open(cmd: list):
    """Fire-and-forget subprocess — each window is fully independent."""
    subprocess.Popen(
        [PYTHON, VIEWER] + cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ── macOS rumps menu bar ───────────────────────────────────────────────────────
def run_macos():
    import rumps
    from src.config import ConfigManager
    from src.story_manager import get_all_stories

    config  = ConfigManager()
    stories = get_all_stories()

    # rumps submenu: must be a dict of {title: MenuItem}
    # The correct rumps API for a submenu is to assign a dict to self.menu[key]
    class FIFAApp(rumps.App):
        def __init__(self):
            super().__init__("⚽", quit_button=None)

            # Build flat menu — rumps submenus require special handling
            # We use a dedicated "Browse" item that opens the settings/browse window
            self.menu = [
                rumps.MenuItem("⚽  Today's Story",   callback=self.today),
                rumps.MenuItem("📖  Browse All Stories", callback=self.browse),
                None,
                rumps.MenuItem("⚙   Settings",        callback=self.open_settings),
                None,
                rumps.MenuItem("✖  Quit",             callback=self.quit_app),
            ]

            if config.settings.show_on_startup:
                t = rumps.Timer(self._show_today_once, 1)
                t.start()

        def _show_today_once(self, sender):
            sender.stop()
            _open(["story"])

        def today(self, _):
            _open(["story"])

        def browse(self, _):
            _open(["browse"])

        def open_settings(self, _):
            _open(["settings"])

        def quit_app(self, _):
            rumps.quit_application()

    FIFAApp().run()


# ── Windows pystray ────────────────────────────────────────────────────────────
def run_windows():
    from PIL import Image, ImageDraw
    import pystray
    from src.config import ConfigManager

    config = ConfigManager()

    def make_icon():
        img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([2, 2, 62, 62], fill=(0, 107, 60, 255))
        for x, y in [(24, 18), (38, 18), (44, 30), (32, 44), (18, 30)]:
            draw.ellipse([x-5, y-5, x+5, y+5], fill=(255, 255, 255, 220))
        return img

    menu = pystray.Menu(
        pystray.MenuItem("Today's Story",    lambda *_: _open(["story"]), default=True),
        pystray.MenuItem("Browse All Stories", lambda *_: _open(["browse"])),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Settings",         lambda *_: _open(["settings"])),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit",             lambda icon, _: icon.stop()),
    )

    icon = pystray.Icon("FIFA", make_icon(), "FIFA Inspirational Stories", menu)

    if config.settings.show_on_startup:
        import threading
        threading.Timer(1.0, lambda: _open(["story"])).start()

    icon.run()


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if sys.platform == "darwin":
        run_macos()
    elif sys.platform == "win32":
        run_windows()
    else:
        _open(["story"])
