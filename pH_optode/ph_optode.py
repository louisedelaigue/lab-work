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


#%% STATS
#%% average last two minutes and create a table
avg = pd.DataFrame({"filename":file_list})
avg["average_pH"] = np.nan

for file in file_list:
    L = data[file].sec>480
    avg.loc[avg.filename==file,"average_pH"] = data[file][L].pH.mean()\
                
#%% plot linear regression for all data points per sample
# doing the math with scipy stats
slope, intercept, r_value, p_value, std_err = stats.linregress(
    data[file_list[2]].sec, data[file_list[2]].pH)
while slope >= 0.00000001:
    print("correcting...")
    slope, intercept, r_value, p_value, std_err = stats.linregress(
    data[file_list[2]].sec, data[file_list[2]].pH)
    data[file_list[2]] = data[file_list[2]].drop(data[file_list[2]].index[0])
    data[file_list[2]].sort_values(by ='sec' )
    print(slope)

        
        
        
        
        
        
        
        
        

#%% PLOTTING
#%% plotting the regression with seaborn
for file in file_list:
    fig, ax = plt.subplots()
    sns.regplot(data[file].sec, data[file].pH, fit_reg=True, x_ci="sd")
    
#%% scatter each plot individually
for file in file_list:
    data[file].plot.scatter("sec", "pH")

#%% plot line each file on same plot
fig, ax = plt.subplots()
for file in file_list:
    data[file].plot("sec", "pH", ax=ax)
    
#%% jointplot of averages distribution
fig, ax = plt.subplots()
sns.despine(left=True)
d = avg.average_pH
#sns.distplot(d, kde=False, color="b", ax=ax)
sns.jointplot(d,d, kind="hex", color="#4CB391")





