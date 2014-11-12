#!/bin/bash

cd $HOME
nohup python3 komlogs/komai/komai.py &
echo $! > /tmp/komai.pid
nohup python3 komlogs/komges/komges.py &
echo $! > /tmp/komges.pid
nohup python3 komlogs/komdc/komdc.py &
echo $! > /tmp/komdc.pid
nohup python3 komlogs/komrc/komrc.py &
echo $! > /tmp/komrc.pid
nohup python3 komlogs/komws2/komws2.py &
echo $! > /tmp/komws2.pid

