# Relay LLM Router

A FastAPI gateway for OpenAI and Gemini. For each quality tier it tries OpenAI first, then falls back to Gemini if OpenAI is unavailable, returns no text, or raises a provider API error. Relay has no request retry loop, rate limiter, or cache.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn main:app
```

Set `OPENAI_API_KEY`, `GEMINI_API_KEY`, or both in the environment or a local `.env` file.

Send `POST /chat` with JSON such as:

```json
{"quality":"fast","messages":[{"role":"user","content":"Explain recursion briefly."}]}
```

Use `fast` or `smart`. Messages support `user`, `assistant`, and an optional leading `system` message. Requests need a user message and allow up to 64 messages, 16,000 characters per message, and 64,000 combined. Optional `max_tokens` accepts 1–8192 and `temperature` accepts 0–2.

Invalid requests return 422. No configured providers returns 503. If all configured providers fail, Relay returns 502. Logs identify provider and error type without including prompts, credentials, or upstream error messages. Missing usage counts are returned as null.
