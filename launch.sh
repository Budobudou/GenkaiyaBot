#! /usr/bin/bash

nohup sh -c 'python3 slash.py; python3 rest.py' &
source env/bin/activate
nohup sh -c 'python3 reaction.py' &