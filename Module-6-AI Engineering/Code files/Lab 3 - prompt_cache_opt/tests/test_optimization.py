import pytest
import time
from src.compressor import PromptCompressor
from src.semantic_cache import SemanticCache

@pytest.fixture
def compressor():
    return PromptCompressor()

@pytest.fixture
def cache():
    return SemanticCache(similarity_threshold=0.75)

def test_prompt_compression_token_reduction(compressor):
    """Ensure compressor strips formatting bloat and reduces token usage."""
    verbose_prompt = (
        "Please can you kindly   summarize the following enterprise contract\n\n\n"
        "for our legal review team?    Make sure to highlight all payment terms."
    )
    result = compressor.measure_compression_ratio(verbose_prompt)
    
    assert result["tokens_saved"] > 0
    assert result["compressed_tokens"] < result["original_tokens"]
    assert "Summarize the following enterprise contract" in result["compressed_text"]

def test_semantic_cache_hit_on_paraphrased_query(cache):
    """Ensure cache hits when a query is rephrased with identical meaning."""
    # Seed cache with baseline interaction
    cache.store(
        user_query="How do I reset my account password?",
        response="Navigate to Settings -> Security -> Reset Password."
    )

    # Paraphrased incoming request
    paraphrased = "What are the steps to change my login password?"
    response, score, is_hit = cache.query(paraphrased)

    assert is_hit is True
    assert score >= 0.75
    assert response == "Navigate to Settings -> Security -> Reset Password."

def test_semantic_cache_miss_on_different_topic(cache):
    """Ensure cache misses when the incoming query is unrelated."""
    cache.store(
        user_query="How do I cancel my subscription?",
        response="Go to Billing and click Cancel Subscription."
    )

    unrelated_query = "What is the company headquarters phone number?"
    response, score, is_hit = cache.query(unrelated_query)

    assert is_hit is False
    assert response is None

def test_latency_comparison(cache):
    """Verify that a cache hit retrieves results significantly faster than an API call simulation."""
    cache.store("Explain gradient descent.", "Gradient descent is an optimization algorithm...")

    # Simulated LLM network call latency: 600ms
    simulated_api_latency = 0.600

    # Measure cache retrieval time
    start = time.perf_counter()
    response, _, is_hit = cache.query("Can you explain how gradient descent works?")
    cache_duration = time.perf_counter() - start

    assert is_hit is True
    assert cache_duration < 0.050, f"Cache retrieval was too slow: {cache_duration}s"
    assert cache_duration < simulated_api_latency