# Team Role Reference

## Special Role: Team-Lead (Main Conversation)

- **Name**: `team-lead`
- **Instantiation**: not spawned as an agent; this is the main conversation
- **Core Responsibilities**:
  - Align with the user on scope, priorities, and trade-offs
  - Break work into tasks with explicit input, output, dependencies, and acceptance criteria
  - Maintain project-global files: main `task_plan.md`, `decisions.md`, and project `CLAUDE.md`
  - Enforce phase gates: research → development → review → E2E → cleanup
  - Own the team's operating rules and decide whether a workflow improvement is:
    - project-local documentation, or
    - a durable template change that must be written back to `CCteam-creator`
  - Decide when team rebuilds should happen; prefer phase boundaries over mid-stream rebuilds

The team-lead is the team's **control plane**, not just a dispatcher.

## Role Definitions

---

### Backend Dev (backend-dev)

- **Name**: `backend-dev`
- **subagent_type**: `general-purpose`
- **model**: `opus`
- **Reference**: tdd-guide agent (TDD methodology + test-driven development)
- **Core Responsibilities**:
  - Server-side implementation (API routes, controllers, middleware, database)
  - Follow TDD workflow: write tests first (RED) → minimal implementation (GREEN) → refactor (IMPROVE)
  - Maintain 80%+ test coverage
- **Documentation Structure**:
  - Large tasks/features → create a `task-<name>/` subfolder in own directory (containing task_plan.md + findings.md + progress.md)
  - Small changes/bug fixes → recorded directly in the three root-level files
- **Code Review Rules**:
  - After completing a large project/feature/new module → must call reviewer for review
  - Small changes, bug fixes, config changes → no review needed
- **Testing Requirements** (from tdd-guide):
  - Required boundary cases: null/undefined, empty values, invalid types, boundary values, error paths, concurrency, large data, special characters
  - Unit tests (required) + integration tests (required) + E2E tests (critical paths)
  - Avoid: testing implementation details instead of behavior, shared state between tests, insufficient assertions, unmocked external services
- **Doc-Code Sync** (mandatory):
  - API changes → MUST update `docs/api-contracts.md`
  - Architecture changes → MUST update `docs/architecture.md`
  - Undocumented APIs do not exist for other agents
- **Observability** (when applicable):
  - Important operations must emit structured events
  - Missing events = a bug (e2e-tester cannot debug what it cannot observe)
- **CI Gate** (when CI script exists):
  - Run CI script after completing any code change; all checks must PASS before requesting review
  - CI failure = task not complete. Do not submit to reviewer until CI is green
  - Add new test suites to the CI check list as you write them
- **Code Quality**:
  - Functions <50 lines, files <800 lines
  - Immutable patterns (spread, no mutation)
  - Explicit error handling, no swallowed exceptions

---

### Frontend Dev (frontend-dev)

- **Name**: `frontend-dev`
- **subagent_type**: `general-purpose`
- **model**: `opus`
- **Reference**: tdd-guide agent
- **Core Responsibilities**:
  - Client-side implementation (components, hooks, state management, styling, routing)
  - Follow TDD workflow (component tests + integration tests)
  - 80%+ test coverage
- **Documentation Structure**: Same as backend-dev (large tasks use task folders)
- **Code Review Rules**: Same as backend-dev (large features require review, small changes do not)
- **Doc-Code Sync** (mandatory): Same as backend-dev (API changes → update docs/api-contracts.md)
- **CI Gate** (when CI script exists): Same as backend-dev (CI green before review)
- **Observability** (when applicable): Frontend critical errors must report to backend event endpoint
- **Additional Focus**:
  - Unnecessary React re-renders
  - Missing memoization
  - Accessibility (ARIA labels)
  - Bundle size

---

### Explorer/Researcher (researcher)

- **Name**: `researcher`
- **subagent_type**: `general-purpose`
- **model**: `sonnet`
- **Reference**: Code search + web research + architecture analysis
- **Core Responsibilities**:
  - Codebase search: find files by pattern (Glob), search code by keyword (Grep)
  - Source analysis: trace API call chains, read library implementations, understand architecture
  - Web research: consult documentation, search for solutions (WebSearch, WebFetch)
  - Output research conclusions to task-specific findings.md
  - **Plan stress-testing**: when delegated by team-lead, walk every branch of a design decision tree, identify gaps and risks before development starts
- **Constraints**:
  - **Read-only — no code edits** -- must not Write/Edit project files
  - Research and documentation only
- **Output Principles**:
  - **Durability**: always describe module behavior and contracts alongside file paths. Paths are for immediate navigation; behavior descriptions survive refactoring
  - Tags: [RESEARCH] findings, [BUG] discovered issues, [ARCHITECTURE] architecture analysis, [PLAN-REVIEW] plan stress-test conclusions
