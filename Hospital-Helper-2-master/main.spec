# -*- mode: python -*-

import os
import importlib
import inspect

block_cipher = None

ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
STATIC = os.path.join(ROOT, 'app', 'gui', 'static')

DATAS = [
    (os.path.join(STATIC, 'icons', '*.png'), os.path.join('app', 'gui', 'static', 'icons')),
    (os.path.join(STATIC, 'style', '*.qss'), os.path.join('app', 'gui', 'static', 'style')),
    (os.path.join(STATIC, '*.png'), os.path.join('app', 'gui', 'static')),
    (os.path.join(STATIC, '*.ico'), os.path.join('app', 'gui', 'static')),
    (os.path.join(ROOT, 'app', 'data', '*.json'), os.path.join('app', 'data')),
]

def get_module_imports(*modules_names):
    # I'm not sure if it is a good decision
    # but it works with my modules
    files = []
    for module_name in modules_names:
        module_dir = os.path.dirname(importlib.import_module(module_name).__file__)
        for each in os.listdir(module_dir):
            if each.endswith('.py'):
                # f = os.path.join(module_dir, each)
                # files.append(os.path.join(module_dir, each))
                files.append('%s.%s' % (module_name, each.replace('.py', '')))
    return files


a = Analysis([os.path.join(ROOT, 'app', 'main.py')],
             pathex=[ROOT],
             binaries=None,
             datas=DATAS,
             hiddenimports=get_module_imports('unidecode'),
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Hospital Helper 2',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon=os.path.join(STATIC, 'icon.ico'))
