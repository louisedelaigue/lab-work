import pandas as pd, numpy as np, seaborn as sns, calkulate as calk
import matplotlib.pyplot as plt
import PyCO2SYS as pyco2
from scipy import stats


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
L = vindta['DIC_vindta'].isnull()
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
# Calculate density for each sample at lab temperature = 23 deg C
df['density'] = calk.density.seawater_1atm_MP81(23, df['salinity'])

# Unit conversion
df['DIC_quaatro_conv'] = df['DIC_quaatro']/df['density']

# === RECALCULATE DIC TO IN-SITU TEMPERATURE
df['DIC_quaatro_insitu'] = pyco2.sys(
    df['TA'],
    df['DIC_quaatro_conv'],
    1,
    2,
    salinity=df['salinity'],
    temperature=23,
    temperature_out=df['temperature'],
    total_phosphate=df['Phosphate'],
    total_silicate=df['Silicate'],
    total_ammonia=df['Ammonium']
    )['dic']

# === COMPARE VINDTA AND QUAATRO DATA
# === PLOTTING
# Prepare figure
sns.set_style('darkgrid')
sns.set_context('paper', font_scale=1)
sns.set(font='Verdana', font_scale=1)

# Create figure
fig, ax = plt.subplots(dpi=300, figsize=(6, 6))

# Linear regression
ax = sns.regplot(x='DIC_quaatro_insitu',
                 y='DIC_vindta',
                 data=df,
                 color='xkcd:blue',
                 label='Linear regression',
                )

# Line through origin
x = [2000, 2300]
y = [2000, 2300]
x_values = [x[0], x[1]]
y_values = [y[0], y[1]]
sns.lineplot(x=x_values,
             y=y_values,
             ax=ax,
             linestyle='--',
             color='black',
             label='Perfect fit',
             )


# Improve figure
xmin = df['DIC_quaatro_insitu'].min() - 10
xmax = df['DIC_quaatro_insitu'].max() + 10
ymin = df['DIC_vindta'].min() - 10
ymax = df['DIC_vindta'].max() + 10
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])

plt.legend()

ax.set_xlabel('$DIC_{QuAAtro}$ / μmol/kg')
ax.set_ylabel('$DIC_{VINDTA}$ / μmol/kg')

# Save plot
plt.savefig('./figs/compare_so279_dic_vindta_quaatro.py.png')

# === STATISTICS
stats = stats.linregress(df['DIC_quaatro_insitu'], df['DIC_vindta'])
