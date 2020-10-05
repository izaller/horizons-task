import numpy as np
import matplotlib.pyplot as plt
from stantools.io import load_model
import pandas as pd
import seaborn as sns
import csv

sns.set_style('white')

# Define parameters.
alpha = 5
side = 0
sigma = 5

df = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/data.csv')
reject = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/reject.csv')


# Info: 0 = [2,2] trial, 1 = [3,1] trial, -1 = [1,3] trial
def adjust_delta(deltas, info):
    for i in range(len(deltas)):
        if info[i] == -1:
            deltas[i] = -deltas[i]
    return deltas


# Define logistic function.
def inv_logit(x):
    return 1. / (1 + np.exp(-x))


def getData(subject, horizon):
    data = df.query('Subject == @subject and Horizon == @horizon and Trial == 5').reset_index(drop=True)
    deltas = data['delta'].copy()  # get delta for horizon 1
    info = data['Info']  # get info for horizon 1
    deltas = adjust_delta(deltas, info)
    y = data['Choice']

    # Prepare and return data for Stan.
    return dict(T=y.size, delta=deltas, info=info, y=y)


def model_h1(StanModel):
    data = []
    subjects = df['Subject'].unique()
    for subject in subjects:
        # get prepared data for Stan.
        dd = getData(subject, 5)

        # Fit model.
        StanFit = StanModel.optimizing(data=dd, seed=0)
        fit = (StanFit['alpha'], StanFit['side'], StanFit['sigma'])
        data.append(fit)

    return data


def model_h6(StanModel):
    data = []
    subjects = df['Subject'].unique()
    for subject in subjects:
        # get prepared data for Stan.
        dd = getData(subject, 10)

        # Fit model.
        StanFit = StanModel.optimizing(data=dd, seed=0)
        fit = (StanFit['alpha'], StanFit['side'], StanFit['sigma'])
        data.append(fit)

    return data


def writeData(params_h1, params_h6, filename):
    subjects = df['Subject'].unique()
    rejects = reject.query('Reject == 1')['Subject'].tolist()
    n = len(subjects)

    with open('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/figures,params/' + filename,
              'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Subject', 'Horizon', 'alpha', 'side', 'sigma'])

        for i in range(n):
            if subjects[i] in rejects:
                continue
            s = subjects[i]
            row1 = [s, 1, params_h1[i][0], params_h1[i][1], params_h1[i][2]]
            row2 = [s, 6, params_h6[i][0], params_h6[i][1], params_h6[i][2]]

            rows = [row1, row2]
            writer.writerows(rows)


def main():
    # Compile model.
    StanModel = load_model('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/scripts/logistic.pkl')

    params_h1 = model_h1(StanModel)
    params_h6 = model_h6(StanModel)
    writeData(params_h1, params_h6, 'params_stan.csv')


if __name__ == '__main__':
    main()
