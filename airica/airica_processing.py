# import toolbox
import pandas as pd
import numpy as np
from matplotlib import dates as mdates
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# run other scripts
exec(open("airica_extractdata.py").read())
data = read_dbs("./data/LD_B1.dbs")

# import spreadsheet
db = pd.read_excel('./data/Aug_20_Wadden_sea_B1_AIRICA.xlsx',
                   skiprows=[1])
L = db.flag == 2
db = db[L]
db = db.reset_index()

# create a list of samples and import data info to db
# create list 
sample_list = db["name"].tolist()

# import area values to db
db.loc[db["name"]==sample_list, "area1"] = data.area_1
db.loc[db["name"]==sample_list, "area2"] = data.area_2
db.loc[db["name"]==sample_list, "area3"] = data.area_3
db.loc[db["name"]==sample_list, "area4"] = data.area_4

# create new columns to hold rest of info from dbs file
db["salinity"] = np.nan
db["density"] = np.nan
db["mass_sample"] = np.nan
db["temperature"] = np.nan
db["dic"] = np.nan
db["time"] = np.nan
db.loc[db["name"]==sample_list, "salinity"] = data.salinity
db.loc[db["name"]==sample_list, "density"] = data.density
db.loc[db["name"]==sample_list, "mass_sample"] = data.mass_sample
db.loc[db["name"]==sample_list, "temperature"] = data.temperature
db.loc[db["name"]==sample_list, "dic"] = data.dic
db.loc[db["name"]==sample_list, "time"] = data.time

#%% calculate conversion factor coeff for CRM
# k = (DIC*density*volume)/area
# isolate CRMs from db and only keep columns of interest to calc k
crm_val = 2012.59
crms = pd.DataFrame()
crms["analysis_date"] = db.analysis_date
crms["name"] = db.name
crms["density"] = db.density
crms["sample_v"] = db.sample_v
crms["area1"] = db.area1
crms["area2"] = db.area2
crms["area3"] = db.area3
crms["area4"] = db.area4
crms["area_av_4"] = (crms.area1+crms.area2+crms.area3+crms.area4)/4
crms["area_av_3"] = (crms.area2+crms.area3+crms.area4)/3
crms["k4"] = (crm_val*crms.density*crms.sample_v)/crms.area_av_4
crms["k3"] = (crm_val*crms.density*crms.sample_v)/crms.area_av_3
crms["DIC_p_v"] = crm_val*crms.density*crms.sample_v
crms["slope_k4"] = stats.linregress(crms.DIC_p_v, crms.area_av_4)[0]  
crms["slope_k3"] = stats.linregress(crms.DIC_p_v, crms.area_av_3)[0]  

# split CRMS into day db
crms = crms[crms.name.str.contains("CRM",case=False)]
crmsd1 = crms[crms.analysis_date.str.contains("22/09/2020",case=False)]
crmsd12 = crms[crms.analysis_date.str.contains("23/09/2020",case=False)]

# plot CRMS dic_p_v vs area_3 or area_4
f, ax = plt.subplots(figsize=(20, 6.5), dpi=300)
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=1)
sns.set(font="Verdana", font_scale=1)
sns.despine(f, left=True, bottom=True)

# line through origin
x = [3000000, 28000]
y = [4600000, 43000]
x_values = [x[0], y[0]]
y_values = [x[1], y[1]]

# scattering
sns.lineplot(x=x_values, y=y_values, ax=ax, color="black")

sns.regplot(x="DIC_p_v", y="area_av_4", data=crmsd1, ci=None, label="4 areas",
               color="xkcd:neon green", ax=ax)
sns.regplot(x="DIC_p_v", y="area_av_3", data=crmsd1, ci=None, label="3 areas",
               color="xkcd:bright blue", ax=ax)

ax.legend()
plt.tight_layout()