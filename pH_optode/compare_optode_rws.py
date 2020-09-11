# run merge_optode_rws.py first
# import toolbox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import data 
datac = pd.read_csv('./data_rws/result_RWS_01_11_comparison.csv',
                   skiprows=[1])
datac = datac.drop(datac.tail(1).index) # systematically drops last CRM

# create new columns to store diff
datac["diff_opt_calc"] = np.nan
datac["diff_opt_spec"] = np.nan
datac["diff_opt_vindta"] = np.nan

datac["diff_opt_calc"] = np.abs(datac["pH_s0_mean"] - datac["pH_calc12_total_20"])
datac["diff_opt_spec"] = np.abs(datac["pH_s0_mean"] - datac["pH_spectro_total_20"])
datac["diff_opt_vindta"] = np.abs(datac["pH_s0_mean"] - datac["pH_vindta_total_20"])

# plot differences
fig, ax = plt.subplots(figsize=(15, 6), dpi=300)
plt.rcParams.update({'font.size': 15})

ax.plot(datac.station, datac.diff_opt_calc, label="pH_opt vs. pH_calc",
        marker='.', markersize=10)
ax.plot(datac.station, datac.diff_opt_spec, label="pH_opt vs. pH_spec",
        marker='.', markersize=10)
ax.plot(datac.station, datac.diff_opt_vindta, label="pH_opt vs. pH_vindta",
        marker='.', markersize=10)

ax.legend(loc='best', facecolor="white", framealpha=1)

ax.axhline(0, c='k', linewidth=0.8)
ax.set_ylim(-0.05, 0.25)

ax.set_ylabel("Difference in pH methods")
ax.set_xlabel("Sample")
plt.xticks(fontsize=13)


plt.tight_layout()