from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, state, actions, explore_exploit):
        pass

    @abstractmethod
    def learn(self, state, action, reward, new_state, done):
        pass

    @abstractmethod
    def save(self, filename):
        pass

    @abstractmethod
    def load(self, filename):
        pass
