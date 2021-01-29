#!/bin/bash

# Creates a zipfile that can be used to create a new challenge on eval.ai

# Remove already existing zip files
rm evaluation_script.zip
rm challenge_config.zip

# Create new zip configuration according the updated code
cd evaluation_script
# Copy NeoGame dependencies
cp -r ../../AI/pyneogame pyneogame
cp -r ../../AI/models models
zip -r evaluation_script.zip *  -x "*.DS_Store"
rm -rf pyneogame
rm -rf models
cd ..
mv evaluation_script/evaluation_script.zip evaluation_script.zip
zip -r challenge_config.zip *  -x "*.DS_Store" -x "evaluation_script/*" -x "*.git" -x "run.sh" -x "code_upload_challenge_evaluation/*" -x "worker/*" -x "challenge_data/*" -x "github/*" -x ".github/*" -x "README.md"
