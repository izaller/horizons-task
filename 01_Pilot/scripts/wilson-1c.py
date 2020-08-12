# Figure 1c from Wilson:
# Learning curves showing the fraction of times the correct option (i.e., the option with the higher generative mean)
# was chosen as a function of free-choice trial number for the different horizon conditions.
# This demonstrates that participants performed at above-chance levels and improved as the game progressed

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load full data
df = pd.read_csv('../data/data.csv')

subjects = df['Subject'].unique()
n = len(subjects)  # number of subjects
blocks = df['Block'].unique()  # 1 block = 1 game

ten = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

h6games = []
h1games = []

for s in range(n):  # iterate through each subject
    # get free choices from subject s game g
    for g in range(80):  # iterate through all games for the subject
        horizon = df.loc[(df['Subject'] == subjects[s]) & (df['Block'] == blocks[g]), 'Horizon'].values
        is_ten = np.array_equal(horizon, ten)  # boolean; true for games with 10 rounds

        choices_g = df.loc[(df['Subject'] == subjects[s]) & (df['Block'] == blocks[g]) & (df['Trial'] > 4), 'Accuracy'].values

        if is_ten:
            h6games.append(choices_g)
        else:
            h1games.append(choices_g)

sum6 = sum(h6games)
sum1 = sum(h1games)
print("H-6", sum6)
print("H-1", sum1)
print("length H-6", len(h6games))  # 760 games, we're counting 6 rounds from each game
print("length H-1", len(h1games))

avg6 = [x / (40 * n) for x in sum6]
avg1 = [x / (40 * n) for x in sum1]

correct = df.loc[(df['Horizon'] == 10) & (df['Trial'] > 4), "Accuracy"].sum()
print("Total number correct (H-6) = ", correct)

fig = plt.figure(figsize=(8, 4))
plt.plot([1], avg1, 'o-', label="Horizon 1")
plt.plot([1, 2, 3, 4, 5, 6], avg6, 'o-', label="Horizon 6")

plt.ylim(0.7, 0.9)
plt.yticks(np.arange(0.65, 0.9, 0.05))
plt.title("choice accuracy as a function of free-choice trial number")
plt.xlabel("Free-choice trial number")
plt.ylabel("fraction correct")

plt.legend()
plt.show()
