import koolstof as ks
import PyCO2SYS as pyco2

# Define file location
spreadsheet_path = "data/vials_test/spreadsheet.xlsx"
text_files_folder_path = "data/vials_test/"

# Import dataset
df = ks.pH_optode(spreadsheet_path, text_files_folder_path)

# Recalculate pH at 25 degrees
df['pH_recalc'] = pyco2.sys(
    df.pH_NBS,
    2300,
    3,
    1,
    opt_pH_scale=1,
    temperature=df.temperature,
    salinity=35,
    temperature_out=25,
)['pH_out']

df['pH_recalc'] = round(df['pH_recalc'], 3)

# Save as csv
df.to_csv("data/vials_test/results.csv", index=False)
