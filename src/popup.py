"""
popup.py  –  All webview window HTML + JS↔Python API classes.
Each function creates exactly one window and blocks until it closes.
"""
import json as _json
import subprocess
import sys
import os
from pathlib import Path

import webview

from .story_manager import get_today_story, get_all_stories, get_story_by_index
from .generator import generate_documents
from .config import ConfigManager

PYTHON = sys.executable
VIEWER = str(Path(__file__).resolve().parent.parent / "viewer.py")


def _open_story_subprocess(index: int):
    """Open a story in a fresh subprocess (used from browse window)."""
    subprocess.Popen(
        [PYTHON, VIEWER, "story", str(index)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ── Shared CSS ────────────────────────────────────────────────────────────────
BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --fs: 13px; }
body {
  font-family: -apple-system, 'Segoe UI', Arial, sans-serif;
  background: #1A1A1A; color: #F5F5F5;
  font-size: var(--fs); height: 100vh; overflow-y: auto;
}
.header {
  background: #006B3C; padding: 12px 20px;
  text-align: center; color: #D4AF37;
  font-size: 1.1em; font-weight: bold; letter-spacing: 1px;
}
.gold-bar { height: 3px; background: #D4AF37; }
.content { padding: 16px 28px 24px; }
h1 { color: #D4AF37; font-size: 2em; text-align: center;
     letter-spacing: 2px; margin: 14px 0 3px; }
.meta { text-align: center; font-size: 0.88em; color: #aaa; margin-bottom: 8px; }
.headline { text-align: center; font-style: italic; font-size: 1.1em;
            color: #D4AF37; margin-bottom: 12px; }
.divider { height: 2px; background: #006B3C; margin: 10px 0; }
.story { font-size: 1em; line-height: 1.8; text-align: justify; }
.story p { margin-bottom: 0.9em; }
.quote {
  text-align: center; font-style: italic; font-weight: bold;
  color: #D4AF37; font-size: 1.05em; margin: 14px 0;
  padding: 10px 18px;
  border-left: 4px solid #D4AF37; border-right: 4px solid #D4AF37;
}
.lesson-row { display: flex; gap: 10px; align-items: flex-start;
              margin-top: 10px; font-size: 0.95em; }
.lesson-label { color: #006B3C; font-weight: bold; white-space: nowrap;
                font-size: 0.85em; padding-top: 2px; }
.lesson-text { font-style: italic; color: #ddd; line-height: 1.6; }
.font-bar {
  display: flex; align-items: center; justify-content: flex-end;
  gap: 6px; padding: 6px 28px 0; background: #1A1A1A;
}
.font-bar span { font-size: 0.8em; color: #888; }
.font-bar button {
  padding: 3px 10px; border-radius: 4px; cursor: pointer;
  background: #2a2a2a; border: 1px solid #006B3C; color: #D4AF37;
  font-size: 0.85em; font-weight: bold;
}
.font-bar button:hover { background: #006B3C; color: #fff; }
.buttons {
  display: flex; flex-wrap: wrap; gap: 8px;
  margin-top: 18px; justify-content: center;
}
button.action {
  padding: 9px 16px; border: none; border-radius: 6px;
  cursor: pointer; font-size: 0.95em; font-weight: bold;
}
.btn-green  { background: #006B3C; color: #fff; }
.btn-gold   { background: #D4AF37; color: #1A1A1A; }
.btn-dark   { background: #2a2a2a; color: #fff; border: 1px solid #006B3C !important; }
.btn-close  { background: #444; color: #fff; }
button.action:hover { opacity: 0.85; }
.footer {
  text-align: center; font-size: 0.75em; color: #444;
  padding: 10px 0 4px; margin-top: 8px;
}
"""

FONT_CONTROLS = """
<div class="font-bar">
  <span>Text size:</span>
  <button onclick="changeFont(-1)">A−</button>
  <button onclick="changeFont(0)">A</button>
  <button onclick="changeFont(1)">A+</button>
  <button onclick="changeFont(2)">A++</button>
</div>
<script>
var sizes = [11, 13, 15, 18];
var si = 1;
function changeFont(idx) {
  if (idx === -1) { si = Math.max(0, si - 1); }
  else if (idx >= 0 && idx <= 3) { si = idx; }
  document.documentElement.style.setProperty('--fs', sizes[si] + 'px');
}
</script>
"""


# ── Story popup HTML ──────────────────────────────────────────────────────────
def _story_html(story: dict, save_dir: str) -> str:
    paragraphs = "".join(
        f"<p>{p.strip()}</p>"
        for p in story["story"].split("\n\n") if p.strip()
    )
    safe_dir = save_dir.replace("\\", "/")
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
{BASE_CSS}
.save-bar {{
  background: #0d2a4a; border-bottom: 3px solid #FF6B00;
  padding: 10px 20px; display: flex; align-items: center;
  flex-wrap: wrap; gap: 10px;
}}
.save-bar label {{
  font-size: 1em; font-weight: bold; color: #FF6B00;
  white-space: nowrap; letter-spacing: 0.5px;
}}
.save-bar input[type=text] {{
  flex: 1; min-width: 200px; padding: 7px 10px;
  background: #0a1f36; border: 2px solid #FF6B00;
  color: #fff; border-radius: 5px; font-size: 0.95em;
}}
.save-bar button {{
  padding: 7px 14px; border-radius: 5px; cursor: pointer;
  background: #FF6B00; border: none; color: #fff;
  font-size: 0.95em; font-weight: bold; letter-spacing: 0.5px;
}}
.save-bar button:hover {{ background: #cc5500; }}
.mode-bar {{
  background: #0d2a4a; border-bottom: 3px solid #1E90FF;
  padding: 9px 20px; display: flex; align-items: center; gap: 22px;
  flex-wrap: wrap;
}}
.mode-bar span {{
  font-size: 1em; font-weight: bold; color: #1E90FF;
  white-space: nowrap; letter-spacing: 0.5px;
}}
.mode-bar label {{
  font-size: 1em; color: #fff; cursor: pointer;
  display: flex; align-items: center; gap: 7px; font-weight: 500;
}}
.mode-bar input[type=radio] {{ accent-color: #1E90FF; width: 16px; height: 16px; }}
</style>
</head><body>
{FONT_CONTROLS}
<div class="header">⚽&nbsp; FIFA WORLD CUP 2026 &nbsp;|&nbsp; Daily Inspiration &nbsp;⚽</div>
<div class="gold-bar"></div>

<div class="save-bar">
  <label>Save to:</label>
  <input type="text" id="save_dir" value="{safe_dir}">
  <button onclick="pywebview.api.pick_folder()">Browse…</button>
</div>

<div class="mode-bar">
  <span>Save mode:</span>
  <label><input type="radio" name="mode" value="append" checked> Append to shared FIFA document</label>
  <label><input type="radio" name="mode" value="individual"> Save as individual file for this player</label>
</div>

<div class="content">
  <h1>{story['name'].upper()}</h1>
  <div class="meta">{story['country']} &nbsp;·&nbsp; {story['position']} &nbsp;·&nbsp; {story['date']}</div>
  <div class="headline">"{story['headline']}"</div>
  <div class="divider"></div>
  <div class="story">{paragraphs}</div>
  <div class="quote">❝ &nbsp;{story['quote']}&nbsp; ❞</div>
  <div class="divider"></div>
  <div class="lesson-row">
    <span class="lesson-label">TODAY'S LESSON</span>
    <span class="lesson-text">{story['lesson']}</span>
  </div>
  <div class="buttons">
    <button class="action btn-green" onclick="doSave('docx')">Save as Word (.docx)</button>
    <button class="action btn-green" onclick="doSave('pptx')">Save as Slide (.pptx)</button>
    <button class="action btn-gold"  onclick="doSave('both')">Save Both</button>
    <button class="action btn-dark"  onclick="pywebview.api.open_folder(getSaveDir())">Open Save Folder</button>
    <button class="action btn-close" onclick="pywebview.api.close_window()">Close</button>
  </div>
  <div class="footer">FIFA 2026 Inspirational Stories &nbsp;·&nbsp; One Player. One Story. Every Day.</div>
</div>
<script>
function getSaveDir() {{
  return document.getElementById('save_dir').value;
}}
function getMode() {{
  return document.querySelector('input[name=mode]:checked').value;
}}
function doSave(fmt) {{
  pywebview.api.save(fmt, getSaveDir(), getMode()).then(function(msg) {{
    alert(msg);
  }});
}}
function set_save_dir(path) {{
  document.getElementById('save_dir').value = path;
}}
</script>
</body></html>"""


# ── Browse gallery HTML ───────────────────────────────────────────────────────
def _browse_html(stories: list) -> str:
    cards = ""
    for i, s in enumerate(stories):
        cards += f"""
        <div class="card" onclick="pywebview.api.open_story({i})">
          <div class="card-date">{s['date']}</div>
          <div class="card-name">{s['name']}</div>
          <div class="card-meta">{s['country']} · {s['position']}</div>
          <div class="card-hl">"{s['headline']}"</div>
        </div>"""
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
{BASE_CSS}
.page-title {{ color: #D4AF37; text-align: center;
               font-size: 1.4em; font-weight: bold; padding: 14px 0 4px; }}
.subtitle   {{ text-align: center; color: #aaa; font-size: 0.85em; margin-bottom: 16px; }}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px; padding: 0 20px 24px;
}}
.card {{
  background: #242424; border: 1px solid #006B3C; border-radius: 8px;
  padding: 14px; cursor: pointer; transition: background 0.15s;
}}
.card:hover {{ background: #006B3C; }}
.card-date {{ font-size: 0.78em; color: #888; margin-bottom: 4px; }}
.card-name {{ font-size: 1.05em; font-weight: bold; color: #D4AF37;
               margin-bottom: 3px; }}
.card-meta {{ font-size: 0.8em; color: #aaa; margin-bottom: 6px; }}
.card-hl   {{ font-size: 0.82em; font-style: italic; color: #ccc; }}
</style></head><body>
<div class="header">⚽&nbsp; FIFA WORLD CUP 2026 &nbsp;|&nbsp; All Inspirational Stories</div>
<div class="gold-bar"></div>
<div class="page-title">Browse All Players</div>
<div class="subtitle">Click any card to read the full story</div>
<div class="grid">{cards}</div>
</body></html>"""


# ── Settings HTML ─────────────────────────────────────────────────────────────
def _settings_html(settings) -> str:
    fmt_opts = {"both": "Both (.docx + .pptx)", "docx": "Word only (.docx)", "pptx": "Slide only (.pptx)"}
    fmt_radios = "\n".join(
        f'<label><input type="radio" name="fmt" value="{v}" {"checked" if settings.output_format == v else ""}> {l}</label>'
        for v, l in fmt_opts.items()
    )
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
{BASE_CSS}
body {{ padding: 24px 28px; overflow-y: auto; height: auto; min-height: 100vh; }}
h2 {{ color: #D4AF37; margin-bottom: 20px; font-size: 1.4em; }}
.section {{ color: #D4AF37; font-weight: bold; font-size: 0.9em;
            margin: 16px 0 6px; text-transform: uppercase; letter-spacing: 1px; }}
input[type=text] {{
  width: 100%; padding: 8px 10px; background: #2a2a2a;
  border: 1px solid #006B3C; color: #fff; border-radius: 5px;
  font-size: 0.95em; margin-bottom: 4px;
}}
.row {{ display: flex; gap: 8px; align-items: center; margin-bottom: 14px; }}
.row input[type=text] {{ margin-bottom: 0; flex: 1; }}
.radio-group {{ display: flex; gap: 16px; margin-bottom: 14px; flex-wrap: wrap; }}
.radio-group label {{ font-size: 0.9em; }}
.check-group label {{
  font-size: 0.9em; margin-bottom: 8px;
  display: flex; align-items: center; gap: 8px; cursor: pointer;
}}
.btn-row {{ display: flex; gap: 10px; margin-top: 20px; }}
.btn-row button {{
  padding: 9px 22px; border: none; border-radius: 6px;
  cursor: pointer; font-size: 0.95em; font-weight: bold;
}}
.btn-save  {{ background: #D4AF37; color: #1A1A1A; }}
.btn-close {{ background: #444; color: #fff; }}
button:hover {{ opacity: 0.85; }}
#status {{ color: #D4AF37; font-size: 0.85em; margin-top: 10px; min-height: 18px; }}
</style></head><body>
<h2>⚙ Settings</h2>

<div class="section">Save Directory</div>
<div class="row">
  <input type="text" id="save_dir" value="{settings.save_directory}">
  <button class="btn-save" onclick="pywebview.api.browse_folder()">Browse…</button>
</div>

<div class="section">Output Format</div>
<div class="radio-group">{fmt_radios}</div>

<div class="section">Startup Behavior</div>
<div class="check-group">
  <label><input type="checkbox" id="autostart" {"checked" if settings.auto_start else ""}> Launch app at login (menu bar)</label>
  <label><input type="checkbox" id="show_popup" {"checked" if settings.show_on_startup else ""}> Show today's story popup at startup</label>
</div>

<div class="btn-row">
  <button class="btn-save"  onclick="save_settings()">Save Settings</button>
  <button class="btn-close" onclick="pywebview.api.close_window()">Close</button>
</div>
<div id="status"></div>

<script>
function save_settings() {{
  var data = {{
    save_directory: document.getElementById('save_dir').value,
    output_format:  document.querySelector('input[name=fmt]:checked').value,
    auto_start:     document.getElementById('autostart').checked,
    show_on_startup: document.getElementById('show_popup').checked,
  }};
  pywebview.api.save_settings(data).then(function(msg) {{
    document.getElementById('status').textContent = msg;
  }});
}}
function set_directory(path) {{
  document.getElementById('save_dir').value = path;
}}
</script>
</body></html>"""


# ── JS↔Python API: Story popup ────────────────────────────────────────────────
class StoryAPI:
    def __init__(self, story, config, win_ref):
        self.story  = story
        self.config = config
        self._win   = win_ref

    def save(self, fmt, directory, mode):
        try:
            individual = (mode == "individual")
            paths = generate_documents(self.story, directory, fmt, individual=individual)
            names = "\n".join(Path(p).name for p in paths)
            return f"Saved to:\n{directory}\n\n{names}"
        except Exception as e:
            return f"Error: {e}"

    def pick_folder(self):
        win = self._win[0]
        if not win:
            return
        result = win.create_file_dialog(webview.FOLDER_DIALOG)
        if result:
            folder = result[0].replace("\\", "/")
            win.evaluate_js(f'set_save_dir({_json.dumps(folder)})')

    def open_folder(self, directory):
        Path(directory).mkdir(parents=True, exist_ok=True)
        if sys.platform == "darwin":
            subprocess.run(["open", directory])
        elif sys.platform == "win32":
            subprocess.run(["explorer", directory])

    def close_window(self):
        if self._win[0]:
            self._win[0].destroy()


# ── JS↔Python API: Browse gallery ────────────────────────────────────────────
class BrowseAPI:
    def open_story(self, index: int):
        _open_story_subprocess(index)


# ── JS↔Python API: Settings ──────────────────────────────────────────────────
class SettingsAPI:
    def __init__(self, config, autostart_helper, win_ref):
        self.config    = config
        self.autostart = autostart_helper
        self._win      = win_ref

    def browse_folder(self):
        win = self._win[0]
        if not win:
            return
        result = win.create_file_dialog(webview.FOLDER_DIALOG)
        if result:
            folder = result[0].replace("\\", "/")
            win.evaluate_js(f'set_directory({_json.dumps(folder)})')

    def save_settings(self, data):
        self.config.update(
            save_directory  = data["save_directory"],
            output_format   = data["output_format"],
            auto_start      = data["auto_start"],
            show_on_startup = data["show_on_startup"],
        )
        if data["auto_start"]:
            self.autostart.enable()
        else:
            self.autostart.disable()
        return "Settings saved successfully."

    def close_window(self):
        if self._win[0]:
            self._win[0].destroy()


def _start(win):
    """Start webview and hard-exit when the window closes."""
    win.events.closed += lambda: os._exit(0)
    webview.start(debug=False)


# ── Public window launchers ───────────────────────────────────────────────────
def show_story_popup(story: dict, config: ConfigManager):
    win_ref = [None]
    api = StoryAPI(story, config, win_ref)
    win = webview.create_window(
        title     = f"⚽  {story['name']} – FIFA Daily Inspiration",
        html      = _story_html(story, config.settings.save_directory),
        js_api    = api,
        width     = 820,
        height    = 740,
        resizable = True,
        min_size  = (620, 520),
    )
    win_ref[0] = win
    _start(win)


def show_browse_window(config: ConfigManager):
    stories = get_all_stories()
    api = BrowseAPI()
    win = webview.create_window(
        title     = "⚽  FIFA 2026 – Browse All Stories",
        html      = _browse_html(stories),
        js_api    = api,
        width     = 900,
        height    = 650,
        resizable = True,
    )
    _start(win)


def show_settings_window(config: ConfigManager, autostart_helper):
    win_ref = [None]
    api = SettingsAPI(config, autostart_helper, win_ref)
    win = webview.create_window(
        title     = "FIFA Inspirational – Settings",
        html      = _settings_html(config.settings),
        js_api    = api,
        width     = 520,
        height    = 480,
        resizable = False,
    )
    win_ref[0] = win
    _start(win)


def show_today_story(config: ConfigManager):
    show_story_popup(get_today_story(), config)
