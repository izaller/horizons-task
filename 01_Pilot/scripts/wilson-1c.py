# Figure 1c from Wilson:
# Learning curves showing the fraction of times the correct option (i.e., the option with the higher generative mean)
# was chosen as a function of free-choice trial number for the different horizon conditions.
# This demonstrates that participants performed at above-chance levels and improved as the game progressed

import numpy as np
import scipy as sp
import pandas as pd
import scipy.io as io
import os
import seaborn as sns
import matplotlib.pyplot as plt

# load full data
df = pd.read_csv('../data/data.csv')

subjects = df['Subject'].unique()
n = len(subjects)
blocks = df['Block'].unique()  # 1 block = 1 game

corr_choices6 = [0, 0, 0, 0, 0, 0]
corr_choices1 = 0
ten = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

for s in range(0, n):  # iterate through each subject
    # get free choices from subject s game g
    for g in range(0, 80):  # iterate through all games for the subject
        horizon = df.loc[(df['Subject'] == subjects[s]) & (df['Block'] == blocks[g]), 'Horizon'].values
        isten = np.array_equal(horizon, ten)

        choices_g = df.loc[(df['Subject'] == subjects[s]) & (df['Block'] == blocks[g]) & (df['Trial'] > 4), 'Choice'].values

        if isten:
            corr_choices6 = np.add(corr_choices6, choices_g)
        else:
            corr_choices1 += choices_g

print("H-6", corr_choices6)
print("H-1", corr_choices1)

# newList = [x / myInt for x in myList]
avg6 = [x / ]

plt.plot([1, 2, 3, 4, 5, 6], corr_choices6)
plt.show()
