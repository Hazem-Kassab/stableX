import matplotlib.pyplot as plt
from mpl_toolkits.axisartist import Subplot

from stableX import Structure
from stableX.Visualization.visual_element_factory import create_visual_element

# fig = plt.figure(facecolor='black')
# ax = Subplot(fig, 111, facecolor='black')
# fig.add_subplot(ax)


def plot_structure(structure: Structure):
    x_coordinates = [node.x for node in structure.nodes]
    y_coordinates = [node.y for node in structure.nodes]
    x_min = min(x_coordinates)
    y_min = min(y_coordinates)
    x_max = max(x_coordinates)
    y_max = max(y_coordinates)
    x_range = x_max - x_min
    y_range = y_max - y_min
    plt.axis([x_min - 1.1 * x_range/2,
              x_max + 1.1 * x_range/2,
              y_min - 1.1 * y_range/2,
              y_max + 1.1 * y_range/2])
    for element in structure.elements:
        # if type(element) is not LinearRotationalSpringElement:
        vse = create_visual_element(element)
        # print(vse)
        vse.plot_element()
        vse.plot_global_displacement()
