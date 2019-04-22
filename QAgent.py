import numpy as np


class QAgent(object):

    def __init__(self):
        self.Q = {}
        self.n_cards_to_pick = 3
        self.epsilon = 1
        self.learning_rate = 0.7          # Learning rate
        # gamma = 0.95                 # Discounting rate
        # Exploration parameters
        self.decay_rate = 0.005

    def unexplored(self):
        return 0

    def get_Q(self, state, action):
        if state in self.Q and action in self.Q[state]:
            return self.Q[state][action]
        else:
            return self.unexplored()

    def set_Q(self, state, action, value):
        if state in self.Q:
            self.Q[state][action] = value
        else:
            self.Q[state] = {action: value}

    def get_action(self, state, actions):
        exp_exp_tradeoff = np.random.uniform(0, 1)

        # If this number > greater than epsilon --> exploitation
        if exp_exp_tradeoff > self.epsilon:
            _, action = max(map(lambda m: (self.get_Q(state, m), m), actions),
                            key=lambda x: x[0])

        # Else doing a random choice --> exploration
        else:
            # print(actions)
            action = np.random.choice(actions,  1)

        # Reduce epsilon (because we need less and less exploration)
        self.epsilon *= np.exp(-self.decay_rate)
        return action

    def update_Q(self, state, action, reward):
        # TODO:
        new_value = self.get_Q(state, action) * (1 - self.learning_rate) + \
            self.learning_rate * reward
        self.set_Q(state, action, new_value)
