import numpy as np
import matplotlib.pyplot as plt
from stantools.io import load_model
import seaborn as sns

sns.set_style('white')

## Define parameters.
b0 = -1
b1 = 2


## Define logistic function.
def inv_logit(x):
    return 1. / (1 + np.exp(-x))


## Define observed variables.
x = np.linspace(-5, 5, 500)

## Define probability of choice.
theta = inv_logit(b0 + b1 * x)

## Simulate choice.
y = np.random.binomial(1, theta)

plt.plot(x, theta, '-')
plt.show()

## Compile model.
StanModel = load_model('/pilot-v0.2/scripts/basic-logistic/logistic-demo.stan')

## Prepare data for Stan.
dd = dict(T=x.size, x=x, y=y)

## Fit model.
StanFit = StanModel.optimizing(data=dd, seed=0)
print(StanFit)
