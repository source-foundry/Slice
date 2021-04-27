# Changelog

## v0.5.1

- Fix: Application crash when a user attempts to enter invalid axis value data
- Updated: bump fonttools dependency to v4.22.1 from v4.22.0

## v0.5.0

- New: add support for slicing to files that have a subset of variable axes (commonly known as partial instantiation or sub-spacing)
- New: add new validation that at least one axis value is defined (else user is requesting the input font design space with the new definition approach)
- New: add indefinite progress indicator during slicing operation
- New: add axis editor tag tooltips with full axis names that are derived from (1) OpenType registered axes; (2) Google Fonts axis registry; (3) font's fvar table definitions
- New: add embedded Recursive typeface instance subset for formatting of the in-app view of application name (SIL OFL)
- New: add embedded IBM Plex typeface for formatting of the axis and name table editor text (SIL OFL)
- New: add Code of Conduct
- Fixed: address (some) of the VirusTotal false positive flags for the Win executable build (required PyInstaller update)
- Fixed: axis editor table view max height
- Updated: Changed "Axis Definitions" view title to "Axis Editor"
- Updated: Changed "Name Table Definitions" view title to "Name Editor"
- Updated: Changed "Bit Flag Settings" view title to "Bit Flag Editor"
- Updated: improve application launch center position
- Updated: About dialog window width increased
- Updated: About dialog dependencies list text size increased
- Updated: change axis and name table editor field header strings to "Edit Values" from "Instance Values"
- Updated: change Makefile `run` target with build of automated fontresources and imageresources on each execution
- Updated: pin the PyInstaller build dependency at production release v4.3
- Updated: bump fonttools dependency to v4.22.0 from v4.21.1
- Removed: embedded Monoton typeface

## v0.4.0

- add macOS code signed / installer notarization support
- add new macOS code signing, notarization, and code signing/notary validation make targets
- add Arch Linux AUR package support and documentation (thanks Caleb!)
- add Homebrew cask tap install/uninstall/upgrade support and documentation
- add maintainer docs on path `docs/MAINTAINER.md`

## v0.3.1

- minor patch for Homebrew distribution testing
- minor patch for macOS code sign testing

## v0.3.0

- add Windows installer support to releases
- add Inno Setup Windows installer configuration
- fix: axis value editor table vertical header spacing for all caps axis tags, the axis tag column should now automatically resize to the max width axis tag in the list
- fix: set the window icon to the Slice icon on Windows views
- fix: set the About dialog title and icon on Windows views
- fix: update image conversion approach to maintain alpha transparency in Windows application icon

## v0.2.1

- update FontNameModel model flags definitions based on qabstractitemmodel.cpp fails

## v0.2.0

- update macOS app bundle embedded cPython interpreter to v3.9.2 from v3.8.2
- update SliceBaseTableModel model row and column count approaches based on qabstractitemmodel.cpp fails
- update DesignAxisModel model flags definitions based on qabstractitemmodel.cpp fails

## v0.1.3

- Add fonttools version number in the About dialog
- Add Windows .ico icon generator Makefile target
- Add Python packaging configuration/support
- Add PyPI distribution packaging and release support
- Add GitHub Actions based GitHub release automation
- Add GitHub Actions based PyPI release automation
- Add CodeQL testing

## v0.1.2

- Push the PyInstaller spec file to support PyInstaller Makefile target compiles (sorry GitHub snuck it into the default Python .gitignore file)
- Update .gitignore to remove `target` dir and `.spec` files

## v0.1.1

- Fix: drag and drop support on the Windows platform (#1)
- Add new format Makefile target with isort and black executables

## v0.1.0

- initial release
