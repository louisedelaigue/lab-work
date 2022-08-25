import pandas as pd, numpy as np
from sklearn.utils import shuffle

# Create df
df = pd.DataFrame()

df["box"] = np.arange(5, 24)
df = pd.concat([df]*24, ignore_index=True)

df = df.sort_values(by="box")

df["start"] = 1

boxes = list(df["box"])

for b in boxes:
    df.loc[df["box"]==b, "bottle"] = df.loc[df["box"]==b, "start"].cumsum()

df["sample"] = "SO289" + "-" + df["box"].astype(str) + "-" + df["bottle"].astype(str)

df = df.drop(columns=["box", "start", "bottle"])

df = shuffle(df)