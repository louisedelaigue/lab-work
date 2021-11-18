import numpy as np, pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import koolstof as ks, calkulate as calk
from pandas.tseries.offsets import DateOffset
from scipy import stats

# Import logfile and dbs file
logfile = ks.read_logfile(
    "./data/LD_storage_test_TA/logfile.bak",
    methods=[
        "3C standard separator",
        "3C standard separator modified LD",
        "3C standard separator modified LD temp",
        "3C standard AT only"
    ],
)
dbs = ks.read_dbs("data/LD_storage_test_TA/LD_storage_test_TA.dbs", logfile=logfile)

# Create empty metadata columns
for meta in [
    "salinity",
    "dic_certified",
    "alkalinity_certified",
    "total_phosphate",
    "total_silicate",
    "total_ammonia",
]:
    dbs[meta] = np.nan

# Modify date error for 06/10/2021
L = (dbs['analysis_datetime'].dt.day == 2) & (dbs['analysis_datetime'].dt.month == 5) & (dbs['analysis_datetime'].dt.year == 2005) & (dbs['analysis_datetime'].dt.hour < 9)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'] + DateOffset(hours=10)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'].apply(lambda dt: dt.replace(year=2021, month=10, day=6))

# Modify date error for 27/10/2021
L = (dbs['analysis_datetime'].dt.day == 2) & (dbs['analysis_datetime'].dt.month == 5) & (dbs['analysis_datetime'].dt.year == 2005) & (dbs['analysis_datetime'].dt.hour > 9)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'] - DateOffset(hours=10)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'].apply(lambda dt: dt.replace(year=2021, month=10, day=27))
L = (dbs['analysis_datetime'].dt.day == 3) & (dbs['analysis_datetime'].dt.month == 5) & (dbs['analysis_datetime'].dt.year == 2005)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'] - DateOffset(hours=10)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'].apply(lambda dt: dt.replace(year=2021, month=10, day=27))

# Modify date error for 18/11/2021
L = dbs.index >= 54
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'].apply(lambda dt: dt.replace(year=2021, month=11, day=18))

# Assign metadata values for CRMs batch 189
prefixes = ["CRM-189-"]
dbs["crm"] = dbs.bottle.str.startswith("CRM-189")
dbs["crm_batch_189"] = dbs.bottle.str.startswith(tuple(prefixes))
dbs.loc[dbs.crm_batch_189, "dic_certified"] = 2009.48  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "alkalinity_certified"] = 2205.26  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "salinity"] = 33.494
dbs.loc[dbs.crm_batch_189, "total_phosphate"] = 0.45  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_silicate"] = 2.1  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_ammonia"] = 0  # micromol/kg-sw

# Assign metadata values for CRMs batch 189
prefixes = ["CRM-195-"]
dbs["crm"] = dbs.bottle.str.startswith("CRM-195")
dbs["crm_batch_189"] = dbs.bottle.str.startswith(tuple(prefixes))
dbs.loc[dbs.crm_batch_189, "dic_certified"] = 2024.96 # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "alkalinity_certified"] = 2213.51  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "salinity"] = 33.485
dbs.loc[dbs.crm_batch_189, "total_phosphate"] = 0.49  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_silicate"] = 3.6  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_ammonia"] = 0  # micromol/kg-sw

# Assign temperature = 25.0 for VINDTA analysis temperature
dbs["temperature_override"] = 25.0

# Assign salinity to junks and samples
dbs['salinity'] = dbs['salinity'].fillna(35)
dbs['total_phosphate'] = dbs['total_phosphate'].fillna(0)
dbs['total_silicate'] = dbs['total_silicate'].fillna(0)
dbs['total_ammonia'] = dbs['total_ammonia'].fillna(0)

# Assign alkalinity metadata
dbs["analyte_volume"] = 95.939  # TA pipette volume in ml
dbs["file_path"] = "data/LD_storage_test_TA/"

# Assign TA acid batches
dbs['analysis_batch'] = 1 # made 15/09/2021

# Select which TA CRMs to use/avoid for calibration
dbs["reference_good"] = ~np.isnan(dbs.alkalinity_certified)
# dbs.loc[np.isin(dbs.bottle, ["CRM-189-0960-1023-U"]), "reference_good"] = False
dbs.loc[dbs['bottle']=='CRM-189-0159-3', 'reference_good'] = False

