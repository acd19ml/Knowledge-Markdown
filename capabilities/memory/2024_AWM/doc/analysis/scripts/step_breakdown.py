"""
step_breakdown.py — 按维度交叉分解 AWM 逐步指标

用途（对应 mechanism-analysis.md 第 1 节）：
  从 JSON 日志中提取逐步指标，按 action_type / step_position / website / condition
  交叉统计，输出 delta 表，回答"workflow 改善了什么环节"。

用法：
  # 默认扫描整个 results 目录
  python step_breakdown.py --results_root ../../../experiments/mind2web/results

  # 只看 gpt-4o / test_task
  python step_breakdown.py --results_root ../../../experiments/mind2web/results/gpt-4o/test_task

  # 导出 CSV
  python step_breakdown.py --results_root ../../../experiments/mind2web/results --csv output.csv
"""

import os
import re
import json
import argparse
from collections import defaultdict
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. 解析单个 JSON 日志，提取逐步记录
# ---------------------------------------------------------------------------

def parse_action_type(act_str: str) -> str:
    """从 'CLICK [id]' / 'TYPE [id] [val]' / 'SELECT [id] [val]' 中提取操作类型。"""
    if not act_str:
        return "UNKNOWN"
    m = re.match(r"(CLICK|TYPE|SELECT)", act_str.strip())
    return m.group(1) if m else "UNKNOWN"


def load_task_steps(json_path: str) -> list[dict]:
    """
    返回一个 task 的逐步记录列表，每条包含：
      action_type, step_idx, total_steps,
      element_acc, action_f1, step_success
    """
    with open(json_path) as f:
        data = json.load(f)

    if not data:
        return []

    # 最后一条是指标汇总
    metrics = data[-1]
    if not isinstance(metrics, dict) or "element_acc" not in metrics:
        return []

    ea_list = metrics["element_acc"]
    af_list = metrics["action_f1"]
    ss_list = metrics["step_success"]
    total_steps = len(ea_list)

    # 从前面的条目中提取每一步的 target_act
    target_acts = []
    for entry in data[:-1]:
        if isinstance(entry, dict) and "target_act" in entry:
            target_acts.append(entry["target_act"])
        elif isinstance(entry, str) and "ground truth" in entry.lower():
            target_acts.append(None)  # skipped step

    # 对齐：target_acts 的长度应该等于 total_steps
    # 如果不等（极少数异常），用 None 填充
    while len(target_acts) < total_steps:
        target_acts.append(None)

    steps = []
    for i in range(total_steps):
        act_str = target_acts[i] if i < len(target_acts) else None
        steps.append({
            "action_type": parse_action_type(act_str) if act_str else "SKIP",
            "step_idx": i,
            "total_steps": total_steps,
            "element_acc": ea_list[i],
            "action_f1": af_list[i],
            "step_success": ss_list[i],
        })
    return steps


# ---------------------------------------------------------------------------
# 2. 扫描 results 目录，自动识别层级
# ---------------------------------------------------------------------------

def discover_conditions(results_root: str) -> list[dict]:
    """
    自动发现 results_root 下所有 condition 目录。
    返回 [{model, split, website, condition, path}, ...]

    支持两种目录结构：
      results/{model}/{split}/{website}/{condition}/       (gpt-4o)
      results/{model}/{submodel}/{split}/{website}/{condition}/  (qwen)
    """
    found = []
    root = Path(results_root)

    for json_file in root.rglob("*.json"):
        if not json_file.stem.isdigit():
            continue
        cond_dir = json_file.parent
        rel = cond_dir.relative_to(root)
        parts = rel.parts

        # 识别 split（以 test_ 开头）
        split_idx = None
        for i, p in enumerate(parts):
            if p.startswith("test_"):
                split_idx = i
                break
        if split_idx is None:
            continue

        model = "/".join(parts[:split_idx])
        split = parts[split_idx]
        website = parts[split_idx + 1] if split_idx + 1 < len(parts) else "unknown"
        condition = parts[split_idx + 2] if split_idx + 2 < len(parts) else "unknown"

        key = (model, split, website, condition)
        if not any(
            (d["model"], d["split"], d["website"], d["condition"]) == key
            for d in found
        ):
            found.append({
                "model": model,
                "split": split,
                "website": website,
                "condition": condition,
                "path": str(cond_dir),
            })

    found.sort(key=lambda d: (d["model"], d["split"], d["website"], d["condition"]))
    return found


