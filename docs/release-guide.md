# 发布流程指南 (Release Guide)

> 本文档记录 CCteam-creator 的发布流程,以及所有来自实际调试的"坑"和对应的检查项。
> 每次准备推新版本时,**从头到尾过一遍这份清单**。
>
> 最后更新: 2026-04-10 (基于 1.3.2 修复经验)

---

## 核心不变量 (Critical Invariants)

**这些规则绝对不能破。破了就是用户看不到/用不了 skill 的 bug。**

### 🔴 不变量 1:三个名字必须完全一致

对每个 plugin(EN 和 CN 各一套),以下三个名字**必须严格相同**:

| # | 位置 | EN 期望值 | CN 期望值 |
|---|---|---|---|
| 1 | `.claude-plugin/plugin.json` 的 `name` 字段 | `CCteam-creator` | `CCteam-creator-cn` |
| 2 | skill 目录名(在 `skills/` 下面) | `skills/CCteam-creator/` | `cn/skills/CCteam-creator-cn/` |
| 3 | SKILL.md frontmatter 的 `name` 字段 | `name: CCteam-creator` | `name: CCteam-creator-cn` |

**为什么**:Claude Code 把 plugin skill 注册成 namespace `plugin-name:skill-directory-name`,三者对齐后 slash 命令 `/CCteam-creator` 和 `Skill(CCteam-creator:CCteam-creator)` 才能工作。任何一个不对齐 → `Unknown skill` 错误。

**参考对照**:`planning-with-files` 这个 plugin 的三者完全一致(所有名字都是 `planning-with-files`),这是业界惯例。

### 🔴 不变量 2:SKILL.md frontmatter 必须是合法的 YAML

**正确格式**(两个 `---` 之间是 YAML,字段名前**不能**有 `#`):

```yaml
---
name: CCteam-creator
description: >
  Multi-line description
  using YAML block scalar...
---

# Markdown content starts here
```

**错误示例**(今天踩过的坑):

```yaml
---

## name: setup          ← ❌ "## name:" 是 Markdown 标题,不是 YAML 键
description: >
  ...

# 团队项目设置           ← ❌ 没有闭合的 ---,frontmatter 永远不结束
```

**验证方法**:用任何 YAML parser 尝试解析前两个 `---` 之间的内容,如果失败就是坏的。`validate-release.py` 自动做这个检查。

### 🔴 不变量 3:版本号必须在三处同时 bump

每次发布,以下三个文件的 version 字段**必须**同时更新到相同的值:

```
.claude-plugin/plugin.json           → "version": "X.Y.Z"
cn/.claude-plugin/plugin.json        → "version": "X.Y.Z"
.claude-plugin/marketplace.json      → "metadata": { "version": "X.Y.Z" }
```

**为什么**:
- 第一个文件是 EN plugin 的版本
- 第二个文件是 CN plugin 的版本
- 第三个文件是 marketplace 的版本(marketplace 可能在 UI 显示,用户凭它判断 marketplace 本身新不新)
- 只要有一个没 bump,Claude Code 的 `/plugin marketplace update` 可能检测不到变化(即使有 bug,它至少能 diff 版本字符串)

**版本号递增规则**(语义化):

| 改动类型 | 示例 | 版本跳变 |
|---|---|---|
| **Breaking 变更** | 角色名改了、模板结构改了、入职 prompt 完全重写 | `major` bump (`1.x` → `2.0`) |
| **Minor 功能** | 新增协议(如 Step 0 Update Check)、新增角色、新增 skill | `minor` bump (`1.3` → `1.4`) |
| **Patch 修复** | frontmatter bug、文案错字、调整现有流程 | `patch` bump (`1.3.1` → `1.3.2`) |

### 🔴 不变量 4:EN 和 CN 必须保持同构(parallel structure)

EN 和 CN 是**同一个 skill 的两个语言变体**,结构必须对称:

- `skills/CCteam-creator/` 里有什么,`cn/skills/CCteam-creator-cn/` 里就该有什么
- `references/`、`scripts/` 的文件名必须一致
- 只有**文案和注释**应该是不同语言
- 版本号必须同步

**反模式**:
- ❌ 只改 EN 忘了改 CN(用户装 CN 拿到旧行为)
- ❌ CN 比 EN 多/少一个 reference 文件
- ❌ CN 的某个部分翻译成了中文,但其他部分还是英文

**记忆规则**:我的 MEMORY 里有"deployment checklist",每次改完自动同步 EN 和 CN——但手动改时很容易漏。validate-release.py 会检查文件清单对称性。

---

## 发布前检查清单 (Pre-Release Checklist)

每次准备发布新版本,**从上到下**过一遍这份列表。

### 第 1 步:代码改动自检

