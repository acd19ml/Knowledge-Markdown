"""Online Induction and Workflow Utilization Pipeline."""

import argparse
import json
import os
import subprocess
import time
from shutil import copyfile
from utils.data import load_json


def run_command(cmd: list[str], label: str, retries: int, retry_delay: float):
    for attempt in range(retries + 1):
        process = subprocess.Popen(cmd)
        process.wait()
        if process.returncode == 0:
            return

        if attempt >= retries:
            raise RuntimeError(f"{label} failed after {retries + 1} attempts.")

        wait_seconds = retry_delay * (2**attempt)
        print(
            f"{label} failed with exit code {process.returncode}. "
            f"Retrying in {wait_seconds:.1f}s ({attempt + 1}/{retries + 1})..."
        )
        time.sleep(wait_seconds)


def get_existing_indices(results_dir: str) -> list[int]:
    if not os.path.isdir(results_dir):
        return []

    indices = []
    for filename in os.listdir(results_dir):
        if not filename.endswith(".json"):
            continue
        stem = filename[:-5]
        if stem.isdigit():
            indices.append(int(stem))
    return sorted(indices)


def get_completed_prefix(results_dir: str) -> int:
    indices = get_existing_indices(results_dir)
    if not indices:
        return 0

    expected = 0
    for idx in indices:
        if idx == expected:
            expected += 1
            continue
        raise ValueError(
            f"Non-contiguous result files found in [{results_dir}]. "
            f"Expected index {expected}, found {idx}. Clean up or repair before resuming."
        )
    return expected


def assert_range_completed(results_dir: str, start_idx: int, end_idx: int):
    existing = set(get_existing_indices(results_dir))
    missing = [idx for idx in range(start_idx, end_idx) if idx not in existing]
    if missing:
        raise RuntimeError(
            f"Missing result files in [{results_dir}] for indices: {missing}."
        )


def get_state_paths(results_dir: str, workflow_path: str):
    state_path = os.path.join(results_dir, "_pipeline_state.json")
    checkpoint_path = workflow_path + ".checkpoint"
    return state_path, checkpoint_path


def save_resume_state(results_dir: str, workflow_path: str, next_start_idx: int):
    state_path, checkpoint_path = get_state_paths(results_dir, workflow_path)
    os.makedirs(results_dir, exist_ok=True)
    if os.path.exists(workflow_path):
        copyfile(workflow_path, checkpoint_path)
    with open(state_path, "w") as fw:
        json.dump({"next_start_idx": next_start_idx}, fw)


def load_resume_state(results_dir: str, workflow_path: str):
    state_path, checkpoint_path = get_state_paths(results_dir, workflow_path)
    if not os.path.exists(state_path):
        return None
    state = json.load(open(state_path, "r"))
    if "next_start_idx" not in state:
        raise ValueError(f"Invalid pipeline state file: {state_path}")
    if not os.path.exists(checkpoint_path):
        raise ValueError(
            f"Missing workflow checkpoint for resume: {checkpoint_path}"
        )
    return state


def restore_workflow_checkpoint(workflow_path: str, checkpoint_path: str):
    if os.path.exists(checkpoint_path):
        copyfile(checkpoint_path, workflow_path)


def remove_result_files_from(results_dir: str, start_idx: int):
    for idx in get_existing_indices(results_dir):
        if idx >= start_idx:
            os.remove(os.path.join(results_dir, f"{idx}.json"))

def offline():
    # workflow induction
    run_command([
        'python', 'offline_induction.py',
        '--mode', 'auto', '--website', args.website,
        '--domain', args.domain, '--subdomain', args.subdomain,
        '--model_name', args.model, '--output_dir', "workflow",
        '--instruction_path', args.instruction_path,
        '--one_shot_path', args.one_shot_path,
    ], "offline induction", args.command_retries, args.retry_delay)

    # test inference
    run_command([
        'python', 'run_mind2web.py',
        '--website', args.website,
        '--workflow_path', f"workflow/{args.website}.txt",
        '--model', args.model,
    ], "offline inference", args.command_retries, args.retry_delay)


