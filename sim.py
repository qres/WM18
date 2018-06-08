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
     47.72, 718.34, 184.54,  29.70,
     25.03,   6.81, 434.75, 468.08,
      7.46, 334.75, 184.54,  99.43,
     10.01, 217.93,  33.03, 217.93,
      5.03, 109.46, 434.75, 201.21,
      5.52, 109.46, 167.88, 551.42,
     12.05, 885.01, 718.34,  18.19,
     66.73, 201.26,  42.71, 334.75,
]
team_quote = np.array(team_quote).reshape((-1,4))
team_grade = 32 - np.argsort(np.argsort(team_quote.reshape(-1))).reshape((-1,4))

print("Team grades:")
print(team_grade)

wins   = np.zeros(team_quote.shape)
points = np.zeros(team_quote.shape)

num_wms = 3000
for _ in range(num_wms):
    # how many points you get if you win against this team
    
    team_grade = np.array(team_quote) * rnd.random(team_quote.shape)
    team_grade = 32 - np.argsort(np.argsort(team_grade.reshape(-1))).reshape((-1,4))

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

points = points / num_wms
print("Average points")
print(points)

max_cost = 61
team_cost  = 32 - np.argsort(np.argsort(team_quote.reshape(-1))) # use standard cost
team_value = points.reshape(-1)

best_value = 0
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
                if value > best_value:
                    best_teams = [[t0,t1,t2,t3]]
                    best_value = value
                elif value == best_value:
                    best_teams.append([t0,t1,t2,t3])
                else:
                    pass
for bet in best_teams:
    print("{:.2f}@{} with teams ix_in_group:{}, grade:{}, place:{}".format(best_value, np.sum(team_cost[bet]), bet, team_cost[bet], 32-team_cost[bet]))
    print(*[teams[-i][0] for i in team_cost[bet]])


