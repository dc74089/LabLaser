# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for GKTW Laser Tool
Usage: pyinstaller build_exe.spec
"""

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Get the project directory
project_dir = Path(SPECPATH)

# Collect EVERYTHING from the app directory and svgs directory
all_data_files = []
for item in ['app', 'LabLaser', 'svgs']:
    item_path = project_dir / item
    if item_path.exists():
        for root, dirs, files in os.walk(item_path):
            # Skip __pycache__ and .pyc files
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for file in files:
                if not file.endswith('.pyc'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, project_dir)
                    dest_dir = os.path.dirname(rel_path)
                    all_data_files.append((file_path, dest_dir))

# Also collect all of Django
datas_django, binaries_django, hiddenimports_django = collect_all('django')
all_data_files.extend(datas_django)

a = Analysis(
    ['run_server.py'],
    pathex=[str(project_dir)],
    binaries=binaries_django,
    datas=all_data_files,
    hiddenimports=hiddenimports_django + collect_submodules('app') + collect_submodules('LabLaser') + [
        'requests',
        'requests.adapters',
        'requests.auth',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GKTW_Laser_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one: icon='icon.ico'
)
