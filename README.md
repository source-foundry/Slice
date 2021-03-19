# Slice

## About

Slice is a GUI application that takes a variable font and compiles a new "slice" instance of the variable design space with user-defined axis values.  It provides an OpenType name table editor to support unique slice names so that artifacts show up in application menus as different families according to the area of the design space that you use.

Slice is built with PyQt5 and supports cross-platform use on macOS, Windows, and Linux. Design space slices are generated with the [fonttools Python library](https://github.com/fonttools/fonttools).  The application is free software. Please see the Licenses section below for additional details.

## Installation

Slice is alpha stage software. Install the application for testing with the following instructions.

### macOS and Linux

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


### Windows

The following instructions work in Powershell 7 on Windows 10.

Clone the repository with:

```
$ git clone https://github.com/source-foundry/Slice.git
```

Create a Python 3.6+ virtual environment with:

```
$ cd Slice
$ python3 -m venv venv
```

Install the required build dependencies with:

```
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
```

Run the application with:

```
$ python src\run.py
```



## Usage

1. Drag and drop a variable font file onto the Font Path free text entry area.  Your variable font axis values with min, max, and default settings display in the Axis Definitions editor table.
2. Click the Instance Value fields of the Axis Definitions editor table and set the desired values.  The value defaults to the default axis value if the field is blank.
3. Edit the Name Table Definitions fields to define the menu names for your slice
4. If you need to master the bit flags for the font, use the checkboxes to select the appropriate bits to set in the font
5. Click the Slice button and enter a save path in the dialog window that opens.  The status bar in the bottom left corner of the main application window will indicate when your font is ready.

## Contributing

Please file issue reports on the [project tracker](https://github.com/source-foundry/Slice/issues).  Source contributions are welcome.  Fork the repository and submit a pull request with your change proposal.

## Licenses

The Slice project is licensed under the GNU General Public License version 3. Please see [LICENSE](LICENSE) for details.

Please see the [thirdparty directory](https://github.com/source-foundry/Slice/tree/main/thirdparty) for additional details about third-party licenses.
