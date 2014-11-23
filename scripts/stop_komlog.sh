#!/bin/bash

if [ -f /tmp/komweb.pid ]
then
    kill $(cat /tmp/komweb.pid)
fi

if [ -f /tmp/komges.pid ]
then
    kill $(cat /tmp/komges.pid)
fi

if [ -f /tmp/komdc.pid ]
then
    kill $(cat /tmp/komdc.pid)
fi

if [ -f /tmp/komai.pid ]
then
    kill $(cat /tmp/komai.pid)
fi

if [ -f /tmp/komrc.pid ]
then
    kill $(cat /tmp/komrc.pid)
fi
