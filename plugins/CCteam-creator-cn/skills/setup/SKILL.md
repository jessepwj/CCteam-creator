---
name: setup
description: >
  Set up a complete agent team with file-based planning for complex multi-agent projects.
  Use when: (1) user asks to start a new complex project with a team/swarm, (2) user says
  "set up team", "create team", "build a team for X", "start project X", (3) user invokes
  /CCteam-creator-cn:setup with a project name, (4) user wants to organize a multi-phase project
  with parallel agent workers and persistent progress tracking. Creates TeamCreate, planning
  files (.plans/project/), per-agent work directories, and spawns configured
  teammates. TRIGGER on: "team", "swarm", "start project", "set up project", "create team
  for", "build team", "organize project", "multi-agent project".
---

# 团队项目设置

为复杂项目设置多智能体团队，使用持久化文件进行规划和进度追踪。

## 流程

1. **需求咨询** — 向用户介绍团队机制、了解需求
2. **确认方案** — 汇总需求，让用户确认团队配置
3. 创建规划文件（含智能体子目录）
4. 创建团队 + 生成智能体
5. 确认设置

## 第 1 步：需求咨询（先沟通，后动手）

**这一步的目标**：让用户充分理解团队是怎么运作的，同时收集用户的真实需求。不要急于创建任何文件或团队。

### 1.1 向用户介绍团队机制

用自然对话的方式（不要照搬下面的原文，根据上下文灵活表达），向用户解释以下要点：

**团队是什么**：
- 你（Claude）作为 team-lead，会同时指挥多个 AI 智能体并行工作
- Team-lead 是**主对话的控制平面**，不是一个被生成的 teammate
- 每个智能体有明确的角色分工（开发、研究、测试、审查等）
- 智能体之间可以直接沟通（如 dev 直接找 reviewer 审查代码）
- 所有进度通过文件系统持久化，不怕上下文丢失

**适合什么场景**：
- 多模块并行开发的项目（前后端同时推进）
- 需要调研 + 开发 + 测试多阶段协作的任务
- 代码量较大，需要审查和质量把关的项目

**不适合什么场景**：
- 简单的单文件修改或小 Bug 修复
- 只需要单一角色的任务（直接用单个 Agent 更高效）

**运作逻辑**：
- team-lead（你自己）负责分配任务、协调进度、做决策
- team-lead 还负责用户对齐、阶段推进以及团队持久化运营规则的维护
- 每个智能体有自己的工作目录（`.plans/<项目>/`），记录任务、发现和进度
- 智能体遇到问题会上报 team-lead，team-lead 裁决后给出方向
- 代码开发完成后，dev 会自动找 reviewer 做代码审查

### 1.2 了解用户需求

在介绍完机制后，通过对话了解：

1. **用户想做什么** — 项目目标、功能需求、技术偏好
2. **项目现状** — 是全新项目还是已有代码库？有没有现成的技术栈？
3. **用户的参与度** — 想全程参与决策，还是希望团队自主推进？
4. **特殊要求** — 有没有特定的编码规范、测试要求、部署目标？

**注意**：不要一次性抛出所有问题。根据用户的回答逐步深入，像正常对话一样自然交流。如果用户的需求已经很清晰，可以跳过部分问题。

### 1.3 推荐团队配置

根据用户需求，推荐合适的角色组合。解释每个角色的作用和为什么推荐它。

可用的标准角色：

| 角色 | 名称 | 参考智能体 | model | 核心能力 |
|------|------|-----------|-------|---------|
| 后端开发 | backend-dev | tdd-guide | opus | 写代码 + TDD + 大任务按 task 分文件夹 |
| 前端开发 | frontend-dev | tdd-guide | opus | 写代码 + TDD + 大任务按 task 分文件夹 |
| 探索/研究 | researcher | — | sonnet | 代码搜索 + 网页搜索 + 只读不改代码 |
| 联调测试 | e2e-tester | e2e-runner | sonnet | E2E 测试 + 浏览器自动化 + Bug 记录 |
| 代码审查 | reviewer | code-reviewer | opus | 只读审查 + 安全/质量/性能深度检查 |
| 代码清理 | cleaner | refactor-cleaner | sonnet | 死代码清理 + 重复合并 + 重构 |

