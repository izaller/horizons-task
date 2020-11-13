// model choice probability vs delta

data {

    // Metadata
    int  T;             // Number of trials

    // Data
    int        y[T];
    vector[T]  delta;
    vector[T]  info;

}
parameters {

    real  alpha;
    real  side;
    real  sigma;

}
model {

    // Priors
    alpha ~ normal(0, 1);
    side ~ normal(0, 1);
    sigma ~ normal(5, 1);

    // Likelihood
    y ~ bernoulli_logit((delta + alpha * info  + side) / sigma);

}