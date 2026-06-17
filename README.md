# FIFA Player Inspirational Stories

> **One player. One story. Every day.**
> Daily inspirational stories from FIFA World Cup players with humble, unique backgrounds — delivered to your desktop.

---

## What it does

- Delivers a new inspiring story each day (June 16 – July 11, 2026) about a World Cup player
- Saves a beautifully formatted **Word document (.docx)** and/or **PowerPoint slide (.pptx)** to a folder you choose
- Lives quietly in your **system tray / menu bar** — right-click the ⚽ icon for access
- Optional **popup at startup** so the first thing you see each morning is that day's story
- Lets you **browse all 26 stories** at any time from the Settings panel

---

## Quick Start (run from source)

### Requirements
- Python 3.10 or later
- macOS or Windows

```bash
# 1. Clone / download the project
cd fifa-player-inspirational

# 2. Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# 3. Run the app
python main.py
```

A ⚽ icon appears in your menu bar (Mac) or system tray (Windows).

---

## Build a standalone app (no Python required for end users)

### macOS
```bash
chmod +x build_mac.sh
./build_mac.sh
# Output: dist/FIFAInspirational.app
# Drag to /Applications to install
```

### Windows
```bat
build_windows.bat
REM Output: dist\FIFAInspirational.exe
REM Copy anywhere and double-click
```

---

## How to use

| Action | How |
|---|---|
| See today's story | Double-click tray icon **or** right-click → "Today's Story" |
| Save story to disk | Click "Save as Word", "Save as Slide", or "Save Both" in the popup |
| Change save folder | Settings → Browse |
| Browse all stories | Right-click tray → "Browse All Stories" |
| Enable launch at login | Settings → check "Launch at login" |
| Disable startup popup | Settings → uncheck "Show story popup at startup" |
| Quit | Right-click tray → Quit |

---

## Sharing with coworkers

1. Build the `.app` (Mac) or `.exe` (Windows) using the build scripts above
2. Share the single file — no Python or other software needed on their machine
3. They double-click to run, choose their save folder, and optionally enable auto-start
4. Files are saved locally on their machine in their chosen folder

---

## Story Schedule (June 16 – July 11, 2026)

| Date | Player | Country |
|---|---|---|
| Jun 16 | Cristiano Ronaldo | Portugal |
| Jun 17 | Lionel Messi | Argentina |
| Jun 18 | Rui Costa | Cabo Verde |
| Jun 19 | Sadio Mané | Senegal |
| Jun 20 | N'Golo Kanté | France |
| Jun 21 | Mohamed Salah | Egypt |
| Jun 22 | Son Heung-min | South Korea |
| Jun 23 | Didier Drogba | Côte d'Ivoire |
| Jun 24 | Zlatan Ibrahimović | Sweden |
| Jun 25 | Gianluigi Buffon | Italy |
| Jun 26 | Luka Modrić | Croatia |
| Jun 27 | Kylian Mbappé | France |
| Jun 28 | Robert Lewandowski | Poland |
| Jun 29 | Keylor Navas | Costa Rica |
| Jun 30 | Neymar Jr. | Brazil |
| Jul 01 | Hakim Ziyech | Morocco |
| Jul 02 | Achraf Hakimi | Morocco |
| Jul 03 | Riyad Mahrez | Algeria |
| Jul 04 | Hugo Lloris | France |
| Jul 05 | Andres Iniesta | Spain |
| Jul 06 | Marcus Rashford | England |
| Jul 07 | Ederson | Brazil |
| Jul 08 | Kasper Schmeichel | Denmark |
| Jul 09 | Vinicius Jr. | Brazil |
| Jul 10 | Thomas Müller | Germany |
| Jul 11 | Youssouf Fofana | France |

---

## Project Structure

```
fifa-player-inspirational/
├── main.py                  # Entry point — system tray app
├── requirements.txt         # Python dependencies
├── fifa_mac.spec            # PyInstaller spec for macOS
├── fifa_windows.spec        # PyInstaller spec for Windows
├── build_mac.sh             # One-command Mac build
├── build_windows.bat        # One-command Windows build
├── stories/
│   └── players.json         # All 26 player stories
└── src/
    ├── config.py            # Settings persistence (~/.fifa_inspirational/)
    ├── story_manager.py     # Story loading and date-matching logic
    ├── generator.py         # Word (.docx) and PowerPoint (.pptx) generation
    ├── popup.py             # CustomTkinter popup and settings windows
    └── autostart.py         # Launch-at-login (LaunchAgent / Registry)
```

---

## Ideas for future versions

- **Email digest** — auto-email the daily story to a team distribution list
- **Slack / Teams integration** — post to a #inspiration channel automatically
- **Admin dashboard** — web page where a manager can see who opened each story
- **Custom stories** — allow your team to submit their own inspiring stories
- **Screensaver mode** — display the story as a full-screen screensaver
- **Story reactions** — let coworkers leave a one-click emoji reaction
# fifa-player-inspirational
