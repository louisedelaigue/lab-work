import pandas as pd, seaborn as sns, calkulate as calk
import matplotlib.pyplot as plt
import PyCO2SYS as pyco2
from scipy import stats

# === VINDTA DATA
# Import VINDTA DIC values
vindta = pd.read_csv("data/SO279_CTD_discrete_samples.csv", na_values=-999)

# Rename colums
rn = {
    "Station_ID": "station",
    "Niskin_ID": "niskin",
    "CTDTEMP_ITS90": "temperature",
    "CTDSAL_PSS78": "salinity",
    "DIC": "DIC_vindta",
}
vindta.rename(rn, axis=1, inplace=True)

# Only keep DIC values that aren't nan
L = vindta["DIC_vindta"].isnull()
vindta = vindta[~L]

# Recalculate DIC from pH(initial talk) and TA
# Recalculate pH(initial_talk) at insitu temperature using DIC
# and convert from free scale to total scale
vindta["DIC_recalc"] = pyco2.sys(
    vindta.pH_initial_talk,
    vindta.TA,
    3,
    1,
    opt_pH_scale=3,
    salinity=vindta.salinity,
    temperature_out=vindta.temperature,
    total_phosphate=vindta.Phosphate,
    total_silicate=vindta.Silicate,
)["dic"]

# === QUAATRO DATA
# Import QuAAtro DIC values
quaatro = pd.read_excel("data/210521-LouiseD-DIC.xlsx", skiprows=19)

# Rename and drop useless columns
rn = {"Unnamed: 0": "stncode", "Unnamed: 2": "DIC_quaatro"}
quaatro.rename(rn, axis=1, inplace=True)
quaatro.drop(columns=["Unnamed: 1", "Unnamed: 3", "Unnamed: 4"], inplace=True)

# Drop nans
quaatro.dropna(inplace=True)

# Convert DIC values to numbers
quaatro["DIC_quaatro"] = pd.to_numeric(quaatro["DIC_quaatro"], errors="coerce")

# Remove useless rows
quaatro = quaatro[
    ~quaatro["stncode"].isin(
        ["DICKSON#186", "COMM", "LNSW NUTS", "METH", "Sample ID", "UNIT"]
    )
]

# Remove space in sample names
quaatro["stncode"] = quaatro["stncode"].str.replace(" ", "")

# Rename samples
sample_list = quaatro["stncode"].tolist()
sample_names = []

for sample in sample_list:
    if len(sample.split("-")) == 3:
        stn = sample.split("-")[0]
        sample_names.append(sample)
    else:
        sample_names.append(stn + "-" + sample)

quaatro["sample_names"] = sample_names

# Remove useless parts of sample names
quaatro["sample_names"] = quaatro["sample_names"].str.replace("-01", "")
quaatro["sample_names"] = quaatro["sample_names"].str.replace("CTDST", "")

# Split sample names into columns for station and niskin
quaatro["station"] = quaatro["sample_names"].apply(lambda x: x.split("-")[0]).str[-1]
quaatro["niskin"] = quaatro["sample_names"].apply(lambda x: x.split("-")[1])

# Drop useless columns
quaatro.drop(columns=["stncode", "sample_names"], axis=1, inplace=True)

# Average duplicates
quaatro = quaatro.groupby(by=["station", "niskin"]).mean().reset_index()

# Ensure quaatro contains only numbers
quaatro["station"] = pd.to_numeric(quaatro["station"])
quaatro["niskin"] = pd.to_numeric(quaatro["niskin"])

# === BRING VINDTA AND QUAATRO DATA TOGETHER
df = pd.merge(vindta, quaatro, on=["station", "niskin"], how="left")

# === CONVERT QUAATRO DIC units from uM/Lto uM/kg
# Calculate density for each sample at lab temperature = 23 deg C
df["density"] = calk.density.seawater_1atm_MP81(23, df["salinity"])

