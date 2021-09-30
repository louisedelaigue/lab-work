import numpy as np
import pandas as pd

# Create random numbers
numbers = pd.DataFrame()
numbers['time'] = np.random.randint(1,101,5)
# numbers['var'] = np.linspace(7, 9, 30)
numbers.sort_values(by=['time'], inplace=True)

# Only keep last 20 min of data
# short = numbers['time'].tail(1200)
# evenshorter = numbers.tail(1200)

if numbers.time.max() > 1200:
    numbers = numbers.tail(1200)
else:
    numbers = numbers

print(len(numbers.time))