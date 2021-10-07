import numpy as np, pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import koolstof as ks, calkulate as calk
from pandas.tseries.offsets import DateOffset
from scipy import stats

# Import logfile and dbs file
logfile = ks.read_logfile(
    "data/LD_storage_test_TA/logfile.bak",
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
L = (dbs['analysis_datetime'].dt.day == 2) & (dbs['analysis_datetime'].dt.month == 5) & (dbs['analysis_datetime'].dt.year == 2005)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'] + DateOffset(hours=10)
dbs.loc[L, 'analysis_datetime'] = dbs['analysis_datetime'].apply(lambda dt: dt.replace(year=2021, month=10, day=6))

# Assign metadata values for CRMs
prefixes = ["CRM-189-"]
dbs["crm"] = dbs.bottle.str.startswith("CRM")
dbs["crm_batch_189"] = dbs.bottle.str.startswith(tuple(prefixes))
dbs.loc[dbs.crm_batch_189, "dic_certified"] = 2009.48  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "alkalinity_certified"] = 2205.26  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "salinity"] = 33.494
dbs.loc[dbs.crm_batch_189, "total_phosphate"] = 0.45  # micromol/kg-sw
dbs.loc[dbs.crm_batch_189, "total_silicate"] = 2.1  # micromol/kg-sw
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
dbs['analysis_batch'] = 1

# Select which TA CRMs to use/avoid for calibration
dbs["reference_good"] = ~np.isnan(dbs.alkalinity_certified)
# dbs.loc[np.isin(dbs.bottle, ["CRM-189-0960-1023-U"]), "reference_good"] = False

# Calibrate and solve alkalinity and plot calibration
calk.io.get_VINDTA_filenames(dbs)
calk.dataset.calibrate(dbs)
calk.dataset.solve(dbs)
calk.plot.titrant_molinity(dbs, figure_fname="figs/LD_storage_test_TA/titrant_molinity.png", show_bad=False)
calk.plot.alkalinity_offset(dbs, figure_fname="figs/LD_storage_test_TA/alkalinity_offset.png", show_bad=False)

# Demote dbs to a standard DataFrame
dbs = pd.DataFrame(dbs)

# === STATISTICS
# Statistics on sample replicates
L = dbs['bottle'].str.startswith('S')
replicates = dbs[L]

# Print standard error of the mean
variable = 'alkalinity'
SE = stats.mstats.sem(replicates[variable], axis=None, ddof=0)
print('Standard error of measurement for all replicates = {}'.format(SE))

# === PLOT
# Prepare figure
sns.set_style('darkgrid')
sns.set_context('paper', font_scale=1)
sns.set(font='Verdana', font_scale=1)

# Create figure
fig, ax = plt.subplots(dpi=300, figsize=(7, 6))

# Linear regression
L = dbs['bottle'].str.startswith('S')
sns.regplot(y='alkalinity',
                 x='analysis_datenum',
                 data=dbs[L],
                 color='xkcd:blue',
                 ci=False,
                 ax=ax
                )

# Improve figure
ymin = dbs['alkalinity'][L].min() - 2
ymax = dbs['alkalinity'][L].max() + 2
xmin = dbs['analysis_datenum'][L].min() - 0.01
xmax = dbs['analysis_datenum'][L].max() + 0.01
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])

# plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off
#     top=False,         # ticks along the top edge are off
#     labelbottom=False) # labels along the bottom edge are off

ax.set_ylabel('Alkalinity / μmol/kg')
ax.set_xlabel('Time')

plt.tight_layout()

# Save plot
plt.savefig('./figs/LD_storage_test_TA/storage_test_TA.png')

