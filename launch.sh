#! /usr/bin/bash
echo GenkaiyaBot_bootloader
nohup sh -c 'python3 slash.py' &
nohup sh -c 'python3 rest.py' &
source env/bin/activate
nohup sh -c 'python3 reaction.py' &
