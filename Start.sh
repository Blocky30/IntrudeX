#!/bin/bash
echo -ne "\033]0;IntrudeX.exe\007"
echo -e "\e[32m"
python3 main.py
read -p "Press any key to continue..."