# CCteam-creator

> [Claude Code](https://code.claude.com/) 多智能体团队编排技能。

[English](./README.md) | [中文](./README_CN.md)

## 站在巨人的肩膀上

CCteam-creator 基于以下优秀的开源项目和工程实践构建：

| 来源 | 我们学到的 |
|------|-----------|
| [**planning-with-files**](https://github.com/OthmanAdi/planning-with-files) | Manus 风格的持久化 Markdown 规划 — 三文件模式（task_plan.md / findings.md / progress.md），经得起上下文压缩。"上下文窗口 = 内存，文件系统 = 磁盘"的核心理念。 |
| [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | Anthropic 黑客松获奖者的智能体优化体系。13 个专家智能体，40+ 技能。启发了我们的角色化智能体设计和技能结构。 |
| [**mattpocock/skills**](https://github.com/mattpocock/skills) | TDD 垂直切片哲学、"设计两次"并行子智能体模式、接口耐久性原则、以及方案压测方法论。 |
| [**OpenAI Harness Engineering**](https://openai.com/index/harness-engineering/) | 设计约束、反馈循环和文档系统以使 AI 智能体在规模化下可靠运行的工程学科。启发了我们的 docs/ 知识库、不变量驱动审查、Doc-Code 同步、失败→护栏闭环、以及反膨胀原则。 |

---

## 功能概述

CCteam-creator 在 Claude Code 中设置并行 AI 智能体团队。不再是单个 AI 助手，而是多个专业智能体 —— 开发、研究、测试、审查 —— 协同工作。

调用后，CCteam-creator 会：

1. **先沟通** — 介绍团队机制，了解项目需求，推荐团队配置
2. **完成搭建** — 创建规划文件、docs/ 知识库、CLAUDE.md 运营手册、智能体入职
3. **管理协作** — 智能体直接沟通，状态持久化到文件，遵循内置协议

## 实战演示

以下截图来自真实项目会话（ChatR —— 全栈聊天应用，带事件驱动可观测性）。

### 1. 团队花名册 & 依赖链

搭建完成后，team-lead 汇总团队成员、任务分配和依赖图。所有智能体接收入职信息并开始准备。

![团队花名册](docs/images/01-team-roster.png)

### 2. 并行任务调度

Team-lead 同时编排 6 个智能体 —— researcher 和 cleaner 立即启动（无依赖），dev 们准备就绪等待研究产出。每个智能体清楚自己的依赖关系。

![并行调度](docs/images/02-parallel-dispatch.png)

### 3. 开发阶段 — 3 个智能体并行工作

Backend-dev、frontend-dev 和 e2e-tester 同时工作。Team-lead 跟踪状态、做调度决策（如跳过依赖阻塞）、协调交接。

![开发阶段](docs/images/03-development-phase.png)

### 4. 代码审查 & 对等协作

智能体间直接通信 —— frontend-dev 提交审查给 reviewer，reviewer 报告完成，team-lead 通过状态表实时追踪全部 6 个智能体的进展。

![审查协作](docs/images/04-review-coordination.png)

### 5. 阶段 Harness 验收

Team-lead 运行阶段级 harness 检查 —— 验证每个任务的完成状态、reviewer 裁定、e2e 测试结果和文档一致性，确认后才推进到下一阶段。

![Harness 验收](docs/images/05-harness-validation.png)

### 6. 最终面板 — 全员一览

完整验收清单，含 reviewer [OK]、e2e-tester PASS/FAIL 状态、文档一致性验证。底部展示 Claude Code 的实时智能体 HUD，显示全部 6 个队友及 token 用量。

![最终面板](docs/images/06-final-dashboard.png)

---

## 前置条件

智能体团队是 Claude Code 的实验性功能，需要先启用：

```bash
# 方式 A：环境变量
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 方式 B：在 ~/.claude/settings.json 中
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## 安装

> **重要**：英文版和中文版只需安装一个，不要同时安装。

### 方式 1：Marketplace 安装（推荐）

```bash
# 第 1 步：添加 marketplace（在 Claude Code 中运行）
/plugin marketplace add jessepwj/CCteam-creator

# 第 2 步：安装 — 选择一个语言
/plugin install CCteam-creator@ccteam        # 英文
/plugin install CCteam-creator-cn@ccteam     # 中文
```

### 方式 2：手动安装

```bash
git clone https://github.com/jessepwj/CCteam-creator.git

# 英文
cp -r CCteam-creator/skills/CCteam-creator ~/.claude/skills/CCteam-creator

# 或中文
cp -r CCteam-creator/cn/skills/CCteam-creator ~/.claude/skills/CCteam-creator
```

### 方式 3：项目级安装

```bash
# 通过项目目录与团队共享
cp -r CCteam-creator/cn/skills/CCteam-creator .claude/skills/CCteam-creator
```

## 使用方法

```
> 帮我的电商项目搭建一个团队
> /CCteam-creator-cn:setup
> 我要做一个 REST API，帮我建个团队
```

> 手动安装时，命令是 `/CCteam-creator` 而不是 `/CCteam-creator-cn:setup`。

**触发关键词**：`团队`、`team`、`swarm`、`开始项目`、`创建团队`、`搭建团队`、`多智能体项目`。

## 可用角色

| 角色 | 名称 | 模型 | 核心能力 |
|------|------|------|---------|
| 后端开发 | `backend-dev` | opus | 服务端代码 + TDD + Doc-Code 同步 + 可观测性（适用时） |
| 前端开发 | `frontend-dev` | opus | 客户端代码 + TDD + Doc-Code 同步 + 组件测试 |
| 探索/研究 | `researcher` | sonnet | 代码搜索 + 网页调研 + 方案压测（只读） |
| 联调测试 | `e2e-tester` | sonnet | Playwright E2E + 事件优先调试 + Bug 追踪 |
| 代码审查 | `reviewer` | opus | 安全/质量/性能 + 文档一致性 + 不变量驱动审查 |
| 代码清理 | `cleaner` | sonnet | 死代码清理 + 文档新鲜度扫描 + 安全重构 |

不是每个项目都需要全部角色。CCteam-creator 会根据你的需求推荐合适的组合。

## 核心特性

### Team-Lead 作为控制平面

主对话作为 team-lead——不只是任务派发器，而是**控制平面**，负责用户对齐、阶段门禁和团队持久化运营规则。Team-lead 维护项目 CLAUDE.md（始终在上下文中）、task_plan.md 和 decisions.md。

### docs/ 知识库（Harness Engineering）

受 OpenAI Harness Engineering 方法启发，每个项目都有结构化的 `docs/` 目录作为知识的唯一真理源：

```
.plans/<project>/docs/
  architecture.md     -- 系统架构、组件、数据流
  api-contracts.md    -- 前后端 API 定义（字段级规范）
  invariants.md       -- 不可违反的系统边界（安全、数据隔离、接口契约）
```

**Doc-Code 同步**：代码变更 API 或架构时，dev 必须同步更新对应的 docs/ 文件。Reviewer 每次审查都检查这一点。未文档化的 API 对其他智能体来说不存在。

### 精简导航图

task_plan.md 是一张**导航图**，不是百科全书。架构、API 规范和技术栈细节放在 `docs/` 中。主计划保持聚焦可读，即使大项目也不会膨胀。

### 不变量驱动审查

反复出现的 Bug 模式从 Known Pitfalls 提升为 `docs/invariants.md` 中的正式不变量。Reviewer 对照不变量检查代码，并建议将重复模式转为自动化测试。目标：自动化测试是第一道防线，reviewer 是第二道。

### 失败→护栏闭环

当 3-Strike 上报解决或 reviewer [BLOCK] 修复后，team-lead 会问："会再发生吗？"如果会，就记入 CLAUDE.md 的 Known Pitfalls——确保同样的错误不再发生。这是 Harness Engineering 的核心洞察：每次失败都变成永久性护栏。

### 反膨胀原则

源自文件膨胀到 50,000+ token 的实战教训：
- **根 findings.md** 是纯索引——不堆内容
- **progress.md** 太长时归档旧条目
- **task_plan.md** 保持精简——细节属于 docs/

### 需求对齐（阶段 0）

开发前，团队先进行结构化需求对齐：
- **Researcher** 探索现有代码库，记录架构现状
- **Team-lead** 与用户深入对齐需求细节
- 架构决策和范围写入计划后，才开始分配开发任务

### 垂直切片任务分解

任务按**垂直切片**（tracer bullet）拆分，不按技术层水平拆。每个切片贯穿所有层（schema → API → UI → 测试），可独立验证。

### 深度 TDD

开发者遵循增强版 TDD：
- **垂直切片**：一个测试 → 一个实现 → 重复（绝不先写所有测试）
- **行为测试**：通过公开接口测试系统做什么，而非怎么做
- **Mock 边界**：只在系统边界 mock（外部 API、数据库），不 mock 内部模块

### 架构感知代码审查

Reviewer 不仅检查安全/质量/性能，还检查：
- **Doc-Code 一致性** — API/架构文档是否同步更新？
- **不变量违反** — 变更是否突破了系统边界？
- **浅模块检测** — 接口复杂度 ≈ 实现复杂度
- **测试策略** — "替换而非叠加"冗余测试

### 可观测性支持（适用时）

对于 Web 应用和服务，引导 dev 发出结构化事件。E2E tester 使用**事件优先调试**：先查事件日志，再看浏览器控制台，最后才截图。可观测性不足标记为 `[OBSERVABILITY-GAP]`——比 Bug 本身更高优先级的发现。

### 文件持久化

所有进度持久化到 `.plans/<project>/`：

```
.plans/<project>/
  task_plan.md          -- 精简导航图
  docs/                 -- 项目知识库
    architecture.md / api-contracts.md / invariants.md
  archive/              -- 归档历史

  backend-dev/
    findings.md         -- 索引 → 各任务 findings
    task-auth/
      task_plan.md / findings.md / progress.md

  researcher/
    findings.md         -- 索引 → 各调研报告
    research-tech-stack/
      findings.md       -- 调研报告（核心交付物）

  reviewer/
    findings.md         -- 索引 → 各审查报告
    review-auth-module/
      findings.md       -- 完整审查报告
```

### 内置智能体协议

| 协议 | 作用 |
|------|------|
| 2-Action Rule | 每 2 次搜索操作后写 findings |
| 3-Strike 上报 | 3 次失败后上报，绝不静默重试 |
| 护栏捕获 | 将已解决的失败转化为 Known Pitfalls |
| 上下文恢复 | 渐进式展开：docs/ → 任务文件 → progress |
| 定期自检 | 每 ~10 次工具调用检查是否偏离计划 |
| Doc-Code 同步 | Dev 代码变更时更新 docs/；reviewer 验证 |
| 阶段健康检查 | 阶段边界时检查文档新鲜度、过期任务、索引完整性 |

### 活文档 CLAUDE.md

CLAUDE.md 不是一次性生成物——它是一份**活文档**，随项目演进。当捕获到失败模式、团队名单变动或建立新协议时更新。

## 已知限制：团队成员无法压缩上下文

团队成员（生成的 agent）与主对话共享相同的上下文窗口大小（如 1M token）。但**团队成员无法运行 `/compact` 来清理上下文**——只有主对话（team-lead）可以。随着上下文增长，智能体性能会下降。

**推荐的解决方案**：

1. 完全退出 Claude Code（`Ctrl+C` 或 `/exit`）
2. 用 `claude --continue` 恢复会话
3. Team-lead 读取 `.plans/` 文件恢复项目状态（CLAUDE.md 会自动加载）
4. 重新生成团队成员——它们以干净的上下文启动，通过读取各自的 `.plans/` 文件恢复工作进度

这是 Claude Code 平台的限制，不是 CCteam-creator 的问题。所有工作进度都持久化在 `.plans/` 文件中，重启不会丢失任何工作。

## 项目结构

```
CCteam-creator/
  .claude-plugin/
    marketplace.json              -- Marketplace 目录
    plugin.json                   -- 英文插件元数据
  skills/
    CCteam-creator/               -- 英文技能
      SKILL.md
      references/
        roles.md / onboarding.md / templates.md
  cn/                             -- 中文变体
    .claude-plugin/plugin.json
    skills/
      CCteam-creator/
        SKILL.md
        references/
          roles.md / onboarding.md / templates.md
  docs/images/                    -- 截图
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

## 许可证

MIT
