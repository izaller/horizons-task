import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/data.csv')


# function for taking inverse log
def inv_logit(arr):
    return 1. / (1 + np.exp(-arr))


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_likelihood_1(params, subject):
    alpha, side, sigma = params
    ll_h1 = 0

    # Do some fancy stuff to compute trial-by-trial likelihoods
    for i in range(1, 81):
        line = df.loc[(df['Subject'] == subject) & (df['Block'] == i) & (df['Trial'] == 5)]  # grab line from data

        delta = line.filter(items=['delta']).to_numpy()[0][0]
        rounds = line.filter(items=['Horizon']).to_numpy()[0][0]
        info = line.filter(items=['Info']).to_numpy()[0][0]  # need to convert from (-1, 0, 1) to (0, 1)
        if info == -1:
            info = 0  # fix right more informative case (info = -1 --> 0)

        # Compute difference in expected value.
        dEV = (delta + alpha * info + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        # # To simulate arbitrary data, pass theta (predicted choice) into the bernoulli!
        y_hat = np.random.binomial(1, theta)

        # Compute likelihood of observation.
        y = 0  # TODO: what does this mean?? (y = 0 vs 1)

        ll = np.log(theta * y_hat + (1 - theta) * (1 - y_hat))

        # sum ll by horizon
        if rounds == 5:
            ll_h1 += ll

    # Return overall (sum) likelihood
    return -ll_h1


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_likelihood_6(params, subject):
    alpha, side, sigma = params
    ll_h6 = 0

    # Do some fancy stuff to compute trial-by-trial likelihoods
    for i in range(1, 81):
        line = df.loc[(df['Subject'] == subject) & (df['Block'] == i) & (df['Trial'] == 5)]  # grab line from data

        delta = line.filter(items=['delta']).to_numpy()[0][0]
        rounds = line.filter(items=['Horizon']).to_numpy()[0][0]
        info = line.filter(items=['Info']).to_numpy()[0][0]  # need to convert from (-1, 0, 1) to (0, 1)
        if info == -1:
            info = 0  # fix right more informative case (info = -1 --> 0)

        # Compute difference in expected value.
        dEV = (delta + alpha * info + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        # # To simulate arbitrary data, pass theta (predicted choice) into the bernoulli!
        y_hat = np.random.binomial(1, theta)

        # Compute likelihood of observation.
        y = 0  # TODO: what does this mean?? (y = 0 vs 1)

        ll = np.log(theta * y_hat + (1 - theta) * (1 - y_hat))

        # sum ll by horizon
        if rounds == 10:
            ll_h6 += ll

    # Return overall (sum) likelihood
    return -ll_h6


parameters = np.array([1, 1, 1])

subjects = df['Subject'].unique()
print(minimize(model_likelihood_1, parameters, args=subjects[0]))
print(minimize(model_likelihood_6, parameters, args=subjects[0]))


# for s in subjects:
#     print(minimize(model_likelihood_1, parameters, args=s))