def online():
    result_suffix = os.path.basename(os.path.normpath(args.results_dir))
    expected_tail = os.path.join(args.model, args.benchmark, args.website, result_suffix)
    normalized_results_dir = os.path.normpath(args.results_dir)
    if normalized_results_dir.endswith(expected_tail):
        log_dir = normalized_results_dir[: -len(expected_tail)].rstrip(os.sep) or "."
    else:
        log_dir = "results"

    os.makedirs(args.results_dir, exist_ok=True)
    workflow_dir = os.path.dirname(args.workflow_path)
    if workflow_dir:
        os.makedirs(workflow_dir, exist_ok=True)
    state_path, checkpoint_path = get_state_paths(args.results_dir, args.workflow_path)

    # load all examples for streaming
    samples = load_json(args.data_dir, args.benchmark)
    print(f"Loaded #{len(samples)} test examples")
    if args.website is not None:
        samples = [s for s in samples if s["website"] == args.website]
        print(f"Filtering down to #{len(samples)} examples on website [{args.website}]")
    n = len(samples)
    
    if args.resume:
        state = load_resume_state(args.results_dir, args.workflow_path)
        if state is None:
            if get_existing_indices(args.results_dir):
                raise RuntimeError(
                    "Resume requested, but no safe checkpoint exists. "
                    "Clean results and restart once, or create a checkpoint with the updated pipeline."
                )
            start_from = 0
            save_resume_state(args.results_dir, args.workflow_path, next_start_idx=0)
        else:
            start_from = int(state["next_start_idx"])
            restore_workflow_checkpoint(args.workflow_path, checkpoint_path)
            remove_result_files_from(args.results_dir, start_from)
            print(f"Resuming online pipeline from example index {start_from}.")
    else:
        start_from = 0
        save_resume_state(args.results_dir, args.workflow_path, next_start_idx=0)

    if start_from >= n:
        print("All examples already completed.")
        return

    for i in range(start_from, n, args.induce_steps):
        j = min(n, i + args.induce_steps)
        print(f"Running inference on {i}-{j} th example..")

        run_command([
            'python', 'run_mind2web.py',
            '--benchmark', args.benchmark,
            '--workflow_path', args.workflow_path,
            '--website', args.website, 
            '--start_idx', f'{i}', '--end_idx', f'{j}',
            '--domain', args.domain, '--subdomain', args.subdomain,
            '--model', args.model,
            '--log_dir', log_dir,
            '--suffix', result_suffix,
        ], f"online inference {i}-{j}", args.command_retries, args.retry_delay)
        assert_range_completed(args.results_dir, i, j)
        print(f"Finished inference on {i}-{j} th example!\n")

        if j < len(samples):
            run_command([
                'python', 'online_induction.py',
                '--benchmark', args.benchmark,
                '--website', args.website,
                '--results_dir', args.results_dir,
                '--output_path', args.workflow_path,
                '--model_name', args.model,
            ], f"online induction 0-{j - 1}", args.command_retries, args.retry_delay)
            if not os.path.exists(args.workflow_path) or os.path.getsize(args.workflow_path) == 0:
                raise RuntimeError(f"Workflow file [{args.workflow_path}] missing or empty after induction.")
            save_resume_state(args.results_dir, args.workflow_path, next_start_idx=j)
            print(f"Finished workflow induction with 0-{j - 1} th examples!\n")
        else:
            save_resume_state(args.results_dir, args.workflow_path, next_start_idx=j)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # examples
    parser.add_argument("--data_dir", type=str, default="data")
    parser.add_argument("--benchmark", type=str, default="test_task",
        choices=["test_task", "test_website", "test_domain", "train"])
    parser.add_argument("--website", type=str, required=True)
    parser.add_argument("--domain", type=str, default=None)
    parser.add_argument("--subdomain", type=str, default=None)

    # results and workflows
    parser.add_argument("--results_dir", type=str, default=None)
    parser.add_argument("--workflow_path", type=str, default=None)

    # prompt
    parser.add_argument("--instruction_path", type=str, default="prompt/instruction_action.txt")
    parser.add_argument("--one_shot_path", type=str, default="prompt/one_shot_action.txt")
    parser.add_argument("--prefix", type=str, default=None)
    parser.add_argument("--suffix", type=str, default="# Summary Workflows")

    # gpt
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--temperature", type=str, default=0.0)

    # induction frequency
    parser.add_argument("--induce_steps", type=int, default=1)
    parser.add_argument("--command_retries", type=int, default=2)
    parser.add_argument("--retry_delay", type=float, default=5.0)
    parser.add_argument("--resume", action="store_true")

    # setup
    parser.add_argument("--setup", type=str, required=True,
                        choices=["online", "offline"])

    args = parser.parse_args()

    if args.setup == "online":
        assert (args.results_dir is not None) and (args.workflow_path is not None)
        online()
    elif args.setup == "offline":
        assert (args.domain is not None) and (args.subdomain is not None)
        offline()
