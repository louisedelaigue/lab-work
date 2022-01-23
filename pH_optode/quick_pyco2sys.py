import PyCO2SYS as pyco2
import calkulate as calk

# Start
Density = calk.density.seawater_1atm_MP81(23, 33.525)
TA_start = 2212.0
DIC_start = 2012.59
pH_start = pyco2.sys(
    2212.0,
    2012.59,
    1,
    2,
    salinity=33.525,
    temperature=23,
    pressure_out=0,
    opt_pH_scale=3,
    total_phosphate=0.42,
    total_silicate=3.3,
)["pH_nbs"]

# t = 0
acid = 2.5190 * (10 ** -6)  # umol/L (0.1 M HCl)
TA_loss = acid / Density  # umol/kg
TA_t0 = TA_start - TA_loss

pH_t0 = pyco2.sys(
    TA_t0,
    2012.59,
    1,
    2,
    salinity=33.525,
    temperature=23,
    pressure_out=0,
    opt_pH_scale=3,
    total_phosphate=0.42,
    total_silicate=3.3,
)["pH_nbs"]

# t = req
TA_req = TA_start
pCO2 = 416.17

pH_end = pyco2.sys(
    TA_req,
    pCO2,
    1,
    4,
    salinity=33.525,
    temperature=23,
    pressure_out=0,
    opt_pH_scale=3,
    total_phosphate=0.42,
    total_silicate=3.3,
)["pH_nbs"]


TA_target = pyco2.sys(
    6.3,
    2012.59,
    3,
    2,
    salinity=33.525,
    temperature=23,
    pressure_out=0,
    opt_pH_scale=3,
    total_phosphate=0.42,
    total_silicate=3.3,
)["alkalinity"]

#%%
volume_sample = 300
density_sample = calk.density.seawater_1atm_MP81(23, 33.525)
mass_sample = volume_sample * density_sample
TA_sample = 2212.0
TA_mix = pyco2.sys(
    6.3,
    2012.59,
    3,
    2,
    salinity=33.525,
    temperature=23,
    pressure_out=0,
    opt_pH_scale=3,
    total_phosphate=0.42,
    total_silicate=3.3,
)["alkalinity"]

TA_acid = -0.1 * (10 ** 6)

mass_acid = (mass_sample * (TA_sample - TA_mix)) / (TA_mix - TA_acid)
density_acid = calk.density.HCl_NaCl_25C_DSC07(0.1, 0.6)
volume_acid = mass_acid / density_acid

pH_end = pyco2.sys(
    TA_mix,
    416,
    1,
    4,
    salinity=33.525,
    temperature=23,
    pressure_out=0,
    opt_pH_scale=3,
    total_phosphate=0.42,
    total_silicate=3.3,
)["pH_nbs"]
