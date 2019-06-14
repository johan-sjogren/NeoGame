import pandas as pd
import numpy as np
from . import BaseAgent
from collections import deque
import random
from keras import Model
from keras.layers import Input, Dense, Embedding, Flatten, LSTM, Bidirectional

# TODO: Create a Dueling DQN as well
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
                 update_interval = 200,
                 verbose=0):

        self.actions = actions
        self.verbose = verbose
        self.epsilon = epsilon
        self.decay_rate = decay_rate
        self.memory = deque(maxlen=3000)
        self.update_dnn_interval = update_interval
        self.episode_counter = 0
        self.state_size = state_size
        self.r_sum = 0
        self.avg_r_sum = []

        if model is None:
            print("Building default model")
            self.dnn_model = self._make_model()
        else:
            self.dnn_model = model

    def __str__(self):
        return "Deep Q Agent"

    def _make_model2(self):
        '''Start with a simple default model for now'''
        input_layer = Input(shape=(self.state_size,))
        dense_1 = Dense(10, activation='sigmoid')(input_layer)
        dense_2 = Dense(10, activation='sigmoid')(dense_1)
        output = Dense(len(self.actions), activation='sigmoid')(dense_2)
        model = Model(inputs = input_layer, outputs=output)
        model.compile(loss='mae',
                      optimizer='adam')
        if self.verbose:
            print(model.summary())
        return model

    def _make_model(self):
        '''Start with a simple default model for now'''
        input_layer = Input(shape=(self.state_size,))
        embedding = Embedding(input_dim=5, output_dim=5)(input_layer)
        x_layer = Bidirectional(LSTM(10))(embedding)
        #x_layer = Dense(100, activation='sigmoid')(x_layer)
        # flat = Flatten()(x_layer)
        dense_2 = Dense(10, activation='sigmoid')(x_layer)
        output = Dense(len(self.actions), activation='sigmoid')(dense_2)
        model = Model(inputs = input_layer, outputs=output)
        model.compile(loss='mae',
                      optimizer='adam')
        if self.verbose:
            print(model.summary())
        return model

    def _act(self, state):
        state = state.reshape(1, state.shape[0])
        act_values = self.dnn_model.predict(state)
        act_idx = np.argmax(act_values[0])
        return self.actions[act_idx]

    def get_action(self, state, actions=None,
                   explore_exploit='none',
                   as_string=False):

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

    def remember(self, state, action, reward, new_state):
        # The action have to be converted back into the index given by the NN
        act_idx= np.where(np.all(self.actions == action,axis=1))[0]
        if new_state:
            self.memory.append((state, act_idx, reward))
        else:
            self.memory.append((state, act_idx, reward))

    def learn(self, state, action, reward, new_state=None):
        self.remember(state, action, reward, new_state)
        self.episode_counter += 1
        self.r_sum += reward
        if self.verbose > 0:
            print(self.episode_counter)
        if self.episode_counter >= self.update_dnn_interval:
            self.avg_r_sum.append(self.r_sum/self.episode_counter)
            self.episode_counter = 0
            self.r_sum = 0
            # self.replay_experience()

    def replay_experience(self, batch_size=1000):
        if self.verbose > 0:
            print('Doing replay')
        # TODO: Do actual batch run rather than selecting a subset of the data and loop over it
        batches = random.sample(self.memory, batch_size if len(self.memory)>batch_size else len(self.memory))
        for state, action, reward in batches:
            if self.verbose > 0:
                print(state, action, reward)
            state = state.reshape(1, state.shape[0])
            target = self.dnn_model.predict(state)
            target[0][action] = reward
            self.dnn_model.fit(state, target, epochs=1, verbose=0)
