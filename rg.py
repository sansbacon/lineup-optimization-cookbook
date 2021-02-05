# convert rotoguru ssv

import numpy as np
import pandas as pd

df = pd.read_csv(ssv, sep=';')

# get rid of irrelevant columns
df = df.iloc[:, 3:]
df.columns = ['full_name', 'position', 'team', 'ha', 'opp', 'fppg', 'salary']

# names are last, first with team city for DST
names = df['full_name'].str.split(', ', expand=True)
names[1] = names[1].fillna(names[0])
names[0] = np.where(names[0] == names[1], 'Defense', names[0])
df['first_name'] = names[1]
df['last_name'] = names[0]

# fix positions
df['position'] = df['position'].str.replace('Def', 'DST')

# fix teams
df['team'] = df['team'].str.upper()

# fix salaries
df = df.dropna()
df['salary'] = df['salary'].astype(int)

# add player_id
df.insert(0, 'player_id', pd.Series(range(1, len(df) + 1)))

# remove unwanted columns
df = df.loc[:, ['first_name', 'last_name', 'position', 'team', 'salary', 'fppg']]

# save to disk
df.to_csv('pool.csv', index=False)

import pandas as pd
from pathlib import Path
import pulp

df = pd.read_csv(Path.home() / 'pool.csv')

# create variables
player_vars = pulp.LpVariable.dicts('Player', df.full_name, cat='Binary')

# setup problem
prob = pulp.LpProblem('FPOpt', pulp.LpMaximize)

# objective function - sum of fantasy points
prob += pulp.lpSum([pts * pvar for pvar, pts in zip(player_vars.values(), df.fppg)])

# constraint: salary must not exceed cap
prob += pulp.lpSum([sal * pvar for pvar, sal in zip(player_vars.values(), df.salary)]) <= 50000

# constraint: lineup must have 9 players
prob += pulp.lpSum(player_vars.values()) == 9

# add positional constraints
prob += pulp.lpSum([v for v, pos in zip(player_vars.values(), df.pos) 
                    if pos == 'QB']) == 1
prob += pulp.lpSum([v for v, pos in zip(player_vars.values(), df.pos) 
                    if pos == 'RB']) >= 2
prob += pulp.lpSum([v for v, pos in zip(player_vars.values(), df.pos) 
                    if pos == 'RB']) <= 3
prob += pulp.lpSum([v for v, pos in zip(player_vars.values(), df.pos) 
                    if pos == 'WR']) >= 3
prob += pulp.lpSum([v for v, pos in zip(player_vars.values(), df.pos) 
                    if pos == 'WR']) <= 4
prob += pulp.lpSum([v for v, pos in zip(player_vars.values(), df.pos) 
                    if pos == 'TE']) >= 1
prob += pulp.lpSum([v for v, pos in zip(player_vars.values(), df.pos) 
                    if pos == 'TE']) <= 2
prob += pulp.lpSum([v for v, pos in zip(player_vars.values(), df.pos) 
                    if pos == 'DST']) == 1


# solve problem and print solution
prob.solve()
[v.name for v in prob.variables() if v.varValue == 1]

# sanity check against data
df.sort_values('fppg', ascending=False).head(25)
