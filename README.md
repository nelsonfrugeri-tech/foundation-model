# Foundation Model
> Responsible by containing all Providers and Models in the Market, through the Hub is possible have a unique and simple interface to the comunication between the most diverse Providers and Models.

## Features

* **Unified Interface:** Interact with LLMs from different providers using a consistent API.
* **Provider Abstraction:**  Switch between providers seamlessly without modifying your application code.
* **Tool Integration:** Extend LLM capabilities by defining custom functions ("tools") that can be invoked.
* **Error Handling:** Robust error handling mechanisms for graceful handling of invalid requests.

## Supported Providers and Models

| Provider | Model | Description | Context Window | Training Data | Parameters |
|---|---|---|---|---|---|
| OpenAI | GPT-3.5 Turbo | Advanced language model for text generation. | 2048 tokens | Diverse internet text | `temperature`: (Optional[float]) Controls the randomness of the output.  `max_tokens`: (Optional[int]) Limits the length of the generated text. |
| OpenAI | GPT-4 | Advanced language model for text generation. | 2048 tokens | Diverse internet text | `temperature`: (Optional[float]) Controls the randomness of the output.  `max_tokens`: (Optional[int]) Limits the length of the generated text. |
| Anthropic | Claude | Generative model with enhancements in safety and ethics. | 4096 tokens | Broad and ethically sourced datasets | `temperature`: (Optional[float]) Controls the randomness of the output.  `max_tokens`: (Optional[int]) Limits the length of the generated text. |
| Bedrock | Llama3 |  |  |  | `temperature`: (Optional[float]) Controls the randomness of the output.  `max_tokens`: (Optional[int]) Limits the length of the generated text. |
| Gemini | Gemini 2 (Flash/Pro) | Google's generative models. | - | Proprietary | `temperature`: (Optional[float])  `max_tokens`: (Optional[int]) |

## Parameters

**Common Parameters:**

* **`provider`:** (str) The name of the LLM provider (e.g., "openai", "anthropic", "bedrock").
* **`model`:** (str) The name of the specific LLM model (e.g., "gpt-3.5-turbo", "claude-v1", "meta.llama3-70b-instruct-v1:0").
* **`messages`:** (List[Dict]) A list of messages representing the conversation history. Each message has a `role` ("user" or "assistant") and `content` (str).

**Provider-Specific Parameters:**

Refer to the table above for parameters specific to each provider and model.

## Running the Project

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/foundation-model.git
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Use code with caution:**
Set up environment variables:

Create a .env file in the root directory and set the following variables:
```bash
OPENAI_KEY=your_openai_api_key
ANTHROPIC_KEY=your_anthropic_api_key
# Gemini models
GEMINI_KEY=your_gemini_api_key
# Bedrock credentials are configured in .env.bedrock
```

3. **Use code with caution.**
Run the application:
```bash
python src/app.py
```

### Example request using Gemini

```bash
curl -X POST http://localhost:8080/v1/generate/text \
  -H "Content-Type: application/json" \
  -d '{
    "provider": {"name": "gemini", "model": {"name": "gemini-2.0-pro"}},
    "prompt": {"parameter": {"temperature": 0.7, "max_tokens": 150},
               "messages": [{"role": "user", "content": "Qual a capital da França?"}]},
    "tool_choice": "auto",
    "store": true
  }'
```

**Project Structure:**
The project is structured to maintain a clear separation between the hub (API) and provider layers:

* **`hub`:** (str) Contains the core API logic, including routes, controllers, request/response models, and exception handling.
* **`provider`:** (str) Houses provider-specific implementations, including adapters, service classes, and request/response mapping logic.

This separation ensures that the API code remains independent of specific provider implementations, making it easier to add or modify providers in the future.