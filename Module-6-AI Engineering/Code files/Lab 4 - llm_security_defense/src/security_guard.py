import regex as re
from typing import Tuple, Dict, Any, List

class SecurityViolationError(Exception):
    """Raised when an adversarial prompt injection or security policy violation is detected."""
    pass

class SecurityGuard:
    def __init__(self):
        # Precompiled regex patterns for standard PII entities
        self.pii_patterns = {
            "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"),
            "PHONE": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
            "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "CREDIT_CARD": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")
        }

        # Signatures commonly associated with prompt injections and jailbreaks
        self.injection_signatures = [
            re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+(instructions|prompts|directives)", re.IGNORECASE),
            re.compile(r"system\s*prompt\s*override", re.IGNORECASE),
            re.compile(r"you\s+are\s+now\s+(in\s+developer\s+mode|dan|unrestricted)", re.IGNORECASE),
            re.compile(r"disregard\s+(the\s+above|all\s+safety\s+rules)", re.IGNORECASE),
            re.compile(r"print\s+(your\s+)?(system\s+instructions|initial\s+prompt)", re.IGNORECASE),
            re.compile(r"bypass\s+(all\s+)?(content\s+filters|moderation)", re.IGNORECASE)
        ]

    def redact_pii(self, text: str) -> Tuple[str, Dict[str, int]]:
        """Identify PII entities and replace them with standard redaction tokens."""
        redacted_text = text
        redaction_counts = {}

        for pii_type, pattern in self.pii_patterns.items():
            matches = pattern.findall(redacted_text)
            if matches:
                redaction_counts[pii_type] = len(matches)
                redacted_text = pattern.sub(f"[REDACTED_{pii_type}]", redacted_text)

        return redacted_text, redaction_counts

    def detect_prompt_injection(self, text: str) -> bool:
        """Scan input for recognized adversarial injection and jailbreak signatures."""
        for signature in self.injection_signatures:
            if signature.search(text):
                return True
        return False

    def validate_and_sanitize_input(self, user_input: str) -> str:
        """Validate input against injection attacks and redact any PII prior to model consumption."""
        if self.detect_prompt_injection(user_input):
            raise SecurityViolationError("Potential prompt injection attack detected. Input rejected.")
        
        sanitized_input, _ = self.redact_pii(user_input)
        return sanitized_input

    def sanitize_output(self, model_output: str) -> str:
        """Sanitize LLM completions to ensure no PII is accidentally leaked to the client."""
        sanitized_output, _ = self.redact_pii(model_output)
        return sanitized_output