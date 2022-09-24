#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
path = os.path.dirname(os.path.realpath(__file__))
os.system("sudo apt install python3-pip -y")
os.system("sudo apt install python3-pyqt5 -y")
os.system("python3 -m pip install numpy")
os.system("python3 -m pip install pyqt5")
os.system("python3 -m pip install matplotlib")
os.system("chmod u+x edosv.py")
os.system(f"ln -s {path}/edosv.desktop  ~/.local/share/applications/edosv.desktop")

