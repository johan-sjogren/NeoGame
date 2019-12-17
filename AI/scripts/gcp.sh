#!/bin/sh
# Prerequisites:
#   gcloud auth login `ACCOUNT`

# GCP settings
BUCKET=gs://<YOUR-BUCKET>
REGION=<YOUR-REGION>

# Task settings
PARENT=$(dirname "$0")/..
PACKAGE=trainer
PACKAGE_PATH=$PARENT/$PACKAGE
PACKAGE_TAR=$PARENT/dist/NeoGameAI-0.1.0.tar.gz
TASK=task

submit_package()
{
  [ -f $PACKAGE_TAR ] || python3 ../setup.py sdist bdist_wheel
  echo Copying $PACKAGE_TAR to $BUCKET
  gsutil cp $PACKAGE_TAR $BUCKET
}

submit_job()
{
  JOBNAME=${TASK}_$(date -u +%Y%m%d_%H%M%S)
  gcloud ai-platform jobs submit training $JOBNAME \
    --package-path=$PACKAGE_PATH \
    --module-name=$PACKAGE.$TASK \
    --region=$REGION \
    --staging-bucket=$BUCKET \
    --scale-tier=BASIC \
    --runtime-version=1.14 \
    --python-version 3.5 \
    -- \
    -o $BUCKET/$JOBNAME
}

case $1 in
  submit_package)
    submit_package
    ;;
  submit_job)
    submit_job
    ;;
  *)
    echo Please 'submit_job'
    ;;
esac
  