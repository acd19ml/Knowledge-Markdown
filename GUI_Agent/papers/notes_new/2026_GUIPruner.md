# GUIPruner — Spatio-temporal token pruning for efficient pure-vision GUI agents

## Meta
- **Title**: Spatio-Temporal Token Pruning for Efficient High-Resolution GUI Agents
- **Authors**: Zhou Xu et al. | Tsinghua University + Xidian University + CUHK
- **Venue**: Preprint, 2026 | arXiv:2602.23235
- **Links**: [PDF](../source_todo/Spatio-Temporal-Token-Pruning.pdf) | Code: not listed in PDF | Project: not listed in PDF
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-06
- **Priority**: P1 | **Reading progress**: Pass 1

## One-line Summary
GUIPruner 针对高分辨率 pure-vision GUI agents 中的时空冗余，提出 TAR + SSP 两级 training-free token compression，在保持 94%+ 原始性能的同时实现 3.4x FLOPs reduction、3.3x encoder speedup，并显著缓解大模型在 Mind2Web 上的 pruning collapse（Abstract / Table 1-2, p.1-2, p.6-7）。

## Problem Setting
- **Core problem**: existing compression methods mis-handle GUI-specific redundancy because of "the temporal mismatch" and "the spatial topology conflict" (Abstract, p.1)
- **Assumptions**: GUI attention 对历史具有 recency bias / fading memory；当前帧不能只做无结构 token pruning，因为坐标 grounding 依赖 2D topology；训练后分布不应被激进 pre-LLM pruning 破坏（Section 1, p.1-2）。
- **Insufficiency of existing approaches**: unstructured pruning "compromises the grid integrity required for precise coordinate grounding, inducing spatial hallucinations" (Abstract, p.1)

## Core Method
- **Method overview**: GUIPruner 把 GUI compression 拆成两个不同问题。对历史帧，作者认为不需要统一高分辨率，因为 attention 天然偏向最近帧，因此提出 Temporal-Adaptive Resolution (TAR)，按 temporal decay 分配历史 token budget，远处历史只保留低分辨率语义轮廓。对当前帧，则提出 Stratified Structure-aware Pruning (SSP)，优先保留可交互 foreground 与 semantic anchors，并保留 coarse uniform grid，确保 layout topology 不会被打碎。

  这种 decoupled design 与通用 VLM pruning 最大不同在于，它承认 GUI grounding 是 coordinate-sensitive 的。历史上下文需要“时间上衰减”，当前界面需要“空间上成骨架”。两者若都用同一种 token selection 规则，就会要么浪费算力、要么损坏 grounding。
- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| History compression | TAR with temporal decay | 对齐 GUI agent 的 recency-biased attention | Yes |
| Current-frame pruning | SSP with foreground + background saliency + uniform grid | 保住 spatial topology，避免 hallucination | Yes |
| Deployment mode | Training-free plug-in | 降低接入门槛，适配现有 GUI agents | Indirectly verified |
| Pruning stage | Current frame pruned in shallow layers | 减少分布偏移，避免 large-scale collapse | Yes |

- **Core difference from prior work**: 与 FastV / DivPrune / CDPruner / MoB 等通用视觉压缩不同，GUIPruner 显式把 GUI token compression 设计成 topology-aware、history-aware 的特殊问题，而不是沿用 generic attention-based pruning（Section 1, 5.3-5.5, p.1-7）。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| Qwen2-VL-2B, AITW (40%/75%) | 67.5 | FastV 66.2 | +1.3 | Original full-token upper bound 69.5 (Table 1, p.6) |
| Qwen2-VL-2B, Mind2Web (40%/75%) | 33.6 | FastV 33.4 | +0.2 | Much higher than DivPrune/CDPruner (Table 1, p.6) |
| Qwen2.5-VL-7B, Mind2Web (40%/75%) | 34.7 | FastV 34.3 | +0.4 | Avoids collapse to 7.7 / 6.8 seen in baselines (Table 1, p.6) |
| FLOPs (Qwen2-VL-2B) | 3.4 | Base 11.5 | 3.4x lower | Table 2, p.7 |
| Encoder latency (Qwen2-VL-2B) | 26.6 ms | Base 87.9 ms | 3.3x faster | Table 2, p.7 |
| GPU memory (Qwen2-VL-2B) | 5902 MB | Base 8956 MB | -3054 MB | Table 2, p.7 |

