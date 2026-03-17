# 规划文件模板

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
