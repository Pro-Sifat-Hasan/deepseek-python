# DeepSeek Python Client

A feature-rich Python client for interacting with DeepSeek's powerful language models, supporting both synchronous and asynchronous operations.

## Installation

```bash
pip install deepseek-sdk
```

## Quick Start

```python
from deepseek import DeepSeekClient

# Initialize client
client = DeepSeekClient(api_key="your-api-key")

# Basic chat completion
response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)
```

## Features

✅ Synchronous & Async Support  
🚀 Streaming Responses  
🔧 Customizable Parameters  
🛠 Error Handling  
⚡️ Context Manager Support  
🔁 Retry Mechanisms  

## Complete Usage Guide

### 1. Basic Chat Completion

```python
response = client.chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ],
    model="deepseek-chat",  # default model
    temperature=0.8,        # control randomness (0-2)
    max_tokens=500          # limit response length
)
```

### 2. Streaming Responses

**Synchronous Streaming:**
```python
for chunk in client.stream_response(
    messages=[{"role": "user", "content": "Tell me a story about AI"}]
):
    content = chunk.choices[0].delta.content or ""
    print(content, end="", flush=True)
```

**Async Streaming:**
```python
async def stream_response():
    async for chunk in client.async_stream_response(
        messages=[{"role": "user", "content": "Explain blockchain technology"}]
    ):
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)

# Run in event loop
import asyncio
asyncio.run(stream_response())
```

### 3. Advanced Configuration

**Custom Client Initialization:**
```python
client = DeepSeekClient(
    api_key="your-api-key",
    base_url="https://api.deepseek.com",  # Custom endpoint
    default_model="deepseek-reasoner"   # Set default model
)
```

**Context Manager for Streams:**
```python
with client.stream_response(
    messages=[{"role": "user", "content": "Generate Python code for quicksort"}]
) as stream:
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
```

### 4. Error Handling

```python
try:
    response = client.chat_completion(messages=[{"role": "user", "content": "Hello"}])
except DeepSeekAPIError as e:
    print(f"API Error: {str(e)}")
except DeepSeekError as e:
    print(f"Client Error: {str(e)}")
```

### 5. Advanced Parameters

**Using All Available Options:**
```python
response = client.chat_completion(
    messages=[{"role": "user", "content": "Compare Python and JavaScript"}],
    model="deepseek-chat",
    temperature=1.2,
    top_p=0.9,
    max_tokens=1000,
    presence_penalty=0.5,
    frequency_penalty=0.5,
    stream=False
)
```

### 6. Retry Mechanism

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class RobustClient(DeepSeekClient):
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def chat_completion(self, *args, **kwargs):
        return super().chat_completion(*args, **kwargs)

# Usage
client = RobustClient(api_key="your-api-key")
```

## Inspiration: What Can You Build?

### 🤖 Intelligent Chatbot
```python
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
        
    response = client.chat_completion(
        messages=[{"role": "user", "content": user_input}],
        temperature=0.9
    )
    print(f"AI: {response.choices[0].message.content}")
```

### 📝 Content Generation System
```python
def generate_blog_post(topic: str) -> str:
    prompt = f"Write a 500-word blog post about {topic} with markdown formatting:"
    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content
```

### 💻 CLI Interface (using Click)
```python
import click

@click.command()
@click.option('--api-key', required=True, help='Your DeepSeek API key')
@click.option('--prompt', required=True, help='Your query/prompt')
@click.option('--stream', is_flag=True, help='Enable streaming')
def deepseek_cli(api_key, prompt, stream):
    client = DeepSeekClient(api_key=api_key)
    
    if stream:
        for chunk in client.stream_response([{"role": "user", "content": prompt}]):
            click.echo(chunk.choices[0].delta.content or "", nl=False)
    else:
        response = client.chat_completion([{"role": "user", "content": prompt}])
        click.echo(response.choices[0].message.content)

if __name__ == '__main__':
    deepseek_cli()
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -am 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

## License

MIT License - See [LICENSE](LICENSE) for details

## Support

For issues and feature requests, please [open an issue](https://github.com/Pro-Sifat-Hasan/deepseek-python/issues)

---

**🚀 Pro Tip:** Combine with other libraries like `rich` for beautiful console output, or `fastapi` to create AI-powered web services!
