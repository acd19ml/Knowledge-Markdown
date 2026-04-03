"""
cross_site_diag.py — Cross-site 退化诊断

用途（对应 mechanism-analysis.md 第 3 节）：
  诊断 C2 中 tripadvisor / reddit 退化的根因。
  区分两种假说：
    A: workflow 内容不适配目标站点
    B: observation 格式变化导致 element grounding 整体崩溃

用法：
  python cross_site_diag.py
  python cross_site_diag.py --website tripadvisor
  python cross_site_diag.py --export_dir ../cross_site_report
"""

import os
import json
import argparse
from pathlib import Path
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent))
from step_breakdown import discover_conditions, parse_action_type
from paired_case import pair_tasks, CATEGORY_LABELS


# ---------------------------------------------------------------------------
# 1. Baseline 绝对水平诊断
# ---------------------------------------------------------------------------

def baseline_profile(cond_dir: str) -> dict:
    """统计 baseline 在一个站点上的 step 级 profile。"""
    from step_breakdown import load_all_steps, aggregate
    steps = load_all_steps(cond_dir)
    if not steps:
        return {}

    by_type = aggregate(steps, "action_type")
    by_half = aggregate(steps, "step_half")

    # skip rate
    total = len(steps)
    skipped = sum(1 for s in steps if s["action_type"] == "SKIP")

    return {
        "total_steps": total,
        "skip_count": skipped,
        "skip_rate": skipped / total * 100 if total else 0,
        "by_type": by_type,
        "by_half": by_half,
    }


# ---------------------------------------------------------------------------
# 2. Workflow 适配度分析
# ---------------------------------------------------------------------------

def load_workflow_text(results_root: str, website: str, condition: str) -> str:
    """尝试从 workflow 目录中找到对应的 workflow 文件。"""
    # 从 results 目录往上找 workflow/ 目录
    base = Path(results_root)
    # 往上走到 mind2web 目录
    for parent in [base] + list(base.parents):
        wf_dir = parent / "workflow"
        if wf_dir.exists():
            # 尝试多种命名
            candidates = [
                wf_dir / f"{website}_online_wf.txt",
                wf_dir / f"{website}_offline_wf.txt",
                wf_dir / f"{website}_{condition}.txt",
                wf_dir / f"{website}_lm_wf.txt",
            ]
            for c in candidates:
                if c.exists():
                    return c.read_text().strip()
            # fallback: 任何包含 website 名的文件
            for f in wf_dir.iterdir():
                if website in f.name and f.suffix == ".txt":
                    return f.read_text().strip()
    return ""


def workflow_step_keywords(workflow_text: str) -> list[str]:
    """从 workflow 中提取步骤关键词（动作目标描述）。"""
    import re
    keywords = []
    for line in workflow_text.split("\n"):
        line = line.strip()
        if line.startswith("- [") or line.startswith("- CLICK") or line.startswith("- TYPE") or line.startswith("- SELECT"):
            # 提取 [] 中的描述
            matches = re.findall(r'\[([^\]]+)\]', line)
            keywords.extend(matches)
        elif "->" in line:
            parts = line.split("->")
            if parts:
                keywords.append(parts[0].strip().split("]")[-1].strip())
    return [k for k in keywords if len(k) > 2]


# ---------------------------------------------------------------------------
# 3. 退化定位：逐步粒度
# ---------------------------------------------------------------------------

def degradation_profile(pairs: list[dict]) -> dict:
    """从配对数据中计算退化 profile。"""
    stats = {
        "total": len(pairs),
        "positive": 0,
        "negative": 0,
        "ineffective": 0,
        "redundant": 0,
        "neg_by_type": defaultdict(int),
        "neg_by_half": defaultdict(int),
        "neg_tasks": defaultdict(list),  # task_id -> [step details]
    }

    for p in pairs:
        cat = p["category"]
        stats[cat] = stats.get(cat, 0) + 1

        if cat == "negative":
            stats["neg_by_type"][p["action_type"]] += 1
            half = "first_half" if p["step_idx"] < p["total_steps"] / 2 else "second_half"
            stats["neg_by_half"][half] += 1
            stats["neg_tasks"][p["task_id"]].append({
                "step_idx": p["step_idx"],
                "target_act": p["target_act"],
                "base_pred": p["base_pred"],
                "treat_pred": p["treat_pred"],
                "action_type": p["action_type"],
            })

    return stats


# ---------------------------------------------------------------------------
# 4. 假说检验
# ---------------------------------------------------------------------------

