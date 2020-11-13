import pystan
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from stantools.io import load_model, save_fit

df = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/data.csv')
reject = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/reject.csv')

subjects = df['Subject'].unique()
rejects = reject.query('Reject == 1')['Subject'].tolist()

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
def getData():
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
        data = df.query('Subject == @s and Horizon == 5 and Trial == 5')
        Y[i] = data['Choice']
        info[i] = data['Info']
        delta[i] = adjust_delta(data['delta'].reset_index(drop=True), info[i])
        i += 1

    ## Assemble data and return.
    return dict(N=N, K=K, T=T, X=X, Y=Y, info=info, delta=delta)


# Info: 0 = [2,2] trial, 1 = [3,1] trial, -1 = [1,3] trial
def adjust_delta(deltas, info):
    for i in range(len(deltas)):
        if info[i] == -1:
            deltas[i] = -deltas[i]
    return deltas


def main():
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Define parameters.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## I/O parameters.
    stan_model = 'hierarchical-logistic.stan'

    ## Sampling parameters.
    samples = 2000
    warmup = 1500
    chains = 4
    thin = 1
    n_jobs = 4

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Fit model w/ Stan.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## Load Stan model.
    StanModel = load_model(stan_model)

    dd = getData()

    # Fit model.
    StanFit = StanModel.sampling(data=dd, iter=samples, warmup=warmup, chains=chains, thin=thin,
                                 n_jobs=n_jobs, seed=47404)
    print(StanFit)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### inspect data
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## inspect chains
    chains = StanFit.extract(inc_warmup=True, permuted=False)
    print(chains.shape)
    plt.figure()
    plt.plot(chains[...,0])

    ## inspect distributions
    samples = StanFit.extract()

    plt.figure()
    sns.distplot(samples['mu'][:,0])

    ## posterior predictive check
    beta_hat = np.median(samples['beta'], axis=0)
    plt.figure()
    ax = sns.scatterplot(x=beta[0], y=beta_hat[:,0])
    ax = sns.scatterplot(x=beta[1], y=beta_hat[:,1])
    ax.plot([-1,5],[-1,5])
    ax.set(xlabel='True', ylabel='Predicted')

    print(np.corrcoef(beta[0], beta_hat[:,0]))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Save data
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    from stantools.io import load_fit

    test = load_fit('hierarchical-logistic.pkl')

    save_fit(stan_model, StanFit, data=dd)


if __name__ == '__main__':
    main()
