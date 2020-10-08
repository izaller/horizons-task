# plot parameters by subject
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# load global data
anxiety = pd.read_csv('../data/surveys.csv').copy()
reject = pd.read_csv('../data/reject.csv')
subjects = anxiety['Subject'].unique()
rejects = reject.query('Reject == 1')['Subject'].tolist()


def plot_alpha_hist(filename, figname):
    df = pd.read_csv(filename)
    alpha_h1 = df.query('Horizon == 1')['alpha']
    alpha_h6 = df.query('Horizon == 6')['alpha']

    # plot histogram of all alphas
    fig, (h1, h6) = plt.subplots(1, 2, figsize=(16, 4))
    h1.set(title='Information Parameter H1', xlabel='alpha parameter')
    h6.set(title='Information Parameter H6', xlabel='alpha parameter')

    h1.hist(alpha_h1, bins=20, edgecolor='black', linewidth=1)
    h6.hist(alpha_h6, bins=20, edgecolor='black', linewidth=1)
    plt.savefig('../figures,params/' + figname)


def get_params(df):
    alphas_h1 = []
    alphas_h6 = []
    sides_h1 = []
    sides_h6 = []
    sigmas_h1 = []
    sigmas_h6 = []
    for s in range(len(subjects)):
        sub = subjects[s]
        if sub in rejects:
            continue
        # get function parameters from subject
        query_1 = df.query('Subject == @sub and Horizon == 1')
        alphas_h1.append(query_1['alpha'].tolist()[0])
        sides_h1.append(query_1['side'].tolist()[0])
        sigmas_h1.append(query_1['sigma'].tolist()[0])
        query_6 = df.query('Subject == @sub and Horizon == 6')
        alphas_h6.append(query_6['alpha'].tolist()[0])
        sides_h6.append(query_6['side'].tolist()[0])
        sigmas_h6.append(query_6['sigma'].tolist()[0])

    return alphas_h1, alphas_h6, sides_h1, sides_h6, sigmas_h1, sigmas_h6


def get_pswq():
    pswq_sums = []
    for s in range(len(subjects)):
        sub = subjects[s]
        if sub in rejects:
            continue
        row = anxiety.iloc[s, 6:23]
        # sum anxiety scores for the subject
        pswq_sums.append(sum(row))
    return pswq_sums


def get_ius12():
    ius12_sums = []
    for s in range(len(subjects)):
        sub = subjects[s]
        if sub in rejects:
            continue
        row = anxiety.iloc[s, 28:41]
        # sum anxiety scores for the subject
        ius12_sums.append(sum(row))
    return ius12_sums


def get_ncs(fullrow):
    ncs_sums = []
    for s in range(len(subjects)):
        sub = subjects[s]
        if sub in rejects:
            continue
        row = anxiety.iloc[s, 46:62]
        if not fullrow:
            row = row[6:9]
        # sum anxiety scores for the subject
        ncs_sums.append(sum(row))
    return ncs_sums


def scatter_params(test, filename, figname, fullrow=True):
    scores = -1
    if test.upper() == 'PSWQ':
        scores = get_pswq()
    elif test.upper() == 'IUS12':
        scores = get_ius12()
    elif test.upper() == 'NCS':
        scores = get_ncs(fullrow)

    df = pd.read_csv(filename)
    alphas_h1, alphas_h6, sides_h1, sides_h6, sigmas_h1, sigmas_h6 = get_params(df)

    fig, (alpha, side, sigma) = plt.subplots(nrows=1, ncols=3, figsize=(17,4))

    alpha.plot(scores, alphas_h1, 'o', color='blue', label='Horizon 1')
    alpha.plot(scores, alphas_h6, 'o', color='orange', label='Horizon 6')
    rho_1 = stats.spearmanr(scores, alphas_h1)[0]
    rho_6 = stats.spearmanr(scores, alphas_h6)[0]
    corr = 'spearman correlation, H1 = %f\nspearman correlation, H6 = %f' % (rho_1, rho_6)
    alpha.set(title='%s score vs. alpha' % test, xlabel='%s score\n%s' % (test, corr), ylabel='alpha')
    alpha.legend()

    side.plot(scores, sides_h1, 'o', color='blue', label='Horizon 1')
    side.plot(scores, sides_h6, 'o', color='orange', label='Horizon 6')
    side.set(title='%s score vs. side (spatial parameter)' % test, xlabel='%s score' % test, ylabel='side')
    side.legend()

    sigma.plot(scores, sigmas_h1, 'o', color='blue', label='Horizon 1')
    sigma.plot(scores, sigmas_h6, 'o', color='orange', label='Horizon 6')
    sigma.set(title='%s score vs. sigma (information noise)' % test, xlabel='%s score' % test, ylabel='sigma')
    sigma.legend()

    plt.tight_layout()
    plt.savefig('../figures,params/' + figname)


def main():
    # plot_pswq('PSWQ',
    #           '../figures,params/params_by_horizon_zscored.csv',
    #           'Penn State Worry Questionnaire score vs. %s\n(z scored)',
    #           'PSWQ_params_by_horizon_zscored.png')
    # plot_pswq('PSWQ',
    #           '../figures,params/params_by_horizon.csv',
    #           'Penn State Worry Questionnaire score vs. %s',
    #           'PSWQ_params_by_horizon.png')
    # scatter_params('PSWQ',
    #                '../figures,params/params_stan.csv',
    #                'PSWQ_params_stan.png')
    # # plot_alpha_hist('../figures,params/params_stan.csv', 'alpha_hist_stan.png')
    # scatter_params('IUS12',
    #                '../figures,params/params_stan.csv',
    #                'IUS12_params_stan.png')
    scatter_params('NCS',
                   '../figures,params/params_stan.csv',
                   'NCS_params_stan.png')
    scatter_params('NCS',
                   '../figures,params/params_stan.csv',
                   'NCS_decisiveness_params_stan.png',
                   fullrow=False)


if __name__ == '__main__':
    main()
