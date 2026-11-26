# Architecture and development

Transport: `main.py` owns API routes and the FastAPI lifecycle. Application: `app/application.py` composes configured providers and closes their resources at shutdown. Domain behavior: `app/routing/` selects provider attempts, `app/providers/` translates messages and responses, and `app/body_limit.py` bounds incoming chat bodies.

Relay remains an API service with its existing interactive OpenAPI documentation. Start `python -m uvicorn main:app --host 127.0.0.1 --port 8013`, then open `http://relay.localhost:8013/docs`. `GET /health` reports ready or unconfigured without exposing keys. Provider credentials stay in local environment variables. A live model reply still depends on provider availability and account access.

## Engineering conventions

Each repository is independently runnable. Presentation calls a transport adapter, which invokes application behavior. I/O stays at explicit boundaries so tests can replace external providers. Long browser operations have one owner, reject overlapping requests, and report success or failure through the UI. Relay uses async provider requests; video and desktop work use a worker or an existing sequential CLI loop.

New behavior should validate input before touching a user's files or desktop, report partial failures accurately, and have a regression test for a concrete failure mode. Run the repository's checks before committing and document the exact manual checks separately from mocked tests.

The local apps share a request/status pattern, accessible form controls, and a responsive layout. Small standard-library transports are kept inside each repository so they do not require a sixth repository at runtime. The matching transport modules should be updated together when changing that contract.

## Local addresses

The browser resolves `.localhost` names to the loopback interface. These addresses are scoped to this computer. Start the Python process before opening the address. Chrome and Edge support this setup. A distinct port lets each project run alongside the others without an OS hosts-file change.

## Evaluation

Automated checks verify the workflows represented by their fixtures. Real model access, physical microphones and desktop focus still need environment-specific checks. CI is included under `.github/workflows/checks.yml`; its remote result must be checked after pushing.

Remaining work should be driven by observations from real use. Dataset accuracy, provider access and desktop-device behavior cannot be established by a successful test run alone.

## Verification for this change

10 tests passed using simulated providers. The suite covers request validation, fallback, adapter parsing and cleanup after a provider close failure. Live provider access remains account-dependent and was not exercised in this pass.
