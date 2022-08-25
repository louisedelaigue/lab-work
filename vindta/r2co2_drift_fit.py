import pandas as pd
import matplotlib.pyplot as plt

# Import data
dbs = pd.read_csv("data/R2CO2/r2co2.csv")

# Convert datetime column to right format
dbs["analysis_datetime"] = pd.to_datetime(dbs["analysis_datetime"])

# Only keep last testing day (that includes CRMs and nuts water)
L = dbs["analysis_datetime"].dt.day == 24
dbs = dbs[L]

# Plot data    
# Create figure
fig, ax = plt.subplots(dpi=300, figsize=(6, 4))

# Scatter non self DIC
L = dbs["bottle"].str.startswith("junk")
ax.scatter(dbs["analysis_datenum"][L],
           dbs["dic"][L],
           label="DIC")

ax.scatter(dbs["analysis_datenum"][L],
           dbs["dic_self"][L],
           label="DIC self")

ax.legend()

# Plot nuts water
# Create figure
fig, ax = plt.subplots(dpi=300, figsize=(6, 4))

# Scatter nuts waterand CRMs
L = dbs["bottle"].str.startswith("nuts")
ax.scatter(dbs["analysis_datenum"][L],
           dbs["dic"][L],
           label="NUTS")

fig, ax = plt.subplots(dpi=300, figsize=(6, 4))
L = dbs["bottle"].str.startswith("CRM")
ax.scatter(dbs["analysis_datenum"][L],
           dbs["dic"][L],
           label="CRMs")

