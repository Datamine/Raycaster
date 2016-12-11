# -*- coding: utf-8 -*-
# John Loeber | Dec 11 2016 | Python 2.7.12 | contact@johnloeber.com

import unittest
from Raytracer_Helpers import raytracer_plumbing as plumbing

class PlumbingTests(unittest.TestCase):
    """
    tests for raytracer_plumbing.py
    """
    def test_sort_contacts(self):
        self.assertEqual(5+3, 8)

if __name__ == '__main__':
    unittest.main()
