#!/bin/bash

cd $HOME
nohup python komlog/komai/komai.py > /var/log/komlog/komai.log 2>&1 &
echo $! > /tmp/komai.pid
nohup python komlog/komges/komges.py > /var/log/komlog/komges.log 2>&1 &
echo $! > /tmp/komges.pid
nohup python komlog/komdc/komdc.py > /var/log/komlog/komdc.log 2>&1 &
echo $! > /tmp/komdc.pid
nohup python komlog/komrc/komrc.py > /var/log/komlog/komrc.log 2>&1 &
echo $! > /tmp/komrc.pid
nohup python komlog/komws2/komws2.py > /var/log/komlog/komws2.log 2>&1 &
echo $! > /tmp/komws2.pid

