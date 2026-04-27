# IDE AI Agent Components Standard

This document defines a practical standard for building and operating IDE AI agent systems with MCP. It covers:

- 6 standard components (established and well-supported today)
- 4 experimental/emerging components (real patterns with evolving implementations)
- Minimum MCP server sets by stack type

Use this as a baseline architecture checklist for new projects and as a review reference for existing setups.

---

## The Full Stack: 6 Standard Components

These components are mature enough to be considered core for most teams.

### 1) MCP Servers ("The Hands")

**Role**: Provide standardized, model-agnostic access to tools, resources, and prompts.

**What it includes**:
- Filesystem and repository operations
- API and database access layers
- Observability and ops integrations
- Domain-specific tool wrappers

**Why standard**: MCP is the de facto interface for controlled tool use across modern agent stacks.

---

### 2) Rules ("The Standing Orders")

**Role**: Persistent behavioral constraints and priorities for the agent.

**What it includes**:
- Coding standards and repo conventions
- Safety and compliance constraints
- Workflow preferences and guardrails

**Why standard**: Rules produce consistent behavior across sessions and reduce drift.

---

### 3) Skills ("The Playbooks")

**Role**: Reusable procedures for recurring tasks.

**What it includes**:
- Structured task recipes
- Tool selection guidance
- Repeatable troubleshooting and operational flows

**Why standard**: Skills improve reliability, reduce prompt overhead, and accelerate execution.

---

### 4) Hooks ("The Guardrails & Automation")

**Role**: Event-driven automation and controls around agent activity.

**What it includes**:
- Pre/post action checks
- Automated validation and notifications
- Safety interlocks before high-risk operations

**Why standard**: Hooks enforce process quality and reduce human toil.

---

### 5) Context Files ("The Institutional Knowledge")

**Role**: Durable project context for architecture, standards, and workflows.

**What it includes**:
- Architecture and setup docs
- Operational runbooks
- Team-specific guidance and assumptions

**Why standard**: Shared context is required for accurate agent planning and execution.

---

### 6) Settings ("The Environment")

**Role**: Local IDE/runtime configuration that shapes agent behavior and developer UX.

**What it includes**:
- Editor and workspace defaults
- Runtime and model preferences
- Permission and sandbox defaults

**Why standard**: Environment controls affect reliability, speed, and safety of agent actions.

---

## Experimental/Emerging Components

These are increasingly important, but patterns are still evolving by team and platform.

### 7) Subagents / Multi-Agent Orchestration ("The Team")

**Role**: Delegate subtasks to specialist agents with scoped responsibilities.

**Current maturity**: Useful in complex workflows; orchestration patterns are still stabilizing.

---

### 8) Canvas ("Live Artifacts")

**Role**: Rich, interactive artifacts for analysis, planning, and results presentation.

**Current maturity**: High potential, but best practices vary by workflow and team habits.

---

### 9) Memory Systems ("Persistent Learning")

**Role**: Cross-session memory and retrieval for preferences, history, and long-term context.

**Current maturity**: Multiple approaches exist; quality and governance vary widely.

---

### 10) Domain Tools YAML ("Dynamic Tool Configuration")

**Role**: Declarative, domain-level configuration for tool behavior and exposure.

**What it commonly controls**:
- Tool registration and metadata
- Input/output schemas and constraints
- Routing and categorization by business domain

**Current maturity**: Real and increasingly common, but not yet universal as a formal standard.

---

## Minimum MCP Server Sets by Stack Type

Use these as "minimum viable" sets. Expand only when a repeated workflow is blocked.

### Which Stack Are You?

Use this quick decision tree:

1. Are you mostly a single developer shipping one product?
   - Yes -> Start with **A) Solo Builder**
   - No -> Continue
2. Do you need shared app API/data access for a small-to-medium team moving quickly?
   - Yes -> Start with **B) Startup Team**
   - No -> Continue
3. Are compliance, audit trails, and strict access boundaries first-class requirements?
   - Yes -> Start with **C) Enterprise Team**
   - No -> Continue
