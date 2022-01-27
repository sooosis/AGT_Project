# -*- coding: utf-8 -*-
"""Uniform.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wUSdPRoUHkwkUFgoITGE2dlUunnCwaV7
"""

import random, math
import matplotlib.pyplot as plt
import numpy as np

def create_game_matrix(n,m,t):
  
  l = []
  g = []
  for i in range(0,m):
    l.append(random.uniform(0,1))
  for i in range(0,n):
    if t == 1:
      g.append(random.sample(l, k=len(l)))
    elif t == 2:
      temp=[]
      for i in range(0,m):
        temp.append(random.uniform(0,1))
      g.append(temp)
    else:
      g.append(l)
    

  
  return np.array(g)

def sampling(dist,m,agent):

  s = 0
  sample_dist = []

  mini = min(dist)
  for i in range(0,m):
    dist[i] = dist[i] - mini
    s += np.exp(dist[i])
  
  for i in range(0,m):
    sample_dist.append(np.exp(dist[i])/s)
  
  '''if(agent == 0):
    print(sample_dist)'''

  return(np.random.choice( np.arange(0, m), p=sample_dist))

#linear fairness
T = 2000
eta = np.sqrt(1/T)
n = 5
m = 5
beta = np.sqrt(1/T)/2
alpha = 0


dist=[]
ne_dist=[]

ne_rw = [0]*n
rw = [0]*n

for i in range(0,n):
  dist.append([0] * m)
  ne_dist.append([0] * m)


game = create_game_matrix(n,m,1)
print(game)

for t in range(T):
  actions = []
  ne_actions = []

  rewards = [0]*n
  ne_rewards = [0]*n

  for i in range(0,n):
    actions.append(sampling(dist[i],m,130))
    ne_actions.append(sampling(ne_dist[i],m,i))
  
  for i in range(0,n):

    if actions.count(actions[i]) > 1:
      rewards[i] = alpha
      #rw[i] += alpha
    else:
      rewards[i] = game[i][actions[i]]
      rw[i] += game[i][actions[i]]

    if ne_actions.count(ne_actions[i]) > 1:
      ne_rewards[i] = alpha
      #ne_rw[i] += alpha
    else:
      ne_rewards[i] = game[i][ne_actions[i]]
      ne_rw[i] += game[i][ne_actions[i]]
  
  
  mi = min(rw)

  for i in range(0,n):
    for j in range(0,m):
      if(j == actions[i]):
        dist[i][j] += eta*(1 - ( 1-(rewards[i]- beta*(rw[i]-mi)*(rw[i]-mi))/ (np.exp(dist[i][j])/np.sum(np.exp(dist[i]))) )     )
      else:
        dist[i][j] += eta
  



print('Linear Fairness = ',max(rw)-min(rw), max(ne_rw)-min(ne_rw))
print('Social welfare = ',sum(rw),sum(ne_rw))
print('Nash Social Welfare = ',np.power(np.prod(rw),1/n),np.power(np.prod(ne_rw),1/n))


for i in range(0,m):
  ne = []
  y = []
  x = []
  for j in range(0,n):
    x.append(j)
    y.append(np.exp(dist[j][i]) / np.sum(np.exp(dist[j])))
    ne.append(np.exp(ne_dist[j][i]) / np.sum(np.exp(ne_dist[j])))
  ax = plt.subplot(1,2,1)
  ax.set_ylim([0, 1])
  ax.bar(x, y, width=0.1, color='b',)
  ax = plt.subplot(1,2,2)
  ax.set_ylim([0, 1])
  ax.bar(x, ne, width=0.1, color='g')
  
  
  plt.figure()