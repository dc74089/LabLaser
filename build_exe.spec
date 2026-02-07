# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for GKTW Laser Tool
Usage: pyinstaller build_exe.spec
"""

import os
from pathlib import Path

# Get the project directory
project_dir = Path(SPECPATH)

# Collect all Django template files
template_files = []
for root, dirs, files in os.walk(project_dir / 'app' / 'templates'):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, project_dir)
            dest_dir = os.path.dirname(rel_path)
            template_files.append((file_path, dest_dir))

# Collect all static files
static_files = []
for root, dirs, files in os.walk(project_dir / 'app' / 'static'):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, project_dir)
        dest_dir = os.path.dirname(rel_path)
        static_files.append((file_path, dest_dir))

# Collect settings and other config files
config_files = [
    (str(project_dir / 'LabLaser' / 'settings.py'), 'LabLaser'),
    (str(project_dir / 'LabLaser' / 'urls.py'), 'LabLaser'),
    (str(project_dir / 'LabLaser' / 'wsgi.py'), 'LabLaser'),
    (str(project_dir / 'app' / 'urls.py'), 'app'),
    (str(project_dir / 'app' / 'views.py'), 'app'),
    (str(project_dir / 'app' / 'models.py'), 'app'),
]

# Combine all data files
all_data_files = template_files + static_files + config_files

a = Analysis(
    ['run_server.py'],
    pathex=[str(project_dir)],
    binaries=[],
    datas=all_data_files,
    hiddenimports=[
        'django',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'app',
        'app.models',
        'app.views',
        'app.urls',
        'LabLaser.settings',
        'LabLaser.urls',
        'LabLaser.wsgi',
        'requests',
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