参见 [references/roles.md](references/roles.md) 了解角色详细定义和能力。

**推荐原则**：
- 不是角色越多越好，根据项目实际需要选择
- 小项目可能只需要 1 个 dev + 1 个 researcher
- 大项目可以配齐全部角色
- 用户可以添加自定义角色（解释自定义角色需要提供：名称、职责、模型选择）

### 1.4 用户可自定义的内容

告知用户以下内容都可以根据需要调整：

- **角色组合**：选择需要的角色，去掉不需要的
- **自定义角色**：如果标准角色不满足需求，可以定义新角色
- **任务阶段**：项目分几个阶段、每个阶段的目标
- **技术决策**：技术栈、框架选择、编码规范
- **审查严格度**：是否需要代码审查、安全审查

Team-lead = 主对话（你自己）。不要生成 team-lead 智能体。

如果用户是在改进**现有团队系统**而不是从零开始，需要明确判断变更属于：

- 仅限当前项目的文档变更，还是
- 需要写回 `CCteam-creator` 源模板的持久变更

判断标准：

- 项目特定的流程调整 → 更新项目文档
- 持久的团队协议变更（team-lead 职责、角色边界、入职 prompt、CLAUDE.md 模板、任务/发现/进度约定）→ 先更新 `CCteam-creator`

不要在模板变更写回之前就推荐重建活跃团队，除非已选定了阶段边界。

## 第 2 步：确认方案

在充分沟通后，使用 AskUserQuestion 让用户最终确认：

- **项目名称**：简短、ASCII、kebab-case（例如 `chatr`、`data-pipeline`）
- **简要描述**：1-2 句话
- **确认的角色列表**：哪些角色参与，各自负责什么
- **初步的阶段规划**：项目大致分几步走

只有用户确认后，才进入后续的创建步骤。

## 第 3 步：创建规划文件

参见 [references/templates.md](references/templates.md) 了解文件模板。

### 目录结构

```
.plans/<project>/
  task_plan.md                -- 主计划
  findings.md                 -- 团队级汇总
  progress.md                 -- 工作日志
  decisions.md                -- 架构决策记录

  <agent-name>/               -- 每个智能体一个目录
    task_plan.md              -- 智能体任务清单
    findings.md               -- 索引，链接到各任务专属发现
    progress.md               -- 智能体工作日志
    <prefix>-<task>/          -- 任务文件夹（每个分配的任务一个）
      task_plan.md / findings.md / progress.md
```

### 任务文件夹模式（所有角色通用）

所有角色在接到独立任务时都创建任务文件夹。根 `findings.md` 作为**索引**——链接到各任务专属的发现文件，而不是把所有内容塞进一个巨大的文档。

| 角色 | 文件夹前缀 | 示例 |
|------|-----------|------|
| backend-dev / frontend-dev | `task-` | `task-auth/`、`task-payments/` |
| researcher | `research-` | `research-tech-stack/`、`research-auth-options/` |
| e2e-tester | `test-` | `test-auth-flow/`、`test-checkout/` |
| reviewer | `review-` | `review-auth-module/`、`review-payments/` |
| cleaner | （使用根目录文件） | — |

完整多角色示例结构见 [references/templates.md](references/templates.md) § "任务文件夹模板"。

快速的零散笔记（Bug 修复、配置变更）可以直接写在根文件中，不需要任务文件夹。

## 第 3.5 步：生成项目 CLAUDE.md

项目工作目录下的 CLAUDE.md 会被 Claude Code **始终加载到主会话的上下文中**。这是让 team-lead 在上下文压缩后仍然保持团队运营知识的核心机制。

### 生成内容

在**项目工作目录**（不是 `.plans/` 里面）创建或追加 `CLAUDE.md` 文件。

参见 [references/templates.md](references/templates.md) 中的 CLAUDE.md 模板。模板必须根据第 2 步确认的实际角色**动态填充**：
- 只列出确认参与的角色
- 填入项目名称和目录路径
- 如有自定义角色也要包含

