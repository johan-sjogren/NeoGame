# %%
import matplotlib.pyplot as plt
import numpy as np
from pyneogame.Engine import Game
from tqdm import tqdm
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.ActiveTable import ActiveTable
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Agent.RandomAgent import RandomAgent
from pyneogame.Agent.PolicyGradient import ReInforce

from keras.callbacks import EarlyStopping

# %%
game = Game()
player = ReInforce(state_size=len(game.get_player_state()),
                   actions=game.get_actions(),
                   update_interval=10000,
                   memory_size=30000,
                   verbose=0)
# player.load('DQN_model.h5')

opponent = GreedyAgent()
player_action = player.get_action(game.get_player_state())
print(player_action)

for _ in tqdm(range(500000)):
    game.dealCards()

    player_action = player.get_action(
        game.get_player_state(), explore_exploit='exploit')
    opponent_action = opponent.get_action(game.get_opponent_state(),
                                          game.get_actions())

    # print(type(player_action), type(opponent_action))
    # print(player_action,opponent_action)
    player_score, opponent_score = (game.set_player_action(player_action)
                                    .set_opponent_action(opponent_action)
                                    .get_scores())
    # print(player_score, opponent_score)

    player.learn(state=game.get_player_state(),
                 action=player_action,
                 reward=player_score-opponent_score
                 #1 if player_score-opponent_score>0 else 0
                 )


print(player.avg_r_sum)
player.save('DQN_model.h5')
plt.plot(player.avg_r_sum)
plt.show()

# player = DeepQAgent(state_size=len(game.get_player_state()),
#                     actions=game.get_actions(),
#                     update_interval=10000,
#                     memory_size=40000,
#                     verbose=0)
# player.load('DQN_model.h5')

TEST_EPISODES = 10
player_wins = []
opponent_wins = []
n_test = 1000
for _ in tqdm(range(n_test)):
    game = Game()
    for i in range(TEST_EPISODES):
        game.dealCards()

        player_action = player.get_action(
            game.get_player_state(), explore_exploit='exploit')
        opponent_action = opponent.get_action(game.get_opponent_state(),
                                              game.get_actions())

        # print(type(player_action), type(opponent_action))
        # print(player_action,opponent_action)
        player_score, opponent_score = (game.set_player_action(player_action)
                                        .set_opponent_action(opponent_action)
                                        .get_scores())
        # print(player_score, opponent_score)

        player.learn(state=game.get_player_state(),
                     action=player_action,
                     reward=player_score-opponent_score
                     #1 if player_score-opponent_score>0 else 0
                     )

    player_wins.append(sum(
        list(play > opp for opp, play in
             zip(game.opponent_score[-TEST_EPISODES:],
                 game.player_score[-TEST_EPISODES:])
             )))

    opponent_wins.append(
        sum(
            list(play < opp for opp, play in
                 zip(game.opponent_score[-TEST_EPISODES:],
                     game.player_score[-TEST_EPISODES:])
                 )))

# print(list(zip(game.opponent_score[-10:], game.player_score[-10:])))
# print(player_wins)
# print(opponent_wins)
print(sum(play > opp for play, opp in
          zip(player_wins, opponent_wins)
          )/len(player_wins))
print(sum(play < opp for play, opp in
          zip(player_wins, opponent_wins)
          )/len(player_wins))


player.save('DQN_model.h5')

plt.plot(np.array(player_wins) - np.array(opponent_wins))
plt.show()
# %%
# player_mem = np.asarray(player.memory)
# states = np.vstack(player_mem[:,0])
# actions = np.vstack(player_mem[:,1])
# rewards = player_mem[:,2]

# #%%
# target = player.dnn_model.predict(states)

# #%%
# new_target = target.copy()
# for i, act_idx in enumerate(actions):
#     new_target[i, act_idx]=rewards[i]

# #%%
# es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)
# history = player.dnn_model.fit(states, new_target,
#                                epochs=30, verbose=0,
#                                callbacks=[es], validation_split=0.10)

# #%%
# import matplotlib.pyplot as plt
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.show()

# %%
