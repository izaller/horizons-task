# plot parameters by subject
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load desired data
df = pd.read_csv('../figures,params/params_by_horizon.csv')
anxiety = pd.read_csv('../data/surveys.csv').copy()
reject = pd.read_csv('../data/reject.csv')

# function for taking inverse log
def inv_logit(arr):
    return 1. / (1 + np.exp(-arr))


def choice_probability(params, deltas, info):
    alpha, side, sigma = params
    thetas = []

    for i in range():

        # Compute difference in expected value.
        dEV = (deltas[i] + alpha * info[i] + side) / sigma

        # compute choice probability.
        thetas[i] = inv_logit(dEV)

    # return probability array
    return thetas

def plot_hist():
    alpha_h1 = df.query('Horizon == 1')['alpha']
    alpha_h6 = df.query('Horizon == 6')['alpha']

    # plot histogram of all alphas
    fig, (h1, h6) = plt.subplots(1, 2, figsize=(16, 4))
    h1.set(title='alpha param H1', xlabel='alpha values')
    h6.set(title='alpha param H6', xlabel='alpha values')

    h1.hist(alpha_h1, bins=20)
    h6.hist(alpha_h6, bins=20)


# plot curve of average params
def plot_curves():
    alpha_h1 = df.query('Horizon == 1')['alpha'].mean()
    side_h1 = df.query('Horizon == 1')['side'].mean()
    sigma_h1 = df.query('Horizon == 1')['sigma'].mean()
    mean_params_h1 = alpha_h1, side_h1, sigma_h1

    alpha_h6 = df.query('Horizon == 6')['alpha'].mean()
    side_h6 = df.query('Horizon == 6')['side'].mean()
    sigma_h6 = df.query('Horizon == 6')['sigma'].mean()
    mean_params_h6 = alpha_h6, side_h6, sigma_h6

    deltas = np.arange(-30, 30, 1)
    thetas = choice_probability(params, deltas)

    # plot histogram of all alphas
    fig, (h1, h6) = plt.subplots(1, 2, figsize=(16, 4))
    h1.plot(deltas, choice_probability(mean_params_h1, deltas))


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


def plot_params_pswq():
    subjects = anxiety['Subject']
    rejects = reject.query('Reject == 1')['Subject'].tolist()
    data = {}
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
        print(s)
        pswq_sums.append(sum(row))
        # get function parameters from subject
        query_1 = df.query('Subject == @sub and Horizon == 1')
        alphas_h1.append(query_1['alpha'].tolist()[0])
        sides_h1.append(query_1['side'].tolist()[0])
        sigmas_h1.append(query_1['sigma'].tolist()[0])
        print(alphas_h1)
        # params_h1 = [query_1['alpha'].tolist()[0], query_1['side'].tolist()[0], query_1['sigma'].tolist()[0]]
        query_6 = df.query('Subject == @sub and Horizon == 6')
        # params_h6 = [query_6['alpha'].tolist()[0], query_6['side'].tolist()[0], query_6['sigma'].tolist()[0]]
        alphas_h6.append(query_6['alpha'].tolist()[0])
        sides_h6.append(query_6['side'].tolist()[0])
        sigmas_h6.append(query_6['sigma'].tolist()[0])

        # # add sum and params to dict
        # data[subjects[s]] = [pswq_sum, params_h1, params_h6]

    fig = plt.figure(figsize=(8, 4))
    plt.plot(alphas_h1, pswq_sums, 'o', label='Horizon 1')
    plt.plot(alphas_h6, pswq_sums, 'o', label='Horizon 6')
    # fig.plt(, label='Horizon 6')
    plt.show()

plot_params_pswq()
