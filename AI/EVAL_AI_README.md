# NeoGame AI challenge at eval.ai

This documents how to take part in the NeoGame AI challenge hosted on eval.ai
by Neodev AB.
The challenge is to create and train your own agent, and test it versus
other agents. You can find the challenge at https://eval.ai/web/challenges/list.
The challenge is based on the NeoGame cardgame. You can access this source code
at https://github.com/neodev-ab/NeoGame ('develop' branch)
and try playing the game at http://cardgame.neodev.se.
For any questions regarding the challenge or the code contact nura.mahmod@neodev.se
The process is divided into four parts

- Setting up the code
- Creating your own model
- Training your model
- Uploading your model

# Setting up the code
You can download the source code by, for example:  
```git clone https://github.com/neodev-ab/NeoGame.git```  
Checkout the development branch with:  
```git checkout develop```  
You can use anaconda for installing dependencies https://docs.anaconda.com/anaconda/install/.

Setup a conda env for NeoGame with:  
```conda create --name neogame python=3.7```  
```conda activate neogame```  
Run the setup.py in the AI-folder  
```pip install .```  
All of the code that is relevant for this challenge lies in either the 'AI' or the EvalAI folder,
 the rest of the code is related to the webserver that is hosting the cardgame.

# Creating your own model
[CustomAgent](https://github.com/neodev-ab/NeoGame/blob/develop/EvalAI/examples/CustomAgent.py) contains an example/baseline for the submission agent with the neccessary functions. 

# Training your modelj
[This script](https://github.com/neodev-ab/NeoGame/blob/develop/AI/scripts/training_script.py) gives an example of how your model could be trained.
The Gym class is also used during the evaluation so if you model works with 
this script then it should work for the submission.

# Uploading your model
When you have trained/created an agent that you are happy with, go to
https://eval.ai/web/challenges/list and look for 'NeoGame AI Challenge'.
Make sure that your model is saved within a '.zip' file. This file should contain:  
* CustomAgent.py (Yes, the name is important)
* CustomAgent.csv (Optional)
* CustomAgent.h5 (Optional)

Go to the submit tab and upload your model. The model will be automatically
evaluated and your model should show up on the leaderboard as long as nothing
went wrong during the evaluation.
