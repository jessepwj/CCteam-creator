# CCteam-creator

> Multi-agent team orchestration skill for [Claude Code](https://code.claude.com/).

[English](./README.md) | [中文](./README_CN.md)

## Standing on the Shoulders of Giants

CCteam-creator is built upon outstanding open-source projects:

| Project | What We Learned |
|---------|-----------------|
| [**planning-with-files**](https://github.com/OthmanAdi/planning-with-files) | Manus-style persistent markdown planning — the 3-file pattern (task_plan.md / findings.md / progress.md) that survives context compression. The "context window = RAM, file system = disk" philosophy. |
| [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | Agent harness optimization by Anthropic hackathon winner. 13 expert agents, 40+ skills. Inspired our role-based agent design and skill structure. |
| [**mattpocock/skills**](https://github.com/mattpocock/skills) | TDD vertical-slice philosophy, "design it twice" parallel sub-agent pattern, interface durability principles, and plan stress-testing methodology. |

---

## What It Does

CCteam-creator sets up parallel AI agent teams in Claude Code. Instead of a single AI assistant, you orchestrate multiple specialized agents — developers, researchers, testers, reviewers — working together on your project.

When invoked, CCteam-creator:

1. **Consults with you** — explains how agent teams work, understands your project, recommends a team
2. **Sets up everything** — planning files, work directories, CLAUDE.md operations guide, agent onboarding
3. **Manages collaboration** — agents communicate directly, persist state to files, follow built-in protocols

## Prerequisites

Agent teams are an experimental feature in Claude Code. Enable them first:

```bash
# Option A: Environment variable
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Option B: In ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Installation

> **Important**: Install either the English OR Chinese version — not both.

### Option 1: Marketplace (Recommended)

```bash
# Step 1: Add the marketplace (in Claude Code)
/plugin marketplace add jessepwj/CCteam-creator

# Step 2: Install — choose ONE language
/plugin install CCteam-creator@ccteam        # English
/plugin install CCteam-creator-cn@ccteam     # Chinese
```

### Option 2: Manual Install

```bash
git clone https://github.com/jessepwj/CCteam-creator.git

# English
cp -r CCteam-creator/plugins/CCteam-creator/skills/setup ~/.claude/skills/CCteam-creator

# Or Chinese
cp -r CCteam-creator/plugins/CCteam-creator-cn/skills/setup ~/.claude/skills/CCteam-creator
```

### Option 3: Project-level Install

```bash
# Share with your team via project directory
cp -r CCteam-creator/plugins/CCteam-creator/skills/setup .claude/skills/CCteam-creator
```

## Usage

```
> Set up a team for my e-commerce project
> /CCteam-creator:setup
> Build a REST API with a team
```

> If installed manually, the command is `/CCteam-creator` instead of `/CCteam-creator:setup`.

**Trigger keywords**: `team`, `swarm`, `start project`, `set up project`, `create team`, `build team`, `multi-agent project`.

## Available Roles

| Role | Name | Model | Key Capabilities |
|------|------|-------|-----------------|
| Backend Dev | `backend-dev` | opus | Server code + TDD (vertical slices) + architecture-aware testing |
| Frontend Dev | `frontend-dev` | opus | Client code + TDD (vertical slices) + component testing |
| Researcher | `researcher` | sonnet | Code search + web research + plan stress-testing (read-only) |
| E2E Tester | `e2e-tester` | sonnet | Playwright E2E + browser automation + bug tracking |
| Code Reviewer | `reviewer` | opus | Security/quality/performance/architecture review (read-only on source) |
| Code Cleaner | `cleaner` | sonnet | Dead code removal + safe refactoring |

You don't need all roles. CCteam-creator recommends the right combination for your project.

## Key Features

### Requirements Alignment (Phase 0)

Before any development starts, the team performs structured requirements alignment:
- **Researcher** explores the existing codebase and documents architecture
- **Team-lead** aligns detailed requirements with the user
- Architecture decisions and scope are recorded in the plan before assigning dev tasks

### Vertical Slice Task Decomposition

Tasks are broken into **vertical slices** (tracer bullets), not horizontal layers. Each slice cuts through all layers end-to-end (schema → API → UI → tests) and is independently verifiable.

Every task includes:
- **[AFK]/[HITL]** — autonomous or needs human decision
- **blocked-by** — explicit dependency chain
- **Input/Output** — self-contained, minimizes inter-agent information loss
- **Acceptance criteria** — agents know exactly when they're done

### Plan Stress-Testing

Before finalizing architecture, team-lead delegates the researcher to stress-test the plan — walking every branch of the decision tree, identifying gaps and risks before development starts.

### TDD with Depth

Developers follow enhanced TDD:
- **Vertical slices**: one test → one implementation → repeat (never all tests first)
- **Behavior testing**: test WHAT the system does through public interfaces, not HOW
- **Mock boundaries**: only mock at system boundaries (external APIs, databases), never internal modules
- **Testable interfaces**: dependency injection, return results over side effects

### Architecture-Aware Code Review

The reviewer checks not just security/quality/performance, but also:
- **Shallow module detection** — interface complexity ≈ implementation complexity
- **Dependency classification** — in-process / local-substitutable / remote-owned / true-external
- **Test strategy assessment** — "replace, don't layer" redundant tests

### Durable Research Output

Researcher findings include both file paths (for immediate navigation) AND behavior descriptions (survive refactoring). Example:
> Auth logic in `src/auth/middleware.ts:42` — intercepts all /api/* routes, validates JWT from Authorization header, attaches decoded user to req.user.

### File-Based State Persistence

All progress persists to `.plans/<project>/`:

```
.plans/<project>/
  task_plan.md          -- Master plan with vertical slices
  findings.md           -- Team-level summary
  progress.md           -- Work log

  backend-dev/
    findings.md         -- INDEX → task findings
    task-auth/
      task_plan.md / findings.md / progress.md

  researcher/
    findings.md         -- INDEX → research reports
    research-tech-stack/
      findings.md       -- Research report (main deliverable)

  reviewer/
    findings.md         -- INDEX → review reports
    review-auth-module/
      findings.md       -- Full review report
```

### Built-in Agent Protocols

| Protocol | Purpose |
|----------|---------|
| 2-Action Rule | Write findings after every 2 search operations |
| 3-Strike Escalation | Escalate after 3 failures, never silent retry |
| Context Recovery | Re-read planning files after context compression |
| Periodic Self-Check | Verify alignment with plan every ~10 tool calls |
| Task Handoff | File-based handoff with summary + document location |

## Project Structure

```
CCteam-creator/
  .claude-plugin/
    marketplace.json              -- Marketplace catalog
  plugins/
    CCteam-creator/               -- English plugin
      .claude-plugin/plugin.json
      skills/setup/
        SKILL.md
        references/
          roles.md / onboarding.md / templates.md
    CCteam-creator-cn/            -- Chinese plugin
      .claude-plugin/plugin.json
      skills/setup/
        SKILL.md
        references/
          roles.md / onboarding.md / templates.md
  README.md / README_CN.md
  LICENSE
```

## License

MIT
