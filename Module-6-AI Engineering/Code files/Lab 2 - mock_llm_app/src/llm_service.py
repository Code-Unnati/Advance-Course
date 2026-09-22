import requests
from typing import Dict, Any

class LLMBaseException(Exception):
    """Base exception for LLM communication failures."""
    pass

class LLMRateLimitError(LLMBaseException):
    """Raised when the LLM provider returns an HTTP 429 status."""
    pass

class LLMServiceUnavailableError(LLMBaseException):
    """Raised when the LLM provider experiences timeouts or 5xx outages."""
    pass

class CustomerFeedbackClassifier:
    def __init__(self, api_key: str, endpoint_url: str):
        self.api_key = api_key
        self.endpoint_url = endpoint_url

    def _post_inference(self, prompt: str) -> Dict[str, Any]:
        """Send inference request to external API with explicit timeouts and error interception."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"prompt": prompt, "temperature": 0.0}

        try:
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                json=payload,
                timeout=3.0
            )
        except requests.exceptions.Timeout:
            raise LLMServiceUnavailableError("Inference request timed out after 3.0 seconds.")
        except requests.exceptions.ConnectionError:
            raise LLMServiceUnavailableError("Failed to establish connection to LLM API provider.")

        if response.status_code == 429:
            raise LLMRateLimitError("API quota or rate limit exceeded.")
        elif response.status_code >= 500:
            raise LLMServiceUnavailableError(f"Upstream provider error: HTTP {response.status_code}")
        elif response.status_code != 200:
            raise LLMBaseException(f"Unexpected API error: HTTP {response.status_code} - {response.text}")

        return response.json()

    def classify_urgency(self, feedback_text: str) -> str:
        """Classify user feedback into HIGH, MEDIUM, or LOW urgency with safe fallbacks."""
        prompt = f"Classify the urgency of this support feedback as HIGH, MEDIUM, or LOW: {feedback_text}"

        try:
            data = self._post_inference(prompt)
            # Parse target response string from completion payload
            label = data.get("choices", [{}])[0].get("text", "").strip().upper()
            
            if label not in ["HIGH", "MEDIUM", "LOW"]:
                return "MANUAL_REVIEW"
            return label

        except LLMRateLimitError:
            # Fallback when rate-limited: queue for delayed background batch processing
            return "QUEUED_FOR_RETRY"

        except LLMServiceUnavailableError:
            # Fallback during provider outage: route directly to manual review triage
            return "MANUAL_REVIEW"