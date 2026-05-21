#!/usr/bin/env python3
"""
Xuan-Master Full Family Audit Script

Usage:
    python3 full_audit.py [--verbose] [--summary-only]

Scans all 27 models and produces a report with:
    - Frontmatter integrity
    - Section completeness (7 standard sections)
    - Content quality (blockquotes, reflection, cross-model refs)
    - Size distribution
    - Priority findings (P0/P1/P2/P3)

Run this before and after any optimization session.
"""

import os, re, sys

SKILLS_DIR = os.path.expanduser("~/.hermes/skills/cognition")
VERBOSE = "--verbose" in sys.argv
SUMMARY_ONLY = "--summary-only" in sys.argv

# Standard sections that every model should have
STANDARD_SECTIONS = [
    "核心定义",
    "多元领域映射",
    "核心原则",
    "实践要点",
    "典型案例",
    "跨模型关联",  # also checks "与其他...模型"
    "实战练习",
]

def get_v(field, fm_text):
    """Extract a YAML field value from frontmatter text."""
    m = re.search(rf'(?m)^{field}:\s*(.+)', fm_text)
    return m.group(1).strip().strip('"') if m else None


def scan_model(path):
    """Scan a single SKILL.md and return a dict of metrics."""
    with open(path) as f:
        raw = f.read()

    num_match = re.search(r'-0*(\d+)-', path)
    num = int(num_match.group(1)) if num_match else 0
    lines = raw.count("\n") + 1
    chars = len(raw)

    # Frontmatter parsing
    parts = raw.split("---", 2)
    has_fm = len(parts) >= 3
    fm = parts[1] if has_fm else ""
    body = parts[2] if has_fm else raw

    version = get_v("version", fm) or "N/A"
    category = (get_v("category", fm) or "N/A").strip()

    # Check frontmatter fields
    required_fm = ["name", "icon", "color", "version", "author", "description", "tags", "category", "related_skills"]
    missing_fm = [f for f in required_fm if not get_v(f, fm)]

    # Section check (7 standard)
    present_sections = {}
    for sec in STANDARD_SECTIONS:
        if sec == "跨模型关联":
            present_sections[sec] = (sec in body or "与其他" in body)
        elif sec == "核心定义":
            present_sections[sec] = (sec in body or "定义" in body.split("#")[0] if not body.split("#")[0] else False)
            # fallback: check if first section after frontmatter is "核心定义" or "定义"
            first_heading = re.search(r'^##\s+(.+)', body, re.MULTILINE)
            if first_heading:
                present_sections[sec] = ("核心定义" in first_heading.group(1) or "定义" in first_heading.group(1))
        else:
            present_sections[sec] = sec in body

    missing_sections = [s for s in STANDARD_SECTIONS if not present_sections[s]]

    # Content quality
    has_recs = "推荐场景" in body or "场景组合" in body
    has_deep_reflection = "💡" in body or "启发" in body
    blockquotes = len(re.findall(r'^>\s+', body, re.MULTILINE))
    same_cat_cross = "同分类" in body
    cross_cat_cross = "跨分类" in body

    # Count cross-model references (mentions of other model numbers)
    cross_refs = len(set(re.findall(r'(?<!\d)(?:00[1-9]|0[1-9]\d|1[0-9]\d|2[0-7])(?!\d)', body)))

    return {
        "num": num,
        "path": path,
        "has_fm": has_fm,
        "fm_fields_ok": len(missing_fm) == 0,
        "missing_fm": missing_fm,
        "version": version,
        "category": category,
        "chars": chars,
        "lines": lines,
        "total_sec": len([s for s, p in present_sections.items() if p]),
        "missing_sec": missing_sections,
        "has_recs": has_recs,
        "has_reflection": has_deep_reflection,
        "blockquotes": blockquotes,
        "same_cat_cross": same_cat_cross,
        "cross_cat_cross": cross_cat_cross,
        "cross_refs": cross_refs,
    }


