# import toolbox
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# run other scripts
exec(open("fx_ph_optode.py").read())
exec(open("merge_optode_rws.py").read())

# import data 
datac = pd.read_csv('./results/results_rws_comparison.csv',
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

# remove CRM and outliers (according to lab flags)
indexCRM = datac[datac["name"] == "CRM_CRM"].index
datac.drop(indexCRM, inplace = True)
L = (datac.flag == 2)
datac = datac[L]

#%% scatterplot all method different subplots
f, ax = plt.subplots(1, 3, figsize=(20, 6.5), dpi=300)
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=2)
sns.set(font="Verdana", font_scale=1)
sns.despine(f, left=True, bottom=True)

# line through origin
x = [7.70, 7.70]
y = [8.20, 8.20]
x_values = [x[0], y[0]]
y_values = [x[1], y[1]]

# scattering
ax1 = sns.lineplot(x=x_values, y=y_values, ax=ax[0], color="black")
ax2 = sns.lineplot(x=x_values, y=y_values, ax=ax[1], color="black")
ax3 = sns.lineplot(x=x_values, y=y_values, ax=ax[2], color="black")

sns.scatterplot(x="pH_s0_mean", y="pH_calc12_total_20", palette = "cool",
                hue="diff_opt_calc", s=150, data=datac, ax=ax[0])
sns.scatterplot(x="pH_s0_mean", y="pH_spectro_total_20", palette = "cool",
                hue="diff_opt_spec", s=150, data=datac, ax=ax[1])
sns.scatterplot(x="pH_s0_mean", y="pH_vindta_total_20", palette = "cool",
                hue="diff_opt_vindta", s=150, data=datac, ax=ax[2])

# axis labels
ax1.set_xlabel("$pH_{optode}$ @ 20°C")
ax2.set_xlabel("$pH_{optode}$ @ 20°C")
ax3.set_xlabel("$pH_{optode}$ @ 20°C")
ax1.set_ylabel("$pH_{calc}$ @ 20°C")
ax2.set_ylabel("$pH_{spectro}$ @ 20°C")
ax3.set_ylabel("$pH_{VINDTA}$ @ 20°C")

# legend 
for ax in ax:
    L = ax.legend()
    L.get_texts()[0].set_text("Difference")

plt.tight_layout()

# save plot
plt.savefig('./figures/scatter_all_methods.png', format = 'png')
plt.show()

#%% scatterplot all methods on same plot per station
f, ax = plt.subplots(figsize=(20, 6.5), dpi=300)
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=2)
sns.set(font="Verdana", font_scale=1)
sns.despine(f, left=True, bottom=True)

# sort by station
datac = datac.sort_values(by = "name")

# vertical line at diff = 0
ax.axhline(y=0, linewidth=3, color='xkcd:black')

# plotting
ax1 = ax.plot(datac.name, datac.diff_opt_calc, c="xkcd:cyan", linewidth=3,
              label="$∆pH_{calc}$", marker="o")
ax2 = ax.plot(datac.name, datac.diff_opt_spec,  c="xkcd:fuchsia", linewidth=3,
              label = "$∆pH_{spectro}$", marker="o")
ax3 = ax.plot(datac.name, datac.diff_opt_vindta, c="xkcd:blue violet",
              linewidth=3, label = "$∆pH_{VINDTA}$",  marker="o")

# axis labels
plt.xticks(rotation=90)
ax.set_ylabel("∆pH")

# legend
ax.legend()

plt.tight_layout()

# save plot
plt.savefig('./figures/plot_diff_stations.png', format = 'png')
plt.show()

#%% scatter diff through time
# prep data
day1 = "2020-10-09 00:00:00"
day2 = "15/09/2020"
day3 = "16/09/2020"

# prep plot
f, ax = plt.subplots(1, 3, figsize=(20, 6.5), dpi=300)
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=2)
sns.set(font="Verdana", font_scale=1)
sns.despine(f, left=True, bottom=True)

# linear regression
ax1 = sns.regplot(datac.index[datac.analysis_date == day1],
                  datac.diff_opt_calc[datac.analysis_date == day1],
                  fit_reg=True, marker='o', label="$∆pH_{calc}$",
                  color="xkcd:cyan", ci=None, ax=ax[0])
sns.regplot(datac.index[datac.analysis_date == day1],
                  datac.diff_opt_spec[datac.analysis_date == day1],
                  fit_reg=True, marker='o', label = "$∆pH_{spectro}$",
                  color="xkcd:fuchsia", ci=None, ax=ax[0])
sns.regplot(datac.index[datac.analysis_date == day1],
                  datac.diff_opt_vindta[datac.analysis_date == day1],
                  fit_reg=True, marker='o', label = "$∆pH_{VINDTA}$",
                  color="xkcd:blue violet", ci=None, ax=ax[0])

ax2 = sns.regplot(datac.index[datac.analysis_date == day2],
                  datac.diff_opt_calc[datac.analysis_date == day2],
                  fit_reg=True, marker='o', label="$∆pH_{calc}$",
                  color="xkcd:cyan", ci=None, ax=ax[1])
sns.regplot(datac.index[datac.analysis_date == day2],
                  datac.diff_opt_spec[datac.analysis_date == day2],
                  fit_reg=True, marker='o', label = "$∆pH_{spectro}$",
                  color="xkcd:fuchsia", ci=None, ax=ax[1])
sns.regplot(datac.index[datac.analysis_date == day2],
                  datac.diff_opt_vindta[datac.analysis_date == day2],
                  fit_reg=True, marker='o', label = "$∆pH_{VINDTA}$",
                  color="xkcd:blue violet", ci=None, ax=ax[1])

ax3 = sns.regplot(datac.index[datac.analysis_date == day3],
                  datac.diff_opt_calc[datac.analysis_date == day3],
                  fit_reg=True, marker='o', label="$∆pH_{calc}$",
                  color="xkcd:cyan", ci=None, ax=ax[2])
sns.regplot(datac.index[datac.analysis_date == day3],
                  datac.diff_opt_spec[datac.analysis_date == day3],
                  fit_reg=True, marker='o', label = "$∆pH_{spectro}$",
                  color="xkcd:fuchsia", ci=None, ax=ax[2])
sns.regplot(datac.index[datac.analysis_date == day3],
                  datac.diff_opt_vindta[datac.analysis_date == day3],
                  fit_reg=True, marker='o', label = "$∆pH_{VINDTA}$",
                  color="xkcd:blue violet", ci=None, ax=ax[2])

# vertical line at diff = 0
for ax in ax:
    ax.axhline(y=0, linewidth=2, color='xkcd:black')

# axis limits
ax1.set_ylim([-0.035, 0.015])
ax2.set_ylim([-0.035, 0.015])
ax3.set_ylim([-0.035, 0.015])

# axis labels
ax1.set_xlabel("Time")
ax2.set_xlabel("Time")
ax3.set_xlabel("Time")
ax1.set_ylabel("∆pH @ 20°C")
ax2.set_ylabel("∆pH @ 20°C")
ax3.set_ylabel("∆pH @ 20°C")
ax1.title.set_text("Day 1")
ax2.title.set_text("Day 2")
ax3.title.set_text("Day 3")
ax1.xaxis.set_ticklabels([])
ax2.xaxis.set_ticklabels([])
ax3.xaxis.set_ticklabels([])

# legend
ax1.legend(loc="lower left")
ax2.legend(loc="lower left")
ax3.legend(loc="lower left")

plt.tight_layout()

# save plot
plt.savefig('./figures/diff_vs_time.png', format = 'png')
plt.show()