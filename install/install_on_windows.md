# Installation on Windows

The following instructions are for setting up a development environment on a Windows machine. It is not recommended to use this for a production environment.

The installation on Windows is possible but some aspects don't work e.g. export and import functions.

These instructions are still in an experimental stage, not fully tested and still missing some information.

## Requirements

### Python, Local Http, Pip
To ease installation and use in Windows we suggest to use the Freeware tool [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)
which includes a development server as well as a current version of Python (>=3.7) and the necessary
Python dependency management ([pip](https://pypi.org/project/pip/)).

Install needed libraries with pip:

    pip install -r install/requirements.txt
    
In case you also want to run tests execute:

    pip install -r install/requirements_tests.txt

### PostgreSQL, PostGIS
Choose the appropriate [PostgreSQL - Installer](https://www.postgresql.org/download/windows/) (>=11)

To install the PostGIS extension use the provided PostgreSQL extension manager during install.

## Installation

see [install.md](../install.md)
