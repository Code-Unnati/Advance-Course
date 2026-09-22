import re
import tiktoken

class PromptCompressor:
    def __init__(self, model_name: str = "cl100k_base"):
        self.encoder = tiktoken.get_encoding(model_name)

    def count_tokens(self, text: str) -> int:
        """Return the exact number of tokens in the given text string."""
        return len(self.encoder.encode(text))

    def compress(self, prompt: str) -> str:
        """Clean redundant whitespace, extraneous markdown bullets, and filler conversational phrasing."""
        # 1. Normalize line breaks and multiple spaces
        text = re.sub(r"[ \t]+", " ", prompt)
        text = re.sub(r"\n\s*\n+", "\n", text).strip()

        # 2. Strip redundant conversational preamble
        filler_patterns = [
            r"^(please\s+)?can\s+you\s+(kindly\s+)?",
            r"^i\s+would\s+like\s+you\s+to\s+",
            r"^as\s+an\s+ai\s+assistant,\s*",
        ]
        for pattern in filler_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # 3. Capitalize the first character of the cleaned string
        if text:
            text = text[0].upper() + text[1:]
        return text

    def measure_compression_ratio(self, original_text: str) -> dict:
        """Measure token counts before and after compression to calculate percentage savings."""
        compressed = self.compress(original_text)
        orig_tokens = self.count_tokens(original_text)
        comp_tokens = self.count_tokens(compressed)
        savings = ((orig_tokens - comp_tokens) / orig_tokens * 100) if orig_tokens > 0 else 0.0

        return {
            "original_tokens": orig_tokens,
            "compressed_tokens": comp_tokens,
            "tokens_saved": orig_tokens - comp_tokens,
            "savings_percentage": round(savings, 2),
            "compressed_text": compressed
        }