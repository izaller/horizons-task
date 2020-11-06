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

    // Group-level parameters
    vector[K]           mu;
    vector<lower=0>[K]  sigma;

    // Subject-level parameters
    vector[K]  beta[N];

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