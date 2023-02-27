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

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that returns the correct value"""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/google/repos"}
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url,
                         "https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        (
            "google",
            {"google-repo1", "google-repo2"}
        ),
        (
            "abc",
            {"abc-repo1", "abc-repo2"}
        )
    ])
    @patch('client.get_json')
    def test_public_repos(self, org_name, expected_repos, mock_get_json):
        """Test public repos method"""
        # create payload for get_json
        payload = [{"name": repo} for repo in expected_repos]

        # make get_json return payload
        mock_get_json.return_value = payload

        # create instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # use patch as context manager to mock _public_repos_url property
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=Mock) as mock_public_url:

            # make _public_repos_url return fake url
            mock_public_url.return_value = "https://fake.url"

            # call public_repos method on client instance
            repos = client.public_repos()

            # assert that repos is expected set of repo names
            self.assertEqual(repos, expected_repos)

            # assert that _public_repos_url was called once
            mock_public_url.assert_called_once()

            # assert that get_json was called once with fake url
            mock_get_json.assert_called_once_with("https://fake.url")

    @parameterized.expand([
        (
            {"license": {"key": "my_license"}},
            "my_license",
            True
        ),
        (
            {"license": {"key": "other_license"}},
            "my_license",
            False
        )
    ])
    def test_has_license(self, repo, license_key, expected_returned_value):
        """Test has_license method"""
        # create instance of GithubOrgClient with any org name
        client = GithubOrgClient("any_org")

        # call has_license method on client instance with repo and license_key
        result = client.has_license(repo, license_key)

        # assert that result is equal to expected_returned_value
        self.assertEqual(result, expected_returned_value)
