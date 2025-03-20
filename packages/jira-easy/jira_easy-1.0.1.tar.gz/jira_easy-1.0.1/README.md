# jira_easy

A simple Python library that performs basic JIRA operations (like fetching and creating issues via JQL).

## Installation

Install directly from source:
```bash
pip install jira_easy
```

## Usage

# Fetching

```python
from jira_easy import JIRAClient

# Provide your JIRA URL and API token
jira_url = "https://your-jira-instance.atlassian.net/rest/api/2/search"
api_token = "YOUR_JIRA_API_TOKEN"

# Initialize the client
client = JIRAClient(jira_url, api_token)

# Define your JQL query
jql_query = 'project = "PROJ" AND status = "Open" ORDER BY key ASC'

# Fetch issues matching the query
issues = client.fetch_issues(jql_query)
print(f"Number of issues found: {len(issues)}")
for issue in issues:
    print(issue.get("key"), "-", issue["fields"].get("summary"))
```

# Creating

```python
from jira_easy import JIRAClient

# Use your actual JIRA URL base (without /search or /issue appended).
# Example: "https://your-domain.atlassian.net/rest/api/2"
jira_base_url = "https://your-domain.atlassian.net/rest/api/2"
api_token = "YOUR_JIRA_API_TOKEN"

# Initialize the JIRA client
client = JIRAClient(jira_base_url, api_token)

# Create a new issue with a specified priority
created_issue = client.create_issue(
    project_key="MYPROJECT",
    summary="Bug: App crashing on startup",
    description="Steps to reproduce...\n1. ...\n2. ...\netc.",
    issue_type="Bug",
    priority="High"
)

# The response JSON contains details about the new issue
print("New issue key:", created_issue.get("key"))

```