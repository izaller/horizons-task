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


def best_fit_line(data, param):
    z1 = np.polyfit(data, param, 1)
    return np.poly1d(z1)


def plot_pswq(filename, title, figname):
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

    fig, (alpha, side, sigma) = plt.subplots(1, 3, figsize=(32, 4))
    alpha.plot(pswq_sums, alphas_h1, 'o', color='blue', label='Horizon 1')
    fit_a1 = best_fit_line(pswq_sums, alphas_h1)
    alpha.plot(pswq_sums, fit_a1(pswq_sums), "-", color='blue')
    alpha.plot(pswq_sums, alphas_h6, 'o', color='orange', label='Horizon 6')
    fit_a6 = best_fit_line(pswq_sums, alphas_h6)
    alpha.plot(pswq_sums, fit_a6(pswq_sums), "-", color='orange')
    alpha.set(title=title % 'alpha (information)', xlabel='Sum PSWQ', ylabel='alpha')
    alpha.legend()

    side.plot(pswq_sums, sides_h1, 'o', color='blue', label='Horizon 1')
    fit_sides1 = best_fit_line(pswq_sums, sides_h1)
    side.plot(pswq_sums, fit_sides1(pswq_sums), "-", color='blue')
    side.plot(pswq_sums, sides_h6, 'o', color='orange', label='Horizon 6')
    fit_sides6 = best_fit_line(pswq_sums, sides_h6)
    side.plot(pswq_sums, fit_sides6(pswq_sums), "-", color='orange')
    side.set(title=title % 'side (spatial parameter)', xlabel='Sum PSWQ', ylabel='side')
    side.legend()

    sigma.plot(pswq_sums, sigmas_h1, 'o', color='blue', label='Horizon 1')
    fit_sigmas1 = best_fit_line(pswq_sums, sigmas_h1)
    sigma.plot(pswq_sums, fit_sigmas1(pswq_sums), "-", color='blue')
    sigma.plot(pswq_sums, sigmas_h6, 'o', color='orange', label='Horizon 6')
    fit_sigmas6 = best_fit_line(pswq_sums, sigmas_h6)
    sigma.plot(pswq_sums, fit_sigmas6(pswq_sums), "-", color='orange')
    sigma.set(title=title % 'sigma (information noise)', xlabel='Sum PSWQ', ylabel='sigma')
    sigma.legend()

    plt.tight_layout()
    plt.savefig('../figures,params/' + figname)


def main():
    plot_pswq('../figures,params/params_by_horizon_zscored.csv',
              'Plot of anxiety scores\n vs %s parameters\n(z scored)',
              'params_by_horizon_zscored.png')
    plot_pswq('../figures,params/params_by_horizon.csv',
              'Plot of anxiety scores\n vs %s parameters',
              'params_by_horizon.png')
    plot_pswq('../figures,params/params_stan.csv',
              'Plot of anxiety scores\n vs %s parameters',
              'params_stan.png')


if __name__ == '__main__':
    main()
