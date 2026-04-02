# CCteam-creator

> Multi-agent team orchestration skill for [Claude Code](https://code.claude.com/).

**One skill, a full engineering team.** CCteam-creator turns a single Claude Code session into a coordinated team of 2-6 AI agents — with built-in CI enforcement, code review, doc-code sync, and a taste feedback loop that encodes your preferences into automated checks. Human steers, agents execute.

[English](./README.md) | [中文](./README_CN.md)

## Standing on the Shoulders of Giants

CCteam-creator is built upon outstanding open-source projects and engineering practices:

| Source | What We Learned |
|--------|-----------------|
| [**planning-with-files**](https://github.com/OthmanAdi/planning-with-files) | Manus-style persistent markdown planning — the 3-file pattern (task_plan.md / findings.md / progress.md) that survives context compression. The "context window = RAM, file system = disk" philosophy. |
| [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | Agent harness optimization by Anthropic hackathon winner. 13 expert agents, 40+ skills. Inspired our role-based agent design and skill structure. |
| [**mattpocock/skills**](https://github.com/mattpocock/skills) | TDD vertical-slice philosophy, "design it twice" parallel sub-agent pattern, interface durability principles, and plan stress-testing methodology. |
| [**OpenAI Harness Engineering**](https://openai.com/index/harness-engineering/) | The discipline of designing constraints, feedback loops, and documentation systems that make AI agents reliable at scale. Inspired our docs/ knowledge base, invariant-driven review, Doc-Code Sync, failure-to-guardrail loop, and anti-bloat principles. |
| [**Anthropic Harness Design**](https://www.anthropic.com/engineering/harness-design) | Anthropic Labs' research on multi-agent architectures for long-running autonomous coding. Three key lessons absorbed into CCteam-creator: (1) **Evaluator calibration** — out-of-the-box LLMs are poor QA agents that rationalize away issues; the fix is few-shot calibration anchors with concrete STRONG/WEAK examples, which shaped our Review Dimensions system. (2) **Every harness component is an assumption** — each mechanism encodes a belief about what the model can't do alone, and these assumptions go stale as models improve; this became our Assumption Audit checklist. (3) **Generator-evaluator separation** — separating the agent doing the work from the agent judging it is more tractable than making a generator self-critical, validating our existing dev/reviewer split and motivating the anti-leniency rule. |

---

## What It Does

CCteam-creator sets up parallel AI agent teams in Claude Code. Instead of a single AI assistant, you orchestrate multiple specialized agents — developers, researchers, testers, reviewers — working together on your project.

When invoked, CCteam-creator:

1. **Consults with you** — explains how agent teams work, understands your project, recommends a team
2. **Sets up everything** — planning files, docs/ knowledge base, CLAUDE.md operations guide, agent onboarding
3. **Manages collaboration** — agents communicate directly, persist state to files, follow built-in protocols

## In Action

Screenshots from a real project session (ChatR — a full-stack chat application with event-driven observability).

### 1. Team Roster & Dependency Chain

After setup, team-lead summarizes the team roster, task assignments, and dependency graph. All agents receive their onboarding and begin preparing.

![Team Roster](docs/images/01-team-roster.png)

### 2. Parallel Task Dispatch

Team-lead orchestrates 6 agents simultaneously — researcher and custodian start immediately (no dependencies), while devs prepare and wait for research output. Each agent knows its dependencies.

![Parallel Dispatch](docs/images/02-parallel-dispatch.png)

### 3. Development Phase — 3 Agents Working in Parallel

Backend-dev, frontend-dev, and e2e-tester all working concurrently. Team-lead tracks status, makes scheduling decisions (e.g., bypassing a dependency when enough info is available), and coordinates handoffs.

![Development Phase](docs/images/03-development-phase.png)

### 4. Code Review & Peer Coordination

Agents communicate directly — frontend-dev submits to reviewer, reviewer reports completion, team-lead tracks the status table with real-time progress from all 6 agents.

![Review Coordination](docs/images/04-review-coordination.png)

### 5. Phase Harness Validation

Team-lead runs a phase-level harness check — verifying each task's completion status, reviewer verdicts, e2e test results, and doc consistency before advancing to the next phase.

![Harness Validation](docs/images/05-harness-validation.png)

### 6. Final Dashboard — All Agents, One View

The complete validation checklist with reviewer [OK], e2e-tester PASS/FAIL status, and doc consistency verification. Bottom shows Claude Code's real-time agent HUD with all 6 teammates and their token usage.

![Final Dashboard](docs/images/06-final-dashboard.png)

---

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
cp -r CCteam-creator/skills/CCteam-creator ~/.claude/skills/CCteam-creator

# Or Chinese
cp -r CCteam-creator/cn/skills/CCteam-creator ~/.claude/skills/CCteam-creator
```

### Option 3: Project-level Install

```bash
# Share with your team via project directory
cp -r CCteam-creator/skills/CCteam-creator .claude/skills/CCteam-creator
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
| Backend Dev | `backend-dev` | sonnet | Server code + TDD + Doc-Code Sync + observability (when applicable) |
| Frontend Dev | `frontend-dev` | sonnet | Client code + TDD + Doc-Code Sync + component testing |
| Researcher | `researcher` | sonnet | Code search + web research + plan stress-testing (read-only) |
| E2E Tester | `e2e-tester` | sonnet | Playwright E2E + event-first debugging + bug tracking |
| Code Reviewer | `reviewer` | sonnet | Security/quality/performance + doc consistency + invariant-driven review |
| Custodian | `custodian` | sonnet | Constraint compliance + doc governance + pattern→automation + code cleanup |

You don't need all roles. CCteam-creator recommends the right combination for your project.

## Key Features

### Team-Lead as Control Plane

The main conversation acts as team-lead — not just a task dispatcher, but the **control plane** owning user alignment, phase gates, and the team's durable operating rules. Team-lead maintains the project CLAUDE.md (always in context), task_plan.md, and decisions.md.

### docs/ Knowledge Base (Harness Engineering)

Inspired by OpenAI's harness engineering approach, each project gets a structured `docs/` directory as the single source of truth:

```
.plans/<project>/docs/
  architecture.md     -- System architecture, components, data flow
  api-contracts.md    -- Frontend-backend API definitions (field-level specs)
  invariants.md       -- Unbreakable system boundaries (security, data isolation, contracts)
```

**Doc-Code Sync**: When code changes an API or architecture, devs MUST update the corresponding docs/ file. Reviewer checks this on every review. Undocumented APIs don't exist for other agents.

### Lean Navigation Map

task_plan.md is a **navigation map**, not an encyclopedia. Architecture, API specs, and tech stack details live in `docs/`. This keeps the main plan focused and prevents bloat — the plan stays readable even in large projects.

### Invariant-Driven Review

Recurring bug patterns are promoted from Known Pitfalls to formal invariants in `docs/invariants.md`. Reviewer checks code against invariants and recommends converting repeated patterns into automated tests. Goal: automated tests are the first line of defense, reviewer is the second.

### Failure-to-Guardrail Loop

When a 3-Strike escalation is resolved or a reviewer [BLOCK] is fixed, team-lead asks: "Will this recur?" If yes, it gets captured in CLAUDE.md's Known Pitfalls section — ensuring the same mistake never happens again. This is the core harness engineering insight: every failure becomes a permanent guardrail.

### Anti-Bloat Principles

Learned from real projects where files grew to 50,000+ tokens:
- **Root findings.md** is a pure index — no content dumping
- **progress.md** gets archived when it becomes too long to scan
- **task_plan.md** stays lean — details belong in docs/

### Requirements Alignment (Phase 0)

Before any development starts, the team performs structured requirements alignment:
- **Researcher** explores the existing codebase and documents architecture
- **Team-lead** aligns detailed requirements with the user
- Architecture decisions and scope are recorded in the plan before assigning dev tasks

### Vertical Slice Task Decomposition

Tasks are broken into **vertical slices** (tracer bullets), not horizontal layers. Each slice cuts through all layers end-to-end (schema → API → UI → tests) and is independently verifiable.

### TDD with Depth

Developers follow enhanced TDD:
- **Vertical slices**: one test → one implementation → repeat (never all tests first)
- **Behavior testing**: test WHAT the system does through public interfaces, not HOW
- **Mock boundaries**: only mock at system boundaries (external APIs, databases), never internal modules

### Architecture-Aware Code Review with Calibrated Scoring

The reviewer checks security/quality/performance, plus:
- **Doc-Code consistency** — API/architecture docs updated?
- **Invariant violations** — does the change break system boundaries?
- **Shallow module detection** — interface complexity ≈ implementation complexity
- **Test strategy** — "replace, don't layer" redundant tests

**Review Dimensions** (inspired by Anthropic's evaluator calibration research): Each project defines 3-5 weighted review dimensions during setup (e.g., product depth, code testability, API design elegance). The reviewer scores each dimension as STRONG / ADEQUATE / WEAK with calibration anchors — concrete descriptions of what good and bad look like in this project's context. If any dimension scores WEAK, the review cannot pass. An **anti-leniency rule** prevents the reviewer from rationalizing issues away — a known failure mode of LLM self-evaluation identified in Anthropic's research.

### Observability Support (When Applicable)

For web apps and services, devs are guided to emit structured events. E2E tester uses **event-first debugging**: query event logs first, browser console second, screenshots last. Insufficient observability is tagged `[OBSERVABILITY-GAP]` — a higher-priority finding than the bug itself.

### Golden Rules (Pre-installed CI Checks)

Every project ships with `golden_rules.py` — 5 universal code health checks that run automatically as part of CI:

| Check | What It Catches |
|-------|----------------|
| GR-1 File Size | Files over 800/1200 lines |
| GR-2 Secrets | Hardcoded API keys, tokens, passwords |
| GR-3 Console Log | console.log in production code |
| GR-4 Doc Freshness | docs/ files stale vs source code |
| GR-5 Invariant Coverage | Invariants without automated tests |

All error messages are agent-readable (`[WHAT] + [WHERE] + [HOW TO FIX]`), so agents can fix issues directly. Custodian adds project-specific checks over time — the script grows with the project.

### Taste Feedback Loop

User preferences don't get lost between sessions. When you say "don't name it like that" or "always use X pattern":

1. **team-lead captures** the preference in CLAUDE.md `Style Decisions`
2. **reviewer checks** new code against recorded style decisions
3. **After 3+ occurrences**, custodian **encodes it into golden_rules.py** as an automated check
4. The preference is now **mechanically enforced** — no one needs to remember it

This is the taste-to-code pipeline: human judgment becomes automated enforcement.

### Team Snapshot (Fast Resume)

When a team is first created, CCteam-creator saves a **team snapshot** (`.plans/<project>/team-snapshot.md`) containing the fully rendered onboarding prompts for every agent, along with skill source file timestamps. When you resume a project after exiting Claude Code:

- **Skill files unchanged** → agents are spawned directly from cached prompts, skipping the expensive re-read of all skill reference files (~2500 lines → ~200 lines)
- **Skill files updated** → lead is informed and can choose: fast resume with cached config, or re-read skill files to pick up latest protocol changes

This makes team resume nearly instant while ensuring you always know when cached config might be stale.

### File-Based State Persistence

All progress persists to `.plans/<project>/`:

```
.plans/<project>/
  task_plan.md          -- Lean navigation map
  team-snapshot.md      -- Cached onboarding prompts for fast resume
  docs/                 -- Project knowledge base
    architecture.md / api-contracts.md / invariants.md
  archive/              -- Archived history

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
| Guardrail Capture | Turn resolved failures into Known Pitfalls |
| Context Recovery | Progressive disclosure: docs/ → task files → progress |
| Periodic Self-Check | Verify alignment with plan every ~10 tool calls |
| Doc-Code Sync | Devs update docs/ when code changes; reviewer verifies |
| Phase Health Check | Verify doc freshness, stale tasks, index integrity at phase boundaries |
| Assumption Audit | Review whether each harness component is still load-bearing at model upgrades or retros |
| Review Dimensions | Reviewer scores project-specific quality dimensions with calibration anchors |
| Escalation Judgment | Devs classify decisions: decide yourself vs must ask team-lead with options |
| Task Confirmation | Devs read full context and confirm understanding before starting large tasks |
| Taste Capture | Record user style preferences; encode into automated checks after 3+ occurrences |
| Golden Rules CI | Pre-installed checks run automatically; custodian adds project-specific checks over time |

### Assumption Audit (Harness Evolution)

Inspired by Anthropic's insight that "every harness component encodes an assumption about what the model cannot do well on its own." At phase boundaries or model upgrades, team-lead runs an Assumption Audit — reviewing each mechanism (task folders, 3-Strike, context recovery, reviewer pass, etc.) to determine if it's still load-bearing. Components that triggered fewer than 2 times in the last phase and whose removal wouldn't have caused quality drops are candidates for simplification. **Principle**: the interesting harness combinations don't shrink as models improve — they move.

### Dev Escalation Judgment

Dev agents are not purely mechanical executors. They classify decisions into two levels:
- **Decide yourself** — implementation details, test strategy, tool choices within established patterns
- **Must ask team-lead** — ambiguous requirements, scope explosion, architecture impact, irreversible choices (API shape, DB schema)

When escalating, devs must include options and a recommendation — never bare questions. This prevents both silent derailment (going off track without asking) and excessive interruption (asking about every detail).

### Task Confirmation (Sprint Contract)

For large tasks, dev agents first read and understand the full context — referenced planning files, relevant source code, existing architecture — then confirm their understanding with team-lead before starting. If team-lead's dispatch message is missing document setup info, the dev reminds them. Inspired by the sprint contract pattern from Anthropic's research, where generator and evaluator negotiate "what done looks like" before any code is written.

### Living CLAUDE.md

CLAUDE.md is not a one-time generation — it's a **living document** that evolves with the project. Updated when failure patterns are captured, team roster changes, or new protocols are established.

## Known Limitation: Teammate Context Cannot Be Compacted

With **200k context** (default), teammates auto-compact when context fills up — this works fine and requires no special handling.

With **1M context**, teammates **cannot auto-compact** and cannot run `/compact` manually. As context grows, performance degrades and costs increase significantly — yet the extra context often provides diminishing returns.

**Recommendation**: Use 200k context (default) for team projects. If you do use 1M context and notice slowdowns:

1. Exit Claude Code completely (`Ctrl+C` or `/exit`)
2. Resume with `claude --continue`
3. Team-lead reads `.plans/` files to restore project state (CLAUDE.md is auto-loaded)
4. Re-spawn teammates — they start fresh with clean context and re-read their own `.plans/` files for recovery

This is a Claude Code platform limitation, not a CCteam-creator issue. All agent progress is persisted in `.plans/` files, so no work is lost on restart.

## Project Structure

```
CCteam-creator/
  .claude-plugin/
    marketplace.json              -- Marketplace catalog
    plugin.json                   -- English plugin metadata
  skills/
    CCteam-creator/               -- English skill
      SKILL.md
      scripts/
        golden_rules.py           -- Pre-installed universal code health checks
      references/
        roles.md / onboarding.md / templates.md
  cn/                             -- Chinese variant
    .claude-plugin/plugin.json
    skills/
      CCteam-creator/
        SKILL.md
        scripts/
          golden_rules.py
        references/
          roles.md / onboarding.md / templates.md
  docs/images/                    -- Screenshots
  README.md / README_CN.md
  LICENSE
```

## Star History

<a href="https://star-history.com/#jessepwj/CCteam-creator&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=jessepwj/CCteam-creator&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=jessepwj/CCteam-creator&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=jessepwj/CCteam-creator&type=Date" />
 </picture>
</a>

## License

MIT
