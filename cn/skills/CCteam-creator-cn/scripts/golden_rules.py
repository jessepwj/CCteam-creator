#!/usr/bin/env python3
"""
黄金规则 -- CCteam-creator 项目的通用代码质量检查工具。

由 CCteam-creator 技能预安装，在步骤 3.6（工具链配置）时复制到 <project>/scripts/ 目录。
作为 CI 管道的一部分，由 run_ci.py 调用执行。

使用方式：
    # 独立运行
    python golden_rules.py src/backend src/frontend

    # 从 run_ci.py 调用
    from golden_rules import check_all
    result = check_all(["src/backend", "src/frontend"], docs_dir=".plans/<project>/docs")

错误消息遵循代理可读的格式：
    [TAG] <问题描述>
      File: <路径:行号>
      FIX: <具体修复方案>
"""
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# 结果收集器（无全局可变状态）
# ---------------------------------------------------------------------------


@dataclass
class CheckResult:
    fails: int = 0
    warns: int = 0
    infos: int = 0

    def fail(self, tag, msg, fix):
        self.fails += 1
        print(f"  [FAIL] [{tag}] {msg}")
        print(f"    FIX: {fix}\n")

    def warn(self, tag, msg, fix):
        self.warns += 1
        print(f"  [WARN] [{tag}] {msg}")
        print(f"    FIX: {fix}\n")

    def info(self, tag, msg, fix):
        self.infos += 1
        print(f"  [INFO] [{tag}] {msg}")
        print(f"    FIX: {fix}\n")


# ---------------------------------------------------------------------------
# 共享的辅助函数
# ---------------------------------------------------------------------------
CODE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte",
    ".go", ".rs", ".java", ".kt", ".rb", ".php",
}

EXCLUDE_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", ".nuxt", "coverage", ".plans",
}


def _iter_code_files(src_dirs):
    """遍历源目录中的代码文件，跳过排除目录和压缩文件。"""
    for src_dir in src_dirs:
        root = Path(src_dir)
        if not root.exists():
            continue
        for f in root.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix not in CODE_EXTENSIONS:
                continue
            if any(part in EXCLUDE_DIRS for part in f.parts):
                continue
            # 跳过压缩文件（如 foo.min.js）
            if ".min." in f.name:
                continue
            yield f


# ---------------------------------------------------------------------------
# GR-1: 文件大小检查
# ---------------------------------------------------------------------------
def check_file_size(src_dirs, result, warn_limit=800, fail_limit=1200):
    """文件行数超过 warn_limit 发出警告；超过 fail_limit 则失败。"""
    print("[GR-1] File Size Check")
    found = False
    for f in _iter_code_files(src_dirs):
        try:
            lines = len(f.read_text(encoding="utf-8", errors="ignore").splitlines())
        except Exception:
            continue
        if lines > fail_limit:
            result.fail("GR-FILE-SIZE", f"{f} -- {lines} lines (limit: {fail_limit})",
                        "Split into smaller modules. Extract helper functions or classes.")
            found = True
        elif lines > warn_limit:
            result.warn("GR-FILE-SIZE", f"{f} -- {lines} lines (limit: {warn_limit})",
                        "Consider splitting. Files over 800 lines are hard for agents to navigate.")
            found = True
    if not found:
        print("  [OK] All files within size limits.\n")


# ---------------------------------------------------------------------------
# GR-2: 硬编码秘密检查
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    (r"""['"]sk-[a-zA-Z0-9]{20,}['"]""", "Possible OpenAI/Stripe API key"),
    (r"""['"]ghp_[a-zA-Z0-9]{30,}['"]""", "Possible GitHub personal access token"),
    (r"""['"]AKIA[A-Z0-9]{16}['"]""", "Possible AWS access key"),
    (r"""(?i)(password|secret|api_key|apikey|token)\s*[:=]\s*['"][^'"]{8,}['"]""",
     "Possible hardcoded secret"),
]

# 包含这些标记的行可能是示例/占位符，不是真实秘密
EXAMPLE_MARKERS = ("example", "placeholder", "your_key_here", "xxx", "changeme", "<your")


def check_secrets(src_dirs, result):
    """使用正则表达式模式扫描硬编码的秘密。"""
    print("[GR-2] Hardcoded Secrets Check")
    found = False
    for f in _iter_code_files(src_dirs):
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            # 跳过明显的示例/占位符行
            if any(marker in stripped.lower() for marker in EXAMPLE_MARKERS):
                continue
            for pattern, desc in SECRET_PATTERNS:
                if re.search(pattern, line):
                    result.fail("GR-SECRET", f"{f}:{i} -- {desc}",
                                "转移到环境变量。永远不要在代码中提交秘密。")
                    found = True
                    break  # 每行一个匹配就够了
    if not found:
        print("  [OK] No hardcoded secrets detected.\n")


# ---------------------------------------------------------------------------
# GR-3: 生产代码中无 console.log 检查
# ---------------------------------------------------------------------------
CONSOLE_PATTERN = re.compile(r"\bconsole\.(log|debug|info|warn|error)\b")
TEST_DIR_NAMES = {"test", "tests", "__tests__", "spec", "scripts", "e2e", "cypress"}


