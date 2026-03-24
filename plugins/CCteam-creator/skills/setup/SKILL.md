---
name: setup
description: >
  Set up a complete agent team with file-based planning for complex multi-agent projects.
  Use when: (1) user asks to start a new complex project with a team/swarm, (2) user says
  "set up team", "create team", "build a team for X", "start project X", (3) user invokes
  /CCteam-creator:setup with a project name, (4) user wants to organize a multi-phase project
  with parallel agent workers and persistent progress tracking. Creates TeamCreate, planning
  files (.plans/project/), per-agent work directories, and spawns configured
  teammates. TRIGGER on: "team", "swarm", "start project", "set up project", "create team
  for", "build team", "organize project", "multi-agent project".
  IMPORTANT: You (team-lead) MUST read all reference files directly — do NOT delegate to subagents.
---

# Team Project Setup

Set up a multi-agent team for complex projects, using persistent files for planning and progress tracking.

## Prerequisites

**Before starting Step 1**, you (team-lead) MUST read all reference files directly into your own context:

```
Read references/onboarding.md
Read references/templates.md
Read references/roles.md
```

Do NOT delegate this to a subagent (Explore, general-purpose, etc.). Subagents return summaries, losing critical detail — you need the full templates and onboarding prompts to generate files and spawn agents correctly.

## Process

1. **Requirements Consultation** — Introduce the team mechanism to the user and gather requirements
2. **Confirm the Plan** — Summarize requirements and let the user confirm the team configuration
3. Create planning files (including per-agent subdirectories)
4. Create the team + spawn agents
5. Confirm setup + guide user to compact context

## Step 1: Requirements Consultation (Talk First, Then Act)

**Goal of this step**: Help the user fully understand how the team works, while gathering their actual requirements. Do not rush to create any files or teams.

### 1.1 Introduce the Team Mechanism

In a natural, conversational tone (do not copy this text verbatim — adapt to context), explain the following points:

**What a team is**:
- You (Claude) act as team-lead, simultaneously directing multiple AI agents working in parallel
- Team-lead is the **main conversation control plane**, not a spawned teammate
- Each agent has a clearly defined role (development, research, testing, review, etc.)
- Agents can communicate directly with each other (e.g., dev reaching out to reviewer directly)
- All progress is persisted via the file system, so context loss is not a concern

**When it's a good fit**:
- Projects with parallel multi-module development (frontend and backend progressing simultaneously)
- Tasks requiring research + development + testing across multiple phases
- Larger codebases that need code review and quality assurance

**When it's not a good fit**:
- Simple single-file changes or small bug fixes
- Tasks that only need a single role (a single agent is more efficient)

**How it works**:
- The team-lead (you) assigns tasks, coordinates progress, and makes decisions
- The team-lead also owns user alignment, phase transitions, and the team's durable operating rules
- Each agent has its own working directory (`.plans/<project>/`), recording tasks, findings, and progress
- Agents escalate blockers to the team-lead, who provides direction after review
- After development, devs automatically request a code review from the reviewer

### 1.2 Gather User Requirements

After the introduction, learn the following through conversation:

1. **Task type** — Is this software development, research/analysis, content creation, data processing, or a mix? This determines whether standard roles apply directly or need adaptation
2. **What the user wants to accomplish** — Project goals, deliverables, success criteria
3. **Current state** — Is this a greenfield project or existing work? What tools/tech/resources are already in place?
4. **User involvement** — Do they want to be involved in every decision, or prefer the team to work autonomously?
5. **Special requirements** — Domain-specific standards, quality bars, deadlines, constraints

**Note**: Do not fire all questions at once. Follow up naturally based on the user's answers, like a normal conversation. If the user's requirements are already clear, you may skip some questions.

### 1.3 Recommend a Team Configuration

Based on the user's needs, recommend an appropriate combination of roles. Explain each role's purpose and why you're recommending it.

**The standard roles below are optimized for software development projects.** For non-software or mixed tasks, the team **framework** is universal (file-based planning, task folders, phase gates, review protocols) — but the **roles should be adapted** to the actual work. See "Adapting for Non-Software Projects" below.

