import math
import unittest
from stableX import Node, Rectangle
from tests.elements.unidimensional_elements.unidimensional_element_subclass import UniDimensionalElementSubClass


class TestUniDimensionalElement(unittest.TestCase):

    def setUp(self):
        self.start_node = Node(1, 1)
        self.end_node = Node(2, 2)
        self.section = Rectangle(100, 200)
        self.element = UniDimensionalElementSubClass(self.start_node,
                                                     self.end_node, self.section)

    def test_length(self):
        self.assertEqual(self.element.length, math.sqrt(2))
