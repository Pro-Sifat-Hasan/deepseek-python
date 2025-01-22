# DeepSeek Python Client

A Python client library for interacting with DeepSeek's language models.

## Installation

```bash
pip install deepseek-sdk
```

## Usage

```python
from deepseek import DeepSeekClient

# Initialize client
client = DeepSeekClient(api_key="your-api-key")

# Regular completion
response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)

# Streaming response
for chunk in client.stream_response(
    messages=[{"role": "user", "content": "Hello"}]
):
    print(chunk.choices[0].delta.content or "", end="")

# Async usage
import asyncio

async def main():
    response = await client.async_chat_completion(
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```