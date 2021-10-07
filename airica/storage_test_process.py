import pandas as pd
from fx_airica import process_airica
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt

# Import lab file
db = pd.read_excel('./data/LD_storage_test/AIRICA_storage_test.xlsx',
                   na_values=-9999)

# Only keep flag = 2
L = db['flag'] == 2
db = db[L]

# Process AIRICA data
results = process_airica(2009.48, 
                         db,
                         './data/LD_storage_test/LD_storage_test.dbs',
                         './data/LD_storage_test/results_storage_test.csv'
                    )

# === STATISTICS
# Statistics on replicates
L = results['name'].str.startswith(('R', 'U'))
replicates = results[L]

# Print standard error of the mean
variable = 'TCO2_3'
SE = stats.mstats.sem(replicates[variable], axis=None, ddof=0)
print('Standard error of measurement for all replicates = {}'.format(SE))

# Print standard error of the mean for R and U
L = replicates['name'].str.startswith('R')
rinsed = replicates[L]
L = replicates['name'].str.startswith('U')
unrinsed = replicates[L]

SE_R = stats.mstats.sem(rinsed[variable], axis=None, ddof=0)
print('Standard error of measurement for rinsed replicates = {}'.format(SE_R))

SE_U = stats.mstats.sem(unrinsed[variable], axis=None, ddof=0)
print('Standard error of measurement for unrinsed replicates = {}'.format(SE_U))

# === PLOT 4 AREAS
# Prepare figure
sns.set_style('darkgrid')
sns.set_context('paper', font_scale=1)
sns.set(font='Verdana', font_scale=1)

# Create figure
fig, ax = plt.subplots(dpi=300, figsize=(7, 6))

# Scatter rinsed samples in dark blue
L = results['name'].str.startswith('R')
sns.scatterplot(y='TCO2_4',
                 x='datenum',
                 data=results[L],
                 color='xkcd:blue',
                 label='Rinsed vials',
                 ci=False,
                 ax=ax
                )

# Scatter unrinsed samples in light blue
L = results['name'].str.startswith('U')
sns.scatterplot(y='TCO2_4',
                 x='datenum',
                 data=results[L],
                 color='xkcd:fuchsia',
                 label='Unrinsed vials',
                 ci=False,
                 ax=ax
                )

# Improve figure
ax.set_ylabel('$DIC_{4 areas}$ / μmol/kg')
ax.set_xlabel('Time')

plt.tight_layout()

# Save plot
plt.savefig('./figures/storage_test_DIC_4areas.png')

# === PLOT 3 AREAS
# Prepare figure
sns.set_style('darkgrid')
sns.set_context('paper', font_scale=1)
sns.set(font='Verdana', font_scale=1)

# Create figure
fig, ax = plt.subplots(dpi=300, figsize=(7, 6))

# Scatter rinsed samples in dark blue
L = results['name'].str.startswith('R')
sns.scatterplot(y='TCO2_3',
                 x='datenum',
                 data=results[L],
                 color='xkcd:blue',
                 label='Rinsed vials',
                 ci=False,
                 ax=ax
                )

# Scatter unrinsed samples in light blue
L = results['name'].str.startswith('U')
sns.scatterplot(y='TCO2_3',
                 x='datenum',
                 data=results[L],
                 color='xkcd:fuchsia',
                 label='Unrinsed vials', 
                 ci=False,
                 ax=ax
                )

# Improve figure
plt.legend()
ax.set_ylabel('$DIC_{3 areas}$ / μmol/kg')
ax.set_xlabel('Time')

plt.tight_layout()

# Save plot
plt.savefig('./figures/storage_test_DIC_3areas.png')