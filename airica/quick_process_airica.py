import pandas as pd

exec(open("fx_airica.py").read())
process_airica(2012.59, './data/RWS_01_11_DIC.xlsx',
              './data/LDRWS1.dbs', './results_rws.csv')
db = pd.read_csv('./results_rws.csv')