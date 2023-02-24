#!/usr/bin/env python3

"""doc goes here"""
import unittest
from unittest import mock
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
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
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: any):
        """test the access_nested_map method of utils"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a", )),
        ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence):
        self.assertRaises(KeyError, access_nested_map, nested_map, path)


class TestClass:

    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()

# This is your test case for TestClass


class TestMemoize(unittest.TestCase):
    class TestClass:

        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    # Use patch to mock out a_method
    @mock.patch('TestClass.a_method')
    def test_memoize(self, mock_a_method):
        # Set the return value of the mock to 42
        mock_a_method.return_value = 42
        # Create an instance of TestClass
        test_class = TestClass()
        # Call a_property twice and assert that it returns 42 both times
        self.assertEqual(test_class.a_property(), 42)
        self.assertEqual(test_class.a_property(), 42)
        # Assert that a_method was called only once
        mock_a_method.assert_called_once()
