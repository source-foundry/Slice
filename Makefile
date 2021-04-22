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

build-macos-installer:
	# https://github.com/sindresorhus/create-dmg
	- rm dist/*.dmg
	cd dist && create-dmg --identity="BOGUS" Slice.app

# -------------------------------------------
# macOS platform distribution code signatures
# -------------------------------------------

# code sign the application distribution bundle
codesign-macos:
	codesign --deep --timestamp --force --options runtime -s "Developer ID Application: Christopher Simpkins" dist/Slice.app

# verify code signature on the distribution bundle
verify-codesign-macos:
	spctl -a -v dist/Slice.app

# code sign the macOS installer
codesign-macos-installer:
	codesign --timestamp --force --options runtime -s "Developer ID Application: Christopher Simpkins" dist/*.dmg

upload-macos-installer-for-notarize:
	# Requires Apple Developer account user name to be exported as the environment variable
	# APPLDEV_USERNAME before this target is executed
	# This will prompt for an app-specific password to be entered in stdin
	xcrun altool --notarize-app --type osx --primary-bundle-id "org.sourcefoundry.slice" --username @env:APPLEDEV_USERNAME --file dist/*.dmg

notarize-macos-installer:
	# Must export the notarization ID returned by upload-macos-installer-for-notarize
	# make target before this target is executed
	xcrun altool --notarization-info @env:SLICE_NOTARIZE_ID --username @env:APPLEDEV_USERNAME

staple-notary-macos:
	# requires successful notarize-macos-installer step completion
	xcrun stapler staple -v dist/*.dmg

# verify code signature on the macOS installer
verify-notarize-macos-installer:
	spctl -a -t open --context context:primary-signature -v dist/*.dmg


# -----------------------
# Windows platform builds
# -----------------------

win-ico:
	magick convert icons/1024.png -alpha on -resize 256x256 \
          -define icon:auto-resize="256,128,96,64,48,32,16" \
          icons/Icon.ico


# -------------------------------
# PyPI packaging and distribution
# -------------------------------

clean:
	- rm dist/*.whl dist/*.tar.gz dist/*.zip

dist-build: clean
	python3 setup.py sdist bdist_wheel

dist-push:
	twine upload dist/*.whl dist/*.tar.gz

# ---------------------
# Testing/debugging
# ---------------------

# directly execute the application without a PyInstaller build
run: build-image-resource build-font-resource
	python src/run.py


# ---------------------
# Source formatting
# ---------------------
format:
	isort src
	black --exclude=".*fontresources\.py|.*imageresources\.py" src


.PHONY: build-image-resource build-font-resource\
build-macos macos-iconset codesign-macos build-macos-installer\
run