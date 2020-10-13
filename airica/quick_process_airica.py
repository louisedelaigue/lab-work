import pandas as pd
from fx_airica import process_airica

# exec(open("fx_airica.py").read())
db = pd.read_excel(xlsx_filepath, skiprows=[1])

# remove bad flag values
db = db.reset_index()
L = (db.flag == 2)
db = db[L]
# db.loc[~L, ['area_1', 'area_2', 'area_3', 'area_4']] = np.nan

# update salinity and density values in db

db = process_airica(2012.59, db,
              './data/LDRWS1.dbs', './results_rws.csv')
# db = pd.read_csv('./results_rws.csv')