# Ignore bad files
dbs['file_good'] = True
dbs.loc[dbs['bottle']=='S20.2', 'file_good'] = False
dbs.loc[dbs['bottle']=='S24', 'file_good'] = False
dbs.loc[dbs['bottle']=='S99', 'file_good'] = False
dbs.loc[dbs['bottle']=='J17', 'file_good'] = False
dbs.loc[dbs['bottle']=='CRM-189-0159-3', 'file_good'] = False

# Calibrate and solve alkalinity and plot calibration
calk.io.get_VINDTA_filenames(dbs)
calk.dataset.calibrate(dbs)
calk.dataset.solve(dbs)
calk.plot.titrant_molinity(dbs, figure_fname="figs/LD_storage_test_TA/titrant_molinity.png", show_bad=False)
calk.plot.alkalinity_offset(dbs, figure_fname="figs/LD_storage_test_TA/alkalinity_offset.png", show_bad=False)

# Demote dbs to a standard DataFrame
dbs = pd.DataFrame(dbs)

# === TIME SINCE SAMPLING COLUMN
dbs['time_since_sampling'] = np.nan
start_date = pd.to_datetime('2021-10-05', format='%Y-%m-%d')
dbs['time_since_sampling'] = (dbs['analysis_datetime'] - start_date).dt.days

# === STATISTICS
# Statistics on all replicates
L = (dbs['bottle'].str.startswith('S')) & (dbs['alkalinity'].notnull())
SE = stats.mstats.sem(dbs['alkalinity'][L], axis=None, ddof=0)
print('Standard error of measurement for all replicates = {}'.format(SE))

# Create stats table per analysis batch
dbs['group'] = 1
dbs.loc[dbs['analysis_datetime'].dt.day==13, 'group'] = 2
dbs.loc[dbs['analysis_datetime'].dt.day==27, 'group'] = 3
dbs.loc[dbs['analysis_datetime'].dt.day==18, 'group'] = 4

batches = list(dbs['group'].unique())
statistics = pd.DataFrame({"batch_number":batches})
statistics['analysis_date'] = np.nan
statistics['n_samples'] = np.nan
statistics['mean'] = np.nan
statistics['median'] = np.nan
statistics['standard_error_batch'] = np.nan
statistics['standard_error_all_batches'] = np.nan

for batch in batches:
    L = ((dbs['bottle'].str.startswith('S')) 
         & (dbs['alkalinity'].notnull())
         & (dbs['group']==batch))
    statistics.loc[statistics['batch_number']==batch, 'analysis_date'] = dbs['analysis_datetime'][L].dt.date.iloc[0]
    statistics.loc[statistics['batch_number']==batch, 'n_samples'] = dbs['alkalinity'][L].count()
    statistics.loc[statistics['batch_number']==batch, 'mean'] = dbs['alkalinity'][L].mean()
    statistics.loc[statistics['batch_number']==batch, 'median'] = dbs['alkalinity'][L].median()
    statistics.loc[statistics['batch_number']==batch, 'standard_error_batch'] = stats.mstats.sem(dbs['alkalinity'][L], axis=None, ddof=0)
    L = (dbs['bottle'].str.startswith('S')) & (dbs['alkalinity'].notnull())
    statistics.loc[statistics['batch_number']==batch, 'standard_error_all_batches'] = stats.mstats.sem(dbs['alkalinity'][L], axis=None, ddof=0)

statistics.to_csv('./data/stats_vindta.csv', index=False)

# === PLOT
# Create figure
fig, ax = plt.subplots(dpi=300)

# Linear regression
L = (dbs['bottle'].str.startswith('S'))
sns.scatterplot(y='alkalinity',
                 x='time_since_sampling',
                 data=dbs[L],
                 color='xkcd:blue'
                )

# Improve figure
ymin = dbs['alkalinity'][L].min() - 2
ymax = dbs['alkalinity'][L].max() + 2
xmin = dbs['time_since_sampling'].min() - 1
xmax = dbs['time_since_sampling'].max() + 1
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])

ax.grid(alpha=0.3)

ax.set_ylabel('Alkalinity / μmol/kg')
ax.set_xlabel('Time since sampling (days)')

plt.tight_layout()

# Save plot
plt.savefig('./figs/LD_storage_test_TA/storage_test_TA.png')