Available standard roles (software development):

| Role | Name | Reference Agent | model | Core Capability |
|------|------|----------------|-------|----------------|
| Backend Dev | backend-dev | tdd-guide | opus | Write code + TDD + large tasks split into task folders |
| Frontend Dev | frontend-dev | tdd-guide | opus | Write code + TDD + large tasks split into task folders |
| Explorer/Researcher | researcher | — | sonnet | Code search + web research + read-only (no code edits) |
| E2E Tester | e2e-tester | e2e-runner | sonnet | E2E testing + browser automation + bug tracking |
| Code Reviewer | reviewer | code-reviewer | opus | Read-only review + deep security/quality/performance checks |
| Code Cleaner | cleaner | refactor-cleaner | sonnet | Dead code removal + deduplication + refactoring |

See [references/roles.md](references/roles.md) for detailed role definitions and capabilities.

**Recommendation principles**:
- More roles is not always better — choose based on actual project needs
- Small projects may only need 1 dev + 1 researcher
- Large projects can have the full set of roles
- **Multi-instance researchers**: For research-heavy projects with multiple independent directions (e.g., tech stack evaluation + codebase analysis + competitor research), spawn multiple researchers in parallel. Name them `researcher-1`/`researcher-2` or by focus area (`researcher-api`/`researcher-arch`). Each gets its own `.plans/` directory. No race conditions — researchers are read-only on source code and write only to their own directories
- Users can add custom roles (explain that custom roles require: name, responsibilities, model choice)

**Adapting for Non-Software Projects**:

The standard roles above are one proven configuration. For non-software or mixed tasks, design your own roles based on these principles:

1. **Separate creation from review** — whoever creates deliverables should not be the one reviewing them
2. **Research can parallelize** — independent information-gathering directions should be separate agents (see multi-instance researcher)
3. **Every team needs a quality gate** — someone whose job is to check the output before it's "done"
4. **The framework is universal** — task folders, findings.md, progress.md, 3-Strike, phase gates, and context recovery all work regardless of what the team is doing. Only the role names and responsibilities change

### 1.4 What Users Can Customize

Inform the user that the following can all be adjusted as needed:

- **Role composition**: Choose which roles to include and which to leave out
- **Custom roles**: If standard roles don't cover the need, new roles can be defined
- **Task phases**: How many phases the project has and the goal of each phase
- **Technical decisions**: Tech stack, framework choices, coding standards
- **Review strictness**: Whether code review or security review is required

Team-lead = the main conversation (you). Do not generate a team-lead agent.

If the user is improving an **existing team system** rather than starting from scratch, explicitly decide whether the change belongs in:

- the current project's docs only, or
- the `CCteam-creator` source templates themselves

Rule of thumb:

- project-specific workflow tweaks → update project docs
- durable team protocol changes (team-lead responsibilities, role boundaries, onboarding prompts, CLAUDE.md template, task/finding/progress conventions) → update `CCteam-creator` first

Do not recommend immediately rebuilding an active team unless the template changes are already written back and a phase boundary has been chosen.

## Step 2: Confirm the Plan

After thorough discussion, use AskUserQuestion to get final user confirmation on:

- **Project name**: Short, ASCII, kebab-case (e.g., `chatr`, `data-pipeline`)
- **Brief description**: 1-2 sentences
- **Confirmed role list**: Which roles are participating and what each is responsible for
- **Initial phase plan**: A rough breakdown of the project's key steps

Only proceed to the creation steps after the user confirms.

## Step 3: Create Planning Files

See [references/templates.md](references/templates.md) for file templates.

### Directory Structure

