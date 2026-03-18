---
name: CCteam-creator
description: >
  Set up a complete agent team with file-based planning for complex multi-agent projects.
  Use when: (1) user asks to start a new complex project with a team/swarm, (2) user says
  "set up team", "create team", "build a team for X", "start project X", (3) user invokes
  /CCteam-creator with a project name, (4) user wants to organize a multi-phase project
  with parallel agent workers and persistent progress tracking. Creates TeamCreate, planning
  files (.plans/project/), memory files, per-agent work directories, and spawns configured
  teammates. TRIGGER on: "team", "swarm", "start project", "set up project", "create team
  for", "build team", "organize project", "multi-agent project".
---

# Team Project Setup

Set up a multi-agent team for complex projects, using persistent files for planning and progress tracking.

## Process

1. **Requirements Consultation** — Introduce the team mechanism to the user and gather requirements
2. **Confirm the Plan** — Summarize requirements and let the user confirm the team configuration
3. Create planning files (including per-agent subdirectories)
4. Create memory files
5. Create the team + spawn agents
6. Confirm setup

## Step 1: Requirements Consultation (Talk First, Then Act)

**Goal of this step**: Help the user fully understand how the team works, while gathering their actual requirements. Do not rush to create any files or teams.

### 1.1 Introduce the Team Mechanism

In a natural, conversational tone (do not copy this text verbatim — adapt to context), explain the following points:

**What a team is**:
- You (Claude) act as team-lead, simultaneously directing multiple AI agents working in parallel
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
- Each agent has its own working directory (`.plans/<project>/`), recording tasks, findings, and progress
- Agents escalate blockers to the team-lead, who provides direction after review
- After development, devs automatically request a code review from the reviewer

### 1.2 Gather User Requirements

After the introduction, learn the following through conversation:

1. **What the user wants to build** — Project goals, feature requirements, technology preferences
2. **Current state** — Is this a greenfield project or an existing codebase? Is there an existing tech stack?
3. **User involvement** — Do they want to be involved in every decision, or prefer the team to work autonomously?
4. **Special requirements** — Any specific coding standards, testing requirements, or deployment targets?

**Note**: Do not fire all questions at once. Follow up naturally based on the user's answers, like a normal conversation. If the user's requirements are already clear, you may skip some questions.

### 1.3 Recommend a Team Configuration

Based on the user's needs, recommend an appropriate combination of roles. Explain each role's purpose and why you're recommending it.

Available standard roles:

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
- Users can add custom roles (explain that custom roles require: name, responsibilities, model choice)

### 1.4 What Users Can Customize

Inform the user that the following can all be adjusted as needed:

- **Role composition**: Choose which roles to include and which to leave out
- **Custom roles**: If standard roles don't cover the need, new roles can be defined
- **Task phases**: How many phases the project has and the goal of each phase
- **Technical decisions**: Tech stack, framework choices, coding standards
- **Review strictness**: Whether code review or security review is required

Team-lead = the main conversation (you). Do not generate a team-lead agent.

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
  task_plan.md                -- Main plan
  findings.md                 -- Team-level summary
  progress.md                 -- Work log

  <agent-name>/               -- One directory per agent
    task_plan.md              -- Agent task list
    findings.md               -- INDEX linking to task-specific findings
    progress.md               -- Agent work log
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

## Step 4: Create Memory Files

In the project memory directory:

1. Create `memory/<project>-decisions.md` with only a title
2. Append the project entry to `memory/MEMORY.md`:
   ```
   ## Project: <Name>
   - Status: PLANNING
   - Plans: .plans/<project>/
   - Decisions: [<project>-decisions.md](<project>-decisions.md)
   ```

## Step 5: Create Team + Spawn Agents

1. `TeamCreate(team_name: "<project>")`
2. Spawn each role in parallel, `run_in_background: true`

See [references/onboarding.md](references/onboarding.md) for the onboarding prompt for each role.

## Step 6: Confirm

Show the user a table of team members and the file locations.

## Key Rules

- **Planning files are the progress tracker** -- Do not also use TaskCreate/TodoWrite
- **Context recovery**: After an agent is compacted, it must first read its task folder's files (or root files if no active task folder)
- **All roles use task folders**: Every assigned task gets a dedicated folder with its own findings/progress files; root findings.md is an index
- **Code review trigger**: Call reviewer after completing a feature/new module; small changes/bug fixes do not require review
- **researcher uses sonnet model**: Research requires sufficient depth
- **Spawn in parallel**: Launch all independent agents simultaneously
- **Peer Review**: dev reaches out to reviewer directly, without going through team-lead
- **Code is the source of truth**: Documentation follows the code

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

### Handling Agent 3-Strike Escalations

When an agent reports "3 failures, escalating to team-lead":
1. Read the attempted steps recorded in its progress.md
2. Assess whether the main plan (task_plan.md) needs to be revised
3. Provide a clear new direction, or reassign the task to another agent

### Phase Advancement Cadence

- Research phase complete → Read researcher findings.md → Update the architecture decisions section in the main task_plan.md
- Development phase complete → Wait for reviewer results → Confirm [OK] or [WARN] before advancing to the next phase
- All done → Read each agent's progress.md in parallel, confirm all tasks are marked complete
