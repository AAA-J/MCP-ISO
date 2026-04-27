# MCP Stack Profiles

Concrete `mcp.json` examples for three common team configurations. Pick the profile that matches your situation, copy it to `~/.cursor/mcp.json`, and replace the placeholder values.

Not sure which profile fits? Use the [stack decision tree](../IDE_AI_AGENT_COMPONENTS_STANDARD.md#which-stack-are-you) in the components standard.

---

## Available Profiles

| Profile | File | Servers included | Best for |
|---------|------|-----------------|----------|
| Solo Builder | [solo-builder.json](./solo-builder.json) | filesystem, github, app-docs | Single developer, fastest onboarding |
| Startup Team | [startup-team.json](./startup-team.json) | + app-db-readonly, app-api, app-ops | Small/medium team with shared product access |
| Enterprise Team | [enterprise-team.json](./enterprise-team.json) | + app-domain + governance notes | Teams with compliance, audit, and access control needs |

---

## How to Use

```bash
# 1. Copy your chosen profile to Cursor's MCP config location
cp docs/stack-profiles/startup-team.json ~/.cursor/mcp.json

# 2. Replace all /path/to/MCP-ISO placeholders
#    (Use setup-project-mcp.sh to do this automatically)
./setup-project-mcp.sh

# 3. Replace token and connection string placeholders manually
#    Look for: ghp_your_*, your_api_*, your-server.*, etc.

# 4. Validate the config
python scripts/validate_mcp_config.py ~/.cursor/mcp.json

# 5. Restart Cursor
# 6. Verify servers are running
./scripts/check_mcp_servers.sh
```

---

## Tradeoffs at a Glance

### Solo Builder
- Smallest surface area — only what every developer needs.
- Add `app-api` or `app-db-readonly` the moment you hit a repeated workflow that requires them.
- No shared auth complexity.

### Startup Team
- Covers the full product loop: code → review → debug data → monitor ops.
- Requires shared credentials for DB and API; scope them to read-only and non-production where possible.
- Good default for most SaaS product teams.

### Enterprise Team
- Adds `app-domain` for domain-specific business logic tools (YAML-configurable).
- JSON includes inline notes on where to add auth gateway, RBAC, and audit logging layers.
- Larger surface area requires explicit server ownership (see [SERVER_QUALITY_BAR.md](../SERVER_QUALITY_BAR.md)).

---

## Adding Your Own Profile

1. Copy the closest existing profile JSON.
2. Remove the `_comment` keys (they are informal documentation, not a JSON standard).
3. Add or remove servers based on your stack.
4. Validate: `python scripts/validate_mcp_config.py your-profile.json`
5. Submit a PR with a brief description of the use case.

---

## Related Documents

- [IDE AI Agent Components Standard](../IDE_AI_AGENT_COMPONENTS_STANDARD.md) — Stack decision tree and maturity tiers
- [Server Quality Bar](../SERVER_QUALITY_BAR.md) — Per-server quality requirements
- [mcp.example.json](../../mcp.example.json) — Full example with all available servers
- [SETUP.md](../../SETUP.md) — Complete setup guide
