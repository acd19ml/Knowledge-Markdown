"""Convert text workflows into code-style prompt workflows."""

import argparse
import os
import re


HEADER_RE = re.compile(r"^##\s+([A-Za-z0-9_]+)\s*$")
STEP_RE = re.compile(
    r"^\[(?P<tag>[^\]]+)\]\s+\{?(?P<element>[^}\n]+)\}?\s*->\s*(?P<op>CLICK|TYPE|SELECT)(?::\s*\{?(?P<arg>[^}\n]+)\}?)?\s*$"
)


def normalize_identifier(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", text.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        return "arg"
    if cleaned[0].isdigit():
        cleaned = f"arg_{cleaned}"
    return cleaned.lower()


def collect_args(steps: list[dict]) -> list[str]:
    ordered = []
    seen = set()
    for step in steps:
        for raw in [step["element"], step.get("arg")]:
            if raw is None:
                continue
            value = normalize_identifier(raw)
            if value not in seen:
                seen.add(value)
                ordered.append(value)
    return ordered


def parse_workflows(text: str) -> list[dict]:
    workflows = []
    current = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.lower().startswith("## summary workflows"):
            continue

        header = HEADER_RE.match(line)
        if header:
            if current is not None:
                workflows.append(current)
            current = {"name": header.group(1), "doc": "", "steps": []}
            continue

        if current is None:
            continue

        if line.lower().startswith("given that"):
            current["doc"] = line
            continue

        step = STEP_RE.match(line)
        if step:
            current["steps"].append(
                {
                    "tag": step.group("tag").strip(),
                    "element": step.group("element").strip(),
                    "op": step.group("op").strip(),
                    "arg": step.group("arg").strip() if step.group("arg") else None,
                }
            )

    if current is not None:
        workflows.append(current)
    return workflows


def render_code_workflow(workflow: dict) -> str:
    args = collect_args(workflow["steps"])
    signature = ", ".join(args)
    lines = [f"def {workflow['name']}({signature}):"]
    if workflow["doc"]:
        lines.append(f'    """{workflow["doc"]}"""')
    for step in workflow["steps"]:
        element = normalize_identifier(step["element"])
        if step["arg"] is None:
            lines.append(f"    {step['op']}({element})")
        else:
            arg = normalize_identifier(step["arg"])
            lines.append(f"    {step['op']}({element}, {arg})")
    return "\n".join(lines)


def build_output(text: str) -> str:
    workflows = parse_workflows(text)
    rendered = [render_code_workflow(workflow) for workflow in workflows if workflow["steps"]]
    return "\n\n".join(rendered).strip() + ("\n" if rendered else "")


def resolve_output_path(args) -> str:
    if args.output_path:
        return args.output_path
    filename = os.path.basename(args.input_path)
    stem, _ = os.path.splitext(filename)
    return os.path.join(os.path.dirname(args.input_path), f"{stem}_code.txt")


def main():
    with open(args.input_path, "r") as f:
        source = f.read()

    rendered = build_output(source)
    output_path = resolve_output_path(args)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(rendered)
    print(f"Saved code workflow to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default=None)
    args = parser.parse_args()
    main()
