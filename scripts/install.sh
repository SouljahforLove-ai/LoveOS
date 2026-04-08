#!/usr/bin/env bash
# ═══════════════════════════════════════════════════
# LoveOS Installation Script
# ═══════════════════════════════════════════════════
# N2 m(THYSELF)e | 👁️ .
# ═══════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo "  ╔═══════════════════════════════════════════════╗"
echo "  ║         L O V E O S   I N S T A L L E R       ║"
echo "  ║         Sovereign Microkernel Runtime          ║"
echo "  ╚═══════════════════════════════════════════════╝"
echo ""

# ─── Check Python ─────────────────────────────────
echo "[INSTALL] Checking Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "[INSTALL] ERROR: Python 3 is required."
    echo "[INSTALL] Install Python 3.10+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "[INSTALL] ERROR: Python 3.10+ required, found $PYTHON_VERSION"
    exit 1
fi
echo "[INSTALL] ✓ Python $PYTHON_VERSION"

# ─── Verify Repository Structure ──────────────────
echo "[INSTALL] Verifying repository structure..."

REQUIRED_DIRS=(
    "kernel" "engines" "schemas" "modules" "processors"
    "guards" "dispatchers" "registry" "maps" "rituals"
    "patterns" "permissions" "integration" "config"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$ROOT_DIR/$dir" ]; then
        echo "[INSTALL]   ✓ $dir/"
    else
        echo "[INSTALL]   ✗ $dir/ — MISSING"
        exit 1
    fi
done

# ─── Create Virtual Environment (optional) ────────
if [ "${LOVEOS_VENV:-0}" = "1" ]; then
    echo "[INSTALL] Creating virtual environment..."
    python3 -m venv "$ROOT_DIR/.venv"
    source "$ROOT_DIR/.venv/bin/activate"
    echo "[INSTALL] ✓ Virtual environment created at .venv/"
fi

# ─── Verify Core Files ────────────────────────────
echo "[INSTALL] Verifying core files..."
CORE_FILES=(
    "kernel/microkernel.py"
    "kernel/boot.py"
    "kernel/sovereignty.py"
    "kernel/syscalls.py"
    "config/default_config.yaml"
    "README.md"
)

for f in "${CORE_FILES[@]}"; do
    if [ -f "$ROOT_DIR/$f" ]; then
        echo "[INSTALL]   ✓ $f"
    else
        echo "[INSTALL]   ✗ $f — MISSING"
        exit 1
    fi
done

# ─── Run Syntax Check ─────────────────────────────
echo "[INSTALL] Running syntax check..."
python3 -c "
import py_compile, os, sys
errors = []
for root, dirs, files in os.walk('$ROOT_DIR'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            try:
                py_compile.compile(path, doraise=True)
            except py_compile.PyCompileError as e:
                errors.append(str(e))
if errors:
    for e in errors:
        print(f'[INSTALL]   ✗ {e}', file=sys.stderr)
    sys.exit(1)
print('[INSTALL]   ✓ All Python files pass syntax check')
"

# ─── Complete ──────────────────────────────────────
echo ""
echo "[INSTALL] ═══════════════════════════════════════════"
echo "[INSTALL]   LoveOS installation verified."
echo "[INSTALL]   Run: bash scripts/boot.sh"
echo "[INSTALL] ═══════════════════════════════════════════"
echo ""
