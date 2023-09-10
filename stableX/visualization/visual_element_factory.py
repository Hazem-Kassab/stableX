from stableX.elements.spring_elements.rotational_spring_element import LinearRotationalSpringElement
from stableX.elements.unidimensional_elements.unidimensional_element import UniDimensionalElement
from stableX.elements.element import Element
from stableX.visualization.visual_unidimensional_element import VisualUniDimensionalElement
from stableX.visualization.visual_element import VisualElement
from stableX.visualization.visual_rotational_spring_element import VisualRotationalSpringElement


def create_visual_element(element: Element) -> VisualElement:
    if isinstance(element, UniDimensionalElement):
        return VisualUniDimensionalElement(element)

    elif isinstance(element, LinearRotationalSpringElement):
        return VisualRotationalSpringElement(element)

    else:
        print("Element does not have a visual twin")

