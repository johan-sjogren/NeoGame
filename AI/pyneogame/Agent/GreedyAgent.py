import pandas as pd
import numpy as np
from . import BaseAgent
from pyneogame.Engine import Game

class GreedyAgent(BaseAgent.BaseAgent):

    def __init__(self, value_func=Game.calc_score):
        self.value_func = value_func

    def __str__(self):
        return "Greedy Agent"

    def get_action(self, state, actions, as_string=False):
        player_hand = np.array(state[:5])
        opponent_table = np.array(state[-2:])

        # possibles = [player_hand[a == 1] for a in actions]
        
        def diff_score(player, opponent):
            return (self.value_func(player, opponent) -
                    self.value_func(opponent, player))

        greedy_list = list(
                        map(
                            lambda a: (diff_score(
                                player_hand[a == 1], opponent_table), a),
                            actions))

        # print(sorted(greedy_list, key=lambda x: x[0])[::-1])
        _, action = max(greedy_list, key=lambda x: x[0])

        if as_string:
            return ''.join([str(x) for x in action])
        else:
            return action
        return 0

    def learn(self, state, action, reward, new_state=None):
        # Static strategy, just return self
        return self
    

def test():
    print("Running 3 tests on the greedy agent")
    game = Game()
    actions = game.get_actions()
    agent = GreedyAgent(value_func=Game.calc_score)
    
    state_1 = [1, 2, 3, 4, 4, 0, 0, 1, 3]
    action_1 = agent.get_action(state_1, actions).tolist()
    # There are three equally good solutions here...
    assert ( action_1 == [1,1,0,0,0] or 
             action_1 == [1,0,1,0,0] or
             action_1 == [0,1,1,0,0]
            )

    state_2 = [2, 3, 3, 4, 4, 0, 4, 1, 4]
    action_2 = agent.get_action(state_2, actions).tolist()
    assert action_2 == [0, 1, 1, 0, 0]

    state_3 = [0, 2, 2, 4, 4, 1, 2, 0, 3]
    action_3 = agent.get_action(state_3, actions).tolist()
    assert action_3 == [0, 1, 1, 0, 0]
    print("Greedy agent passed all tests")

def main():
    pass
    
if __name__ == "__main__":
    main()