def load_all_steps(cond_dir: str) -> list[dict]:
    """加载一个 condition 目录下所有 task 的逐步记录。"""
    all_steps = []
    json_files = sorted(
        [f for f in os.listdir(cond_dir) if f.endswith(".json") and f[:-5].isdigit()]
    )
    for fname in json_files:
        task_id = int(fname[:-5])
        steps = load_task_steps(os.path.join(cond_dir, fname))
        for s in steps:
            s["task_id"] = task_id
        all_steps.extend(steps)
    return all_steps


# ---------------------------------------------------------------------------
# 3. 聚合统计
# ---------------------------------------------------------------------------

def aggregate(steps: list[dict], group_key: str) -> dict:
    """
    按 group_key 分组，计算每组的 element_acc / action_f1 / step_success 均值。
    返回 {group_value: {metric: mean, ..., n: count}, ...}
    """
    buckets = defaultdict(lambda: {"ea": [], "af": [], "ss": []})
    for s in steps:
        if group_key == "step_half":
            val = "first_half" if s["step_idx"] < s["total_steps"] / 2 else "second_half"
        else:
            val = s.get(group_key, "UNKNOWN")
        buckets[val]["ea"].append(s["element_acc"])
        buckets[val]["af"].append(s["action_f1"])
        buckets[val]["ss"].append(s["step_success"])

    result = {}
    for k, v in sorted(buckets.items()):
        n = len(v["ea"])
        result[k] = {
            "Elem Acc": sum(v["ea"]) / n * 100 if n else 0,
            "Act F1": sum(v["af"]) / n * 100 if n else 0,
            "Step SR": sum(v["ss"]) / n * 100 if n else 0,
            "n": n,
        }
    return result


# ---------------------------------------------------------------------------
# 4. 打印表格
# ---------------------------------------------------------------------------

def print_table(title: str, rows: dict, indent: str = "  "):
    """rows: {label: {metric: value, ...}}"""
    print(f"\n{title}")
    print(f"{indent}{'':20s} {'Elem Acc':>9s} {'Act F1':>9s} {'Step SR':>9s} {'n':>6s}")
    print(f"{indent}{'-'*56}")
    for label, metrics in rows.items():
        print(
            f"{indent}{str(label):20s} "
            f"{metrics['Elem Acc']:8.1f}% "
            f"{metrics['Act F1']:8.1f}% "
            f"{metrics['Step SR']:8.1f}% "
            f"{metrics['n']:5d}"
        )


def print_delta_table(title: str, base_rows: dict, wf_rows: dict):
    """打印 workflow - baseline 的 delta 表。"""
    print(f"\n{title}")
    indent = "  "
    print(f"{indent}{'':20s} {'dElem':>9s} {'dActF1':>9s} {'dStepSR':>9s}")
    print(f"{indent}{'-'*50}")
    all_keys = sorted(set(base_rows.keys()) | set(wf_rows.keys()))
    for k in all_keys:
        b = base_rows.get(k, {"Elem Acc": 0, "Act F1": 0, "Step SR": 0})
        w = wf_rows.get(k, {"Elem Acc": 0, "Act F1": 0, "Step SR": 0})
        de = w["Elem Acc"] - b["Elem Acc"]
        da = w["Act F1"] - b["Act F1"]
        ds = w["Step SR"] - b["Step SR"]
        print(f"{indent}{str(k):20s} {de:+8.1f}% {da:+8.1f}% {ds:+8.1f}%")


# ---------------------------------------------------------------------------
# 5. 主逻辑
# ---------------------------------------------------------------------------

