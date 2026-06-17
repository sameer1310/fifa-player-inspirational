# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec – macOS (.app bundle)
# Build:  pyinstaller fifa_mac.spec

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('stories/players.json', 'stories'),
    ],
    hiddenimports=[
        'customtkinter',
        'pystray',
        'pystray._darwin',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'docx',
        'pptx',
        'pptx.util',
        'pptx.dml.color',
        'pptx.enum.text',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name='FIFAInspirational',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas,
    strip=False, upx=True, upx_exclude=[],
    name='FIFAInspirational',
)

app = BUNDLE(
    coll,
    name='FIFAInspirational.app',
    icon=None,
    bundle_identifier='com.fifainspirational.app',
    info_plist={
        'CFBundleName':              'FIFA Inspirational Stories',
        'CFBundleDisplayName':       'FIFA Inspirational Stories',
        'CFBundleShortVersionString':'1.0.0',
        'NSHighResolutionCapable':   True,
        'LSUIElement':               True,   # Hide from Dock (tray-only)
        'NSRequiresAquaSystemAppearance': False,
    },
)
