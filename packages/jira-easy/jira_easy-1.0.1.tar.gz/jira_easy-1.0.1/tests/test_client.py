import unittest
from jira_easy import JIRAClient

class TestJIRAClient(unittest.TestCase):
    def setUp(self):
        # Use placeholder values for testing
        self.jira_url = "https://dummy-jira-instance.atlassian.net/rest/api/2/search"
        self.api_token = "dummy_api_token"
        self.client = JIRAClient(self.jira_url, self.api_token)

    def test_initialization(self):
        """
        Ensure the client initializes with correct URL and token.
        """
        self.assertEqual(self.client.jira_url, self.jira_url)
        self.assertEqual(self.client.api_token, self.api_token)
        self.assertIn("Authorization", self.client.headers)

if __name__ == "__main__":
    unittest.main()