def main(args):
    conditions = discover_conditions(args.results_root)
    if not conditions:
        print(f"No conditions found under {args.results_root}")
        return

    print("=" * 70)
    print("AWM Step-Level Breakdown Analysis")
    print("=" * 70)

    # 按 (model, split, website) 分组
    groups = defaultdict(dict)
    for c in conditions:
        key = (c["model"], c["split"], c["website"])
        groups[key][c["condition"]] = c

    csv_rows = []

    for (model, split, website), cond_map in sorted(groups.items()):
        print(f"\n{'='*70}")
        print(f"  Model: {model}  |  Split: {split}  |  Website: {website}")
        print(f"  Conditions: {', '.join(sorted(cond_map.keys()))}")
        print(f"{'='*70}")

        # 加载每个 condition 的 steps
        steps_by_cond = {}
        for cond_name, cond_info in sorted(cond_map.items()):
            steps_by_cond[cond_name] = load_all_steps(cond_info["path"])

        # --- 总体指标 ---
        overall = {}
        for cond_name, steps in steps_by_cond.items():
            overall[cond_name] = aggregate(steps, "action_type").get(
                "CLICK", {"Elem Acc": 0, "Act F1": 0, "Step SR": 0, "n": 0}
            )
            # 重新算总体
            agg_all = aggregate(steps, "action_type")
            n_total = sum(v["n"] for v in agg_all.values())
            if n_total:
                overall[cond_name] = {
                    "Elem Acc": sum(v["Elem Acc"] * v["n"] for v in agg_all.values()) / n_total,
                    "Act F1": sum(v["Act F1"] * v["n"] for v in agg_all.values()) / n_total,
                    "Step SR": sum(v["Step SR"] * v["n"] for v in agg_all.values()) / n_total,
                    "n": n_total,
                }
        print_table("[Overall]", overall)

        # --- 按 action_type 分解 ---
        for cond_name, steps in steps_by_cond.items():
            agg = aggregate(steps, "action_type")
            print_table(f"[By Action Type] {cond_name}", agg)

        # --- 按 step_half 分解 ---
        for cond_name, steps in steps_by_cond.items():
            agg = aggregate(steps, "step_half")
            print_table(f"[By Step Half] {cond_name}", agg)

        # --- Delta 表：baseline vs 各 workflow condition ---
        baseline_key = "no_workflow"
        if baseline_key in steps_by_cond:
            base_by_type = aggregate(steps_by_cond[baseline_key], "action_type")
            base_by_half = aggregate(steps_by_cond[baseline_key], "step_half")
            for cond_name, steps in steps_by_cond.items():
                if cond_name == baseline_key:
                    continue
                wf_by_type = aggregate(steps, "action_type")
                wf_by_half = aggregate(steps, "step_half")
                print_delta_table(
                    f"[Delta: {cond_name} - {baseline_key}] by action_type",
                    base_by_type, wf_by_type,
                )
                print_delta_table(
                    f"[Delta: {cond_name} - {baseline_key}] by step_half",
                    base_by_half, wf_by_half,
                )

        # --- 收集 CSV ---
        if args.csv:
            for cond_name, steps in steps_by_cond.items():
                for dim in ["action_type", "step_half"]:
                    agg = aggregate(steps, dim)
                    for group_val, metrics in agg.items():
                        csv_rows.append({
                            "model": model,
                            "split": split,
                            "website": website,
                            "condition": cond_name,
                            "dimension": dim,
                            "group": group_val,
                            **metrics,
                        })

    # --- 输出 CSV ---
    if args.csv and csv_rows:
        import csv
        fieldnames = [
            "model", "split", "website", "condition",
            "dimension", "group", "Elem Acc", "Act F1", "Step SR", "n",
        ]
        with open(args.csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"\nCSV exported to {args.csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWM step-level breakdown analysis")
    parser.add_argument(
        "--results_root",
        type=str,
        default=str(
            Path(__file__).resolve().parent.parent.parent.parent
            / "experiments" / "mind2web" / "results"
        ),
        help="Root directory of results (auto-discovered)",
    )
    parser.add_argument("--csv", type=str, default=None, help="Export to CSV file")
    args = parser.parse_args()
    main(args)
