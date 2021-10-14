import PyCO2SYS as pyco2

pCO2_12C = pyco2.sys(2281.91,
                    2167.865,
                    1,
                    2,
                    salinity=32,
                    temperature=12.5,
                      )['pCO2']

pCO2_4C = pyco2.sys(2281.91,
                    2167.865,
                    1,
                    2,
                    salinity=32,
                    temperature=4,
                      )['pCO2']

