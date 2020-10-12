# import toolbox
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from scipy import stats

# import data
exec(open("fx_airica.py").read())
process_airica(2012.59, './data/Aug_20_Wadden_sea_B1_AIRICA.xlsx',
              './data/LD_B1.dbs', './results_rws.csv')
db = pd.read_csv('./results_rws.csv',
                   skiprows=[1])

#%% scatterplot 3 areas vs 4 areas
f, ax = plt.subplots(figsize=(8, 6.5), dpi=300)
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=2)
sns.set(font="Verdana", font_scale=1)
sns.despine(f, left=True, bottom=True)

# line through origin
x = [1800, 1800]
y = [2400, 2400]
x_values = [x[0], y[0]]
y_values = [x[1], y[1]]

# axis limits
ax.set_xlim([1800,2400])
ax.set_ylim([1800,2400])

# scattering
ax = sns.lineplot(x=x_values, y=y_values, ax=ax, color="black")
sns.regplot(data=db, x="TCO2_3", y="TCO2_4", ci=False, color="xkcd:primary blue")

# add R2 to graph
mask = ~np.isnan(db.TCO2_3) & ~np.isnan(db.TCO2_4)
r2 = stats.linregress(db.TCO2_3[mask], db.TCO2_4[mask])[2]
r2s = str(round(r2, 2))
text = "$R^2$ = " + r2s

# formatting
plt.tight_layout()
ax.set_xlabel("$DIC_{3 AREAS}$")
ax.set_ylabel("$DIC_{4 AREAS}$")
ax.text(1850, 2350, text, horizontalalignment='left',
        verticalalignment='center', fontsize=15)

# save figure
plt.savefig('./figures/scatter_3areas_vs_4areas.png', format = 'png')
plt.show()

#%% stats given duplicate samples
stats = pd.DataFrame()
stats['CRM_std_err1_3'] = np.nan

# standard error per analysis batch
L = (db.analysis_batch == 1) & (db.location == 'CRM')
stats['CRM_std_err1_3'] = sem(db.TCO2_3[L])
