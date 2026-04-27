# Discord Upstream Update Plan

This plan defines how to keep `discord-mcp-server` aligned with Discord documentation and API changes while minimizing regressions for MCP tool users.

## Scope

Applies to:
- `mcp-servers/development/discord-mcp-server`
- Tool contracts exposed by that server (tool names, input schemas, output shapes, auth assumptions)

---

## Goals

1. Detect Discord upstream changes early.
2. Assess impact on MCP tool contracts before code changes.
3. Update implementation with backward compatibility when possible.
4. Verify with both local contract checks and live canary calls.
5. Release with clear versioning and changelog notes.

---

## Sources of Truth

Use only official upstream sources for change decisions:

- Discord Change Log: <https://discord.com/developers/docs/change-log>
- Discord API reference root: <https://discord.com/developers/docs/reference>
- Discord docs index captured in repo: `mcp-servers/development/discord-mcp-server/docs/DISCORD_DEV_DOCS.md`

---

## Operating Cadence

### Weekly Baseline (recommended)
- Check upstream changelog and impacted docs sections once per week.
- Record findings in a short update note (no-op is valid).

### Event-Driven Check (mandatory)
- Re-run impact assessment whenever Discord ships a notable API/docs change affecting interactions, components, activities, Social SDK, auth/scopes, or rate limits.

---

## Workflow

### Step 1: Detect

Collect all relevant upstream changes since the last check.

Output:
- List of changed Discord docs/API areas.
- Link to each source entry.

### Step 2: Impact Assessment

Create a change-impact matrix:

| Upstream change | Affected MCP tool(s) | Type | Risk | Action |
|---|---|---|---|---|
| Endpoint/field added | One or more | Non-breaking | Low | Add support/tests/docs |
| Field renamed/removed | One or more | Breaking | High | Add compatibility layer or deprecate |
| Auth/scope changes | One or more | Potentially breaking | High | Update env/config/docs and errors |
| Rate limit behavior changes | One or more | Behavioral | Medium | Adjust retries/backoff/errors |

Type definitions:
- **Non-breaking**: Existing tool contract remains valid.
- **Potentially breaking**: Runtime behavior may fail without schema changes.
- **Breaking**: Existing tool contract can no longer be honored.

### Step 3: Plan the Update

For each impacted tool:
- Keep tool identity stable where possible (name + core shape).
- Implement upstream translation in adapters/handlers.
- If break is unavoidable, mark old behavior as deprecated first.

### Step 4: Implement + Verify

Required verification lanes:

1. **Contract checks (local/offline)**
   - Input schema still valid.
   - Output shape unchanged unless intentionally versioned.
   - Error payloads are clear and non-leaking.

2. **Live canary checks (test Discord app)**
   - Run a small set of high-value tool calls against real Discord endpoints.
   - Validate auth/scope/rate-limit behavior.

Minimum live canary set:
- One interaction-related call
- One activity or Social SDK related call (if applicable)
- One failure-mode check (e.g., invalid input or missing permissions)

### Step 5: Release

Use semantic versioning:
- **PATCH**: internal fixes, no contract changes.
- **MINOR**: additive features, backward-compatible.
- **MAJOR**: breaking contract changes.

Release note must include:
- Discord upstream reference(s)
- Affected MCP tools
- Compatibility/deprecation notes
- Verification date

---

## Compatibility Policy

Default policy: **conservative compatibility**.

- Prefer adding new optional fields instead of replacing existing ones.
- Keep deprecated behavior available for at least one MINOR release when feasible.
- Emit clear deprecation guidance in docs and release notes.

---

## Rollback Plan

If live verification fails after update:

1. Revert to last known good `discord-mcp-server` version.
2. Mark upstream change as blocked with reason.
3. Add a temporary warning in docs/README if end-user impact exists.
4. Reopen update with narrowed scope.

---

## Ownership and Decision Rules

- Assign one owner for weekly checks and release decisions.
- Escalate to reviewer when:
  - a breaking change is detected,
  - auth scope changes are required,
  - or behavior diverges from current MCP tool contracts.

---

## Runbook Checklist

Use this checklist for each upstream update cycle:

- [ ] Reviewed Discord changelog and relevant docs sections.
- [ ] Built/updated change-impact matrix.
- [ ] Classified each change (non-breaking/potentially breaking/breaking).
- [ ] Updated MCP tool handling with compatibility-first approach.
- [ ] Ran local contract checks.
- [ ] Ran live canary checks with test app credentials.
- [ ] Updated docs/examples for affected tools.
- [ ] Bumped version according to semver policy.
- [ ] Wrote release notes with upstream references and verification date.

---

## References

- Discord docs map in repo: `mcp-servers/development/discord-mcp-server/docs/DISCORD_DEV_DOCS.md`
- Setup guide: `SETUP.md`
- Verification guide: `VERIFY_MCP_SERVERS.md`
- Server quality bar: `docs/SERVER_QUALITY_BAR.md`
- Component standard and tiers: `docs/IDE_AI_AGENT_COMPONENTS_STANDARD.md`