```
.plans/<project>/
  task_plan.md                -- Main plan (lean navigation map, not encyclopedia)
  findings.md                 -- Team-level summary
  progress.md                 -- Work log (archive old entries when bloated)
  decisions.md                -- Architecture decision log
  docs/                       -- Project knowledge base
    architecture.md           -- System architecture, components, data flow
    api-contracts.md          -- Frontend-backend API definitions
    invariants.md             -- Unbreakable system boundaries
  archive/                    -- Archived history (old progress, old plans)

  <agent-name>/               -- One directory per agent
    task_plan.md              -- Agent task list
    findings.md               -- INDEX only (keep lean, no content dumping)
    progress.md               -- Agent work log (archive old entries when bloated)
    <prefix>-<task>/          -- Task folder (one per assigned task)
      task_plan.md / findings.md / progress.md
```

### Task Folder Pattern (All Roles)

Every role creates task folders when assigned distinct tasks. The root `findings.md` serves as an **index** — linking to each task-specific findings file instead of dumping everything into one giant document.

| Role | Folder Prefix | Example |
|------|--------------|---------|
| backend-dev / frontend-dev | `task-` | `task-auth/`, `task-payments/` |
| researcher | `research-` | `research-tech-stack/`, `research-auth-options/` |
| e2e-tester | `test-` | `test-auth-flow/`, `test-checkout/` |
| reviewer | `review-` | `review-auth-module/`, `review-payments/` |
| cleaner | (uses root files) | — |

Example structure with multiple roles:

```
.plans/<project>/
  backend-dev/
    task_plan.md              -- Agent overview
    findings.md               -- INDEX: links to each task
    progress.md
    task-auth/                -- Feature: auth module
      task_plan.md / findings.md / progress.md
    task-payments/            -- Feature: payments
      task_plan.md / findings.md / progress.md

  researcher/
    task_plan.md              -- Research agenda
    findings.md               -- INDEX: links to each research report
    progress.md
    research-tech-stack/      -- Research: tech stack evaluation
      task_plan.md / findings.md / progress.md
    research-auth-options/    -- Research: auth approaches
      task_plan.md / findings.md / progress.md

  e2e-tester/
    task_plan.md              -- Test plan overview
    findings.md               -- INDEX: links to each test round
    progress.md
    test-auth-flow/           -- Test scope: auth flow
      task_plan.md / findings.md / progress.md

  reviewer/
    task_plan.md              -- Review queue
    findings.md               -- INDEX: links to each review
    progress.md
    review-auth-module/       -- Review: auth module
      findings.md / progress.md
```

Quick one-off notes (bug fixes, config changes) can go directly in root files without a task folder.

## Step 3.5: Generate Project CLAUDE.md

CLAUDE.md in the project working directory is **always loaded into the main session's context** by Claude Code. This is the mechanism that keeps team-lead operational knowledge persistent across context compressions.

### What to Generate

Create (or append to) a `CLAUDE.md` file in the **project working directory** (not inside `.plans/`).

See [references/templates.md](references/templates.md) for the CLAUDE.md template. The template must be **dynamically filled** based on the actual roles chosen in Step 2:
- Only list the roles that were confirmed
- Fill in the project name and directory paths
- Include custom roles if any were defined

### If CLAUDE.md Already Exists

If the project directory already has a CLAUDE.md, **append** the team operations section at the end (with a clear separator), do not overwrite the existing content.

### Why This Matters

Without this file, after context compression the team-lead loses all knowledge of:
- Which agents exist and their names
- How to dispatch tasks and check status
- Core protocols (3-Strike handling, code review triggers, phase advancement)

The CLAUDE.md solves this by keeping a concise operations guide permanently in context.

### When to Update CLAUDE.md

CLAUDE.md is a **living document**, not a one-time generation. Update it when:
- A recurring failure pattern is captured (→ append to `## Known Pitfalls`)
- Team roster changes (agent added/removed/rebuilt)
- A new protocol is established mid-project
- An architecture decision affects team workflow

Do NOT put task-level details here — only durable operational knowledge that survives context compression.

## Step 3.6: Create CI Script Skeleton (When Applicable)

If the project has testable code (backend, frontend, or both), create a CI script skeleton in the project directory (e.g., `scripts/run_ci.py` or `scripts/ci.sh`). The script should:

- Run all quality checks in one command (tests, type checks, contract validation, etc.)
- Exit 0 = all pass, exit 1 = failures
- Start with an empty check list — devs add checks as they write tests
- The first check is usually contract validation (if `docs/api-contracts.md` exists)

