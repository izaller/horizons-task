// used by file 'stan-fitting-hierarchical.py'

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

    // Group-level parameters TODO make separate parameters instead of vector
    real                gr_alpha;
    real                gr_side;
    real<lower=0>       gr_sigma;
    vector<lower=0>[K]  gr_sd;  // standard dev for all params

    // Subject-level parameters
    real                alpha;
    real                side;
    real<lower=0>       sigma;

}
model {

    // Priors
    mu ~ normal(0, 1);
    sigma ~ normal(0, 2);

    for (i in 1:N) {
        beta[i] ~ normal( mu, sigma );
    }

    // Likelihood
    for (i in 1:N) {
        Y[i] ~ bernoulli_logit( (delta[i] + info[i] * beta[i,1] + beta[i,2]) / beta[i,3] );
    }

}