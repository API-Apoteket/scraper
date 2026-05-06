# AI Agent Coordination

This repository is maintained with help from two AI agents:

- **Claude Code** (Anthropic) — scheduled weekly reviews, CI/CD, infra, Dependabot/security fixes
- **Codex** (OpenAI) — interactive feature work and bug fixes invoked by the maintainer

## Branch Naming

| Agent | Prefix | Example |
|---|---|---|
| Claude | `claude/` | `claude/fix-build-timeout` |
| Codex | `codex/` | `codex/add-retry-logic` |

Both prefixes auto-merge via the `auto-merge.yml` workflow once CI passes.

## Ownership Map

Each agent has primary ownership over certain areas. Both agents may read anything, but should avoid opening PRs that modify another agent's primary files unless there is a clear, non-conflicting change.

| Area | Primary owner | Notes |
|---|---|---|
| `.github/workflows/` | Claude | CI/CD, auto-merge, CodeQL, release-please |
| `.github/dependabot.yml` | Claude | Dependency update schedule |
| `docker-compose.yml` | Claude | Infrastructure, image versions |
| `Dockerfile` | Claude | Container build |
| `SECURITY.md`, `AGENTS.md` | Claude | Maintenance docs |
| `src/`, `scraper/`, `webui/` | Codex | Application logic, features |
| `tests/` | Codex | Test coverage |
| `README.md`, `CHANGELOG.md` | Shared | Either may update; release-please owns CHANGELOG |

## Conflict Protocol

Before opening a PR:

1. Run `gh pr list --repo API-Apoteket/scraper --state open` and check for open PRs touching the same files.
2. If another agent has an open PR on a file you need to modify, either:
   - Wait for it to merge and rebase, or
   - Scope your change to non-overlapping lines with a comment explaining why.
3. Never force-push to a branch you did not create.
4. Never close or edit another agent's PR.

## PR Labels

Apply a label to every PR you open:

- Claude PRs: `ai:claude`
- Codex PRs: `ai:codex`

## Standards

- Python: follow existing style (no new linters beyond what's in CI)
- All secrets via environment variables — never hardcoded
- Docker images pinned by digest in production; `latest` tag acceptable in `docker-compose.yml`
- Do not introduce new dependencies without updating `requirements.txt`
- Run `docker compose build` locally before opening a PR that changes `Dockerfile` or `requirements.txt`
