#!/bin/bash

cd $HOME
nohup python komlogs/komai/komai.py > /var/log/komlog/komai.log 2>&1 &
echo $! > /tmp/komai.pid
nohup python komlogs/komges/komges.py > /var/log/komlog/komges.log 2>&1 &
echo $! > /tmp/komges.pid
nohup python komlogs/komdc/komdc.py > /var/log/komlog/komdc.log 2>&1 &
echo $! > /tmp/komdc.pid
nohup python komlogs/komrc/komrc.py > /var/log/komlog/komrc.log 2>&1 &
echo $! > /tmp/komrc.pid
nohup python komlogs/komws2/komws2.py > /var/log/komlog/komws2.log 2>&1 &
echo $! > /tmp/komws2.pid

