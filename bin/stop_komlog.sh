#!/bin/bash

if [ -f /tmp/komwebagent.pid ]
then
    kill $(cat /tmp/komwebagent.pid)
fi

if [ -f /tmp/komweb.pid ]
then
    kill $(cat /tmp/komweb.pid)
fi

if [ -f /tmp/komanom.pid ]
then
    kill $(cat /tmp/komanom.pid)
fi

if [ -f /tmp/komev.pid ]
then
    kill $(cat /tmp/komev.pid)
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
