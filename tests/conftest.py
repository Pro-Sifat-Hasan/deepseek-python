"""Pytest configuration and fixtures"""
import pytest


@pytest.fixture
def sample_messages():
    """Fixture providing sample chat messages"""
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]


@pytest.fixture
def api_key():
    """Fixture providing a test API key"""
    return "test_api_key_12345"


@pytest.fixture
def custom_base_url():
    """Fixture providing a custom base URL"""
    return "https://custom.api.deepseek.com"
