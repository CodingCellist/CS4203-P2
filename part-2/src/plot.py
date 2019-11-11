import argparse

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument('csv_file', help='The csv-file to plot')
parser.add_argument('--sem', action='store_true',
                    help='aggregate the samples and plot SEM along with the average')
args = parser.parse_args()

# enable seaborn for pretty plots
sns.set(style='darkgrid')

# read the file
if args.sem:
    df = pd.read_csv(args.csv_file)
    # filter based on input-type
    id_df = df.loc[df['input-type'] == 'id']
    pwd_df = df.loc[df['input-type'] == 'pwd']
    # plot the dfs with standard error (ci=68)
    id_plt = sns.lineplot(x='char-no', y='time (ns)', data=id_df, ci=68,
                          marker='o')
    plt.figure()
    pwd_plt = sns.lineplot(x='char-no', y='time (ns)', data=pwd_df, ci=68,
                           marker='o')
else:
    df = pd.read_csv(args.csv_file, index_col=[0, 1, 2])
    # transform the multi-index to get time taken; dropna fixes the case where
    # len(id) != len(pwd)
    id_df = df.unstack(level=1)['time (ns)', 'id'].unstack(level=0).dropna()
    pwd_df = df.unstack(level=1)['time (ns)', 'pwd'].unstack(level=0).dropna()
    # plot the dfs
    id_plt = id_df.plot()
    pwd_plt = pwd_df.plot()

# configure title and labels
id_plt.set_title(args.csv_file[:-4] + ' - ID entry')
id_plt.set_xlabel('char no.')
id_plt.set_ylabel('time (ns)')
pwd_plt.set_title(args.csv_file[:-4] + ' - PWD entry')
pwd_plt.set_xlabel('char no.')
pwd_plt.set_ylabel('time (ns)')
plt.show()
