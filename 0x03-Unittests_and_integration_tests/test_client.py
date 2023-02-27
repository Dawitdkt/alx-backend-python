#!/usr/bin/env python3
"""
This module contains the TestGithubOrgClient
class that tests the GithubOrgClient class.

The TestGithubOrgClient class inherits from
unittest.TestCase and uses the patch and
parameterized decorators to mock the get_json
function and parametrize the test cases.

The test_org method tests that
GithubOrgClient.org returns the correct
value for different org names.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """This class tests the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """Test that GithubOrgClient.org returns the correct value"""
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"name": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
