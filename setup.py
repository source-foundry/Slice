import io
import json
import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

# Package meta-data.
NAME = "slicegui"
DESCRIPTION = "Variable font instance generator PyQt5 GUI application"
LICENSE = "GNU General Public License v3 (GPLv3)"
URL = "https://github.com/source-foundry/Slice"
EMAIL = "chris@sourcefoundry.org"
AUTHOR = "Source Foundry Authors"
REQUIRES_PYTHON = ">=3.6.0"

INSTALL_REQUIRES = [
    "fontTools >= 4.21.1",
]
# Optional packages
EXTRAS_REQUIRES = {
    # for developer installs
    "dev": ["coverage", "pytest", "pytest-qt", "tox", "flake8", "black", "isort"],
    # for maintainer installs
    "maintain": ["wheel", "setuptools", "twine"],
}

this_file_path = os.path.abspath(os.path.dirname(__file__))

# Version
with open(Path("src/build/settings/base.json")) as f:
    base_json = json.load(f)
    VERSION = base_json["version"]

# Use repository Markdown README.md for PyPI long description
try:
    with io.open("README.md", encoding="utf-8") as f:
        readme = f.read()
except IOError as readme_e:
    sys.stderr.write(
        "[ERROR] setup.py: Failed to read the README.md file for the long description definition: {}".format(
            str(readme_e)
        )
    )
    raise readme_e

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    platforms=["Any"],
    long_description=readme,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    python_requires=REQUIRES_PYTHON,
    entry_points={"console_scripts": ["slicegui = slice.__main__:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia",
    ],
)