- [ ] 改动只涉及预期的文件(没有误改别的)
- [ ] 如果改了 SKILL.md 或 references/,EN 和 CN **两边都改了**
- [ ] 如果新增了 skill 协议/功能,README 的"Core Features"章节也更新了
- [ ] 如果改了角色定义,`roles.md` 和 `onboarding.md` **两边**都一致

### 第 2 步:运行自动化验证脚本

```bash
cd E:/aigc内容整理/开源团队skills/CCteam-creator
python scripts/validate-release.py
```

期望输出:`[OK] All checks passed.`

如果报错,**先修 bug,再推送**。不要跳过。

### 第 3 步:Bump 版本号

根据改动类型决定 major/minor/patch,然后**三处同时改**:

```bash
# 查看当前版本
grep version .claude-plugin/plugin.json cn/.claude-plugin/plugin.json .claude-plugin/marketplace.json

# 手动改三个文件的 version 字段,保持一致
```

### 第 4 步:检查 git 工作区

```bash
git status
git diff --stat
```

**警告:git 工作区里可能有"年久失修"的未提交改动**。今天就踩过这个坑——`README_CN.md` 里有 8 天前的图片 markdown 删除,差点被误提交。

- [ ] `git status` 的每一个 modified 文件都是**你这次有意**改的
- [ ] 看到意外修改的文件,**先搞清楚来源**再决定是 reset 还是一起提交
- [ ] 绝对不要 `git add -A` 一把梭,除非你对每个文件都 100% 有数

### 第 5 步:写有意义的 commit message

格式(半强制):

```
<type>: v<version> — <one-line summary>

Root cause / Motivation:
  <why this change was needed>

Changes:
  1. <what>
  2. <what>
  3. <what>

Expected post-update behavior:
  <how users should verify this works>

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

Type 词汇:
- `feat` — 新功能(minor bump)
- `fix` — bug 修复(patch bump)
- `refactor` — 重构,行为不变(一般不 bump)
- `docs` — 只改文档(一般不 bump,但如果改了 README 的协议描述就要 bump)

### 第 6 步:Push 到 GitHub

```bash
git push origin master
```

不要 `--force`,不要 `--no-verify`。

### 第 7 步:验证 GitHub 上的提交

打开 https://github.com/jessepwj/CCteam-creator/commits/master ,确认:
- [ ] 最新 commit 是你推的那个
- [ ] Commit message 没有渲染错误
- [ ] 文件 diff 看起来和你本地一致

---

## 发布后验证 (Post-Release Verification)

**必须在新 session 里做**,因为当前 session 已经加载了旧版 skill。

### 新 session 里的操作

```
# 1. 刷新 marketplace 元数据
/plugin marketplace update ccteam

# 2. 如果上一步说 "no changes" 但你确实推了新版,强制刷新:
/plugin marketplace remove ccteam
/plugin marketplace add jessepwj/CCteam-creator

# 3. 安装/升级 plugin
/plugin install CCteam-creator@ccteam           # EN
/plugin install CCteam-creator-cn@ccteam        # CN (二选一或都装)

# 4. 关键步骤:reload
/reload-plugins
```

### 验证清单

- [ ] `ls ~/.claude/plugins/cache/ccteam/CCteam-creator/` 看到新版本号目录
- [ ] `head -5 ~/.claude/plugins/cache/ccteam/CCteam-creator/<new-version>/skills/CCteam-creator/SKILL.md` 看到正确的 frontmatter(`name: CCteam-creator`,有闭合 `---`)
- [ ] 对 Claude 说"你有什么 skills",列表里出现 `CCteam-creator`(或至少可以通过 namespace 调用)
- [ ] `/CCteam-creator` → 应该触发 skill(或者 `Skill(CCteam-creator:CCteam-creator)`)
- [ ] 自然语言触发:"帮我搭建一个测试团队" → Claude 应该 match 到 skill
- [ ] Step 0 Update Check 行为正确:本地版本 = 远程版本时**完全静默**,无多余输出

### 如果新版本没生效

按顺序排查:

1. **检查 `installed_plugins.json`**:
   ```bash
   cat ~/.claude/plugins/installed_plugins.json | python -c "import sys,json; d=json.load(sys.stdin); print(json.dumps({k:v for k,v in d['plugins'].items() if 'ccteam' in k.lower()}, indent=2))"
   ```
   确认 gitCommitSha 和版本是新推的那个。

2. **检查 frontmatter 是否真的拉下来了**:
   ```bash
   head -5 ~/.claude/plugins/cache/ccteam/CCteam-creator/<version>/skills/CCteam-creator/SKILL.md
   ```

3. **检查 `/reload-plugins` 是否真的跑了**:在 Claude Code 里重新输入一遍

4. **终极大招**:`/exit` 完全退出 Claude Code,重新打开一次新 session

---

## 常见坑 (Common Pitfalls)

全部来自实际调试记录。每条都有历史版本参考。

### 坑 1:Frontmatter 写成 Markdown 标题

**症状**:plugin 装上了但 skill 列表里找不到,或报 "Unknown skill"。

**原因**:
```yaml
---
## name: setup    ← 这是 Markdown H2 标题!不是 YAML 键!
```

**修复**:
```yaml
---
name: setup
---
```

**检测**:`scripts/validate-release.py` 会 YAML parse 两个 `---` 之间的内容,失败即报错。

**历史**:1.3.0 的 CN SKILL.md 就是这个问题,用户装完发现 skill 不出现。1.3.1 修复。

### 坑 2:Frontmatter 没有闭合 `---`

**症状**:同上,plugin 装了但 skill 不识别。

**原因**:
```yaml
---
name: setup
description: >
  ...
