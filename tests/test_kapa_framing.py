import math
import unittest

import numpy as np

from scripts.kapa_framing import make_frame, polygon_area


class FrameGeometryTests(unittest.TestCase):
    def setUp(self):
        self.rectangle = np.array([[0., 0.], [2., 0.], [2., 8.], [0., 8.], [0., 0.]])

    def test_landscape_fits_entire_tall_rectangle(self):
        frame = make_frame(self.rectangle, 0., 1.5, 0.)
        self.assertAlmostEqual(frame['width_m'], 12.)
        self.assertAlmostEqual(frame['height_m'], 8.)
        self.assertAlmostEqual(frame['airport_area_fraction'], 1 / 6)

    def test_turning_long_axis_horizontal_preserves_full_rectangle(self):
        frame = make_frame(self.rectangle, math.pi / 2, 1.5, 0.)
        self.assertAlmostEqual(frame['width_m'], 8.)
        self.assertAlmostEqual(frame['height_m'], 8 / 1.5)
        self.assertAlmostEqual(polygon_area(frame['corners']), 8 * 8 / 1.5)

    def test_margin_is_added_on_both_sides(self):
        frame = make_frame(self.rectangle, 0., 1.5, .1)
        self.assertAlmostEqual(frame['width_m'], 14.4)
        self.assertAlmostEqual(frame['height_m'], 9.6)

    def test_utm_translation_does_not_change_frame_dimensions_or_area(self):
        shift = np.array([500000., 4380000.])
        plain = make_frame(self.rectangle, .37, 1.5, .1)
        moved = make_frame(self.rectangle + shift, .37, 1.5, .1)
        self.assertAlmostEqual(plain['width_m'], moved['width_m'], places=7)
        self.assertAlmostEqual(plain['height_m'], moved['height_m'], places=7)
        self.assertAlmostEqual(polygon_area(self.rectangle + shift), 16.)
        np.testing.assert_allclose(moved['corners'] - shift, plain['corners'], atol=1e-8)


if __name__ == '__main__':
    unittest.main()