def check_console_log(src_dirs, result):
    """检测生产代码中的 console.log（排除测试文件）。"""
    print("[GR-3] Console Log 检查")
    found = False
    for f in _iter_code_files(src_dirs):
        if f.suffix not in {".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte"}:
            continue
        if any(part in TEST_DIR_NAMES for part in f.parts):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(content.splitlines(), 1):
            if CONSOLE_PATTERN.search(line):
                stripped = line.strip()
                if stripped.startswith("//"):
                    continue
                result.warn("GR-CONSOLE", f"{f}:{i} -- {stripped[:80]}",
                            "从生产代码中移除 console.log。使用结构化日志记录器代替。")
                found = True
    if not found:
        print("  [OK] No console.log in production code.\n")


# ---------------------------------------------------------------------------
# GR-4: 文档新鲜度检查（需要 git）
# ---------------------------------------------------------------------------
def check_doc_freshness(docs_dir, src_dirs, result, stale_commit_threshold=10):
    """比较 docs/ 最后修改的提交与源代码提交。

    如果源代码自上次更新文档后有 N+ 个提交，则发出警告。
    需要 git。如果 git 不可用或 docs_dir 不存在则静默跳过。
    """
    print("[GR-4] 文档新鲜度检查")
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        print("  [SKIP] 未找到 docs/ 目录。跳过新鲜度检查。\n")
        return

    doc_files = {
        "api-contracts.md": "API 契约",
        "architecture.md": "架构",
        "invariants.md": "不变量",
    }

    found = False
    for doc_name, label in doc_files.items():
        doc_file = docs_path / doc_name
        if not doc_file.exists():
            continue
        try:
            last_doc_commit = subprocess.run(
                ["git", "log", "-1", "--format=%H", "--", str(doc_file)],
                capture_output=True, text=True, timeout=10
            ).stdout.strip()

            if not last_doc_commit:
                continue

            src_commits = 0
            for src_dir in src_dirs:
                if not Path(src_dir).exists():
                    continue
                count_result = subprocess.run(
                    ["git", "rev-list", "--count", f"{last_doc_commit}..HEAD", "--", src_dir],
                    capture_output=True, text=True, timeout=10
                )
                count = count_result.stdout.strip()
                if count.isdigit():
                    src_commits += int(count)

            if src_commits >= stale_commit_threshold:
                quoted_dirs = " ".join(f'"{d}"' for d in src_dirs)
                result.warn(
                    "GR-DOC-STALE",
                    f"{doc_file} -- 上次更新文档后有 {src_commits} 个源代码提交",
                    f"查看并更新 {label} 文档。运行：git log --oneline {last_doc_commit}..HEAD -- {quoted_dirs}")
                found = True
        except Exception:
            continue

    if not found:
        print("  [OK] 所有文档看起来是最新的。\n")


# ---------------------------------------------------------------------------
# GR-5: 不变量测试覆盖率检查
# ---------------------------------------------------------------------------
def check_invariant_coverage(docs_dir, result):
    """扫描 invariants.md 文件中标记为"无测试"的项目并报告。"""
    print("[GR-5] 不变量覆盖率检查")
    inv_file = Path(docs_dir) / "invariants.md"
    if not inv_file.exists():
        print("  [SKIP] 未找到 docs/invariants.md。跳过。\n")
        return

    try:
        content = inv_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        print("  [SKIP] 无法读取 invariants.md。\n")
        return

    no_test_count = 0
    for i, line in enumerate(content.splitlines(), 1):
        if re.search(r"(?i)status:\s*no\s*test", line):
            result.info(
                "GR-INV-NO-TEST",
                f"docs/invariants.md:{i} -- 没有自动化测试的不变量：{line.strip()[:80]}",
                "为此不变量编写自动化测试。未经测试的不变量依赖人工记忆。")
            no_test_count += 1

    if no_test_count == 0:
        print("  [OK] 所有不变量都有测试覆盖（或没有定义不变量）。\n")
    else:
        print(f"  {no_test_count} 个不变量没有自动化测试。\n")


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------
def check_all(src_dirs, docs_dir=None):
    """运行所有黄金规则检查。返回（失败数, 警告数, 信息数）。"""
    result = CheckResult()

    print("=" * 60)
    print("黄金规则检查")
    print("=" * 60 + "\n")

    check_file_size(src_dirs, result)
    check_secrets(src_dirs, result)
    check_console_log(src_dirs, result)

    if docs_dir:
        check_doc_freshness(docs_dir, src_dirs, result)
        check_invariant_coverage(docs_dir, result)

    print("=" * 60)
    print(f"黄金规则汇总：{result.fails} 个失败，{result.warns} 个警告，{result.infos} 个信息")
    if result.fails > 0:
        print("结果：失败 -- 继续之前修复失败项。")
    elif result.warns > 0:
        print("结果：通过，有警告 -- 查看警告项。")
    else:
        print("结果：通过")
    print("=" * 60)

    return result.fails, result.warns, result.infos


# ---------------------------------------------------------------------------
# CLI 入口点
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python golden_rules.py <src_dir1> [src_dir2] ... [--docs <docs_dir>]")
        print("示例：python golden_rules.py src/ --docs .plans/myproject/docs")
        sys.exit(2)

    args = sys.argv[1:]
    docs = None
    src = []
    i = 0
    while i < len(args):
        if args[i] == "--docs" and i + 1 < len(args):
            docs = args[i + 1]
            i += 2
        else:
            src.append(args[i])
            i += 1

    fails, warns, infos = check_all(src, docs_dir=docs)
    sys.exit(1 if fails > 0 else 0)
