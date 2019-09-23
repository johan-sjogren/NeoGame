# %%

# %%
import numpy as np
from pyneogame.Engine import Game
from tqdm import tqdm
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.ActiveTable import ActiveTable
from pyneogame.Agent.RandomAgent import RandomAgent
from collections import defaultdict

# %%
TRAIN_EPISODES = 10 #10000
TEST_EPISODES = 10 #10000
game = Game()
# player = ActiveTable(unexplored=1).load('test.csv')
player = QTableAgent(unexplored=1)  # .load('test.csv')
# opponent = RandomAgent()

opponent = GreedyAgent()
exp_states = defaultdict(int)

for i in tqdm(range(TRAIN_EPISODES)):

    if isinstance(player, ActiveTable) and i > 10:

        if player.seen_state(game.deal_cards().get_player_state()):
            state = player.recommend_state()
            game.dealFromRecommendation(state)

    else:
        game.deal_cards().get_player_state()

    player_action = player.get_action(game.get_player_state(),
                                      game.get_actions(),
                                      explore_exploit='explore')
    state = np.array2string(game.get_player_state())
    exp_states[state] += 1

    opponent_action = opponent.get_action(game.get_opponent_state(),
                                          game.get_actions())

    player_score, opponent_score = (game.set_player_action(player_action)
                                    .set_opponent_action(opponent_action)

                                    .get_scores())
    player.learn(state=game.get_player_state(),
                 action=player_action,
                 reward=1 if player_score-opponent_score > 0 else -1)

if isinstance(player, ActiveTable):
    maximum = max(player.state_count, key=player.state_count.get)
    minimum = min(player.state_count, key=player.state_count.get)
else:
    maximum = max(exp_states, key=exp_states.get)
    minimum = min(exp_states, key=exp_states.get)
    print(maximum, exp_states[maximum])
    print(minimum, exp_states[minimum])

# print(list((x, exp_states[x]) for x in sorted(exp_states,
#                                               key=exp_states.get)[:10]))

# print(min(exp_states, key=lambda x: x[1]), max(exp_states))
# print(player.get_QTable(as_dataframe=True))
print(len(player.get_qtable(as_dataframe=True).columns))
player.save('test.csv')
# saved_loaded = (player.save('test.csv')
#                       .load('test.csv').get_QTable(as_dataframe=True)
#                 )
# print(saved_loaded)
# print(saved_loaded.columns)

player = ActiveTable().load('test.csv')
# print(player.get_QTable(as_dataframe=True))
opponent = GreedyAgent()
player_wins = []
opponent_wins = []
n_test = 20
for _ in tqdm(range(n_test)):
    game = Game()
    for i in range(TEST_EPISODES):
        game.deal_cards().get_player_state()
        player_action = player.get_action(game.get_player_state(),
                                          game.get_actions(),
                                          explore_exploit='exploit')

        opponent_action = opponent.get_action(game.get_opponent_state(),
                                              game.get_actions())

        player_score, opponent_score = (game.set_player_action(player_action)
                                        .set_opponent_action(opponent_action)
                                        .get_scores())

        player.learn(state=game.get_player_state(),
                     action=player_action,
                     reward=1 if player_score-opponent_score > 0 else -1)

    player_wins.append(sum(
        list(play > opp for opp, play in
             zip(list(game.opponent_score)[-TEST_EPISODES:],
                 list(game.player_score)[-TEST_EPISODES:])
             )))

    opponent_wins.append(
        sum(
            list(play < opp for opp, play in
                 zip(list(game.opponent_score)[-TEST_EPISODES:],
                     list(game.player_score)[-TEST_EPISODES:])
                 )))

# print(list(zip(game.opponent_score[-10:], game.player_score[-10:])))

# %%

print(player_wins)
print(opponent_wins)
print(sum(play > opp for play, opp in
          zip(player_wins, opponent_wins)
          )/len(player_wins))

if isinstance(player, ActiveTable):
    print('Recommended state')
    player.recommend_state()


#%%
