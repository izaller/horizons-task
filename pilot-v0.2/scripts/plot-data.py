# plot parameters by subject
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load desired data
anxiety = pd.read_csv('../data/surveys.csv').copy()
reject = pd.read_csv('../data/reject.csv')


# function for taking inverse log
def inv_logit(arr):
    return 1. / (1 + np.exp(-arr))


def plot_hist(filename):
    df = pd.read_csv(filename)
    alpha_h1 = df.query('Horizon == 1')['alpha']
    alpha_h6 = df.query('Horizon == 6')['alpha']

    # plot histogram of all alphas
    fig, (h1, h6) = plt.subplots(1, 2, figsize=(16, 4))
    h1.set(title='alpha param H1', xlabel='alpha values')
    h6.set(title='alpha param H6', xlabel='alpha values')

    h1.hist(alpha_h1, bins=20)
    h6.hist(alpha_h6, bins=20)


# adjust scores for Penn State Worry Questionnaire
# reverse score for PSWQ 1, 3, 8, 10, 11
# 5 --> 1, 4 --> 2, 3 --> 3, 2 --> 4, 1 --> 5
# TODO make this a lot faster
def adjust_pswq(row):
    for i in range(len(row)):
        if i in [0, 2, 7, 9, 10]:
            if row[i] == 5:
                row[i] = 1
            elif row[i] == 4:
                row[i] = 2
            elif row[i] == 2:
                row[i] = 4
            elif row[i] == 1:
                row[i] = 5
    return row


def plot_alpha_pswq(filename, title, figname):
    df = pd.read_csv(filename)
    subjects = anxiety['Subject']
    rejects = reject.query('Reject == 1')['Subject'].tolist()
    pswq_sums = []

    alphas_h1 = []
    alphas_h6 = []

    sides_h1 = []
    sides_h6 = []

    sigmas_h1 = []
    sigmas_h6 = []

    # grab a subject
    for s in range(len(subjects)):
        sub = subjects[s]
        if sub in rejects:
            continue

        row = anxiety.iloc[s, 6:23]
        row = adjust_pswq(row)
        # sum anxiety scores for the subject
        pswq_sums.append(sum(row))
        # get function parameters from subject
        query_1 = df.query('Subject == @sub and Horizon == 1')
        alphas_h1.append(query_1['alpha'].tolist()[0])
        sides_h1.append(query_1['side'].tolist()[0])
        sigmas_h1.append(query_1['sigma'].tolist()[0])
        query_6 = df.query('Subject == @sub and Horizon == 6')
        alphas_h6.append(query_6['alpha'].tolist()[0])
        sides_h6.append(query_6['side'].tolist()[0])
        sigmas_h6.append(query_6['sigma'].tolist()[0])


    fig = plt.figure(figsize=(8, 4))
    plt.plot(pswq_sums, alphas_h1, 'o', color='blue', label='Horizon 1')
    z1 = np.polyfit(pswq_sums, alphas_h1, 1)
    p1 = np.poly1d(z1)
    plt.plot(pswq_sums, p1(pswq_sums), "-", color='blue')
    plt.plot(pswq_sums, alphas_h6, 'o', color='orange', label='Horizon 6')
    z2 = np.polyfit(pswq_sums, alphas_h6, 1)
    p2 = np.poly1d(z2)
    plt.plot(pswq_sums, p2(pswq_sums), "-", color='orange')

    plt.title(title)
    plt.xlabel('Sum PSWQ')
    plt.ylabel('alpha (information parameter)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('../figures,params/' + figname)


plot_alpha_pswq('../figures,params/params_by_horizon_zscored.csv',
                'Plot of anxiety scores vs alpha (information) parameters (z scored, bounded on +-10)',
                'params_by_horizon_zscored.png')
plot_alpha_pswq('../figures,params/params_by_horizon.csv',
                'Plot of anxiety scores vs alpha (information) parameters (bounded on +-20)',
                'params_by_horizon.png')

