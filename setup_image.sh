#!/bin/bash

# Update apt
sudo apt-get update
sudo apt-get upgrade -y
sudo apt install python3-pip -y

# # Get and unzip MIND dataset
# wget https://mind201910small.blob.core.windows.net/release/MINDsmall_train.zip
# sudo apt-get install unzip
# unzip MINDsmall_train.zip

# # Set up working directory
# git clone https://github.com/schwartzadev/info-4871.git
# mv news.tsv info-4871/
# mv behaviors.tsv info-4871/
# cd info-4871

# Configure + run python
pip3 install pandas
pip3 install librec_auto
# python3 generate_ratings.py
python3 -m librec_auto -t schwartz-mind run
