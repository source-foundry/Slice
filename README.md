# Slice

## About

Slice is a GUI application that takes a variable font and compiles a new "slice" instance of the variable design space with user-defined axis values.  It provides an OpenType name table editor to support unique slice names so that artifacts show up in application menus as different families according to the area of the design space that you use.

Slice is built with PyQt5 and supports cross-platform use on macOS, Windows, and Linux. Design space slices are generated with the [fonttools Python library](https://github.com/fonttools/fonttools).  The application is free software that can be used at no cost. Please see the Licenses section below for additional details.

## Installation

This is alpha stage software. Install the application for testing with the following instructions.

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

The following instructions were confirmed in Powershell 7.

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

## Contributing

## Licenses

The Slice project is licensed under the GNU General Public License version 3. Please see [LICENSE](LICENSE) for details.

Please see the [thirdparty directory](https://github.com/source-foundry/Slice/tree/main/thirdparty) for additional details about third party licenses.
