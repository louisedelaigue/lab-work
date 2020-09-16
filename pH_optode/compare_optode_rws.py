# run merge_optode_rws.py first
# import toolbox
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# import data 
datac = pd.read_csv('./results/rws_1609_comparison.csv',
                   skiprows=[1])
#datac = datac.drop(datac.tail(1).index) # systematically drops last CRM

# replace nan by "CRM" for station/bottle columns
datac.bottle.replace(np.nan, 'CRM', regex=True, inplace=True)
datac.station.replace(np.nan, 'CRM', regex=True, inplace=True)

# create name column
datac.bottle = datac.bottle.astype(str)
datac["name"] = datac["station"] +"_"+ datac["bottle"]

# create new columns to store diff
datac["diff_opt_calc"] = np.nan
datac["diff_opt_spec"] = np.nan
datac["diff_opt_vindta"] = np.nan

datac["diff_opt_calc"] = datac["pH_s0_mean"] - datac["pH_calc12_total_20"]
datac["diff_opt_spec"] = datac["pH_s0_mean"] - datac["pH_spectro_total_20"]
datac["diff_opt_vindta"] = datac["pH_s0_mean"] - datac["pH_vindta_total_20"]

# remove CRM and outlier
indexCRM = datac[datac["name"] == "CRM_CRM"].index
datac.drop(indexCRM, inplace = True)
indexO = datac[datac["name"] == "WALCRN20_2020005960.0"].index
datac.drop(indexO, inplace = True)

#%% scatterplot
f, ax = plt.subplots(1, 3, figsize=(20, 6.5))
sns.set_style("darkgrid")
sns.set_context("paper")
sns.set(font="Verdana")
sns.despine(f, left=True, bottom=True)

# line through origin
x = [7.70, 7.70]
y = [8.20, 8.20]
x_values = [x[0], y[0]]
y_values = [x[1], y[1]]

sns.lineplot(x=x_values, y=y_values, ax=ax[0], color="black")
sns.lineplot(x=x_values, y=y_values, ax=ax[1], color="black")
sns.lineplot(x=x_values, y=y_values, ax=ax[2], color="black")

sns.scatterplot(x="pH_s0_mean", y="pH_calc12_total_20", 
                hue="diff_opt_calc",  s=120,
                palette="ch:r=-.2,d=.3_r", data=datac, ax=ax[0])
sns.scatterplot(x="pH_s0_mean", y="pH_spectro_total_20", 
                hue="diff_opt_spec", s=120,
                palette="ch:r=-.2,d=.3_r", data=datac, ax=ax[1])
sns.scatterplot(x="pH_s0_mean", y="pH_vindta_total_20", 
                hue="diff_opt_vindta", s=120,
                palette="ch:r=-.2,d=.3_r", data=datac, ax=ax[2])

plt.tight_layout()
