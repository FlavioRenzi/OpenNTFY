#!/bin/sh
# This script is used to install the application

cd /usr/local/bin
sudo wget -O OpenNTFY "https://github.com/FlavioRenzi/OpenNTFY/raw/master/dist/OpenNTFY"
sudo chmod +x OpenNTFY

# Create config file

cd ~
if [ ! -d ".config" ]; then
  echo "Creating .config folder"
  sudo mkdir .config
fi
cd .config
if [ ! -d "OpenNTFY" ]; then
    echo "Creating OpenNTFY folder"
  sudo mkdir OpenNTFY
fi
cd OpenNTFY
if [ ! -f "config.json" ]; then
    echo "Creating config.json file"
  sudo wget -O config.json "https://raw.githubusercontent.com/FlavioRenzi/OpenNTFY/master/example-config.json"
fi
