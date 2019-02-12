#!/bin/bash
# Installing spaCy.

# Verify python 3 is the main path installed version
PYTHON=$(python -V 2>&1)

if command -v python3 &>/dev/null; then
    echo "Updating spaCy at $PYTHON"
else
    echo 'Python 3 installation could not be found.'
    exit 1
fi

# store python version major and minor
PYMAJOR=($(python -c "import sys; print(sys.version_info.major)"))
PYMINOR=($(python -c "import sys; print(sys.version_info.minor)"))

# move to spaCy and pull the latest 
cd ~/spaCy
# clone spaCy repo
git fetch origin
git pull origin master 
# install requirements
pip install -r requirements.txt
# clean spaCy
python setup.py clean
rm spacy/spacy_nlp.cpp
# install spaCy
python setup.py build_ext --inplace
# install spaCy developed language models
#python -m spacy download en
#python -m spacy download en_core_web_sm
#python -m spacy download en_core_web_md
# install our models

# create the cpp files with cython
cython --embed -o spacy/spacy_nlp.cpp spacy/spacy_nlp.py
# build the binary wrapper
gcc -v -Os -I ${CONDAHOME}/include/python${PYMAJOR}.${PYMINOR}m -L ${CONDAHOME}/lib -o ${SPACYHOME}/bin/spacy_nlp ${SPACYHOME}/spacy/spacy_nlp.cpp  -lpython${PYMAJOR}.${PYMINOR}m -lpthread -lm -lutil -ldl
