import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from stantools.io import load_model, save_fit, load_fit
from scipy import stats

# load global data
df = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/data.csv')
reject = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/reject.csv')
subjects = df['Subject'].unique()
rejects = reject.query('Reject == 1')['Subject'].tolist()
anxiety = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/surveys.csv').copy()

np.random.seed(47404)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.

N = len(subjects) - len(rejects)  ## number of subjects
K = 3   ## number of params to be fitted per subject (info, side, sigma)
T = 40  ## number of trials per participant (40 for each horizon)

## Group-level parameters.
mu = np.random.normal(0, 1, K)
sigma = np.abs(np.random.normal(1,0.25,K))

## Subject-level parameters.
beta = np.random.normal(mu, sigma, (N,K)).T


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Get data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def getData(gameLength):
    ## Define design matrix.
    X = np.column_stack([
        np.ones(T),
        np.linspace(-2, 2, T),
        np.linspace(-2, 2, T)
    ])

    ## Preallocate space.
    Y = np.zeros((N, T), dtype=int)  ### choice data
    info = np.zeros((N, T), dtype=int)  ### info
    delta = np.zeros((N, T), dtype=int)  ### delta

    i = 0
    for s in subjects:
        if s in rejects:
            continue
        data = df.query('Subject == @s and Horizon == @gameLength and Trial == 5')
        Y[i] = data['Choice']
        info[i] = data['Info']
        delta[i] = adjust_delta(data['delta'].reset_index(drop=True), info[i])
        i += 1

    ## Assemble data and return.
    return dict(N=N, K=K, T=T, X=X, Y=Y, info=info, delta=delta)


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
def get_ncs(fullrow=True):
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


# Info: 0 = [2,2] trial, 1 = [3,1] trial, -1 = [1,3] trial
def adjust_delta(deltas, info):
    for i in range(len(deltas)):
        if info[i] == -1:
            deltas[i] = -deltas[i]
    return deltas


def model(horizon):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Define parameters.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## I/O parameters.
    if horizon == 1:
        gameLength = 5
        output_name = 'hierarchical-logistic-1'  ## horizon = 1
    elif horizon == 6:
        gameLength = 10
        output_name = 'hierarchical-logistic-6'  ## horizon = 6
    else:
        print("Horizon must be either 1 or 6", file=sys.stderr)
        return

    stan_model = 'hierarchical-logistic'

    ## Sampling parameters.
    samples = 2000
    warmup = 1500
    chains = 4
    thin = 1
    n_jobs = 4

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Fit model w/ Stan.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## Load Stan model.
    StanModel = load_model(stan_model)
    dd = getData(gameLength)

    # Fit model.
    StanFit = StanModel.sampling(data=dd, iter=samples, warmup=warmup, chains=chains, thin=thin, n_jobs=n_jobs,
                                 seed=47404)
    print(StanFit)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Save data
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    save_fit(output_name, StanFit, data=dd)
    return StanFit


def trend(x, y):
    z = np.polyfit(x, y, 1)
    return np.poly1d(z)


