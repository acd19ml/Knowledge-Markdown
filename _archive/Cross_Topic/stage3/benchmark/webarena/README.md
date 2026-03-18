# WebArena Benchmark Workspace

> **Status**: Source-grounded pilot binding in place
> **Target Output**: 把 [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md) 中的 pilot slots 绑定到真实 `task id / page path / site / interaction motif`

## What Is Missing

当前不再缺官方 task 级原始信息，已经具备：

- 官方 benchmark 论文
- 官方 `test.raw.json`
- task 级 `task_id / site / start_url / intent / intent_template_id`

当前仍然缺少，且被明确延后到下一阶段的信息：

- generated config 展开的真实 URL / page path
- browser walkthrough 验证后的 motif 命中检查
- final holdout / leakage audit

## What To Add Here

建议把以下材料放进这个目录：

- `webarena-paper.pdf`
- `official-task-list.md` 或导出的 task 表
- `site-map.md` 或站点路径说明
- `task-binding-notes.md`

## Extracted Artifacts

- [webarena-paper-extraction.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-paper-extraction.md)
- [webarena-task-binding-prep.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-task-binding-prep.md)
- [webarena-task-binding.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-task-binding.md)
- [webarena-motif-audit.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-motif-audit.md)
- [task-453-route-check.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/task-453-route-check.md)
- [webarena_extracted.txt](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena_extracted.txt)
- [webarena_extracted_clean.txt](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena_extracted_clean.txt)

## Next Step

当前建议按以下顺序继续：

1. 解析 generated config，把 placeholder token 展开成真实 URL / page path，优先覆盖新引入的 `task 453`
2. 对 [webarena-task-binding.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-task-binding.md) 中的 24 个 task 做 browser walkthrough
3. 完成 stronger motif hit 检查与 route-level leakage audit
4. 若实现阶段需要压力测试，可把 `task 774` 作为 `dev-only` 额外案例

Current note:

- `task 453` has passed a repo-grounded route-level sanity check, see [task-453-route-check.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/task-453-route-check.md).
- live browser verification is still pending because the local Docker daemon is not currently running.
