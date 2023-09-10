from matplotlib import pyplot as plt
from mpl_toolkits.axisartist import Subplot

fig = plt.figure(facecolor='black')
ax = Subplot(fig, 111, facecolor='black')
ax.axis('equal')
fig.add_subplot(ax)
