#!/bin/bash

cd $HOME
nohup komlogs/bin/komai.py &
echo $! > /tmp/komai.pid
nohup komlogs/bin/komges.py &
echo $! > /tmp/komges.pid
nohup komlogs/bin/komdc.py &
echo $! > /tmp/komdc.pid
nohup komlogs/bin/komrc.py &
echo $! > /tmp/komrc.pid
nohup komlogs/bin/komweb.py &
echo $! > /tmp/komweb.pid
