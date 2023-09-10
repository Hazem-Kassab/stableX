from stableX.visualization.visual_element import VisualElement
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from stableX.visualization import ax
import pathlib


class VisualRotationalSpringElement(VisualElement):
    def __init__(self, element):
        super().__init__(element)
        # self.image = Image.open(str(pathlib.Path().absolute()) + r"\stableX\visualization\image.png", "r")
        self.image = Image.open(r"D:\LENOVO\Desktop\ASU MS\Research\stableX\stableX\visualization\image.png", "r")

    def plot_element(self):
        imagebox = OffsetImage(self.image, zoom=0.1)
        ab = AnnotationBbox(imagebox, self.element.start_node.coordinates, frameon=False)
        ax.add_artist(ab)
        plt.draw()

    def plot_global_displacement(self, scale):
        imagebox = OffsetImage(self.image, zoom=0.1)
        x_coord = self.element.start_node.x + self.element.start_node.x_dof.displacement*scale
        y_coord = self.element.start_node.y + self.element.start_node.y_dof.displacement*scale
        ab = AnnotationBbox(imagebox, (x_coord, y_coord), frameon=False)
        ax.add_artist(ab)
        plt.draw()
