from stableX.Elements.SprningElements.linear_rotational_spring_element import LinearRotationalSpringElement
from stableX.Elements.UniDimensionalElements.unidimensional_element import UniDimensionalElement
from stableX.Elements.element import Element
from stableX.Visualization import VisualUniDimensionalElement
from stableX.Visualization.visual_element import VisualElement
from stableX.Visualization.visual_rotational_spring_element import VisualRotationalSpringElement


def create_visual_element(element: Element) -> VisualElement:
    if isinstance(element, UniDimensionalElement):
        return VisualUniDimensionalElement(element)

    elif isinstance(element, LinearRotationalSpringElement):
        return VisualRotationalSpringElement(element)

    else:
        print("Element does not have a visual twin")

