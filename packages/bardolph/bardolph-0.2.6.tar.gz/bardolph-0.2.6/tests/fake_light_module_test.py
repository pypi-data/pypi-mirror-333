#!/usr/bin/env python

import unittest

from bardolph.controller import i_controller
from bardolph.lib.injection import provide

from tests import test_module


class FakeLightModuleTest(unittest.TestCase):
    def setUp(self):
        test_module.configure()

    def test_large_set(self):
        light_set = provide(i_controller.LightSet)
        self.assertIsNotNone(light_set)
        self.assertEqual(light_set.get_light_count(), 15)
        self.assertListEqual(light_set.get_light('table-3').get_color(),
                             [0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
