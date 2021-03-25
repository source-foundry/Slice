# <img height="36" src="https://raw.githubusercontent.com/source-foundry/Slice/main/src/resources/img/slice-icon.svg"/>  Slice

## About

Slice is a GUI application that takes a variable font and compiles a new instance "slice" of the variable design space with user-defined axis values.  It provides an OpenType name table editor to support unique slice names so that artifacts show up in application menus as different families according to the area of the design space that you build.  These builds are called "static instances" in fancy font parlance.

Slice is built with PyQt5 and supports cross-platform use on macOS, Windows, and Linux. Design space slices are generated with the [fonttools Python library](https://github.com/fonttools/fonttools).  The application is free software. Please see the Licenses section below for additional details.

## Installation

Install the application on your platform with the following instructions.

### [macOS]()

Download the [latest macOS dmg installer](https://github.com/source-foundry/Slice/releases/latest) in our Releases.

Launch the installer and acknowledge the license during the install process. Drag and drop the Slice.app bundle into your Applications directory when the installer prompts you to do so.  Open Launchpad and launch Slice by clicking the icon.


### [Linux]()

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

Please file issue reports on the [project tracker](https://github.com/source-foundry/Slice/issues).  

Source contributions are welcome.  Fork the repository and submit a pull request with your changes.

## Licenses

The Slice project is licensed under the GNU General Public License version 3. Please see [LICENSE](LICENSE) for details.

Please see the [thirdparty directory](https://github.com/source-foundry/Slice/tree/main/thirdparty) for additional details about third-party licenses.
