import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import zscore
import csv


df = pd.read_csv('../../data/data.csv')
reject = pd.read_csv('../../data/reject.csv')


# function for taking inverse log
def inv_logit(arr):
    return 1. / (1 + np.exp(-arr))


# Info: 0 = [2,2] trial, 1 = [3,1] trial, -1 = [1,3] trial
def adjust_delta(deltas, info):
    for i in range(len(deltas)):
        if info[i] == -1:
            deltas[i] = -deltas[i]
    return deltas


def loglik(y, theta):
    return np.log(theta * y + (1 - theta) * (1 - y) + 1e-9)


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_1_eq(params, subject, zscored=True):
    alpha, side, sigma = params
    ll = 0

    data = df.query('Subject == @subject and Horizon == 5 and Info == 0 and Trial == 5').reset_index(drop=True)
    deltas = data['delta']
    if zscored:
        deltas = zscore(deltas)
    info = data['Info']
    choice = data['Choice']

    for i in range(20):

        # Compute difference in expected value.
        dEV = (deltas[i] + alpha * info[i] + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = choice[i]  # TODO: check if this is right

        # compute and sum ll
        ll += loglik(y, theta)

    # Return overall (sum) likelihood
    return -ll


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_6_eq(params, subject, zscored=True):
    alpha, side, sigma = params
    ll = 0

    data = df.query('Subject == @subject and Horizon == 10 and Info == 0 and Trial == 5').reset_index(drop=True)
    deltas = data['delta']
    if zscored:
        deltas = zscore(deltas)
    info = data['Info']
    choice = data['Choice']

    for i in range(20):

        # Compute difference in expected value.
        dEV = (deltas[i] + alpha * info[i] + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = choice[i]  # TODO: check if this is right

        # compute and sum ll
        ll += loglik(y, theta)

    # Return overall (sum) likelihood
    return -ll


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_1_uneq(params, subject, zscored=True):
    alpha, side, sigma = params
    ll = 0

    data = df.query('Subject == @subject and Horizon == 5 and Info != 0 and Trial == 5').reset_index(drop=True)
    deltas = data['delta']
    if zscored:
        deltas = zscore(deltas)
    info = data['Info']
    #info = [adjust_info(i) for i in info]
    choice = data['Choice']

    for i in range(20):

        # Compute difference in expected value.
        dEV = (deltas[i] + alpha * info[i] + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = choice[i]  # TODO: check if this is right

        # compute and sum ll
        ll += loglik(y, theta)

    # Return overall (sum) likelihood
    return -ll


# function for getting log likelihoods for H=1
# only care about 5th round ***2a/b***
def model_6_uneq(params, subject, zscored=True):
    alpha, side, sigma = params
    ll = 0

    data = df.query('Subject == @subject and Horizon == 10 and Info != 0 and Trial == 5').reset_index(drop=True)
    deltas = data['delta']
    if zscored:
        deltas = zscore(deltas)
    info = data['Info']
    #info = [adjust_info(i) for i in info]
    choice = data['Choice']

    for i in range(20):

        # Compute difference in expected value.
        dEV = (deltas[i] + alpha * info[i] + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = choice[i]

        # compute and sum ll
        ll += loglik(y, theta)

    # Return overall (sum) likelihood
    return -ll


def model_1(params, subject, zscored=True):
    alpha, side, sigma = params
    ll = 0

    data = df.query('Subject == @subject and Horizon == 5 and Trial == 5').reset_index(drop=True)
    deltas = data['delta'].copy()
    info = data['Info']
    deltas = adjust_delta(deltas, info)
    if zscored:
        deltas = zscore(deltas)
    choice = data['Choice']

    for i in range(40):
        # Compute difference in expected value.
        dEV = (deltas[i] + alpha * info[i] + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = choice[i]

        # compute and sum ll
        ll += loglik(y, theta)

    # Return overall (sum) likelihood
    return -ll


def model_6(params, subject, zscored=True):
    alpha, side, sigma = params
    ll = 0

    data = df.query('Subject == @subject and Horizon == 10 and Trial == 5').reset_index(drop=True)
    deltas = data['delta'].copy()  # TODO need to fix deltas for info = -1 case
    info = data['Info']
    deltas = adjust_delta(deltas, info)
    if zscored:
        deltas = zscore(deltas)
    choice = data['Choice']

    for i in range(40):
        # Compute difference in expected value.
        dEV = (deltas[i] + alpha * info[i] + side) / sigma

        # Compute choice probability.
        theta = inv_logit(dEV)

        y = choice[i]

        # compute and sum ll
        ll += loglik(y, theta)

    # Return overall (sum) likelihood
    return -ll


def run_four(zscored=True):
    # params = alpha, side, sigma
    parameters = np.array([10, 0, 5])
    subjects = df['Subject'].unique().tolist()
    n = len(subjects)
    rejects = reject.query('Reject == 1')['Subject'].tolist()

    with open('../../param-csv-output/params_by_horizon_and_info.csv', 'w', newline='') as file:  ## horizon x more and less informative
        writer = csv.writer(file)
        writer.writerow(['Subject', 'type', 'alpha', 'side', 'sigma'])
        bounds = ([-20,20],[-10,10],[1e-9,None])  # alpha, side, sigma

        for i in range(n):
            if subjects[i] in rejects:
                continue
            s = subjects[i]

            row1 = [s, 1] + minimize(model_1_eq, parameters, args=(s, zscored), bounds=bounds).x.tolist()  # type 1
            row2 = [s, 2] + minimize(model_6_eq, parameters, args=(s, zscored), bounds=bounds).x.tolist()  # type 2
            row3 = [s, 3] + minimize(model_1_uneq, parameters, args=(s, zscored), bounds=bounds).x.tolist()  # type 3
            row4 = [s, 4] + minimize(model_6_uneq, parameters, args=(s, zscored), bounds=bounds).x.tolist()  # type 4

            rows = [row1, row2, row3, row4]
            writer.writerows(rows)


def run_by_horizon(filename, zscored=True):
    # params = alpha, side, sigma
    parameters = np.array([10, 0, 5])
    subjects = df['Subject'].unique().tolist()
    n = len(subjects)
    rejects = reject.query('Reject == 1')['Subject'].tolist()

    with open('../figures/' + filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Subject', 'Horizon', 'alpha', 'side', 'sigma'])  #
        bounds = ([-20, 20], [-20, 20], [1e-9, 20])  # alpha, side, sigma

        for i in range(n):
            if subjects[i] in rejects:
                continue
            s = subjects[i]

            row1 = [s, 1] + minimize(model_1, parameters, args=(s, zscored), bounds=bounds).x.tolist()  # type 1
            row2 = [s, 6] + minimize(model_6, parameters, args=(s, zscored), bounds=bounds).x.tolist()  # type 2

            rows = [row1, row2]
            writer.writerows(rows)


def main():
    run_by_horizon('params_by_horizon.csv', zscored=False)
    run_by_horizon('params_by_horizon_zscored.csv', zscored=True)


if __name__ == '__main__':
    main()
