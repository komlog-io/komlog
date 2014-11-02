#!/bin/bash

cd $HOME
nohup python komlogs/komai/komai.py &
echo $! > /tmp/komai.pid
nohup python komlogs/komges/komges.py &
echo $! > /tmp/komges.pid
nohup python komlogs/komdc/komdc.py &
echo $! > /tmp/komdc.pid
nohup python komlogs/komrc/komrc.py &
echo $! > /tmp/komrc.pid
nohup python komlogs/komws2/komws2.py &
echo $! > /tmp/komws2.pid

