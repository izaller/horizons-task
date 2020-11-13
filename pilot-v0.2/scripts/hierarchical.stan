// used by file 'regression-stan.py'

data {

    // Metadata
    int  T;             // Number of subjects

    // Data
    int        y[T];
    vector[T]  delta;
    vector[T]  info;

}
parameters {

    // Group-level parameters
        //real          group_mu;      // Mean of the group-level variable
        //real<lower=0> group_sd;      // Standard deviation of the group-level variable

    real            group_alpha;
    real<lower=0>   alpha_sd;
    real            group_side;
    real<lower=0>   side_sd;
    real<lower=0>   group_sigma;
    real<lower=0>   sigma_sd;


    // Subject-parameters
        //vector[N] beta_pr;           // Subject level coefficients

    real alpha_pr;
    real side_pr;
    real<lower=0> sigma_pr;

}
transformed parameters {

    // In this section, we transform the subject-level parameters from standard normal
    // to a normal distribution with mu = group_mu and sd = group_sd

    // vector[N] beta;
    // beta = beta_pr * group_sd + group_mu;

    real alpha;
    real side;
    real sigma;

    alpha = alpha_pr * alpha_sd + group_alpha; // TODO group mu/sd??
    side = side_pr * side_sd + group_side;
    sigma = sigma_pr * sigma_sd + group_sigma;
}
model {

    // Group-level priors
        // group_mu ~ normal(0, 2);      // Diffuse priors on the group-mean
        // group_sd ~ normal(0, 2);      // Diffuse priors on the group-sd
    group_alpha ~ normal(0, 5);
    group_side ~ normal(0, 2);
    group_sigma ~ normal(0, 1);

    // Subject-level priors
        // beta_pr ~ normal(0, 1);       // Equivalent to: beta ~ normal(group_mu, group_sd)
    alpha_pr ~ normal(0, 1);
    side_pr ~ normal(0, 1);
    sigma_pr ~ normal(0, 1);

    // Likelihood
    y ~ bernoulli_logit((delta + alpha * info + side) / sigma);
}