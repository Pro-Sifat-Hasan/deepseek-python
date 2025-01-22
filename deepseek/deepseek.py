from typing import Optional, Dict, List, Generator, AsyncGenerator
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

class DeepSeekError(Exception):
    """Base exception class for DeepSeek errors"""
    pass

class DeepSeekAPIError(DeepSeekError):
    """Exception raised for API errors"""
    pass

class DeepSeekClient:
    """
    A client for interacting with DeepSeek's language models.
    
    Args:
        api_key (str): Your DeepSeek API key
        base_url (str, optional): Base API URL. Defaults to "https://api.deepseek.com".
        default_model (str, optional): Default model to use. Defaults to "deepseek-chat".
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.deepseek.com",
        default_model: str = "deepseek-chat"
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.async_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.default_model = default_model

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> ChatCompletion:
        model = model or self.default_model
        try:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                **kwargs
            )
        except Exception as e:
            raise DeepSeekAPIError(f"API Error: {str(e)}") from e

    async def async_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> ChatCompletion:
        model = model or self.default_model
        try:
            return await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                **kwargs
            )
        except Exception as e:
            raise DeepSeekAPIError(f"API Error: {str(e)}") from e

    def stream_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Generator[ChatCompletionChunk, None, None]:
        model = model or self.default_model
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )
            for chunk in stream:
                yield chunk
        except Exception as e:
            raise DeepSeekAPIError(f"API Error: {str(e)}") from e

    async def async_stream_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        model = model or self.default_model
        try:
            stream = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )
            async for chunk in stream:
                yield chunk
        except Exception as e:
            raise DeepSeekAPIError(f"API Error: {str(e)}") from e