import pandas as pd
import pulp



def optimize_lineup(df, stack=None, bringback=None, verbose=False):
    """Optimizes lineup

    Args:
        df (pd.DataFrame)
        stack (int): number of players to stack with QB, default None
        bringback (int): number of opp players to stack with QB, default None
        verbose (bool): include debugging output

    Returns:
        pd.DataFrame

    """
    prob = pulp.LpProblem('FPOpt', pulp.LpMaximize)
    player_vars = pulp.LpVariable.dicts('Player', df.full_name, cat='Binary')

    prob += pulp.lpSum([pts * pvar for pvar, pts in zip(player_vars.values(), df.fppg)])

    # players constraint
    prob += pulp.lpSum(player_vars.values()) == 9

    # salary constraint
    prob += pulp.lpSum([sal * pvar for pvar, sal in zip(player_vars.values(), df.salary)]) <= 50000

    # positional constraint
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
   
    if stack in (0,):
        for row in df.loc[df.pos == 'QB', :].itertuples(index=False):
            prob += pulp.lpSum([v for k,v in player_vars.items() if
                df.loc[df.full_name == k, 'team'].values[0] == row.team and
                        df.loc[df.full_name == k, 'pos'].values[0] in ('WR', 'TE')] +
                        [8 * player_vars[row.full_name]]) <= 8

    elif stack in (1, 2, 3, 4, 5, 6):
        for row in df.loc[df.pos == 'QB', :].itertuples(index=False):
            prob += pulp.lpSum([v for k,v in player_vars.items() if
                df.loc[df.full_name == k, 'team'].values[0] == row.team and
                        df.loc[df.full_name == k, 'pos'].values[0] in ('WR', 'TE')] +
                        [-stack * player_vars[row.full_name]]) >= 0  

    if bringback in (1, 2, 3, 4, 5, 6):
        for row in df.loc[df.pos == 'QB', :].itertuples(index=False):
            prob += pulp.lpSum([v for k,v in player_vars.items() if
                                df.loc[df.full_name == k, 'team'].values[0] == row.opp and
                                df.loc[df.full_name == k, 'pos'].values[0] == 'WR'] +
                                [-bringback * player_vars[row.full_name]]) >= 0  

    prob.solve()
    chosen = [v.name.replace('Player_', '') for v in prob.variables() 
              if v.varValue == 1]
    
    if verbose:
        fn = f'stack{"none" if stack is None else stack}_bb{"none" if bringback is None else bringback}.txt'
        with open(f'data/{fn}', 'w') as f:
            print (f'Stack: {stack}, Bringback: {bringback}', file=f)
            for v in prob.variables():
                print((v.name, v.varValue), file=f)
    
    return df.loc[df.full_name.isin(chosen), :]


if __name__ == '__main__':
    pass