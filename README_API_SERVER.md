# Perplexity AI - OpenAI Compatible API Server

This API server provides an OpenAI-compatible interface for the Perplexity AI service, making it easy to use with tools like Cline and other OpenAI-compatible clients.

## Features

- **OpenAI Compatible**: Implements the `/v1/chat/completions` endpoint
- **Multiple Models**: Support for different Perplexity modes (auto, pro, reasoning, research)
- **Streaming Support**: Both streaming and non-streaming responses
- **Authentication**: Flexible API key format supporting cookies
- **CORS Enabled**: Ready for web applications

## Installation

1. Install the server dependencies:
```bash
pip install -r requirements_server.txt
```

2. Make sure you have the base Perplexity dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
# From the project root directory
python -m api_server.main
```

The server will start on `http://localhost:8000` by default.

### Environment Variables

- `SERVER_HOST`: Server host (default: "0.0.0.0")
- `SERVER_PORT`: Server port (default: 8000)

### API Endpoints

#### List Models
```
GET /v1/models
```

Returns a list of available models.

#### Chat Completions
```
POST /v1/chat/completions
```

OpenAI-compatible chat completions endpoint.

**Request Format:**
```json
{
  "model": "perplexity-auto",
  "messages": [
    {"role": "user", "content": "What is artificial intelligence?"}
  ],
  "stream": false,
  "temperature": 0.7,
  "max_tokens": 4096
}
```

**Response Format:**
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "perplexity-auto",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Artificial intelligence (AI) refers to..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

## Available Models

| Model ID | Description | Perplexity Mode |
|----------|-------------|-----------------|
| `perplexity-auto` | Fastest responses | auto |
| `perplexity-pro` | Enhanced capabilities | pro |
| `perplexity-reasoning` | Step-by-step thinking | reasoning |
| `perplexity-research` | Comprehensive analysis | deep research |
| `perplexity-pro-gpt4o` | Pro with GPT-4o | pro + gpt-4o |
| `perplexity-pro-claude` | Pro with Claude 3.7 | pro + claude |
| `perplexity-reasoning-r1` | Reasoning with R1 | reasoning + r1 |
| `perplexity-reasoning-o3` | Reasoning with O3-mini | reasoning + o3-mini |

## Authentication

This API server uses hardcoded Perplexity cookies and **ignores any external API key**. You can pass any string as the API key or omit it entirely.

```bash
# Any of these work the same way:
curl -H "Authorization: Bearer any-string" ...
curl -H "Authorization: Bearer dummy-key" ...
curl -H "Authorization: Bearer test" ...
# Or even without Authorization header
curl ...
```

The server will always use the built-in Perplexity cookies for authentication.

## Cline Configuration

To use with Cline:

1. **API Provider**: Select "OpenAI Compatible"
2. **Base URL**: `http://localhost:8000/v1`
3. **API Key**: Any string (e.g., "dummy-key", "test", or anything else - it will be ignored)
4. **Model**: Choose from available models (e.g., `perplexity-auto`)

## Examples

### Basic Usage with curl

```bash
# Non-streaming request
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy-key" \
  -d '{
    "model": "perplexity-auto",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'

# Streaming request
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy-key" \
  -d '{
    "model": "perplexity-auto", 
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

### Python Client Example

```python
import openai

# Configure client
client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy-key"  # or your cookies JSON
)

# Make request
response = client.chat.completions.create(
    model="perplexity-auto",
    messages=[{"role": "user", "content": "What is AI?"}]
)

print(response.choices[0].message.content)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure both `requirements.txt` and `requirements_server.txt` are installed
2. **Connection Refused**: Check if the server is running on the correct host/port
3. **Model Not Found**: Use one of the supported model IDs from the list above
4. **Authentication Issues**: Check your cookie format if using authenticated requests

### Logging

The server provides detailed logging. Check the console output for debugging information.

### Testing

You can test the server with:

```bash
# Test server health
curl http://localhost:8000/

# Test models endpoint
curl http://localhost:8000/v1/models

# Test chat completions
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test" \
  -d '{"model":"perplexity-auto","messages":[{"role":"user","content":"test"}]}'
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
