#!/usr/bin/env python3
"""
alignment_rate.py — Compute workflow-target action alignment rates for AWM experiments.

For each site, this script checks how many ground-truth target actions in the
evaluation JSON files are "covered" by at least one pattern in the corresponding
offline workflow file.

Matching heuristic (keyword overlap):
  1. Parse the workflow file to extract (element_type, descriptive_text, action_type)
     tuples.  Descriptive text is lowered; placeholder tokens like {location} are
     kept as-is but ignored during matching.
  2. For each target action step in a task JSON, extract (action_type, element_id).
     Then retrieve the observation HTML from the preceding INPUT entry and locate
     the element description text associated with that element ID.
  3. A target step is "aligned" if ANY workflow pattern satisfies:
       a) The action types are compatible (CLICK-CLICK, TYPE-TYPE, SELECT-SELECT,
          or the workflow uses a placeholder element like {filter}).
       b) At least one non-trivial keyword (>= 3 chars) from the workflow pattern's
          descriptive text appears in the observation's element context for the
          target element ID.

Limitations:
  - **Label lag**: The workflow was induced from training tasks; test-time pages may
    use different labels for the same widget (e.g., "Search Cars" vs "Search").
  - **Keyword ambiguity**: Short or generic keywords ("go", "click") can produce
    false-positive alignments.
  - **Placeholder patterns**: Workflow steps with {placeholder} text cannot be
    matched by keyword; we fall back to action-type-only matching for these.
  - **Element ID mismatch**: If the observation HTML does not contain the target
    element ID (SKIP entries), the step is excluded from the count.
  - **Partial coverage**: A workflow step may match the element but prescribe a
    different value for TYPE/SELECT; we do not check value alignment.

Usage:
    python alignment_rate.py                        # uses default relative paths
    python alignment_rate.py --base /path/to/AWM    # override base directory
"""

import argparse
import json
import glob
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Workflow parsing
# ---------------------------------------------------------------------------

# Matches lines like:  [button] Browse the Parks Below -> CLICK
#                       1. [textbox]  Search Site -> TYPE: {search-term}
STEP_RE = re.compile(
    r"(?:^\d+\.\s*)?(?:^-\s*)?"    # optional leading "1. " or "- "
    r"\[(\w+(?:/\w+)?)\]\s*"       # [element_type] or [element_type/subtype]
    r"(.*?)\s*->\s*"               # descriptive text (may be empty)
    r"(CLICK|TYPE|SELECT|HOVER)"   # action verb
    r"(?::\s*(.*))?"               # optional value after colon
    r"\s*$",
    re.IGNORECASE,
)

# Placeholder token: {some-thing}
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def parse_workflow(filepath: str) -> List[dict]:
    """Return list of workflow pattern dicts from a workflow text file."""
    patterns = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            m = STEP_RE.match(line)
            if not m:
                continue
            elem_type = m.group(1).lower()
            desc_raw = m.group(2).strip()
            action = m.group(3).upper()
            value = (m.group(4) or "").strip()

            # Check if desc is entirely a placeholder
            is_placeholder = bool(PLACEHOLDER_RE.fullmatch(desc_raw))

            # Extract meaningful keywords (non-placeholder, length >= 3)
            desc_lower = desc_raw.lower()
            # Remove placeholder tokens for keyword extraction
            desc_clean = PLACEHOLDER_RE.sub("", desc_lower).strip()
            keywords = [
                w for w in re.split(r"[\s/,]+", desc_clean)
                if len(w) >= 3 and w not in ("the", "and", "for", "your", "with", "from")
            ]

            patterns.append({
                "elem_type": elem_type,
                "desc_raw": desc_raw,
                "desc_lower": desc_lower,
                "action": action,
                "value": value,
                "is_placeholder": is_placeholder,
                "keywords": keywords,
            })
    return patterns


# ---------------------------------------------------------------------------
# JSON task parsing
# ---------------------------------------------------------------------------

