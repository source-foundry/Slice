# Changelog

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
