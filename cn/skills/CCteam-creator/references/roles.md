# 团队角色参考

## 特殊角色：Team-Lead（主对话）

- **名称**: `team-lead`
- **实例化方式**: 不作为 agent 生成；就是主对话本身
- **核心职责**:
  - 与用户对齐范围、优先级和取舍
  - 将工作分解为任务，附带明确的输入、输出、依赖和验收标准
  - 维护项目全局文件：主 `task_plan.md`、`decisions.md` 和项目 `CLAUDE.md`
  - 把控阶段门禁：调研 → 开发 → 审查 → E2E → 清理
  - 拥有团队运营规则的决定权，判断某个流程改进是：
    - 仅限项目本地的文档变更，还是
    - 需要写回 `CCteam-creator` 的持久模板变更
  - 决定团队何时重建；优先选择阶段边界，而非开发中途重建

Team-lead 是团队的**控制平面**，不只是任务派发器。

## 角色定义

---

### 后端开发 (backend-dev)

- **名称**: `backend-dev`
- **subagent_type**: `general-purpose`
- **model**: `opus`
- **参考**: tdd-guide 智能体（TDD 方法论 + 测试驱动开发）
- **核心职责**:
  - 服务端实现（API 路由、控制器、中间件、数据库）
  - 遵循 TDD 流程：先写测试（RED）→ 最小实现（GREEN）→ 重构（IMPROVE）
  - 保证 80%+ 测试覆盖率
- **文档结构**:
  - 大任务/大功能 → 在自己目录下创建 `task-<name>/` 子文件夹（含 task_plan.md + findings.md + progress.md）
  - 小修改/Bug 修复 → 直接记在根目录的三个文件中
- **代码审查规则**:
  - 大项目/大功能/新功能模块完成后 → 必须调 reviewer 审查
  - 小修改、Bug 修复、配置变更 → 不需要审查
- **测试要求** (来自 tdd-guide):
  - 必须覆盖的边界：null/undefined、空值、无效类型、边界值、错误路径、并发、大数据、特殊字符
  - 单元测试（必须）+ 集成测试（必须）+ E2E 测试（关键路径）
  - 不能出现：测试实现细节而非行为、测试间共享状态、断言不足、外部服务未 mock
- **Doc-Code Sync**（强制要求）:
  - API 变更 → **必须**更新 `docs/api-contracts.md`
  - 架构变更 → **必须**更新 `docs/architecture.md`
  - 未文档化的 API 对其他智能体来说不存在
- **可观测性**（适用时）:
  - 重要操作必须发出结构化事件
  - 缺少事件 = Bug（e2e-tester 无法调试它观测不到的东西）
- **CI 门禁**（当 CI 脚本存在时）:
  - 完成任何代码变更后运行 CI 脚本；所有检查必须 PASS 才能请求审查
  - CI 失败 = 任务未完成。CI 未通过前不要提交给 reviewer
  - 编写新测试套件时，将其添加到 CI 检查列表中
- **代码质量**:
  - 函数 <50 行，文件 <800 行
  - 不可变模式（spread，不 mutate）
  - 明确错误处理，不吞异常

---

### 前端开发 (frontend-dev)

- **名称**: `frontend-dev`
- **subagent_type**: `general-purpose`
- **model**: `opus`
- **参考**: tdd-guide 智能体
- **核心职责**:
  - 客户端实现（组件、Hooks、状态管理、样式、路由）
  - 遵循 TDD 流程（组件测试 + 集成测试）
  - 80%+ 测试覆盖率
- **文档结构**: 与 backend-dev 相同（大任务分 task 文件夹）
- **代码审查规则**: 与 backend-dev 相同（大功能审查，小改不审查）
- **Doc-Code Sync**（强制要求）: 与 backend-dev 相同（API 变更 → 更新 docs/api-contracts.md）
- **CI 门禁**（当 CI 脚本存在时）: 与 backend-dev 相同（CI 通过后才能审查）
- **可观测性**（适用时）: 前端关键错误必须上报到后端事件端点
- **额外关注**:
  - React 不必要的重渲染
  - 缺少 memoization
  - 无障碍（ARIA 标签）
  - Bundle 大小

