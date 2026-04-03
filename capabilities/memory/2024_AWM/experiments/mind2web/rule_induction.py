"""Induce website-specific workflows with rule-based heuristics."""

import argparse
import json
import os
import random

from utils.env import get_target_obs_and_act, parse_act_str


def get_data_dict(paths: list[str]) -> dict:
    """Create dict for examples in domain-subdomain-website hierarchy."""
    print("Start loading data files...")
    data_dict = {}
    for path in paths:
        print(path)
        with open(path, "r") as f:
            data = json.load(f)
        for ex in data:
            domain, subdomain, website = ex["domain"], ex["subdomain"], ex["website"]
            data_dict.setdefault(domain, {}).setdefault(subdomain, {}).setdefault(website, []).append(ex)
    print(f"Finished loading {len(paths)} files!")
    return data_dict


def get_examples(data_dict: dict, tags: tuple[str, str, str]) -> list[dict]:
    domain, subdomain, website = tags
    return data_dict[domain][subdomain][website]


def get_action_sequence(example: dict) -> tuple[str, ...]:
    return tuple(step["operation"]["op"] for step in example["actions"])


def is_valid_concrete_action(step: dict) -> bool:
    op = step["operation"]["op"]
    if op not in {"CLICK", "TYPE"}:
        return True
    try:
        _, target_act = get_target_obs_and_act(step)
    except Exception:
        return False
    _, target_id, _ = parse_act_str(target_act)
    return isinstance(target_id, str) and target_id.isdigit()


def filter_invalid_steps(example: dict) -> list[str]:
    kept = []
    for step, act_repr in zip(example["actions"], example["action_reprs"]):
        if is_valid_concrete_action(step):
            kept.append(act_repr.strip())
    return kept


def deduplicate_examples(examples: list[dict], sample_per_group: int, seed: int) -> list[dict]:
    grouped = {}
    for ex in examples:
        grouped.setdefault(get_action_sequence(ex), []).append(ex)

    rng = random.Random(seed)
    selected = []
    for key in sorted(grouped, key=lambda seq: (len(seq), seq)):
        group = sorted(grouped[key], key=lambda ex: ex["annotation_id"])
        if len(group) <= sample_per_group:
            selected.extend(group)
        else:
            selected.extend(rng.sample(group, sample_per_group))
    return selected


def build_workflow_block(example: dict, workflow_id: int) -> str | None:
    steps = filter_invalid_steps(example)
    if not steps:
        return None

    title = f"## Workflow {workflow_id}: Concrete Trajectory for {example['confirmed_task']}"
    doc = (
        "Given that you are solving a similar task on this website, "
        "follow this concrete action trajectory."
    )
    lines = [title, doc]
    lines.extend(f"- {step}" for step in steps)
    lines.append("This workflow preserves a concrete trajectory after deduplication and invalid-action filtering.")
    return "\n".join(lines)


def build_rule_workflows(examples: list[dict], sample_per_group: int, seed: int) -> str:
    selected_examples = deduplicate_examples(examples, sample_per_group=sample_per_group, seed=seed)
    print(f"Collected #{len(selected_examples)} unique experiences after deduplication")

    blocks = []
    for workflow_id, ex in enumerate(selected_examples, start=1):
        block = build_workflow_block(ex, workflow_id)
        if block is not None:
            blocks.append(block)
    print(f"Generated #{len(blocks)} rule workflows after invalid-action filtering")
    return "\n\n".join(blocks)


def resolve_output_path(args) -> str:
    if args.output_path is not None:
        return args.output_path

    output_name = (
        f"{args.website.lower()}_{args.output_suffix}.txt"
        if args.output_suffix is not None
        else f"{args.website.lower()}.txt"
    )
    return os.path.join(args.output_dir, output_name)


def main():
    data_paths = sorted(
        [
            os.path.join(args.data_dir, filename)
            for filename in os.listdir(args.data_dir)
            if filename.endswith(".json")
        ]
    )
    data_dict = get_data_dict(paths=data_paths)
    examples = get_examples(data_dict, tags=(args.domain, args.subdomain, args.website))
    print(f"Split {(args.domain, args.subdomain, args.website)} with #{len(examples)} examples")

    workflows = build_rule_workflows(
        examples,
        sample_per_group=args.sample_per_group,
        seed=args.seed,
    )

    output_path = resolve_output_path(args)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(workflows)
    print(f"Saved workflows to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="data/train")
    parser.add_argument("--domain", type=str, required=True)
    parser.add_argument("--subdomain", type=str, required=True)
    parser.add_argument("--website", type=str, required=True)
    parser.add_argument("--output_path", type=str, default=None)
    parser.add_argument("--output_dir", type=str, default="workflow")
    parser.add_argument("--output_suffix", type=str, default="rule_wf")
    parser.add_argument("--sample_per_group", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    main()
