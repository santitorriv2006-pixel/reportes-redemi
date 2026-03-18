# -*- mode: python ; coding: utf-8 -*-
"""
Configuración de PyInstaller para Sistema de Reportes
"""

import os

block_cipher = None

a = Analysis(
    ['run_portable.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app/templates', 'app/templates'),
        ('app/static', 'app/static'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_login',
        'flask_sqlalchemy',
        'flask_mail',
        'flask_wtf',
        'pandas',
        'openpyxl',
        'sqlalchemy',
        'apscheduler',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SistemaReportes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app/static/img/icon.ico' if os.path.exists('app/static/img/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SistemaReportes',
)
