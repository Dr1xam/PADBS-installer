#!/bin/bash
rm -rf "./ansible"
mkdir ./ansible
#створення локального серидовища
python3 -m venv ./ansible/venv --without-pip
#використання локального серидовища (venv)
source ./ansible/venv/bin/activate
#Встановлення pip у venv
python3 ./resources/software/pip/get-pip.py --no-index --find-links=./resources/software/pip/
#Встановлення ansible у venv
pip install --no-index --find-links=./resources/software/ansible/ ansible
mkdir ./ansible/playbooks