def extract_element_context(observation: str, elem_id: str) -> Optional[str]:
    """
    Given an observation HTML string and an element ID (e.g., '602'),
    extract a window of text around that ID to use for keyword matching.

    The observation format is simplified HTML like:
        <a id=602 find out where you can> ... </a>
    We grab the text from the tag containing id=<elem_id>.
    """
    # Pattern: find id=ELEM_ID followed by descriptive text until >
    # The ID might appear as  id=602  (with space or >) after it
    pattern = re.compile(
        r"id=" + re.escape(elem_id) + r"[\s>]([^<]*)", re.IGNORECASE
    )
    m = pattern.search(observation)
    if m:
        return m.group(1).strip().lower()

    # Broader search: grab surrounding context (100 chars each side)
    idx = observation.find(f"id={elem_id}")
    if idx == -1:
        return None
    start = max(0, idx - 120)
    end = min(len(observation), idx + 200)
    return observation[start:end].lower()


def parse_target_act(target_act: str) -> Tuple[str, str, str]:
    """
    Parse target_act string like 'CLICK [602]' or 'TYPE [148] [little ferry]'.
    Returns (action_type, element_id, value).
    """
    # CLICK [602]
    m = re.match(r"(CLICK|TYPE|SELECT|HOVER)\s+\[(\d+)\](?:\s+\[(.+?)\])?", target_act)
    if m:
        return m.group(1), m.group(2), m.group(3) or ""
    return "", "", ""


def load_task_steps(filepath: str) -> List[dict]:
    """
    Load a task JSON and return a list of step dicts, each containing:
      - target_act: the raw target action string
      - action_type, elem_id, value: parsed from target_act
      - observation: the observation HTML from the preceding INPUT entry
      - elem_context: extracted element description text for matching
    """
    with open(filepath) as f:
        data = json.load(f)

    steps = []
    last_observation = ""

    for entry in data:
        # Skip string entries (SKIP steps like "The ground truth element is not...")
        if isinstance(entry, str):
            continue

        # INPUT entry — extract the last user message's observation
        if "input" in entry and "output" in entry:
            messages = entry["input"]
            if isinstance(messages, list):
                # Find the last user message
                for msg in reversed(messages):
                    if isinstance(msg, dict) and msg.get("role") == "user":
                        content = msg.get("content", "")
                        if isinstance(content, str) and "Observation:" in content:
                            last_observation = content
                        break
            continue

        # TARGET entry — has pred_act and target_act
        if "target_act" in entry:
            target_act = entry["target_act"]
            action_type, elem_id, value = parse_target_act(target_act)
            if not action_type:
                continue

            elem_context = extract_element_context(last_observation, elem_id)

            steps.append({
                "target_act": target_act,
                "action_type": action_type,
                "elem_id": elem_id,
                "value": value,
                "observation": last_observation,
                "elem_context": elem_context,
            })

        # Metrics dict at the end — skip
        # (has keys like 'element_acc', 'action_f1', etc.)

    return steps


# ---------------------------------------------------------------------------
# Alignment checking
# ---------------------------------------------------------------------------

def check_alignment(step: dict, patterns: List[dict]) -> Tuple[bool, Optional[dict]]:
    """
    Check if a target step is aligned with any workflow pattern.

    Returns (is_aligned, matching_pattern_or_None).
    """
    action = step["action_type"]
    elem_context = step.get("elem_context") or ""
    observation_lower = step.get("observation", "").lower()

    for pat in patterns:
        # Action type must be compatible (HOVER treated as CLICK)
        pat_action = pat["action"]
        step_action = action
        if pat_action == "HOVER":
            pat_action = "CLICK"
        if step_action == "HOVER":
            step_action = "CLICK"

        if pat_action != step_action:
            continue

        # If pattern is a placeholder (e.g., {filter}), match on action type alone
        # but require at least the element type keyword appears in context
        if pat["is_placeholder"]:
            # Loose match: action type matches, and element type keyword appears
            # in the observation near the target element
            if pat["elem_type"] in elem_context or pat["elem_type"] in observation_lower:
                return True, pat
            # Even looser: just action type match for placeholder patterns
            # This is aggressive but captures the intent
            continue

        # Keyword matching: at least one keyword from the workflow pattern
        # must appear in the element's context or nearby observation text
        if not pat["keywords"]:
            # No meaningful keywords (empty desc after removing placeholders)
            # Fall back to action-type match only if elem_type matches
            if pat["elem_type"] in elem_context:
                return True, pat
            continue

        # Check keywords against element context first, then broader observation
        match_target = elem_context if elem_context else observation_lower
        for kw in pat["keywords"]:
            if kw in match_target:
                return True, pat

        # Also try the full workflow description as a substring
        desc = pat["desc_lower"]
        desc_clean = PLACEHOLDER_RE.sub("", desc).strip()
        if len(desc_clean) >= 5 and desc_clean in match_target:
            return True, pat

    return False, None


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

