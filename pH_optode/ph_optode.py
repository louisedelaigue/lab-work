# import toolbox
import pandas as pd
import os 

# import spreadsheet
db = pd.read_excel('.\lab_cs_instruments_config_mock.xlsx',
                   skiprows=[1])

#%% create list and loop
file_list = [file for file in os.listdir('.\data') if 
                  '_'.join(file.split('_')[2:]) in db.pH_optN.values]

