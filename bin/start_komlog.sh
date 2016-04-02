#!/bin/bash

cd $HOME
nohup komai.py &
echo $! > /tmp/komai.pid
nohup komges.py &
echo $! > /tmp/komges.pid
nohup komdc.py &
echo $! > /tmp/komdc.pid
nohup komrc.py &
echo $! > /tmp/komrc.pid
nohup komev.py &
echo $! > /tmp/komev.pid
nohup komanom.py &
echo $! > /tmp/komanom.pid
nohup komweb.py &
echo $! > /tmp/komweb.pid
nohup komwebagent.py &
echo $! > /tmp/komwebagent.pid

