#!/usr/bin/env python3

"""doc goes here"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a", ), 1),
        ({"a": {"b": 2}}, ("a", ), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)])
    def test_access_nested_map(self,nested_map: Mapping, path: Sequence, expected:any):
        """test the access_nested_map method of utils"""
        self.assertEqual(access_nested_map(nested_map, path),expected)
