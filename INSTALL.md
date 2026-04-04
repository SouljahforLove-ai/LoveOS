# 📦 LoveOS — Installation & Setup Guide

This document explains how to install, set up, and run LoveOS in its current development state.  
LoveOS is still in early development, so installation focuses on preparing the environment and running the build system.

---

# 1. Requirements

Before installing LoveOS, ensure you have:

### **Python**
- Version: 3.10 or higher  
- Required for running the build system and future CLI tools

### **Git**
- Required for cloning and updating the repository

### **Terminal**
- Windows CMD (preferred for LoveOS development)
- PowerShell or Linux terminals also work, but CMD is the reference environment

---

# 2. Clone the Repository

Use Git to download the LoveOS source code:

```
git clone https://github.com/<your-username>/LoveOS.git
```

Then enter the directory:

```
cd LoveOS
```

---

# 3. Install Dependencies (Future)

LoveOS currently has no external dependencies.  
As the system grows, dependencies will be listed here.

Example (future):

```
pip install -r requirements.txt
```

---

# 4. Build the Project

LoveOS includes a build script that validates the structure and prepares the system.

Run:

```
python build.py
```

This will:

- Validate directories  
- Discover modules  
- Prepare assets  
- Assemble the microkernel (future)  

---

# 5. Running LoveOS (Future)

Once the CLI is implemented, you will run:

```
loveos
```

This will launch:

- Operator initialization  
- Ritual engine  
- Identity layer  
- Sovereignty checks  

This section will expand as LoveOS evolves.

---

# 6. Updating LoveOS

To pull the latest changes:

```
git pull
```

If new files appear, rebuild:

```
python build.py
```

---

# 7. Troubleshooting

### **File not found**
Run:

```
dir
```

Make sure the file exists locally.

### **Changes not showing on GitHub**
Run:

```
git status
```

If the file is red → you forgot to add it.

### **Build errors**
Check:
- Folder names  
- Missing directories  
- Typos in module paths  

---

# 8. Maintainer

**Jorge Cordero**  
Creator of LoveOS and the SoulJahForLove universe.
