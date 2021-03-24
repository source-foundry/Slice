# -*- mode: python ; coding: utf-8 -*-

# This file is part of Slice.
#
#    Slice is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Slice is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Slice.  If not, see <https://www.gnu.org/licenses/>.

import json
from pathlib import Path


with open(Path("src/build/settings/base.json")) as f:
    base_json = json.load(f)
    VERSION = base_json["version"]
    APP_NAME = base_json["app_name"]
    MAIN_MODULE_PATH = base_json["main_module"]

ICON_PATH = Path("icons/Icon.ico").resolve()

block_cipher = None


a = Analysis([Path(MAIN_MODULE_PATH).resolve()],
             pathex=[Path('target/PyInstaller-Windows').resolve()],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=APP_NAME,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False ,
          runtime_tmpdir=None,
          icon=[str(ICON_PATH)], )
