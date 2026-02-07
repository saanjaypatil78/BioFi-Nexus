from dataclasses import dataclass
import os


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    openclaw_enabled: bool
    openclaw_bin: str
    openclaw_thinking: str
    openclaw_timeout: int


def load_settings() -> Settings:
    enabled_value = os.getenv("OPENCLAW_ENABLED", "false")
    timeout_value = os.getenv("OPENCLAW_TIMEOUT", "30")
    try:
        timeout = int(timeout_value)
    except ValueError:
        timeout = 30
    timeout = max(timeout, 1)

    return Settings(
        openclaw_enabled=_parse_bool(enabled_value),
        openclaw_bin=os.getenv("OPENCLAW_BIN", "openclaw"),
        openclaw_thinking=os.getenv("OPENCLAW_THINKING", "medium"),
        openclaw_timeout=timeout,
    )
