# Planning File Templates

## Main task_plan.md

```markdown
# <Project Name> - Main Plan

> Status: PLANNING
> Created: <date>
> Updated: <date>
> Team: <team-name> (<role list>)
> Decision Log: memory/<project>-decisions.md

---

## 1. Project Overview

<1-2 paragraph project description>

---

## 2. Key Architecture Decisions

<Fill in during planning phase; record each decision and its rationale>

---

## 3. Tech Stack

<List of technologies, frameworks, and versions>

---

## 4. Directory Structure

<Project file layout>

---

## 5. Task Breakdown

### Phase 1: Research
- [ ] T1: <description> — Assigned to: researcher

### Phase 2: Core Development
- [ ] T2: <description> — Assigned to: backend-dev
- [ ] T3: <description> — Assigned to: frontend-dev

### Phase 3: Integration Testing
- [ ] T4: <description> — Assigned to: e2e-tester

### Phase 4: Review & Cleanup
- [ ] T5: Code review — Assigned to: reviewer
- [ ] T6: Dead code cleanup — Assigned to: cleaner

---

## 6. API Documentation

<Fill in incrementally as APIs are designed/discovered>
```

## Main findings.md

```markdown
# <Project Name> - Findings & Technical Log

> Automatically updated by team agents. Each entry is tagged with its source.

---

<Add entries during work in the following format:>

## [TAG] <date> — <title>

### Source: <agent-name>

<content>

---

Tag Reference:
- [RESEARCH] Research findings
- [BUG] Defect records
- [CODE-REVIEW] Code review results
- [REVIEW-FIX] Review issue fixes
- [SECURITY-REVIEW] Security review
- [ARCHITECTURE] Architecture analysis
- [E2E-TEST] End-to-end test results
- [INTEGRATION] Integration issues
```

## Main progress.md

```markdown
# <Project Name> - Progress Log

> Recorded chronologically. Each entry notes who did what.

---

## <date> Session N — <title>

### Completed
- [x] <item>

### To Do
- [ ] <item>

### Key Decisions
- <decision and rationale>
```

---

## Agent Root task_plan.md

```markdown
# <Agent Name> - Task Plan

> Role: <role description>
> Status: pending
> Assigned Tasks: <list>

## Tasks

- [ ] Step 1: <description>
- [ ] Step 2: <description>
- [ ] Step 3: <description>

## Notes

<Context, constraints, and references relevant to this agent>
```

## Agent Root findings.md

```markdown
# <Agent Name> - Findings Log

> Issues and technical notes discovered during work.

---

<Empty initially; fill in during work>
```

## Agent Root progress.md

```markdown
# <Agent Name> - Work Journal

> For context recovery. Read this file first after compaction/restart.

---

<Empty initially; fill in during work>
```

---

## Task Folder Templates

All roles use task folders when assigned distinct tasks. The folder prefix varies by role:

| Role | Prefix | Example |
|------|--------|---------|
| backend-dev / frontend-dev | `task-` | `task-auth/`, `task-payments/` |
| researcher | `research-` | `research-tech-stack/`, `research-auth-options/` |
| e2e-tester | `test-` | `test-auth-flow/`, `test-checkout/` |
| reviewer | `review-` | `review-auth-module/`, `review-payments/` |
| cleaner | (uses root files) | — |

---

### Dev Task Folder (backend-dev / frontend-dev)

```
.plans/<project>/<agent-name>/task-<feature-name>/
```

#### task_plan.md

```markdown
# <Feature Name> - Task Plan

> Agent: <agent-name>
> Status: in_progress
> Created: <date>

## Goal

<What this feature needs to accomplish>

## Detailed Steps

- [ ] 1. <step description>
- [ ] 2. <step description>
- [ ] 3. <step description>
- [ ] 4. Write tests (TDD)
- [ ] 5. Verify coverage >= 80%
- [ ] 6. Request reviewer review (required for features)

## Files Involved

- `path/to/file1.ts` — <description>
- `path/to/file2.ts` — <description>

## Dependencies

- Depends on T1 research conclusions (see researcher/research-<topic>/findings.md)
- Depends on xxx API design (see main task_plan.md §6)
```

#### findings.md

```markdown
# <Feature Name> - Findings Log

> Technical findings during development of this task.

---

<Empty initially>
```

