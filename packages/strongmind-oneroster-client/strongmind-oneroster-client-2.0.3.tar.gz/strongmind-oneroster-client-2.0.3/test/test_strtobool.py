#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

import unittest

from oneroster_client.api_client import strtobool


class TestStrtobool(unittest.TestCase):
    """Test case for the strtobool function"""

    def test_true_values(self):
        """Test true values are correctly identified."""
        true_values = ['y', 'yes', 't', 'true', 'on', '1', 
                       'Y', 'YES', 'T', 'TRUE', 'ON', '1']
        for val in true_values:
            with self.subTest(val=val):
                self.assertEqual(strtobool(val), 1)
                self.assertTrue(bool(strtobool(val)))

    def test_false_values(self):
        """Test false values are correctly identified."""
        false_values = ['n', 'no', 'f', 'false', 'off', '0',
                        'N', 'NO', 'F', 'FALSE', 'OFF', '0']
        for val in false_values:
            with self.subTest(val=val):
                self.assertEqual(strtobool(val), 0)
                self.assertFalse(bool(strtobool(val)))

    def test_invalid_values(self):
        """Test invalid values raise ValueError."""
        invalid_values = ['maybe', 'perhaps', '2', '-1', 'truish', 'falsy']
        for val in invalid_values:
            with self.subTest(val=val):
                with self.assertRaises(ValueError):
                    strtobool(val)


if __name__ == '__main__':
    unittest.main() 