# import toolbox
import pandas as pd
import os
import matplotlib as plt

# import spreadsheet
db = pd.read_excel('.\lab_cs_instruments_config_mock.xlsx',
                   skiprows=[1])

#%% create list of files we want to keep
file_list = [file for file in os.listdir('.\data') if 
                  '_'.join(file.split('_')[2:]) in db.pH_optN.values]

#%% create loop to extract data
data = {} # tell python this is an empty dict so we can put the tables in
for file in file_list:
    fname = ".\data\{}\{}.txt".format(file,file)
    data[file] = pd.read_table(fname, skiprows=20, encoding="unicode_escape",
                               na_values='nan')

#%% rename headers in df inside dict and get rid off empty columns
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

#%% plot pH vs. time
for file in file_list:
    data[file].plot.scatter("time","pH")