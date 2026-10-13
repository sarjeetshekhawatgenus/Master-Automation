# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, copy_metadata, collect_submodules

block_cipher = None

# Collect all Streamlit metadata, data files (static assets, fonts), and submodules
streamlit_datas = collect_data_files('streamlit')
streamlit_metadata = copy_metadata('streamlit')
streamlit_submodules = collect_submodules('streamlit')

# Collect pandas data and application modules
pandas_datas = collect_data_files('pandas')
app_submodules = collect_submodules('master_update_automation')

datas = [
    ('app.py', '.'),
    ('.streamlit', '.streamlit'),
    ('master_update_automation', 'master_update_automation'),
] + streamlit_datas + streamlit_metadata + pandas_datas

hiddenimports = [
    'streamlit',
    'streamlit.web.bootstrap',
    'streamlit.web.cli',
    'streamlit.runtime',
    'streamlit.runtime.scriptrunner.magic_expressions',
    'openpyxl',
    'openpyxl.cell._writer',
    'pandas',
    'starlette',
    'uvicorn',
    'tornado',
] + streamlit_submodules + app_submodules

a = Analysis(
    ['launcher.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy', 'IPython', 'pytest', 'unittest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MasterAutomation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MasterAutomation',
)
