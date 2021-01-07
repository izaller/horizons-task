import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

meta = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/metadata.csv')

n_sex = meta['Gender-categorical'].value_counts()
p_sex = meta['Gender-categorical'].value_counts(normalize=True)
print('gender')
print(n_sex)
print(p_sex)
print()

n_race = meta['Race'].value_counts()
p_race = meta['Race'].value_counts(normalize=True)
print('race')
print(n_race)
print(p_race)
print()

age = meta['Age'].describe()
print('age')
print(age)
print()

anxiety = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/surveys.csv').copy()
reject = pd.read_csv('/Users/isabelzaller/Desktop/GitHub/horizons-task/pilot-v0.2/data/reject.csv')
subjects = anxiety['Subject'].unique()
rejects = reject.query('Reject == 1')['Subject'].tolist()


# returns sum pswq score for all subjects
def get_pswq():
    pswq_sums = []
    for s in range(len(subjects)):
        sub = subjects[s]
        if sub in rejects:
            continue
        row = anxiety.iloc[s, 6:23]
        # sum anxiety scores for the subject
        pswq_sums.append(sum(row))
    return pswq_sums


# returns sum IUS12 score for all subjects
def get_ius12():
    ius12_sums = []
    for s in range(len(subjects)):
        sub = subjects[s]
        if sub in rejects:
            continue
        row = anxiety.iloc[s, 28:41]
        # sum anxiety scores for the subject
        ius12_sums.append(sum(row))
    return ius12_sums


# returns sum NCS score
    # if fullrow is True, sum across the entire row
    # if fullrow is False, sum only the questions corresponding to decisiveness
def get_ncs(fullrow):
    ncs_sums = []
    for s in range(len(subjects)):
        sub = subjects[s]
        if sub in rejects:
            continue
        row = anxiety.iloc[s, 46:62]
        if not fullrow:
            row = row[6:9]
        # sum anxiety scores for the subject
        ncs_sums.append(sum(row))
    return ncs_sums


def avg(lst):
    return sum(lst) / len(lst)


pswq = pd.Series(get_pswq())
ius = pd.Series(get_ius12())
ncs = pd.Series(get_ncs(fullrow=True))


fig, (pswq_ius, ius_ncs, ncs_pswq) = plt.subplots(nrows=1, ncols=3, sharey='row', figsize=(16, 4))

pswq_ius.plot(pswq, ius, 'o')   ## 1
ius_ncs.plot(pswq, ncs, 'o')    ## 2
ncs_pswq.plot(ncs, pswq, 'o')   ## 3

print(stats.spearmanr(pswq, ius))
print(stats.spearmanr(ius, ncs))
print(stats.spearmanr(ncs, pswq))

# rho_1, p1 = stats.spearmanr(pswq, ius)
# rho_2, p2 = stats.spearmanr(ius, ncs)
# rho_3, p3 = stats.spearmanr(ncs, pswq)

fig.suptitle('Anxiety questionnaire correlations')
pswq_ius.set(title='PSWQ vs. IUS-12')
ius_ncs.set(title='IUS-12 vs. NCS')
ncs_pswq.set(title='NCS vs. PSWQ')
fig.tight_layout(pad=2.5)

# corr = '''Spearman correlations
    #             H1: rho = %f, p = %f
    #             H6: rho = %f, p = %f''' % (rho_1, p1, rho_6, p6)
    # alpha1.set(title='Horizon 1', xlabel='%s score' % test, ylabel='Information bonus')
    # alpha6.set(title='Horizon 6', xlabel='%s score' % test)
    # fig1.suptitle('%s score vs. information bonus' % test, fontsize=16)
    # fig1.text(.5, 0.01, corr, ha='center', fontsize=8)
    # fig1.tight_layout(pad=2.5)
    # fig1.savefig(figname + '-alpha.png')

# pswq_mean = avg(pswq)
# pswq_sd = statistics.stdev(pswq)
#
# ius_mean = avg(ius)
# ius_sd = statistics.stdev(ius)
#
# ncs_mean = avg(ncs)
# ncs_sd = statistics.stdev(ncs)
#
# print('pswq mean: %d' % pswq_mean)
# print('ius-12 mean: %d' % ius_mean)
# print('ncs mean: %d' % ncs_mean)
# print('pswq')
# print(pswq.quantile([0, .25, .5, .75, 1]))
# print('ius')
# print(ius.quantile([0, .25, .5, .75, 1]))
# print('ncs')
# print(ncs.quantile([0, .25, .5, .75, 1]))
