import numpy as np, pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import seaborn as sns
import koolstof as ks, calkulate as calk
from pandas.tseries.offsets import DateOffset
from scipy import stats

# Import logfile and dbs file
logfile = ks.read_logfile(
    "./data/LD_storage_test_TA/logfile.bak",
    methods=[
        "3C standard AT only"
    ],
)
dbs = ks.read_dbs("data/LD_storage_test_TA/LD_storage_test_TA.dbs", logfile=logfile)

# Remove Hanna's samples
L = dbs["bottle"].str.startswith("H")
dbs = dbs[~L]

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

# === DATE ERRORS
# Modify date error for 06/10/2021
L = ((dbs['analysis_datetime'].dt.day == 2) 
     & (dbs['analysis_datetime'].dt.month == 5) 
     & (dbs['analysis_datetime'].dt.year == 2005) 
     & (dbs['analysis_datetime'].dt.hour < 9))
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'] + DateOffset(hours=10)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'].apply(lambda dt: dt.replace(year=2021, month=10, day=6))

# No date error for 13/10/2021

# # Modify date error for 27/10/2021
october_list = ["J10",
                "J11",
                "J12",
                "J13",
                "J14",
                "J15",
                "CRM-189-0159-1",
                "S48",
                "S71",
                "S51",
                "S13",
                "S75",
                "S93",
                "S49",
                "S24",
                "S99",
                "J16",
                "J17",
                "J18",
                "S40",
                "CRM-189-0159-2",
                "CRM-189-0159-3"
                ]
for sample in october_list:
    L = dbs["bottle"] == sample
    dbs.loc[L, 'analysis_datetime'] = (dbs['analysis_datetime']
                                       .apply(lambda dt: dt.replace(year=2021,
                                                                    month=10,
                                                                    day=27
                                                                    )
                                              )
                                       )

# # Modify date error for 18/11/2021
november_list = ["J20",
                 "J21",
                 "J22",
                 "J23",
                 "CRM-195-0052-1",
                 "S10", 
                 "S43",
                 "S52",
                 "S73",
                 "S27",
                 "S61",
                 "S83",
                 "S85",
                 "S95",
                 "S42",
                 "CRM-195-0052-2",
                 "H08",
                 "H07",
                 "H06",
                 "H05",
                 "H04",
                 "H02",
                 "H03-1",
                 "H01-1",
                 "H01-2",
                 "H01-2",
                 "H03-2",
                 "CRM-195-0052-3",
                 "CRM-195-0052-4"
                 ]

for sample in november_list:
    L = dbs["bottle"] == sample
    dbs.loc[L, 'analysis_datetime'] = (dbs['analysis_datetime']
                                       .apply(lambda dt: dt.replace(year=2021,
                                                                    month=11,
                                                                    day=18
                                                                    )
                                              )
                                       )
# dbs.loc[L, 'analysis_datetime'] = (dbs['analysis_datetime']
#                                    .apply(lambda dt: dt.replace(year=2021,
#                                                                 month=11,
#                                                                 day=18
#                                                                 )
#                                           )
#                                    )

# Reparse datenum
dbs["analysis_datenum"] = mdates.date2num(dbs.analysis_datetime)

# Assign metadata values for CRMs batch 189
prefixes = "CRM-189-"
dbs["crm"] = dbs.bottle.str.startswith("CRM")
dbs["crm_batch_189"] = dbs.bottle.str.startswith(prefixes)
dbs.loc[dbs.crm_batch_189, "dic_certified"] = 2009.48  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "alkalinity_certified"] = 2205.26  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "salinity"] = 33.494
dbs.loc[dbs.crm_batch_189, "total_phosphate"] = 0.45  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_silicate"] = 2.1  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_ammonia"] = 0  # micromol/kg-sw

# Assign metadata values for CRMs batch 195
prefixes = "CRM-195-"
dbs["crm"] = dbs.bottle.str.startswith("CRM")
dbs["crm_batch_195"] = dbs.bottle.str.startswith(prefixes)
dbs.loc[dbs.crm_batch_195, "dic_certified"] = 2024.96 # micromol/kg-sw
dbs.loc[dbs.crm_batch_195, "alkalinity_certified"] = 2213.51  # micromol/kg-sw
dbs.loc[dbs.crm_batch_195, "salinity"] = 33.485
dbs.loc[dbs.crm_batch_195, "total_phosphate"] = 0.49  # micromol/kg-sw
dbs.loc[dbs.crm_batch_195, "total_silicate"] = 3.6  # micromol/kg-sw
dbs.loc[dbs.crm_batch_195, "total_ammonia"] = 0  # micromol/kg-sw

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
# Here we consider each analysis batch has its own acid batch, although 
# first 4 analysis had the same bach made 15/09/2021
# Second acid batch made on 19/01/2022
# // this remedies the acid drift
dbs['analysis_batch'] = 1 # made 15/09/2021
dbs.loc[dbs['analysis_datetime'].dt.day==13, 'analysis_batch'] = 2
dbs.loc[dbs['analysis_datetime'].dt.day==27, 'analysis_batch'] = 3
dbs.loc[dbs['analysis_datetime'].dt.day==18, 'analysis_batch'] = 4
dbs.loc[dbs['analysis_datetime'].dt.day==19, 'analysis_batch'] = 5

