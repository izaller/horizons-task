# Figure 2a/b from Wilson:
#  plot left/right bandit choice as a function of the average difference between bandits, split by horizon 1 and 6 and
#  [2,2] and [3,1] games.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 12)

# load full data
df = pd.read_csv('../../data/data.csv')

filt = df.loc[df['Trial'] == 5].filter(items=['Horizon', 'delta', 'Info', 'Choice'])

# split into equal [2,2] and unequal [3,1][1,3] info games
eq = filt.loc[filt['Info'] == 0].filter(items=['delta', 'Horizon', 'Choice'])
uneq = filt.loc[filt['Info'] != 0].copy()

# add col to uneq to describe if subject made the more informative choice that round: 1 = made info choice, 0 = did not
uneq['made_info_choice'] = np.where(((uneq.Choice == 1)&(uneq.Info == 1)) | ((uneq.Choice == 0)&(uneq.Info == -1)),1,0)
# adjust so that (delta = more informative - less informative) rather than (delta = left - right)
uneq['adjusted_delta'] = np.where((uneq.Info == -1), -uneq.delta, uneq.delta)

h1_eq = eq.loc[eq['Horizon'] == 5].filter(items=['delta', 'Choice']).groupby('delta').mean('Choice')
h6_eq = eq.loc[eq['Horizon'] == 10].filter(items=['delta', 'Choice']).groupby('delta').mean('Choice')

h1_uneq = uneq.loc[uneq['Horizon'] == 5].filter(items=['adjusted_delta', 'made_info_choice']).groupby('adjusted_delta')\
    .mean('made_info_choice')
h6_uneq = uneq.loc[uneq['Horizon'] == 10].filter(items=['adjusted_delta', 'made_info_choice'])\
    .groupby('adjusted_delta').mean('made_info_choice')

# plot the data
fig, (unequal, equal) = plt.subplots(1, 2, figsize=(10, 4))

unequal.set(title="unequal information [3, 1]",
            xlabel="difference in means between\nmore and less informative options",
            ylabel="probability of choosing\nmore informative option", ylim=(0, 1), yticks=np.arange(0, 1, 0.1))
unequal.plot(h1_uneq, 'o-', label='Horizon 1')
unequal.plot(h6_uneq, 'o-', label='Horizon 6')
unequal.legend(loc='upper left')

equal.set(title="equal information [2, 2]", xlabel="difference in means between\nleft and right options",
          ylabel="probability of choosing\nleft option", ylim=(0, 1), yticks=np.arange(0, 1, 0.1))
equal.plot(h1_eq, 'o-', label='Horizon 1')
equal.plot(h6_eq, 'o-', label='Horizon 6')
equal.legend()

plt.tight_layout()
plt.show()
