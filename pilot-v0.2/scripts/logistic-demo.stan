data {

    // Metadata
    int  T;             // Number of trials

    // Data
    int        y[T];
    vector[T]  x;

}
parameters {

    real  b0;
    real  b1;

}
model {

    // Priors
    b0 ~ normal(0, 1);
    b1 ~ normal(0, 1);

    // Likelihood
    y ~ bernoulli_logit( b0 + b1 * x );

}