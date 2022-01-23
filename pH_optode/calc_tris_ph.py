# import toolbox
import pandas as pd
import numpy as np

# function
def calc_tris_ph(S, T):
    """Calculate pH value of Dickson's TRIS buffer based on S and T."""
    return (
        ((11911.08 - (18.2499 * S) - (0.039336 * (S ** 2))) / T)
        - 366.27059
        + (0.53993607 * S)
        + (0.00016329 * (S ** 2))
        + (64.52243 - (0.084041 * S)) * np.log(T)
        - (0.11149858 * T)
    )


# variables and convert celcius to kelvin
S = 35
t = 50
T = t + 273.15

# run function
ans = calc_tris_ph(S, T)
