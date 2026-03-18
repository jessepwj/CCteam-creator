---
name: team-project-setup
description: >
  Set up a complete agent team with file-based planning for complex multi-agent projects.
  Use when: (1) user asks to start a new complex project with a team/swarm, (2) user says
  "set up team", "create team", "build a team for X", "start project X", (3) user invokes
  /team-project-setup with a project name, (4) user wants to organize a multi-phase project
  with parallel agent workers and persistent progress tracking. Creates TeamCreate, planning
  files (.plans/project/), memory files, per-agent work directories, and spawns configured
  teammates. TRIGGER on: "team", "swarm", "start project", "set up project", "create team
  for", "build team", "organize project", "multi-agent project".
---

# 团队项目设置

为复杂项目设置多智能体团队，使用持久化文件进行规划和进度追踪。

## 流程

1. **需求咨询** — 向用户介绍团队机制、了解需求
2. **确认方案** — 汇总需求，让用户确认团队配置
3. 创建规划文件（含智能体子目录）
4. 创建记忆文件
5. 创建团队 + 生成智能体
6. 确认设置

## 第 1 步：需求咨询（先沟通，后动手）

**这一步的目标**：让用户充分理解团队是怎么运作的，同时收集用户的真实需求。不要急于创建任何文件或团队。

### 1.1 向用户介绍团队机制

用自然对话的方式（不要照搬下面的原文，根据上下文灵活表达），向用户解释以下要点：

**团队是什么**：
- 你（Claude）作为 team-lead，会同时指挥多个 AI 智能体并行工作
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
  findings.md                 -- 发现、Bug、审查结果
  progress.md                 -- 工作日志

  <agent-name>/               -- 每个智能体一个目录
    task_plan.md              -- 智能体任务清单
    findings.md               -- 智能体发现记录
    progress.md               -- 智能体工作日志
```

### 前后端开发智能体的特殊结构

前后端开发智能体（backend-dev、frontend-dev）在接收大任务/大功能时，
应在自己目录下为每个大任务创建独立的 task 文件夹：

```
.plans/<project>/backend-dev/
  task_plan.md                -- 智能体总览（列出所有 task）
  findings.md                 -- 通用发现
  progress.md                 -- 通用进度

  task-auth/                  -- 大任务：认证模块
    task_plan.md              -- 此任务的详细步骤
    findings.md               -- 此任务的发现
    progress.md               -- 此任务的进度
  task-file-upload/           -- 大任务：文件上传
    task_plan.md
    findings.md
    progress.md
```

其他智能体（researcher、e2e-tester、reviewer、cleaner）任务通常不大，
不需要按 task 分文件夹，直接用智能体根目录的三个文件即可。

## 第 4 步：创建记忆文件

在项目记忆目录中：

1. 创建 `memory/<project>-decisions.md`，仅包含标题
2. 将项目条目追加到 `memory/MEMORY.md`：
   ```
   ## Project: <Name>
   - Status: PLANNING
   - Plans: .plans/<project>/
   - Decisions: [<project>-decisions.md](<project>-decisions.md)
   ```

## 第 5 步：创建团队 + 生成智能体

1. `TeamCreate(team_name: "<project>")`
2. 对每个角色并行生成，`run_in_background: true`

参见 [references/onboarding.md](references/onboarding.md) 了解每个角色的入职 prompt。

## 第 6 步：确认

向用户展示团队成员表和文件位置。

## 关键规则

- **规划文件就是进度追踪器** -- 不要同时用 TaskCreate/TodoWrite
- **上下文恢复**：智能体被压缩后，必须先读自己的 task_plan.md + findings.md + progress.md 才能继续工作
- **前后端大任务分 task 文件夹**：每个大功能/新功能独立一组三文件
- **代码审查触发条件**：大项目/大功能/新建功能完成后调 reviewer；小修改/Bug 修复不需要
- **researcher 用 sonnet 模型**：调研需要一定深度
- **并行生成**：同时启动所有独立智能体
- **Peer Review**：dev 直接找 reviewer，不经 team-lead
- **代码是真理**：文档跟着代码走
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

### 智能体 3-Strike 上报处理

当智能体报告"3次失败，上报 team-lead"时：
1. 读取其 progress.md 中的已尝试记录
2. 分析是否需要修改主计划（task_plan.md）
3. 给出明确的新方案方向，或重新分配任务给其他智能体

### 阶段推进节奏

- 调研阶段完成 → 读 researcher findings.md → 更新主 task_plan.md 的架构决策章节
- 开发阶段完成 → 等 reviewer 审查结果 → 确认 [OK] 或 [WARN] 后推进下一阶段
- 全部完成 → 并行读各 agent progress.md，确认所有任务已 complete
