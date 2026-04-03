"""
paired_case.py — 同 task 配对案例提取与分类

用途（对应 mechanism-analysis.md 第 2 节）：
  对同一 task 在 baseline 与 workflow condition 下逐步比较 step_success，
  将每一步分为四类：正向贡献 / 负向干扰 / 无效 / 冗余，
  输出统计表 + 典型案例详情。

��法：
  # 默认：扫描所有 website，baseline=no_workflow vs 所有 workflow condition
  python paired_case.py

  # 指定对比
  python paired_case.py --baseline no_workflow --treatment offline_wf

  # 导出详细案例到目录
  python paired_case.py --export_dir ../case_studies

  # 只看特定 website
  python paired_case.py --website kayak
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict

# Reuse discovery logic from step_breakdown
import sys
sys.path.insert(0, str(Path(__file__).parent))
from step_breakdown import discover_conditions, parse_action_type


# ---------------------------------------------------------------------------
# 1. 加载单个 task 的逐步详情
# ---------------------------------------------------------------------------

def load_task_detail(json_path: str):
    """
    返回 task 的详细信息：
      task_text, steps: [{target_act, pred_act, element_acc, action_f1, step_success,
                          workflow_text, observation, model_output}, ...]
    """
    with open(json_path) as f:
        data = json.load(f)

    if not data:
        return None

    metrics = data[-1]
    if not isinstance(metrics, dict) or "element_acc" not in metrics:
        return None

    ea_list = metrics["element_acc"]
    af_list = metrics["action_f1"]
    ss_list = metrics["step_success"]
    total_steps = len(ea_list)

    # Extract step-level details
    steps = []
    step_idx = 0
    task_text = ""
    workflow_text = ""

    for entry in data[:-1]:
        if isinstance(entry, str) and "ground truth" in entry.lower():
            # Skipped step
            if step_idx < total_steps:
                steps.append({
                    "step_idx": step_idx,
                    "target_act": None,
                    "pred_act": None,
                    "observation": "",
                    "model_output": "",
                    "element_acc": ea_list[step_idx],
                    "action_f1": af_list[step_idx],
                    "step_success": ss_list[step_idx],
                    "skipped": True,
                })
                step_idx += 1

        elif isinstance(entry, dict) and "pred_act" in entry:
            if step_idx < total_steps:
                steps.append({
                    "step_idx": step_idx,
                    "target_act": entry["target_act"],
                    "pred_act": entry["pred_act"],
                    "observation": "",
                    "model_output": "",
                    "element_acc": ea_list[step_idx],
                    "action_f1": af_list[step_idx],
                    "step_success": ss_list[step_idx],
                    "skipped": False,
                })
                step_idx += 1

        elif isinstance(entry, dict) and "input" in entry:
            # Extract task text and workflow from prompt
            msgs = entry["input"]
            for m in msgs:
                content = m["content"]
                if m["role"] == "user":
                    if content.strip().startswith(("## Workflow", "### Workflow")):
                        workflow_text = content[:500]
                    elif "Task:" in content and not task_text:
                        # Extract task description
                        idx = content.find("Task:")
                        end = content.find("\nTrajectory:", idx)
                        if end == -1:
                            end = content.find("\nObservation:", idx)
                        task_text = content[idx:end].strip() if end != -1 else content[idx:idx+200].strip()
                    # Last user message is observation
                    if content.startswith("Observation:"):
                        if step_idx < total_steps and len(steps) == step_idx:
                            pass  # will be attached to next step
                        elif steps and not steps[-1].get("_obs_set"):
                            steps[-1]["observation"] = content[:300]
                            steps[-1]["_obs_set"] = True

            # Model output
            output = entry.get("output", "")
            if steps and not steps[-1].get("_out_set"):
                steps[-1]["model_output"] = output[:200]
                steps[-1]["_out_set"] = True

    # Clean up internal flags
    for s in steps:
        s.pop("_obs_set", None)
        s.pop("_out_set", None)

    return {
        "task_text": task_text,
        "workflow_text": workflow_text,
        "steps": steps,
        "total_steps": total_steps,
    }


# ---------------------------------------------------------------------------
# 2. 配对比较
# ---------------------------------------------------------------------------

CATEGORY_LABELS = {
    (0, 1): "positive",    # baseline wrong, workflow right
    (1, 0): "negative",    # baseline right, workflow wrong
    (0, 0): "ineffective", # both wrong
    (1, 1): "redundant",   # both right
}


def pair_tasks(base_dir: str, treat_dir: str) -> list[dict]:
    """
    对同一 task_id 的 baseline 和 treatment 逐步配对。
    返回 [{task_id, category, step_idx, base_step, treat_step, task_text, workflow_text}, ...]
    """
    base_files = {
        int(f[:-5]): os.path.join(base_dir, f)
        for f in os.listdir(base_dir)
        if f.endswith(".json") and f[:-5].isdigit()
    }
    treat_files = {
        int(f[:-5]): os.path.join(treat_dir, f)
        for f in os.listdir(treat_dir)
        if f.endswith(".json") and f[:-5].isdigit()
    }

    common_ids = sorted(set(base_files) & set(treat_files))
    pairs = []

    for tid in common_ids:
        base_detail = load_task_detail(base_files[tid])
        treat_detail = load_task_detail(treat_files[tid])
        if not base_detail or not treat_detail:
            continue

        n = min(len(base_detail["steps"]), len(treat_detail["steps"]))
        for i in range(n):
            bs = base_detail["steps"][i]
            ts = treat_detail["steps"][i]
            cat_key = (bs["step_success"], ts["step_success"])
            pairs.append({
                "task_id": tid,
                "step_idx": i,
                "total_steps": base_detail["total_steps"],
                "category": CATEGORY_LABELS.get(cat_key, "unknown"),
                "task_text": base_detail["task_text"],
                "workflow_text": treat_detail.get("workflow_text", ""),
                "base_pred": bs.get("pred_act", ""),
                "treat_pred": ts.get("pred_act", ""),
                "target_act": bs.get("target_act") or ts.get("target_act") or "",
                "action_type": parse_action_type(bs.get("target_act") or ""),
                "base_skipped": bs.get("skipped", False),
                "treat_skipped": ts.get("skipped", False),
                # F1 deltas
                "base_af": bs["action_f1"],
                "treat_af": ts["action_f1"],
                "base_ea": bs["element_acc"],
                "treat_ea": ts["element_acc"],
            })

    return pairs


# ---------------------------------------------------------------------------
# 3. 统计与输出
# ---------------------------------------------------------------------------

def print_summary(pairs: list[dict], label: str):
    """打印四类配对的统计。"""
    counts = defaultdict(int)
    by_type = defaultdict(lambda: defaultdict(int))

    for p in pairs:
        counts[p["category"]] += 1
        by_type[p["action_type"]][p["category"]] += 1

    total = len(pairs)
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  Total paired steps: {total}")
    print(f"{'='*60}")

    print(f"\n  [Overall Distribution]")
    print(f"  {'Category':15s} {'Count':>6s} {'Pct':>7s}")
    print(f"  {'-'*30}")
    for cat in ["positive", "negative", "ineffective", "redundant"]:
        n = counts[cat]
        pct = n / total * 100 if total else 0
        print(f"  {cat:15s} {n:6d} {pct:6.1f}%")

    print(f"\n  [By Action Type]")
    print(f"  {'Type':10s} {'pos':>5s} {'neg':>5s} {'ineff':>6s} {'redun':>6s} {'total':>6s}")
    print(f"  {'-'*40}")
    for atype in sorted(by_type.keys()):
        row = by_type[atype]
        t = sum(row.values())
        print(
            f"  {atype:10s} "
            f"{row['positive']:5d} {row['negative']:5d} "
            f"{row['ineffective']:5d} {row['redundant']:5d} {t:5d}"
        )

    # Workflow contribution rate
    pos = counts["positive"]
    neg = counts["negative"]
    non_skip = sum(1 for p in pairs if not p["base_skipped"])
    if pos + neg > 0:
        print(f"\n  [Workflow Impact]")
        print(f"  Positive / (Positive + Negative) = {pos}/{pos+neg} = {pos/(pos+neg)*100:.1f}%")
        print(f"  Net gain (positive - negative)   = {pos - neg:+d} steps")


def export_cases(pairs: list[dict], category: str, n: int, export_dir: str, label: str):
    """��出指定类别的 top-n 案例到文件。"""
    filtered = [p for p in pairs if p["category"] == category and not p["base_skipped"]]

    # Sort: positive by treat_af desc, negative by base_af desc
    if category == "positive":
        filtered.sort(key=lambda p: p["treat_af"], reverse=True)
    elif category == "negative":
        filtered.sort(key=lambda p: p["base_af"], reverse=True)

    selected = filtered[:n]
    if not selected:
        return

    safe_label = re.sub(r'[^\w\-]', '_', label)
    out_path = os.path.join(export_dir, f"{category}_{safe_label}.md")

    lines = [f"# {category.title()} Cases: {label}\n"]
    lines.append(f"Total {category} steps: {len(filtered)}, showing top {len(selected)}\n")

    for i, p in enumerate(selected):
        lines.append(f"\n## Case {i+1}: task={p['task_id']}, step={p['step_idx']}/{p['total_steps']}")
        lines.append(f"\n**Task:** {p['task_text']}")
        lines.append(f"\n**Target:** `{p['target_act']}`")
        lines.append(f"\n**Baseline pred:** `{p['base_pred']}` (ea={p['base_ea']}, af={p['base_af']:.2f})")
        lines.append(f"\n**Workflow pred:** `{p['treat_pred']}` (ea={p['treat_ea']}, af={p['treat_af']:.2f})")
        if p["workflow_text"]:
            lines.append(f"\n**Workflow (excerpt):**\n```\n{p['workflow_text']}\n```")
        lines.append("")

    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Exported {len(selected)} {category} cases -> {out_path}")


# ---------------------------------------------------------------------------
# 4. 主逻辑
# ---------------------------------------------------------------------------

def main(args):
    results_root = args.results_root
    conditions = discover_conditions(results_root)

    if not conditions:
        print(f"No conditions found under {results_root}")
        return

    # Group by (model, split, website)
    groups = defaultdict(dict)
    for c in conditions:
        key = (c["model"], c["split"], c["website"])
        groups[key][c["condition"]] = c

    if args.export_dir:
        os.makedirs(args.export_dir, exist_ok=True)

    for (model, split, website), cond_map in sorted(groups.items()):
        if args.website and website != args.website:
            continue

        baseline_key = args.baseline
        if baseline_key not in cond_map:
            continue

        treatments = (
            [args.treatment] if args.treatment
            else [k for k in cond_map if k != baseline_key]
        )

        for treat_key in treatments:
            if treat_key not in cond_map:
                continue

            label = f"{model}/{split}/{website}: {treat_key} vs {baseline_key}"
            pairs = pair_tasks(cond_map[baseline_key]["path"], cond_map[treat_key]["path"])

            if not pairs:
                print(f"\n  [SKIP] {label} — no common tasks")
                continue

            print_summary(pairs, label)

            if args.export_dir:
                for cat in ["positive", "negative"]:
                    export_cases(
                        pairs, cat, args.top_n,
                        args.export_dir,
                        f"{model}_{split}_{website}_{treat_key}",
                    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWM paired case extraction")
    parser.add_argument(
        "--results_root", type=str,
        default=str(
            Path(__file__).resolve().parent.parent.parent.parent
            / "experiments" / "mind2web" / "results"
        ),
    )
    parser.add_argument("--baseline", type=str, default="no_workflow")
    parser.add_argument("--treatment", type=str, default=None, help="Specific treatment condition")
    parser.add_argument("--website", type=str, default=None, help="Filter by website")
    parser.add_argument("--export_dir", type=str, default=None, help="Export case studies to directory")
    parser.add_argument("--top_n", type=int, default=10, help="Number of cases to export per category")
    args = parser.parse_args()
    main(args)
