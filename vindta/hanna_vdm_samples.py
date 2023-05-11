import numpy as np, pandas as pd
import koolstof as ks, calkulate as calk
from koolstof import vindta as ksv

# Import logfile and dbs file
logfile = ksv.read_logfile("./data/LD_storage_test_TA/logfile.bak", methods="3C standard AT only")
dbs = ks.read_dbs("data/LD_storage_test_TA/LD_storage_test_TA.dbs")

# Only keep HVDM's samples and CRMs
dbs = dbs[dbs["bottle"].apply(lambda x: x.startswith(("H", "CRM")))]

# Drop useless CRMs
dbs = dbs[~dbs["bottle"].apply(lambda x: x.startswith(("CRM-189-", "CRM-195-0114-", "CRM-195-0306-", "CRM-195-0117-")))]

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
dbs.loc[dbs.crm_batch_195, "dic_certified"] = 2024.96  # micromol/kg-sw
dbs.loc[dbs.crm_batch_195, "alkalinity_certified"] = 2213.51  # micromol/kg-sw
dbs.loc[dbs.crm_batch_195, "salinity"] = 33.485
dbs.loc[dbs.crm_batch_195, "total_phosphate"] = 0.49  # micromol/kg-sw
dbs.loc[dbs.crm_batch_195, "total_silicate"] = 3.6  # micromol/kg-sw
dbs.loc[dbs.crm_batch_195, "total_ammonia"] = 0  # micromol/kg-sw

# Assign temperature = 25.0 for VINDTA analysis temperature
dbs["temperature_override"] = 25.0

# Assign salinity to samples
dbs["salinity"] = dbs["salinity"].fillna(28.3)
dbs["total_phosphate"] = dbs["total_phosphate"].fillna(0)
dbs["total_silicate"] = dbs["total_silicate"].fillna(0)
dbs["total_ammonia"] = dbs["total_ammonia"].fillna(0)

# Assign alkalinity metadata
dbs["analyte_volume"] = 95.939  # TA pipette volume in ml
dbs["file_path"] = "data/LD_storage_test_TA/"

# Assign TA acid batches
# Here we consider all samples for HVDM are the same acid batch
dbs["analysis_batch"] = 1 

# Select which TA CRMs to use/avoid for calibration
# Only keep CRMs from day of HVDM"s analysis
dbs["reference_good"] = False #~np.isnan(dbs.alkalinity_certified)
dbs.loc[dbs["bottle"] == "CRM-195-0052-1", "reference_good"] = True
dbs.loc[dbs["bottle"] == "CRM-195-0052-2", "reference_good"] = True
dbs.loc[dbs["bottle"] == "CRM-195-0052-3", "reference_good"] = False
dbs.loc[dbs["bottle"] == "CRM-195-0052-4", "reference_good"] = True

# Calibrate and solve alkalinity and plot calibration
calk.io.get_VINDTA_filenames(dbs)
calk.dataset.calibrate(dbs)
calk.dataset.solve(dbs)
calk.plot.titrant_molinity(
    dbs, figure_fname="figs/HVDM/titrant_molinity.png", show_bad=False
)
calk.plot.alkalinity_offset(
    dbs, figure_fname="figs/HVDM/alkalinity_offset.png", show_bad=False
)

# Demote dbs to a standard DataFrame
dbs = pd.DataFrame(dbs)

# Only keep HVDM samples
L = dbs["bottle"].str.startswith("H")
dbs = dbs[L]

# Sort by sample name
dbs = dbs.sort_values("bottle")

# Only keep useful columns
dbs = dbs[[
    "bottle",
    "salinity",
    "file_name",
    "titrant_molinity",
    "alkalinity"
    ]]

# Save as csv
dbs.to_csv("./data/HVDM_TA_results.csv", index=False)
