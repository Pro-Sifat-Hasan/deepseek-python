"""Tests for DeepSeekClient"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from deepseek import DeepSeekClient, DeepSeekError, DeepSeekAPIError


class TestDeepSeekClientInit:
    """Test client initialization"""

    def test_client_initialization(self):
        """Test basic client initialization"""
        client = DeepSeekClient(api_key="test_key")
        assert client.default_model == "deepseek-chat"
        assert client.client is not None
        assert client.async_client is not None

    def test_client_custom_base_url(self):
        """Test client with custom base URL"""
        client = DeepSeekClient(
            api_key="test_key",
            base_url="https://custom.api.com"
        )
        assert client.client.base_url == "https://custom.api.com"

    def test_client_custom_model(self):
        """Test client with custom default model"""
        client = DeepSeekClient(
            api_key="test_key",
            default_model="deepseek-coder"
        )
        assert client.default_model == "deepseek-coder"


class TestChatCompletion:
    """Test synchronous chat completion"""

    @patch('deepseek.deepseek.OpenAI')
    def test_chat_completion_basic(self, mock_openai):
        """Test basic chat completion"""
        # Setup mock
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        # Test
        client = DeepSeekClient(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        response = client.chat_completion(messages=messages)

        # Verify
        assert response is not None
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['model'] == "deepseek-chat"
        assert call_kwargs['messages'] == messages
        assert call_kwargs['temperature'] == 0.7
        assert call_kwargs['stream'] is False

    @patch('deepseek.deepseek.OpenAI')
    def test_chat_completion_custom_params(self, mock_openai):
        """Test chat completion with custom parameters"""
        # Setup mock
        mock_client = Mock()
        mock_response = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        # Test
        client = DeepSeekClient(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        response = client.chat_completion(
            messages=messages,
            model="custom-model",
            temperature=0.5,
            max_tokens=100
        )

        # Verify
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['model'] == "custom-model"
        assert call_kwargs['temperature'] == 0.5
        assert call_kwargs['max_tokens'] == 100

    @patch('deepseek.deepseek.OpenAI')
    def test_chat_completion_api_error(self, mock_openai):
        """Test chat completion error handling"""
        # Setup mock to raise exception
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client

        # Test
        client = DeepSeekClient(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        
        with pytest.raises(DeepSeekAPIError) as exc_info:
            client.chat_completion(messages=messages)
        
        assert "API Error" in str(exc_info.value)


class TestAsyncChatCompletion:
    """Test asynchronous chat completion"""

    @pytest.mark.asyncio
    @patch('deepseek.deepseek.AsyncOpenAI')
    async def test_async_chat_completion_basic(self, mock_async_openai):
        """Test basic async chat completion"""
        # Setup mock
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_async_openai.return_value = mock_client

        # Test
        client = DeepSeekClient(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        response = await client.async_chat_completion(messages=messages)

        # Verify
        assert response is not None
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['model'] == "deepseek-chat"
        assert call_kwargs['messages'] == messages

    @pytest.mark.asyncio
    @patch('deepseek.deepseek.AsyncOpenAI')
    async def test_async_chat_completion_error(self, mock_async_openai):
        """Test async chat completion error handling"""
        # Setup mock to raise exception
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
        mock_async_openai.return_value = mock_client

        # Test
        client = DeepSeekClient(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        
        with pytest.raises(DeepSeekAPIError) as exc_info:
            await client.async_chat_completion(messages=messages)
        
        assert "API Error" in str(exc_info.value)


class TestStreamResponse:
    """Test streaming responses"""

    @patch('deepseek.deepseek.OpenAI')
    def test_stream_response(self, mock_openai):
        """Test streaming response"""
        # Setup mock
        mock_client = Mock()
        mock_chunk1 = Mock()
        mock_chunk1.choices = [Mock(delta=Mock(content="Hello"))]
        mock_chunk2 = Mock()
        mock_chunk2.choices = [Mock(delta=Mock(content=" World"))]
        
        mock_client.chat.completions.create.return_value = iter([mock_chunk1, mock_chunk2])
        mock_openai.return_value = mock_client

        # Test
        client = DeepSeekClient(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        
        chunks = list(client.stream_response(messages=messages))
        
        # Verify
        assert len(chunks) == 2
        assert chunks[0] == mock_chunk1
        assert chunks[1] == mock_chunk2
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['stream'] is True

    @patch('deepseek.deepseek.OpenAI')
    def test_stream_response_error(self, mock_openai):
        """Test streaming response error handling"""
        # Setup mock to raise exception
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("Stream Error")
        mock_openai.return_value = mock_client

        # Test
        client = DeepSeekClient(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        
        with pytest.raises(DeepSeekAPIError) as exc_info:
            list(client.stream_response(messages=messages))
        
        assert "Stream Error" in str(exc_info.value)


class TestAsyncStreamResponse:
    """Test async streaming responses"""

    @pytest.mark.asyncio
    @patch('deepseek.deepseek.AsyncOpenAI')
    async def test_async_stream_response(self, mock_async_openai):
        """Test async streaming response"""
        # Setup mock
        mock_client = Mock()
        mock_chunk1 = Mock()
        mock_chunk1.choices = [Mock(delta=Mock(content="Hello"))]
        mock_chunk2 = Mock()
        mock_chunk2.choices = [Mock(delta=Mock(content=" World"))]
        
        async def async_generator():
            yield mock_chunk1
            yield mock_chunk2
        
        mock_stream = Mock()
        mock_stream.__aiter__ = lambda self: async_generator()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_stream)
        mock_async_openai.return_value = mock_client

        # Test
        client = DeepSeekClient(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        
        chunks = []
        async for chunk in client.async_stream_response(messages=messages):
            chunks.append(chunk)
        
        # Verify
        assert len(chunks) == 2
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['stream'] is True


class TestExceptions:
    """Test custom exceptions"""

    def test_deepseek_error_hierarchy(self):
        """Test exception hierarchy"""
        assert issubclass(DeepSeekAPIError, DeepSeekError)
        assert issubclass(DeepSeekError, Exception)

    def test_raise_deepseek_error(self):
        """Test raising DeepSeekError"""
        with pytest.raises(DeepSeekError) as exc_info:
            raise DeepSeekError("Test error")
        assert str(exc_info.value) == "Test error"

    def test_raise_deepseek_api_error(self):
        """Test raising DeepSeekAPIError"""
        with pytest.raises(DeepSeekAPIError) as exc_info:
            raise DeepSeekAPIError("API test error")
        assert str(exc_info.value) == "API test error"
