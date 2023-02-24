#!/usr/bin/env python3

"""doc goes here"""

from email.headerregistry import ParameterizedMIMEHeader
import unittest

from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    
    @ParameterizedMIMEHeader.expand([({"a": 1},("a",),1),({"a": {"b": 2}},("a",),{'b': 2}),{"a": {"b": 2}}, ("a", "b"),2])
    def test_access_nested_map(self):
        """test the access_nested_map method of utils"""
        self.assertTrue(access_nested_map(nested_map={"a": 1}, path=("a",)))