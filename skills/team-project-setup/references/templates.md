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

## Large Task Folder Templates (backend-dev / frontend-dev Only)

When a frontend or backend dev agent receives a large feature or new module, create the following in their directory:

```
.plans/<project>/<agent-name>/task-<feature-name>/
```

### Task Folder task_plan.md

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
- [ ] 6. Request reviewer review (required for large features)

## Files Involved

- `path/to/file1.ts` — <description>
- `path/to/file2.ts` — <description>

## Dependencies

- Depends on T1 research conclusions (see researcher findings.md)
- Depends on xxx API design (see main task_plan.md §6)
```

### Task Folder findings.md

```markdown
# <Feature Name> - Findings Log

> Technical findings during development of this task.

---

<Empty initially>
```

### Task Folder progress.md

```markdown
# <Feature Name> - Work Journal

> For context recovery, only this file needs to be read (not other task folders).

---

<Empty initially>
```
