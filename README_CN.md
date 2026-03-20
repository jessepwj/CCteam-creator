# CCteam-creator

> [Claude Code](https://code.claude.com/) 多智能体团队编排技能。

[English](./README.md) | [中文](./README_CN.md)

## 站在巨人的肩膀上

CCteam-creator 基于以下优秀的开源项目构建：

| 项目 | 我们学到的 |
|------|-----------|
| [**planning-with-files**](https://github.com/OthmanAdi/planning-with-files) | Manus 风格的持久化 Markdown 规划 — 三文件模式（task_plan.md / findings.md / progress.md），经得起上下文压缩。"上下文窗口 = 内存，文件系统 = 磁盘"的核心理念。 |
| [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | Anthropic 黑客松获奖者的智能体优化体系。13 个专家智能体，40+ 技能。启发了我们的角色化智能体设计和技能结构。 |
| [**mattpocock/skills**](https://github.com/mattpocock/skills) | TDD 垂直切片哲学、"设计两次"并行子智能体模式、接口耐久性原则、以及方案压测方法论。 |

---

## 功能概述

CCteam-creator 在 Claude Code 中设置并行 AI 智能体团队。不再是单个 AI 助手，而是多个专业智能体 —— 开发、研究、测试、审查 —— 协同工作。

调用后，CCteam-creator 会：

1. **先沟通** — 介绍团队机制，了解项目需求，推荐团队配置
2. **完成搭建** — 创建规划文件、工作目录、CLAUDE.md 运营手册、智能体入职
3. **管理协作** — 智能体直接沟通，状态持久化到文件，遵循内置协议

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
cp -r CCteam-creator/plugins/CCteam-creator/skills/setup ~/.claude/skills/CCteam-creator

# 或中文
cp -r CCteam-creator/plugins/CCteam-creator-cn/skills/setup ~/.claude/skills/CCteam-creator
```

### 方式 3：项目级安装

```bash
# 通过项目目录与团队共享
cp -r CCteam-creator/plugins/CCteam-creator-cn/skills/setup .claude/skills/CCteam-creator
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
| 后端开发 | `backend-dev` | opus | 服务端代码 + TDD（垂直切片）+ 架构感知测试 |
| 前端开发 | `frontend-dev` | opus | 客户端代码 + TDD（垂直切片）+ 组件测试 |
| 探索/研究 | `researcher` | sonnet | 代码搜索 + 网页调研 + 方案压测（只读） |
| 联调测试 | `e2e-tester` | sonnet | Playwright E2E + 浏览器自动化 + Bug 追踪 |
| 代码审查 | `reviewer` | opus | 安全/质量/性能/架构审查（源码只读） |
| 代码清理 | `cleaner` | sonnet | 死代码清理 + 安全重构 |

不是每个项目都需要全部角色。CCteam-creator 会根据你的需求推荐合适的组合。

## 核心特性

### 需求对齐（阶段 0）

开发前，团队先进行结构化需求对齐：
- **Researcher** 探索现有代码库，记录架构现状
- **Team-lead** 与用户深入对齐需求细节
- 架构决策和范围写入计划后，才开始分配开发任务

### 垂直切片任务分解

任务按**垂直切片**（tracer bullet）拆分，不按技术层水平拆。每个切片贯穿所有层（schema → API → UI → 测试），可独立验证。

每个任务包含：
- **[AFK]/[HITL]** — 可自主完成 / 需要用户决策
- **blocked-by** — 明确依赖链
- **输入/输出** — 自包含，最小化智能体间信息损失
- **验收标准** — 智能体明确知道何时完成

### 方案压测

确定架构前，team-lead 委派 researcher 对方案进行压力测试 — 走遍决策树的每个分支，在开发前发现漏洞和风险。

### 深度 TDD

开发者遵循增强版 TDD：
- **垂直切片**：一个测试 → 一个实现 → 重复（绝不先写所有测试）
- **行为测试**：通过公开接口测试系统做什么，而非怎么做
- **Mock 边界**：只在系统边界 mock（外部 API、数据库），不 mock 内部模块
- **可测试接口**：依赖注入、返回结果优于副作用

### 架构感知代码审查

Reviewer 不仅检查安全/质量/性能，还检查：
- **浅模块检测** — 接口复杂度 ≈ 实现复杂度
- **依赖分类** — in-process / local-substitutable / remote-owned / true-external
- **测试策略评估** — "替换而非叠加"冗余测试

### 耐久性研究输出

Researcher 的发现同时包含文件路径（当前定位）和行为描述（重构后仍有效）。示例：
> 认证逻辑在 `src/auth/middleware.ts:42` — 拦截所有 /api/* 路由，验证 Authorization header 中的 JWT，将解码后的用户信息附加到 req.user。

### 文件持久化

所有进度持久化到 `.plans/<project>/`：

```
.plans/<project>/
  task_plan.md          -- 主计划（含垂直切片）
  findings.md           -- 团队级摘要
  progress.md           -- 工作日志

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
| 上下文恢复 | 压缩后先读规划文件再继续 |
| 定期自检 | 每 ~10 次工具调用检查是否偏离计划 |
| 任务交接 | 基于文件的交接（摘要 + 文档位置） |

## 项目结构

```
CCteam-creator/
  .claude-plugin/
    marketplace.json              -- Marketplace 目录
  plugins/
    CCteam-creator/               -- 英文插件
      .claude-plugin/plugin.json
      skills/setup/
        SKILL.md
        references/
          roles.md / onboarding.md / templates.md
    CCteam-creator-cn/            -- 中文插件
      .claude-plugin/plugin.json
      skills/setup/
        SKILL.md
        references/
          roles.md / onboarding.md / templates.md
  README.md / README_CN.md
  LICENSE
```

## 许可证

MIT
