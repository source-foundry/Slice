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



# --------------------
# Resource file builds
# --------------------

build-image-resource:
	cd src/resources/img && pyrcc5 -o ../../slice/imageresources.py image-resources.qrc

build-font-resource:
	cd src/resources/fonts && pyrcc5 -o ../../slice/fontresources.py font-resources.qrc

# ---------------------
# macOS platform builds
# ---------------------

# Updates the Icon.icns file from the icon images in icons/Icon.iconset 
macos-iconset:
	cd icons && iconutil -c icns Icon.iconset

build-macos: macos-iconset build-image-resource build-font-resource
	pyinstaller --noconfirm "target/PyInstaller-macOS/Slice-macOS.spec"
	cp LICENSE dist/license.txt

codesign-macos:
	codesign --deep -s "Christopher Simpkins" dist/Slice.app

build-macos-installer:
	# https://github.com/sindresorhus/create-dmg
	cd dist && create-dmg --overwrite Slice.app


# -----------------------
# Windows platform builds
# -----------------------

win-ico:
	magick convert icons/1024.png -alpha off -resize 256x256 \
          -define icon:auto-resize="256,128,96,64,48,32,16" \
          icons/Icon.ico

# ---------------------
# Testing/debugging
# ---------------------

# directly execute the application without a PyInstaller build
run:
	python src/run.py


# ---------------------
# Source formatting
# ---------------------
format:
	isort src && black src


.PHONY: build-image-resource build-font-resource\
build-macos macos-iconset codesign-macos build-macos-installer\
run