- **Key ablation findings**: TAR consistently beats uniform history allocation across retention ratios；SSP 中保留 deterministic uniform grid 明显优于 random sampling；最佳 pruning depth 出现在较浅层，因为过浅或过深都会伤害 grounding（Section 5.5-5.6, p.7-8）。
- **Failure cases**: Baselines 在 Mind2Web 等高稀疏、高分辨率任务上会出现 catastrophic collapse，尤其是 7B 模型上的 pre-LLM pruning；GUIPruner 的提出本身就是在修复这种 failure mode（Table 1 / Section 5.3, p.6）。

## Limitations
- **Author-stated limitations**: "there exists a theoretic lower bound to token reduction" and aggressive compression inevitably discards fine-grained cues, so performance degradation becomes unavoidable beyond the Pareto frontier (Limitations, p.14)
- **My observed limitations**: 
> ⚠️ NEEDS YOUR INPUT: (1) 这篇优化的是视觉编码成本，而不是高层规划，所以它更像底层加速模块，不会直接解决 GUI agent 的 intent / memory 问题。(2) 实验仍主要围绕 Qwen 系列 backbone，跨模型稳定性还需更多验证。(3) 论文题目强调 high-resolution GUI，但对 OCR-heavy 或极端动态场景的收益没有单独拆解。
- **Experimental design gaps**: 缺少与 end-to-end textual / DOM agents 的整体系统级成本对比；也未分析压缩对 downstream reflection / self-correction 模块的影响。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 适合放在 **Efficiency / Perception Optimization** 小节，作为 pure-vision GUI agent 的底层系统优化工作。
- **Role**: Positive example / Background reference

### Gap Signals (extracted from this paper)
- Gap signal 1: "highresolution, lowattention" configuration wastes computation (Section 1, p.1-2) → 历史帧处理仍有明显结构性浪费。
- Gap signal 2: baseline methods collapse on Mind2Web for 7B models (Table 1, p.6) → 通用视觉 pruning 在 GUI grounding 上并不可靠。
- Gap signal 3: even GUIPruner admits a lower bound to compression (Limitations, p.14) → efficiency 与 grounding fidelity 之间存在不可消除的信息瓶颈。

> ⚠️ NEEDS YOUR INPUT: 如果你的 survey 主线不聚焦系统优化，可以把它作为 supporting evidence，用来说明 pure-vision GUI agents 的扩展性问题真实存在。

### Reusable Elements
- **Methodology**: TAR 的 recency-aware token budgeting、SSP 的 topology-preserving pruning，都可作为 GUI encoder 前端模块复用。
> ⚠️ NEEDS YOUR INPUT: 我更看重它的分析框架，即把 GUI compression 分成 history 与 current-frame 两类完全不同的问题，而不是照搬具体超参。
- **Experimental design**: 同时汇报 accuracy、FLOPs、encoder latency、prefill latency、GPU memory，是效率论文应有的完整评价方式。

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 可与 [2026_M2](./2026_M2.md) 对比“视觉 token 压缩 vs 文本/轨迹记忆压缩”；与 [2025_MobileAgentV3](../notes/2025_MobileAgentV3.md) 的历史图像消融结果形成呼应。

## Citation Tracking
- [ ] FastV / DivPrune / CDPruner / MoB: 通用 pruning baseline
- [ ] AITW / Mind2Web / GUI-Odyssey / AndroidControl: benchmark 差异
- [ ] Qwen2-VL / Qwen2.5-VL: backbone 与压缩鲁棒性关系

## Key Passages
> "the temporal mismatch" and "the spatial topology conflict" (Abstract, p.1)

> "our method delivers a 3.4× reduction in FLOPs and a 3.3× speedup in vision encoding latency" (Abstract, p.1)

> "there exists a theoretic lower bound to token reduction" (Limitations, p.14)
