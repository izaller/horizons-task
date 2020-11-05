import pystan
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from stantools.io import load_model, save_fit

np.random.seed(47404)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
N = 20
K = 2
T = 50

## Group-level parameters.
mu = np.random.normal(0, 1, K)
sigma = np.abs(np.random.normal(1,0.25,K))

## Subject-level parameters.
beta = np.random.normal(mu, sigma, (N,K)).T

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Get data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define logistic function.
def inv_logit(x):
     return 1 / (1 + np.exp(-x))

## Define design matrix.
X = np.column_stack([
    np.ones(T),
    np.linspace(-2,2,T)
])

## Preallocate space.
Y = np.zeros((N,T), dtype=int)

## Iteratively simulate choices.
for i in range(N):
    theta = inv_logit( X @ beta[:,i] )
    Y[i] = np.random.binomial(1, theta)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'hierarchical_logistic'

## Sampling parameters.
samples = 2000
warmup = 1500
chains = 4
thin = 1
n_jobs = 4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit model w/ Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(N=N, K=K, T=T, X=X, Y=Y)

## Load Stan model.
StanModel = load_model(stan_model)

## Fit model.
StanFit = StanModel.sampling(data=dd, iter=samples, warmup=warmup, chains=chains, thin=thin,
                             n_jobs=n_jobs, seed=47404)

print(StanFit)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### inspect data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## inspect chains
chains = StanFit.extract(inc_warmup=True, permuted=False)
print(chains.shape)
plt.plot(chains[...,0])

## inspect distributions
samples = StanFit.extract()

sns.histplot(samples['mu'][:,0])

## posterior predictive check
beta_hat = np.median(samples['beta'], axis=0)
ax = sns.scatterplot(x=beta[0], y=beta_hat[:,0])
ax = sns.scatterplot(x=beta[1], y=beta_hat[:,1])
ax.plot([-1,5],[-1,5])
ax.set(xlabel='True', ylabel='Predicted')

np.corrcoef(beta[0], beta_hat[:,0])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from stantools.io import load_fit

test = load_fit('hierarchical-logistic.pxkl')

save_fit(stan_model, StanFit, data=dd)