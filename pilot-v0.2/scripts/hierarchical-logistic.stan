data {

    // Metadata
    int  N;                 // Number of subjects
    int  K;                 // Number of regressors
    int  T;                 // Number of trials

    // Data
    matrix[T,K]  X;         // Design matrix
    int          Y[N,T];    // Choice data


}
parameters {

    // Group-level parameters
    vector[K]           mu;
    vector<lower=0>[K]  sigma;

    // Subject-level parameters
    vector[K]           beta[N];

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

        Y[i] ~ bernoulli_logit( X * beta[i] );

    }

}