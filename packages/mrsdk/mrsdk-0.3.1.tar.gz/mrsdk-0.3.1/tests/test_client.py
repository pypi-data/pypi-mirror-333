"""
Tests for the MindRoot SDK client.
"""

import pytest
from unittest.mock import patch, MagicMock
import requests
import os

from mrsdk import MindRootClient, MindRootError


class TestMindRootClient:
    """Test suite for the MindRootClient class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a test API key for testing
        os.environ["MINDROOT_API_KEY"] = "test-api-key"
        # Create client with required base_url
        self.client = MindRootClient(base_url="http://localhost:8010")
        
    def teardown_method(self):
        """Tear down test fixtures."""
        # Remove test API key
        if "MINDROOT_API_KEY" in os.environ:
            del os.environ["MINDROOT_API_KEY"]
    
    def test_init_with_api_key(self):
        """Test initialization with explicit API key."""
        client = MindRootClient(api_key="my-custom-key", base_url="http://localhost:8010")
        assert client.api_key == "my-custom-key"
        assert client.base_url == "http://localhost:8010"
        assert client.timeout == 300
    
    def test_init_with_env_var(self):
        """Test initialization with API key from environment variable."""
        assert self.client.api_key == "test-api-key"
        assert self.client.base_url == "http://localhost:8010"
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        if "MINDROOT_API_KEY" in os.environ:
            del os.environ["MINDROOT_API_KEY"]
            
        with pytest.raises(ValueError) as excinfo:
            MindRootClient(base_url="http://localhost:8010")
        assert "API key must be provided" in str(excinfo.value)
    
    def test_init_without_base_url(self):
        """Test initialization without base_url raises error."""
        with pytest.raises(ValueError) as excinfo:
            MindRootClient(api_key="test-key")
        assert "base_url must be provided" in str(excinfo.value)
    
    def test_init_with_custom_url_and_timeout(self):
        """Test initialization with custom URL and timeout."""
        client = MindRootClient(
            api_key="test-key",
            base_url="https://custom.mindroot.com",
            timeout=600
        )
        assert client.base_url == "https://custom.mindroot.com"
        assert client.timeout == 600
    
    def test_run_task_success(self):
        """Test successful task execution."""
        # Mock response for successful API call
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "results": "Task result",
            "full_results": [{"cmd": "test_cmd", "result": "test_result"}],
            "log_id": "test-log-id"
        }
        
        with patch("requests.post", return_value=mock_response) as mock_post:
            result = self.client.run_task("Assistant", "Test instructions")
            
            # Check that the API was called correctly
            mock_post.assert_called_once_with(
                "http://localhost:8010/task/Assistant",
                params={"api_key": "test-api-key"},
                json={"instructions": "Test instructions"},
                timeout=300
            )
            
            # Check the result
            assert result == {"results": "Task result"}
    
    def test_run_task_with_trace(self):
        """Test task execution with trace included."""
        # Mock response for successful API call
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "results": "Task result",
            "full_results": [{"cmd": "test_cmd", "result": "test_result"}],
            "log_id": "test-log-id"
        }
        
        with patch("requests.post", return_value=mock_response) as mock_post:
            result = self.client.run_task("Assistant", "Test instructions", include_trace=True)
            
            # Check the result includes full trace
            assert result == {
                "results": "Task result",
                "full_results": [{"cmd": "test_cmd", "result": "test_result"}],
                "log_id": "test-log-id"
            }
    
    def test_run_task_api_error(self):
        """Test handling of API error response."""
        # Mock response for API error
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "error",
            "message": "API error message"
        }
        
        with patch("requests.post", return_value=mock_response) as mock_post:
            with pytest.raises(MindRootError) as excinfo:
                self.client.run_task("Assistant", "Test instructions")
            
            assert "API error message" in str(excinfo.value)
    
    def test_run_task_network_error(self):
        """Test handling of network error."""
        with patch("requests.post", side_effect=requests.RequestException("Network error")) as mock_post:
            with pytest.raises(MindRootError) as excinfo:
                self.client.run_task("Assistant", "Test instructions")
            
            assert "Request failed: Network error" in str(excinfo.value)