### 如果 CLAUDE.md 已存在

如果项目目录已有 CLAUDE.md，在末尾**追加**团队运营部分（用清晰的分隔线），不要覆盖已有内容。

### 为什么需要这个

没有这个文件，上下文压缩后 team-lead 会丢失：
- 有哪些智能体、分别叫什么名字
- 怎么下发任务、怎么检查状态
- 核心协议（3-Strike 处理、代码审查触发、阶段推进）

CLAUDE.md 通过把精简的运营手册永久保留在上下文中来解决这个问题。

### 何时更新 CLAUDE.md

CLAUDE.md 是一份**活文档**，不是一次性生成物。以下情况需要更新：
- 捕获到一个反复出现的失败模式（→ 追加到 `## Known Pitfalls`）
- 团队成员变动（新增/移除/重建智能体）
- 项目中期建立了新协议
- 架构决策影响了团队工作流

不要在这里放任务级细节——只放能穿越上下文压缩的持久化运营知识。

## 第 4 步：创建团队 + 生成智能体

1. `TeamCreate(team_name: "<project>")`
2. 通过 TaskCreate 创建任务——描述中包含一句话范围 + 验收标准 + `.plans/` 路径。通过 TaskUpdate 设置依赖（`addBlockedBy`）和负责人（`owner`）。优先 [AFK] 任务；注明输入/输出以减少智能体间信息损耗
3. 对每个角色并行生成，`run_in_background: true`

参见 [references/onboarding.md](references/onboarding.md) 了解每个角色的入职 prompt。

## 第 5 步：确认

向用户展示团队成员表和文件位置。

## 关键规则

- **双系统，不重复**：.plans/ 文件是数据源头（持久化、跟项目走）；原生 TaskCreate 是实时调度层（快速查询、依赖自动解锁，但仅会话级——存储在 `~/.claude/tasks/`，不在项目中）。TaskCreate 描述 = 一句话摘要 + `.plans/` 路径。在新会话中恢复项目时，从各智能体的 findings.md 索引重建任务
- **Team-lead 是控制平面**：主对话负责用户对齐、任务分解、阶段门禁、主计划维护和 CLAUDE.md 更新
- **上下文恢复**：智能体被压缩后，必须先读自己的 task_plan.md + findings.md + progress.md 才能继续工作
- **所有角色用任务文件夹**：每个分配的任务都有独立文件夹和三文件；根 findings.md 是索引
- **代码审查触发条件**：大项目/大功能/新建功能完成后调 reviewer；小修改/Bug 修复不需要
- **researcher 用 sonnet 模型**：调研需要一定深度
- **并行生成**：同时启动所有独立智能体
- **Peer Review**：dev 直接找 reviewer，不经 team-lead
- **代码是真理**：文档跟着代码走
- **模板优先处理持久流程变更**：如果发现的改进影响角色定义、入职 prompt、CLAUDE.md 结构或下发协议，先更新 `CCteam-creator` 源文件再建议重建
- **在阶段边界重建**：不要在开发中途重建活跃团队；优先先同步模板、再同步项目文档、然后在主要阶段之间重建
- **不要归档文件夹**：已完成的任务文件夹留在原地，在根 findings.md 索引中标记 `Status: complete` 即可。不要重命名、移动或加 `_archive_` 前缀——索引是导航层，文件夹位置必须稳定，否则交叉引用会断裂
- **默认中文回复**

## Team-Lead 运营指南

### planning-with-files 在团队中的应用

planning-with-files 的核心思想是：**文件系统 = 磁盘，上下文 = 内存，重要的东西必须写到磁盘上**。

团队项目中，这套思想在三个层面运作：

| 层面 | 谁负责 | 文件位置 | 关注什么 |
|------|--------|---------|---------|
| 项目全局 | team-lead | `.plans/<project>/task_plan.md` | 阶段进度、架构决策、任务分配 |
| 智能体级 | 各 agent 自己 | `.plans/<project>/<agent>/` | 自己的任务、发现、工作日志 |
| 大任务级 | dev agent | `.plans/<project>/<agent>/task-<name>/` | 单个大功能的详细步骤 |

