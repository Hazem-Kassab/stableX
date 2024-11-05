import numpy as np

from src.stablex._visualization import ax
from src.stablex._visualization._visual_element import VisualElement


class VisualUniDimensionalElement(VisualElement):
    no_of_segments = 10

    def transformation_matrix(self):
        s = (self.element.end_node.y - self.element.start_node.y)/self.element.length
        c = (self.element.end_node.x - self.element.start_node.x)/self.element.length
        return np.array([[c, -s],
                        [s, c]])

    def plot_element(self):
        x_array = np.array([self.element.start_node.x, self.element.end_node.x])
        y_array = np.array([self.element.start_node.y, self.element.end_node.y])
        ax.plot(x_array, y_array, 'yellow', linestyle="solid", marker='o')

    def _get_local_coordinates(self):
        return np.stack(np.array([[x/self.no_of_segments * self.element.length, 0]
                                 for x in range(self.no_of_segments+1)]), axis=1)

    def _get_global_coordinates(self):
        translation_array = np.stack(np.array([self.element.start_node.coordinates] * (self.no_of_segments+1)), axis=1)
        return self.transformation_matrix().dot(self._get_local_coordinates()) + translation_array

    def _get_local_displacement(self):
        local_array = np.array([self.element.get_local_displacement(x/self.no_of_segments * self.element.length)
                                for x in range(self.no_of_segments+1)])
        return np.stack(local_array, axis=1)

    def plot_global_displacement(self, scale):
        global_array = self.transformation_matrix().dot(scale * self._get_local_displacement()) + \
                       self._get_global_coordinates()
        ax.plot(global_array[0].real, global_array[1].real, 'white', linestyle='--')
