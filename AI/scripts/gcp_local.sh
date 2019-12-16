#!/bin/sh

# Task settings
PARENT=$(dirname "$0")/..
PACKAGE=trainer
PACKAGE_PATH=$PARENT/$PACKAGE
TASK=task

export PYTHONPATH=${PYTHONPATH}:${PACKAGE_PATH}

train()
{
  JOBNAME=${TASK}_$(date -u +%Y%m%d_%H%M%S)
  gcloud ai-platform local train \
    --package-path=$PACKAGE_PATH \
    --module-name=$PACKAGE.$TASK \
    -- \
    -o $PARENT/jobs/$JOBNAME
}

case $1 in
  train)
    train
    ;;
  *)
    echo Please 'train'
    ;;
esac