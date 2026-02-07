import subprocess

from .config import Settings


class OpenClawError(Exception):
    pass


def run_openclaw(message: str, thinking: str | None, settings: Settings) -> str:
    if not message.strip():
        raise OpenClawError("Message cannot be empty.")

    command = [settings.openclaw_bin, "agent", "--message", message]
    if thinking:
        command.extend(["--thinking", thinking])

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=settings.openclaw_timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise OpenClawError(
            "OpenClaw CLI not found. Install it with 'npm install -g openclaw@latest' "
            "or set OPENCLAW_BIN to the binary path."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise OpenClawError(
            f"OpenClaw request timed out after {settings.openclaw_timeout} seconds."
        ) from exc

    if result.returncode != 0:
        error_output = (result.stderr or result.stdout or "").strip()
        message = error_output or "No output received."
        raise OpenClawError(
            f"OpenClaw CLI failed with exit code {result.returncode}: {message}"
        )

    output = (result.stdout or "").strip()
    if not output:
        raise OpenClawError("OpenClaw returned an empty response.")

    return output
