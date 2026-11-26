# Relay LLM Router

Relay gives applications one FastAPI endpoint for OpenAI and Gemini. Each quality tier chooses a preferred model and a fallback. Relay skips missing providers and tries the next provider after an API error, timeout or empty reply.

## Requirements and setup

Use Python 3.10 or later. The server can start without credentials, but a live response requires an API key with access to one of the configured models.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Set `OPENAI_API_KEY`, `GEMINI_API_KEY`, or both in the environment or a private `.env` in the repository root. Then start the local service:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open [Swagger UI](http://127.0.0.1:8000/docs) or send a PowerShell request:

```powershell
$body = @{ quality = "fast"; messages = @(@{ role = "user"; content = "Explain recursion in one sentence." }) } | ConvertTo-Json -Depth 4
Invoke-RestMethod http://127.0.0.1:8000/chat -Method Post -ContentType "application/json" -Body $body
```

## Request and response

| Quality | First choice | Fallback |
| --- | --- | --- |
| `fast` | `gpt-4o-mini` | `gemini-2.5-flash` |
| `smart` | `gpt-4o` | `gemini-2.5-pro` |

Clients send `messages` with user and assistant roles and an optional leading system message. A user message is required. The request can also set `max_tokens` (1–8192) and `temperature` (0–2). Relay accepts up to 64 messages, 16,000 characters each, and 64,000 characters combined.

A successful reply includes the text, actual provider and model, token counts when available, and the upstream finish reason when supplied. A finish reason such as `length` can indicate truncated output. Each provider attempt has a 30-second deadline.

| Status | Meaning |
| --- | --- |
| 413 | Body exceeds 512 KiB |
| 422 | Request fails validation |
| 503 | No provider is configured |
| 502 | All configured provider attempts failed |

Relay logs provider failures without including prompts, keys or raw upstream error messages. The local prototype has no authentication, rate limiter, cache, or application-level same-provider retry loop.

## Working proof

The route and adapter suite passed **9 tests**. It covers invalid requests, body limits, fallback, missing usage, and completion status using simulated responses. The PowerShell example above needs a live provider key. Live provider access was not verified in that test run.

```powershell
.\.venv\Scripts\python.exe -m pip install pytest httpx
.\.venv\Scripts\python.exe -m pytest -q
```
