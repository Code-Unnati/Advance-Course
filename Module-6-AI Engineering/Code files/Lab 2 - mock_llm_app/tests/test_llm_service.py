import pytest
from unittest.mock import patch, MagicMock
import requests
from src.llm_service import (
    CustomerFeedbackClassifier,
    LLMRateLimitError,
    LLMServiceUnavailableError,
    LLMBaseException
)

@pytest.fixture
def classifier():
    """Provides a fresh classifier instance configured with mock credentials."""
    return CustomerFeedbackClassifier(
        api_key="mocked-test-api-token",
        endpoint_url="https://api.mock-provider.internal/v1/completions"
    )

@patch("src.llm_service.requests.post")
def test_successful_classification(mock_post, classifier):
    """Verify standard positive API response parses the urgency tag correctly."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [{"text": "HIGH"}]
    }
    mock_post.return_value = mock_resp

    result = classifier.classify_urgency("System is down and data is corrupt!")

    assert result == "HIGH"
    mock_post.assert_called_once()
    
    # Assert header and payload structure
    sent_headers = mock_post.call_args[1]["headers"]
    sent_json = mock_post.call_args[1]["json"]
    assert sent_headers["Authorization"] == "Bearer mocked-test-api-token"
    assert "System is down and data is corrupt!" in sent_json["prompt"]

@patch("src.llm_service.requests.post")
def test_rate_limit_triggers_queued_fallback(mock_post, classifier):
    """Verify HTTP 429 returns the fallback QUEUED_FOR_RETRY status."""
    mock_resp = MagicMock()
    mock_resp.status_code = 429
    mock_resp.text = "Too Many Requests"
    mock_post.return_value = mock_resp

    result = classifier.classify_urgency("App is loading slowly.")
    assert result == "QUEUED_FOR_RETRY"

@patch("src.llm_service.requests.post")
def test_network_timeout_triggers_manual_review_fallback(mock_post, classifier):
    """Verify request timeouts trigger the MANUAL_REVIEW fallback."""
    mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")

    result = classifier.classify_urgency("Cannot login to dashboard.")
    assert result == "MANUAL_REVIEW"

@patch("src.llm_service.requests.post")
def test_server_500_error_triggers_manual_review_fallback(mock_post, classifier):
    """Verify upstream 500 server errors are caught and trigger fallback handling."""
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.text = "Internal Server Error"
    mock_post.return_value = mock_resp

    result = classifier.classify_urgency("Please help with billing.")
    assert result == "MANUAL_REVIEW"

@patch("src.llm_service.requests.post")
def test_malformed_model_completion_handling(mock_post, classifier):
    """Verify unexpected responses (hallucinations or conversational filler) route to manual review."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [{"text": "I am an AI assistant and I cannot determine this."}]
    }
    mock_post.return_value = mock_resp

    result = classifier.classify_urgency("Payment question.")
    assert result == "MANUAL_REVIEW"