"""
autostart.py – Enable/disable launch-at-login on macOS and Windows.
"""
import sys
import os
from pathlib import Path


def _app_path():
    """Return the path to the running executable or script."""
    if getattr(sys, 'frozen', False):          # PyInstaller bundle
        return sys.executable
    return sys.argv[0]                         # running from source


class AutoStartHelper:
    def enable(self):
        if sys.platform == "darwin":
            self._mac_enable()
        elif sys.platform == "win32":
            self._win_enable()

    def disable(self):
        if sys.platform == "darwin":
            self._mac_disable()
        elif sys.platform == "win32":
            self._win_disable()

    # ── macOS – LaunchAgent plist ────────────────────────────────────────────
    def _plist_path(self):
        return Path.home() / "Library/LaunchAgents/com.fifainspirational.app.plist"

    def _mac_enable(self):
        plist = self._plist_path()
        plist.parent.mkdir(parents=True, exist_ok=True)
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fifainspirational.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>{_app_path()}</string>
        <string>--tray</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
"""
        plist.write_text(content)
        os.system(f"launchctl load '{plist}'")

    def _mac_disable(self):
        plist = self._plist_path()
        if plist.exists():
            os.system(f"launchctl unload '{plist}'")
            plist.unlink()

    # ── Windows – Registry run key ───────────────────────────────────────────
    def _win_enable(self):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "FIFAInspirational", 0, winreg.REG_SZ,
                              f'"{_app_path()}" --tray')
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[autostart] Windows registry error: {e}")

    def _win_disable(self):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, "FIFAInspirational")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[autostart] Windows registry error: {e}")