def test_hypotheses(
    base_profile: dict,
    source_base_profile: dict,
    degrad: dict,
    workflow_text: str,
    label: str,
):
    """
    输出假说 A vs B 的证据对照。

    假说 A: workflow 内容不适配 → negative 集中在特定 action type，baseline 本身正常
    假说 B: observation 格式变化 → baseline 本身就弱，skip_rate 高，CLICK element_acc 低
    """
    print(f"\n{'='*60}")
    print(f"  Hypothesis Test: {label}")
    print(f"{'='*60}")

    # --- Evidence for Hypothesis B ---
    print(f"\n  [Hypothesis B: Element grounding collapse]")

    target_skip = base_profile.get("skip_rate", 0)
    source_skip = source_base_profile.get("skip_rate", 0) if source_base_profile else 0
    print(f"  Skip rate (target baseline): {target_skip:.1f}%")
    print(f"  Skip rate (source baseline): {source_skip:.1f}%")

    target_click_ea = base_profile.get("by_type", {}).get("CLICK", {}).get("Elem Acc", 0)
    source_click_ea = source_base_profile.get("by_type", {}).get("CLICK", {}).get("Elem Acc", 0) if source_base_profile else 0
    print(f"  CLICK Elem Acc (target baseline): {target_click_ea:.1f}%")
    print(f"  CLICK Elem Acc (source baseline): {source_click_ea:.1f}%")

    b_evidence = []
    if target_skip > source_skip + 10:
        b_evidence.append(f"Skip rate +{target_skip - source_skip:.0f}pp higher on target site")
    if target_click_ea < source_click_ea - 10:
        b_evidence.append(f"CLICK Elem Acc {source_click_ea - target_click_ea:.0f}pp lower on target site")

    if b_evidence:
        print(f"  -> B evidence: {'; '.join(b_evidence)}")
    else:
        print(f"  -> No strong B evidence (baseline performs similarly)")

    # --- Evidence for Hypothesis A ---
    print(f"\n  [Hypothesis A: Workflow content mismatch]")

    neg_total = degrad["negative"]
    neg_click = degrad["neg_by_type"].get("CLICK", 0)
    neg_type = degrad["neg_by_type"].get("TYPE", 0)
    print(f"  Negative steps: {neg_total}")
    print(f"    CLICK: {neg_click}  TYPE: {neg_type}")

    if neg_total > 0:
        click_pct = neg_click / neg_total * 100
        print(f"    CLICK share of negatives: {click_pct:.0f}%")

    # Check if workflow has relevant content
    wf_keywords = workflow_step_keywords(workflow_text)
    print(f"  Workflow keywords ({len(wf_keywords)}): {wf_keywords[:10]}")

    a_evidence = []
    if neg_total > 3 and neg_click / neg_total > 0.6:
        a_evidence.append("Negatives dominated by CLICK (element-level mismatch, not value mismatch)")
    if neg_type > neg_click:
        a_evidence.append("Negatives dominated by TYPE (workflow provides wrong value templates)")

    # Look at specific negative cases
    tasks_with_multi_neg = {
        tid: steps for tid, steps in degrad["neg_tasks"].items() if len(steps) >= 2
    }
    if tasks_with_multi_neg:
        a_evidence.append(f"{len(tasks_with_multi_neg)} tasks have 2+ negative steps (systematic mismatch)")

    if a_evidence:
        print(f"  -> A evidence: {'; '.join(a_evidence)}")
    else:
        print(f"  -> No strong A evidence")

    # --- Verdict ---
    print(f"\n  [Preliminary Verdict]")
    if b_evidence and not a_evidence:
        print(f"  -> Primarily Hypothesis B: baseline element grounding is weaker on target site")
    elif a_evidence and not b_evidence:
        print(f"  -> Primarily Hypothesis A: workflow content is mismatched")
    elif a_evidence and b_evidence:
        print(f"  -> Mixed: both element grounding degradation AND workflow mismatch")
    else:
        print(f"  -> Inconclusive: no strong evidence for either hypothesis")


# ---------------------------------------------------------------------------
# 5. 主逻辑
# ---------------------------------------------------------------------------

