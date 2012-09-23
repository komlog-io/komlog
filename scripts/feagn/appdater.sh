#!/bin/bash

function notify_by_mail {
   mail -s "AppDater Execution - `date +"%Y/%m/%d - %T"`" jcazor@gmail.com < $HOME/tmp/appdater.log
}

cd $HOME/komlog

git fetch

SHA=`git log --pretty=format:"%H" -n1`

if [ -f $HOME/tmp/komlog.vrs ]; then
   OLD_SHA=`cat $HOME/tmp/komlog.vrs`
else
   OLD_SHA=0
fi

if [ "$SHA" == "$OLD_SHA" ]; then
   echo "CHANGES: NO" > $HOME/tmp/appdater.log
   echo "VERSION: $SHA" >> $HOME/tmp/appdater.log
   exit
else
   echo "CHANGES: YES" > $HOME/tmp/appdater.log
   echo "VERSION: $SHA" >> $HOME/tmp/appdater.log
   echo "" >> $HOME/tmp/appdater.log
   echo $SHA > $HOME/tmp/komlog.vrs
   notify_by_mail
fi