def scatter_params(fit1, fit6, test, figname):
    scores = -1
    if test.upper() == 'PSWQ':
        scores = get_pswq()
    elif test.upper() == 'IUS-12':
        scores = get_ius12()
    elif test.upper() == 'NCS':
        scores = get_ncs()

    samples1 = fit1.extract()
    info1 = samples1['alpha'][0,]
    sides1 = samples1['side'][0,]
    sigmas1 = samples1['sigma'][0,]

    samples6 = fit6.extract()
    info6 = samples6['alpha'][0,]
    sides6 = samples6['side'][0,]
    sigmas6 = samples6['sigma'][0,]

    fig1, (alpha1, alpha6) = plt.subplots(nrows=1, ncols=2, sharey='row', figsize=(12, 4))
    alpha1.plot(scores, info1, 'o', color='blue', label='Horizon 1')
    tr = trend(scores, info1)
    alpha1.plot(scores, tr(scores), '-')
    alpha6.plot(scores, info6, 'o', color='orange', label='Horizon 6')
    tr = trend(scores, info6)
    alpha6.plot(scores, tr(scores), '-')
    rho_1, p1 = stats.spearmanr(scores, info1)
    rho_6, p6 = stats.spearmanr(scores, info6)
    corr = '''Spearman correlations
                H1: rho = %f, p = %f
                H6: rho = %f, p = %f''' % (rho_1, p1, rho_6, p6)
    alpha1.set(title='Horizon 1', xlabel='%s score' % test, ylabel='Information bonus')
    alpha6.set(title='Horizon 6', xlabel='%s score' % test)
    fig1.suptitle('%s score vs. information bonus' % test, fontsize=16)
    fig1.text(.5, 0.01, corr, ha='center', fontsize=8)
    fig1.tight_layout(pad=2.5)
    fig1.savefig(figname + '-alpha.png')
    print(corr)

    fig2, (side1, side6) = plt.subplots(nrows=1, ncols=2, sharey='row', figsize=(12, 4))
    side1.plot(scores, sides1, 'o', color='blue', label='Horizon 1')
    tr = trend(scores, sides1)
    side1.plot(scores, tr(scores), '-')
    side6.plot(scores, sides6, 'o', color='orange', label='Horizon 6')
    tr = trend(scores, sides6)
    side6.plot(scores, tr(scores), '-')
    rho_1, p1 = stats.spearmanr(scores, sides1)
    rho_6, p6 = stats.spearmanr(scores, sides6)
    corr = '''Spearman correlations
                H1: rho = %f, p = %f
                H6: rho = %f, p = %f''' % (rho_1, p1, rho_6, p6)
    side1.set(title='Horizon 1', xlabel='%s score' % test, ylabel='Side bias')
    side6.set(title='Horizon 6', xlabel='%s score' % test)
    fig2.suptitle('%s score vs. side bias' % test, fontsize=16)
    fig2.text(.5, .01, corr, ha='center', fontsize=8)
    fig2.tight_layout(pad=2.5)
    plt.savefig(figname + '-side.png')

    fig3, (sigma1, sigma6) = plt.subplots(nrows=1, ncols=2, sharey='row', figsize=(12, 4))
    sigma1.plot(scores, sigmas1, 'o', color='blue', label='Horizon 1')
    tr = trend(scores, sigmas1)
    sigma1.plot(scores, tr(scores), '-')
    sigma6.plot(scores, sigmas6, 'o', color='orange', label='Horizon 6')
    tr = trend(scores, sigmas6)
    sigma6.plot(scores, tr(scores), '-')
    rho_1, p1 = stats.spearmanr(scores, sigmas1)
    rho_6, p6 = stats.spearmanr(scores, sigmas6)
    corr = '''Spearman correlations
                H1: rho = %f, p = %f
                H6: rho = %f, p = %f''' % (rho_1, p1, rho_6, p6)
    sigma1.set(title='Horizon 1', xlabel='%s score' % test, ylabel='Decision noise')
    sigma6.set(title='Horizon 6', xlabel='%s score' % test)
    fig3.suptitle('%s score vs. decision noise' % test, fontsize=16)
    fig3.text(.5, .01, corr, ha='center', fontsize=8)
    fig3.tight_layout(pad=2.5)
    plt.savefig(figname + '-sigma.png')


