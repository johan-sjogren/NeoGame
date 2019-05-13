# %%
import numpy as np
from game_engine import Game
from tqdm import tqdm
from QAgent import QTableAgent

# %%
TRAIN_EPISODES = 3000000
TEST_EPISODES = 10000
game = Game()
player = QTableAgent(unexplored=4)
opponent = QTableAgent()

for i in tqdm(range(TRAIN_EPISODES+TEST_EPISODES)):
    game.dealCards().get_player_state()
    if i > TRAIN_EPISODES:
        player_action = player.get_action(game.get_player_state(),
                                          game.get_actions(),
                                          explore_exploit='exploit')
    else:
        player_action = player.get_action(game.get_player_state(),
                                          game.get_actions(),
                                          explore_exploit='explore')
    opponent_action = opponent.get_action(game.get_opponent_state(),
                                          game.get_actions())

    player_score, opponent_score = (game.set_player_action([int(x) for x in
                                                           player_action[0]])
                                    .set_opponent_action([int(x) for x in
                                                         opponent_action[0]])
                                    .get_scores())
    # print('Player action: ',player_action)
    player.learn(state=game.get_player_state(),
                 action=player_action,
                 reward=player_score-opponent_score)

    # opponent.learn(state=game.get_opponent_state(),
    #              action=opponent_action[0],
    #              reward=opponent_score)

print(player.get_QTable(as_dataframe=True))
# print(opponent.get_QTable(as_dataframe=True))
# print(list(zip(game.opponent_score, game.player_score)))
print(list(zip(game.opponent_score[-10:], game.player_score[-10:])))

# %%
player_wins = sum(
                list(play > opp for opp, play in
                     zip(game.opponent_score[-TEST_EPISODES:],
                         game.player_score[-TEST_EPISODES:])
                     ))

opponent_wins = sum(
                list(play < opp for opp, play in
                     zip(game.opponent_score[-TEST_EPISODES:],
                         game.player_score[-TEST_EPISODES:])
                     ))

print(player_wins)
print(opponent_wins)



#%%
