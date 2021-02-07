# lineup-optimization-cookbook
python notebooks explaining lineup optimization concepts

## optimization: Stacking is not optimal, but that's OK because projections can't really be optimized

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sansbacon/optimization-binder-environment/main?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fsansbacon%252Flineup-optimization-cookbook%26urlpath%3Dtree%252Flineup-optimization-cookbook%252Fstacking.ipynb%26branch%3Dmain)

Shows how stacking often is not optimal when projections are correct (or when looking at 'perfect' lineups), but stacking makes sense given the inaccuracies that plague even the best projections.


## pulp: Using PuLP to Optimize a Lineup
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sansbacon/optimization-binder-environment/main?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fsansbacon%252Flineup-optimization-cookbook%26urlpath%3Dtree%252Flineup-optimization-cookbook%252Fpulp_optimizer.ipynb%26branch%3Dmain)

Shows each step of creating an integer program in PuLP to optimize a lineup. Provides code for core constraints (position, salary, # players) and shows how to implement stacking and bring-back rules.


## pydfs-lineup-optimizer: Loading Players
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sansbacon/optimization-binder-environment/main?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fsansbacon%252Flineup-optimization-cookbook%26urlpath%3Dtree%252Flineup-optimization-cookbook%252Floading_players.ipynb%26branch%3Dmain)

In-depth tutorial of the different ways to create Player objects and load them into the optimizer.
