import PyCO2SYS as pyco2
CRM = pyco2.CO2SYS_nd(2205.26, 2009.48, 1, 2, 
                      salinity=33.494,
                      temperature=20.1,
                      pressure_out=0,
                      total_phosphate=0.45,
                      total_silicate=2.1,
                      opt_pH_scale=1,
                      opt_k_carbonic=16,
                      opt_total_borate=1
                      )

print(CRM['pH_total_out'])