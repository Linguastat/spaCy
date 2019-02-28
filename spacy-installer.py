#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import importlib
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
os.environ["CC"] = cc

# startup and save python version numbers
print("Spacy install destination:\n" + sys.version)

# store python3 version, major and minor
py3_major = sys.version_info.major
py3_minor = sys.version_info.minor
#PY3VERSION=$(python3 -V 2>&1)
#PY3MAJOR=($(python3 -c "import sys; print(sys.version_info.major)"))
#PY3MINOR=($(python3 -c "import sys; print(sys.version_info.minor)"))

# Verify proper setup
#os.environ["FARTS"] = "Gaseous"
#subprocess.call("./callfrompy.sh")

# is $CONDAHOME set?
if "CONDAHOME" not in os.environ:
    print("$CONDAHOME must be set with the path to an installed python3 conda environment.")
    exit(1)
# is spacy not installed as a module?
#if 'spacy' in sys.modules:
#    print("Spacy has been installed as a module (perhaps in pip).  Uninstall before continuing.")
#    exit(1)

# checking if spacy installed $SPACYHOME and its module
#try:
#    imp.find_module('spacy')
#    found = True;
#except ImportError:
#    found = False

#print(found)

# make sure gcc has cc1plus



#    echo "\$SPACYHOME must not already be installed.  Run the spacy-update.sh instead"
#    exit 1
#fi

# update spacy
call("./spacy-update.sh")

