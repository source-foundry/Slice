# <img height="36" src="https://raw.githubusercontent.com/source-foundry/Slice/main/src/resources/img/slice-icon.svg"/>  Slice

### An open-source application to create custom static fonts from variable fonts

## About

Slice is a GUI application that takes a variable font and compiles a new custom "slice" of the variable design space with user-defined design axis values.  This output file is commonly known as a "static instance" font in type software developer parlance.  The application supports custom font family naming so that you can view output files as different families in application menus.

Slice is built with PyQt5 and supports cross-platform use on macOS, Windows, and Linux. Static instance fonts are generated with the [fonttools Python library](https://github.com/fonttools/fonttools).  The application is free software. Please see the Licenses section below for additional details.

If you are a licensed user of the font that you intend to edit, please understand your font license before you use this application!

## Use case examples

- You want to use a font, file size optimization is important, and you only need a small subset of a variable font design space
- You want to use a font in an application that lacks support for, or only partially supports, the variable font format
- You want to use fonts that cover different areas of the design space and have different family names for A/B testing
- You develop type software and want to easily generate multiple static instances of your variable design space to support the client or reviewer review process

## Installation

Install the application on your platform with the following instructions.

### [macOS]()

Download the [latest macOS dmg installer](https://github.com/source-foundry/Slice/releases/latest) in our Releases.

Launch the installer and acknowledge the license during the install process. Drag and drop the Slice.app bundle into your Applications directory when the installer prompts you to do so.  Open Launchpad and launch Slice by clicking the icon.

A Homebrew installation approach is in development.  See [#6](https://github.com/source-foundry/Slice/issues/6).

### [Linux]()

Linux packages are in development.  For now, please use the following instructions.

Clone the repository with:

```
$ git clone https://github.com/source-foundry/Slice.git
```

Create a Python 3.6+ virtual environment with:

```
$ cd Slice
$ python3 -m venv .venv
```

Install the required build dependencies with:

```
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Run the application with:

```
$ make run
```

### [Windows]()

Download the [latest Windows .exe installer](https://github.com/source-foundry/Slice/releases/latest) in our Releases.

Launch the installer, acknowledge the license, and follow the instructions.  When the install process completes, type "Slice" in the Win 10 Search bar and launch the application (or click the desktop icon if you chose to install it during the installation process).

## Usage

1. Drag and drop a variable font file onto the Font Path free text entry area.  Your variable font axis names with associated min, max, and default axis values display in the Axis Definitions editor table.
2. Click the Instance Value fields of the Axis Definitions editor table and set the desired values.  Default axis tag values are used when you leave a field blank.
3. Edit the Name Table Definitions fields to define the menu names for your instance slice.  Refer to the [OpenType specification name table documentation](https://docs.microsoft.com/en-us/typography/opentype/spec/name) for additional details about how to set these values.
4. Use the checkboxes at the bottom of the application window to set the appropriate bits.  Checkboxes that are not clicked indicate that you want the bit cleared. Refer to the OpenType specification [head](https://docs.microsoft.com/en-us/typography/opentype/spec/head) and [OS/2](https://docs.microsoft.com/en-us/typography/opentype/spec/os2) table documentation for additional details.
5. Click the Slice button and enter a save path in the dialog window.  The status bar in the bottom left corner of the main application window will indicate when your new slice is ready.

## Contributing

Please file issues on the [project tracker](https://github.com/source-foundry/Slice/issues).  

Source contributions are welcome.  Please see the [DEVELOPER.md](DEVELOPER.md) documentation for instructions on how to set up a development environment and test source changes.  Submit a pull request with any changes that you would like to share upstream.

## Licenses

The Slice project is licensed under the GNU General Public License version 3. Please see the [LICENSE](LICENSE) document for details.

Please see the [thirdparty directory](https://github.com/source-foundry/Slice/tree/main/thirdparty) for additional details about third-party licenses.
