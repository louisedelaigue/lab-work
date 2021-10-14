import PyCO2SYS as pyco2

pCO2_12C = pyco2.sys(2281.91,
                    2167.865,
                    1,
                    2,
                    salinity=32,
                    temperature=23.46,
                    temperature_out=12.5,
                      )['pCO2_out']

pCO2_4C = pyco2.sys(2281.91,
                    2167.865,
                    1,
                    2,
                    salinity=32,
                    temperature=23.46,
                    temperature_out=4,
                      )['pCO2_out']

