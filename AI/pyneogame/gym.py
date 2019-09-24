
#!/usr/bin/python3
"""The Gym module used for training and evaluating agents playing NeoGame 

Usage:
    from pyneogame.Gym import Gym

    gym = Gym(<Agent>, <Agent>)
    
    gym.train()
    gym.eval_exp_states()

    gym.test()
    gym.eval()

TODO: Define and implement tests
TODO: Add ActiveTable specific code? 
"""

from collections import defaultdict

import numpy as np
from tqdm import tqdm

from .Engine import Game

class Gym:

    def __init__(self, player, opponent):
        
        self.game = None
        self.player = player
        self.opponent = opponent

        # Placeholder for bookkeeping visited states (?)
        self.exp_states = None

        # Placeholder for bookkeeping wins
        self.player_wins = None
        self.opponent_wins = None

    def _get_reward(self, player_score, opponent_score):
        """Get the reward of one round

        Only reward the player agent if player wins

        Arguments:
            player_score
            opponent_score
        
        TODO: Implement other reward functions?
        """

        return 1 if player_score-opponent_score > 0 else -1

    def train(self, num_episodes=10000):
        """Train the player agent against the opponent
        
        During training the player agent deploys an exploration strategy

        Arguments:
            num_episodes (int) - The number of episodes in the training
        """

        self.game = Game()

        self.exp_states = defaultdict(int)

        for i in tqdm(range(num_episodes)):

            self.game.deal_cards()

            possible_actions = self.game.get_actions()

            player_state = self.game.get_player_state()
            player_action = self.player.get_action(player_state,
                                                   possible_actions,
                                                   explore_exploit='explore')
            
            # Bookkeep visited states (?)
            player_state_str = np.array2string(player_state)
            self.exp_states[player_state_str] += 1

            opponent_state = self.game.get_opponent_state()
            opponent_action = self.opponent.get_action(opponent_state,
                                                       possible_actions)

            self.game.set_player_action(player_action)\
                     .set_opponent_action(opponent_action)

            player_score, opponent_score = self.game.get_scores()
            
            reward = self._get_reward(player_score, opponent_score)
            self.player.learn(player_state,
                         player_action,
                         reward)
        
        print("Training done!")

    def eval_exp_table(self):
        """Get the min/max exp_states
        
        TODO: Add a more descriptive print
        """

        maximum = max(self.exp_states, key=self.exp_states.get)
        minimum = min(self.exp_states, key=self.exp_states.get)
        print(maximum, self.exp_states[maximum])
        print(minimum, self.exp_states[minimum])

    def test(self, num_runs=20, num_episodes=1000):
        """Test the player agent against the opponent
        
        During test the player agent chooses the action producing the highest reward

        Arguments:
            runs (int)         - The number of test runs
            num_episodes (int) - The number of episodes in each test run
        """

        self.player_wins = []
        self.opponent_wins = []

        for run in range(num_runs):
            print("Run", run, "of", num_runs)

            self.game = Game()

            for i in tqdm(range(num_episodes)):
                
                self.game.deal_cards()

                possible_actions = self.game.get_actions()
                
                player_state = self.game.get_player_state()
                player_action = self.player.get_action(player_state,
                                                       possible_actions,
                                                       explore_exploit='exploit')
                
                opponent_state = self.game.get_opponent_state()
                opponent_action = self.opponent.get_action(opponent_state,
                                            possible_actions)

                self.game.set_player_action(player_action)\
                         .set_opponent_action(opponent_action)
                
                player_score, opponent_score = self.game.get_scores()
 
                reward = self._get_reward(player_score, opponent_score)
                self.player.learn(player_state,
                                  player_action,
                                  reward)

            last_player_scores = list(self.game.player_score)[-num_episodes:]
            last_opp_scores = list(self.game.opponent_score)[-num_episodes:]
            last_episode_scores = [(x, y) for x, y in zip(last_opp_scores,
                                                          last_player_scores)]

            # Create boolean arrays from the zipped list and sum (draws not used)
            did_player_win = [play > opp for opp, play in last_episode_scores]
            self.player_wins.append(sum(did_player_win))
            did_opp_win = [play < opp for opp, play in last_episode_scores]
            self.opponent_wins.append(sum(did_opp_win))

        print("Testing done!")

    def eval(self):
        """Evaluate performance of the two agents

        Performance metric: Aggregate wins
        
        TODO: Define the different metrics to evaluate
        TODO: Define when an agent is significantly better than the other
        """
        
        # Aggregate wins
        agg_wins = dict(player=0, opponent=0)

        for p, o in zip(self.player_wins, self.opponent_wins):
            if (p > o):
                agg_wins['player'] += 1
            elif (p < o):
                agg_wins['opponent'] += 1
            else:
                # Draw, not used for now
                pass
        
        diff = agg_wins['player'] - agg_wins['opponent']
        if diff > 0:
            print("Player won")
        elif diff < 0:
            print("Opponent won")
        else:
            print("Draw")

        print("\nAggregate wins:")
        print("\tPlayer   {player:6d}".format(**agg_wins))
        print("\tOpponent {opponent:6d}".format(**agg_wins))