# Select which TA CRMs to use/avoid for calibration
dbs["reference_good"] = ~np.isnan(dbs.alkalinity_certified)
dbs.loc[dbs['bottle']=='CRM-189-0159-3', 'reference_good'] = False

# Ignore bad files
dbs['file_good'] = True
dbs.loc[dbs['bottle']=='S20.2', 'file_good'] = False
dbs.loc[dbs['bottle']=='S24', 'file_good'] = False
dbs.loc[dbs['bottle']=='S99', 'file_good'] = False
dbs.loc[dbs['bottle']=='J17', 'file_good'] = False
dbs.loc[dbs['bottle']=='CRM-189-0159-3', 'file_good'] = False
dbs.loc[dbs["bottle"]=="S04", "file_good"] = False
dbs.loc[dbs["bottle"]=="S04_2", "file_good"] = False

# Calibrate and solve alkalinity and plot calibration
calk.io.get_VINDTA_filenames(dbs)
calk.dataset.calibrate(dbs)

# == CONTINUE SOLVING
titrant_molinity_fname = "figs/LD_storage_test_TA/titrant_molinity.png"
alkalinity_offset_fname = "figs/LD_storage_test_TA/alkalinity_offset.png"
calk.dataset.solve(dbs)
calk.plot.titrant_molinity(dbs,
                           figure_fname=titrant_molinity_fname,
                           show_bad=False,
                           xvar="analysis_datenum"
                           )
calk.plot.alkalinity_offset(dbs,
                            figure_fname=alkalinity_offset_fname,
                            show_bad=False
                            )

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
print('Standard error for all replicates = {}'.format(SE))
slope = stats.linregress(dbs[L]["analysis_batch"], dbs[L]["alkalinity"])[0]
print("Slope for all replicates = {}".format(slope))

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
    A = statistics['batch_number']==batch
    statistics.loc[A, 'analysis_date'] = dbs['analysis_datetime'][L].dt.date.iloc[0]
    statistics.loc[A, 'n_samples'] = dbs['alkalinity'][L].count()
    statistics.loc[A, 'mean'] = dbs['alkalinity'][L].mean()
    statistics.loc[A, 'median'] = dbs['alkalinity'][L].median()
    statistics.loc[A, 'standard_error_batch'] = stats.mstats.sem(dbs['alkalinity'][L],
                                                                 axis=None,
                                                                 ddof=0
                                                                 )
    L = (dbs['bottle'].str.startswith('S')) & (dbs['alkalinity'].notnull())
    statistics.loc[A, 'standard_error_all_batches'] = stats.mstats.sem(dbs['alkalinity'][L],
                                                                       axis=None,
                                                                       ddof=0
                                                                       )

statistics.to_csv('./data/stats_vindta.csv', index=False)

# === ISOLATE HANNA'S DATA
# L = dbs.bottle.str.startswith("H")
# hanna = dbs[L]
# hanna_mean = round(hanna.alkalinity.mean(), 2)

# === PLOT
# Create figure
fig, ax = plt.subplots(dpi=300)

# Linear regression
L = (dbs['bottle'].str.startswith('S'))
sns.stripplot(y='alkalinity',
              x='time_since_sampling',
              data=dbs[L],
              color='xkcd:blue',
              jitter=True,
              ax=ax
)

# Improve figure
ymin = round(dbs['alkalinity'][L].min() - 2)
ymax = round(dbs['alkalinity'][L].max() + 2)
plt.ylim([ymin, ymax])

ax.grid(alpha=0.3)

ax.set_ylabel('Alkalinity / $μmol⋅kg^{-1}$')
ax.set_xlabel('Time since sampling (days)')

plt.tight_layout()

# Save plot
plt.savefig('./figs/LD_storage_test_TA/storage_test_TA.png')
