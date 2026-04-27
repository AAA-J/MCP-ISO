#!/usr/bin/env python3
"""
Validate an mcp.json / mcp.example.json config file.

Checks:
  1. File is valid JSON.
  2. Top-level key is "mcpServers".
  3. Each server entry has "command" and "args" fields.
  4. "args" is a non-empty list.
  5. No plaintext secrets (basic heuristic: no values containing real tokens).

Usage:
    python scripts/validate_mcp_config.py mcp.example.json
    python scripts/validate_mcp_config.py ~/.cursor/mcp.json
"""

import json
import sys
from pathlib import Path

SECRET_PATTERNS = [
    "ghp_",      # GitHub personal access tokens
    "sk-",       # OpenAI-style API keys
    "xoxb-",     # Slack bot tokens
    "xoxp-",     # Slack user tokens
]

REQUIRED_SERVER_FIELDS = ["command", "args"]


def validate(path: str) -> bool:
    config_path = Path(path)
    errors = []
    warnings = []

    # 1. File exists
    if not config_path.exists():
        print(f"ERROR: File not found: {path}")
        return False

    # 2. Valid JSON
    try:
        with open(config_path) as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}")
        return False

    # 3. Top-level key
    if "mcpServers" not in config:
        errors.append('Missing required top-level key: "mcpServers"')

    servers = config.get("mcpServers", {})

    if not isinstance(servers, dict) or len(servers) == 0:
        errors.append('"mcpServers" must be a non-empty object')

    for server_name, server_config in servers.items():
        if not isinstance(server_config, dict):
            errors.append(f'Server "{server_name}": value must be an object')
            continue

        # 4. Required fields
        for field in REQUIRED_SERVER_FIELDS:
            if field not in server_config:
                errors.append(f'Server "{server_name}": missing required field "{field}"')

        # 5. args is a non-empty list
        args = server_config.get("args")
        if args is not None and (not isinstance(args, list) or len(args) == 0):
            errors.append(f'Server "{server_name}": "args" must be a non-empty list')

        # 6. Secret heuristic check on env values
        env = server_config.get("env", {})
        for env_key, env_val in env.items():
            if isinstance(env_val, str):
                is_placeholder = "your_" in env_val or "/path/to/" in env_val or "yourPassword" in env_val

                for pattern in SECRET_PATTERNS:
                    # Only flag as error if it looks like a real secret, not a placeholder
                    if env_val.startswith(pattern) and not is_placeholder:
                        errors.append(
                            f'Server "{server_name}": env var "{env_key}" appears to '
                            f'contain a real secret (starts with "{pattern}"). '
                            "Use placeholder values in example configs."
                        )

                # Warn on placeholder values that look incomplete
                if is_placeholder:
                    warnings.append(
                        f'Server "{server_name}": env var "{env_key}" contains a '
                        f'placeholder value — expected in example configs.'
                    )

    # Report
    if warnings:
        for w in warnings:
            print(f"  WARN: {w}")

    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        print(f"\nValidation FAILED for {path} — {len(errors)} error(s).")
        return False

    print(f"Validation PASSED for {path} ({len(servers)} server(s) defined).")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_mcp_config.py <path-to-mcp.json>")
        sys.exit(1)

    ok = validate(sys.argv[1])
    sys.exit(0 if ok else 1)