#### progress.md

```markdown
# <Feature Name> - Work Journal

> For context recovery, only this file needs to be read (not other task folders).

---

<Empty initially>
```

---

### Research Folder (researcher)

```
.plans/<project>/researcher/research-<topic>/
```

#### task_plan.md

```markdown
# Research: <Topic> - Plan

> Agent: researcher
> Status: in_progress
> Created: <date>

## Research Questions

1. <What needs to be answered?>
2. <What are the alternatives?>
3. <What are the trade-offs?>

## Approach

- [ ] 1. <search/read strategy>
- [ ] 2. <web research targets>
- [ ] 3. <source code analysis scope>
- [ ] 4. Compile conclusions into findings.md
- [ ] 5. Update root index

## Scope

<What is in scope / out of scope for this research>
```

#### findings.md (Main Deliverable)

```markdown
# Research: <Topic> - Report

> This is the main research deliverable. Others read this to get conclusions.
> Agent: researcher
> Status: in_progress
> Created: <date>

---

## Summary

<Executive summary — fill in when research is complete>

## Detailed Findings

<Add findings as research progresses, using 2-Action Rule>

### [RESEARCH] <date> — <finding title>

<content with exact file paths, line numbers, and evidence>

---

## Conclusions & Recommendations

<Fill in when research is complete>
```

#### progress.md

```markdown
# Research: <Topic> - Search Log

> Records what was searched and found. For context recovery and avoiding redundant searches.

---

<Empty initially>
```

---

### Test Folder (e2e-tester)

```
.plans/<project>/e2e-tester/test-<scope>/
```

#### task_plan.md

```markdown
# Test: <Scope> - Plan

> Agent: e2e-tester
> Status: in_progress
> Created: <date>

## Test Scope

<What user flows / features are being tested>

## Test Cases

- [ ] TC1: <description> — Priority: CRITICAL
- [ ] TC2: <description> — Priority: HIGH
- [ ] TC3: <description> — Priority: MEDIUM

## Prerequisites

- <What must be deployed/running before tests can execute>
```

#### findings.md

```markdown
# Test: <Scope> - Results

> Test results and bug reports for this scope.
> Agent: e2e-tester
> Status: in_progress

---

## Summary

| Metric | Value |
|--------|-------|
| Total tests | — |
| Passed | — |
| Failed | — |
| Pass rate | — |

## Results

<Add test results as tests are executed>

### [E2E-TEST] <date> — <test name>

- Status: PASS | FAIL
- Duration: <time>
- Details: <notes>

### [BUG] <date> — <bug title>

- File: <path:line>
- Severity: CRITICAL | HIGH | MEDIUM | LOW
- Root cause: <analysis>
- Fix recommendation: <suggestion>
```

#### progress.md

```markdown
# Test: <Scope> - Execution Log

> For context recovery.

---

<Empty initially>
```

---

### Review Folder (reviewer)

```
.plans/<project>/reviewer/review-<target>/
```

#### findings.md

```markdown
# Review: <Target> - Report

> Code review results.
> Agent: reviewer
> Requested by: <dev-agent-name>
> Status: in_progress
> Created: <date>

---

## Verdict: [OK] | [WARN] | [BLOCK]

## Issues

<Add issues found during review>

### [CRITICAL] <title>

- File: <path:line>
- Issue: <description>
- Fix: <recommendation with code example>

### [HIGH] <title>

- File: <path:line>
- Issue: <description>
- Fix: <recommendation>

## Summary

- CRITICAL: 0
- HIGH: 0
- MEDIUM: 0
- LOW: 0
```

#### progress.md

```markdown
# Review: <Target> - Notes

> Review process notes.

---

<Empty initially>
```

---

### Root findings.md as Index (All Roles)

Every agent's root findings.md should serve as an index. Example:

```markdown
# <Agent Name> - Findings Index

> Links to task-specific findings. Quick one-off notes also go here.

---

## task-auth
- Status: complete
- Report: [findings.md](task-auth/findings.md)
- Summary: Auth module implemented with JWT + refresh tokens

## task-payments
- Status: in_progress
- Report: [findings.md](task-payments/findings.md)
- Summary: Payment integration with Stripe

---

## Quick Notes

<One-off observations that don't belong to any specific task>
```