def generate_report(models):
    """Generate a structured audit report."""
    lines = []
    lines.append("=" * 95)
    lines.append("XUAN-MASTER FAMILY AUDIT REPORT")
    lines.append("=" * 95)
    lines.append(f"Total models: {len(models)}")
    lines.append(f"Total size: {sum(m['chars'] for m in models)/1024:.0f}KB")
    lines.append(f"Average: {sum(m['chars'] for m in models)/len(models)/1024:.1f}KB/model")
    lines.append("")

    # 1. Frontmatter integrity
    fm_issues = [m for m in models if not m["fm_fields_ok"]]
    lines.append(f"1. FRONTMATTER: {len(fm_issues)}/{len(models)} have issues")
    for m in fm_issues:
        lines.append(f"   #{m['num']:03d}: missing {m['missing_fm']}")

    # 2. Section completeness
    lines.append(f"\n2. SECTIONS (target: 7/7)")
    ranking = sorted(models, key=lambda m: m["total_sec"])
    for m in ranking:
        emoji = "✅" if m["total_sec"] == 7 else "⚠️" if m["total_sec"] >= 5 else "❌"
        lines.append(f"   {emoji} #{m['num']:03d}: {m['total_sec']}/7 — missing: {m['missing_sec'] or 'none'}")

    # 3. Size ranking (bottom 5)
    lines.append(f"\n3. SMALLEST MODELS (P3 candidates)")
    bottom = sorted(models, key=lambda m: m["chars"])[:5]
    for m in bottom:
        lines.append(f"   #{m['num']:03d}: {m['chars']/1024:.1f}KB / {m['lines']}L — {os.path.basename(os.path.dirname(m['path']))}")

    # 4. Cross-model health
    no_cross = [m for m in models if not m["same_cat_cross"] and not m["cross_cat_cross"]]
    lines.append(f"\n4. CROSS-MODEL NETWORK")
    lines.append(f"   Without any cross-refs: {len(no_cross)} models — {[m['num'] for m in no_cross]}")
    lines.append(f"   With both same+class cross-refs: {sum(1 for m in models if m['same_cat_cross'] and m['cross_cat_cross'])} models")

    # 5. Quality gaps
    no_recs = [m for m in models if not m["has_recs"]]
    no_ref = [m for m in models if not m["has_reflection"]]
    low_insight = [m for m in models if m["blockquotes"] < 3 and m["chars"] > 3000]
    lines.append(f"\n5. QUALITY GAPS")
    lines.append(f"   No 场景组合: {len(no_recs)} — {[m['num'] for m in no_recs]}")
    lines.append(f"   No 💡反思: {len(no_ref)} — {[m['num'] for m in no_ref]}")
    lines.append(f"   Low insight density: {len(low_insight)} — {[m['num'] for m in low_insight]}")

    # 6. Priority findings
    lines.append(f"\n6. PRIORITY FINDINGS")
    for m in sorted(models, key=lambda x: x['chars']):
        prios = []
        if m["total_sec"] < 7:
            prios.append("P0-MISS-SEC")
        if not m["has_recs"] and "跨模型关联" in m["missing_sec"]:
            prios.append("P0-ISOLATED")
        if m["chars"] < 5000:
            prios.append("P1-TOO-SMALL")
        if m["chars"] < 8000 and m["blockquotes"] < 3:
            prios.append("P2-LEAN")
        if not m["has_reflection"]:
            prios.append("P3-NO-REFLECT")
        if prios:
            lines.append(f"   #{m['num']:03d}: {' | '.join(prios)}")

    return "\n".join(lines)


def main():
    models = []
    for entry in sorted(os.listdir(SKILLS_DIR)):
        if not entry.startswith("xuan-master-") or entry in ("xuan-master",) or "optimization" in entry:
            continue
        path = os.path.join(SKILLS_DIR, entry, "SKILL.md")
        if not os.path.exists(path):
            continue
        try:
            m = scan_model(path)
            models.append(m)
        except Exception as e:
            if VERBOSE:
                print(f"Error scanning {entry}: {e}", file=sys.stderr)

    if SUMMARY_ONLY:
        # Compact one-line per model
        print(f"{'#':>3} {'KB':>5} {'Sec':>3} {'Ins':>3} {'Rec':<4} {'Ref':<4} {'Cross':>2} {'Ver':<6} {'Cat':<5}")
        print("-" * 45)
        for m in sorted(models, key=lambda x: x["num"]):
            cross_ok = m["same_cat_cross"] and m["cross_cat_cross"]
            cross = "Y" if cross_ok else ("P" if m["same_cat_cross"] or m["cross_cat_cross"] else "N")
            print(f"{m['num']:03d} {m['chars']/1024:5.1f} {m['total_sec']:3d} {m['blockquotes']:3d} {'Y' if m['has_recs'] else 'N':<4} {'Y' if m['has_reflection'] else 'N':<4} {cross:>2} {m['version'][:6]:<6} {m['category'][:5]:<5}")
    else:
        report = generate_report(models)
        print(report)

        if VERBOSE:
            print(f"\n{'='*95}")
            print("DETAILED MODEL DATA")
            print("=" * 95)
            for m in sorted(models, key=lambda x: x["num"]):
                print(f"\n#{m['num']:03d}: {os.path.basename(os.path.dirname(m['path']))}")
                print(f"   FM: {'✅' if m['has_fm'] else '❌'}, Fields: {'✅' if m['fm_fields_ok'] else f'⚠️ {m[\"missing_fm\"]}'}")
                print(f"   Size: {m['chars']/1024:.1f}KB / {m['lines']}L")
                print(f"   Sections: {m['total_sec']}/7 — missing: {m['missing_sec'] or 'none'}")
                print(f"   Quality: {'Recs' if m['has_recs'] else 'No Recs'} | {'Reflection' if m['has_reflection'] else 'No Reflect'} | {m['blockquotes']} insights | {m['cross_refs']} cross-refs")


if __name__ == "__main__":
    main()
