# import toolbox
import pandas as pd
import numpy as np

# variables init (to add to fx)
crm_val = 2012.59

# import ".xlsx" file
db = pd.read_excel("./data/Aug_20_Wadden_sea_B1_AIRICA.xlsx", skiprows=[1])
L = db.flag == 2
db = db[L]
db = db.reset_index()

# import ".dbs" file
exec(open("airica_extractdata.py").read())
data = read_dbs("./data/LD_B1.dbs")

# add ".dbs" data to ".xlsx"
sample_list = db["name"].tolist()

db.loc[db["name"] == sample_list, "temperature"] = data.temperature
db.loc[db["name"] == sample_list, "salinity"] = data.salinity
db.loc[db["name"] == sample_list, "density"] = data.density
db.loc[db["name"] == sample_list, "mass_sample"] = data.mass_sample
db.loc[db["name"] == sample_list, "time"] = data.time
db.loc[db["name"] == sample_list, "area_1"] = data.area_1
db.loc[db["name"] == sample_list, "area_2"] = data.area_2
db.loc[db["name"] == sample_list, "area_3"] = data.area_3
db.loc[db["name"] == sample_list, "area_4"] = data.area_4
db.loc[db["name"] == sample_list, "bottle"] = data.bottle

# check that ".dbs" bottle = ".xlsx" name and drop "bottle" column
if db["name"].equals(db["bottle"]):
    print("SUCCESSFUL DBS IMPORT")
    db = db.drop(columns=["bottle"])
else:
    KeyError
    print("ERROR: mismatch between dbs and xlsx files")

# average areas with all areas and only last 3 areas
db["area_av_4"] = (db.area_1 + db.area_2 + db.area_3 + db.area_4) / 4
db["area_av_3"] = (db.area_2 + db.area_3 + db.area_4) / 3

# create columns to hold conversion factor (CF) values
db["CF_3"] = np.nan
db["CF_4"] = np.nan

# calc CRM coeff factor
def get_CF(db):
    """Calculate conversion factor CF for each analysis batch."""
    db.CF_3 = (crm_val * db.density * db.sample_v) / db.area_av_3
    db.CF_4 = (crm_val * db.density * db.sample_v) / db.area_av_4
    CF_3f = db.loc[db["location"] == "CRM", "CF_3"].mean()
    CF_4f = db.loc[db["location"] == "CRM", "CF_4"].mean()
    return pd.Series(
        {
            "CF_3f": CF_3f,
            "CF_4f": CF_4f,
        }
    )


db_cf = db.groupby(by=["analysis_batch"]).apply(get_CF)

# assign a CRM CF to samples based on analysis batch
db["CF_3"] = db_cf.loc[db.analysis_batch.values, "CF_3f"].values
db["CF_4"] = db_cf.loc[db.analysis_batch.values, "CF_4f"].values

# calculate TCO2 values
db["TCO2_3"] = np.nan
db["TCO2_4"] = np.nan

db["TCO2_3"] = (db.CF_3 * db.area_av_3) / (db.density * db.sample_v)
db["TCO2_4"] = (db.CF_4 * db.area_av_4) / (db.density * db.sample_v)
