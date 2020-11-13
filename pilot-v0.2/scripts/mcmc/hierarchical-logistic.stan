// used by file 'stan-fitting-hierarchical.py'

data {

    // Metadata
    int  N;                  // Number of subjects
    int  K;                  // Number of regressors (params per subject that we're trying to fit)
    int  T;                  // Number of trials (per participant)

    // Data
    int        Y[N,T];
    vector[T]  info[N];
    vector[T]  delta[N];

}
parameters {

    // Group-level parameters
    real                gr_alpha;
    real                gr_side;
    real<lower=0>       gr_sigma;
    vector<lower=0>[K]  gr_sd;  // standard dev for all group params

    // Subject-level parameters
    real                alpha[N];
    real                side[N];
    real<lower=0>       sigma[N];

}
model {

    // Priors
    gr_alpha ~ normal(0, 1);
    gr_side ~ normal(0, 1);
    gr_sigma ~ normal(0, 1);
    gr_sd ~ normal(0, 2);

    for (i in 1:N) {
        alpha[i] ~ normal( gr_alpha, gr_sd[1] );
        side[i] ~ normal( gr_side, gr_sd[2] );
        sigma[i] ~ normal( gr_sigma, gr_sd[3] );
    }

    // Likelihood
    for (i in 1:N) {
        Y[i] ~ bernoulli_logit( (delta[i] + info[i] * alpha[i] + side[i]) / sigma[i] );
    }

}