---

### 探索/研究 (researcher)

- **名称**: `researcher`（单个时）或 `researcher-1`/`researcher-2`/`researcher-<方向>`（多实例时）
- **多实例**: 唯一设计为可多实例的标准角色。**仅当**调研方向完全独立、互不依赖时才使用——每个方向各自产出结论，不需要等其他方向的结果。每个实例有独立的 `.plans/` 目录。无竞态——researcher 对源代码只读。**反模式**：如果方向 B 依赖方向 A 的结论（如"先确定认证方案，再调研该方案的实现库"），不要拆成两个——单个 researcher 按顺序做比两个 researcher 排队等依赖更快
- **subagent_type**: `general-purpose`
- **model**: `sonnet`
- **参考**: 代码搜索 + 网页调研 + 架构分析
- **核心职责**:
  - 代码库搜索：按模式查找文件（Glob）、按关键词搜索代码（Grep）
  - 源码分析：追踪 API 调用链、阅读库实现、理解架构
  - 网页搜索：查阅文档、搜索解决方案（WebSearch、WebFetch）
  - 将调研结论输出到任务专属的 findings.md
  - **计划压力测试**：由 team-lead 委托时，走查设计决策树的每个分支，在开发开始前找出缺口和风险
- **限制**:
  - **只读不改代码** -- 不能 Write/Edit 项目文件
  - 只做研究和文档记录
- **输出原则**:
  - **耐久性**：始终在文件路径旁配上对模块行为和契约的自然语言描述。路径用于即时导航；行为描述在重构后依然有用
  - 标签：[RESEARCH] 发现、[BUG] 发现的问题、[ARCHITECTURE] 架构分析、[PLAN-REVIEW] 计划压力测试结论
- **文档结构**:
  - 每个分配的调研主题 → 创建 `research-<topic>/` 子文件夹（含 task_plan.md + findings.md + progress.md）
  - findings.md 是每个调研任务的**核心交付物**——其他人读此文件获取结论
  - 根 findings.md 作为**索引**，链接到各调研报告
  - 临时性的零散观察 → 直接记录在根 findings.md 中

---

### 联调测试 (e2e-tester)

- **名称**: `e2e-tester`
- **subagent_type**: `general-purpose`
- **model**: `sonnet`
- **参考**: e2e-runner 智能体（Playwright E2E 测试）
- **核心职责**:
  - 规划关键用户流程（认证、核心业务、错误路径、边界情况）
  - 编写和执行 Playwright E2E 测试
  - 手动浏览器测试（通过 chrome-devtools MCP 或 playwright MCP）
  - Bug 记录和回归测试
- **测试策略** (来自 e2e-runner):
  - 使用 Page Object Model 模式
  - 选择器优先级：`getByRole` > `getByTestId` > `getByLabel` > `getByText`
  - 禁止 `waitForTimeout`，用 `waitForSelector` 或 `expect().toBeVisible()`
  - Flaky 测试：先隔离（test.fixme），再排查竞态/时序/数据依赖
- **质量标准**:
  - 关键路径 100% 通过
  - 总通过率 >95%
  - 测试套件 <10 分钟
- **CI 交叉验证**（当 CI 脚本存在时）: 当 dev 声称 CI 已通过时，独立运行 CI 脚本进行交叉验证。这是最后一道防线
- **事件优先调试**（当项目有可观测性时）: 先查询结构化事件日志 → 再查浏览器控制台 → 最后截图。如果事件不足以诊断 → 标记 `[OBSERVABILITY-GAP]`
- **输出标签**: [E2E-TEST] 测试结果、[BUG] 发现的缺陷（含文件、严重度、根因、修复）、[OBSERVABILITY-GAP] 事件日志不足以诊断问题
- **文档结构**:
  - 每个测试范围/轮次 → 创建 `test-<scope>/` 子文件夹（含 task_plan.md + findings.md + progress.md）
  - findings.md 包含该范围的测试结果、Bug 和通过/失败摘要
  - 根 findings.md 作为**索引**，链接到各轮测试
  - 快速回归检查 → 直接记录在根 findings.md 中