The skeleton does not need to be complete at project start — it grows as the project grows. But **the file must exist from day one**, otherwise no one will create it later.

Add the CI command to the project CLAUDE.md Key Protocols table so it survives context compression.

## Step 4: Create Team + Spawn Agents

1. `TeamCreate(team_name: "<project>")`
2. Create tasks via TaskCreate — each with a one-line scope + acceptance criteria + `.plans/` path in the description. Set dependencies (`addBlockedBy`) and owners (`owner`) via TaskUpdate. Prefer [AFK] tasks; specify input/output to minimize inter-agent information loss
3. Spawn each role in parallel, `run_in_background: true`

See [references/onboarding.md](references/onboarding.md) for the onboarding prompt for each role.

## Step 5: Confirm + Compact

Show the user a table of team members and the file locations.

Then **guide the user to run `/compact`** to free up context. Explain why:
- The setup process consumed significant context (reading templates, creating files, spawning agents)
- All operational knowledge is now persisted in CLAUDE.md (always loaded) and `.plans/` files
- Compacting reclaims context space for actual team management work
- After compaction, team-lead can resume immediately — CLAUDE.md keeps all protocols in context

## Key Rules

- **Dual-system, no duplication**: .plans/ files are the source of truth (persistent, project-scoped); native TaskCreate is the live dispatch layer (fast queries, auto-unblocking dependencies, but session-scoped — stored in `~/.claude/tasks/`, not in project). TaskCreate description = one-line summary + `.plans/` path. When resuming a project in a new session, reconstruct tasks from each agent's findings.md index
- **Team-lead is the control plane**: the main conversation owns user alignment, task decomposition, phase gates, main-plan maintenance, and CLAUDE.md upkeep
- **Context recovery**: After an agent is compacted, it must first read its task folder's files (or root files if no active task folder)
- **All roles use task folders**: Every assigned task gets a dedicated folder with its own findings/progress files; root findings.md is an index
- **Code review trigger**: Call reviewer after completing a feature/new module; small changes/bug fixes do not require review
- **researcher uses sonnet model**: Research requires sufficient depth
- **Spawn in parallel**: Launch all independent agents simultaneously
- **Peer Review**: dev reaches out to reviewer directly, without going through team-lead
- **Code is the source of truth**: Documentation follows the code. Devs MUST update `docs/api-contracts.md` and `docs/architecture.md` when code changes — undocumented APIs do not exist for other agents
- **Invariant-first for high-risk boundaries**: Recurring bugs should be promoted from Known Pitfalls to `docs/invariants.md`, then converted to automated tests. Reviewer is the second line of defense; automated tests are the first
- **Anti-bloat principle**: Root findings.md is a pure index (no content dumping). progress.md should be archived when it gets too long to scan quickly. task_plan.md is a lean navigation map — architecture, API specs, and tech details belong in `docs/`, not here
- **CI gate before review**: When a CI script exists, dev must run it and confirm all checks pass before submitting for review. Reviewer may reject code that hasn't passed CI. Tests written but not run = tests not written
- **Template-first for durable workflow changes**: if a discovered improvement affects role definitions, onboarding, CLAUDE.md structure, or dispatch protocols, update `CCteam-creator` source files before recommending a rebuild
- **Rebuild at phase boundaries**: do not rebuild an active team mid-stream unless necessary; prefer syncing templates first, then syncing project docs, then rebuilding between major phases
- **No archiving**: Completed task folders stay in place — just mark `Status: complete` in the root findings.md index. Do not rename, move, or prefix folders with `_archive_`. The index is the navigation layer; folder location must remain stable so cross-references don't break

## Team-Lead Operations Guide

### Applying planning-with-files in a Team Context

The core idea behind planning-with-files is: **file system = disk, context = memory, important things must be written to disk**.

In a team project, this principle operates at three levels:

