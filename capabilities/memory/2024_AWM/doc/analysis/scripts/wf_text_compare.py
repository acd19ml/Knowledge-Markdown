"""
wf_text_compare.py — LM vs Rule workflow 文本特征对比

用途（对应 mechanism-analysis.md 第 4 节）：
  对比同一 website 的 LM 和 Rule workflow 文本，量化抽象性差异，
  并结合 C3 性能数据归因差异来源。

用法：
  python wf_text_compare.py
  python wf_text_compare.py --website kayak
"""

import os
import re
import argparse
from pathlib import Path
from collections import defaultdict


WF_DIR = Path(__file__).resolve().parent.parent.parent.parent / "experiments" / "mind2web" / "workflow"


# ---------------------------------------------------------------------------
# 1. Workflow 解析
# ---------------------------------------------------------------------------

def parse_workflows(text: str) -> list[dict]:
    """解析 workflow 文本为结构化列表。"""
    workflows = []
    current = None

    for line in text.split("\n"):
        line = line.rstrip()

        # Workflow header
        if line.startswith("## ") or line.startswith("### "):
            if current:
                workflows.append(current)
            title = line.lstrip("#").strip()
            current = {"title": title, "description": "", "steps": [], "raw_lines": []}
        elif current is not None:
            current["raw_lines"].append(line)
            if line.startswith("- [") or line.startswith("- CLICK") or line.startswith("- TYPE") or line.startswith("- SELECT"):
                current["steps"].append(line.strip("- ").strip())
            elif line.startswith("Given that") or line.startswith("This workflow"):
                current["description"] += line + " "
            elif line.startswith("[") and "->" in line:
                current["steps"].append(line.strip())

    if current:
        workflows.append(current)

    return workflows


# ---------------------------------------------------------------------------
# 2. 文本特征提取
# ---------------------------------------------------------------------------

def extract_features(workflows: list[dict]) -> dict:
    """提取 workflow 集合的统计特征。"""
    total_wf = len(workflows)
    total_steps = sum(len(w["steps"]) for w in workflows)
    avg_steps = total_steps / total_wf if total_wf else 0

    # Placeholder analysis: {xxx} patterns
    all_steps_text = " ".join(s for w in workflows for s in w["steps"])
    placeholders = re.findall(r'\{[^}]+\}', all_steps_text)

    # Concrete values: things like "Las Vegas", specific numbers, etc.
    # Heuristic: tokens in steps that are capitalized multi-word or quoted
    concrete_values = []
    for w in workflows:
        for s in w["steps"]:
            # After -> TYPE: or -> CLICK, look for concrete values
            if "TYPE:" in s:
                val_match = re.search(r'TYPE:\s*(.+)', s)
                if val_match:
                    val = val_match.group(1).strip()
                    if not val.startswith("{"):
                        concrete_values.append(val)
            # Element descriptions that are very specific
            bracket_content = re.findall(r'\[([^\]]+)\]', s)
            for bc in bracket_content:
                if any(c.isupper() for c in bc) and len(bc.split()) > 2:
                    # Likely a specific element name
                    if not bc.startswith("{"):
                        concrete_values.append(bc)

    # Action type distribution
    action_types = defaultdict(int)
    for w in workflows:
        for s in w["steps"]:
            if "-> CLICK" in s or s.startswith("CLICK"):
                action_types["CLICK"] += 1
            elif "-> TYPE" in s or s.startswith("TYPE"):
                action_types["TYPE"] += 1
            elif "-> SELECT" in s or s.startswith("SELECT"):
                action_types["SELECT"] += 1

    # Title patterns
    has_task_description = sum(
        1 for w in workflows
        if "trajectory" in w["title"].lower() or "concrete" in w["title"].lower()
    )

    return {
        "num_workflows": total_wf,
        "total_steps": total_steps,
        "avg_steps_per_wf": avg_steps,
        "num_placeholders": len(placeholders),
        "unique_placeholders": len(set(placeholders)),
        "placeholder_examples": list(set(placeholders))[:8],
        "num_concrete_values": len(concrete_values),
        "concrete_examples": concrete_values[:8],
        "action_types": dict(action_types),
        "task_specific_wf_count": has_task_description,
        "abstract_wf_count": total_wf - has_task_description,
    }


