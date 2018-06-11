import numpy as np
import numpy.random as rnd

from collections import defaultdict


teams = [
    ("Brazil", 5.03),
    ("Germany", 5.52),
    ("Spain", 6.81),
    ("France", 7.46),
    ("Argentina", 10.01),
    ("Belgium", 12.05),
    ("England", 18.19),
    ("Portugal", 25.03),
    ("Uruguay", 29.70),
    ("Croatia", 33.03),
    ("Colombia", 42.71),
    ("Russia", 47.72),
    ("Poland", 66.73),
    ("Denmark", 99.43),
    ("Mexico", 109.46),
    ("Switzerland", 109.46),
    ("Sweden", 167.88),
    ("Peru", 184.54),
    ("Egypt", 184.54),
    ("Serbia", 201.21),
    ("Senegal", 201.26),
    ("Nigeria", 217.93),
    ("Iceland", 217.93),
    ("Japan", 334.75),
    ("Australia", 334.75),
    ("Costa Rica", 434.75),
    ("Morocco", 434.75),
    ("Iran", 468.08),
    ("South Korea", 551.42),
    ("Tunisia", 718.34),
    ("Saudi Arabia", 718.34),
    ("Panama", 885.01),
]

team_ix = np.arange(32).reshape((-1,4))

# how good each team is
team_quote = [
    #Team1  Team 2  Team 3  Team 4
     47.72, 718.34, 184.54,  29.70, # Group A
     25.03,   6.81, 434.75, 468.08, # Group B
      7.46, 334.75, 184.54,  99.43, # Group C
     10.01, 217.93,  33.03, 217.93, # Group D
      5.03, 109.46, 434.75, 201.21, # Group E
      5.52, 109.46, 167.88, 551.42, # Group F
     12.05, 885.01, 718.34,  18.19, # Group G
     66.73, 201.26,  42.71, 334.75, # Group H
]
team_quote = np.array(team_quote).reshape((-1,4))
team_grade = [
    17,  0, 10, 21,
    26, 29,  2,  3,
    30, 14, 11, 22,
    27, 19, 25, 12,
    31, 16,  8,  7,
    32, 20, 15,  4,
    24,  6,  5, 28,
    23,  9, 18, 13,
]
team_grade = np.array(team_grade).reshape((-1,4))

print("Team grades:")
print(team_grade)

wins   = np.zeros(team_quote.shape)
points = np.zeros(team_quote.shape)

for i in range(0,4):
    for j in range(i+1,4):
        # i vs j in each group
        #random = rnd.random(team_quote.shape[0]) * (team_quote[:,i] + team_quote[:,j])
        #i_winner  = (random < team_quote[:,j])
        i_winner = team_quote[:,j] / (team_quote[:,i] + team_quote[:,j])
        i_loser = 1 - i_winner # 0:i 1:j

        wins  [:,i] += i_winner
        wins  [:,j] += i_loser
        points[:,i] += i_winner*team_grade[:,j]
        points[:,j] += i_loser *team_grade[:,i]

print("Estimated points")
print(points)

max_cost = 60
team_cost  = 32 - np.argsort(np.argsort(team_quote.reshape(-1))) # use standard cost
team_value = points.reshape(-1)

best_value = []
best_teams = []

# I ... am sorry ...
for t0 in range(32):
    for t1 in range(t0,32):
        if t1 == t0: continue
        for t2 in range(t1,32):
            if t2 == t0 or t2 == t1: continue
            for t3 in range(t2,32):
                if t3 == t0 or t3 == t1 or t3 == t2: continue
                value = np.sum(team_value[[t0,t1,t2,t3]])
                cost  = np.sum(team_cost [[t0,t1,t2,t3]])

                if cost > max_cost: continue
                best_value.append(value)
                best_teams.append([t0,t1,t2,t3])

best_value = np.array(best_value)
best_teams = np.array(best_teams)
sort = np.argsort(best_value)[-20:]
best_value = best_value[sort]
best_teams = best_teams[sort]


for val,bet in zip(best_value,best_teams):
    print("{:.2f}@{:2d} with teams ix_in_group:{}, grade:{}, place:{} points:{}".format(val, np.sum(team_cost[bet]), bet, team_cost[bet], 32-team_cost[bet], points.reshape(-1)[bet]))
    print("{:.2f}".format(val), *[teams[-i][0] for i in team_cost[bet]])

