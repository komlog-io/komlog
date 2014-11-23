#!/bin/bash

cd $HOME
nohup python3 bin/komai.py &
echo $! > /tmp/komai.pid
nohup python3 bin/komges.py &
echo $! > /tmp/komges.pid
nohup python3 bin/komdc.py &
echo $! > /tmp/komdc.pid
nohup python3 bin/komrc.py &
echo $! > /tmp/komrc.pid
nohup python3 bin/komweb.py &
echo $! > /tmp/komweb.pid

