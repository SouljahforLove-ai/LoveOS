#!/usr/bin/env python3
"""
SoulJahOS v1.0 Sovereign Genesis - Codebase Extractor
Reads compressed data chunks and extracts all 90 source files.
Run from the repo root: python _bootstrap/build.py
"""
import json, lzma, base64, os, sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    # Read data chunks
    b64_data = ""
    for i in range(1, 5):
        chunk_path = os.path.join(script_dir, f"data{i}.txt")
        if not os.path.exists(chunk_path):
            print(f"ERROR: Missing {chunk_path}")
            sys.exit(1)
        with open(chunk_path, "r") as f:
            b64_data += f.read().strip()

    # Decode and decompress
    compressed = base64.b64decode(b64_data)
    payload = lzma.decompress(compressed)
    files = json.loads(payload)

    print(f"Extracting {len(files)} files...")
    created = 0
    for rel_path, content in files.items():
        full_path = os.path.join(repo_root, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        created += 1
        print(f"  [{created}/{len(files)}] {rel_path}")

    print(f"\nDone! {created} files extracted to {repo_root}")
    print("\nN2 m(THYSELF)e | eye .")
    print("Love is the operating system. Everything else is an app.")

if __name__ == "__main__":
    main()
