#!/usr/bin/env python3
import os
import sys
import imp
import subprocess

# what's the default gcc and g++
#print(subprocess.Popen(["gcc","-v"]))
#print(subprocess.call(["g++","-v"]))
os.environ["CC"] = "/usr/bin/gcc48"

# specify gcc for ami production
#os.environ['CC']="/usr/bin/gcc48"
# startup and save python version numbers
print("Spacy modified at: \n" + sys.version)

# store python3 version, major and minor
py3_major = sys.version_info.major
py3_minor = sys.version_info.minor
#PY3VERSION=$(python3 -V 2>&1)
#PY3MAJOR=($(python3 -c "import sys; print(sys.version_info.major)"))
#PY3MINOR=($(python3 -c "import sys; print(sys.version_info.minor)"))

# Verify proper setup
os.environ["FARTS"] = "Gaseous"
subprocess.call("./callfrompy.sh")

# is $CONDAHOME set?
if "CONDAHOME" not in os.environ:
    print("$CONDAHOME must be set with the path to an installed python3 conda environment.")
    exit(1)
# is spacy not installed as a module?
if 'spacy' in sys.modules:
    print("Spacy has been installed as a module (perhaps in pip).  Uninstall before continuing.")
    exit(1)

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


