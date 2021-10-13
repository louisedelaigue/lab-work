import pandas as pd

# Import dbs
dbs_cheat = pd.read_csv('data/LPS/laura_pacho_150921_data.dbs',
                  delimiter='\s')

# dbs_cheat = dbs_cheat.replace('red (1)', 'red')

dbs_cheat = dbs_cheat.drop(['(1)'], axis=1)

# Add headers
columns_list = [
    'run type',
    'bottle',
    'station',
    'cast',
    'niskin',
    'depth',
    'i.s. temperature',
    'salinity',
    'counts',
    'run time',
    'CT',
    'factor CT',
    'blank',
    'TCT',
    'last CRM CT',
    'cert. CRM CT',
    'last CRM AT',
    'cert. CRM AT',
    'batch',
    'AT',
    'factor AT',
    'rms',
    'calc ID',
    'Titrino',
    'sample line',
    'pip vol',
    'comment',
    'Lat.',
    'Long.',
    'date',
    'time',
    'cell ID',
    ]

# Assign columns to dbs
dbs_cheat.columns = columns_list

# Save dbs to csv
dbs_cheat.to_csv('data/LPS/LPS_dbs_complete.dbs')