SITES = ["kayak", "newegg", "budget", "sixflags"]


def analyze_site(
    site: str, workflow_dir: str, results_dir: str
) -> dict:
    """Analyze alignment for a single site. Returns a results dict."""

    wf_path = os.path.join(workflow_dir, f"{site}_offline_wf.txt")
    task_dir = os.path.join(results_dir, site, "offline_wf")

    if not os.path.isfile(wf_path):
        return {"error": f"Workflow file not found: {wf_path}"}
    if not os.path.isdir(task_dir):
        return {"error": f"Task directory not found: {task_dir}"}

    patterns = parse_workflow(wf_path)
    task_files = sorted(glob.glob(os.path.join(task_dir, "*.json")))

    total = 0
    aligned = 0
    by_action = defaultdict(lambda: {"total": 0, "aligned": 0})
    examples_aligned = []
    examples_misaligned = []

    for tf in task_files:
        task_name = os.path.basename(tf)
        steps = load_task_steps(tf)

        for step in steps:
            total += 1
            act = step["action_type"]
            by_action[act]["total"] += 1

            is_aligned, matched_pat = check_alignment(step, patterns)
            if is_aligned:
                aligned += 1
                by_action[act]["aligned"] += 1
                if len(examples_aligned) < 3:
                    examples_aligned.append({
                        "task": task_name,
                        "target_act": step["target_act"],
                        "elem_context": (step.get("elem_context") or "")[:80],
                        "matched_pattern": matched_pat["desc_raw"] if matched_pat else "N/A",
                        "matched_action": matched_pat["action"] if matched_pat else "N/A",
                    })
            else:
                if len(examples_misaligned) < 3:
                    examples_misaligned.append({
                        "task": task_name,
                        "target_act": step["target_act"],
                        "elem_context": (step.get("elem_context") or "")[:80],
                    })

    rate = (aligned / total * 100) if total > 0 else 0.0

    return {
        "site": site,
        "workflow_patterns": len(patterns),
        "task_files": len(task_files),
        "total_steps": total,
        "aligned_steps": aligned,
        "alignment_rate": rate,
        "by_action": dict(by_action),
        "examples_aligned": examples_aligned,
        "examples_misaligned": examples_misaligned,
    }


