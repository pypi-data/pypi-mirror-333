import os

import requests


def get_client() -> "A79Client":
    """
    Create an A79Client instance using environment variables.

    Returns:
        A79Client: Configured client instance

    Raises:
        ValueError: If A79_API_KEY is not set in environment variables
    """
    api_key = os.environ.get("A79_API_KEY")
    if not api_key:
        raise ValueError("A79_API_KEY environment variable must be set")

    api_url = os.environ.get("A79_API_URL", "https://app.a79.ai")

    return A79Client(api_url=api_url, api_key=api_key)


class A79Client:
    """Simple HTTP client for interacting with A79 API."""

    def __init__(self, *, api_url: str, api_key: str):
        """
        Initialize the A79 API client.

        Args:
            api_url: Base URL for A79 API
            api_key: API key for authentication
        """
        self.base_url = api_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def execute_workflow_tool(self, *, tool_type: str, tool_inputs: dict) -> dict:
        """
        Execute a workflow tool directly.

        Args:
            tool_type: The type identifier of the tool to instantiate
            tool_inputs: Dictionary of input values for the tool

        Returns:
            dict: The result of the tool execution

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/api/v1/workflow/tool/execute"
        response = requests.post(
            url,
            json={"tool_type": tool_type, "tool_inputs": tool_inputs},
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()
