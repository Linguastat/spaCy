#!/bin/bash
# Installing the conda python application required for spaCy.

# Python install
# move $HOME and install at user priveleges
cd ~
# download specific python 3 conda version
wget https://repo.anaconda.com/miniconda/Miniconda3-4.5.12-Linux-x86_64.sh -O ~/miniconda.sh
# batch install of miniconda using standard miniconda name
bash ~/miniconda.sh -b -p ~/miniconda
# set environment variables
echo -e '\n' >> ~/.bashrc
echo '# Linguastat Conda and Python environment settings added by conda-install.sh' >> ~/.bashrc
echo 'export CONDAHOME="$HOME/miniconda"' >> ~/.bashrc
echo '#LD_LIBRARY_PATH="$CONDAHOME/lib"' >> ~/.bashrc
echo 'export PATH="$PATH:$CONDAHOME/bin"' >> ~/.bashrc