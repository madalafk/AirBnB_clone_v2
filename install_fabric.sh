#!/bin/bash

# Uninstall Fabric
pip3 uninstall Fabric

# Install required packages
sudo apt-get update
sudo apt-get install -y libffi-dev libssl-dev build-essential python3.4-dev libpython3-dev

# Install Python packages
pip3 install pyparsing appdirs
pip3 install setuptools==40.1.0 cryptography==2.8 bcrypt==3.1.7 PyNaCl==1.3.0 Fabric3==1.14.post1

# Clean up
sudo apt-get autoremove -y
sudo apt-get clean

echo "Installation complete."

