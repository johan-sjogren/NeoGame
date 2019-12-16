import pandas as pd
import numpy as np
from collections import deque
import random
from os import path
from keras import Model
from keras.models import save_model, load_model
from keras.layers import Input, Dense, Embedding, Flatten, LSTM, Bidirectional
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.regularizers import l2
import h5py

from . import BaseAgent

# TODO: Create a Dueling DQN
# TODO: Prioritized experience replay
# TODO: Create and compare with a policy learning agent


class DeepQAgent(BaseAgent.BaseAgent):
    """ Deep Q-learning Agent
    This implementation will take a state as input,
    estimate the Q value Q(s, a_x) for all actions a_x and
    select the action with the highest Q value if exploiting.
    """

    def __init__(self, state_size, actions,
                 model=None,
                 epsilon=0.9,
                 decay_rate=1e-5,
                 update_interval=25000,
                 memory_size=100000,
                 verbose=0,
                 loss="mse",
                 reg_lambda=0.0001,
                 filename="dq_agent",
                 preprocess=True):

        self.actions = actions
        self.verbose = verbose
        self.epsilon = epsilon
        self.decay_rate = decay_rate
        self.memory = deque(maxlen=memory_size)
        self.update_dnn_interval = 2 * update_interval
        self.episode_counter = 0
        self.state_size = state_size
        self.r_sum = 0
        self.avg_r_sum = []
        self.loss=loss
        self.reg_lambda = reg_lambda
        self.filename = filename
        self.training_iterations = 0
        self.preprocess = preprocess

        if model is None:
            print("Building default model")
            self.dnn_model = self._make_model()
        else:
            model.compile(loss=self.loss,
                      optimizer='adam')
            self.dnn_model = model
        self.org_weights = self.dnn_model.get_weights()

    def __str__(self):
        return "Deep Q Agent"

    def save(self, filename):
        """Saving DeepQ agent as filename (default extension .h5)"""
        filename += '.h5'
        self.dnn_model.save(filename)
        return self

    def load(self, filename, custom_objects=None, compile=True):
        if not path.isfile(filename):
            raise IOError("No model can be loaded since {} does not exist".format(filename))
        if not h5py.is_hdf5(filename):
            raise ValueError('No model can be loaded since {} is not an HDF5 file'.format(filename))

        self.dnn_model = load_model(filename,
                                    custom_objects=custom_objects,
                                    compile=compile)
        self.dnn_model._make_predict_function()
        
        print('Model loaded')

        return self

    def _make_model(self):
        '''Start with a simple default model for now'''
        input_layer = Input(shape=(self.state_size,))
        embedding = Embedding(input_dim=5, output_dim=4)(input_layer)
        flat = Flatten()(embedding)
        dense_1 = Dense(32, activation='relu', use_bias=True,
            kernel_regularizer=l2(self.reg_lambda), bias_regularizer=l2(self.reg_lambda))(flat)  # input_layer)
        x = Dense(32, activation='relu', use_bias=True,
            kernel_regularizer=l2(self.reg_lambda), bias_regularizer=l2(self.reg_lambda))(dense_1)
        output = Dense(len(self.actions), use_bias=True,
            kernel_regularizer=l2(self.reg_lambda), bias_regularizer=l2(self.reg_lambda))(x) # Linear as it is predicting a Q value
        model = Model(inputs=input_layer, outputs=output)
        model.compile(loss=self.loss,
                      optimizer='adam')
        if self.verbose:
            print(model.summary())
        return model

    def _act(self, state):
        state = state.reshape(1, state.shape[0])
        act_values = self.dnn_model.predict(state)
        # Get and return the action given by the index
        act_idx = np.argmax(act_values[0])
        return self.actions[act_idx]

    def get_action(self, state, actions=None,
                   explore_exploit='none',
                   as_string=False):
        if self.preprocess:
            state = self._preprocess(state)
        exp_tradeoff = np.random.uniform(0, 1)
        if explore_exploit == 'explore':
            action = random.choice(self.actions)
        elif exp_tradeoff > self.epsilon or explore_exploit == 'exploit':
            action = self._act(state)
        # Else doing a random choice --> exploration
        else:
            action = random.choice(self.actions)
            # Reduce epsilon (because we need less and less exploration)
            self.epsilon *= np.exp(-self.decay_rate)
        return action

    def remember(self, state, action, reward, new_state=None, done=None):
        # The action have to be converted back into the index given by the NN
        act_idx = np.where(np.all(self.actions == action, axis=1))[0]
        self.memory.append((state, act_idx, reward))

    def learn(self, state, action, reward, new_state=None):
        if self.preprocess:
            state = self._preprocess(state)
        self.remember(state, action, reward, new_state)
        self.episode_counter += 1
        self.r_sum += reward
        if self.verbose > 0:
            print(self.episode_counter)
        if self.episode_counter >= self.update_dnn_interval:
            self.avg_r_sum.append(self.r_sum/self.episode_counter)
            self.episode_counter = 0
            self.r_sum = 0
            self.replay_experience()
            checkpoint_name = self.filename + "_chkpt" + str(self.training_iterations) + ".h5"
            self.save(checkpoint_name)
            self.training_iterations += 1

    def _preprocess(self, state):
        '''Offset all states with the first value for faster learning'''
        offset = state[0]
        for i in range(len(state)):
            state[i] -= offset
            if state[i] < 0:
                state[i] += 5
        return state

    def replay_experience(self, batch_size=64, epochs=30):
        if self.verbose > 0:
            print('Doing replay')
        # Extract data from the experience buffer
        player_mem = np.asarray(self.memory)
        states = np.vstack(player_mem[:, 0])
        actions = np.vstack(player_mem[:, 1])
        rewards = player_mem[:, 2]

        # Use current model to predict state action values
        target = self.dnn_model.predict(states)

        # Update the target values with the known rewards. Not that
        # this games is essentionatlly series of one-shots
        for i, act_idx in enumerate(actions):
            target[i, act_idx] = rewards[i]

        # TODO: Use Early stopping or not?
        es = EarlyStopping(monitor='val_loss', mode='min',
                           verbose=0, patience=4)
        self.dnn_model.set_weights(self.org_weights)
        history = self.dnn_model.fit(states,
                                     target,
                                     epochs=epochs,
                                     verbose=0,
                                     batch_size=batch_size,
                                     callbacks=[es],
                                     validation_split=0.10
                                     )
        return history

    def get_entry(self):
        return self.state_size
    
    def get_action_size(self):
        return len(self.actions)
    
    def input_model(self, model):
        if model.optimizer==None:
            print("Compiling model, default loss and optimizer")
            model.compile(loss=self.loss,
                          optimizer='adam')
        self.dnn_model=model
