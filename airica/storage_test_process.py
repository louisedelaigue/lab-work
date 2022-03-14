import pandas as pd, numpy as np
from fx_airica_koolstof import process_airica
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt

# Import lab file
db = pd.read_excel(
    "./data/LD_storage_test/AIRICA_storage_test_mod_14032022.xlsx", na_values=-9999
)

# Remove nan
L = db["DIC"].isnull()
db = db[~L]

# Remove AIRICA malfunction days
bad_batches = [3, 5, 8]
db = db[~db["analysis_batch"].isin(bad_batches)]

# Assign metadata
db.loc[db["name"].str.startswith(("J", "U", "R")), "salinity"] = 32
db.loc[db["name"].str.startswith("CRM-189"), "salinity"] = 33.494
db.loc[db["name"].str.startswith("CRM-195"), "salinity"] = 33.485

# Select which CRMs to use/avoid for calibration
db["reference_good"] = False
db.loc[db["name"].str.startswith("CRM-"), "reference_good"] = True
db.loc[db["name"] == "CRM-189-0468-10", "reference_good"] = False
db.loc[db["name"] == "CRM-189-0468-09", "reference_good"] = False
db.loc[db["name"] == "CRM-189-0468-07", "reference_good"] = False
db.loc[db["name"] == "CRM-195-0078-1200-2", "reference_good"] = False
db.loc[db["name"] == "CRM-189-0468-17", "reference_good"] = False
db.loc[db["name"] == "CRM-195-0078-25", "reference_good"] = False
db.loc[db["name"] == "CRM-189-0408-1200-7", "reference_good"] = False

# Process AIRICA data
results = process_airica(
    db,
    "./data/LD_storage_test/LD_storage_test_mod_14032022.dbs",
    "./data/LD_storage_test/results_storage_test.csv",
)

results.to_csv("./data/LD_storage_test/results.csv", index=False)

# Add a label column
results["label"] = np.nan
results.loc[results["location"] == "R", "label"] = "Rinsed"
results.loc[results["location"] == "U", "label"] = "Unrinsed"

# === STATISTICS
# Statistics on all replicates
L = results["name"].str.startswith(("R", "U"))
SE = stats.mstats.sem(results["TCO2"][L], axis=None, ddof=0)
print("Standard error for all replicates = {}".format(SE))
slope = stats.linregress(results[L]["analysis_batch"], results[L]["TCO2"])[0]
print("Slope for all replicates = {}".format(slope))

# Create table to hold statistics for each analysis batch
batches = list(results["analysis_batch"].unique())
statistics = pd.DataFrame({"batch_number": batches})
statistics["analysis_date"] = np.nan
statistics["n_samples"] = np.nan
statistics["mean_all"] = np.nan
statistics["median_all"] = np.nan
statistics["slope_all"] = np.nan
statistics["standard_error_batch"] = np.nan
statistics["standard_error_all_batches"] = np.nan
statistics["mean_R"] = np.nan
statistics["median_R"] = np.nan
statistics["standard_error_batch_R"] = np.nan
statistics["standard_error_all_batches_R"] = np.nan
statistics["mean_U"] = np.nan
statistics["median_U"] = np.nan
statistics["standard_error_batch_U"] = np.nan
statistics["standard_error_all_batches_U"] = np.nan

for batch in batches:
    # Compute overall statistics
    L = (
        (results["name"].str.startswith(("R", "U")))
        & (results["TCO2"].notnull())
        & (results["analysis_batch"] == batch)
    )
    statistics.loc[statistics["batch_number"] == batch, "analysis_date"] = results[
        "datetime"
    ][L].dt.date.iloc[0]
    statistics.loc[statistics["batch_number"] == batch, "n_samples"] = results["TCO2"][
        L
    ].count()
    statistics.loc[statistics["batch_number"] == batch, "mean_all"] = results["TCO2"][
        L
    ].mean()
    statistics.loc[statistics["batch_number"] == batch, "median_all"] = results["TCO2"][
        L
    ].median()
    statistics.loc[
        statistics["batch_number"] == batch, "standard_error_batch"
    ] = stats.mstats.sem(results["TCO2"][L], axis=None, ddof=0)
    L = (results["name"].str.startswith(("R", "U"))) & (results["TCO2"].notnull())
    statistics.loc[
        statistics["batch_number"] == batch, "standard_error_all_batches"
    ] = stats.mstats.sem(results["TCO2"][L], axis=None, ddof=0)

    # Compute statistics for R vs. U
    # R
    L = (
        (results["name"].str.startswith("R"))
        & (results["TCO2"].notnull())
        & (results["analysis_batch"] == batch)
    )
    statistics.loc[statistics["batch_number"] == batch, "mean_R"] = results["TCO2"][
        L
    ].mean()
    statistics.loc[statistics["batch_number"] == batch, "median_R"] = results["TCO2"][
        L
    ].median()
    statistics.loc[
        statistics["batch_number"] == batch, "standard_error_batch_R"
    ] = stats.mstats.sem(results["TCO2"][L], axis=None, ddof=0)
    L = (results["name"].str.startswith(("R"))) & (results["TCO2"].notnull())
    statistics.loc[
        statistics["batch_number"] == batch, "standard_error_all_batches_R"
    ] = stats.mstats.sem(results["TCO2"][L], axis=None, ddof=0)

    # U
    L = (
        (results["name"].str.startswith("U"))
        & (results["TCO2"].notnull())
        & (results["analysis_batch"] == batch)
    )
    statistics.loc[statistics["batch_number"] == batch, "mean_U"] = results["TCO2"][
        L
    ].mean()
    statistics.loc[statistics["batch_number"] == batch, "median_U"] = results["TCO2"][
        L
    ].median()
    statistics.loc[
        statistics["batch_number"] == batch, "standard_error_batch_U"
    ] = stats.mstats.sem(results["TCO2"][L], axis=None, ddof=0)
    L = (results["name"].str.startswith(("U"))) & (results["TCO2"].notnull())
    statistics.loc[
        statistics["batch_number"] == batch, "standard_error_all_batches_U"
    ] = stats.mstats.sem(results["TCO2"][L], axis=None, ddof=0)

statistics.to_csv("./data/stats_airica_storage_test.csv", index=False)

# === TIME SINCE SAMPLING COLUMN
results["time_since_sampling"] = np.nan
start_date = pd.to_datetime("2021-09-28", format="%Y-%m-%d")
results["time_since_sampling"] = (results["datetime"] - start_date).dt.days

# === PLOT 3 AREAS
# Create figure
fig, ax = plt.subplots(dpi=300)

# Isolate rinsed and unrinsed replicates from dataset
L = results["name"].str.startswith(("R", "U"))

# Scatter rinsed samples in dark blue
sns.stripplot(
    y="TCO2",
    x="time_since_sampling",
    hue="label",
    data=results[L],
    palette="viridis",
    jitter=True,
    ax=ax,
)

# Improve figure
ymin = round(results["TCO2"][L].min() - 2)
ymax = round(results["TCO2"][L].max() + 3)
plt.ylim([ymin, ymax])

ax.legend(loc="upper left").set_title("")

ax.set_ylabel("$TCO_{2}$ / $μmol⋅kg^{-1}$")
ax.set_xlabel("Time since sampling (days)")

ax.grid(alpha=0.3)
plt.tight_layout()

# Save plot
plt.savefig("./figures/storage_test_DIC.png")
