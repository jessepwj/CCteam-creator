---
name: CCteam-creator
description: >
  Set up a complete agent team with file-based planning for complex multi-agent projects.
  Use when: (1) user asks to start a new complex project with a team/swarm, (2) user says
  "set up team", "create team", "build a team for X", "start project X", (3) user invokes
  /CCteam-creator with a project name, (4) user wants to organize a multi-phase project
  with parallel agent workers and persistent progress tracking. Creates TeamCreate, planning
  files (.plans/project/), per-agent work directories, and spawns configured
  teammates. TRIGGER on: "team", "swarm", "start project", "set up project", "create team
  for", "build team", "organize project", "multi-agent project".
  IMPORTANT: You (team-lead) MUST read all reference files directly — do NOT delegate to subagents.
  NOTE: After initial setup, you can add new teammates at any time — just spawn a new Agent with the team_name and follow the same onboarding pattern. The team is not locked after creation.
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

**Step 0 Update Check (auto)**: Background version fetch + one-line notification if newer version exists
**Step 0 Detect (auto)**: Check if `.plans/` exists → if yes, offer to resume existing project
1. **Requirements Consultation** — Introduce the team mechanism to the user and gather requirements
2. **Confirm the Plan** — Summarize requirements and let the user confirm the team configuration
3. Create planning files (including per-agent subdirectories)
4. Create the team + spawn agents
5. Confirm setup + guide user to compact context

## Step 0 Update Check: Version Self-Check (Auto — Before Anything Else, ~2s)

Before any other step, perform a lightweight version check. **No user consent needed, do not ask any questions.**

1. **Remote version**: WebFetch `https://raw.githubusercontent.com/jessepwj/CCteam-creator/master/.claude-plugin/plugin.json` with prompt: "What is the value of the version field? Respond with just the version string."
2. **Local version**: Use Bash to read local plugin.json (try these paths in order, use the first that exists):

   ```bash
   cat ~/.claude/plugins/cache/ccteam/CCteam-creator/*/.claude-plugin/plugin.json 2>/dev/null || \
   cat ~/.claude/plugins/cache/ccteam/CCteam-creator-cn/*/.claude-plugin/plugin.json 2>/dev/null || \
   cat ~/.claude/skills/CCteam-creator/.claude-plugin/plugin.json 2>/dev/null
   ```

   Extract the version field from the output.
3. **Compare**:
   - **remote ≤ local**, OR **WebFetch failed**, OR **local plugin.json not found** → **completely silent**, proceed to the next step. Do NOT print "version check passed" or any confirmation noise
   - **remote > local** → print **one** notification line (just one, then immediately continue, do NOT wait for user reply):
     > ℹ️ A newer CCteam-creator version is available (<local> → <remote>). It will auto-apply on next Claude Code startup. Continuing with <local> in this session. For immediate effect: `/plugin marketplace update ccteam` → `/exit` → restart → re-trigger this skill.

**Hard rules**:
- ❌ Do NOT ask the user "continue with old version?" — no confirmation at all
- ❌ Do NOT attempt to Bash-update the plugin cache yourself — that's Claude Code's job, not the skill's
- ❌ Do NOT render the version check as a visible task in TodoWrite/TaskCreate — it should run in the background invisibly
- ❌ If the network fails, do NOT retry — just proceed
- ✅ At most one notification line, then **immediately** proceed to the next step

## Step 0 Detect: Detect Existing Project (Auto — Before Anything Else)

Before starting setup, check if `.plans/` directory exists in the current working directory.

**If `.plans/` exists**:
1. Read the project CLAUDE.md (auto-loaded) to get the team roster and project context
2. Scan `.plans/` for project directories — if multiple, list them
3. Tell the user: "I found an existing project [name] with [roster]. Resume this project or start a new one?"
4. **If resume**:
   a. Check if `.plans/<project>/team-snapshot.md` exists
   b. **If snapshot exists**: Read the snapshot header metadata. Compare skill source file timestamps against snapshot generation time:
      - **Source files unchanged** → use cached onboarding prompts from snapshot to spawn agents directly (skip reading skill reference files)
      - **Source files changed** → inform user: "Skill files have been updated since this team was created. Use cached config for fast resume, or re-read skill files to pick up latest protocols?" Let user decide
   c. **If no snapshot**: Fall back to reading all skill reference files (onboarding.md, roles.md) to rebuild onboarding prompts, then spawn agents
   d. After spawning, check TaskList / read progress files to pick up where things left off