(缺少闭合的 ---)

# 正文 Markdown 内容 ← YAML parser 认为 frontmatter 一直延伸到这里
```

**修复**:在 description 结束后加一行 `---`。

### 坑 3:Skill name 和 plugin name 不匹配

**症状**:`Skill(CCteam-creator)` 报 "Unknown skill",只有 `Skill(CCteam-creator:CCteam-creator)` 或错误的 `Skill(CCteam-creator:setup)` 能用。

**原因**:三个名字不一致(见不变量 1)。

**修复**:把 frontmatter `name:` 改成和 plugin 名 + 目录名都一致。

**历史**:1.3.0/1.3.1 时 EN frontmatter 是 `name: setup`,和 plugin 名 `CCteam-creator` 不匹配。1.3.2 修复。

### 坑 4:CN skill 目录名和 plugin 名不匹配

**症状**:EN 版 `/CCteam-creator` 能用,但 CN 版 `/CCteam-creator-cn` 不能用(或用错误的 namespace)。

**原因**:
```
cn/.claude-plugin/plugin.json → name: "CCteam-creator-cn"
cn/skills/CCteam-creator/     ← 目录名错了!应该是 CCteam-creator-cn/
```

**修复**:`git mv cn/skills/CCteam-creator cn/skills/CCteam-creator-cn`

**历史**:1.3.2 修复。

### 坑 5:版本没 bump 就 push

**症状**:用户跑 `/plugin marketplace update ccteam` 说"没有更新"。

**原因**:plugin.json version 没改,Claude Code 认为版本没变。

**修复**:每次发布前强制 bump 版本(见第 3 步)。

**防御**:validate-release.py 可以对比 git HEAD 和工作区的 version 字段,如果 HEAD 已经提交了同样的 version 但工作区又 push 了新改动,警告。

### 坑 6:git 工作区有遗留的未提交改动

**症状**:`git diff --stat` 显示一些你**没改过**的文件(`README_CN.md` 少了图片、`golden_rules.py` 翻译成中文等)。

**原因**:之前 session 改了但忘了提交/reset。今天就有两个:
- `README_CN.md` 8 天前被删了图片 markdown(regression,会让 GitHub 渲染失去图片)
- `cn/.../golden_rules.py` 翻译了但没提交

**检测**:`git status --short` 有任何非预期文件就停下来排查。

**修复**:根据情况选择:
- 意外的 regression → `git checkout HEAD -- <file>` 恢复
- 忘了提交的合理改动 → `git add <file>` 加入本次 commit,commit message 里注明
- 不确定 → 单独 commit 这部分改动,加上明确说明

### 坑 7:推了但忘了 `/reload-plugins`

**症状**:`/plugin install` 显示 "Successfully installed" 但 skill 不出现在列表/调用失败。

**原因**:Claude Code 的 plugin install 不会自动激活,需要 `/reload-plugins` 或重启 session。

**防御**:README 的安装说明里**必须**包含 `/reload-plugins` 作为强制步骤(1.3.2 已修)。

### 坑 8:混淆 `/plugin marketplace add` 和 `/plugin install`

**症状**:用户说"我装了但看不到",但 `installed_plugins.json` 里没条目。

**原因**:`/plugin marketplace add` 只注册 marketplace 源(仓库的克隆),`/plugin install` 才是真正的安装。用户容易只跑前者。

**防御**:README 的安装步骤必须明确两条命令都要跑,顺序不能错。

### 坑 9:LF / CRLF 警告

**症状**:`git diff` 时出现:
```
warning: in the working copy of 'SKILL.md', LF will be replaced by CRLF the next time Git touches it
```

**原因**:Windows 的 git config 是 `autocrlf=true`,文件在 checkout 时会变 CRLF,commit 时又变回 LF。

**影响**:通常无害,不用修。

**如果真的出问题**:repo 根加一个 `.gitattributes`:
```
*.md text eol=lf
*.py text eol=lf
*.json text eol=lf
```

---

## 回滚流程 (Rollback)

如果推了 v1.3.3 后发现严重问题,需要回滚。

### 方式 1:发一个快速 hotfix 版本(推荐)

**不要回滚**,而是发一个 `v1.3.4` 修复 bug。用户只会看到版本号递增,Step 0 Update Check 会通知他们更新。

```bash
# 1. 修 bug
# 2. bump 到 1.3.4
# 3. commit + push
# 4. 文档里说明 "1.3.3 has a known issue, upgrade to 1.3.4 immediately"
```

### 方式 2:真的要回滚到旧 commit

```bash
# 1. 不要用 git reset --hard 直接改历史
# 2. 用 revert 创建一个反向提交:
git revert <bad-commit-sha>

