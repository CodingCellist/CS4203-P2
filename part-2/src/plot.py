import sys
import argparse

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument('csv_file', help='The csv-file to plot')
args = parser.parse_args()

# read the file
df = pd.read_csv(args.csv_file, index_col=[0, 1, 2])
# transform the multi-index to get time taken
id_df = df.unstack(level=1)['time (ns)', 'id'].unstack(level=0)
pwd_df = df.unstack(level=1)['time (ns)', 'pwd'].unstack(level=0).dropna()

# enable seaborn for pretty plots
sns.set()
# plot the dfs
id_plt = id_df.plot(title='ID entry')
id_plt.set_xlabel('char no.')
id_plt.set_ylabel('time (ns)')
pwd_plt = pwd_df.plot(title='PWD entry')
pwd_plt.set_xlabel('char no.')
pwd_plt.set_ylabel('time (ns)')
plt.show()
