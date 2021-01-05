## -------------------------------------------------- ##
# Plot anxiety scores vs. model parameter fits
## -------------------------------------------------- ##

# plot parameters by subject
from statistics import mean
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# load global data
anxiety = pd.read_csv('../data/surveys.csv').copy()
reject = pd.read_csv('../data/reject.csv')
subjects = anxiety['Subject'].unique()
rejects = reject.query('Reject == 1')['Subject'].tolist()


# filename is the path to df
# figname is the filepath where the figure will be saved
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
    plt.savefig(figname)


# returns parameters of interest (alpha, side, sigma) split by horizon
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


# returns sum pswq score for all subjects
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


# returns sum IUS12 score for all subjects
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


# returns sum NCS score
    # if fullrow is True, sum across the entire row
    # if fullrow is False, sum only the questions corresponding to decisiveness
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


# test is the name of the anxiety questionnaire (PSWQ, IUS12, NCS)
# filename is the path to df
# figname is the filepath where the figure will be saved
# fullrow is set to false in the main function only when we want to analyze individual sections of questionnaires
    # for further info, see function "get_ncs"
def scatter_params(test, filename, figname, fullrow=True):
    scores = -1
    if test.upper() == 'PSWQ':
        scores = get_pswq()
    elif test.upper() == 'IUS-12':
        scores = get_ius12()
    elif test.upper() == 'NCS':
        scores = get_ncs(fullrow)

    df = pd.read_csv(filename)
    alphas_h1, alphas_h6, sides_h1, sides_h6, sigmas_h1, sigmas_h6 = get_params(df)

    fig1, (alpha1, alpha6) = plt.subplots(nrows=1, ncols=2, sharey='row', figsize=(12, 4))
    alpha1.plot(scores, alphas_h1, 'o', color='blue', label='Horizon 1')
    alpha6.plot(scores, alphas_h6, 'o', color='orange', label='Horizon 6')
    rho_1, p1 = stats.spearmanr(scores, alphas_h1)
    rho_6, p6 = stats.spearmanr(scores, alphas_h6)
    print(rho_1, p1, rho_6, p6)
    corr = 'spearman correlation, H1 = %f\nspearman correlation, H6 = %f\n' % (rho_1, rho_6)
    alpha1.set(title='Horizon 1', xlabel='%s score' % test, ylabel='Information bonus')
    alpha6.set(title='Horizon 6', xlabel='%s score' % test)
    fig1.suptitle('%s score vs. information bonus' % test, fontsize=16)
    fig1.text(.5, 0, corr, ha='center', fontsize=8)
    fig1.tight_layout(pad=2.5)
    fig1.savefig(figname + '-alpha.png')
    print(corr)

    # fig2, (side1, side6) = plt.subplots(nrows=1, ncols=2, sharey='row', figsize=(12, 4))
    # side1.plot(scores, sides_h1, 'o', color='blue', label='Horizon 1')
    # side6.plot(scores, sides_h6, 'o', color='orange', label='Horizon 6')
    # rho_1 = stats.spearmanr(scores, sides_h1)[0]
    # rho_6 = stats.spearmanr(scores, sides_h6)[0]
    # corr = 'spearman correlation, H1 = %f\nspearman correlation, H6 = %f' % (rho_1, rho_6)
    # side1.set(title='Horizon 1', xlabel='%s score' % test, ylabel='Side bias')
    # side6.set(title='Horizon 6', xlabel='%s score' % test)
    # fig2.text(.5, .05, corr, ha='center', fontsize=8)
    # fig2.suptitle('%s score vs. side bias' % test, fontsize=16)
    # fig2.tight_layout(pad=2.5)
    # plt.savefig(figname + '-side.png')
    #
    # fig3, (sigma1, sigma6) = plt.subplots(nrows=1, ncols=2, sharey='row', figsize=(12, 4))
    # sigma1.plot(scores, sigmas_h1, 'o', color='blue', label='Horizon 1')
    # sigma6.plot(scores, sigmas_h6, 'o', color='orange', label='Horizon 6')
    # rho_1 = stats.spearmanr(scores, sigmas_h1)[0]
    # rho_6 = stats.spearmanr(scores, sigmas_h6)[0]
    # corr = 'spearman correlation, H1 = %f\nspearman correlation, H6 = %f' % (rho_1, rho_6)
    # sigma1.set(title='Horizon 1', xlabel='%s score' % test, ylabel='Decision noise')
    # sigma6.set(title='Horizon 6', xlabel='%s score' % test)
    # fig3.text(.5, .05, corr, ha='center', fontsize=8)
    # fig3.suptitle('%s score vs. decision noise' % test, fontsize=16)
    # fig3.tight_layout(pad=2.5)
    # plt.savefig(figname + '-sigma.png')


# filename is the path to df
# figname is the filepath where the figure will be saved
def plot_bars(filename, figname):
    df = pd.read_csv(filename)

    alphas_h1, alphas_h6, sides_h1, sides_h6, sigmas_h1, sigmas_h6 = get_params(df)

    fig, (alpha, side, sigma) = plt.subplots(nrows=1, ncols=3, figsize=(17, 4))

    alpha.bar([1, 2], [mean(alphas_h1), mean(alphas_h6)], tick_label=["Horizon 1", "Horizon 6"], color=('tab:blue', 'tab:orange'), edgecolor='k')
    alpha.set(title='Information Parameter', ylabel='average infomation bonus')
    alpha.axhline(y=0, color='black')

    side.bar([1, 2], [mean(sides_h1), mean(sides_h6)], tick_label=["Horizon 1", "Horizon 6"], color=('tab:blue', 'tab:orange'), edgecolor='k')
    side.set(title='Spatial Parameter', ylabel='average spatial bias')

    sigma.bar([1, 2], [mean(sigmas_h1), mean(sigmas_h6)], tick_label=["Horizon 1", "Horizon 6"], color=('tab:blue', 'tab:orange'), edgecolor='k')
    sigma.set(title='Decision Noise', ylabel='average sigma')

    plt.tight_layout()
    plt.savefig(figname)


def main():
    # scatter_params('PSWQ',
    #                '../figures/params_stan.csv',
    #                '../figures/PSWQ_params_stan.png')
    # plot_alpha_hist('../figures/params_stan.csv', 'alpha_hist_stan.png')
    # scatter_params('IUS12',
    #                '../figures/params_stan.csv',
    #                '../figures/IUS12_params_stan.png')
    # scatter_params('NCS',
    #                '../figures/params_stan.csv',
    #                '../figures/NCS_params_stan.png')
    # scatter_params('NCS',
    #                '../figures/params_stan.csv',
    #                '../figures/NCS_decisiveness_params_stan.png',
    #                fullrow=False)
    # plot_bars('../param-csv-output/params_stan.csv', '../figures/bar_plot_params.png')

    csvname = '../param-csv-output/params_stan.csv'
    dir = './'
    # plot_bars(csvname, dir + 'bar_plot_params_hierarchical.png')
    # scatter_params('PSWQ',
    #                csvname,
    #                dir + 'PSWQ_params_stan_hierachical.png')
    # plot_alpha_hist(csvname, dir + 'alpha_hist_stan.png')
    scatter_params('IUS-12',
                   csvname,
                   dir + 'IUS-12_hierachical')
    # scatter_params('NCS',
    #                csvname,
    #                dir + 'NCS_params_stan_hierachical.png')
    # scatter_params('NCS',
    #                csvname,
    #                '../figures/NCS_decisiveness_params_stan_hierachical.png',
    #                fullrow=False)


if __name__ == '__main__':
    main()
