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
blocks = df['Block'].unique()  # 1 block = 1 game

muL = df['mu_L']
muR = df['mu_R']


choices = [0, 0, 0, 0, 0, 0]
avg = 0

# get free choices from subject s game g

# if
#if df.loc[(df['Subject'] == subjects[0]) & (df['Block'] == blocks[0]), 'Horizon']:
choices_g = df.loc[(df['Subject'] == subjects[0]) & (df['Block'] == blocks[0]) & (df['Trial'] > 4), 'Choice'].values
choices = np.add(choices, choices_g)
# avg =
print(choices)

plt.plot([1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12])
# plt.show()
