from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, state, actions):
        pass

    @abstractmethod
    def learn(self, state, action, reward, new_state):
        pass
