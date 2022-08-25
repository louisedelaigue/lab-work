import pandas as pd, numpy as np
from sklearn.utils import shuffle

# Create dataframe
louise = pd.DataFrame()

# Create box column
louise["box"] = np.arange(5, 24)

# Add 24 rows for each box
louise = pd.concat([louise]*24, ignore_index=True)

# Sort values by box
louise = louise.sort_values(by="box")

# Add 24 bottles per box
louise["start"] = 1
boxes = list(louise["box"])

for b in boxes:
    louise.loc[louise["box"]==b, "bottle"] = louise.loc[louise["box"]==b, "start"].cumsum()

# Create code name for bottles
louise["Cruise_samples"] = "SO289" + "-" + louise["box"].astype(str) + "-" + louise["bottle"].astype(str)

# Drop useless columns
louise = louise.drop(columns=["box", "start", "bottle"])

# Import Yasmine's samples
yasmine = pd.read_excel("data/SO289/sample list.xlsx")

# Merge both dataframes
df = pd.concat([louise, yasmine])

# Shuffle rows to randomize sample list
df = shuffle(df)

# Save as csv
df.to_csv("./data/SO289/sample_list_20220825.csv", index=False)
