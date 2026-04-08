# 🏗️ SoulJahOS — Building From Source

This document explains how to build SoulJahOS from source during its early development phase.  
The build system validates structure, discovers modules, and prepares the microkernel for future expansion.

---

# 1. Requirements

Before building SoulJahOS, ensure you have:

### Python
- Version 3.10 or higher

### Git
- Required for cloning and updating the repository

### Terminal
- Windows CMD (reference environment for SoulJahOS development)

---

# 2. Repository Structure Requirements

The build system expects the following directories to exist:

```
kernel/
engines/
operators/
rituals/
config/
assets/
docs/
```

If any of these are missing, the build script will warn you or fail.

---

# 3. Running the Build Script

To build SoulJahOS, run:

```
python build.py
```

The script performs:

### 1. Directory Validation
Ensures required folders exist.

### 2. Module Discovery
Scans:

- `/kernel/`
- `/engines/`
- `/operators/`
- `/rituals/`

### 3. Asset Preparation
Prepares:

- Sigils  
- UI elements  
- Future sound cues  

### 4. Kernel Assembly (Future)
Will eventually:

- Register engines  
- Initialize identity constants  
- Prepare ritual dispatcher  
- Build sovereignty checks  

---

# 4. Adding New Modules

When adding a new module, follow this structure:

```
engines/
    emotional/
        __init__.py
        metrics.py
        transitions.py
```

Or for rituals:

```
rituals/
    grounding/
        breathe.py
        reset.py
```

The build script will automatically detect:

- New folders  
- New modules  
- New rituals  

As long as they follow the directory map.

---

# 5. Build Errors & Fixes

### **Missing Directory**
Error:
```
Directory not found: engines/
```
Fix:
```
mkdir engines
```

### **Module Not Detected**
Cause:
- Wrong folder name  
- Missing `__init__.py` (future requirement)  
- File placed in the wrong directory  

### **Python Errors**
Fix:
- Check syntax  
- Check indentation  
- Check file names  

---

# 6. Rebuilding After Changes

Whenever you add or modify modules:

```
python build.py
```

If you pull new changes from GitHub:

```
git pull
python build.py
```

---

# 7. Future Build Features

The build system will eventually support:

- Kernel compilation  
- Engine registration  
- Ritual sequencing  
- Identity signature verification  
- CLI bundling  
- Release packaging  

---

# 8. Maintainer

**Jorge Cordero**  
Creator of LoveOS and the SoulJahForLove universe.
