from stablex.visualization.visual_element import VisualElement
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from stablex.visualization import ax
import pathlib


class VisualRotationalSpringElement(VisualElement):
    def __init__(self, element):
        super().__init__(element)
        image_path = pathlib.Path(__file__).parent / "image.png"
        self.image = Image.open(image_path, "r")

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
