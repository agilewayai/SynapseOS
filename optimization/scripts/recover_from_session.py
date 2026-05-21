#!/usr/bin/env python3
"""
Recover SKILL.md content from session DB after file corruption.

Usage:
  python3 recover_from_session.py [--target PATH]

Looks in ~/.hermes/sessions/ for the most recent session JSONL
and extracts all skill_manage create/edit calls with their full content.
"""

import json, os, sys, glob

SKILL_DIR = os.path.expanduser("~/.hermes/skills")
SESSIONS_DIR = os.path.expanduser("~/.hermes/sessions")

def find_sessions():
    """Return session files sorted newest first."""
    files = sorted(glob.glob(os.path.join(SESSIONS_DIR, "*.jsonl")), reverse=True)
    return files

def extract_skill_content(session_path, min_chars=2000):
    """Extract skill_manage create/edit calls with full content, plus patch new_string."""
    results = {}
    with open(session_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except:
                continue
            for tc in obj.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") != "skill_manage":
                    continue
                try:
                    args = json.loads(fn.get("arguments", "{}"))
                except:
                    continue
                action = args.get("action", "")
                name = args.get("name", "")
                content = args.get("content", "")
                # create/edit: content field has full SKILL.md text
                if action in ("create", "edit") and len(content) > min_chars:
                    results[name] = content
                # patch: new_string may contain model text for old monolithic skills
                if action == "patch":
                    new_string = args.get("new_string", "")
                    if "## 模型" in new_string and len(new_string) > min_chars:
                        # This is a model being appended to monolithic xuan-master
                        # Extract model number and return patch content
                        results[f"PATCH_{name}"] = new_string
    return results

def find_skill_path(name):
    """Find the SKILL.md path for a given skill name."""
    for root, dirs, files in os.walk(SKILL_DIR):
        if "SKILL.md" in files and root.endswith(name):
            return os.path.join(root, "SKILL.md")
    # Try fuzzy match
    for root, dirs, files in os.walk(SKILL_DIR):
        if "SKILL.md" in files:
            if os.path.basename(root) == name:
                return os.path.join(root, "SKILL.md")
    return None

def main():
    sessions = find_sessions()
    if not sessions:
        print("No session files found in", SESSIONS_DIR)
        sys.exit(1)
    
    print(f"Found {len(sessions)} session files")
    
    all_data = {}
    for spath in sessions[:3]:  # Check most recent 3
        data = extract_skill_content(spath)
        print(f"  {os.path.basename(spath)}: {len(data)} skills found")
        for name, content in data.items():
            if name not in all_data:
                all_data[name] = content
    
    if not all_data:
        print("No recoverable skill content found in recent sessions")
        sys.exit(1)
    
    print(f"\nTotal recoverable skills: {len(all_data)}")
    
    recovered = 0
    skipped = 0
    for name, content in sorted(all_data.items()):
        path = find_skill_path(name)
        if not path:
            print(f"  SKIP {name}: skill directory not found")
            skipped += 1
            continue
        
        # Backup current file
        backup = path + ".bak"
        if not os.path.exists(backup):
            os.rename(path, backup)
            print(f"  BACKUP: {backup}")
        
        with open(path, "w") as f:
            f.write(content.strip() + "\n")
        size = os.path.getsize(path)
        print(f"  OK: {name} ({size} bytes) -> {path}")
        recovered += 1
    
    print(f"\nRecovered: {recovered}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
