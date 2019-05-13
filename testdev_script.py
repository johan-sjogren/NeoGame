# %%
import numpy as np
from game_engine import Game
# from tqdm import tqdm
from QAgent import QTableAgent, GreedyAgent

# %%
game = Game()
player = GreedyAgent()
opponent = QTableAgent()

game.get_actions(as_string=False)

# %%
game.get_player_state()
game.dealCards().get_player_state()

# %%
player_action = player.get_action(game.get_player_state(as_string=False),
                                  game.get_actions(as_string=False),
                                  value_func=Game.calc_score)
print(player_action)
# opponent_action = opponent.get_action(game.get_opponent_state(),
#                                       game.get_actions())
# print(opponent_action)

""" 
play_env, opp_env = game.getEnv()

print("Player Action " + player_action[0])
acts = list(int(x) for x in player_action[0])
# print( acts)
print('Player Env', play_env[0], play_env[1])
# print(play_env[1][1] )
print('Player line', play_env[0][acts], '  ', play_env[1])

acts = list(int(x) for x in player_action[0])
# print( acts)
print('Oppone line', opp_env[0][acts], '  ', opp_env[1])
# print(opp_env[1][1] )
print('Oppone Env',  opp_env[0], opp_env[1])


print("Oppon Action " + opponent_action[0])
player_score, opponent_score = (game.set_player_action([int(x) for x in
                                                        player_action[0]])
                                    .set_opponent_action([int(x) for x in
                                                         opponent_action[0]])
                                    .get_scores())

print(player_score, opponent_score)
# %%
print([y, x for x, x in game.getEnv())])
print('Environment', np.concatenate(game.getEnv()))
 """