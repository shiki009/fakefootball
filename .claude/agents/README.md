# fakefootball Agent Pipelines

## Quick Reference

| Pipeline | Command | When to Use | Stages |
|----------|---------|-------------|--------|
| **Feature** | `@ff-orchestrator` | New feature touching 3+ layers | planner → architect → db-engineer → backend → frontend → tester → reviewer |
| **Bugfix** | `@ff-bug-orchestrator` | Bug report, unknown root cause | triager → fixer → tester → reviewer |
| **Hotfix** | `@ff-hotfix-orchestrator` | Bug with known root cause, needs fast fix | fixer → reviewer |
| **Refactor** | `@ff-refactor-orchestrator` | Restructure code, preserve behavior | analyzer → executor → tester → reviewer |
| **Migration** | `@ff-migration-orchestrator` | DB-only changes, no new UI | db-engineer → backend → tester → reviewer |

## How Pipelines Work

### 1. You describe the work

Tell the orchestrator what you need in natural language:

```
@ff-orchestrator Add post bookmarks — visitors can bookmark posts to read later
@ff-bug-orchestrator The vote scores are wrong on the post list page
@ff-hotfix-orchestrator The enrichment in routers/posts.py has a KeyError when score dict is empty
@ff-refactor-orchestrator Extract the batch enrichment logic from routers into a shared utility
@ff-migration-orchestrator Add a "reports" table with post_id and reason columns
```

### 2. The orchestrator creates a work directory

Each pipeline type has its own directory:

```
.planning/
├── features/{slug}/      ← feature pipeline
├── bugs/{slug}/          ← bugfix pipeline
├── hotfixes/{slug}/      ← hotfix pipeline
├── refactors/{slug}/     ← refactor pipeline
└── migrations/{slug}/    ← migration pipeline
```

### 3. Agents run in sequence

The orchestrator spawns one agent at a time. Each agent:
- Reads its instructions from `.claude/agents/ff-{name}.md`
- Reads predecessor artifacts from the work directory
- Does its work (investigation, code changes, testing, review)
- Writes its output artifact to the work directory
- Reports status: `complete`, `blocked`, or `failed`

### 4. Artifacts pass between agents

Agents communicate through markdown files with YAML frontmatter:

```yaml
---
feature: post-bookmarks
stage: planner
status: complete
produced_by: ff-planner
consumed_by: ff-architect
---
```

The orchestrator tracks everything in `PIPELINE-STATE.md`:

```
| # | Stage | Agent | Status | Started | Completed | Artifact |
|---|-------|-------|--------|---------|-----------|----------|
| 1 | Plan | ff-planner | complete | 12:00 | 12:02 | 01-SPEC.md |
| 2 | Architect | ff-architect | running | 12:02 | | 02-ARCHITECTURE.md |
| 3 | Database | ff-db-engineer | pending | | | 03-DB-CHANGES.md |
```

### 5. The reviewer decides the outcome

Every pipeline ends with the reviewer. Three possible verdicts:
- **pass** — ship it
- **pass-with-warnings** — ship it, but address the warnings
- **fail** — the orchestrator determines which stage to re-run

## Running Individual Agents

You can run any agent standalone without a pipeline:

```
# Investigation only
@ff-bug-triager Investigate why vote scores are wrong on the dashboard

# Code review only
@ff-reviewer Review backend/routers/posts.py against project conventions

# Quick analysis
@ff-refactor-analyzer Map all dependencies of backend/schemas.py

# Database design
@ff-db-engineer Add a "bookmarks" model with post_id and fingerprint columns
```

When running standalone, tell the agent where to write its output.

## Choosing the Right Pipeline

```
"I need a new feature"                    → @ff-orchestrator (feature)
"Something is broken, not sure why"       → @ff-bug-orchestrator (bugfix)
"Something is broken, I know the cause"   → @ff-hotfix-orchestrator (hotfix)
"I want to restructure this code"         → @ff-refactor-orchestrator (refactor)
"I need to change the database schema"    → @ff-migration-orchestrator (migration)
"Single-file fix, trivial change"         → just do it directly, no pipeline needed
```

## Multi-Language Notes

This project has two codebases:

