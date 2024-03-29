# import toolbox
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# import spreadsheet
db = pd.read_excel(".\Aug_20_Wadden_sea_B1.xlsx", skiprows=[1])

# create list of files we want to keep
file_list = [
    file
    for file in os.listdir(".\data")
    if "_".join(file.split("_")[2:]) in db.pH_optN.values
]

# create loop to extract data
data = {}  # tell python this is an empty dict so we can put the tables in
for file in file_list:
    fname = ".\data\{}\{}.txt".format(file, file)
    data[file] = pd.read_table(fname, skiprows=20, encoding="unicode_escape")

# rename headers of df inside dict and get rid off empty columns
rn = {
    "Date [A Ch.1 Main]": "date",
    "Time [A Ch.1 Main]": "time",
    " dt (s) [A Ch.1 Main]": "sec",
    "pH [A Ch.1 Main]": "pH",
    "Fixed Temp (?C) [A Ch.1 CompT]": "temp",
}

for file in file_list:
    data[file].rename(rn, axis=1, inplace=True)
    data[file].drop(
        columns=[
            "Date [Comment]",
            "Time [Comment]",
            "Comment",
            "Unnamed: 18",
            "Unnamed: 19",
            "Unnamed: 20",
            "Unnamed: 21",
            "Unnamed: 22",
            "Unnamed: 23",
            "Unnamed: 24",
            "Unnamed: 25",
            "Unnamed: 26",
            "Unnamed: 27",
            "Unnamed: 28",
            "Unnamed: 29",
        ],
        inplace=True,
    )
    data[file].dropna()

# make a copy of data dict
data_c = data.copy()

# create table to hold results
results = pd.DataFrame({"filename": file_list})
results["time"] = np.nan
results["pH_raw_mean"] = np.nan
results["pH_raw_median"] = np.nan
results["pH_last2min_mean"] = np.nan
results["pH_last2min_median"] = np.nan
results["slope"] = np.nan
results["lowest_ix"] = np.nan
results["pH_s0_mean"] = np.nan
results["pH_s0_median"] = np.nan
results["pH_s0_stderr"] = np.nan
results["pH_s0_std"] = np.nan
results["pH_s0_intercept"] = np.nan

# compute mean and median of last 2min of measurements using all datapoints
for file in file_list:
    L = data[file].sec > 480
    results.loc[results.filename == file, "pH_last2min_mean"] = data[file][L].pH.mean()
    results.loc[results.filename == file, "pH_last2min_median"] = data[file][
        L
    ].pH.median()

    # perform linear regression on all data
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        data_c[file].sec, data_c[file].pH
    )

    data[file]["slope_here"] = np.nan

    for i in data[file].index[:-5]:
        print("correcting...")
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            data_c[file].sec, data_c[file].pH
        )
        data_c[file] = data_c[file].drop(data_c[file].index[0])
        data_c[file].sort_values(by="sec")
        # plot regression
        # fig, ax = plt.subplots()
        # sns.regplot(data_c[file].sec, data_c[file].pH,
        #            fit_reg=True, ax=ax)
        # ax.set_xlim([0, 600])
        # ax.set_ylim([data[file].pH.min(),
        #             data[file].pH.max()])
        data[file].loc[i, "slope_here"] = np.abs(slope)
        print(slope)

    # find index of lowest abs slope
    lowest_ix = data[file].slope_here.idxmin()

    # calculate the mean
    mean = data[file].pH[lowest_ix:].mean()

    # store time for slope 0 in df
    results.loc[results.filename == file, "time"] = data[file].time[lowest_ix][:5]

    # store the raw mean in df
    results.loc[results.filename == file, "pH_raw_mean"] = data[file].pH.mean()

    # store the raw mean in df
    results.loc[results.filename == file, "pH_raw_median"] = data[file].pH.median()

    # store index of lowest abs slope in df
    results.loc[results.filename == file, "lowest_ix"] = data[file].slope_here.idxmin()

    # store slope from lowest_ix in df
    results.loc[results.filename == file, "slope"] = data[file].slope_here[lowest_ix]

    # store the mean in df
    results.loc[results.filename == file, "pH_s0_mean"] = (
        data[file].pH[lowest_ix:].mean()
    )

    # store the median in df
    results.loc[results.filename == file, "pH_s0_median"] = (
        data[file].pH[lowest_ix:].median()
    )

    # store the std_err for slope 0 in df
    results.loc[results.filename == file, "pH_s0_stderr"] = stats.linregress(
        data[file].sec[lowest_ix:], data[file].pH[lowest_ix:]
    )[4]

    # store the std for slope 0 in df
    results.loc[results.filename == file, "pH_s0_std"] = (
        data[file].pH[lowest_ix:]
    ).std()

    # store the intercept for slope 0 in df
    results.loc[results.filename == file, "pH_s0_intercept"] = stats.linregress(
        data[file].sec[lowest_ix:], data[file].pH[lowest_ix:]
    )[1]


results["lowest_ix"] = results.lowest_ix.astype(int)

#%% create figure with two subplots showing slope and pH measurement for each sample
for file in file_list:
    # create 1 fig per sample w/ 2 subplots
    fig, ax = plt.subplots(2, 1, figsize=(8, 6), dpi=300)
    plt.rcParams.update({"font.size": 15})

    # subplot 1
    data[file].plot.scatter("sec", "slope_here", c="xkcd:electric blue", ax=ax[0])
    ax[0].set_xlim([0, 600])
    # ax[0].set_ylim([data[file].slope_here.min(),
    # data[file].slope_here.max()])
    ax[0].set_ylim(np.array([-1, 1]) * 5e-5)
    ax[0].axhline(0, c="k", linewidth=0.8)
    ax[0].set_xlabel("")
    ax[0].set_ylabel("Slope")
    ax[0].set_title("Sample " + str(file.split("_")[2:]))

    # subplot 2
    data[file].plot.scatter("sec", "pH", c="xkcd:electric blue", ax=ax[1])
    data[file].loc[
        results[results.filename == file].lowest_ix.values[0] :
    ].plot.scatter("sec", "pH", c="r", ax=ax[1])
    ax[1].axhline(results[results.filename == file].pH_s0_mean.values, c="r")
    ax[1].set_xlim([0, 600])
    ax[1].set_ylim([data[file].pH.min(), data[file].pH.max()])
    ax[1].set_xlabel("Time (sec)")
    ax[1].set_ylabel("pH")

    # save image in high quality, png format
    plt.tight_layout()
    filen = "./figures/ph_optode/{}.png".format(file)
    plt.savefig(filen)
    plt.show()

# save results as text file
results.to_csv("./results/results.csv", index=None)

#%% create a graph showing all mean samples at slope closest to 0
fig, ax = plt.subplots(figsize=(15, 6), dpi=300)
plt.rcParams.update({"font.size": 15})
ax.scatter(results.time, results.pH_s0_mean, c="xkcd:electric blue")
ax.set_ylabel("pH")
ax.set_xlabel("Time")
fig.suptitle("pH vs. time - all samples", fontsize=25, y=1.08)

# save image in high quality, png format
plt.tight_layout()
filen = "./figures/ph_optode/all_samples_pH.png"
plt.savefig(filen)
plt.show()

#%% save results as text file
results.to_csv("./results/results.csv", index=None)
