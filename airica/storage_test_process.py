import pandas as pd, numpy as np
from fx_airica_koolstof import process_airica
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt

# Import lab file
db = pd.read_excel('./data/LD_storage_test/AIRICA_storage_test_mod_20012022.xlsx',
                   na_values=-9999)

# Remove nan
L = db['DIC'].isnull()
db = db[~L]

# Ignore data from 27/10/2021 (AIRICA malfunction)
L = db['analysis_batch'] == 3
db = db[~L]

# TEST - Ignore U12
# L = db['name'] == 'U12'
# db = db[~L]

# TEST - Ignore sample CRMS from 20/01/2022
L = db['name'] =="CRM-189-0468-17"
db = db[~L]
L = db['name'] =="CRM-195-0078-25"
db = db[~L]

# Process AIRICA data
results = process_airica(db,
                         './data/LD_storage_test/LD_storage_test_mod_20012022.dbs',
                           './data/LD_storage_test/results_storage_test.csv',
                    )

results.to_csv('./data/LD_storage_test/results.csv', index=False)

# Drop analysis_batch = 5 (AIRICA malfunction)
L = results["analysis_batch"] == 5
results = results[~L]

# === STATISTICS
# Statistics on all replicates
L = results['name'].str.startswith(('R', 'U'))
SE = stats.mstats.sem(results['TCO2'][L], axis=None, ddof=0)
print('Standard error of measurement for all replicates = {}'.format(SE))

# Create table to hold statistics for each analysis batch
batches = list(results['analysis_batch'].unique())
statistics = pd.DataFrame({"batch_number":batches})
statistics['analysis_date'] = np.nan
statistics['n_samples'] = np.nan
statistics['mean_all'] = np.nan
statistics['median_all'] = np.nan
statistics['standard_error_batch'] = np.nan
statistics['standard_error_all_batches'] = np.nan
statistics['mean_R'] = np.nan
statistics['median_R'] = np.nan
statistics['standard_error_batch_R'] = np.nan
statistics['standard_error_all_batches_R'] = np.nan
statistics['mean_U'] = np.nan
statistics['median_U'] = np.nan
statistics['standard_error_batch_U'] = np.nan
statistics['standard_error_all_batches_U'] = np.nan

for batch in batches:
    # Compute overall statistics
    L = ((results['name'].str.startswith(('R', 'U'))) 
         & (results['TCO2'].notnull())
         & (results['analysis_batch']==batch))
    statistics.loc[statistics['batch_number']==batch, 'analysis_date'] = results['datetime'][L].dt.date.iloc[0]
    statistics.loc[statistics['batch_number']==batch, 'n_samples'] = results['TCO2'][L].count()
    statistics.loc[statistics['batch_number']==batch, 'mean_all'] = results['TCO2'][L].mean()
    statistics.loc[statistics['batch_number']==batch, 'median_all'] = results['TCO2'][L].median()
    statistics.loc[statistics['batch_number']==batch, 'standard_error_batch'] = stats.mstats.sem(results['TCO2'][L], axis=None, ddof=0)
    L = (results['name'].str.startswith(('R', 'U'))) & (results['TCO2'].notnull())
    statistics.loc[statistics['batch_number']==batch, 'standard_error_all_batches'] = stats.mstats.sem(results['TCO2'][L], axis=None, ddof=0)
    
    # Compute statistics for R vs. U
    # R
    L = ((results['name'].str.startswith('R')) 
         & (results['TCO2'].notnull())
         & (results['analysis_batch']==batch))
    statistics.loc[statistics['batch_number']==batch, 'mean_R'] = results['TCO2'][L].mean()
    statistics.loc[statistics['batch_number']==batch, 'median_R'] = results['TCO2'][L].median()
    statistics.loc[statistics['batch_number']==batch, 'standard_error_batch_R'] = stats.mstats.sem(results['TCO2'][L], axis=None, ddof=0)
    L = (results['name'].str.startswith(('R'))) & (results['TCO2'].notnull())
    statistics.loc[statistics['batch_number']==batch, 'standard_error_all_batches_R'] = stats.mstats.sem(results['TCO2'][L], axis=None, ddof=0)
    
    # U
    L = ((results['name'].str.startswith('U')) 
    & (results['TCO2'].notnull())
    & (results['analysis_batch']==batch))
    statistics.loc[statistics['batch_number']==batch, 'mean_U'] = results['TCO2'][L].mean()
    statistics.loc[statistics['batch_number']==batch, 'median_U'] = results['TCO2'][L].median()
    statistics.loc[statistics['batch_number']==batch, 'standard_error_batch_U'] = stats.mstats.sem(results['TCO2'][L], axis=None, ddof=0)
    L = (results['name'].str.startswith(('U'))) & (results['TCO2'].notnull())
    statistics.loc[statistics['batch_number']==batch, 'standard_error_all_batches_U'] = stats.mstats.sem(results['TCO2'][L], axis=None, ddof=0)

statistics.to_csv('./data/stats_airica_storage_test.csv', index=False)

# === TIME SINCE SAMPLING COLUMN
results['time_since_sampling'] = np.nan
start_date = pd.to_datetime('2021-09-28', format='%Y-%m-%d')
results['time_since_sampling'] = (results['datetime'] - start_date).dt.days

# === PLOT 3 AREAS
# Create figure
fig, ax = plt.subplots(dpi=300)

# Scatter rinsed samples in dark blue
L = results['name'].str.startswith('R')
sns.scatterplot(y='TCO2',
                 x='time_since_sampling',
                 data=results[L],
                 color='xkcd:blue',
                 label='Rinsed vials',
                 ci=False,
                 ax=ax
                )

# Scatter unrinsed samples in light blue
L = results['name'].str.startswith('U')
sns.scatterplot(y='TCO2',
                 x='time_since_sampling',
                 data=results[L],
                 color='xkcd:fuchsia',
                 label='Unrinsed vials', 
                 ci=False,
                 ax=ax
                )

# Improve figure
ymin = results['TCO2'][L].min() - 2
ymax = results['TCO2'][L].max() + 2
xmin = results['time_since_sampling'].min() - 1
xmax = results['time_since_sampling'].max() + 1
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])

ax.set_ylabel('$TCO_{2}$ / μmol/kg')
ax.set_xlabel('Time since sampling (days)')

ax.grid(alpha=0.3)
plt.tight_layout()

# Save plot
plt.savefig('./figures/storage_test_DIC_3areas.png')