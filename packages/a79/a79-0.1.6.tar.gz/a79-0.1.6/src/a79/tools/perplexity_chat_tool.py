from typing import Any

from a79.client import get_client


# TODO: This class should be auto-generated
# We should also have pydantic models for the input and output
class PerplexityChatTool:
    """
    Tool for querying Perplexity AI with questions.

    This tool sends queries to Perplexity AI and returns the answers.
    """

    def __init__(self, input: list[dict[str, Any]]):
        """
        Initialize the PerplexityChatTool.

        Args:
            input: List of questions to send to Perplexity AI.
        """
        self.client = get_client()
        self.input = input
        self.outputs = self._execute()

    def _execute(self) -> dict[str, Any]:
        """
        Execute the Perplexity queries and return the results.

        Returns:
            Raw output from the Perplexity API call.
        """
        # Prepare the input for the API call
        tool_inputs = {"input": self.input}

        # Execute the Perplexity tool through the A79 API
        return self.client.execute_workflow_tool(
            tool_type=self.__class__.__name__, tool_inputs=tool_inputs
        )