# 3. bump 版本到 1.3.x+1(即使内容退回旧版,版本号也必须前进)
# 4. push
# 5. 用户通过 update 拿到"退回旧行为"的新版本
```

**绝对不要**:
- `git push --force` 覆盖 master(会破坏其他人的 fork)
- 删除 tag 再重推同名 tag
- 降低版本号(用户的 Step 0 Update Check 会检测到"本地 > 远程"然后静默跳过,拿不到回滚)

---

## 已知上游 bugs (Upstream Bugs to Be Aware Of)

这些是 Claude Code 本身的 bug,不是我们的,但会影响发布体验。知道了就好绕开。

### Bug 1:第三方 marketplace 自动更新不可靠

**Issue**: [anthropics/claude-code#31462](https://github.com/anthropics/claude-code/issues/31462) 和 #37252, #38271

**现象**:`/plugin marketplace update <name>` 有时显示 "no updates" 即使确实有新版本。

**绕法**:
```
/plugin marketplace remove ccteam
/plugin marketplace add jessepwj/CCteam-creator
/plugin install CCteam-creator@ccteam
/plugin install CCteam-creator-cn@ccteam
/reload-plugins
```

这个"remove + add"组合强制重新克隆。

**我们的应对**:Step 0 Update Check 会在每次触发 skill 时主动告诉用户有新版,弥补 Claude Code 自动更新的不可靠。

### Bug 2:`/skills` CLI 命令不列出 symlinked skill

**Issue**: [anthropics/claude-code#37590](https://github.com/anthropics/claude-code/issues/37590)

**现象**:如果 skill 是符号链接(`ln -s` 或 `mklink /J`)装到 `~/.claude/skills/` 的,`/skills` 命令看不到它,但功能上能用。

**影响**:如果我们未来加"直接 skill 安装"模式(之前讨论过的 install.sh / install.ps1),需要用**真实复制**而不是符号链接。

---

## 附录:MEMORY.md 部署清单更新

每次发布完,更新 `C:\Users\msi\.claude\projects\E--aigc---------skills\memory\MEMORY.md` 里的 "CCteam-creator Project Memory" 段,记录:

- 当前版本
- 本次改动的关键决策(不是改了什么代码,是**为什么**这么改)
- 踩到的新坑(如果有)

示例(1.3.2 之后应该加的):

```markdown
## Key Decisions (updated 2026-04-10)

- v1.3.2: Three-name alignment discovered as critical invariant.
  Plugin name == skill directory name == SKILL.md frontmatter name.
  Mismatch → `Unknown skill` error. Reference: planning-with-files as the canonical pattern.
```

---

## 附录:快速命令速查

```bash
# 本地验证(push 前必跑)
python scripts/validate-release.py

# 查看三处版本
grep -H version .claude-plugin/plugin.json cn/.claude-plugin/plugin.json .claude-plugin/marketplace.json

# 查看 frontmatter
head -15 skills/CCteam-creator/SKILL.md
head -15 cn/skills/CCteam-creator-cn/SKILL.md

# 查看已安装的 CCteam-creator 版本
cat ~/.claude/plugins/installed_plugins.json | grep -A5 ccteam

# 查看当前 cache 版本号
ls ~/.claude/plugins/cache/ccteam/CCteam-creator/
ls ~/.claude/plugins/cache/ccteam/CCteam-creator-cn/

# 查看 cache 里的 frontmatter(确认 marketplace 拉对了)
head -5 ~/.claude/plugins/cache/ccteam/CCteam-creator/*/skills/CCteam-creator/SKILL.md

# git 状态全貌
git status --short && echo "---" && git diff --stat
```

---

**文档终结,祝发布顺利。下次如果又踩到新坑,记得回来补充 "常见坑" 章节。**