def plotFit(fit1, fit6):
    ## plot chains
    chains = fit1.extract(inc_warmup=True, permuted=False)
    fig = plt.figure()
    plt.plot(chains[..., 0])
    figname = 'mcmc-chains-h1'
    # plt.set(title='MCMC chains horizon 1')
    fig.savefig(figname)

    chains = fit6.extract(inc_warmup=True, permuted=False)
    fig = plt.figure()
    plt.plot(chains[..., 0])
    figname = 'mcmc-chains-h6'
    # plt.set(title='MCMC chains horizon 6')
    fig.savefig(figname)

    ## inspect distributions
    samples1 = fit1.extract()
    info1 = samples1['alpha'][0,]
    gr_info1 = samples1['gr_alpha'][0,]
    sides1 = samples1['side'][0,]
    gr_side1 = samples1['gr_side'][0,]
    sigmas1 = samples1['sigma'][0,]
    gr_sigma1 = samples1['gr_sigma'][0,]

    samples6 = fit6.extract()
    info6 = samples6['alpha'][0,]
    gr_info6 = samples6['gr_alpha'][0,]
    sides6 = samples6['side'][0,]
    gr_side6 = samples6['gr_side'][0,]
    sigmas6 = samples6['sigma'][0,]
    gr_sigma6 = samples6['gr_sigma'][0,]

    print(gr_info1, gr_side1, gr_sigma1)
    print(gr_info6, gr_side6, gr_sigma6)

    fig, (alpha, side, sig) = plt.subplots(nrows=1, ncols=3)

    fig, axes = plt.subplots(1, 3, figsize=(10, 3), dpi=100)

    sns.distplot(info1, label='Horizon 1', ax=axes[0])
    sns.distplot(info6, label='Horizon 6', ax=axes[0])
    axes[0].set(title='Information bonus')
    axes[0].legend(loc='right', fontsize='xx-small')

    sns.distplot(sides1, label='Horizon 1', ax=axes[1])
    sns.distplot(sides6, label='Horizon 6', ax=axes[1])
    axes[1].set(title='Side bias')

    sns.distplot(sigmas1, label='Horizon 1', ax=axes[2])
    sns.distplot(sigmas6, label='Horizon 6', ax=axes[2])
    axes[2].set(title='Decision noise')

    fig.suptitle('Model parameters by horizon', fontsize=16)
    fig.tight_layout(pad=2.5)
    fig.savefig('all-params-dist')

    # fig1, (alpha1, alpha6) = plt.subplots(nrows=2, ncols=1, sharex='col')
    # alpha1.sns.displot(info1)
    # alpha6.sns.distplot(info6)
    # figname = 'info-param-distribution'
    # alpha1.set(title='Horizon 1')
    # alpha6.set(title='Horizon 6', ylabel='Information bonus parameter')
    # fig1.suptitle('Distribution of information bonus parameters by horizon', fontsize=16)
    # fig1.tight_layout(pad=2.5)
    # fig1.savefig(figname)
    #
    # fig2, (side1, side6) = plt.subplots(nrows=2, ncols=1, sharex='col')
    # side1.sns.displot(sides1)
    # side6.sns.distplot(sides6)
    # figname = 'side-param-distribution'
    # side1.set(title='Horizon 1')
    # side6.set(title='Horizon 6', ylabel='Side bias parameter')
    # fig2.suptitle('Distribution of side bias parameters by horizon', fontsize=16)
    # fig2.tight_layout(pad=2.5)
    # fig2.savefig(figname)
    #
    # fig3, (sigma1, sigma6) = plt.subplots(nrows=2, ncols=1, sharex='col')
    # sigma1.sns.displot(sigmas1)
    # sigma6.sns.distplot(sigmas6)
    # figname = 'side-param-distribution'
    # sigma1.set(title='Horizon 1')
    # sigma6.set(title='Horizon 6', ylabel='Decision noise parameter')
    # fig3.suptitle('Distribution of decision noise parameters by horizon', fontsize=16)
    # fig3.tight_layout(pad=2.5)
    # fig3.savefig(figname)


    # ## posterior predictive check TODO fix so that it corresponds to new parameter names
    # sigma_hat = np.median(samples['sigma'], axis=0)
    # plt.figure()
    # ax = sns.scatterplot(x=sigma[0], y=sigma_hat[0])
    # ax = sns.scatterplot(x=beta[1], y=beta_hat[:,1])
    # ax.plot([-1,5],[-1,5])
    # ax.set(xlabel='True', ylabel='Predicted')
    #
    # print(np.corrcoef(beta[0], beta_hat[:,0]))


def main():
    fit1 = model(horizon=1)
    fit6 = model(horizon=6)

    plotFit(fit1, fit6)

    scatter_params(fit1, fit6, 'IUS-12', './IUS-12_hierachical')
    scatter_params(fit1, fit6, 'PSWQ', './PSWQ_hierachical')
    scatter_params(fit1, fit6, 'NCS', './NCS_hierachical')


# fit1 = model(horizon=1)
# samples1 = fit1.extract()
# info1 = samples1['alpha'][0,]
# sides1 = samples1['side'][0,]
# sigmas1 = samples1['sigma'][0,]


if __name__ == '__main__':
    main()