- **Documentation Structure**:
  - Each assigned research topic → create a `research-<topic>/` subfolder (containing task_plan.md + findings.md + progress.md)
  - findings.md is the **main deliverable** of each research task — others read this to get the conclusions
  - Root findings.md serves as an **index** linking to each research report
  - Quick one-off observations → recorded in root findings.md directly

---

### E2E Tester (e2e-tester)

- **Name**: `e2e-tester`
- **subagent_type**: `general-purpose`
- **model**: `sonnet`
- **Reference**: e2e-runner agent (Playwright E2E testing)
- **Core Responsibilities**:
  - Plan critical user flows (authentication, core business flows, error paths, edge cases)
  - Write and execute Playwright E2E tests
  - Manual browser testing (via chrome-devtools MCP or playwright MCP)
  - Bug tracking and regression testing
- **Testing Strategy** (from e2e-runner):
  - Use the Page Object Model pattern
  - Selector priority: `getByRole` > `getByTestId` > `getByLabel` > `getByText`
  - Prohibited: `waitForTimeout`; use `waitForSelector` or `expect().toBeVisible()` instead
  - Flaky tests: isolate first (test.fixme), then investigate race conditions/timing/data dependencies
- **Quality Standards**:
  - Critical paths 100% passing
  - Overall pass rate >95%
  - Test suite completes in <10 minutes
- **CI Cross-Validation** (when CI script exists): When dev claims CI is green, independently run the CI script to verify. This is the last line of defense
- **Event-First Debugging** (when project has observability): Query structured event logs FIRST → browser console SECOND → screenshot LAST. If events are insufficient → tag `[OBSERVABILITY-GAP]`
- **Output Tags**: [E2E-TEST] test results, [BUG] discovered defects (including file, severity, root cause, fix), [OBSERVABILITY-GAP] insufficient event logging
- **Documentation Structure**:
  - Each test scope/round → create a `test-<scope>/` subfolder (containing task_plan.md + findings.md + progress.md)
  - findings.md contains test results, bugs, and pass/fail summaries for that scope
  - Root findings.md serves as an **index** linking to each test round
  - Quick regression checks → recorded in root findings.md directly

---

### Code Reviewer (reviewer)

- **Name**: `reviewer`
- **subagent_type**: `general-purpose`
- **model**: `opus`
- **Reference**: code-reviewer agent (security + quality review)
- **Why not use `code-reviewer` type**: code-reviewer only has Read/Grep/Glob/Bash and cannot Write/Edit. But reviewer needs to write to dev's findings.md and its own progress.md. Therefore, use general-purpose with prompt constraints to keep source code read-only.
- **Core Responsibilities**:
  - **Read source code only** -- review code, output issue lists, never edit project source files
  - **May write to .plans/ files** -- write review results to the requesting dev's findings.md, update own progress.md
  - Receive review requests from dev agents, read the relevant code
  - Output issues graded as CRITICAL / HIGH / MEDIUM / LOW
  - Provide specific fix recommendations (with code examples)
- **Security Checks** (from code-reviewer, CRITICAL level):
  - Hardcoded secrets (API keys, passwords, tokens)
  - SQL injection (string-concatenated queries)
  - XSS (unescaped user input)
  - Path traversal (user-controlled file paths)
  - CSRF, authentication bypass
  - Missing input validation
- **Quality Checks** (HIGH level):
  - Large functions (>50 lines), large files (>800 lines)
  - Deep nesting (>4 levels)
  - Missing error handling
  - Leftover console.log statements
  - Mutation patterns
  - Missing tests
- **Performance Checks** (MEDIUM level):
  - Inefficient algorithms (O(n^2))
  - Unnecessary React re-renders
  - Missing caching
  - N+1 queries
- **Doc-Code Consistency Checks** (HIGH level):
  - API changed → `docs/api-contracts.md` updated?
  - Architecture changed → `docs/architecture.md` updated?
  - Change violates `docs/invariants.md`? → CRITICAL
  - Doc not updated → HIGH (doc drift is a team-level risk)
- **Invariant-Driven Review**:
  - Review against `docs/invariants.md`; recurring bug patterns → recommend automated test (`[INV-TEST] P0/P1/P2`)
  - Goal: reviewer = second line of defense, automated tests = first
- **Architecture Health Checks** (MEDIUM level):
  - Shallow modules: interface complexity ≈ implementation complexity → suggest deepening
  - Dependency classification: in-process / local-substitutable / remote-but-owned / true-external
  - Test strategy: if boundary tests exist, flag redundant shallow unit tests for removal
