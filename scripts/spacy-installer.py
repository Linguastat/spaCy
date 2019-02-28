#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from importlib import util
from subprocess import CalledProcessError, call, check_output
#import yum

# set CC to default gcc on PATH
cc = "gcc"

# There are a few ways to do this. Use the yum module in system python, 
# maybe install gcc-python or just make shell calls.
#yb = yum.YumBase()
#yb.conf.cache = os.geteuid() != 0

# need to default to gcc 4X for inclusion of cc1plus file
try:
    default_gccpath = check_output(["which", "gcc"])
    returncode = 0
except CalledProcessError as e:
    default_gccpath = e.output
    print("\nNo gcc could be found. Exit.")
    exit(e.returncode)
# take default gcc path, open and check for gcc4* versions
gccs_path = Path(default_gccpath.decode("utf-8")).parent
gcc4s_list = list(gccs_path.glob('gcc4[0-9]'))
# should only contain one gcc4X, load as cc
if gcc4s_list:
    cc = gcc4s_list[0].name
# set the environment variable for the session
print("spaCy build gcc version set: " + cc)
os.environ["CC"] = cc

# startup and save python version numbers
print("spaCy install destination:\n" + sys.version)

# set python3 version, major and minor
os.environ["PY3MAJOR"] = str(sys.version_info.major)
os.environ["PY3MINOR"] = str(sys.version_info.minor)

# is $CONDAHOME set?
if "CONDAHOME" not in os.environ:
    print("$CONDAHOME must be set with the path to an installed python3 conda environment.")
    exit(1)
# is spacy not installed as a module?
if 'spacy' in sys.modules:
    print("Spacy has been installed as a module (perhaps in pip).  Uninstall before continuing.")
    exit(1)
# checking if spacy installed at $SPACYHOME
find_spacy = util.find_spec('spacy')
if find_spacy is None:
    print("Invoking spacy-install.sh")
    call("./spacy-install.sh")
else:
    if "SPACYHOME" in os.environ:
        print("Invoking spacy-update.sh")
        call("./spacy-update.sh")
    else:
        print("Spacy is installed via source but SPACYHOME does not exist.  Please set SPACYHOME.")
