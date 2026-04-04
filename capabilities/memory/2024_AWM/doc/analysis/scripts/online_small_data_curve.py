import json
import re
from pathlib import Path


BASE_RESULTS = Path(
    "/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results"
)

SITES = [
    ("gpt-4o", "test_task", "kayak"),
    ("qwen/qwen3.5-397b-a17b", "test_website", "tripadvisor"),
    ("qwen/qwen3.5-397b-a17b", "test_domain", "reddit"),
]

PREFIX_BUDGETS = [1, 2, 3, 5, 10]


def load_metrics(path: Path):
    data = json.loads(path.read_text())
    stat = next(item for item in data if isinstance(item, dict) and "step_success" in item)
    elem_acc = sum(stat["element_acc"]) / len(stat["element_acc"])
    action_f1 = sum(stat["action_f1"]) / len(stat["action_f1"])
    step_sr = sum(stat["step_success"]) / len(stat["step_success"])

    user_contents = [
        msg.get("content", "")
        for item in data
        if isinstance(item, dict) and "input" in item
        for msg in item["input"]
        if msg.get("role") == "user"
    ]
    first_user = user_contents[0] if user_contents else ""
    workflow_markers = len(re.findall(r"^(?:##|###)\s", first_user, flags=re.M))

    return {
        "elem_acc": elem_acc,
        "action_f1": action_f1,
        "step_sr": step_sr,
        "workflow_markers": workflow_markers,
        "prompt_chars": len(first_user),
    }


def format_pct(value: float) -> str:
    return f"{value * 100:+.2f}%"


def site_rows(model: str, split: str, site: str):
    online_dir = BASE_RESULTS / model / split / site / "online_wf"
    baseline_dir = BASE_RESULTS / model / split / site / "no_workflow"

    online_files = sorted(online_dir.glob("[0-9]*.json"), key=lambda p: int(p.stem))
    baseline_files = sorted(baseline_dir.glob("[0-9]*.json"), key=lambda p: int(p.stem))
    n = min(len(online_files), len(baseline_files))

    rows = []
    cum_online = {"elem_acc": 0.0, "action_f1": 0.0, "step_sr": 0.0}
    cum_base = {"elem_acc": 0.0, "action_f1": 0.0, "step_sr": 0.0}

    for i in range(n):
        online = load_metrics(online_files[i])
        base = load_metrics(baseline_files[i])

        for key in ("elem_acc", "action_f1", "step_sr"):
            cum_online[key] += online[key]
            cum_base[key] += base[key]

        rows.append(
            {
                "budget": i,
                "workflow_markers": online["workflow_markers"],
                "prompt_chars": online["prompt_chars"],
                "sample_d_elem": online["elem_acc"] - base["elem_acc"],
                "sample_d_act": online["action_f1"] - base["action_f1"],
                "sample_d_step": online["step_sr"] - base["step_sr"],
                "cum_d_elem": cum_online["elem_acc"] / (i + 1) - cum_base["elem_acc"] / (i + 1),
                "cum_d_act": cum_online["action_f1"] / (i + 1) - cum_base["action_f1"] / (i + 1),
                "cum_d_step": cum_online["step_sr"] / (i + 1) - cum_base["step_sr"] / (i + 1),
            }
        )

    return rows


def render_site(model: str, split: str, site: str):
    rows = site_rows(model, split, site)
    out = []
    out.append("=" * 78)
    out.append(f"Site: {site}  |  Model: {model}  |  Split: {split}")
    out.append("=" * 78)
    out.append("Definition: budget = number of prior induced examples available at eval time.")
    out.append("So budget=0 means the first sample, still without induced workflow.")
    out.append("")
    out.append("Selected prefix checkpoints")
    out.append("")
    out.append(
        f"{'budget':>6}  {'wf':>3}  {'chars':>5}  {'cum_dElem':>10}  {'cum_dActF1':>10}  {'cum_dStepSR':>11}"
    )
    out.append("-" * 64)
    seen = set()
    for budget in PREFIX_BUDGETS + [rows[-1]["budget"]]:
        if budget >= len(rows):
            continue
        if budget in seen:
            continue
        seen.add(budget)
        row = rows[budget]
        out.append(
            f"{row['budget']:>6}  {row['workflow_markers']:>3}  {row['prompt_chars']:>5}  "
            f"{format_pct(row['cum_d_elem']):>10}  {format_pct(row['cum_d_act']):>10}  {format_pct(row['cum_d_step']):>11}"
        )

    best = max(rows[1:], key=lambda r: r["cum_d_step"]) if len(rows) > 1 else rows[0]
    positive = next((row for row in rows[1:] if row["cum_d_step"] > 0), None)

    out.append("")
    out.append("Summary")
    out.append("")
    out.append(
        f"- earliest positive prefix on Step SR: "
        f"{'none' if positive is None else f'budget={positive['budget']} ({format_pct(positive['cum_d_step'])})'}"
    )
    out.append(
        f"- best cumulative Step SR delta: budget={best['budget']} ({format_pct(best['cum_d_step'])})"
    )
    out.append(
        f"- final cumulative Step SR delta: budget={rows[-1]['budget']} ({format_pct(rows[-1]['cum_d_step'])})"
    )
    return "\n".join(out)


def main():
    blocks = [render_site(*site) for site in SITES]
    print("\n\n".join(blocks))


if __name__ == "__main__":
    main()
