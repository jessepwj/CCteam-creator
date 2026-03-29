# 规划文件模板

## 目录

- **项目 CLAUDE.md** — 团队运营手册（始终在上下文中），花名册、下发协议、状态检查、文档索引、核心协议
- **主 task_plan.md** — 精简导航图：概述、文档索引、阶段概览、任务汇总、当前阶段
- **主 findings.md** — 团队级发现日志（带标签条目）
- **主 progress.md** — 按时间顺序的工作日志
- **智能体根目录文件** — task_plan.md（智能体总览）、findings.md（索引）、progress.md（工作日志）
- **任务文件夹模板** — 各角色模板：dev（`task-`）、researcher（`research-`）、e2e-tester（`test-`）、reviewer（`review-`）
- **根目录 findings.md 索引模式** — 所有角色的索引示例
- **docs/ 模板** — 项目知识库：architecture.md、api-contracts.md、invariants.md
- **项目 decisions.md** — 架构决策记录

---

## 项目 CLAUDE.md（团队运营手册）

此文件生成在**项目工作目录**下（不是 `.plans/` 里面）。Claude Code 会始终将其加载到主会话上下文中，确保 team-lead 在上下文压缩后不会丢失团队运营知识。

**动态生成**：只包含第 2 步确认的角色。下面的示例展示了全部角色，实际使用时删掉未选的行。