# Unit conversion
df["DIC_quaatro_conv"] = df["DIC_quaatro"] / df["density"]

# === COMPARE VINDTA AND QUAATRO DATA
# === STATISTICS
# Get numbers for Linear Regression
R_orig = stats.linregress(df["DIC_quaatro_conv"], df["DIC_vindta"])[2]
R2_orig = round(R_orig ** 2, 2)
R_recalc = stats.linregress(df["DIC_recalc"], df["DIC_vindta"])[2]
R2_recalc = round(R_recalc ** 2, 2)

# ===== PLOTS
# === LINEAR REGRESSION
# Prepare figure
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=1)
sns.set(font="Verdana", font_scale=1)

# Create figure
fig, ax = plt.subplots(dpi=300, figsize=(7, 6))

# Linear regression
sns.regplot(
    y="DIC_quaatro_conv",
    x="DIC_vindta",
    data=df,
    color="xkcd:blue",
    label="Linear regression original DIC",
    ax=ax,
)

sns.regplot(
    y="DIC_quaatro_conv",
    x="DIC_recalc",
    data=df,
    color="xkcd:cyan",
    label="Linear regression recalc DIC",
)

# Line through origin
x = [2000, 2300]
y = [2000, 2300]
x_values = [x[0], x[1]]
y_values = [y[0], y[1]]
sns.lineplot(
    x=x_values,
    y=y_values,
    ax=ax,
    linestyle="--",
    color="black",
    label="Perfect fit",
)

# Add R2 to plot
ax.text(2102, 2172, "$R^2$(O) = {}".format(R2_orig), fontsize=15)
ax.text(2102, 2162, "$R^2$(R) = {}".format(R2_recalc), fontsize=15)

# Improve figure
ymin = df["DIC_quaatro_conv"].min() - 10
ymax = df["DIC_quaatro_conv"].max() + 10
xmin = df["DIC_vindta"].min() - 10
xmax = df["DIC_vindta"].max() + 10
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])

plt.legend()

ax.set_ylabel("$DIC_{QuAAtro}$ / μmol/kg")
ax.set_xlabel("$DIC_{RECALC/VINDTA}$ / μmol/kg")

# Save plot
plt.savefig("./figs/compare_so279_dic_recalc_vindta_quaatro_linregress.png")

# === DIC VINDTA VS DIC RECALC# === STATISTICS
# Get numbers for Linear Regression
R = stats.linregress(df["DIC_recalc"], df["DIC_vindta"])[2]
R2 = round(R ** 2, 2)

# Prepare figure
sns.set_style("darkgrid")
sns.set_context("paper", font_scale=1)
sns.set(font="Verdana", font_scale=1)

# Create figure
fig, ax = plt.subplots(dpi=300, figsize=(7, 6))

# Linear regression
sns.regplot(
    y="DIC_recalc",
    x="DIC_vindta",
    data=df,
    color="xkcd:blue",
    label="Linear regression",
    ax=ax,
)


# Line through origin
x = [2000, 2300]
y = [2000, 2300]
x_values = [x[0], x[1]]
y_values = [y[0], y[1]]
sns.lineplot(
    x=x_values,
    y=y_values,
    ax=ax,
    linestyle="--",
    color="black",
    label="Perfect fit",
)

# Add R2 to plot
ax.text(2102, 2172, "$R^2$ = {}".format(R2), fontsize=15)

# Improve figure
ymin = df["DIC_recalc"].min() - 10
ymax = df["DIC_recalc"].max() + 10
xmin = df["DIC_vindta"].min() - 10
xmax = df["DIC_vindta"].max() + 10
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])

plt.legend()

ax.set_ylabel("$DIC_{RECALC}$ / μmol/kg")
ax.set_xlabel("$DIC_{VINDTA}$ / μmol/kg")

# Save plot
plt.savefig("./figs/compare_so279_dic_recalc_vindta_linregress.png")
