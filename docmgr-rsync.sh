#!/bin/bash

SRC=$1
SRC_PATH=${2:-"/var/lib/docmgr/files"}
DEST_PATH=${3:-"$SRC_PATH"}
LOG_FILE=${4:-"/var/log/docmgr/rsync.log"}

if [ $# -ne 1 ]
then
    echo "Need to specify host!"
    echo

    echo "Usage: `basename $0` HOST [ SRC_PATH[=$SRC_PATH] DEST_PATH[=$DEST_PATH] LOG_FILE[=$LOG_FILE] ]"
    exit 1
fi

date &>> $LOG_FILE
rsync -e ssh -avzu --delete --stats $SRC:${SRC_PATH}/* ${DEST_PATH} &>> $LOG_FILE