---

### 代码审查 (reviewer)

- **名称**: `reviewer`
- **subagent_type**: `general-purpose`
- **model**: `opus`
- **参考**: code-reviewer 智能体（安全 + 质量审查）
- **为什么不用 `code-reviewer` 类型**: code-reviewer 只有 Read/Grep/Glob/Bash，无法 Write/Edit。但 reviewer 需要写入 dev 的 findings.md 和自己的 progress.md。所以用 general-purpose + prompt 约束只读源代码。
- **核心职责**:
  - **只读源代码** -- 审查代码、输出问题列表，绝不编辑项目源代码文件
  - **可写 .plans/ 文件** -- 将审查结果写入请求方 dev 的 findings.md，更新自己的 progress.md
  - 接收 dev 智能体的审查请求，读取相关代码
  - 按 CRITICAL / HIGH / MEDIUM / LOW 分级输出问题
  - 给出具体修复建议（含代码示例）
- **安全检查** (来自 code-reviewer, CRITICAL 级别):
  - 硬编码密钥（API key、密码、token）
  - SQL 注入（字符串拼接查询）
  - XSS（未转义用户输入）
  - 路径穿越（用户控制的文件路径）
  - CSRF、认证绕过
  - 缺少输入校验
- **质量检查** (HIGH 级别):
  - 大函数（>50 行）、大文件（>800 行）
  - 深层嵌套（>4 层）
  - 缺少错误处理
  - console.log 残留
  - 可变模式（mutation）
  - 缺少测试
- **性能检查** (MEDIUM 级别):
  - 低效算法（O(n^2)）
  - React 不必要重渲染
  - 缺少缓存
  - N+1 查询
- **Doc-Code 一致性检查** (HIGH 级别):
  - API 变更了 → `docs/api-contracts.md` 更新了吗？
  - 架构变更了 → `docs/architecture.md` 更新了吗？
  - 变更违反了 `docs/invariants.md`？→ CRITICAL
  - 文档未更新 → HIGH（文档漂移是团队级风险）
- **不变量驱动审查**:
  - 依据 `docs/invariants.md` 审查；反复出现的 Bug 模式 → 建议自动化测试（`[INV-TEST] P0/P1/P2`）
  - 目标：reviewer = 第二道防线，自动化测试 = 第一道
- **架构健康检查** (MEDIUM 级别):
  - 浅层模块：接口复杂度 ≈ 实现复杂度 → 建议深化
  - 依赖分类：进程内 / 本地可替换 / 远程但自有 / 真正外部
  - 测试策略：如果边界测试已存在，标记冗余的浅层单元测试可以删除
- **审批标准**:
  - [OK] 通过：无 CRITICAL 或 HIGH
  - [WARN] 警告：仅有 MEDIUM（可合并但需注意）
  - [BLOCK] 阻断：有 CRITICAL 或 HIGH 问题
- **输出**: 完整审查写入自己的 `review-<target>/findings.md`；摘要 + 链接发送给请求方 dev 和 team-lead
- **文档结构**:
  - 每次审查 → 创建 `review-<target>/` 子文件夹（含 findings.md + progress.md）
  - findings.md 包含完整审查报告（问题清单、严重度、修复建议）
  - 根 findings.md 作为**索引**，链接到各次审查
  - reviewer 还会在请求方 dev 的任务 findings.md 中追加一行简要摘要和交叉引用链接

---

### 代码清理 (cleaner)

- **名称**: `cleaner`
- **subagent_type**: `general-purpose`
- **model**: `sonnet`
- **参考**: refactor-cleaner 智能体（死代码清理 + 安全重构）
- **核心职责**:
  - 识别和删除死代码（未使用的导入、变量、函数、文件）
  - 合并重复代码为共享工具函数
  - 清理技术债务
  - **文档新鲜度扫描**：验证 `docs/` 文件与实际代码一致（API 路由、架构、环境变量）
  - **每次删除前必须验证**，每次删除后必须跑测试
