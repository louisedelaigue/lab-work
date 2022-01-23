# TO ADD AFTER
# /// Calibrate and solve alkalinity and plot calibration ///

# === REMEDY ACID DRIFT
# Isolate dbs in new pandas DataFrame
L = (dbs["bottle"].str.startswith("CRM-")) & (dbs["reference_good"] == True)
dbs_crms = dbs[L]

# Apply np.polytfit (order 3) to CRM titrant molinity
p = np.polyfit(dbs_crms["analysis_datenum"], dbs_crms["titrant_molinity_here"], 3)

f = np.poly1d(p)

# Apply fit to data
x_new = np.linspace(dbs["analysis_datenum"].min(), dbs["analysis_datenum"].max(), 100)
y_new = f(x_new)

# Plot fit
# Create figure
fig, ax = plt.subplots(dpi=300)

# Plot fit
sns.lineplot(x=x_new, y=y_new, color="xkcd:blue", label="Polynomial fit (deg 3)", ax=ax)

# Scatter titrant molinity from CRMs
sns.scatterplot(
    x="analysis_datenum",
    y="titrant_molinity_here",
    data=dbs_crms,
    color="xkcd:blue",
    label="CRMs titrant molinity",
    ax=ax,
)

# Apply fit to titrant molinity from CRMs
dbs_crms["titrant_molinity_polyfit"] = f(dbs_crms["analysis_datenum"])

# Take the mean from the polyfit titrant molinities
molinity_coefficient = dbs_crms["titrant_molinity_polyfit"].mean()

# Update titrant molity value in dbs file
# dbs["titrant_molinity"] = f(dbs["analysis_datenum"])
# dbs["titrant_molinity"] = molinity_coefficient

# Update titrant molinity value in dbs file
# analysis_dates = dbs["analysis_datetime"].dt.day.unique().tolist()
# for date in analysis_dates:
#     A = dbs["analysis_datetime"].dt.day==date
#     B = dbs_crms["analysis_datetime"].dt.day==date
#     dbs.loc[A, "titrant_molinity"] = dbs_crms.loc[B, "titrant_molinity_polyfit"].mean()

analysis_batch = dbs["analysis_batch"].unique().tolist()
for batch in analysis_batch:
    A = dbs["analysis_batch"] == batch
    B = dbs_crms["analysis_batch"] == batch
    dbs.loc[A, "titrant_molinity"] = dbs_crms.loc[B, "titrant_molinity_polyfit"].mean()

# dbs.loc[dbs['analysis_datetime'].dt.day==6,'titrant_molinity'] = 0.099252498
# dbs.loc[dbs['analysis_datetime'].dt.day==13, 'titrant_molinity'] = 0.099252528
# dbs.loc[dbs['analysis_datetime'].dt.day==27, 'titrant_molinity'] = 0.099252474
# dbs.loc[dbs['analysis_datetime'].dt.day==18, 'titrant_molinity'] = 0.099252388
