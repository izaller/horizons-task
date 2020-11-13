// used by file 'stan-fitting-hierarchical.py'
// fits single-subject data using mcmc

data {

    // Metadata
    int  N;
    int  K;
    int  T;

    // Data
    int        Y[N,T];
    vector[T]  info[N];
    vector[T]  delta[N];

}
parameters {

    // Subject-level parameters
    real                alpha;
    real                side;
    real<lower=0>       sigma;

}
model {

    // Priors
    alpha ~ normal(0, 1);
    side ~ normal(0, 1);
    sigma ~ normal(0, 2);

    // Likelihood
    for (i in 1:N) {
        Y[i] ~ bernoulli_logit( (delta[i] + info[i] * alpha + side) / sigma );
    }

}