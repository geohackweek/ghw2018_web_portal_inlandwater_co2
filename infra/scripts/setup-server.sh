#!/usr/bin/env bash

URL="http://bit.ly/miniconda"

if [ ! -f $HOME/miniconda/bin/conda ] ; then
    echo "Fresh miniconda installation."
    wget $URL -O miniconda.sh
    rm -rf $HOME/miniconda
    bash miniconda.sh -b -p $HOME/miniconda
fi

export PATH="$HOME/miniconda/bin:$PATH"

conda update conda --yes
conda config --set show_channel_urls true
conda config --add channels conda-forge --force
conda env create --file $APP_PATH/src/backend/environment.yml