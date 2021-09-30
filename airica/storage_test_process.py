import pandas as pd
from fx_airica import process_airica
from scipy import stats

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

# Statistics on replicates
L = results['name'].str.startswith(('R', 'U'))
replicates = results[L]

# Print standard error of the mean
variable = 'TCO2_4'
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

