from boat_env import BoatEnvironment, Boat
import pygame as pg
import numpy as np
from vicero.policy import RandomPolicy, KeyboardPolicy
from vicero.algorithms.deepqlearning import DQN
from vicero.algorithms.common.neuralnetwork import NetworkSpecification

import torch
import torch.nn as nn

import matplotlib.pyplot as plt

dim = (400, 400)

pg.init()
screen = pg.display.set_mode(dim)
clock = pg.time.Clock()

env = BoatEnvironment(dim, screen)

framerate = 1000

running = True

spec = NetworkSpecification(hidden_layer_sizes=[12, 8], activation_function=nn.Sigmoid)
dqn = DQN(env, spec, render=False, alpha=0.01, epsilon_start=0.8, epsilon_end=0.01, memory_length=2000)

batch_size = 16
num_episodes = 5 #00
training_iter = 400

print('training...')
dqn.train(num_episodes, batch_size, training_iter, verbose=True, plot=True, eps_decay=True)
boat1_policy = dqn.copy_target_policy(verbose=True)
boat2_policy = dqn.copy_target_policy(verbose=False)
dqn.save('baat.pkl')

boat1_state = env.reset()
boat2_state = boat1_state

plt.plot(dqn.history)
plt.show()

plt.plot(dqn.loss_history)
plt.show()

plt.plot(dqn.maxq_history)
plt.show()

plt.plot(dqn.history)
plt.plot(dqn.maxq_history)
plt.show()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            running = False

    keys = pg.key.get_pressed()    
    if keys[pg.K_SPACE]: env.reset()

    boat1_state, _, done, _ = env.boat1.step(boat1_policy(boat1_state))
    boat2_state, _,    _, _ = env.boat2.step(boat2_policy(boat2_state))
    
    env.draw(screen)
    if done: env.reset()

    pg.display.flip()
    clock.tick(framerate)