def format_results(results: List[dict]) -> str:
    """Format analysis results as a readable report string."""
    lines = []
    lines.append("=" * 78)
    lines.append("  AWM Offline Workflow — Target Action Alignment Analysis")
    lines.append("=" * 78)
    lines.append("")
    lines.append("Heuristic: keyword overlap between workflow pattern descriptions")
    lines.append("           and observation element context for each target action.")
    lines.append("Limitations: label-lag, keyword ambiguity, placeholder fallback,")
    lines.append("             no value-level matching for TYPE/SELECT.")
    lines.append("")

    for r in results:
        if "error" in r:
            lines.append(f"[{r.get('site','?')}] ERROR: {r['error']}")
            lines.append("")
            continue

        site = r["site"]
        lines.append("-" * 78)
        lines.append(f"  Site: {site.upper()}")
        lines.append(f"  Workflow patterns: {r['workflow_patterns']}  |  "
                      f"Task files: {r['task_files']}")
        lines.append("-" * 78)
        lines.append(f"  Total target steps:   {r['total_steps']}")
        lines.append(f"  Aligned steps:        {r['aligned_steps']}")
        lines.append(f"  Alignment rate:       {r['alignment_rate']:.1f}%")
        lines.append("")

        # Breakdown by action type
        lines.append("  Breakdown by action type:")
        lines.append(f"    {'Action':<10} {'Total':>6} {'Aligned':>8} {'Rate':>8}")
        lines.append(f"    {'-'*10} {'-'*6} {'-'*8} {'-'*8}")
        for act in sorted(r["by_action"].keys()):
            info = r["by_action"][act]
            act_rate = (info["aligned"] / info["total"] * 100) if info["total"] > 0 else 0
            lines.append(f"    {act:<10} {info['total']:>6} {info['aligned']:>8} "
                          f"{act_rate:>7.1f}%")
        lines.append("")

        # Examples
        if r["examples_aligned"]:
            lines.append("  Aligned examples:")
            for ex in r["examples_aligned"]:
                lines.append(f"    [{ex['task']}] {ex['target_act']}")
                lines.append(f"      elem context: \"{ex['elem_context']}\"")
                lines.append(f"      matched wf:   \"{ex['matched_pattern']}\" -> {ex['matched_action']}")
            lines.append("")

        if r["examples_misaligned"]:
            lines.append("  Misaligned examples:")
            for ex in r["examples_misaligned"]:
                lines.append(f"    [{ex['task']}] {ex['target_act']}")
                lines.append(f"      elem context: \"{ex['elem_context']}\"")
            lines.append("")

    # Summary table
    lines.append("=" * 78)
    lines.append("  SUMMARY TABLE")
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"  {'Site':<12} {'Patterns':>9} {'Tasks':>6} "
                  f"{'Steps':>6} {'Aligned':>8} {'Rate':>8}")
    lines.append(f"  {'-'*12} {'-'*9} {'-'*6} {'-'*6} {'-'*8} {'-'*8}")

    total_all = 0
    aligned_all = 0
    for r in results:
        if "error" in r:
            lines.append(f"  {r.get('site','?'):<12} {'ERROR':>9}")
            continue
        total_all += r["total_steps"]
        aligned_all += r["aligned_steps"]
        lines.append(f"  {r['site']:<12} {r['workflow_patterns']:>9} "
                      f"{r['task_files']:>6} {r['total_steps']:>6} "
                      f"{r['aligned_steps']:>8} {r['alignment_rate']:>7.1f}%")

    overall = (aligned_all / total_all * 100) if total_all > 0 else 0
    lines.append(f"  {'-'*12} {'-'*9} {'-'*6} {'-'*6} {'-'*8} {'-'*8}")
    lines.append(f"  {'OVERALL':<12} {'':>9} {'':>6} {total_all:>6} "
                  f"{aligned_all:>8} {overall:>7.1f}%")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Compute workflow-target action alignment rates for AWM experiments."
    )
    # Default paths assume the script is run from the AWM project root
    # i.e.  capabilities/memory/2024_AWM/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_base = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    parser.add_argument(
        "--base", default=default_base,
        help="Base directory of the 2024_AWM project "
             "(default: inferred from script location)"
    )
    parser.add_argument(
        "--sites", nargs="+", default=SITES,
        help=f"Sites to analyze (default: {' '.join(SITES)})"
    )
    parser.add_argument(
        "--output", default=None,
        help="Write output to this file (in addition to stdout)"
    )

    args = parser.parse_args()

    workflow_dir = os.path.join(args.base, "experiments", "mind2web", "workflow")
    results_dir = os.path.join(
        args.base, "experiments", "mind2web", "results", "gpt-4o", "test_task"
    )

    print(f"Base directory: {args.base}")
    print(f"Workflow dir:   {workflow_dir}")
    print(f"Results dir:    {results_dir}")
    print()

    all_results = []
    for site in args.sites:
        r = analyze_site(site, workflow_dir, results_dir)
        all_results.append(r)

    report = format_results(all_results)
    print(report)

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(f"Base directory: {args.base}\n")
            f.write(f"Workflow dir:   {workflow_dir}\n")
            f.write(f"Results dir:    {results_dir}\n\n")
            f.write(report)
        print(f"\nOutput saved to: {args.output}")


if __name__ == "__main__":
    main()