| Level | Owner | File Location | Focus |
|-------|-------|--------------|-------|
| Project Global | team-lead | `.plans/<project>/task_plan.md` | Phase progress, architecture decisions, task assignments |
| Agent Level | Each agent individually | `.plans/<project>/<agent>/` | Task index, general notes, work log |
| Task Level | Each agent | `.plans/<project>/<agent>/<prefix>-<name>/` | Detailed steps, findings, and progress for a specific task |

Each agent's onboarding prompt already includes an equivalent self-check protocol (periodic 5-question check, 2-Action Rule, 3-Strike). The team-lead does not need to manually trigger these mechanisms — agents execute them autonomously.

> **Regarding `/planning-with-files:status`**: This command reads the single task_plan.md at the project root directory and is not aware of the team's multi-layered file structure. To check the main plan, directly Read `.plans/<project>/task_plan.md`.

### Team Status Check (team-lead Self-Check)

The team-lead should also follow a periodic self-check principle. It is recommended to proactively check at these moments:

**Quick scan** (read each agent's progress.md in parallel):
```
Read .plans/<project>/backend-dev/progress.md
Read .plans/<project>/frontend-dev/progress.md
Read .plans/<project>/researcher/progress.md
...（adjust for actual roles）
```

**Deep dive** (read findings.md when something seems off):
```
Read .plans/<project>/<agent-name>/findings.md
```

**Decision alignment** (read the main plan when direction needs adjustment):
```
Read .plans/<project>/task_plan.md
```

Reading order: **progress (where are we) → findings (what was encountered) → task_plan (what is the goal)**

### Team-Lead Owns the Control Plane

The team-lead is responsible for more than dispatch:

- user requirement alignment and scope control
- task decomposition with explicit inputs, outputs, and acceptance criteria
- maintaining `.plans/<project>/task_plan.md`, `decisions.md`, and project `CLAUDE.md`
- deciding phase gates: research → dev → review → e2e → cleanup
- deciding whether a workflow change is project-local or should be written back into `CCteam-creator`

If these responsibilities are not kept in the main conversation, the team may continue operating, but it will drift.

### Template Sync vs Project-Local Docs

When a team-level improvement is discovered, team-lead should classify it:

- **Project-local**: only this project needs it → update project docs
- **Template-level**: future teams should inherit it → update `CCteam-creator` source files first

Examples of template-level changes:

- team-lead responsibilities
- role boundaries
- onboarding protocol
- CLAUDE.md structure
- task/finding/progress conventions
- rebuild timing rules

Recommended order:

1. update `CCteam-creator`
2. sync the current project's docs
3. rebuild the team only if the change materially affects spawned-agent behavior

### Rebuild Timing

Do not default to "edit template then rebuild immediately".

Prefer rebuilding:

- after a major phase completes
- before the next major development cycle starts
- when role prompts changed enough that continuing with existing agents would cause inconsistent behavior

### Handling Agent 3-Strike Escalations

When an agent reports "3 failures, escalating to team-lead":
1. Read the attempted steps recorded in its progress.md
2. Assess whether the main plan (task_plan.md) needs to be revised
3. Provide a clear new direction, or reassign the task to another agent
4. **Guardrail check**: Will this failure pattern recur?
   - If YES for this project → append to CLAUDE.md `## Known Pitfalls` (symptom, root cause, fix, prevention)
   - If YES for future teams → also record `[TEAM-PROTOCOL]` and consider template update
   - If NO (one-off) → no further action

### Phase Advancement Cadence

- Research phase complete → Read researcher findings.md → Update the architecture decisions section in the main task_plan.md
- Development phase complete → Wait for reviewer results → Confirm [OK] or [WARN] before advancing to the next phase
- All done → Read each agent's progress.md in parallel, confirm all tasks are marked complete

**Phase boundary health check** (quick, do alongside phase advancement):
- Are all agent root findings.md indexes up to date? (no orphan task folders missing an index entry)
- Are there stale `in_progress` tasks in TaskList that should be completed or reassigned?
- Does main task_plan.md phase status match actual progress?
- Review CLAUDE.md Known Pitfalls — anything to include in next phase's task dispatch?
- Run Harness Checklist (see CLAUDE.md template)
