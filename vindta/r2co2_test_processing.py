import pandas as pd, numpy as np
import copy
import koolstof as ks, calkulate as calk

# Import logfile and dbs file
logfile = ks.read_logfile(
    "data/R2CO2/logfile.bak",
    methods=[
        "3C standard",
    ],
)
dbs = ks.read_dbs("data/R2CO2/testing-2022.dbs", logfile=logfile)

# Assign cell ID
# dbs["dic_cell_id"] = "test"

# Only keep 10 and 11 August 2022
dbs.drop(index=dbs.index[:44], inplace=True)

# Create empty metadata columns
for meta in [
    "salinity",
    "dic_certified",
    "alkalinity_certified",
    "total_phosphate",
    "total_silicate",
    "total_ammonium",
]:
    dbs[meta] = np.nan

# Assign metadata values for CRMs
prefixes = ["CRM-186-"]
dbs["crm"] = dbs.bottle.str.startswith("CRM")
dbs["crm_batch_186"] = dbs.bottle.str.startswith(tuple(prefixes))
dbs.loc[dbs.crm_batch_186, "dic_certified"] = 2012.59  # micromol/kg-sw
dbs.loc[dbs.crm_batch_186, "alkalinity_certified"] = 2212.00  # micromol/kg-sw
dbs.loc[dbs.crm_batch_186, "salinity"] = 33.525
dbs.loc[dbs.crm_batch_186, "total_phosphate"] = 0.42  # micromol/kg-sw
dbs.loc[dbs.crm_batch_186, "total_silicate"] = 3.3 # micromol/kg-sw
dbs.loc[dbs.crm_batch_186, "total_ammonium"] = 0  # micromol/kg-sw

# Assign metadata for junks
dbs["salinity"] = dbs["salinity"].fillna(35)
dbs["total_phosphate"] = dbs["total_phosphate"].fillna(0)
dbs["total_silicate"] = dbs["total_silicate"].fillna(0)
dbs["total_ammonium"] = dbs["total_ammonium"].fillna(0)

# Assign temperature = 25.0 for VINDTA analysis temperature
dbs["temperature_override"] = 25.0

# Add optional column 'file_good'
dbs['file_good'] = True
dbs['k_dic_good'] = True

# Assign alkalinity metadata
dbs["analyte_volume"] = 95.939  # TA pipette volume in ml
dbs["file_path"] = "data/R2CO2/"

# Select which TA CRMs to use/avoid for calibration
dbs["reference_good"] = ~np.isnan(dbs.alkalinity_certified)

# Ignore middle CRM for calibration
dbs.loc[dbs["bottle"]=="CRM-186-0803-01", "reference_good"] = False

# # Add batch columns
dbs.loc[dbs["dic_cell_id"]=="C_Aug_10-22_0908", "analysis_batch"] = 1
dbs.loc[dbs["dic_cell_id"]=="C_Aug_11-22_0708", "analysis_batch"] = 2

# Get blanks and apply correction
dbs.get_blank_corrections()
dbs.plot_blanks(figure_path="figs/R2CO2/dic_blanks/")

dbs.get_standard_calibrations()


# Assign k_dic to other junks
# L = dbs.bottle.str.startswith("CRM")
# dbs.loc[~L, "k_dic"] = 0.010943569450184935
# dbs.loc[~L, "density_analysis_dic"] = 1.02334

# Calibrate DIC and plot calibration
dbs.calibrate_dic()

dbs["dic_self"] = (dbs.counts - dbs.run_time * dbs.blank) * 0.010943569450184935 / 1.02334

dic_sessions = copy.deepcopy(dbs.sessions)
dbs.plot_k_dic(figure_path="figs/R2CO2/")
dbs.plot_dic_offset(figure_path="figs/R2CO2/")

# # Calibrate and solve alkalinity and plot calibration
# calk.io.get_VINDTA_filenames(dbs)
# calk.dataset.calibrate(dbs)
# calk.dataset.solve(dbs)
# calk.plot.titrant_molinity(dbs, figure_fname="figs/R2CO2/titrant_molinity.png", show_bad=False)
# calk.plot.alkalinity_offset(dbs, figure_fname="figs/R2CO2/alkalinity_offset.png", show_bad=False)

# Demote dbs to a standard DataFrame
dbs = pd.DataFrame(dbs)

# Save as csv
dbs.to_csv("./data/R2CO2/r2co2.csv", index=False)