4. Is your core product workflow centered on data pipelines, model experiments, or analytics platforms?
   - Yes -> Start with **D) Data/AI Product Stack**
   - No -> Continue
5. Is your team primarily responsible for platform reliability, CI/CD, and incident response?
   - Yes -> Start with **E) Platform/DevOps-Heavy Stack**
   - No -> Default to **B) Startup Team** and trim/add servers based on weekly usage.

Selection heuristics:
- If two categories fit, choose the stricter one for safety, then remove unused servers after 2-4 weeks.
- If your biggest pain is code delivery, bias toward startup/devops sets.
- If your biggest pain is governance risk, bias toward enterprise set.

---

### A) Solo Builder (Fastest Path)

**Minimum set**:
- `user-filesystem` (or equivalent local filesystem capability)
- `user-github`
- `user-app-docs`

**Optional early add-ons**:
- `user-app-api`
- `user-app-db-readonly`

---

### B) Startup Team (Speed + Shared Reliability)

**Minimum set**:
- `user-filesystem`
- `user-github`
- `user-app-docs`
- `user-app-api`
- `user-app-db-readonly`
- `user-app-ops`

**Optional**:
- `user-dev-mcp-server` (scaffolding and dev workflows)
- `user-discord-mcp-server` or other team-communication integrations

---

### C) Enterprise Team (Governance-First)

**Minimum set**:
- All Startup Team minimum servers
- Identity/auth-aware integration boundary (via existing internal MCP gateway pattern)
- Audit/telemetry-capable operations integration

**Optional**:
- Ticketing/ITSM integration server
- Dedicated policy enforcement server

**Note**: In enterprise environments, minimum viable architecture is defined as much by governance and auditability as by feature coverage.

---

### D) Data/AI Product Stack

**Minimum set**:
- `user-github`
- `user-app-docs`
- `user-app-db-readonly`
- Data/warehouse integration server (project-specific)
- Experiment/model tracking integration (project-specific)

**Optional**:
- `user-app-ops` for model service health and deployment feedback loops

---

### E) Platform/DevOps-Heavy Stack

**Minimum set**:
- `user-github`
- `user-app-ops`
- `user-app-docs`
- `user-app-db-readonly`

**Optional**:
- Communication/incident integration (`user-discord-mcp-server` or similar)
- `user-app-api` for app-level remediation workflows

---

## Server Maturity Tiers

Use these tiers to communicate confidence and operational expectations for any MCP server in the repo.

| Tier | Label | Meaning | Typical example |
|------|-------|---------|-----------------|
| 1 | **Core** | Always-on; required for baseline agent function. High stability and active maintenance expected. | `filesystem`, `github`, `app-docs` |
| 2 | **Recommended** | Used regularly by most stacks. Well-tested, with known edge cases documented. | `app-db-readonly`, `app-api`, `app-ops` |
| 3 | **Experimental** | Actively used but patterns are evolving; may change API or behavior. Requires explicit opt-in. | `app-domain`, custom/community servers |
| 4 | **Deprecated** | Scheduled for removal. Listed only for migration reference. | *(tagged as deprecated in README)* |

### How to assign a tier

A server graduates from Experimental to Recommended when:
- Used successfully in production workflows by at least one team.
- Health check and startup test pass consistently.
- Auth model and permission boundary are documented.
- A named owner or team is responsible for it.

A server graduates from Recommended to Core when:
- Removal would block the baseline agent workflow.
- Zero-downtime upgrade path is documented.
- Included in the default `mcp.example.json`.

---

## Adoption Roadmap

Recommended sequence:

1. Stabilize the 6 standard components.
2. Introduce 1-2 high-value MCP integrations beyond the baseline.
3. Add experimental components behind explicit operational boundaries.
4. Measure reliability and iterate before broad expansion.

---

## Standardization Checklist

- [ ] The 6 standard components are present and documented.
- [ ] Experimental components are explicitly labeled as evolving.
- [ ] Minimum MCP set is selected based on stack type.
- [ ] Server ownership and operational expectations are defined.
- [ ] Security boundaries and approval flows are documented.
- [ ] Verification process exists (see `VERIFY_MCP_SERVERS.md`).

