import matplotlib.pyplot as plt
import numpy as np

# set force and number of increments
P = 1000
n = 1000
i = 0
di = 0

# calculate load step
dP = P/n

# empty arrays to hold displacement and load values:
P_array = []
d_array = []

while i <= n:
    Pi = i * dP
    ki = 1/(3 * (Pi+2)**2)
    di = di + dP/ki
    P_array.append(Pi)
    d_array.append(di)
    i += 1

exact_load = np.arange(0, P, P/1000)

plt.plot(d_array, P_array, "b", label="Numerical (n = %d)" % n)
plt.plot((exact_load+2)**3 - 8, exact_load, "k", label="Exact, Eq.(5)", linestyle="--")
plt.legend()
plt.show()