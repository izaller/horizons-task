data {

    // Metadata
    int  N;             // Number of subjects

    // Data
    int        y[N];
    vector[N]  delta;
    vector[N]  info;

}
parameters {

    // Group-level parameters
        //real          group_mu;      // Mean of the group-level variable
        //real<lower=0> group_sd;      // Standard deviation of the group-level variable

    real            group_alpha;  // TODO need to have standard deviations for each of these???
    real            group_side;
    real<lower=0>   group_sigma;


    // Subject-parameters
        //vector[N] beta_pr;           // Subject level coefficients

    vector[N] alpha_pr;
    vector[N] side_pr;
    vector[N] sigma_pr;

}
transformed parameters {

    // In this section, we transform the subject-level parameters from standard normal
    // to a normal distribution with mu = group_mu and sd = group_sd

    vector[N] beta;
    beta = beta_pr * group_sd + group_mu;

    vector[N] alpha;
    alpha = alpha_pr * group_sd + group_alpha; // TODO group mu/sd??

    vector[N] side;
    side = side_pr * group_sd + group_side;

    vector[N] sigma;
    sigma = sigma_pr * group_sd + group_sigma;

}
model {

    // Group-level priors
        // group_mu ~ normal(0, 2);      // Diffuse priors on the group-mean
        // group_sd ~ normal(0, 2);      // Diffuse priors on the group-sd
    group_alpha ~ normal(0, 2);
    group_side ~ normal(0, 2);
    group_sigma ~ normal(0, 2);

    // Subject-level priors
        // beta_pr ~ normal(0, 1);       // Equivalent to: beta ~ normal(group_mu, group_sd)
    alpha_pr ~ normal(0, 1);
    side_pr ~ normal(0, 1);
    sigma_pr ~ normal(0, 1);

    // Likelihood
    y ~ bernoulli_logit((delta + alpha * info  + side) / sigma);
}