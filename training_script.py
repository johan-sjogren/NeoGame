
# %%
import numpy as numpy
from game_engine import Game
from tqdm import tqdm
from QAgent import QTableAgent

# %%
game = Game()
player = QTableAgent()
opponent = QTableAgent()

game.get_actions()
# %%
# %%
game.get_player_state()
game.dealCards().get_player_state()

# %%
player_action = player.get_action(
    game.get_player_state(), game.get_actions())
opponent_action = opponent.get_action(
    game.get_opponent_state(), game.get_actions())

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
player_score, opponent_score = (game.set_player_action([int(x) for x in player_action[0]])
                                    .set_opponent_action([int(x) for x in opponent_action[0]])
                                    .get_scores())

print(player_score, opponent_score)

# %%
EPISODES = 100000
game = Game()
player = QTableAgent()
opponent = QTableAgent()

for i in tqdm(range(EPISODES)):
    game.dealCards().get_player_state()
    if i > EPISODES - 1000:
        player_action = player.get_action(game.get_player_state(),
                                      game.get_actions(), pure_exploitation=True)
    else:
        player_action = player.get_action(game.get_player_state(),
                                      game.get_actions())
    opponent_action = opponent.get_action(game.get_opponent_state(),
                                      game.get_actions())

    player_score, opponent_score = (game.set_player_action([int(x) for x in player_action[0]])
                                    .set_opponent_action([int(x) for x in opponent_action[0]])
                                    .get_scores())
    player.learn(state=game.get_player_state(),
                 action=player_action[0],
                 reward=player_score-opponent_score)

    # opponent.learn(state=game.get_opponent_state(),
    #              action=opponent_action[0],
    #              reward=opponent_score)                 

print(player.get_QTable(as_dataframe=True))
# print(opponent.get_QTable(as_dataframe=True))
# print(list(zip(game.opponent_score, game.player_score)))
print(list(zip(game.opponent_score[-10:], game.player_score[-10:])))

print( sum(list( play > opp for opp, play in zip(game.opponent_score[-1000:], game.player_score[-1000:]))))
print( sum(list( play < opp for opp, play in zip(game.opponent_score[-1000:], game.player_score[-1000:]))))