```markdown
# <项目名> - 团队运营手册

> 由 team-project-setup 自动生成，可按需修改。
> 此文件让 team-lead 的团队知识在上下文压缩后仍然保持。

## Team-Lead 控制平面

- team-lead = 主对话，不是生成的 agent
- team-lead 负责用户对齐、范围控制、任务分解和阶段推进
- team-lead 维护项目全局真相：主 `task_plan.md`、`decisions.md` 和此 `CLAUDE.md`
- team-lead 决定某个流程改进是项目本地的还是需要写回 `CCteam-creator` 的
- **禁用独立子智能体**：团队存在后，所有工作通过 SendMessage 交给队友。不要启动独立的 Agent/子智能体（Explore、general-purpose 等）——它们绕过团队的规划文件和协作体系。唯一例外：用 `team_name` 生成新队友加入团队

## 团队花名册

| 名称 | 角色 | 模型 | 核心能力 |
|------|------|------|---------|
| backend-dev | 后端开发 | sonnet | 服务端代码 + TDD |
| frontend-dev | 前端开发 | sonnet | 客户端代码 + TDD |
| researcher | 探索/研究 | sonnet | 代码搜索 + 网页调研（只读）。可多实例：按量拆分（最常见）或按独立方向拆分——不用于串行依赖链 |
| e2e-tester | 联调测试 | sonnet | Playwright 测试 + 浏览器自动化 |
| reviewer | 代码审查 | sonnet | 安全/质量/性能审查（只读） |
| custodian | 管家 | sonnet | 约束合规 + 文档治理 + 模式→自动化 + 代码清理 |

## 任务下发协议

### TaskCreate 描述格式（team-lead 上下文压缩后参考）

TaskCreate 描述：一句话范围 + 验收标准 + `.plans/` 路径。
示例：`"JWT 认证模块。输入：researcher 调研在 .plans/x/researcher/research-auth/findings.md。输出：可用的认证 + 测试。详见 .plans/x/backend-dev/task-auth/task_plan.md"`
通过 TaskUpdate 分配负责人和设置依赖。Teammate 可自行通过 TaskList 认领已解锁的任务。

### 大任务（功能开发、新模块）-- 重要！

给任何智能体下发大任务时，消息中**必须包含**：
1. **范围和目标**：要做什么、验收标准
2. **文档提醒**："请创建 `<前缀>-<任务名>/` 任务文件夹（含 task_plan.md + findings.md + progress.md），并在你的根 findings.md 中添加索引条目"
3. **依赖说明**：依赖哪些调研/任务的结论，关键文件路径和行号
4. **审查预期**：完成后是否需要代码审查

示例：
```
SendMessage(to: "backend-dev", message:
  "新任务：实现认证模块。
   范围：JWT 登录 + refresh token + 认证中间件。
   依赖：researcher 的调研结论在 .plans/<project>/researcher/research-auth/findings.md
   请创建 task-auth/ 文件夹，并更新你的根 findings.md 索引。
   这是大功能——完成后请找 reviewer 审查。")
```

各角色的任务文件夹前缀：
- backend-dev / frontend-dev：`task-<名称>/`
- researcher：`research-<主题>/`
- e2e-tester：`test-<范围>/`
- reviewer：`review-<目标>/`

### 小任务（Bug 修复、配置变更）

直接发消息说明改动即可，不需要任务文件夹，也不需要审查。
```
SendMessage(to: "frontend-dev", message: "修复登录表单的 XSS 漏洞，见 src/auth/login.tsx:42")
```

## 通信速查

| 操作 | 命令 |
|------|------|
| 给单个智能体分配任务 | `SendMessage(to: "<名称>", message: "...")` |
| 广播给所有人（慎用） | `SendMessage(to: "*", message: "...")` |
| dev 请求代码审查 | dev 直接联系 reviewer（不经过 team-lead） |

## 状态检查

| 要检查什么 | 怎么做 |
|-----------|--------|
| 全局概览 | `TaskList` — 所有任务、负责人、阻塞情况一览 |
| 快速扫描 | 并行读取各 agent 的 `progress.md` |
| 深入了解 | 读 agent 的 `findings.md`（索引）→ 再看具体任务文件夹 |
| 方向检查 | 读 `.plans/<project>/task_plan.md` |
| 恢复项目 | 读各 agent 的 `findings.md` 索引 → 为未完成任务重建 TaskCreate |

读取顺序：**progress**（到哪了）→ **findings**（遇到什么）→ **task_plan**（目标是什么）

## 文档索引（知识库）

> **导航地图**：`docs/index.md` 有各文档的 section 级导航（含行号范围）。
> custodian 维护 docs/index.md。需要在 docs/ 中查找信息时先 Read 它。
> CLAUDE.md 不是热加载的——动态导航信息放在 docs/index.md 中，不在这里。

| 文档 | 位置 | 维护者 |
|------|------|--------|
| 导航地图 | .plans/<project>/docs/index.md | custodian（sections、行号、新鲜度） |
| 架构 | .plans/<project>/docs/architecture.md | team-lead, devs |
| API 契约 | .plans/<project>/docs/api-contracts.md | devs（API 变更时**必须**同步） |
| 不变量 | .plans/<project>/docs/invariants.md | team-lead, reviewer |

**Doc-Code Sync 规则**：当代码变更了 API 或架构时，对应的 docs/ 文件**必须**在同一个任务中同步更新。未文档化的 API 对其他智能体来说不存在。

## 自动化检查

> custodian 构建和维护检查脚本。列在这里让 team-lead 知道哪些已自动化。

| 检查 | 脚本 | 执行什么 |
|------|------|---------|
| 黄金原则 | scripts/golden_rules.py | 文件大小、密钥、console.log、文档新鲜度、不变量覆盖 |
| CI（测试 + 类型） | scripts/run_ci.py | 黄金原则 + 所有测试通过 + 类型检查 |
| （custodian 构建检查后在此添加） | | |

## Harness 检查清单

team-lead 在阶段边界检查（不是每个任务都查）：

- **文档 harness**：读 CLAUDE.md + 主 task_plan.md——还准确吗？如果过时 → 在下发下一阶段任务前更新
- **可观测性 harness**：Grep progress.md 搜索 "error|fail"——失败记录是否有足够细节（尝试步骤、具体错误、根因）？
- **不变量 harness**：检查下方 Known Pitfalls——是否有条目应提升为 reviewer 检查项或自动化测试断言？
- **回放 harness**：本阶段是否产生了可复用的模式（搜索策略、架构模板、测试方案）？如果有，用 [TEAM-PROTOCOL] 记录供未来参考

## Known Pitfalls

> 当识别到反复出现的失败模式时追加到这里。每个条目都是一次"防火"。
> 格式：症状、根因、修复方法、预防措施。

（初始为空——team-lead 从 3-Strike 解决方案、reviewer [BLOCK] 修复或任何重复失败中添加条目）

## 风格决策

> 项目中捕获的用户品味偏好。
> 当同一模式出现 3+ 次时，custodian 应将其编码到 golden_rules.py 中。
> 格式：决策内容、来源（用户反馈 / 审查 / 事故）、执行状态。

| # | 决策 | 来源 | 状态 |
|---|------|------|------|
| （示例）SD-1 | 变量名使用 camelCase，不用 snake_case | 用户反馈 Session 2 | Manual |

状态值：
- `Manual` — 仅文档记录，reviewer 按惯例检查
- `Pending automation` — 出现 3+ 次，等待 custodian 编码
- `Automated (GR-N)` — 已编码到 golden_rules.py，机械化强制

（删除示例行，在用户提供反馈时填充）

## 核心协议

| 协议 | 触发时机 | 操作 |
|------|---------|------|
| 需求对齐 | 团队搭建后、开发前 | researcher 探索代码库（T0a），再由 team-lead 与用户对齐（T0b）。更新 task_plan.md §1-§2 |
| 计划压力测试 | 架构定稿前 | 委托 researcher："压力测试此计划，走查每个决策分支"。从 findings.md 读取结论 |
| 3-Strike 上报 | 智能体报告 3 次失败 | 读其 progress.md，给新方向或重新分配 |
| 代码审查 | 大功能/新模块完成 | dev 在 findings.md 写改动摘要，发给 reviewer |
| 阶段推进 | 阶段完成 | 调研完：读 findings 更新主计划。开发完：等 reviewer [OK]/[WARN] |
| 上下文溢出 | 智能体报告上下文过长 | 进度已存文件，恢复或生成后继者 |
| CI 门禁 | 任何代码变更（dev 完成任务时） | 运行 CI 脚本，所有检查 PASS 后才能提交审查。CI 失败 = 任务未完成 |
| 护栏捕获 | 3-Strike 上报解决后，或 reviewer [BLOCK] 修复后 | 问：会复现吗？如果会 → 追加到 Known Pitfalls；如果通用 → [TEAM-PROTOCOL] |
| custodian 巡检 | 2-3 个 dev 任务完成后，或阶段边界时 | team-lead 触发 custodian 合规巡检；custodian 报告缺口 |
| 模式→自动化 | reviewer 标记 [AUTOMATE] 时 | team-lead 转给 custodian → 构建检查脚本 → 加入 CI |
| 品味捕获 | 用户对代码风格/命名/结构表达偏好时 | 记录到 CLAUDE.md 风格决策。3+ 次同类 → 标记 `Pending automation`，派 custodian 编码到 golden_rules.py |
| 风格→自动化 | 风格决策达到 `Pending automation` | custodian 编码检查到 golden_rules.py，更新状态为 `Automated (GR-N)`。不可机械化的 → 保持 Manual 并注明原因 |
| 模板同步 | 发现持久流程改进 | 先更新 `CCteam-creator` 源文件，再同步项目文档 |
| 团队重建时机 | 模板变更足以影响已生成智能体行为 | 优先在阶段边界重建，不要在开发中途 |

### 任务下发：最小化信息损耗

智能体间的消息会丢失细节。每次任务下发必须自包含：
- 引用 findings/文档的文件路径（让智能体读文件，而不是读你的摘要）
- 消息中包含验收标准（让智能体知道何时算完成）
- 标注 [AFK] 或 [HITL]，让智能体知道是否可以自主推进

### 模板级 vs 项目本地变更

按以下标准区分：

- **项目本地**：只有当前项目的文档或流程需要变更
- **模板级**：未来团队应继承该变更，需先更新 `CCteam-creator`

典型的模板级变更：

- team-lead 职责
- 角色边界
- 入职协议
- CLAUDE.md 结构
- 任务/发现/进度约定
- 重建时机规则

## 文件结构

```
.plans/<project>/
  task_plan.md          -- 主计划：精简导航图（team-lead 维护）
  findings.md           -- 团队级发现
  progress.md           -- 工作日志
  decisions.md          -- 架构决策记录
  docs/                 -- 项目知识库（架构、API 等的真理源头）
    index.md            -- 导航地图：sections 和行号范围（custodian 维护）
    architecture.md     -- 系统架构、组件、数据流
    api-contracts.md    -- 前后端 API 定义、字段规范、状态机
    invariants.md       -- 系统不变量（不可违反的边界）
  archive/              -- 归档历史（不删除，但不需要每天读取）
  <agent-name>/         -- 各智能体目录
    task_plan.md        -- 智能体任务清单
    findings.md         -- 索引：链接到各任务文件夹（保持精简，不堆内容）
    progress.md         -- 智能体工作日志（条目过多时归档旧内容）
    <前缀>-<任务>/      -- 任务文件夹（每个分配的任务一个）
      task_plan.md / findings.md / progress.md
```
```

---

## 主 task_plan.md

```markdown
# <项目名> - 主计划

> 状态: PLANNING
> 创建: <日期>
> 更新: <日期>
> 团队: <team-name> (<角色列表>)
> 决策记录: .plans/<project>/decisions.md

---

## 1. 项目概述

<1-2 句话描述项目做什么>
详细产品定义 → [docs/product.md](docs/product.md)（如已创建）

---

## 2. 文档索引

| 文档 | 位置 | 内容 |
|------|------|------|
| 架构 | docs/architecture.md | 系统组件、数据流、关键设计决策 |
| API 契约 | docs/api-contracts.md | 前后端接口定义 |
| 不变量 | docs/invariants.md | 不可违反的系统边界 |

---

## 3. 阶段概览

任务调度通过原生 TaskCreate/TaskList 管理（依赖自动解锁）。

### 切片原则

将任务分解为**垂直切片**（追踪子弹），而不是按技术层横向切片。
每个切片提供一条贯穿所有层的窄而完整的路径（schema → API → UI → 测试）。

### 阶段

- 阶段 0: 需求对齐 — researcher 探索代码库，team-lead 与用户对齐需求
- 阶段 1: 调研 — 深入技术问题和架构选型
- 阶段 2: 核心开发 — 垂直切片实现 + TDD
- 阶段 3: 联调测试 — E2E 测试关键用户流程
- 阶段 4: 审查与清理 — 代码审查裁决 + 死代码清理

---

## 4. 任务汇总

| # | 任务 | 负责人 | 状态 | 计划文件 |
|---|------|--------|------|----------|
| T1 | ... | ... | ... | .plans/<project>/<agent>/... |

---

## 5. 当前阶段

<当前正在做什么，下一个里程碑是什么>
```

**精简导航图原则**：task_plan.md 是一张**导航图**，不是百科全书。架构、API 规范、技术栈细节和目录结构属于 `docs/` 文件。保持此文件专注于"去哪找"和"下一步做什么"。

## 主 findings.md

```markdown
# <项目名> - 发现与技术记录

> 由团队智能体自动更新。每条标注来源。

---

<工作中添加条目，格式如下:>

## [标签] <日期> — <标题>

### 来源: <agent-name>

<内容>

---

标签说明:
- [RESEARCH] 调研发现
- [BUG] 缺陷记录
- [CODE-REVIEW] 代码审查结果
- [REVIEW-FIX] 审查问题修复
- [SECURITY-REVIEW] 安全审查
- [ARCHITECTURE] 架构分析
- [E2E-TEST] 端到端测试结果
- [INTEGRATION] 集成问题
```

## 主 progress.md

```markdown
# <项目名> - 进度日志

> 按时间线记录。每条记录谁做了什么。

---

## <日期> Session N — <标题>

### 已完成
- [x] <条目>

### 待办
- [ ] <条目>

### 关键决策
- <决策及理由>
```

---

## 智能体根目录 task_plan.md

```markdown
# <智能体名> - 任务计划

> 角色: <角色描述>
> 状态: pending
> 分配的任务: <列表>

## 任务

- [ ] 步骤 1: <描述>
- [ ] 步骤 2: <描述>
- [ ] 步骤 3: <描述>

## 备注

<智能体相关的上下文、约束、参考>
```

## 智能体根目录 findings.md

```markdown
# <智能体名> - 发现记录

> 工作中发现的问题和技术要点。

---

<初始为空，工作中填写>
```

## 智能体根目录 progress.md

```markdown
# <智能体名> - 工作日志

> 用于上下文恢复。压缩/重启后先读此文件。

---

<初始为空，工作中填写>
```

---

## 任务文件夹模板

所有角色在接到独立任务时都会使用任务文件夹。文件夹前缀因角色而异：

| 角色 | 前缀 | 示例 |
|------|------|------|
| backend-dev / frontend-dev | `task-` | `task-auth/`、`task-payments/` |
| researcher | `research-` | `research-tech-stack/`、`research-auth-options/` |
| e2e-tester | `test-` | `test-auth-flow/`、`test-checkout/` |
| reviewer | `review-` | `review-auth-module/`、`review-payments/` |
| custodian | `audit-` | `audit-phase1-compliance/`、`audit-doc-health/` |

---

### Dev 任务文件夹（backend-dev / frontend-dev）

```
.plans/<project>/<agent-name>/task-<feature-name>/
```

#### task_plan.md

```markdown
# <功能名> - 任务计划

> 所属智能体: <agent-name>
> 状态: in_progress
> 创建: <日期>

## 目标

<此功能要实现什么>

## 详细步骤

- [ ] 1. <步骤描述>
- [ ] 2. <步骤描述>
- [ ] 3. <步骤描述>
- [ ] 4. 编写测试（TDD）
- [ ] 5. 验证覆盖率 >= 80%
- [ ] 6. 请求 reviewer 审查（大功能必须）

## 涉及文件

- `path/to/file1.ts` — <说明>
- `path/to/file2.ts` — <说明>

## 依赖

- 依赖 T1 调研结论（见 researcher/research-<topic>/findings.md）
- 依赖 xxx API 设计（见主 task_plan.md §6）
```

#### findings.md

```markdown
# <功能名> - 发现记录

> 此任务开发中的技术发现。

---

<初始为空>
```

#### progress.md

```markdown
# <功能名> - 工作日志

> 上下文恢复时只需读此文件（不用读其他 task 文件夹）。

---

<初始为空>
```

---

### 调研文件夹（researcher）

```
.plans/<project>/researcher/research-<topic>/
```

#### task_plan.md

```markdown
# 调研: <主题> - 计划

> 智能体: researcher
> 状态: in_progress
> 创建: <日期>

## 调研问题

1. <需要回答什么？>
2. <有哪些备选方案？>
3. <各方案的权衡是什么？>

## 方法

- [ ] 1. <搜索/读取策略>
- [ ] 2. <网页调研目标>
- [ ] 3. <源码分析范围>
- [ ] 4. 将结论整理到 findings.md
- [ ] 5. 更新根索引

## 范围

<此次调研的范围内/范围外>
```

#### findings.md（核心交付物）

```markdown
# 调研: <主题> - 报告

> 这是调研的核心交付物。其他人读此文件获取结论。
> 智能体: researcher
> 状态: in_progress
> 创建: <日期>

---

## 摘要

<执行摘要——调研完成后填写>

## 详细发现

<随调研进展按 2-Action Rule 添加发现>

### [RESEARCH] <日期> — <发现标题>

<内容，含确切文件路径、行号和证据>

---

## 结论与建议

<调研完成后填写>
```

#### progress.md

```markdown
# 调研: <主题> - 搜索日志

> 记录搜索了什么、找到了什么。用于上下文恢复和避免重复搜索。

---

<初始为空>
```

---

### 测试文件夹（e2e-tester）

```
.plans/<project>/e2e-tester/test-<scope>/
```

#### task_plan.md

```markdown
# 测试: <范围> - 计划

> 智能体: e2e-tester
> 状态: in_progress
> 创建: <日期>

## 测试范围

<要测试哪些用户流程/功能>

## 测试用例

- [ ] TC1: <描述> — 优先级: CRITICAL
- [ ] TC2: <描述> — 优先级: HIGH
- [ ] TC3: <描述> — 优先级: MEDIUM

## 前提条件

- <测试执行前必须部署/运行什么>
```

#### findings.md

```markdown
# 测试: <范围> - 结果

> 此范围的测试结果和 Bug 报告。
> 智能体: e2e-tester
> 状态: in_progress

---

## 摘要

| 指标 | 数值 |
|------|------|
| 总测试数 | — |
| 通过 | — |
| 失败 | — |
| 通过率 | — |

## 结果

<随测试执行添加结果>

### [E2E-TEST] <日期> — <测试名称>

- 状态: PASS | FAIL
- 耗时: <时间>
- 详情: <备注>

### [BUG] <日期> — <Bug 标题>

- File: <路径:行号>
- 严重度: CRITICAL | HIGH | MEDIUM | LOW
- 根因: <分析>
- 修复建议: <建议>
```

#### progress.md

```markdown
# 测试: <范围> - 执行日志

> 用于上下文恢复。

---

<初始为空>
```

---

### 审查文件夹（reviewer）

```
.plans/<project>/reviewer/review-<target>/
```

#### findings.md

```markdown
# 审查: <目标> - 报告

> 代码审查结果。
> 智能体: reviewer
> 请求方: <dev-agent-name>
> 状态: in_progress
> 创建: <日期>

---

## 裁决: [OK] | [WARN] | [BLOCK]

## 问题

<添加审查中发现的问题>

### [CRITICAL] <标题>

- File: <路径:行号>
- 问题: <描述>
- 修复: <含代码示例的建议>

### [HIGH] <标题>

- File: <路径:行号>
- 问题: <描述>
- 修复: <建议>

## 汇总

- CRITICAL: 0
- HIGH: 0
- MEDIUM: 0
- LOW: 0
```

#### progress.md

```markdown
# 审查: <目标> - 笔记

> 审查过程笔记。

---

<初始为空>
```

---

### 审计文件夹（custodian）

```
.plans/<project>/custodian/audit-<scope>/
```

#### findings.md

```markdown
# 审计: <范围> - 报告

> 合规审计结果。
> 智能体: custodian
> 范围: <审了什么>
> 日期: <日期>

---

## 汇总

- CRITICAL: 0
- ADVISORY: 0

## Doc-Code Sync

<代码变更与 docs/ 之间发现的缺口>

## 索引完整性

<缺失的 findings.md 索引条目、孤立的任务文件夹>

## docs/index.md 更新

<已做的导航地图变更>

## 建议

<建议 team-lead 下发的操作>
```

#### progress.md

```markdown
# 审计: <范围> - 执行日志

> 审计过程笔记。

---

<初始为空>
```

---

### 根目录 findings.md 作为索引（所有角色）

每个智能体的根 findings.md 都应作为索引。示例：

```markdown
# <智能体名> - 发现索引

> 纯索引——每个条目应简短（Status + Report 链接 + Summary）。
> 如果此文件越来越长，说明内容在往里泄漏——应拆分到任务文件夹中。

---

## task-auth
- Status: complete
- Report: [findings.md](task-auth/findings.md)
- Summary: 认证模块已实现，使用 JWT + refresh token

## task-payments
- Status: in_progress
- Report: [findings.md](task-payments/findings.md)
- Summary: 与 Stripe 的支付集成

---

## 零散笔记

> 保持最少。任何比简短观察更长的内容 → 创建任务文件夹。
```

---

## docs/ 模板

`docs/` 目录是项目的**知识库**——结构化的参考文档，智能体读取它们来恢复上下文。不同于 task_plan.md（导航）或 findings.md（事件日志），docs/ 文件包含**稳定的、经过整理的知识**，随项目演进主动维护。

在第 3 步创建。根据项目需要选择相关文件，不是所有文件都必须创建。

### docs/index.md（导航地图）

```markdown
# <项目名> - 知识库索引

> 动态导航地图。custodian 维护此文件。
> 智能体：需要在 docs/ 中查找信息时先 Read 此文件。
> CLAUDE.md 指向这里但不复制此内容。

| 文档 | 关键 Sections | 最后更新 |
|------|-------------|---------|
| architecture.md | §系统概览 (L1-30): 组件图 · §数据流 (L32-78): 请求链路 · §技术栈 (L80-95): 框架 | <日期> |
| api-contracts.md | §Auth API (L1-45): login/refresh/logout · §Chat API (L47-120): session CRUD | <日期> |
| invariants.md | §安全 (L1-20): session 隔离 · §数据 (L22-35): 边界 · §契约 (L37-50): 字段匹配 | <日期> |

## 如何使用此索引

- 需要了解系统组件？→ 读 architecture.md §系统概览
- 需要 API 字段名？→ 读 api-contracts.md，跳到相关 section
- 需要检查变更是否违反边界？→ 读 invariants.md

## 新鲜度日志

> custodian 每次审计后更新。

| 文档 | 上次审计 | 状态 |
|------|---------|------|
| architecture.md | <日期> | [OK] |
| api-contracts.md | <日期> | [OK] |
| invariants.md | <日期> | [OK] |
```

### docs/architecture.md

```markdown
# <项目名> - 架构

> 系统架构和关键设计决策。
> 维护者：team-lead, devs（架构变更后更新）

## 系统概览

<高层描述：有哪些组件，它们如何交互>

## 组件图

<关键组件/模块及其职责>

## 数据流

<关键操作中数据如何流转>

## 技术栈

<技术、框架、版本>

## 目录结构

<项目文件布局>
```

### docs/api-contracts.md

```markdown
# <项目名> - API 契约

> 前后端接口定义。字段名和类型的真理源头。
> 维护者：devs（添加/变更端点时**必须**更新）

## 端点

### POST /api/example

Request:
\`\`\`json
{ "field": "type — description" }
\`\`\`

Response:
\`\`\`json
{ "field": "type — description" }
\`\`\`

---

<随设计/实现逐步添加端点>
```

### docs/invariants.md

```markdown
# <项目名> - 系统不变量

> 不可违反的系统边界。违反其中任何一条 = CRITICAL Bug。
> 每条不变量应注明：能否自动化？当前状态（已有测试 / 无测试 / 人工检查）

## 安全边界

- INV-1: <描述> — 状态：无测试
- INV-2: <描述> — 状态：已有测试

## 数据隔离

- INV-N: <描述> — 状态：无测试

## 接口契约

- INV-M: 前后端 API 字段名必须与 api-contracts.md 一致 — 状态：人工检查

---

当识别到反复出现的 Bug 模式（通过 reviewer 或 Known Pitfalls），考虑将其添加为正式不变量。目标：reviewer 成为**第二道**防线；自动化测试是**第一道**。
```

---

## 项目 decisions.md

```markdown
# <项目名> - 架构决策记录

> 记录每个决策及其理由。位于 .plans/<project>/decisions.md。

---

<在规划和开发过程中添加决策>

## D1: <决策标题>

- 日期: <日期>
- 决策: <决定了什么>
- 理由: <为什么>
- 考虑过的替代方案: <还评估了什么>
```