# ---------------------------------------------------------------------------
# 3. 对比输出
# ---------------------------------------------------------------------------

def print_comparison(website: str, lm_feat: dict, rule_feat: dict):
    """打印 LM vs Rule 对比表。"""
    print(f"\n{'='*70}")
    print(f"  LM vs Rule Workflow Comparison: {website}")
    print(f"{'='*70}")

    rows = [
        ("Num workflows", lm_feat["num_workflows"], rule_feat["num_workflows"]),
        ("Total steps", lm_feat["total_steps"], rule_feat["total_steps"]),
        ("Avg steps/workflow", f"{lm_feat['avg_steps_per_wf']:.1f}", f"{rule_feat['avg_steps_per_wf']:.1f}"),
        ("Placeholders", lm_feat["num_placeholders"], rule_feat["num_placeholders"]),
        ("Unique placeholders", lm_feat["unique_placeholders"], rule_feat["unique_placeholders"]),
        ("Concrete values", lm_feat["num_concrete_values"], rule_feat["num_concrete_values"]),
        ("Task-specific WFs", lm_feat["task_specific_wf_count"], rule_feat["task_specific_wf_count"]),
        ("Abstract/reusable WFs", lm_feat["abstract_wf_count"], rule_feat["abstract_wf_count"]),
    ]

    print(f"\n  {'Metric':25s} {'LM':>10s} {'Rule':>10s} {'Delta':>10s}")
    print(f"  {'-'*57}")
    for label, lm_val, rule_val in rows:
        if isinstance(lm_val, (int, float)) and isinstance(rule_val, (int, float)):
            delta = lm_val - rule_val
            delta_str = f"{delta:+.1f}" if isinstance(delta, float) else f"{delta:+d}"
        else:
            delta_str = ""
        print(f"  {label:25s} {str(lm_val):>10s} {str(rule_val):>10s} {delta_str:>10s}")

    # Action type breakdown
    all_types = sorted(set(list(lm_feat["action_types"]) + list(rule_feat["action_types"])))
    print(f"\n  [Action Type Distribution]")
    print(f"  {'Type':10s} {'LM':>6s} {'Rule':>6s}")
    print(f"  {'-'*24}")
    for at in all_types:
        lv = lm_feat["action_types"].get(at, 0)
        rv = rule_feat["action_types"].get(at, 0)
        print(f"  {at:10s} {lv:6d} {rv:6d}")

    # Qualitative analysis
    print(f"\n  [Abstraction Indicators]")

    if lm_feat["num_placeholders"] > rule_feat["num_placeholders"]:
        print(f"  + LM uses more placeholders ({lm_feat['num_placeholders']} vs {rule_feat['num_placeholders']})")
        print(f"    Examples: {lm_feat['placeholder_examples'][:5]}")
    else:
        print(f"  - LM does NOT use more placeholders than rule")

    if rule_feat["num_concrete_values"] > lm_feat["num_concrete_values"]:
        print(f"  + Rule retains more concrete values ({rule_feat['num_concrete_values']} vs {lm_feat['num_concrete_values']})")
        print(f"    Examples: {rule_feat['concrete_examples'][:5]}")
    else:
        print(f"  - Rule does NOT retain more concrete values")

    if lm_feat["avg_steps_per_wf"] < rule_feat["avg_steps_per_wf"]:
        print(f"  + LM workflows are more compact ({lm_feat['avg_steps_per_wf']:.1f} vs {rule_feat['avg_steps_per_wf']:.1f} steps/wf)")
    else:
        print(f"  - LM workflows are NOT more compact")

    if lm_feat["abstract_wf_count"] > rule_feat["abstract_wf_count"]:
        print(f"  + LM has more abstract/reusable workflows ({lm_feat['abstract_wf_count']} vs {rule_feat['abstract_wf_count']})")

    # Paper claim verdict
    print(f"\n  [Paper Claim: 'LM induction produces more abstract, reusable sub-routines']")
    score = 0
    if lm_feat["num_placeholders"] > rule_feat["num_placeholders"] * 1.5:
        score += 1
    if rule_feat["num_concrete_values"] > lm_feat["num_concrete_values"] * 1.5:
        score += 1
    if lm_feat["avg_steps_per_wf"] < rule_feat["avg_steps_per_wf"] * 0.8:
        score += 1
    if lm_feat["num_workflows"] < rule_feat["num_workflows"]:
        score += 1

    if score >= 3:
        print(f"  -> SUPPORTED ({score}/4 indicators)")
    elif score >= 2:
        print(f"  -> PARTIALLY SUPPORTED ({score}/4 indicators)")
    else:
        print(f"  -> WEAK/NOT SUPPORTED ({score}/4 indicators)")


