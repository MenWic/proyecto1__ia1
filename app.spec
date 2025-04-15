# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['interface/app.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('interface', 'interface'), ('modelos', 'modelos'), ('utils', 'utils'), ('individuo.py', '.'), ('poblacion.py', '.'), ('algoritmo_genetico.py', '.'), ('main.py', '.')],
    hiddenimports=[
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.platypus',
        'reportlab.platypus.doctemplate',
        'reportlab.platypus.paragraph',
        'reportlab.platypus.tableofcontents',
        'reportlab.lib.styles',
        'reportlab.lib.enums',
        'reportlab.lib.pagesizes',
        'reportlab.lib.units',
        'reportlab.lib.colors',
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

pyz = PYZ(a.pure, a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app'
)
