# CCteam-creator

> Multi-agent team orchestration plugin for [Claude Code](https://code.claude.com/).

[English](./README.md) | [中文](./README_CN.md)

## Standing on the Shoulders of Giants

CCteam-creator is built upon two outstanding open-source projects:

| Project | Stars | What We Learned |
|---------|-------|-----------------|
| [**planning-with-files**](https://github.com/OthmanAdi/planning-with-files) | 16,000+ | Manus-style persistent markdown planning — the 3-file pattern (task_plan.md / findings.md / progress.md) that survives context compression. The "context window = RAM, file system = disk" philosophy is the backbone of our state persistence. Born from the workflow pattern behind the [$2B Manus acquisition](https://github.com/OthmanAdi/planning-with-files). |
| [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | 50,000+ | The agent harness performance optimization system by Anthropic hackathon winner [@affaan-m](https://github.com/affaan-m). 13 expert agents, 40+ skills, 98% test coverage. Inspired our skill structure, role-based agent design, and plugin distribution approach. |

CCteam-creator extends their ideas into the **multi-agent coordination** domain — orchestrating multiple specialized agents working in parallel with structured communication and file-based progress tracking.

---

CCteam-creator helps you set up and manage parallel AI agent teams in Claude Code. Instead of working with a single AI assistant, you can orchestrate multiple specialized agents — developers, researchers, testers, reviewers — all working together on your project.

## What It Does

When you invoke `/CCteam-creator:setup`, CCteam-creator:

1. **Consults with you first** — explains how agent teams work, understands your project needs, and recommends a team configuration
2. **Sets up the team** — creates planning files, work directories, and spawns agents with proper onboarding
3. **Manages collaboration** — agents communicate directly (dev asks reviewer for code review), report progress to the team lead (you), and persist all state to files

## Prerequisites

### Enable Agent Teams

Agent teams are an experimental feature in Claude Code. You **must** enable them first:

**Option A: In your shell**
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**Option B: In settings.json** (`~/.claude/settings.json`)
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Installation

> **Important**: Install either the English version OR the Chinese version — not both. They are the same plugin in different languages. Installing both will cause conflicts.

### Option 1: Marketplace Install (Recommended)

```bash
# Step 1: Add the marketplace (run in Claude Code)
/plugin marketplace add jessepwj/CCteam-creator

# Step 2: Install the plugin — choose ONE language
/plugin install CCteam-creator@ccteam        # English
/plugin install CCteam-creator-cn@ccteam     # Chinese
```

### Option 2: Manual Copy — English (Default)

```bash
git clone https://github.com/jessepwj/CCteam-creator.git
cp -r CCteam-creator/plugins/CCteam-creator/skills/setup ~/.claude/skills/CCteam-creator
```

### Option 3: Manual Copy — Chinese

```bash
git clone https://github.com/jessepwj/CCteam-creator.git
cp -r CCteam-creator/plugins/CCteam-creator-cn/skills/setup ~/.claude/skills/CCteam-creator
```

> **Note**: Both manual options copy into the same target directory (`~/.claude/skills/CCteam-creator`). This ensures only one version is active at a time.

### Option 4: Project-level Install

Share the skill with your team by placing it in your project:

```bash
# English (default)
cp -r CCteam-creator/plugins/CCteam-creator/skills/setup .claude/skills/CCteam-creator

# Or Chinese
cp -r CCteam-creator/plugins/CCteam-creator-cn/skills/setup .claude/skills/CCteam-creator
```

## Usage

Simply tell Claude Code that you want to set up a team:

```
> Set up a team for my e-commerce project
> /CCteam-creator:setup
> I want to build a REST API, can you create a team?
```

> **Note**: If installed manually (Options 2-4), the command is `/CCteam-creator` instead of `/CCteam-creator:setup`.

CCteam-creator will:
1. Explain how the agent team works
2. Ask about your project goals, tech stack, and preferences
3. Recommend which roles you need
4. Confirm the plan with you
5. Create all planning files and spawn agents

### Trigger Keywords

The skill auto-activates when you mention: `team`, `swarm`, `start project`, `set up project`, `create team`, `build team`, `organize project`, `multi-agent project`.

## Available Roles

| Role | Name | Model | Capabilities |
|------|------|-------|-------------|
| Backend Dev | `backend-dev` | opus | Code + TDD + task-level file tracking |
| Frontend Dev | `frontend-dev` | opus | Code + TDD + task-level file tracking |
| Explorer/Researcher | `researcher` | sonnet | Code search + web research (read-only) |
| E2E Tester | `e2e-tester` | sonnet | Playwright E2E + browser automation |
| Code Reviewer | `reviewer` | opus | Security/quality/performance review (read-only on source) |
| Code Cleaner | `cleaner` | sonnet | Dead code removal + safe refactoring |

You don't need all roles for every project. CCteam-creator recommends the right combination based on your needs.

## How It Works

### File-Based Planning

All progress is persisted to `.plans/<project>/` — no state is lost when context compresses:

```
.plans/<project>/
  task_plan.md          -- Master plan (phases, architecture, assignments)
  findings.md           -- Team-level summary
  progress.md           -- Work log

  backend-dev/          -- Each agent's workspace
    findings.md         -- INDEX linking to task-specific findings
    task-auth/          -- Each assigned task gets its own folder
      task_plan.md / findings.md / progress.md

  researcher/
    findings.md         -- INDEX linking to research reports
    research-tech-stack/ -- Each research topic
      findings.md       -- THE research report (main deliverable)

  e2e-tester/
    findings.md         -- INDEX linking to test results
    test-auth-flow/     -- Each test scope
      findings.md       -- Test results and bugs

  reviewer/
    findings.md         -- INDEX linking to reviews
    review-auth-module/ -- Each code review
      findings.md       -- Full review report
```

Every role uses task folders — the root `findings.md` serves as a clean index, not a dump of all content.

### Agent Protocols

Every agent follows built-in protocols:
- **2-Action Rule**: Write findings after every 2 search/read operations (dev roles exempt during coding)
- **3-Strike Protocol**: Escalate to team lead after 3 failures on the same issue
- **Context Recovery**: On context compression, agents re-read their 3 planning files before continuing
- **Periodic Self-Check**: Every ~10 tool calls, agents verify alignment with their task plan

### Team Communication

- Agents report progress to the team lead (you)
- Developers request code review directly from the reviewer
- Large task handoffs include documentation (findings.md location + summary)
- The reviewer writes results to the developer's findings.md
- All communication is transparent and tracked

## Customization

You can customize:
- **Role selection** — pick only the roles you need
- **Custom roles** — define new roles with specific responsibilities
- **Task phases** — organize your project into custom stages
- **Review strictness** — enable/disable code review and security review gates

## Project Structure

```
CCteam-creator/
  .claude-plugin/
    marketplace.json                  -- Marketplace catalog
  plugins/
    CCteam-creator/                   -- English plugin
      .claude-plugin/
        plugin.json                   -- Plugin manifest
      skills/
        setup/                        -- The skill
          SKILL.md
          references/
            roles.md
            onboarding.md
            templates.md
    CCteam-creator-cn/                -- Chinese plugin
      .claude-plugin/
        plugin.json                   -- Plugin manifest
      skills/
        setup/                        -- The skill
          SKILL.md
          references/
            roles.md
            onboarding.md
            templates.md
  README.md                           -- English documentation
  README_CN.md                        -- Chinese documentation
  LICENSE                             -- MIT License
```

## License

MIT
