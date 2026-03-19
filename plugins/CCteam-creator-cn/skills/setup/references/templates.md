# 规划文件模板

## 项目 CLAUDE.md（团队运营手册）

此文件生成在**项目工作目录**下（不是 `.plans/` 里面）。Claude Code 会始终将其加载到主会话上下文中，确保 team-lead 在上下文压缩后不会丢失团队运营知识。

**动态生成**：只包含第 2 步确认的角色。下面的示例展示了全部角色，实际使用时删掉未选的行。

```markdown
# <项目名> - 团队运营手册

> 由 team-project-setup 自动生成，可按需修改。
> 此文件让 team-lead 的团队知识在上下文压缩后仍然保持。

## 团队花名册

| 名称 | 角色 | 模型 | 核心能力 |
|------|------|------|---------|
| backend-dev | 后端开发 | opus | 服务端代码 + TDD |
| frontend-dev | 前端开发 | opus | 客户端代码 + TDD |
| researcher | 探索/研究 | sonnet | 代码搜索 + 网页调研（只读） |
| e2e-tester | 联调测试 | sonnet | Playwright 测试 + 浏览器自动化 |
| reviewer | 代码审查 | opus | 安全/质量/性能审查（只读） |
| cleaner | 代码清理 | sonnet | 死代码清理 + 重构 |

## 任务下发协议

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
| 快速扫描 | 并行读取各 agent 的 `progress.md` |
| 深入了解 | 读 agent 的 `findings.md`（索引）→ 再看具体任务文件夹 |
| 方向检查 | 读 `.plans/<project>/task_plan.md` |

读取顺序：**progress**（到哪了）→ **findings**（遇到什么）→ **task_plan**（目标是什么）

## 核心协议

| 协议 | 触发时机 | 操作 |
|------|---------|------|
| 3-Strike 上报 | 智能体报告 3 次失败 | 读其 progress.md，给新方向或重新分配 |
| 代码审查 | 大功能/新模块完成 | dev 在 findings.md 写改动摘要，发给 reviewer |
| 阶段推进 | 阶段完成 | 调研完：读 findings 更新主计划。开发完：等 reviewer [OK]/[WARN] |
| 上下文溢出 | 智能体报告上下文过长 | 进度已存文件，恢复或生成后继者 |

## 文件结构

```
.plans/<project>/
  task_plan.md          -- 主计划（team-lead 维护）
  findings.md           -- 团队级发现
  progress.md           -- 工作日志
  <agent-name>/         -- 各智能体目录
    task_plan.md        -- 智能体任务清单
    findings.md         -- 索引：链接到各任务文件夹
    progress.md         -- 智能体工作日志
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
> 决策记录: memory/<project>-decisions.md

---

## 1. 项目概述

<1-2 段项目描述>

---

## 2. 关键架构决策

<规划阶段填写，记录每个决策及理由>

---

## 3. 技术栈

<技术、框架、版本列表>

---

## 4. 目录结构

<项目文件布局>

---

## 5. 任务分解

### 阶段 1: 调研
- [ ] T1: <描述> — 分配给: researcher

### 阶段 2: 核心开发
- [ ] T2: <描述> — 分配给: backend-dev
- [ ] T3: <描述> — 分配给: frontend-dev

### 阶段 3: 联调测试
- [ ] T4: <描述> — 分配给: e2e-tester

### 阶段 4: 审查清理
- [ ] T5: 代码审查 — 分配给: reviewer
- [ ] T6: 死代码清理 — 分配给: cleaner

---

## 6. API 文档

<随着 API 设计/发现逐步填写>
```

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

## 大任务 task 文件夹模板（仅 backend-dev / frontend-dev 使用）

当前后端开发智能体接到大功能/新模块时，在自己目录下创建：

```
.plans/<project>/<agent-name>/task-<功能名>/
```

### task 文件夹 task_plan.md

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

- 依赖 T1 调研结论（见 researcher findings.md）
- 依赖 xxx API 设计（见主 task_plan.md §6）
```

### task 文件夹 findings.md

```markdown
# <功能名> - 发现记录

> 此任务开发中的技术发现。

---

<初始为空>
```

### task 文件夹 progress.md

```markdown
# <功能名> - 工作日志

> 上下文恢复时只需读此文件（不用读其他 task 文件夹）。

---

<初始为空>
```
