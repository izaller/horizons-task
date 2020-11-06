data {

    // Metadata
    int  N;                  // Number of subjects
    int  K;                  // Number of regressors (params per subject that we're trying to fit)
    int  T;                  // Number of trials (per participant)

    // Data
    matrix[T,K]  X;          // Design matrix
    int          Y[N,T];     // Choice data
    int          info[N,T];  // info
    int          delta[N,T]; // delta

}
parameters {

    // Group-level parameters
    vector[K]           mu;      // mu[0], mu[1], mu[2]
    vector<lower=0>[K]  sigma;

    // Subject-level parameters
    vector[K]           beta[N]; // beta[0], beta[1], beta[2] = alpha, side, sigma


}
model {

    // Priors
    mu ~ normal(0, 1);
    sigma ~ normal(0, 2);

    for (i in 1:N) {
        beta[i] ~ normal( mu, sigma );
    }

    // Likelihood
    Y ~ bernoulli_logit( (delta + info * beta[0] + beta[1]) / beta[2]

}