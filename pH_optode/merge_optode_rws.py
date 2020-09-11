# Paths relative to location of this script
import pandas as pd

# Import data
data = pd.read_csv('./data_rws/data_v7.csv',
                   skiprows=[1])
optode_file = "data_rws/result_RWS_01_11"
optode = pd.read_csv(optode_file + ".csv")


def get_station_bottle_data(row):
    """Single-row function to get data from other RWS measurements and put them into
    the optode table.
    """
    pH_cols = [  # All converted to Total scale at 20 °C:
        "pH_calc12_total_20",  # calculated from DIC and TA with PyCO2SYS
        "pH_spectro_total_20",  # measured with the spectrophotometer
        "pH_vindta_total_20",  # from the VINDTA TA titration (1st point, before acid)
    ]
    name_split = row.filename.split("_")[2:]
    if len(name_split) == 2:
        station = name_split[0]
        bottle = int(name_split[1])
        d = (data.station == station) & (data.bottleid == bottle)
        assert sum(d) == 1
        pH_data = {col: data[d][col].values[0] for col in pH_cols}
        data_index = data.index[d].values[0]
    else:
        station = bottle = ""
        pH_data = {col: None for col in pH_cols}
        data_index = None
    return pd.Series(
        dict(station=station, bottle=bottle, data_index=data_index, **pH_data)
    )


# Apply the function to the whole table to get the data, then save as new CSV
optode = optode.join(optode.apply(get_station_bottle_data, axis=1))
optode.to_csv(optode_file + "_comparison.csv")