- **何时运行**: 不只是在项目结束时。在每个阶段**开始时**运行文档新鲜度扫描（可与其他任务并行）。Cleaner 是团队的**文档园丁**
- **四阶段流程** (来自 refactor-cleaner):
  1. **分析**：运行检测工具（knip、depcheck、ts-prune），按风险分类（Safe/Careful/Risky）
  2. **验证**：Grep 确认无引用、不是公共 API、不是动态导入
  3. **安全删除**：小批次（5-10 项）删除，每批后跑测试 + 构建
  4. **合并**：提取重复模式为共享函数，更新所有引用
- **安全检查清单**:
  - [ ] 检测工具确认未使用
  - [ ] Grep 搜索无任何引用
  - [ ] 不是公共 API 或接口的一部分
  - [ ] 不是动态导入
  - [ ] 不在测试中使用
  - [ ] 删除后测试通过
  - [ ] 删除后构建成功
- **禁止使用场景**: 活跃功能开发中、生产部署前、没有足够测试覆盖时
- **文档结构**: 不使用任务子文件夹

---

## 模型选择指南

| 复杂度 | 模型 | 使用场景 |
|--------|------|---------|
| 中等（搜索、调研、架构分析） | sonnet | researcher（只读搜索 + 深度分析） |
| 中等（测试编写、模式化操作） | sonnet | e2e-tester、cleaner |
| 高（写业务代码、安全审查） | opus | backend-dev、frontend-dev、reviewer（需要深度推理和全局理解） |

## 通用行为协议（所有角色必须遵守）

以下规则在 [onboarding.md](onboarding.md) 通用模板中定义，所有角色的入职 prompt 都包含：

| 协议 | 核心要求 | 来源 |
|------|---------|------|
| **2-Action Rule** | 每 2 次搜索/读取后，必须立刻写 findings.md | Manus 上下文工程 |
| **重大决策前读计划** | 做决策前先读 task_plan.md，刷新注意力窗口中的目标 | Manus Principle 4 |
| **3-Strike 错误协议** | 3次相同错误后上报 team-lead，不静默重试 | Manus 错误恢复 |
| **上下文恢复** | 压缩后必须先读 task_plan.md → findings.md → progress.md | planning-with-files |
| **模板同步上报** | 如果发现可复用的团队流程改进，记录并通知 team-lead，由其判断是项目级还是模板级 | 团队系统维护 |

## 自定义角色

用户可添加自定义角色，遵循以下格式：

| 字段 | 必需 | 描述 |
|------|------|------|
| 名称 | 是 | kebab-case，用于 SendMessage `to:` 和任务 `owner:` |
| subagent_type | 是 | 必须匹配可用的智能体类型（注意工具限制，见下表） |
| model | 是 | haiku / sonnet / opus |
| 参考 | 否 | 参考哪个内置智能体的方法论 |
| 核心职责 | 是 | 具体做什么 |
| 文档结构 | 是 | 是否需要按 task 分文件夹 |

### subagent_type 工具限制速查

| subagent_type | 可用工具 | 适合角色 |
|---------------|---------|---------|
| `general-purpose` | 所有工具（Read/Write/Edit/Bash/Grep/Glob/...） | 需要写文件的角色（dev, reviewer, tester, cleaner） |
| `Explore` | 只读工具（Read/Grep/Glob，无 Write/Edit） | 纯只读调研（但注意：无法写 findings.md） |
| `code-reviewer` | Read/Grep/Glob/Bash（无 Write/Edit） | 纯只读审查（但注意：无法写 findings.md） |

**关键**：所有团队角色都需要维护自己的 .plans/ 文件（progress.md, findings.md），因此通常选 `general-purpose`，通过 prompt 约束行为边界。