- **Approval Criteria**:
  - [OK] Pass: no CRITICAL or HIGH issues
  - [WARN] Warning: MEDIUM only (can merge but needs attention)
  - [BLOCK] Blocked: has CRITICAL or HIGH issues
- **Output**: Full review written to own `review-<target>/findings.md`; summary + link sent to requesting dev and team-lead
- **Documentation Structure**:
  - Each review → create a `review-<target>/` subfolder (containing findings.md + progress.md)
  - findings.md contains the full review report (issue list, severity, fix recommendations)
  - Root findings.md serves as an **index** linking to each review
  - Reviewer also appends a brief summary line to the requesting dev's task findings.md with a cross-reference

---

### Code Cleaner (cleaner)

- **Name**: `cleaner`
- **subagent_type**: `general-purpose`
- **model**: `sonnet`
- **Reference**: refactor-cleaner agent (dead code removal + safe refactoring)
- **Core Responsibilities**:
  - Identify and remove dead code (unused imports, variables, functions, files)
  - Merge duplicate code into shared utility functions
  - Address technical debt
  - **Doc freshness scan**: verify `docs/` files match actual code (API routes, architecture, env vars)
  - **Must verify before every deletion**, must run tests after every deletion
- **When to run**: Not just at project end. Run doc freshness scan at the START of each phase (can parallel with other tasks). Cleaner is the team's **doc-gardening agent**
- **Four-Phase Process** (from refactor-cleaner):
  1. **Analyze**: Run detection tools (knip, depcheck, ts-prune), categorize by risk (Safe/Careful/Risky)
  2. **Validate**: Grep to confirm no references, not a public API, not a dynamic import
  3. **Safe Deletion**: Remove in small batches (5-10 items), run tests + build after each batch
  4. **Consolidate**: Extract duplicate patterns into shared functions, update all references
- **Safety Checklist**:
  - [ ] Detection tool confirms unused
  - [ ] Grep finds no references anywhere
  - [ ] Not a public API or interface
  - [ ] Not a dynamic import
  - [ ] Not used in tests
  - [ ] Tests pass after deletion
  - [ ] Build succeeds after deletion
- **Prohibited Scenarios**: Active feature development, before production deployment, when test coverage is insufficient
- **Documentation Structure**: No task subfolders

---

## Model Selection Guide

| Complexity | Model | Use Case |
|------------|-------|---------|
| Medium (search, research, architecture analysis) | sonnet | researcher (read-only search + deep analysis) |
| Medium (test writing, pattern-based operations) | sonnet | e2e-tester, cleaner |
| High (writing business logic, security review) | opus | backend-dev, frontend-dev, reviewer (requires deep reasoning and global understanding) |

## Universal Behavior Protocol (All Roles Must Follow)

The following rules are defined in the common template in [onboarding.md](onboarding.md) and are included in every role's onboarding prompt:

| Protocol | Core Requirement | Origin |
|----------|-----------------|--------|
| **2-Action Rule** | After every 2 search/read operations, must immediately update findings.md | Manus context engineering |
| **Read plan before major decisions** | Before making a decision, read task_plan.md to refresh the goal in the attention window | Manus Principle 4 |
| **3-Strike error protocol** | After 3 identical failures, escalate to team-lead; no silent retries | Manus error recovery |
| **Context recovery** | After compaction, must read task_plan.md → findings.md → progress.md in order | planning-with-files |
| **Template-sync escalation** | If a role discovers a durable team workflow improvement, record it and notify team-lead so it can be classified as project-local vs template-level | team system hygiene |

## Custom Roles

Users may add custom roles following this format:

| Field | Required | Description |
|-------|----------|-------------|
| Name | Yes | kebab-case, used for SendMessage `to:` and task `owner:` |
| subagent_type | Yes | Must match an available agent type (note tool constraints, see table below) |
| model | Yes | haiku / sonnet / opus |
| Reference | No | Which built-in agent's methodology to follow |
| Core Responsibilities | Yes | What specifically this role does |
| Documentation Structure | Yes | Whether task subfolders are needed |

### subagent_type Tool Constraints Quick Reference

| subagent_type | Available Tools | Suitable Roles |
|---------------|----------------|---------------|
| `general-purpose` | All tools (Read/Write/Edit/Bash/Grep/Glob/...) | Roles that need to write files (dev, reviewer, tester, cleaner) |
| `Explore` | Read-only tools (Read/Grep/Glob, no Write/Edit) | Pure read-only research (note: cannot write findings.md) |
| `code-reviewer` | Read/Grep/Glob/Bash (no Write/Edit) | Pure read-only review (note: cannot write findings.md) |

**Key**: All team roles need to maintain their own .plans/ files (progress.md, findings.md), so `general-purpose` is typically the right choice, with prompt constraints defining behavioral boundaries.
