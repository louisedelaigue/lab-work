# import toolbox
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# import data
exec(open("airica_process_data.py").read())

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
sns.regplot(data=db, x="TCO2_3", y="TCO2_4", color="xkcd:primary blue")

# formatting
plt.tight_layout()
ax.set_xlabel("$DIC_{3 AREAS}$")
ax.set_ylabel("$DIC_{4 AREAS}$")

# save figure
plt.savefig('./figures/scatter_3areas_vs_4areas.png', format = 'png')
plt.show()