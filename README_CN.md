# CCteam-creator

> 面向 [Claude Code](https://code.claude.com/) 的多智能体团队编排插件。

[English](./README.md) | [中文](./README_CN.md)

## 站在巨人的肩膀上

CCteam-creator 基于两个优秀的开源项目构建：

| 项目 | Stars | 我们学到了什么 |
|------|-------|--------------|
| [**planning-with-files**](https://github.com/OthmanAdi/planning-with-files) | 16,000+ | Manus 风格的持久化 Markdown 规划 — 三文件模式（task_plan.md / findings.md / progress.md）能在上下文压缩后存活。"上下文窗口 = 内存，文件系统 = 磁盘" 的哲学是 CCteam-creator 状态持久化的骨架。源自 [Manus $20 亿收购案](https://github.com/OthmanAdi/planning-with-files)背后的工作流模式。 |
| [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | 50,000+ | Anthropic 黑客松冠军 [@affaan-m](https://github.com/affaan-m) 打造的智能体性能优化系统。13 个专家智能体、40+ 技能、98% 测试覆盖率。启发了我们的 skill 结构、角色化智能体设计和插件分发方式。 |

CCteam-creator 将他们的理念延伸到**多智能体协调**领域 — 编排多个专业智能体并行工作，配以结构化沟通和文件驱动的进度追踪。

---

CCteam-creator 帮助你在 Claude Code 中搭建和管理并行 AI 智能体团队。不再是单个 AI 助手，而是协调多个专业智能体 — 开发者、研究员、测试员、审查员 — 共同协作完成项目。

## 它做什么

当你调用 `/CCteam-creator-cn:setup` 时，CCteam-creator 会：

1. **先跟你沟通** — 解释智能体团队的运作方式，了解你的项目需求，推荐团队配置
2. **搭建团队** — 创建规划文件、工作目录，并为每个智能体生成入职指令
3. **管理协作** — 智能体之间直接沟通（dev 找 reviewer 审查代码），向 team-lead（你）汇报进度，所有状态持久化到文件

## 前置条件

### 启用 Agent Teams

Agent Teams 是 Claude Code 的实验性功能。**必须**先启用才能使用：

**方式 A：在 Shell 中设置**
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**方式 B：在 settings.json 中设置**（`~/.claude/settings.json`）
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## 安装

> **重要提示**：英文版和中文版只需安装其中一个，不要同时安装两个。两者功能完全相同，只是语言不同。同时安装会导致冲突。

### 方式 1：市场安装（推荐）

```bash
# 第 1 步：添加市场（在 Claude Code 中执行）
/plugin marketplace add jessepwj/CCteam-creator

# 第 2 步：安装插件 — 选择一个语言版本
/plugin install CCteam-creator@ccteam        # 英文版
/plugin install CCteam-creator-cn@ccteam     # 中文版
```

### 方式 2：手动复制 — 英文版（默认）

```bash
git clone https://github.com/jessepwj/CCteam-creator.git
cp -r CCteam-creator/plugins/CCteam-creator/skills/setup ~/.claude/skills/CCteam-creator
```

### 方式 3：手动复制 — 中文版

```bash
git clone https://github.com/jessepwj/CCteam-creator.git
cp -r CCteam-creator/plugins/CCteam-creator-cn/skills/setup ~/.claude/skills/CCteam-creator
```

> **注意**：两个版本都复制到相同的目标目录（`~/.claude/skills/CCteam-creator`）。这确保同一时间只有一个版本处于激活状态。

### 方式 4：项目级安装

将 skill 放在项目的 `.claude/skills/` 目录中，团队成员共享：

```bash
# 英文版（默认）
cp -r CCteam-creator/plugins/CCteam-creator/skills/setup .claude/skills/CCteam-creator

# 或中文版
cp -r CCteam-creator/plugins/CCteam-creator-cn/skills/setup .claude/skills/CCteam-creator
```

## 使用方法

直接告诉 Claude Code 你想搭建团队：

```
> 帮我为电商项目搭建一个团队
> /CCteam-creator-cn:setup
> 我想做一个 REST API，能创建一个团队吗？
```

> **注意**：如果通过手动复制安装（方式 2-4），命令为 `/CCteam-creator`，而非 `/CCteam-creator-cn:setup`。

CCteam-creator 会：
1. 解释智能体团队的工作方式
2. 了解你的项目目标、技术栈和偏好
3. 推荐需要的角色组合
4. 和你确认方案
5. 创建所有规划文件并生成智能体

### 触发关键词

当你提到以下词汇时 skill 自动激活：`team`、`swarm`、`start project`、`set up project`、`create team`、`build team`、`organize project`、`multi-agent project`。

## 可用角色

| 角色 | 名称 | 模型 | 核心能力 |
|------|------|------|---------|
| 后端开发 | `backend-dev` | opus | 写代码 + TDD + 大任务按 task 分文件夹 |
| 前端开发 | `frontend-dev` | opus | 写代码 + TDD + 大任务按 task 分文件夹 |
| 探索/研究 | `researcher` | sonnet | 代码搜索 + 网页搜索（只读不改代码） |
| 联调测试 | `e2e-tester` | sonnet | Playwright E2E 测试 + 浏览器自动化 |
| 代码审查 | `reviewer` | opus | 安全/质量/性能深度审查（只读源码） |
| 代码清理 | `cleaner` | sonnet | 死代码清理 + 安全重构 |

不是每个项目都需要全部角色。CCteam-creator 会根据你的需求推荐合适的��合。

## 工作原理

### 文件驱动的规划

所有进度持久化到 `.plans/<项目>/` — 上下文压缩时不会丢失状态：

```
.plans/<project>/
  task_plan.md          -- 主计划（阶段、架构、任务分配）
  findings.md           -- 团队级摘要
  progress.md           -- 工作日志

  backend-dev/          -- 每个智能体的工作区
    findings.md         -- 索引，链接到各任务的具体发现
    task-auth/          -- 每个分配的任务有独立文件夹
      task_plan.md / findings.md / progress.md

  researcher/
    findings.md         -- 索引，链接到各调研报告
    research-tech-stack/ -- 每个调研课题
      findings.md       -- 调研报告（主要交付物）

  e2e-tester/
    findings.md         -- 索引，链接到各轮测试结果
    test-auth-flow/     -- 每个测试范围
      findings.md       -- 测试结果和 Bug

  reviewer/
    findings.md         -- 索引，链接到各次审查
    review-auth-module/ -- 每次代码审查
      findings.md       -- 完整审查报告
```

所有角色都使用任务文件夹 — 根 `findings.md` 作为整洁的索引，而非所有内容的堆砌。

### 智能体协议

每个智能体遵循内置协议：
- **2-Action Rule**：每 2 次搜索/读取操作后，必须更新 findings.md（开发角色编码中读代码豁免）
- **3-Strike 协议**：同一问题失败 3 次后，上报 team-lead
- **上下文恢复**：压缩后，智能体先重读自己的 3 个规划文件再继续工作
- **定期自检**：约每 10 次工具调用，智能体验证是否偏离任务计划

### 团队沟通

- 智能体向 team-lead（你）汇报进度
- 开发者直接找 reviewer 请求代码审查
- 大任务交接时包含文档（findings.md 位置 + 摘要）
- reviewer 将审查结果写入开发者的 findings.md
- 所有沟通透明且有记录

## 自定义选项

你可以自定义：
- **角色组合** — 只选需要的角色
- **自定义角色** — 定义新角色及其职责
- **任务阶段** — 按自己的方式组织项目阶段
- **审查严格度** — 启用/禁用代码审查和安全审查门禁

## 项目结构

```
CCteam-creator/
  .claude-plugin/
    marketplace.json                  -- 市场目录
  plugins/
    CCteam-creator/                   -- 英文版插件
      .claude-plugin/
        plugin.json                   -- 插件清单
      skills/
        setup/                        -- 技能
          SKILL.md
          references/
            roles.md
            onboarding.md
            templates.md
    CCteam-creator-cn/                -- 中文版插件
      .claude-plugin/
        plugin.json                   -- 插件清单
      skills/
        setup/                        -- 技能
          SKILL.md
          references/
            roles.md
            onboarding.md
            templates.md
  README.md                           -- 英文文档
  README_CN.md                        -- 中文文档
  LICENSE                             -- MIT 许可证
```

## 许可证

MIT
