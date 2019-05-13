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

    def __init__(self, learning_rate=0.1, epsilon=0.9,
                 decay_rate=1e-5, unexplored=0,
                 discount_rate=0.95):

        self.Q = {}                # Q-table (Dict)
        self.learning_rate = learning_rate   # Learning rate
        self.discount_rate = discount_rate        # Discount rate
        
        # Exploration parameters
        self.epsilon = epsilon         # Starting exploration probability
        self.decay_rate = decay_rate  
        self.unexplored = unexplored   # Default value of unexplored state
        # This can be used in on-policy learning to force exploration

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

    def get_action(self, state, actions,
                   explore_exploit='none',
                   as_string=True):
        """ Implements an epsilon greedy algorithm for exploration/exploitation

        Args:
            state (string): String representation of the current game state
            actions (list): list of available actions
            explore_exploit: Options 'explore', 'exploit' or 'none'(default)
        Returns:
           string/list: String or list representation of the chosen action
        """

        exp_tradeoff = np.random.uniform(0, 1)

        if explore_exploit == 'explore':
            action = np.random.choice(actions,  1)[0]            
        # If this number > greater than epsilon --> exploitation
        elif exp_tradeoff > self.epsilon or explore_exploit == 'exploit':
            _, action = max(map(lambda m: (self.get_Q(state, m), m), actions),
                            key=lambda x: x[0])
        # Else doing a random choice --> exploration
        else:
            action = np.random.choice(actions,  1)

        # Reduce epsilon (because we need less and less exploration)
        self.epsilon *= np.exp(-self.decay_rate)
        if as_string:
            return action
        else:
            return list(int(x) for x in action)

    def update_Q(self, state, action, reward):
        """Updates the Q-table values via the Q-learning algorithn
            Q[state, action] =
                 Q[state, action] + 
                    learning_rate * (reward +
                                        discount_rate * MAX(Q[new_state]) -
                                            Q[state, action])
        Args:
            state (string):  String representation of the current game state
            action (string): String representation of the action performed
            reward (float): Direct reward of the action on the state

        Returns:
            self
        """
        # max_q = max(map(lambda a: self.get_Q(new_state, a), actions))
        # Since our actions doesn't influence the next step (randomly
        # drawn cards) the new state is not of importance
        max_q = 0
        new_value = self.get_Q(state, action) * (1 - self.learning_rate) + \
            self.learning_rate * (reward + max_q*self.discount_rate)

        self.set_Q(state, action, new_value)
        return self

    def learn(self, state, action, reward, new_state=None):
        """Performs the alorithms learning stage. 
        
        Args:
            state (list/string): representation of game state
            action (list/string): representation of chosen action
            reward (list/string): Immediate reward
            new_state (list/string, optional): representation of 
                                               new game state.
                                               Defaults to None.
        
        Returns:
            self
        """
        # For Q-learning all that is needed is to update the table
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

    def get_action(self, state, actions, value_func, as_string=True):
        print('Greedy actions: ', actions)
        print('Greedy state: ', state)
        player_hand = np.array(state[:5])
        opponent_table = state[-2:]

        print(player_hand, opponent_table)
        # max_q = max(map(lambda a: self.get_Q(new_state, a), actions))

        possibles = [player_hand[a == 1] for a in actions]
        print(possibles)
        # print(list(map(lambda a: value_func(a, opponent_table), possibles)))
        # print(max(map(lambda a: (value_func(a, opponent_table), a), possibles)))
        action = actions[0]
        if as_string:
            return action
        else:
            return list(int(x) for x in action)
        return 0

    def learn(self, state, action, reward, new_state=None):
        # Static strategy, just return self
        return self
