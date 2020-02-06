# Code for development, training and deployment of AI models for the game

## Training the AI models on Google Cloud Platform
This repository contains helper scripts for submitting training jobs to Google Cloud Platform, GCP, and follows the guidelines for packaging the trainer scripts [](https://cloud.google.com/ai-platform/training/docs/packaging-trainer#project-structure). Below is a table of the scripts, including a description of their intended usage.

|Script|Description|
|:-|:-|
|AI/scripts/gcp_local.sh|A helper script for verifying training tasks|
|AI/scripts/gcp.sh|A helper script for submitting jobs|
|AI/trainer/task.py|A sample training task that trains Neogame agents|

### Prerequisites
Before training models on GCP, your Google account has to be set up and some of Google's services need to be activated.

1. Open the **console** on GCP, https://console.cloud.google.com/
2. Setup up your Google account for GCP by entering your address and billing information.
3. Create a project in the console, https://cloud.google.com/resource-manager/docs/creating-managing-projects
3. Enable the following APIs, https://cloud.google.com/endpoints/docs/openapi/enable-api
    - **AI Platform Training & Prediction API**
    - **Compute Engine API**
4. Create a **Storage Bucket** for storing files and data during training, https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-console
5. Install the **Google Cloud SDK** on your machine, https://cloud.google.com/sdk/install

### Step-by-step instructions for submitting jobs
With the account prepared and services set up, one can now submit training jobs to GCP. Below is a step-by-step guideline on how to do this.

1. In a terminal, log in to GCP with your Google account using **gcloud** and follow the instructions
    ```
    gcloud auth login
    ```
2. Set the project
    ```
    gcloud projects list
    gcloud config set project <YOUR-PROJECT>
    ```
3. Before submitting a training job it can be tested locally using **AI/scripts/gcp_local.sh**
    ```
    AI/scripts/gcp_local.sh train
    ```
    NOTE: If you have developed your own python script that you want to submit as a training job, add it to **AI/trainer** and modify the TASK variable in the shell script. This also applies for the shell script that actually submits the training job.
4. When your python script is ready, submit it with **AI/scripts/gcp.sh**. Fill in the **BUCKET**, **REGION** and **TASK** variables according to your GCP setup
    ```
    AI/scripts/gcp.sh submit_job
    ```
    For more settings on how to submit jobs, cf. https://cloud.google.com/ai-platform/training/docs/training-jobs. When the job has been submitted the following print is displayed:
    ```
    AI/scripts/gcp.sh submit_job
    Job [task_20191117_184759] submitted successfully.
    Your job is still active. You may view the status of your job with the command

      $ gcloud ai-platform jobs describe task_20191117_184759

    or continue streaming the logs with the command

      $ gcloud ai-platform jobs stream-logs task_20191117_184759

    jobId: task_20191117_184759
    state: QUEUED
    ```
5. To copy back the result, use **gsutil**
    ```
    gsutil cp -r  gs://<YOUR_BUCKET>/task_20191117_184759 <TARGET>
    ```