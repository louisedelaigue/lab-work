# import toolbox
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

# import spreadsheet
db = pd.read_excel('.\lab_cs_instruments_config_mock.xlsx',
                   skiprows=[1])

# create list of files we want to keep
file_list = [file for file in os.listdir('.\data') if 
                  '_'.join(file.split('_')[2:]) in db.pH_optN.values]

# create loop to extract data
data = {} # tell python this is an empty dict so we can put the tables in
for file in file_list:
    fname = ".\data\{}\{}.txt".format(file,file)
    data[file] = pd.read_table(fname, skiprows=20, encoding="unicode_escape")

# rename headers of df inside dict and get rid off empty columns
rn = {
      "Date [A Ch.1 Main]":"date",
      "Time [A Ch.1 Main]":"time",
      " dt (s) [A Ch.1 Main]":"sec",
      "pH [A Ch.1 Main]":"pH",
      "Fixed Temp (?C) [A Ch.1 CompT]":"temp"
      }

for file in file_list:
    data[file].rename(rn, axis=1, inplace=True)
    data[file].drop(columns=["Date [Comment]",
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
                    "Unnamed: 29"],
                    inplace=True)
    data[file].dropna()

data_c = data.copy()

for file in file_list: #[file_list[2]]:

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        data_c[file].sec, data_c[file].pH)
    
    data[file]['slope_here'] = np.nan
    for i in data[file].index[:-5]:
        print("correcting...")
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            data_c[file].sec, data_c[file].pH)
        data_c[file] = data_c[file].drop(data_c[file].index[0])
        data_c[file].sort_values(by ='sec')
        # plot regression
        #fig, ax = plt.subplots()
        #sns.regplot(data_c[file].sec, data_c[file].pH,
        #            fit_reg=True, ax=ax)
        #ax.set_xlim([0, 600])
        #ax.set_ylim([data[file].pH.min(),
        #             data[file].pH.max()])
        data[file].loc[i, 'slope_here'] = np.abs(slope)
        print(slope)
        
    # find index of lowest abs slope
    lowest_ix = data[file].slope_here.idxmin()
    
    # calculate the mean
    mean = data[file].pH[lowest_ix:].mean()
    
    # calculate the median
    median = data[file].pH[lowest_ix:].median()

    fig, ax = plt.subplots()
    data[file].plot.scatter('sec','slope_here', ax=ax)
    ax.grid(alpha=0.3)
    
    fig, ax = plt.subplots()
    data[file].plot.scatter('sec', 'pH', ax=ax)
    data[file].loc[lowest_ix:].plot.scatter('sec','pH', ax=ax, c='r')
    ax.axhline(mean, c='r')
    ax.grid(alpha=0.3)

#%% VISUALIZATION
# graphs
for file in file_list:
    data[file].plot.scatter("sec", "pH", marker="+",
                facecolors='none', color='b')
    sns.regplot(data_c[file].sec, data_c[file].pH, fit_reg=True, ci=None,
                marker="o", color='r')

# stats table
temp["avg_pH_2min"] = np.nan
temp["median"] = np.nan
temp["mean"] = np.nan
temp["median - mean"] = np.nan
temp["avg_pH_2min - mean"] = np.nan

for file in file_list:
    L = data[file].sec>480
    temp.loc[temp.filename==file,"avg_pH_2min"] = data[file][L].pH.mean()
    temp.loc[temp.filename==file,"median"] = data_c[file].pH.median()
    temp.loc[temp.filename==file,"mean"] = data_c[file].pH.mean()
    temp.loc[temp.filename==file,"median - mean"] = temp["median"]- temp["mean"]
    temp.loc[temp.filename==file,"avg_pH_2min - mean"] = temp["avg_pH_2min"]- temp["mean"]

