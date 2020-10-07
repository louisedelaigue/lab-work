# import toolbox
import pandas as pd
import numpy as np

# variables init (to add to fx)
crm_val = 2012.59

# import ".xlsx" file
db = pd.read_excel('./data/Aug_20_Wadden_sea_B1_AIRICA.xlsx',
                   skiprows=[1])
L = db.flag == 2
db = db[L]
db = db.reset_index()

# import ".dbs" file
exec(open("airica_extractdata.py").read())
data = read_dbs("./data/LD_B1.dbs")

# add ".dbs" data to ".xlsx"
sample_list = db["name"].tolist()

db.loc[db["name"]==sample_list, "temperature"] = data.temperature
db.loc[db["name"]==sample_list, "salinity"] = data.salinity
db.loc[db["name"]==sample_list, "density"] = data.density
db.loc[db["name"]==sample_list, "mass_sample"] = data.mass_sample
db.loc[db["name"]==sample_list, "time"] = data.time
db.loc[db["name"]==sample_list, "area_1"] = data.area_1
db.loc[db["name"]==sample_list, "area_2"] = data.area_2
db.loc[db["name"]==sample_list, "area_3"] = data.area_3
db.loc[db["name"]==sample_list, "area_4"] = data.area_4
db.loc[db["name"]==sample_list, "bottle"] = data.bottle

# check that ".dbs" bottle = ".xlsx" name and drop "bottle" column
if db["name"].equals(db["bottle"]):
    print("SUCCESSFUL DBS IMPORT")
    db = db.drop(columns=["bottle"])
else:
    print("ERROR: dbs names don't match xlsx names")

# average areas with all areas and only last 3 areas
db["area_av_4"] = (db.area_1+db.area_2+db.area_3+db.area_4)/4
db["area_av_3"] = (db.area_1+db.area_2+db.area_3)/3

# create columns to hold conversion factor (CF) values
db["CF_3"] = np.nan
db["CF_4"] = np.nan

# calc CRM coeff factor
batch_list = db["analysis_batch"].tolist()
batch_list = list(dict.fromkeys(batch_list))

#%%
def get_CF(db):
    """ Calculate conversion factor CF for each analysis batch."""
    CF_3 = (crm_val*db.density*db.sample_v)/db.area_av_3
    CF_4 = (crm_val*db.density*db.sample_v)/db.area_av_4
    return pd.Series({
    "date": db.analysis_date,
    "analysis_batch": db.analysis_batch,
    "CF_3": CF_3,
    "CF_4": CF_4,
    })

db_cf = db.groupby(by=["analysis_batch"]).apply(get_CF)
