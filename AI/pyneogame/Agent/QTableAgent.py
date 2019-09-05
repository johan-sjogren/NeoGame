import pandas as pd
import numpy as np
from . import BaseAgent


class QTableAgent(BaseAgent.BaseAgent):

    def __init__(self,
                 learning_rate=0.05,
                 lr_decay=False,
                 epsilon=0.9,
                 decay_rate=1e-5,
                 unexplored=0,
                 discount_rate=0.95):

        self.q = {}                # Q-table (Dict)
        self.learning_rate = learning_rate  # Learning rate
        self.learning_rate_decay = lr_decay
        self.lr_decay = 0.99
        self.discount_rate = discount_rate        # Discount rate

        # Exploration parameters
        self.epsilon = epsilon         # Starting exploration probability
        self.decay_rate = decay_rate
        self.unexplored = unexplored   # Default value of unexplored state
        # This can be used in on-policy learning to force exploration

    def __str__(self):
        return "qTable Agent"

    def _get_q(self, state, action):
        if state in self.q and action in self.q[state]:
            return self.q[state][action]
        else:
            return self.unexplored

    def _set_q(self, state, action, value):
        if state in self.q:
            self.q[state][action] = value
        else:
            self.q[state] = {action: value}

    def get_action(self, state, actions,
                   explore_exploit='none',
                   as_string=False):
        """ Implements an epsilon greedy algorithm for exploration/exploitation
            or accepts an override argument that dictates explore or explot
        Args:
            state (list): String representation of the current game state
            actions (list): list of available actions
            explore_exploit: Options 'explore', 'exploit' or 'none'(default)
        Returns:
           string/list: String or list representation of the chosen action
        """
        # Convert lists to string representations
        actions_str = [''.join([str(x) for x in y]) for y in actions]
        state_str = ''.join([str(x) for x in state])
        exp_tradeoff = np.random.uniform(0, 1)

        if explore_exploit == 'explore':
            action = np.random.choice(actions_str,  1)[0]
        # If this number > greater than epsilon --> exploitation
        elif exp_tradeoff > self.epsilon or explore_exploit == 'exploit':
            _, action = max(map(lambda m: (self._get_q(state_str, m), m),
                                actions_str),
                            key=lambda x: x[0])
        # Else doing a random choice --> exploration
        else:
            action = np.random.choice(actions_str,  1)[0]
            # Reduce epsilon (because we need less and less exploration)
            self.epsilon *= np.exp(-self.decay_rate)

        if as_string:
            return action
        else:
            return np.array([int(x) for x in action])

    def update_q(self, state, action, reward):
        """Updates the q-table values via the Q-learning algorithn
            q[state, action] =
                 q[state, action] +
                    learning_rate * (reward +
                                        discount_rate * MAX(q[new_state]) -
                                            q[state, action])
        Args:
            state (string):  String representation of the current game state
            action (string): String representation of the action performed
            reward (float): Direct reward of the action on the state

        Returns:
            self
        """
        # max_q = max(map(lambda a: self._get_q(new_state, a), actions))
        # Since our actions doesn't influence the next step (randomly
        # drawn cards) the new state is not of importance i.e. max_q = 0
        max_q = 0
        new_value = self._get_q(state, action) * (1 - self.learning_rate) + \
            self.learning_rate * (reward + max_q*self.discount_rate)

        self._set_q(state, action, new_value)
        return self

    def learn(self, state, action, reward, new_state=None):
        """Performs the alorithms learning stage.

        Args:
            state (list): representation of game state
            action (list): representation of chosen action
            reward (int/float): Immediate reward
            new_state (list, optional): representation of
                                               new game state.
                                               Defaults to None.

        Returns:
            self
        """
        # Convert list to string representation
        action_str = ''.join([str(x) for x in action])
        state_str = ''.join([str(x) for x in state])

        # For q-learning all that is needed is to update the table
        self.update_q(state_str, action_str, reward)

        if self.learning_rate_decay:
            self.learning_rate *= self.lr_decay

        return self

    def get_qtable(self, as_dataframe=False):
        if as_dataframe:
            return pd.DataFrame.from_dict(self.q)
        else:
            return self.q

    def save(self, filename):
        self.get_qtable(as_dataframe=True).to_csv(filename)
        return self

    def load(self, filename):
        self.q = pd.read_csv(filename,
                             dtype={0: str}
                             ).set_index('Unnamed: 0').to_dict()
        return self
