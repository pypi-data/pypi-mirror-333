"""
MindRoot API client implementation.
"""

import os
import requests
from typing import Dict, List, Optional, Union, Any

from .exceptions import MindRootError


class MindRootClient:
    """Client for interacting with the MindRoot API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: int = 300):
        """
        Initialize the MindRoot API client.

        Args:
            api_key: API key for authentication. If not provided, will try to get from MINDROOT_API_KEY env variable.
            base_url: Base URL of the MindRoot API server. Must be provided, typically 'http://localhost:8010' for local instances.
            timeout: Request timeout in seconds. Default is 300 (5 minutes).

        Raises:
            ValueError: If no API key is provided or found in environment variables.
            ValueError: If no base_url is provided.
        """
        self.api_key = api_key or os.environ.get("MINDROOT_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as MINDROOT_API_KEY environment variable")
        
        if not base_url:
            raise ValueError("base_url must be provided (e.g., 'http://localhost:8010')")
            
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def run_task(self, agent_name: str, instructions: str, include_trace: bool = False) -> Dict[str, Any]:
        """
        Execute a task with the specified agent using the provided instructions.

        Args:
            agent_name: Name of the agent to run the task.
            instructions: Instructions or prompt for the agent.
            include_trace: Whether to include the full trace of commands in the result. Default is False.

        Returns:
            Dict containing the task results:
            - If include_trace is False, returns only the final textual result.
            - If include_trace is True, returns a dict with 'results' and 'full_results' keys.

        Raises:
            MindRootError: If the API returns an error or if the request fails.
            requests.RequestException: For network-related errors.
        """
        url = f"{self.base_url}/task/{agent_name}"
        params = {"api_key": self.api_key}
        payload = {"instructions": instructions}

        try:
            response = requests.post(
                url,
                params=params,
                json=payload,
                timeout=self.timeout
            )
            
            # Raise exception for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            if result.get("status") == "error":
                raise MindRootError(result.get("message", "Unknown error from MindRoot API"))
                
            # Return either just the results or the full response
            if include_trace:
                return {
                    "results": result.get("results", ""),
                    "full_results": result.get("full_results", []),
                    "log_id": result.get("log_id", "")
                }
            else:
                return {"results": result.get("results", "")}
                
        except requests.RequestException as e:
            raise MindRootError(f"Request failed: {str(e)}")
