import matplotlib.pyplot as plt
import numpy as np

from stableX import Structure
from stableX.Elements.element import Element

plt.rcParams['axes.facecolor'] = 'black'


def _graph_element(element: Element):
    x_array = np.array([element.start_node.x, element.end_node.x])
    y_array = np.array([element.start_node.y, element.end_node.y])
    plt.plot(x_array, y_array, 'white')


def graph_structure(structure: Structure):
    x_coordinates = [node.x for node in structure.nodes]
    y_coordinates = [node.y for node in structure.nodes]
    x_min = min(x_coordinates)-.5
    y_min = min(y_coordinates)-.5
    x_max = max(x_coordinates)+.5
    y_max = max(y_coordinates)+.5
    plt.axis([x_min, x_max, y_min, y_max])
    for element in structure.elements:
        _graph_element(element)
