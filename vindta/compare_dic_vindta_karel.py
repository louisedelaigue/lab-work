import pandas as pd, numpy as np, seaborn as sns, calkulate as calk

# === VINDTA DATA
# Import VINDTA DIC values
vindta = pd.read_csv('data/SO279_CTD_discrete_samples.csv', 
                     na_values=-999)

# Rename colums
rn = {
      'Station_ID':'station',
      'Niskin_ID':'niskin',
      'CTDTEMP_ITS90':'temperature',
      'CTDSAL_PSS78':'salinity',
      'DIC':'DIC_vindta'
      }
vindta.rename(rn, axis=1, inplace=True)

# Only keep DIC values that aren't nan
L = vindta['DIC_vindta'] == np.nan
vindta = vindta[~L]

# === QUAATRO DATA
# Import QuAAtro DIC values
quaatro = pd.read_excel('data/210521-LouiseD-DIC.xlsx',
                        skiprows=19)

# Rename and drop useless columns
rn = {
      'Unnamed: 0':'stncode',
      'Unnamed: 2':'DIC_quaatro'
}
quaatro.rename(rn, axis=1, inplace=True)
quaatro.drop(columns=['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 4'], inplace=True)

# Drop nans
quaatro.dropna(inplace=True)

# Convert DIC values to numbers
quaatro['DIC_quaatro'] = pd.to_numeric(quaatro['DIC_quaatro'], errors='coerce')

# Remove useless rows
quaatro = quaatro[~quaatro['stncode'].isin(['DICKSON#186',
                                            'COMM',
                                            'LNSW NUTS',
                                            'METH',
                                            'Sample ID',
                                            'UNIT'])]

# Remove space in sample names
quaatro['stncode'] = quaatro['stncode'].str.replace(' ', '')

# Rename samples
sample_list = quaatro['stncode'].tolist()
sample_names = []

for sample in sample_list:
    if len(sample.split('-')) == 3:
        stn = sample.split('-')[0]
        sample_names.append(sample)
    else:
        sample_names.append(stn + '-' + sample)

quaatro['sample_names'] = sample_names

# Remove useless parts of sample names
quaatro['sample_names'] = quaatro['sample_names'].str.replace('-01', '')
quaatro['sample_names'] = quaatro['sample_names'].str.replace('CTDST', '')

# Split sample names into columns for station and niskin
quaatro['station'] = quaatro['sample_names'].apply(lambda x: x.split("-")[0]).str[-1]
quaatro['niskin'] = quaatro['sample_names'].apply(lambda x: x.split("-")[1])

# Drop useless columns
quaatro.drop(columns=['stncode', 'sample_names'], axis=1, inplace=True)

# Average duplicates
quaatro = quaatro.groupby(by=['station', 'niskin']).mean().reset_index()

# Ensure quaatro contains only numbers
quaatro['station'] = pd.to_numeric(quaatro['station'])
quaatro['niskin'] = pd.to_numeric(quaatro['niskin'])

# === BRING VINDTA AND QUAATRO DATA TOGETHER
df = pd.merge(vindta, quaatro, on=['station', 'niskin'], how='left')

# === CONVERT QUAATRO DIC units from uM/Lto uM/kg
# Calculate density for each sample
df['density'] = calk.density.seawater_1atm_MP81(df['temperature'], df['salinity'])

# === COMPARE VINDTA AND QUAATRO DATA
