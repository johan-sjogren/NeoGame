#!/bin/sh
# Prerequisites:
#   gcloud auth login `ACCOUNT`

# GCP settings
BUCKET=gs://<YOUR-BUCKET>
REGION=<YOUR-REGION>
SCALE_TIER=BASIC
RUNTIME_VERSION=1.14
PYTHON_VERSION=3.5

# Local settings
PARENT=$(dirname "$0")/..
TAR_NAME=NeoGameAI-0.1.0.tar.gz
PACKAGE=trainer
PACKAGE_PATH=$PARENT/$PACKAGE
PACKAGE_TAR=$PARENT/dist/$TAR_NAME
TASK=task

# Host settings
PACKAGE_TAR_HOST=$BUCKET/$TAR_NAME

submit_package()
{
  [ -f $PACKAGE_TAR ] || python3 ../setup.py sdist bdist_wheel
  echo Copying $PACKAGE_TAR to $BUCKET
  gsutil cp $PACKAGE_TAR $BUCKET
}

run_package_job()
{
  JOBNAME=${TASK}_$(date -u +%Y%m%d_%H%M%S)
  gcloud ai-platform jobs submit training $JOBNAME \
    --packages $PACKAGE_TAR_HOST \
    --module-name $PACKAGE.$TASK \
    --region $REGION \
    --scale-tier $SCALE_TIER \
    --runtime-version $RUNTIME_VERSION \
    --python-version $PYTHON_VERSION \
    -- \
    -o $BUCKET/$JOBNAME
}

submit_job()
{
  JOBNAME=${TASK}_$(date -u +%Y%m%d_%H%M%S)
  gcloud ai-platform jobs submit training $JOBNAME \
    --package-path $PACKAGE_PATH \
    --module-name $PACKAGE.$TASK \
    --region $REGION \
    --staging-bucket $BUCKET \
    --scale-tier $SCALE_TIER \
    --runtime-version $RUNTIME_VERSION \
    --python-version $PYTHON_VERSION \
    -- \
    -o $BUCKET/$JOBNAME
}

case $1 in
  submit_package)
    submit_package
    ;;
  run_package_job)
    run_package_job
    ;;
  submit_job)
    submit_job
    ;;
  *)
    echo "$0"
    echo "Options:"
    echo "    submit_package"
    echo "    run_package_job"
    echo "    submit_job"
    ;;
esac
  