5. **If new**: Proceed to Step 1 as normal

**If `.plans/` does not exist**: Skip directly to Step 1.

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

1. **Working language** — Observe the language the user communicates in. If they use English, the team responds in English; if Chinese, team responds in Chinese. Match the language in CLAUDE.md and onboarding prompts accordingly
2. **Task type** — Is this software development, research/analysis, content creation, data processing, or a mix? This determines whether standard roles apply directly or need adaptation
3. **What the user wants to accomplish** — Project goals, deliverables, success criteria
3. **Current state** — Is this a greenfield project or existing work? What tools/tech/resources are already in place?
4. **User involvement** — Do they want to be involved in every decision, or prefer the team to work autonomously?
5. **Special requirements** — Domain-specific standards, quality bars, deadlines, constraints
6. **Quality priorities** — What matters most for this project beyond "code works"? Examples: product depth (handles real edge cases), visual polish, performance, API design elegance, test coverage depth. These become Review Dimensions that the reviewer scores against. 3-5 dimensions, each with a weight (high/medium/low) and concrete calibration anchors (what STRONG vs WEAK looks like in this project's context)

**Note**: Do not fire all questions at once. Follow up naturally based on the user's answers, like a normal conversation. If the user's requirements are already clear, you may skip some questions.

### 1.3 Recommend a Team Configuration

Based on the user's needs, recommend an appropriate combination of roles. Explain each role's purpose and why you're recommending it.

**The standard roles below are optimized for software development projects.** For non-software or mixed tasks, the team **framework** is universal (file-based planning, task folders, phase gates, review protocols) — but the **roles should be adapted** to the actual work. See "Adapting for Non-Software Projects" below.

Available standard roles (software development):

| Role | Name | Reference Agent | model | Core Capability |
|------|------|----------------|-------|----------------|
| Backend Dev | backend-dev | tdd-guide | sonnet | Write code + TDD + large tasks split into task folders |
| Frontend Dev | frontend-dev | tdd-guide | sonnet | Write code + TDD + large tasks split into task folders |
| Explorer/Researcher | researcher | — | sonnet | Code search + web research + read-only (no code edits) |
| E2E Tester | e2e-tester | e2e-runner | sonnet | E2E testing + browser automation + bug tracking |
| Code Reviewer | reviewer | code-reviewer | sonnet | Read-only review + deep security/quality/performance checks |
| Custodian | custodian | refactor-cleaner | sonnet | Constraint compliance + doc governance + pattern→automation + code cleanup |

> **Model default**: All roles use `sonnet`. Upgrade specific roles to `opus` only when the user requests it, cost is not a concern, or the role handles critical/complex logic (e.g., security-sensitive review, complex business logic). Ask the user during Step 1 if unsure.

See [references/roles.md](references/roles.md) for detailed role definitions and capabilities.

**Recommendation principles**:
- More roles is not always better — choose based on actual project needs
- Small projects may only need 1 dev + 1 researcher
- Large projects can have the full set of roles
- **Multi-instance researchers**: Spawn multiple researchers when the research workload is large enough to benefit from parallelism. Two main patterns:
  - **Volume splitting** (most common): Same type of work, split by quantity. E.g., 30 source files to analyze → researcher-1 takes modules A-M, researcher-2 takes N-Z. Same responsibilities, just faster through parallel processing
  - **Direction splitting**: Fully independent research topics. E.g., tech stack evaluation + codebase analysis + competitor research — each produces its own conclusions with no dependency on the others
  - Name by number (`researcher-1`/`researcher-2`) for volume splits, by focus (`researcher-api`/`researcher-arch`) for direction splits. Each gets its own `.plans/` directory. No race conditions — researchers are read-only on source code
  - **Anti-pattern**: Do NOT split when direction B depends on A's output (e.g., "first determine auth approach, then research libraries for it") — a single researcher sequentially is faster than two in a blocking chain
- **custodian is recommended for teams with 4+ agents or long-running projects**. For small teams (2-3 agents), custodian overhead may not be worth it — team-lead can absorb the compliance checks directly
- Users can add custom roles (explain that custom roles require: name, responsibilities, model choice)

**Adapting for Non-Software Projects**:

The standard roles above are one proven configuration. For non-software or mixed tasks, design your own roles based on these principles:

1. **Separate creation from review** — whoever creates deliverables should not be the one reviewing them
2. **Research can parallelize** — independent information-gathering directions should be separate agents (see multi-instance researcher)
3. **Quality gate and validation are different things** — reviewing the work (is it well-made?) is not the same as validating the result (does it actually achieve the goal?). Consider whether you need both
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
    index.md                  -- Navigation map with sections & line ranges (custodian maintains)
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
| custodian | `audit-` | `audit-phase1-compliance/`, `audit-doc-health/` |

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

### docs/index.md — Dynamic Navigation Map

In Step 3, also create `docs/index.md` — a detailed navigation map showing each doc's sections and line ranges. This file is maintained by custodian and actively Read by agents when they need to find specific information. CLAUDE.md points to it but does NOT duplicate it (CLAUDE.md is only loaded at session start / after compact, so dynamic nav info belongs in docs/index.md).

See [references/templates.md](references/templates.md) for the docs/index.md template.

### When to Update CLAUDE.md

CLAUDE.md is a **living document**, not a one-time generation. Update it when:
- A recurring failure pattern is captured (→ append to `## Known Pitfalls`)
- Team roster changes (agent added/removed/rebuilt)
- A new protocol is established mid-project
- An architecture decision affects team workflow

Do NOT put task-level details here — only durable operational knowledge that survives context compression.

## Step 3.6: Harness Setup (When Applicable)

If the project has testable code (backend, frontend, or both), set up the enforcement infrastructure:

### Golden Rules (Pre-installed Checks)

Copy the bundled golden_rules.py from this skill into the project:

```bash
cp <skill-path>/scripts/golden_rules.py <project>/scripts/golden_rules.py
```

Then configure `SRC_DIRS` at the bottom of the copied file to match the project's source directories (e.g., `["src"]`, `["backend", "frontend"]`).

golden_rules.py provides 5 universal checks out of the box:
- **GR-1 File Size**: files >800 lines WARN, >1200 lines FAIL
- **GR-2 Hardcoded Secrets**: regex scan for API keys, tokens, passwords
- **GR-3 Console Log**: console.log in production code (not test files)
- **GR-4 Doc Freshness**: docs/ files stale vs source code commits
- **GR-5 Invariant Coverage**: invariants.md entries without automated tests

custodian can add project-specific checks to golden_rules.py over time (see roles.md § Golden Rules Maintenance).

### CI Script Skeleton

Create a CI script skeleton (`scripts/run_ci.py`):

- Import and call `golden_rules.check_all()` as the first step
- Run all quality checks in one command (golden rules + tests + type checks + contract validation)
- Exit 0 = all pass, exit 1 = failures
- Devs add project-specific checks as they write tests
- The first project-specific check is usually contract validation (if `docs/api-contracts.md` exists)

### Check Script Error Message Standard

All check scripts (CI, contract validation, architecture linters) MUST produce agent-readable error messages with fix instructions:

```
# BAD: agent cannot act on this
ERROR: api-contracts.md out of sync

# GOOD: agent can directly fix this
[CONTRACT-SYNC] POST /api/auth/refresh — exists in code but not in docs
  File: src/auth/controller.py:142
  FIX: Add to docs/api-contracts.md under "Auth API" section.
  Format: | POST | /api/auth/refresh | Refresh JWT token | { token: string } |
```

The skeleton does not need to be complete at project start — it grows as the project grows. But **the file must exist from day one**, otherwise no one will create it later.

Add the CI command to the project CLAUDE.md Key Protocols table so it survives context compression.

## Step 4: Create Team + Spawn Agents

1. `TeamCreate(team_name: "<project>")`
2. Create tasks via TaskCreate — each with a one-line scope + acceptance criteria + `.plans/` path in the description. Set dependencies (`addBlockedBy`) and owners (`owner`) via TaskUpdate. Specify input/output to minimize inter-agent information loss
3. Spawn each role in parallel, `run_in_background: true`

See [references/onboarding.md](references/onboarding.md) for the onboarding prompt for each role.

4. **Generate team snapshot**: After all agents are spawned, write `.plans/<project>/team-snapshot.md` containing the rendered onboarding prompts and skill file timestamps. See [references/templates.md](references/templates.md) for the template. This enables fast resume without re-reading all skill files.

## Step 5: Confirm + Compact

Show the user a table of team members and the file locations.

Then **guide the user to run `/compact`** to free up context. Explain why:
- The setup process consumed significant context (reading templates, creating files, spawning agents)
- All operational knowledge is now persisted in CLAUDE.md (loaded at session start) and `.plans/` files
- Compacting reclaims context space for actual team management work

### MUST warn the user before compaction (important!)

Tell the user the following — verbatim or paraphrased:

> **After compaction, team-lead may "lose memory"** — forgetting teammate names, operational protocols, and the current project context. This is normal behavior of Claude Code's compaction: CLAUDE.md is only injected at session start, and the compactor rewrites history (including the team roster and protocols) into a summary, so details can be lost.
>
> **If I (team-lead) seem confused after compaction, just tell me one sentence**:
>
> > "Read `.plans/<project>/team-snapshot.md` to restore team state"
>
> This makes me reload the full team roster and all onboarding prompts, returning to a working state immediately. All progress is in `.plans/` files — nothing is lost.

This warning **must** be delivered before guiding `/compact` — otherwise the user will hit an amnesiac lead and not know the rescue command.

## Key Rules

- **Dual-system, no duplication**: .plans/ files are the source of truth (persistent, project-scoped); native TaskCreate is the live dispatch layer (fast queries, auto-unblocking dependencies, but session-scoped — stored in `~/.claude/tasks/`, not in project). TaskCreate description = one-line summary + `.plans/` path. When resuming a project in a new session, reconstruct tasks from each agent's findings.md index
- **Team-lead is the control plane**: the main conversation owns user alignment, task decomposition, phase gates, main-plan maintenance, and CLAUDE.md upkeep
- **Context recovery**: After an agent is compacted, it must first read its task folder's files (or root files if no active task folder)
- **All roles use task folders**: Every assigned task gets a dedicated folder with its own findings/progress files; root findings.md is an index
- **Code review trigger**: Call reviewer after completing a feature/new module; small changes/bug fixes do not require review
- **researcher uses sonnet model**: research requires sufficient depth
- **Spawn in parallel**: Launch all independent agents simultaneously
- **No standalone subagents after team exists**: Once the team is created, ALL work goes through teammates via SendMessage — do NOT spawn standalone Agent/subagent (Explore, general-purpose, etc.) to do work that a teammate should handle. Subagents bypass the team's planning files, findings, and coordination. The only exception is spawning a new teammate (with `team_name`) to permanently join the team
- **Peer Review**: dev reaches out to reviewer directly, without going through team-lead
- **Code is the source of truth**: Documentation follows the code. Devs MUST update `docs/api-contracts.md` and `docs/architecture.md` when code changes — undocumented APIs do not exist for other agents
- **Invariant-first for high-risk boundaries**: Recurring bugs should be promoted from Known Pitfalls to `docs/invariants.md`, then converted to automated tests. Reviewer is the second line of defense; automated tests are the first
- **Pattern → Automation pipeline**: When reviewer tags `[AUTOMATE]` on a recurring pattern, team-lead routes it to custodian, who builds a check script with agent-readable error messages and adds it to CI. Goal: convert manual checks into automated enforcement so reviewer can focus on deeper judgment calls
- **Anti-bloat principle**: Root findings.md is a pure index (no content dumping). progress.md should be archived when it gets too long to scan quickly. task_plan.md is a lean navigation map — architecture, API specs, and tech details belong in `docs/`, not here
- **CI gate before review**: When a CI script exists, dev must run it and confirm all checks pass before submitting for review. Reviewer may reject code that hasn't passed CI. Tests written but not run = tests not written
- **Template-first for durable workflow changes**: if a discovered improvement affects role definitions, onboarding, CLAUDE.md structure, or dispatch protocols, update `CCteam-creator` source files before recommending a rebuild
- **Rebuild at phase boundaries**: do not rebuild an active team mid-stream unless necessary; prefer syncing templates first, then syncing project docs, then rebuilding between major phases
- **No archiving**: Completed task folders stay in place — just mark `Status: complete` in the root findings.md index. Do not rename, move, or prefix folders with `_archive_`. The index is the navigation layer; folder location must remain stable so cross-references don't break
- **Assumption audit**: Every harness component encodes an assumption about what the model cannot do well on its own. These assumptions go stale as models improve. At major model upgrades or when a mechanism repeatedly adds no value, team-lead should run the Assumption Audit (see CLAUDE.md Harness Checklist) and simplify what is no longer load-bearing. Principle: find the simplest solution possible, only increase complexity when needed

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

### Message Delivery Timing Constraint (Critical — Affects All Dispatch)

**Mechanism** (verified empirically, not documented elsewhere): `SendMessage` to a spawned teammate is **NOT delivered mid-turn**. The recipient only picks up new messages when idle (between turns). You cannot interrupt an agent while it is actively working on a task — the message queues until the agent finishes its current turn and replies.

**This is a hard constraint of the spawning/messaging system, not a discipline rule.** Team-lead must plan dispatches around it.

**Consequences for dispatch strategy**:

1. **Front-load everything in the initial message**. Since you cannot add "oh, also do X" mid-task, the dispatch message must contain all context, acceptance criteria, dependency file paths, constraints, and expected output format. Missing context = the agent burns a full turn on wrong assumptions before you get a chance to correct.

2. **You cannot mid-course correct a running agent**. If priorities shift or you spot an error, you must wait for its current turn to end. The correction queues and lands at the next idle. Plan assuming no interruption window.

3. **Dispatch granularity is a speed-vs-control tradeoff**:
   - **Smaller tasks** → more checkpoints, faster course correction, more SendMessage overhead
   - **Larger tasks** → fewer roundtrips, longer blindness windows, harder to redirect if the approach is wrong
   - **Rule of thumb**: High-uncertainty work (exploratory, novel, ambiguous spec) → smaller tasks. Low-uncertainty work (well-specified, routine, familiar pattern) → larger tasks.

4. **Urgent broadcasts are not urgent**. `SendMessage(to: "*", …)` for a stop-everything signal will still only land per-recipient at their next idle. Agents mid-task will run to completion of their current turn. There is no preemption.

5. **"How's it going?" pings do not work mid-task**. You cannot peek at in-progress work via messages. Instead, read the agent's own `progress.md` / `findings.md` / task folder files — **files are live, messages are not**. This is the single most important operational corollary: when you need to know what an agent is doing *right now*, read its files, do not message it.

6. **Multi-part bundling is sometimes the correct choice**. When parts of a job must be done sequentially without roundtrip latency (e.g., "implement A, then immediately run CI, then report all results"), bundle them into one message and rely on the agent's Multi-Part Recognition protocol (see onboarding.md) to enumerate and execute each part. Bundling trades checkpoint granularity for zero-latency sequencing — both directions have costs, pick based on the task.

**Corollary — File system beats messages for live state**: Messages convey intent and decisions at turn boundaries; files convey continuous state at any time. When you need current ground truth about an agent, the answer is always in its files — progress.md for "what just happened", findings.md for "what was learned", task_plan.md for "what's the plan". Messages carry requests and responses, not status.

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
- **Environmental pre-flight check**: Does the next phase require a specific runtime state (service restart, seed data, cache clear, DB migration applied)? Project-specific pre-flight steps are tracked in CLAUDE.md `## Known Pitfalls`. Run them BEFORE dispatching agents that depend on live state (typically e2e-tester and integration-focused devs) — do not rely on the previous phase's dev to remember. Environmental side effects should also appear in each dev's completion report as a standard field
- Run Harness Checklist (see CLAUDE.md template)
