import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class ABCAgent(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, state, actions):
        pass

    @abstractmethod
    def learn(self, state, action, reward, new_state):
        pass


class QTableAgent(ABCAgent):

    def __init__(self):

        self.Q = {}
        self.n_cards_to_pick = 2
        self.epsilon = 0.9         # Starting exploration probability
        self.learning_rate = 0.7   # Learning rate
        # self.gamma = 0.95        # Discount rate
        # Exploration parameters
        self.decay_rate = 0.00001
        self.unexplored = 0 # This can be used in on-policy learning to force exploration

    def get_Q(self, state, action):
        if state in self.Q and action in self.Q[state]:
            return self.Q[state][action]
        else:
            return self.unexplored

    def set_Q(self, state, action, value):
        if state in self.Q:
            self.Q[state][action] = value
        else:
            self.Q[state] = {action: value}

    def get_action(self, state, actions, pure_exploitation=False, as_string=True):
        """ Implements an epsilon greedy algorithm for exploration/exploitation

        Args:
            state (string): String representation of the current game state
            actions (list): list of available actions

        Returns:
           string: String representation of the chosen action
        """

        # if pure_exploitation:
        #     exp_tradeoff = self.epsilon + 1
        # else:
        exp_tradeoff = np.random.uniform(0, 1)

        # If this number > greater than epsilon --> exploitation
        if exp_tradeoff > self.epsilon or pure_exploitation:
            _, action = max(map(lambda m: (self.get_Q(state, m), m), actions),
                            key=lambda x: x[0])
           # print('Exploit')
        # Else doing a random choice --> exploration
        else:
            # print('Explore')
            action = np.random.choice(actions,  1)

        # Reduce epsilon (because we need less and less exploration)
        self.epsilon *= np.exp(-self.decay_rate)
        if as_string:
            return action
        else:
            return list(int(x) for x in action)

    def update_Q(self, state, action, reward):
        """Updates the Q-table values via the Q-learning algorithn
            Q[state, action] = Q[state, action]
                             + learning_rate * (reward
                                                + discount_rate * MAX(Q[new_state])
                                                - Q[state, action])
        Args:
            state (string):  String representation of the current game state
            action (string): String representation of the action performed
            reward (float): Direct reward of the action on the state

        Returns:
            self
        """

        new_value = self.get_Q(state, action) * (1 - self.learning_rate) + \
                    self.learning_rate * reward
        # Since our actions doesn't influence the next step (randomly drawn cards) the
        # new state is not of importance

        self.set_Q(state, action, new_value)
        return self

    def learn(self, state, action, reward, new_state=None):
        self.update_Q(state, action, reward)
        return self

    def get_QTable(self, as_dataframe=False):
        if as_dataframe:
            return pd.DataFrame.from_dict(self.Q)
        else:
            return self.Q

class DeepQAgent(ABCAgent):
    pass


class GreedyAgent(ABCAgent):
    pass
