import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
# from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        # create an instance of GithubOrgClient with org_name
        test_client = GithubOrgClient(org_name)
        # call org method
        test_client.org()
        # assert that get_json is called once with expected argument
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        # mock get_json return value
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload

        # mock _public_repos_url property
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_public_url:
            # set return value for property
            mock_public_url.return_value = "https://fake_url"

            # instantiate client object
            client = GithubOrgClient("test_org")

            # call public_repos method
            repos = client.public_repos()

            # assert expected list of repos
            self.assertEqual(repos, ["repo1", "repo2"])

            # assert mocked property was called once
            mock_public_url.assert_called_once()

            # assert mocked get_json was called once with expected url argument
            mock_get_json.assert_called_once_with("https://fake_url")

        @parameterized.expand([
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False)
        ])
        @patch('client.get_json')
        def test_has_license(self, repo, license_key, expected):
            """Test has_license method"""
            # mock get_json return value
            mock_get_json.return_value = repo

            # instantiate client object
            client = GithubOrgClient("test_org")

            # call has_license method with license_key argument
            result = client.has_license(license_key)

            # assert expected boolean value
            self.assertEqual(result, expected)

            # assert mocked get_json was called once with expected url argument
            mock_get_json.assert_called_once_with(
                f"https://api.github.com/repos/test_org/{repo['name']}")


# @parameterized_class([
#     {'org_payload': org_payload,
#      'repos_payload': repos_payload,
#      'expected_repos': expected_repos,
#      'apache2_repos': apache2_repos}
# ])
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.get_patcher = patch('requests.get')
#         cls.get = cls.get_patcher.start()

#         def side_effect(url):
#             if url == 'https://api.github.com/orgs/google':
#                 return MockResponse(org_payload)
#             if url == 'https://api.github.com/orgs/google/repos':
#                 return MockResponse(repos_payload)
#             if url.startswith('https://api.github.com/repos/google'):
#                 repo_name = url.split('/')[-1]
#                 return MockResponse(apache2_repos[repo_name])

#         cls.get.side_effect = side_effect

#     @classmethod
#     def tearDownClass(cls):
#         cls.get_patcher.stop()

#     def test_public_repos(self):
#         """Test that public_repos returns expected repos"""
#         result = self.client.public_repos()
#         self.assertEqual(result, self.expected_repos)
#         self.get.assert_called_once_with(
#             'https://api.github.com/orgs/google/repos')
