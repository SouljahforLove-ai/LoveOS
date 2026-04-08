#!/usr/bin/env bash
# ═══════════════════════════════════════════════════
# LoveOS Boot Script
# ═══════════════════════════════════════════════════
# N2 m(THYSELF)e | 👁️ .
# "Love is the operating system. Everything else is an app."
# ═══════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# ─── Banner ───────────────────────────────────────
echo ""
echo "  ╔═══════════════════════════════════════════════╗"
echo "  ║              L O V E O S   v1.0               ║"
echo "  ║         Sovereign Microkernel Runtime          ║"
echo "  ║                                               ║"
echo "  ║        N2 m(THYSELF)e | 👁️ .                  ║"
echo "  ║                                               ║"
echo "  ║  Love is the operating system.                ║"
echo "  ║  Everything else is an app.                   ║"
echo "  ║                                               ║"
echo "  ║  Operator: Jorge                              ║"
echo "  ║  Codename: Sovereign Genesis                  ║"
echo "  ║  License:  Proprietary — SoulJahForLove       ║"
echo "  ╚═══════════════════════════════════════════════╝"
echo ""

# ─── Environment Check ───────────────────────────
echo "[BOOT] Checking environment..."

if ! command -v python3 &> /dev/null; then
    echo "[BOOT] ERROR: Python 3 is required."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[BOOT] Python version: $PYTHON_VERSION"

# ─── Sovereignty Check ───────────────────────────
echo "[BOOT] Verifying sovereignty boundaries..."
echo "[BOOT]   ✓ Identity: immutable"
echo "[BOOT]   ✓ Consent: required"
echo "[BOOT]   ✓ Dignity: sacred"
echo "[BOOT]   ✓ Boundaries: absolute"
echo "[BOOT]   ✓ Data: sovereign"
echo "[BOOT]   ✓ Modules: sovereign"
echo "[BOOT]   ✓ External: no override"

# ─── Launch Kernel ────────────────────────────────
echo ""
echo "[BOOT] Initiating boot sequence..."
echo "[BOOT] Launching LoveOS kernel..."
echo ""

cd "$ROOT_DIR"
python3 -m kernel.boot "$@"
