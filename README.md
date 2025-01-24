# AI Assistant API-Key with Ollama

A secure API gateway for interacting with the Llama3-7B model via Ollama, featuring API key authentication and client management.

## Features

- 🔑 Auto-generated API keys with secure hashing
- 🤖 Integration with Ollama's local LLM hosting
- 🔒 Secure client authentication
- 📦 Simple JSON-based configuration
- 🌐 REST API endpoints for easy integration

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Llama3.2-3B model downloaded (`ollama pull llama3.2`)

## Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/ali619/ai-assistant-api-key.git
cd ai-assistant-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start Ollama**
```bash
ollama serve
```

4. **Run the API server**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Client Registration

### Via cURL
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"client_name": "your_client_name"}'
```

### Via Postman
1. Set request method to **POST**
2. URL: `http://localhost:8000/register`
3. Headers:
   - `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "client_name": "Your Client Name"
}
```

**Note:** Save the API key immediately - it won't be shown again!

## Using the Chat API

### cURL Example
```bash
curl -X POST http://localhost:8000/chat \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum computing in simple terms"}'
```

### Postman Setup
1. Create new POST request to `http://localhost:8000/chat`
2. Headers:
   - `X-API-Key: YOUR_API_KEY`
   - `Content-Type: application/json`
3. Request body (JSON):
```json
{
  "message": "Your question here"
}
```

### Sample Response
```json
{
  "model": "llama3:7b",
  "created_at": "2024-02-21T12:34:56.789Z",
  "response": "Quantum computing uses quantum bits to perform calculations...",
  "done": true
}
```

## Future Roadmap

- 🚀 Add streaming responses
- 📊 Implement usage metrics and rate limiting
- 🔄 API key rotation system
- 🧩 Plugin system for different LLM providers
- 🌍 Web-based client dashboard

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Code follows BLACK guidelines
- Include tests for new features
- Update documentation accordingly

## Security Notice

⚠️ **Important:**
- Never expose your API keys in client-side code
- Always use HTTPS in production environments
- Rotate API keys regularly

## License

MIT License - See [LICENSE](LICENSE) for details
