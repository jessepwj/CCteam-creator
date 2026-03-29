#!/usr/bin/env python3
"""
Golden Rules -- universal code health checks for CCteam-creator projects.

Pre-installed by CCteam-creator skill. Copied to <project>/scripts/ during
Step 3.6 (Harness Setup). Called by run_ci.py as part of the CI pipeline.

Usage:
    # Standalone
    python golden_rules.py src/backend src/frontend

    # From run_ci.py
    from golden_rules import check_all
    result = check_all(["src/backend", "src/frontend"], docs_dir=".plans/<project>/docs")

Error messages follow agent-readable format:
    [TAG] <what's wrong>
      File: <path:line>
      FIX: <exactly how to fix it>
"""
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Result collector (no global mutable state)
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
# Shared helpers
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
    """Yield Path objects for code files in src_dirs, skipping excluded dirs and minified files."""
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
            # Skip minified files (e.g., foo.min.js)
            if ".min." in f.name:
                continue
            yield f


# ---------------------------------------------------------------------------
# GR-1: File Size
# ---------------------------------------------------------------------------
def check_file_size(src_dirs, result, warn_limit=800, fail_limit=1200):
    """Files over warn_limit lines get WARN; over fail_limit get FAIL."""
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
# GR-2: Hardcoded Secrets
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    (r"""['"]sk-[a-zA-Z0-9]{20,}['"]""", "Possible OpenAI/Stripe API key"),
    (r"""['"]ghp_[a-zA-Z0-9]{30,}['"]""", "Possible GitHub personal access token"),
    (r"""['"]AKIA[A-Z0-9]{16}['"]""", "Possible AWS access key"),
    (r"""(?i)(password|secret|api_key|apikey|token)\s*[:=]\s*['"][^'"]{8,}['"]""",
     "Possible hardcoded secret"),
]

# Lines containing these markers are likely examples/placeholders, not real secrets
EXAMPLE_MARKERS = ("example", "placeholder", "your_key_here", "xxx", "changeme", "<your")


def check_secrets(src_dirs, result):
    """Scan for hardcoded secrets using regex patterns."""
    print("[GR-2] Hardcoded Secrets Check")
    found = False
    for f in _iter_code_files(src_dirs):
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            # Skip lines that are clearly examples/placeholders
            if any(marker in stripped.lower() for marker in EXAMPLE_MARKERS):
                continue
            for pattern, desc in SECRET_PATTERNS:
                if re.search(pattern, line):
                    result.fail("GR-SECRET", f"{f}:{i} -- {desc}",
                                "Move to environment variable. Never commit secrets to code.")
                    found = True
                    break  # one match per line is enough
    if not found:
        print("  [OK] No hardcoded secrets detected.\n")


# ---------------------------------------------------------------------------
# GR-3: No console.log in Production Code
# ---------------------------------------------------------------------------
CONSOLE_PATTERN = re.compile(r"\bconsole\.(log|debug|info|warn|error)\b")
TEST_DIR_NAMES = {"test", "tests", "__tests__", "spec", "scripts", "e2e", "cypress"}


def check_console_log(src_dirs, result):
    """Detect console.log in production code (not test files)."""
    print("[GR-3] Console Log Check")
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
                            "Remove console.log from production code. Use a structured logger instead.")
                found = True
    if not found:
        print("  [OK] No console.log in production code.\n")


# ---------------------------------------------------------------------------
# GR-4: Doc Freshness (requires git)
# ---------------------------------------------------------------------------
def check_doc_freshness(docs_dir, src_dirs, result, stale_commit_threshold=10):
    """Compare docs/ last-modified commit vs source code commits.

    If source has N+ commits since docs were last touched, emit WARN.
    Requires git. Silently skips if git is not available or docs_dir missing.
    """
    print("[GR-4] Doc Freshness Check")
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        print("  [SKIP] docs/ directory not found. Skipping freshness check.\n")
        return

    doc_files = {
        "api-contracts.md": "API contract",
        "architecture.md": "architecture",
        "invariants.md": "invariants",
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
                    f"{doc_file} -- {src_commits} source commits since last doc update",
                    f"Review and update {label} docs. Run: git log --oneline {last_doc_commit}..HEAD -- {quoted_dirs}")
                found = True
        except Exception:
            continue

    if not found:
        print("  [OK] All docs appear fresh.\n")


# ---------------------------------------------------------------------------
# GR-5: Invariant Coverage
# ---------------------------------------------------------------------------
def check_invariant_coverage(docs_dir, result):
    """Scan invariants.md for items marked 'no test' and report them."""
    print("[GR-5] Invariant Coverage Check")
    inv_file = Path(docs_dir) / "invariants.md"
    if not inv_file.exists():
        print("  [SKIP] docs/invariants.md not found. Skipping.\n")
        return

    try:
        content = inv_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        print("  [SKIP] Could not read invariants.md.\n")
        return

    no_test_count = 0
    for i, line in enumerate(content.splitlines(), 1):
        if re.search(r"(?i)status:\s*no\s*test", line):
            result.info(
                "GR-INV-NO-TEST",
                f"docs/invariants.md:{i} -- Invariant without automated test: {line.strip()[:80]}",
                "Write an automated test for this invariant. Untested invariants rely on human memory.")
            no_test_count += 1

    if no_test_count == 0:
        print("  [OK] All invariants have test coverage (or no invariants defined).\n")
    else:
        print(f"  {no_test_count} invariant(s) without automated tests.\n")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def check_all(src_dirs, docs_dir=None):
    """Run all golden rule checks. Returns (fail_count, warn_count, info_count)."""
    result = CheckResult()

    print("=" * 60)
    print("Golden Rules Check")
    print("=" * 60 + "\n")

    check_file_size(src_dirs, result)
    check_secrets(src_dirs, result)
    check_console_log(src_dirs, result)

    if docs_dir:
        check_doc_freshness(docs_dir, src_dirs, result)
        check_invariant_coverage(docs_dir, result)

    print("=" * 60)
    print(f"Golden Rules Summary: {result.fails} FAIL, {result.warns} WARN, {result.infos} INFO")
    if result.fails > 0:
        print("Result: FAILED -- fix FAIL items before proceeding.")
    elif result.warns > 0:
        print("Result: PASSED with warnings -- review WARN items.")
    else:
        print("Result: PASSED")
    print("=" * 60)

    return result.fails, result.warns, result.infos


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python golden_rules.py <src_dir1> [src_dir2] ... [--docs <docs_dir>]")
        print("Example: python golden_rules.py src/ --docs .plans/myproject/docs")
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
