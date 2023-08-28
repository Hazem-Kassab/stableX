import matplotlib.pyplot as plt
import numpy as np

P = 100
step = 10
P_array_1 = np.array(range(0, P, 1))
P_array = np.array(range(0, P+step, step))

u = (P_array_1 + 1) ** 2 - 1

i = 0
po = 0
u_approx = 0
u_approx_array = np.array([])


for p in P_array:
    dp = p - po
    k = 1 / (2*(po+1))
    u_approx += dp/k
    print(k * u_approx)
    u_approx_array = np.append(u_approx_array, u_approx)
    i += 1
    po = P_array[i - 1]

plt.plot(u, P_array_1, "k")
plt.plot(u_approx_array, P_array, "b")
plt.show()
