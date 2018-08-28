from setuptools import setup
from getpass import getpass
import os
from pathlib import Path

with open("../README.md", 'r') as f:
    long_description = f.read()

with open("./openneurodata/oneibl/params.py") as f:
    param_file = f.read()


def _get_par(pname):
    for l in param_file.split('\n'):
        if l.startswith(pname):
            return l.split('=')[-1].replace('"', '').replace("'", '').strip()


def _set_par(fname, replacements):
    with open(fname) as f:
        param_file = f.read()
    # list with one item per line
    lfile = param_file.split('\n')
    # replaces all values defined
    for key, value in replacements.items():
        for ind, l in enumerate(lfile):
            if l.startswith(key):
                lfile[ind] = key + " = '" + value + "'"
                break
    # overwrite
    with open(fname, 'w') as f:
        f.write('\n'.join(lfile))


# User Input Data
BASE_URL = input("Enter the URL of Alyx Instance [" + _get_par('BASE_URL') + "]:")\
    or _get_par('BASE_URL')
print(BASE_URL)
ALYX_LOGIN = input("Enter Alyx username [" + _get_par('ALYX_LOGIN') + "]:")\
             or _get_par('ALYX_LOGIN')
print(ALYX_LOGIN)

ALYX_PWD = getpass("Enter the Alyx password for " + ALYX_LOGIN + ': ')
if not ALYX_PWD:
    print("A password is mandatory.")
    exit(1)
if getpass("Enter the Alyx password (again):") != ALYX_PWD:
    print("The passwords don't match.")
    exit(1)

CACHE_DIR = str(Path.home()) + os.sep + "Downloads" + os.sep + "FlatIron"
CACHE_DIR = input('Directory to cache FlatIron downloads [' + CACHE_DIR + ']:') or CACHE_DIR
print(CACHE_DIR)

HTTP_DATA_SERVER_LOGIN = input("Enter the FlatIron username [" + _get_par("HTTP_DATA_SERVER_LOGIN")
                               + "]:") or _get_par("HTTP_DATA_SERVER_LOGIN")
print(HTTP_DATA_SERVER_LOGIN)
HTTP_DATA_SERVER_PWD = getpass("Enter the FlatIron password: ")
if not HTTP_DATA_SERVER_PWD:
    print("A password is mandatory.")
    exit(1)
if getpass("Enter the FlatIron password (again):") != HTTP_DATA_SERVER_PWD:
    print("The passwords don't match.")
    exit(1)

# REPLACE IN FILES
replacements = {
    'BASE_URL': BASE_URL,
    'ALYX_LOGIN ': ALYX_LOGIN,
    'HTTP_DATA_SERVER_LOGIN': HTTP_DATA_SERVER_LOGIN,
    'CACHE_DIR': CACHE_DIR
}
_set_par("./openneurodata/oneibl/params.py", replacements)

replacements = {
    'HTTP_DATA_SERVER_PWD': HTTP_DATA_SERVER_PWD,
    'ALYX_PWD': ALYX_PWD
}
_set_par("./openneurodata/oneibl/params_secret.py", replacements)

setup(
   name='ibllib',
   version='0.1.2',
   description='IBL libraries',
   license="MIT",
   long_description=long_description,
   author='IBL Staff',
   url="https://www.internationalbrainlab.com/",
   packages=['ibllib', 'oneibl', 'oneibl.examples'],  # same as name
   package_dir={'oneibl': 'openneurodata/oneibl',
                'oneibl.example': 'openneurodata/oneibl/examples'},
   install_requires=['dataclasses', 'matplotlib', 'numpy', 'pandas',
                     'requests'],  # external packages as dependencies
   scripts=[]
)
