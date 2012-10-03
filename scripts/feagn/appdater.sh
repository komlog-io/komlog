#!/bin/bash

MAILTO="jcazor@gmail.com"
REPOBASEDIR=$HOME/komlog
LOGFILE=$HOME/tmp/appdater.log
TESTDIR=${REPOBASEDIR}/tests



function notify_by_mail {
   mail -s "AppDater Execution - `date +"%Y/%m/%d - %T"`" $MAILTO < $LOGFILE
}

function exec_tests {
   cd $TESTDIR
   for file in `ls test_*.py`
   do
      python $file >> $LOGFILE 2>&1
   done
}

function fetch {
   cd $REPOBASEDIR
   OLD_SHA=`git log --pretty=format:"%H" -n1`
   OLD_CKSUM=`cksum $HOME/komlog/scripts/feagn/appdater.sh`
   git fetch
   git merge origin/master
   NEW_SHA=`git log --pretty=format:"%H" -n1`
   NEW_CKSUM=`cksum $HOME/komlog/scripts/feagn/appdater.sh`
}

. $HOME/.bash_profile
fetch

if [ "$NEW_SHA" == "$OLD_SHA" ]; then
   echo "CHANGES: NO" > $LOGFILE
   echo "VERSION: $NEW_SHA" >> $LOGFILE
   echo "" >> $LOGFILE
   exit
elif [ "$OLD_CKSUM" == "$NEW_CKSUM" ]; then
   echo "CHANGES: YES" > $LOGFILE
   echo "VERSION: $SHA" >> $LOGFILE
   echo "" >> $LOGFILE
   exec_tests
   notify_by_mail
else 
   $HOME/komlog/scripts/feagn/appdater.sh
fi


