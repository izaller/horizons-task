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
def model_1_eq(params, subject):
    alpha, side, sigma = params
    ll = 0

    # Do some fancy stuff to compute trial-by-trial likelihoods
    for i in range(1, 81):
        line = df.loc[(df['Subject'] == subject) & (df['Block'] == i) & (df['Trial'] == 5)]  # grab line from data
        rounds = line.filter(items=['Horizon']).to_numpy()[0][0]
        if rounds == 10:  # only want H=1
            continue
        info = line.filter(items=['Info']).to_numpy()[0][0]  # need to convert from (-1, 0, 1) to (0, 1)
        if info != 0:  # only want equal condition
            continue
        delta = line.filter(items=['delta']).to_numpy()[0][0]

        # Compute difference in expected value.
        dEV = (delta + alpha * info + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = line.filter(items=['Choice']).to_numpy()[0][0]  # TODO: check if this is right

        # Compute likelihood of observation.
        loglik = np.log(theta * y + (1 - theta) * (1 - y))

        # sum ll by horizon
        ll += loglik

    # Return overall (sum) likelihood
    return -ll


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_6_eq(params, subject):
    alpha, side, sigma = params
    ll = 0

    # Do some fancy stuff to compute trial-by-trial likelihoods
    for i in range(1, 81):
        line = df.loc[(df['Subject'] == subject) & (df['Block'] == i) & (df['Trial'] == 5)]  # grab line from data
        rounds = line.filter(items=['Horizon']).to_numpy()[0][0]
        if rounds == 5:  # only want H=6
            continue
        info = line.filter(items=['Info']).to_numpy()[0][0]  # need to convert from (-1, 0, 1) to (0, 1)
        if info != 0:  # only want equal condition
            continue
        delta = line.filter(items=['delta']).to_numpy()[0][0]

        # Compute difference in expected value.
        dEV = (delta + alpha * info + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = line.filter(items=['Choice']).to_numpy()[0][0]  # TODO: check if this is right

        # Compute likelihood of observation.
        loglik = np.log(theta * y + (1 - theta) * (1 - y))

        # sum ll by horizon
        ll += loglik

    # Return overall (sum) likelihood
    return -ll


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_1_uneq(params, subject):
    alpha, side, sigma = params
    ll = 0

    # Do some fancy stuff to compute trial-by-trial likelihoods
    for i in range(1, 81):
        line = df.loc[(df['Subject'] == subject) & (df['Block'] == i) & (df['Trial'] == 5)]  # grab line from data
        rounds = line.filter(items=['Horizon']).to_numpy()[0][0]
        if rounds == 10:  # only want H=1
            continue
        info = line.filter(items=['Info']).to_numpy()[0][0]  # need to convert from (-1, 0, 1) to (0, 1)
        if info == 0:  # only want unequal condition
            continue
        if info == -1:
            info = 0  # fix right more informative case (info = -1 --> 0)
        delta = line.filter(items=['delta']).to_numpy()[0][0]

        # Compute difference in expected value.
        dEV = (delta + alpha * info + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = line.filter(items=['Choice']).to_numpy()[0][0]  # TODO: check if this is right

        # Compute likelihood of observation.
        loglik = np.log(theta * y + (1 - theta) * (1 - y))

        # sum ll by horizon
        ll += loglik

    # Return overall (sum) likelihood
    return -ll


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_6_uneq(params, subject):
    alpha, side, sigma = params
    ll = 0

    # Do some fancy stuff to compute trial-by-trial likelihoods
    for i in range(1, 81):
        line = df.loc[(df['Subject'] == subject) & (df['Block'] == i) & (df['Trial'] == 5)]  # grab line from data
        rounds = line.filter(items=['Horizon']).to_numpy()[0][0]
        if rounds == 5:  # only want H=6
            continue
        info = line.filter(items=['Info']).to_numpy()[0][0]  # need to convert from (-1, 0, 1) to (0, 1)
        if info != 0:  # only want equal condition
            continue
        if info == -1:
            info = 0  # fix right more informative case (info = -1 --> 0)
        delta = line.filter(items=['delta']).to_numpy()[0][0]

        # Compute difference in expected value.
        dEV = (delta + alpha * info + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = line.filter(items=['Choice']).to_numpy()[0][0]  # TODO: check if this is right

        # Compute likelihood of observation.
        loglik = np.log(theta * y + (1 - theta) * (1 - y))

        # sum ll by horizon
        ll += loglik

    # Return overall (sum) likelihood
    return -ll


parameters = np.array([1, 1, 10])
subjects = df['Subject'].unique()
print(minimize(model_1_eq, parameters, args=subjects[0]))
print(minimize(model_6_eq, parameters, args=subjects[0]))
print(minimize(model_1_uneq, parameters, args=subjects[0]))
print(minimize(model_6_uneq, parameters, args=subjects[0]))

# for s in subjects:
#     print(minimize(model_likelihood_1, parameters, args=s))
