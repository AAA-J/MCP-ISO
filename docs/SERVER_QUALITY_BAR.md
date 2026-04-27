# MCP Server Quality Bar

This document defines the minimum quality requirements for every MCP server in this repository. Use it when contributing a new server, reviewing an existing one, or deciding whether a server is ready for promotion to a higher maturity tier.

For maturity tier definitions (Core / Recommended / Experimental / Deprecated), see [IDE AI Agent Components Standard](./IDE_AI_AGENT_COMPONENTS_STANDARD.md#server-maturity-tiers).

---

## 1. Startup & Health Check

Every server must start cleanly and report its own status.

**Minimum requirement**:
```bash
cd mcp-servers/<category>/<server-name>
source venv/bin/activate
python src/index.py
# Expected: starts without errors, waits for input (stdio mode)
```

**Checklist**:
- [ ] Server starts without errors in an isolated venv.
- [ ] No unhandled exceptions on startup.
- [ ] Required environment variables are validated at startup with clear error messages if missing.
- [ ] Server handles `SIGTERM` gracefully (no hard crashes on IDE shutdown).

---

## 2. Tool Contract

Each tool exposed by the server must meet these standards.

**Checklist**:
- [ ] Tool has a name, description, and typed input schema.
- [ ] All required parameters are documented.
- [ ] Tool returns a structured, predictable response.
- [ ] Tool returns a clear, actionable error message on bad input (not a raw Python traceback).
- [ ] Tool does not expose secrets, tokens, or PII in its output.

---

## 3. Authentication & Secrets

**Checklist**:
- [ ] All credentials are passed via environment variables only. No hardcoded secrets.
- [ ] `.env` file is listed in `.gitignore`.
- [ ] The server's README lists all required env vars with descriptions and safe example values.
- [ ] Tokens or connection strings are never echoed back in tool output or logs.
- [ ] Auth failure produces a clear, non-leaking error message.

---

## 4. Required Tests

Each server must have at least a smoke test that can run without external service dependencies.

**Minimum test set**:
- Startup test: server initializes without errors.
- Tool list test: server reports its tools correctly.
- Input validation test: server rejects invalid/missing inputs gracefully.

**Checklist**:
- [ ] At least one test file exists under `tests/` or equivalent.
- [ ] Tests can run offline (mock external calls where needed).
- [ ] Tests are runnable with `python -m pytest` or equivalent from the server directory.
- [ ] Test results are clean (no skips without explanation, no warnings treated as passes).

---

## 5. Documentation

**Checklist**:
- [ ] `README.md` exists in the server directory.
- [ ] README includes: purpose, setup steps, all env vars, tool list, and usage examples.
- [ ] Server is listed in the root `README.md` with a short description.
- [ ] Server is listed in `SETUP.md` with installation instructions.
- [ ] Server entry exists or is planned for `mcp.example.json`.
- [ ] README is updated when tools or config change.

---

## 6. Ownership

Every server must have a declared owner so there is a clear path for questions, issues, and upgrades.

**Ownership fields** (add to the server's `README.md` header):

```markdown
| Field | Value |
|-------|-------|
| Maturity tier | Experimental / Recommended / Core |
| Owner | @handle or team name |
| Last verified | YYYY-MM-DD |
| Requires external service | Yes / No |
```

**Checklist**:
- [ ] Owner or responsible team is named.
- [ ] Last verified date is within 6 months (or marked as unmaintained).
- [ ] External service dependency is clearly declared.

---

## 7. Security Considerations

**Checklist**:
- [ ] Server performs read-only operations where possible; write/mutating operations are explicitly flagged.
- [ ] Inputs are validated and sanitized before use in queries, commands, or API calls.
- [ ] Third-party packages are pinned to known-good versions in `requirements.txt`.
- [ ] No unnecessary filesystem or network permissions are requested.

---

## Quality Gate Summary

Use this as a pre-PR checklist when adding or modifying a server:

```
Startup & Health  [ ] starts clean  [ ] validates env on boot  [ ] graceful shutdown
Tool Contract     [ ] typed schema   [ ] clean errors           [ ] no secret leakage
Auth & Secrets    [ ] env-only creds [ ] .env in .gitignore     [ ] auth errors safe
Tests             [ ] smoke test     [ ] offline runnable       [ ] pytest passes
Documentation     [ ] README exists  [ ] env vars documented    [ ] mcp.example entry
Ownership         [ ] owner named    [ ] last-verified date     [ ] ext deps declared
Security          [ ] inputs validated [ ] deps pinned          [ ] minimal permissions
```

A server must pass **all Startup, Auth, and Documentation checks** before merging. Test and Ownership checks are required for promotion to Recommended or Core tier.

---

## Related Documents

- [IDE AI Agent Components Standard](./IDE_AI_AGENT_COMPONENTS_STANDARD.md) — Maturity tiers and stack decision tree
- [MCP Server Guide](./MCP_SERVER_GUIDE.md) — How to build a new server
- [AI CI/CD Guidelines](../AI_CI_CD_GUIDELINES.md) — Full quality checklist for AI-assisted development
- [VERIFY_MCP_SERVERS.md](../VERIFY_MCP_SERVERS.md) — Runtime verification guide
