import pandas as pd
import statistics


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
print('pswq')
print(pswq.quantile([0, .25, .5, .75, 1]))
print('ius')
print(ius.quantile([0, .25, .5, .75, 1]))
print('ncs')
print(ncs.quantile([0, .25, .5, .75, 1]))