| Layer | Language | Location |
|-------|----------|----------|
| Models | Python (SQLAlchemy) | `backend/models.py` |
| Schemas | Python (Pydantic) | `backend/schemas.py` |
| API Routes | Python (FastAPI) | `backend/routers/` |
| HTTP Client | JavaScript (Axios) | `frontend/src/api.js` |
| State | JavaScript (Pinia) | `frontend/src/stores/` |
| Components | Vue 3 (SFC) | `frontend/src/components/` |
| Pages | Vue 3 (SFC) | `frontend/src/views/` |

Agents that work across both languages:
- **ff-bug-triager**: Traces bugs through Python → JSON → JavaScript
- **ff-bug-fixer**: Can fix Python and/or Vue code
- **ff-reviewer**: Checks conventions for both Python and Vue
- **ff-tester**: Writes pytest (backend) and optionally Vitest (frontend)
- **ff-refactor-analyzer**: Maps dependencies in both Python and JS modules
- **ff-refactor-executor**: Executes refactors in both languages

## Coverage

Every development workflow is covered by either a pipeline or a direct action:

| Workflow | Covered? | How |
|----------|----------|-----|
| Build a new feature | yes | Feature pipeline |
| Fix a bug (unknown cause) | yes | Bugfix pipeline |
| Fix a bug (known cause, fast) | yes | Hotfix pipeline |
| Restructure / migrate code | yes | Refactor pipeline |
| DB schema changes only | yes | Migration pipeline |
| Code review | yes | `@ff-reviewer` standalone |
| Investigation only | yes | `@ff-bug-triager` standalone |
| Dependency analysis | yes | `@ff-refactor-analyzer` standalone |
| Single-file edit | yes | Direct edit, no pipeline needed |
| Config / env changes | yes | Direct edit, no pipeline needed |
| CI/CD, deployment | no | Infrastructure — outside agent scope |
| Documentation | no | Not enough stages to justify a pipeline |

## Agent Inventory

### Feature Pipeline (8 agents)
| Agent | Role | Writes Code? |
|-------|------|-------------|
| `ff-orchestrator` | Coordinates feature pipeline | No |
| `ff-planner` | Writes feature spec | No |
| `ff-architect` | Designs technical approach | No |
| `ff-db-engineer` | Creates SQLAlchemy model changes | Yes |
| `ff-backend` | Implements Pydantic schemas + FastAPI routers | Yes |
| `ff-frontend` | Implements Vue components, stores, views | Yes |
| `ff-tester` | Writes tests (pytest + optionally Vitest) | Yes |
| `ff-reviewer` | Reviews all changes (Python + Vue) | No (read-only) |

### Bugfix Pipeline (3 new + reuses tester, reviewer)
| Agent | Role | Writes Code? |
|-------|------|-------------|
| `ff-bug-orchestrator` | Coordinates bugfix pipeline | No |
| `ff-bug-triager` | Investigates root cause (Python + Vue) | No (read-only) |
| `ff-bug-fixer` | Implements minimal fix (Python + Vue) | Yes |

### Refactor Pipeline (3 new + reuses tester, reviewer)
| Agent | Role | Writes Code? |
|-------|------|-------------|
| `ff-refactor-orchestrator` | Coordinates refactor pipeline | No |
| `ff-refactor-analyzer` | Maps dependencies (Python + JS) | No (read-only) |
| `ff-refactor-executor` | Executes refactor changes | Yes |

### Migration Pipeline (1 new + reuses db-engineer, backend, tester, reviewer)
| Agent | Role | Writes Code? |
|-------|------|-------------|
| `ff-migration-orchestrator` | Coordinates DB-only changes | No |

### Hotfix Pipeline (1 new + reuses bug-fixer, reviewer)
| Agent | Role | Writes Code? |
|-------|------|-------------|
| `ff-hotfix-orchestrator` | Fast-track fix, skip triage | No |

**Total: 16 agent files, 5 pipelines**

## Shared Agents

Some agents are reused across pipelines:

| Agent | Used By |
|-------|---------|
| `ff-tester` | feature, bugfix, refactor, migration |
| `ff-reviewer` | feature, bugfix, hotfix, refactor, migration |
| `ff-db-engineer` | feature, migration |
| `ff-backend` | feature, migration |
| `ff-bug-fixer` | bugfix, hotfix |
