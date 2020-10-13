import pandas as pd
from fx_airica import process_airica

# prepare final db
db = pd.read_excel('./data/RWS_01_11_DIC.xlsx', skiprows=[1])
rws = pd.read_csv('./data/data_v7.csv')

# remove bad flag values
db = db.reset_index()
L = (db.flag == 2)
db = db[L]
#db.loc[~L, ['area_1', 'area_2', 'area_3', 'area_4']] = np.nan

# merge with rws database to import met data
db = pd.merge(left=db, right=rws, how='left',
                  left_on='sample', right_on='bottleid')

# assign salinity to CRM in RWS salinity column
db['salinity_rws'] = db['salinity_rws'].fillna(33.525)

# rename temp column so different than dbs file
rn = {
      "temperature" : "temperature_is"
      }
db.rename(mapper=rn, axis=1, inplace=True)

# process airica data
db = process_airica(2012.59, db,
              './data/LDRWS1.dbs', './results_rws.csv')
