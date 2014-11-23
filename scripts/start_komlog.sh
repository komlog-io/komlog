#!/bin/bash

cd $HOME
nohup python3 komlogs/bin/komai.py &
echo $! > /tmp/komai.pid
nohup python3 komlogs/bin/komges.py &
echo $! > /tmp/komges.pid
nohup python3 komlogs/bin/komdc.py &
echo $! > /tmp/komdc.pid
nohup python3 komlogs/bin/komrc.py &
echo $! > /tmp/komrc.pid
nohup python3 komlogs/bin/komweb.py &
echo $! > /tmp/komweb.pid

