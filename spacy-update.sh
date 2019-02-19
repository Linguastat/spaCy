#!/bin/bash
# Installing spaCy.

# getting default python major version (could be default OS python or an anaconda version)
PYMAJOR=($(python -c "import sys; print(sys.version_info.major)"))
# store python3 version, major and minor
PY3VERSION=$(python3 -V 2>&1)
PY3MAJOR=($(python3 -c "import sys; print(sys.version_info.major)"))
PY3MINOR=($(python3 -c "import sys; print(sys.version_info.minor)"))

# check $CONDAHOME is set
if [ -z "$CONDAHOME" ]
then
      echo "\$CONDAHOME must contain the path to your installed conda."
      exit 1
fi

# Veryify python 2 is the main path installed version
if [ "$PYMAJOR" -ne 2 ]
then
      echo "WARNING: Default Python2 not set as first in PATH, you may need to 'export PATH=\$PATH:\$CONDAHOME/bin' in .bashrc or .bash_profile"
fi

# Verifying $SPACYHOME is set
if [ -z "$SPACYHOME" ]
then
      echo "\$SPACYHOME must contain the path to your previously installed spaCy."
      exit 1
fi

if command -v python3 &>/dev/null; then
    echo "Updating spaCy at $PY3VERSION"
else
    echo 'Python 3 installation could not be found.'
    exit 1
fi

# move to spaCy and pull the latest 
cd $SPACYHOME
# clone spaCy repo
git fetch origin
git checkout master 
git pull origin master 
# install requirements
pip3 install -r requirements.txt
# clean spaCy
python3 setup.py clean
rm spacy/spacy_nlp.cpp
# install spaCy
python3 setup.py build_ext --inplace
# install spaCy developed language models
#python -m spacy download en
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
# install our models

# create the cppd files with cython
cython --embed -o spacy/spacy_nlp.cpp spacy/spacy_nlp.py
# build the binary wrapper
gcc -v -Os -I ${CONDAHOME}/include/python${PY3MAJOR}.${PY3MINOR}m -L ${CONDAHOME}/lib -o ${SPACYHOME}/bin/spacy_nlp ${SPACYHOME}/spacy/spacy_nlp.cpp  -lpython${PY3MAJOR}.${PY3MINOR}m -lpthread -lm -lutil -ldl
