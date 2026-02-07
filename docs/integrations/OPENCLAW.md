# OpenClaw Assistant Integration

BioFi-Nexus can use the OpenClaw assistant as a planning provider through a pluggable CLI adapter.

## Install OpenClaw

Follow the OpenClaw CLI installation steps:

```bash
npm install -g openclaw@latest
openclaw onboard
openclaw gateway
```

## Configure the Orchestrator

Copy the example environment file and enable OpenClaw:

```bash
cp services/orchestrator/.env.example services/orchestrator/.env
```

Update the values as needed:

- `OPENCLAW_ENABLED`: set to `true` to enable the integration.
- `OPENCLAW_BIN`: path to the OpenClaw binary (defaults to `openclaw`).
- `OPENCLAW_THINKING`: default thinking level sent to the CLI.
- `OPENCLAW_TIMEOUT`: timeout (seconds) for each OpenClaw CLI request.

## Run the Orchestrator

Start the FastAPI app:

```bash
uvicorn services.orchestrator.app:app --reload
```

Send a planning request:

```bash
curl -X POST http://localhost:8000/api/v1/assistant/plan \
  -H "Content-Type: application/json" \
  -d '{"message": "Draft a bio-data tokenization plan."}'
```

The response body includes the OpenClaw CLI output.

## Troubleshooting

If OpenClaw is not installed or not configured, the orchestrator returns a 503 response when the integration is disabled, or a 500 response with the CLI error message when enabled.
