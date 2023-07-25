import unittest
from stableX import Rectangle


class TestRectangularSection(unittest.TestCase):
    def setUp(self):
        self.rectangular_section = Rectangle(100, 150)

    def test_area(self):
        self.assertEqual(self.rectangular_section.area, 15000)

    def test_inertia(self):
        self.assertEqual(self.rectangular_section.inertia, 28125000)
