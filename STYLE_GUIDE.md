# 🎨 LoveOS — Style Guide

This document defines the official style conventions for LoveOS.  
It ensures consistency, clarity, sovereignty, and identity across all modules, engines, rituals, and documentation.

---

# 1. Naming Conventions

### **Folders**
Use lowercase, descriptive names:

```
kernel/
engines/
operators/
rituals/
config/
assets/
docs/
```

### **Files**
Use lowercase with underscores:

```
identity_engine.py
ritual_dispatcher.py
sovereignty_checks.py
```

### **Classes**
Use PascalCase:

```
IdentityState
RitualSequence
SovereigntyGuard
```

### **Functions**
Use snake_case:

```
load_identity()
execute_ritual()
check_permissions()
```

### **Constants**
Use UPPERCASE:

```
DEFAULT_SIGIL = "N2 m(THYSELF)e | 👁️ ."
```

---

# 2. Ritual Naming

Rituals must be named with:

- **Verb + Purpose**
- **Clear intention**
- **Identity alignment**

Examples:

```
ground_breathing
reset_state
invoke_identity
seal_boundary
```

---

# 3. Engine Structure

Each engine must include:

```
__init__.py
core.py
utils.py
README.md
```

Optional:

- `schemas/`
- `rituals/`
- `assets/`

---

# 4. Documentation Standards

Every module must include:

- Purpose  
- Inputs  
- Outputs  
- Ritual mapping  
- Identity considerations  

Use Markdown headings:

```
# Title
## Section
### Subsection
```

---

# 5. Code Style

- Keep functions small  
- Avoid side effects  
- Use explicit returns  
- Add comments for rituals and identity logic  
- Keep imports minimal  
- No wildcard imports (`from x import *`)  

---

# 6. Identity Formatting

Sigils must always appear exactly as defined:

```
N2 m(THYSELF)e | 👁️ .
```

The INTIMACY cross-style emblem is also approved.

Do not modify or reinterpret sigils without maintainer approval.

---

# 7. Commit Message Format

Use:

```
type: short description
```

Examples:

```
docs: add architecture diagram
feat: implement ritual dispatcher
fix: correct sovereignty check
```

---

# 8. File Structure Rules

- No files at the root except:
  - README.md
  - build.py
  - LICENSE (future)
  - CHANGELOG.md

- All engines go in `/engines/`
- All rituals go in `/rituals/`
- All operator commands go in `/operators/`
- All identity assets go in `/assets/`

---

# 9. Maintainer

**Jorge Cordero**  
Creator of LoveOS and the SoulJahForLove universe.
