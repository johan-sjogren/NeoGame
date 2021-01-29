# NeoGame AI challenge at eval.ai

This documents how to take part in the NeoGame AI challenge hosted on eval.ai
by Neodev AB.
The challenge is to create and train your own DeepQ model, and test it versus
other agents. You can find the challenge at https://eval.ai/web/challenges/list.
The challenge is based on the NeoGame cardgame. You can access this source code
at https://github.com/neodev-ab/NeoGame ('development' branch)
and try playing the game at http://cardgame.neodev.se.
For any questions regarding the challenge or the code contact nura.mahmod@neodev.se
The process is divided into four parts

- Setting up the code
- Creating your own model
- Training your model
- Uploading your model

# Setting up the code
You can download the source code by, for example 'git clone https://github.com/neodev-ab/NeoGame.git'
Checkout the development branch with 'git checkout development'
You can use anaconda for installing dependencies https://docs.anaconda.com/anaconda/install/.

Setup a conda env for NeoGame with 'conda create --name neogame --file AI/requirements.txt'
and 'conda activate neogame'
All of the code that is relevant for this challenge lies in the 'AI' folder, the rest of the code
is related to the webserver that is hosting the cardgame.

# Creating your own model
DeepQAgent.py contains the logic for using a keras model (.h5 file) to predict the best move.
You are allowed to edit this file to create the best model for a DeepQAgent.
The model inputs the board states and outputs a value for each possible action.
The DeepQAgent will choose the action with the highest value (if it is not training in case it
might explore a random move instead).
The model will then be trained by assigning rewards to actions that it has played in recent games.
A good DeepQAgent will correctly predict the expected rewards for each possible action,
and choose the action with the best possible expected reward.

## _make_model()
The _make_model() function creates this keras model, layer by layer. We are encouraging the
contestants to edit this function for creating the best keras model for NeoGame.
Edit/add/remove layers to create your own model. You are allowed to edit this function however
you want but it is adviceable to keep the 'input_layer', 'embedding', 'flat' and 'output'
layers intact since the sizes of these need to match the sizes of the inputs and outputs
of the agent. 
The default _make_model() function will create an OK DeepQAgent so it can
be a good idea to keep your model relatively close to this. The 'flat' layer has size 36
and 'output' has size 10 so it can be a good idea to keep your edited layers at a similar size.
Another tip can be to not use too many hidden layers as this can cause training to be slow.
You could also edit the kernel_regularizer, bias_regularizer or optimizer.

## training code
You are also allowed to change the way the DeepQAgent trains by changing some of the training
functions. You could for example edit learn() or replay_experience().
These functions are working as they are and you should not need to edit them in order to create
a good model. You should not edit any of the code which is involved in getting an action from the
DeepQAgent (for example get_action()). Your model will be tested on the code from
the development branch, so any local changes in how the agent acts will cause the testing to be invalid.

# Training your model
Running the training_script.py will create a new DeepQAgent with the model from _make_model()
and start training it. The model will play against the opponent model, which is defaulted as
a greedy agent. It will use the results from their games as training data, and also test
how well the model does versus this opponent.
You can train and test your model versus 3 main agents; Random, Greedy and DeepQ.
The moves of the Random agent are completely random. The greedy agent chooses the move that
maximizes the score from the cards that are visible to it. The DeepQ agent uses a pretrained
model to determine the best moves.
You are allowed to edit training_script.py if you want to train your model
differently, or want another name for your model (default is new_dq_agent.h5).
Running keep_training.py will load an existing model (default is new_dq_agent.h5) and keep
training it. At the end of the script the model will be overwritten with the new training.
You can keep running keep_training.py until you are happy with the model
(and edit the script if you want to). Alot of the actual training code is inside gym.py.
You can also edit this training code if you want to (but it should not be needed).
You can test your model versus multiple agents with benchmark.py. The total score should
put a good estimate on how well the model will do on the eval.ai evaluation as long as no code
for getting action or testing has been edited.

# Uploading your model

When you have trained a keras model that you are happy with, go to
https://eval.ai/web/challenges/list and look for 'NeoGame AI Challenge'.
Make sure that your model is saved as a '.h5' file and that it is compatible
with DeepQAgent.py.
Go to the submit tab and upload your model. The model will be automatically
evaluated and your model should show up on the leaderboard as long as nothing
went wrong during the evaluation.