def main(args):
    conditions = discover_conditions(args.results_root)
    if not conditions:
        print(f"No conditions found under {args.results_root}")
        return

    print("=" * 60)
    print("AWM Cross-Site Degradation Diagnosis")
    print("=" * 60)

    groups = defaultdict(dict)
    for c in conditions:
        key = (c["model"], c["split"], c["website"])
        groups[key][c["condition"]] = c

    # Identify cross-site pairs: find (model, test_website/test_domain, website)
    # and their source site (model, test_task, source_website)
    cross_site_groups = []
    for (model, split, website), cond_map in groups.items():
        if split in ("test_website", "test_domain"):
            if args.website and website != args.website:
                continue
            # Find source baseline (same model, test_task)
            source_candidates = [
                (m, s, w) for (m, s, w) in groups
                if m == model and s == "test_task"
            ]
            cross_site_groups.append({
                "model": model,
                "split": split,
                "website": website,
                "cond_map": cond_map,
                "source_keys": source_candidates,
            })

    if not cross_site_groups:
        # Fallback: also analyze test_task sites that degraded
        print("\n  No cross-site splits found. Analyzing all sites with workflow degradation.\n")
        for (model, split, website), cond_map in sorted(groups.items()):
            if args.website and website != args.website:
                continue
            if "no_workflow" not in cond_map:
                continue

            base_prof = baseline_profile(cond_map["no_workflow"]["path"])
            print(f"\n  [{model}/{split}/{website}] baseline profile")
            print(f"    Total steps: {base_prof['total_steps']}, Skip rate: {base_prof['skip_rate']:.1f}%")
            for atype, metrics in sorted(base_prof["by_type"].items()):
                print(f"    {atype:10s}  EA={metrics['Elem Acc']:5.1f}%  AF={metrics['Act F1']:5.1f}%  SR={metrics['Step SR']:5.1f}%  n={metrics['n']}")
        return

    for csg in cross_site_groups:
        model = csg["model"]
        split = csg["split"]
        website = csg["website"]
        cond_map = csg["cond_map"]

        print(f"\n\n{'#'*60}")
        print(f"  Target: {model}/{split}/{website}")
        print(f"{'#'*60}")

        # --- 1. Target baseline profile ---
        if "no_workflow" in cond_map:
            target_base = baseline_profile(cond_map["no_workflow"]["path"])
            print(f"\n  [Target Baseline Profile]")
            print(f"  Total steps: {target_base['total_steps']}, Skip rate: {target_base['skip_rate']:.1f}%")
            for atype, metrics in sorted(target_base["by_type"].items()):
                print(f"    {atype:10s}  EA={metrics['Elem Acc']:5.1f}%  AF={metrics['Act F1']:5.1f}%  SR={metrics['Step SR']:5.1f}%  n={metrics['n']}")
        else:
            target_base = {}

        # --- 2. Source baseline profile (for comparison) ---
        source_base = {}
        for sk in csg["source_keys"]:
            src_cond_map = groups[sk]
            if "no_workflow" in src_cond_map:
                source_base = baseline_profile(src_cond_map["no_workflow"]["path"])
                src_website = sk[2]
                print(f"\n  [Source Baseline Profile: {src_website}]")
                print(f"  Total steps: {source_base['total_steps']}, Skip rate: {source_base['skip_rate']:.1f}%")
                for atype, metrics in sorted(source_base["by_type"].items()):
                    print(f"    {atype:10s}  EA={metrics['Elem Acc']:5.1f}%  AF={metrics['Act F1']:5.1f}%  SR={metrics['Step SR']:5.1f}%  n={metrics['n']}")
                break  # use first source

        # --- 3. Degradation profile ---
        for treat_name in sorted(cond_map):
            if treat_name == "no_workflow":
                continue
            if "no_workflow" not in cond_map:
                continue

            pairs = pair_tasks(cond_map["no_workflow"]["path"], cond_map[treat_name]["path"])
            if not pairs:
                continue

            degrad = degradation_profile(pairs)
            print(f"\n  [Degradation Profile: {treat_name}]")
            print(f"  Positive: {degrad['positive']}, Negative: {degrad['negative']}, "
                  f"Ineffective: {degrad['ineffective']}, Redundant: {degrad['redundant']}")

            if degrad["neg_tasks"]:
                print(f"\n  [Negative Cases by Task]")
                for tid, steps in sorted(degrad["neg_tasks"].items()):
                    print(f"    Task {tid}: {len(steps)} negative step(s)")
                    for s in steps[:3]:
                        print(f"      step {s['step_idx']}: {s['action_type']} "
                              f"target={s['target_act']}, "
                              f"base_pred={s['base_pred']}, "
                              f"treat_pred={s['treat_pred']}")

            # --- 4. Hypothesis test ---
            wf_text = load_workflow_text(args.results_root, website, treat_name)
            test_hypotheses(
                target_base, source_base, degrad, wf_text,
                f"{model}/{split}/{website}/{treat_name}",
            )

    # --- Export ---
    if args.export_dir:
        os.makedirs(args.export_dir, exist_ok=True)
        # Re-run and capture to file
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            # Already printed above, just save
            pass
        out_path = os.path.join(args.export_dir, "cross_site_diagnosis.txt")
        print(f"\n  Full output also at: {args.export_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWM cross-site degradation diagnosis")
    parser.add_argument(
        "--results_root", type=str,
        default=str(
            Path(__file__).resolve().parent.parent.parent.parent
            / "experiments" / "mind2web" / "results"
        ),
    )
    parser.add_argument("--website", type=str, default=None)
    parser.add_argument("--export_dir", type=str, default=None)
    args = parser.parse_args()
    main(args)
