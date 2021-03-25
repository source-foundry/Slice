# Developer Documentation

## Requirements

- Python 3.6+ interpreter
- Build dependencies defined in our `dev-requirements.txt` file installed in a Python virtual environment

## Development Environment Setup by Platform

The following instructions define how to build a Python virtual environment, install the appropriate Python dependencies, and launch the application so that you can test your source edits.

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

Close Slice, edit the source, and use `make run` to view your changes.

The test suite is run with:

```
$ tox
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

Close Slice, edit the source, and use `python src\run.py` to view your changes.

The test suite is run with:

```
$ tox
```