每个 agent 的入职 prompt 已内置了等效的自检协议（定期自检 5 问、2-Action Rule、3-Strike），
team-lead 不需要手动触发这些机制，agent 会自主执行。

> **关于 `/planning-with-files:status`**：该命令读取项目根目录的单个 task_plan.md，
> 不感知团队的多层文件结构。如要查看主计划，直接 Read `.plans/<project>/task_plan.md`。

### 团队状态检查（team-lead 版自检）

team-lead 也应遵循"定期自检"原则。建议在以下时机主动检查：

**快速扫描**（并行读取各 agent 的 progress.md）：
```
Read .plans/<project>/backend-dev/progress.md
Read .plans/<project>/frontend-dev/progress.md
Read .plans/<project>/researcher/progress.md
...（按实际角色）
```

**深挖问题**（有疑问时读 findings.md）：
```
Read .plans/<project>/<agent-name>/findings.md
```

**决策对齐**（需要调整方向时读主计划）：
```
Read .plans/<project>/task_plan.md
```

读取顺序：**progress（到哪了）→ findings（遇到什么）→ task_plan（目标是什么）**

### Team-Lead 拥有控制平面

team-lead 的职责不只是派发任务：

- 与用户对齐需求和范围控制
- 将工作分解为任务，附带明确的输入、输出和验收标准
- 维护 `.plans/<project>/task_plan.md`、`decisions.md` 和项目 `CLAUDE.md`
- 决定阶段门禁：调研 → 开发 → 审查 → E2E → 清理
- 决定某个流程改进是项目本地的还是需要写回 `CCteam-creator` 的

如果这些职责不在主对话中保持，团队可能继续运转，但会逐渐偏离方向。

### 模板同步 vs 项目本地文档

当发现团队级改进时，team-lead 应分类：

- **项目本地**：只有当前项目需要 → 更新项目文档
- **模板级**：未来团队应继承 → 先更新 `CCteam-creator` 源文件

模板级变更的典型例子：

- team-lead 职责
- 角色边界
- 入职协议
- CLAUDE.md 结构
- 任务/发现/进度约定
- 重建时机规则

推荐操作顺序：

1. 更新 `CCteam-creator`
2. 同步当前项目的文档
3. 仅当变更实质影响已生成智能体的行为时才重建团队

### 重建时机

不要默认"改了模板就立刻重建"。

优先在以下时机重建：

- 主要阶段完成之后
- 下一轮主要开发周期开始之前
- 角色 prompt 变更足够大，继续使用现有智能体会导致不一致行为时

### 智能体 3-Strike 上报处理

当智能体报告"3次失败，上报 team-lead"时：
1. 读取其 progress.md 中的已尝试记录
2. 分析是否需要修改主计划（task_plan.md）
3. 给出明确的新方案方向，或重新分配任务给其他智能体
4. **护栏检查**：这个失败模式会复现吗？
   - 如果会（项目内）→ 追加到 CLAUDE.md `## Known Pitfalls`（症状、根因、修复、预防）
   - 如果会（跨项目通用）→ 同时记录 `[TEAM-PROTOCOL]` 并考虑模板级更新
   - 如果不会（一次性）→ 无需额外操作

### 阶段推进节奏

- 调研阶段完成 → 读 researcher findings.md → 更新主 task_plan.md 的架构决策章节
- 开发阶段完成 → 等 reviewer 审查结果 → 确认 [OK] 或 [WARN] 后推进下一阶段
- 全部完成 → 并行读各 agent progress.md，确认所有任务已 complete

**阶段边界健康检查**（快速，配合阶段推进一起做）：
- 各智能体的根 findings.md 索引是否完整？（有没有漏掉索引条目的孤立任务文件夹）
- TaskList 中是否有过期的 `in_progress` 任务应标完成或重新分配？
- 主 task_plan.md 的阶段状态是否与实际进度一致？
- 检查 CLAUDE.md Known Pitfalls——有没有需要在下一阶段任务下发时带上的？
- 执行 Harness 检查清单（见 CLAUDE.md 模板）
