import os

def scan(path):
    return [
        f for f in os.listdir(path)
        if f.endswith(".py")
    ]

print("=== LoveOS Build ===")

print("\n[Kernel]")
print(scan("kernel"))

print("\n[Engines]")
for item in os.listdir("engines"):
    full = os.path.join("engines", item)
    if os.path.isdir(full):
        print(f"{item}: {scan(full)}")

print("\n[Rituals]")
for item in os.listdir("rituals"):
    full = os.path.join("rituals", item)
    if os.path.isdir(full):
        print(f"{item}: {scan(full)}")

print("\n[OK] LoveOS is alive.")
