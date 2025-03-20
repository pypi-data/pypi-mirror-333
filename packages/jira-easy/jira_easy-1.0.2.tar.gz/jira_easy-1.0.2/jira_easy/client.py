import requests

class JIRAClient:
    """
    A simple JIRA client for fetching and creating issues via the REST API.
    """

    def __init__(self, jira_url: str, api_token: str):
        """
        Initialize the JIRA client with the base URL and API token.

        :param jira_url: The JIRA REST API base URL 
                         (e.g., 'https://your-domain.atlassian.net/rest/api/2')
        :param api_token: A valid personal access token or API token for authentication
        """
        self.jira_url = jira_url.rstrip("/")  # remove trailing slash if present
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def fetch_issues(self, jql: str, start_at: int = 0, max_results: int = 50) -> list:
        """
        Fetch issues from JIRA using a JQL query.

        :param jql: A valid JQL string (e.g., 'project = TEST AND status = Open')
        :param start_at: The index of the first issue to return
        :param max_results: Maximum number of issues to return per call
        :return: A list of issue objects
        """
        issues = []
        while True:
            search_url = f"{self.jira_url}/search"
            params = {
                "jql": jql,
                "startAt": start_at,
                "maxResults": max_results,
                "fields": "summary,status,assignee,created,description,issuetype,priority"
            }
            response = requests.get(search_url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                batch = data.get("issues", [])
                issues.extend(batch)
                if len(batch) < max_results:
                    break
                start_at += max_results
            else:
                raise Exception(
                    f"Failed to fetch issues. "
                    f"Status code: {response.status_code}. Response: {response.text}"
                )
        return issues

    def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Task",
        priority: str = None
    ) -> dict:
        """
        Create a new issue in JIRA.

        :param project_key: The key of the project (e.g. 'ABC')
        :param summary: The summary/title of the issue
        :param description: The description of the issue
        :param issue_type: The type of the issue (e.g. 'Bug', 'Task', 'Story')
        :param priority: The priority name (e.g. 'Highest', 'High', 'Medium', etc.)
        :return: The newly created issue's JSON response from JIRA
        """
        create_issue_url = f"{self.jira_url}/issue"

        # Base fields
        fields_data = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }

        # If a priority is specified, add it to the fields
        if priority:
            fields_data["priority"] = {"name": priority}

        payload = {"fields": fields_data}

        response = requests.post(create_issue_url, headers=self.headers, json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(
                f"Failed to create issue. Status code: {response.status_code}, "
                f"Response: {response.text}"
            )
