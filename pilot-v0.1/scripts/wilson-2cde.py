# plot fraction of choices of the higher value bandit on turn 5, split by horizon 1 and 6 and [2,2] and [3,1] games.
# For [3,1] trials, plot the fraction of bandit-1 (lower info) choices by horizon
# For [2,2] trials, plot the fraction of "suboptimal" choices (i.e. lower mean bandits) by horizon

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 12)

# load full data
df = pd.read_csv('../data/data.csv')

filt = df.loc[df['Trial'] == 5].filter(items=['Horizon', 'Info', 'Accuracy'])

# split into equal [2,2] and unequal [3,1][1,3] info games
eq = filt.loc[filt['Info'] == 0]
uneq = filt.loc[filt['Info'] != 0]

# break eq,uneq down by horizon and get the fraction of times the higher value bandit was chosen
eq_h1 = 1 - eq.loc[eq['Horizon'] == 5].filter(['Accuracy']).mean().values[0]  # fraction of times low val bandit was chosen
eq_h6 = 1 - eq.loc[eq['Horizon'] == 10].filter(['Accuracy']).mean().values[0]

uneq_h1 = 1 - uneq.loc[uneq['Horizon'] == 5].filter(['Accuracy']).mean().values[0]  # fraction of times low info bandit was chosen
uneq_h6 = 1 - uneq.loc[uneq['Horizon'] == 10].filter(['Accuracy']).mean().values[0]


# x-axis: horizon length (1 vs. 6)
# y-axis: fraction of times the lower information/value bandit was chosen
fig, (unequal, equal) = plt.subplots(1, 2, figsize=(8, 4))

equal.set(title="Fraction of lower-value choices\nmade in round 5 by horizon", xlabel="Horizon length",
          ylabel="Fraction of lower-value choices\nmade in round 5", ylim=(0, 0.4))
equal.bar([1, 2], [eq_h1, eq_h6], tick_label=["1", "6"], color=('tab:blue', 'tab:orange'), edgecolor='k')

unequal.set(title="Fraction of lower-information choices\nmade in round 5 by horizon", xlabel="Horizon length",
            ylabel="Fraction of lower-information choices\nmade in round 5", ylim=(0, 0.4))
unequal.bar([1, 2], [uneq_h1, uneq_h6], tick_label=["1", "6"], color=('tab:blue', 'tab:orange'), edgecolor='k')

plt.tight_layout()
plt.show()