# ---------------------------------------------------------------------------
# 4. Workflow 文本并排展示
# ---------------------------------------------------------------------------

def print_side_by_side(website: str, lm_wfs: list[dict], rule_wfs: list[dict]):
    """并排展示 workflow titles 和摘要。"""
    print(f"\n  [LM Workflows — {website}] ({len(lm_wfs)} total)")
    for i, w in enumerate(lm_wfs):
        steps_summary = "; ".join(w["steps"][:3])
        if len(w["steps"]) > 3:
            steps_summary += f" ... (+{len(w['steps'])-3} more)"
        print(f"    {i+1}. {w['title']}")
        print(f"       Steps: {steps_summary[:120]}")

    print(f"\n  [Rule Workflows — {website}] ({len(rule_wfs)} total, showing first 5)")
    for i, w in enumerate(rule_wfs[:5]):
        steps_summary = "; ".join(w["steps"][:3])
        if len(w["steps"]) > 3:
            steps_summary += f" ... (+{len(w['steps'])-3} more)"
        print(f"    {i+1}. {w['title'][:80]}")
        print(f"       Steps: {steps_summary[:120]}")
    if len(rule_wfs) > 5:
        print(f"    ... and {len(rule_wfs)-5} more workflows")


# ---------------------------------------------------------------------------
# 5. 主逻辑
# ---------------------------------------------------------------------------

def main(args):
    wf_dir = Path(args.wf_dir)
    if not wf_dir.exists():
        print(f"Workflow directory not found: {wf_dir}")
        return

    print("=" * 70)
    print("AWM LM vs Rule Workflow Text Comparison")
    print("=" * 70)

    # Find LM/Rule pairs
    files = list(wf_dir.glob("*.txt"))
    websites = set()
    for f in files:
        name = f.stem
        for suffix in ("_lm_wf", "_rule_wf"):
            if name.endswith(suffix):
                websites.add(name.replace(suffix, ""))

    for website in sorted(websites):
        if args.website and website != args.website:
            continue

        lm_path = wf_dir / f"{website}_lm_wf.txt"
        rule_path = wf_dir / f"{website}_rule_wf.txt"

        if not lm_path.exists() or not rule_path.exists():
            print(f"\n  [SKIP] {website}: missing LM or Rule workflow file")
            continue

        lm_text = lm_path.read_text()
        rule_text = rule_path.read_text()

        lm_wfs = parse_workflows(lm_text)
        rule_wfs = parse_workflows(rule_text)

        lm_feat = extract_features(lm_wfs)
        rule_feat = extract_features(rule_wfs)

        print_comparison(website, lm_feat, rule_feat)
        print_side_by_side(website, lm_wfs, rule_wfs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LM vs Rule workflow text comparison")
    parser.add_argument(
        "--wf_dir", type=str,
        default=str(WF_DIR),
    )
    parser.add_argument("--website", type=str, default=None)
    args = parser.parse_args()
    main(args)
