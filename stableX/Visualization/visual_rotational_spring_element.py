from stableX.Visualization.visual_element import VisualElement
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from stableX.Visualization import fig, ax


class VisualRotationalSpringElement(VisualElement):
    image = Image.open(r"image.png", "r")

    def plot_element(self):
        imagebox = OffsetImage(VisualRotationalSpringElement.image, zoom=0.1,)
        ab = AnnotationBbox(imagebox, self.element.start_node.coordinates, frameon=False)
        ax.add_artist(ab)
        plt.draw()

    def plot_global_displacement(self):
        pass



