import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

anxiety = pd.read_csv('.../data/surveys.csv').copy()
reject = pd.read_csv('.../data/reject.csv')
subjects = anxiety['Subject'].unique()
rejects = reject.query('Reject == 1')['Subject'].tolist()


def getparams(df1, df6):
    alphas_h1 = []
    sides_h1 = []
    sigmas_h1 = []



    alphas_h6 = []
    sides_h6 = []
    sigmas_h6 = []



    return alphas_h1, alphas_h6, sides_h1, sides_h6, sigmas_h1, sigmas_h6

def main():
    filename_1 = 'hierarchical-logistic-1.csv'
    filename_6 = 'hierarchical-logistic-6.csv'
    df1 = pd.read_csv(filename_1)
    df6 = pd.read_csv(filename_6)
    # alphas_h1, alphas_h6, sides_h1, sides_h6, sigmas_h1, sigmas_h6 = get_params(df)
    #
    # fig, (alpha, side, sigma) = plt.subplots(nrows=1, ncols=3, figsize=(17, 4))
    #
    # alpha.bar([1, 2], [mean(alphas_h1), mean(alphas_h6)], tick_label=["Horizon 1", "Horizon 6"],
    #           color=('tab:blue', 'tab:orange'), edgecolor='k')
    # alpha.set(title='Information Parameter', ylabel='average infomation bonus')
    # alpha.axhline(y=0, color='black')
    #
    # side.bar([1, 2], [mean(sides_h1), mean(sides_h6)], tick_label=["Horizon 1", "Horizon 6"],
    #          color=('tab:blue', 'tab:orange'), edgecolor='k')
    # side.set(title='Spatial Parameter', ylabel='average spatial bias')
    #
    # sigma.bar([1, 2], [mean(sigmas_h1), mean(sigmas_h6)], tick_label=["Horizon 1", "Horizon 6"],
    #           color=('tab:blue', 'tab:orange'), edgecolor='k')
    # sigma.set(title='Decision Noise', ylabel='average sigma')
    #
    # plt.tight_layout()
    # plt.savefig(figname)


if __name__ == '__main__':
    main()


