# Pass 2 Audit Checklist

Use this checklist after the note draft is complete. The goal is not "template filled", but "this note can support survey writing and KB updates without re-reading the paper."

## Promotion Rule

- Keep `Reading progress: Pass 1` by default.
- Upgrade to `Pass 2` only when every `Hard Gate` item passes.
- Re-audit existing `Pass 2` notes with the same checklist; old labels do not count as evidence.
- If any `Hard Gate` fails, keep `Pass 1` and list the blocking items in the delivery message.
- If an existing `Pass 2` note fails the audit, downgrade it back to `Pass 1` until the evidence chain is repaired.
- Even if all `Hard Gate` items pass, downgrade back to `Pass 1` if the note still cannot support `comparison-matrix` / `gap-tracker` updates without reopening the paper.
- If any decision-critical quote or page number looks doubtful, reopen the PDF and verify it before keeping `Pass 2`.

## Hard Gates

- [ ] **One-line Summary** includes all 4 parts: subject + method + benchmark + concrete number
- [ ] **Problem Setting** contains direct textual evidence with section and page for both:
  - the core problem
  - the insufficiency of existing approaches
- [ ] **Key Design Choices** table is filled, and each row marks whether it is ablation-verified
- [ ] **My observed limitations** includes at least one observation not explicitly stated by the authors
- [ ] **Gap Signals** are backed by original quotes or specific result numbers with section and page
- [ ] **Connections to Other Papers in Knowledge Base** names at least one concrete paper/file and explains the relation

## Evidence Quality

- [ ] Quotes are precise enough to be checked quickly; no vague "paper says..." paraphrases
- [ ] Section and page references are present in all core evidence fields, or explicitly marked `位置待确认`
- [ ] Decision-critical quotes can be traced to the original PDF without ambiguity
- [ ] Key Results table contains benchmark names, strongest baselines, and deltas where possible
- [ ] Key Passages includes 1-3 passages that are actually reusable for later argumentation
- [ ] Fewer than 3 unresolved `位置待确认` markers remain in decision-critical sections

## Re-check Against PDF

- [ ] For any shaky `Pass 2` claim, the original PDF was reopened and checked
- [ ] If the PDF was reopened, a clean extracted text file was saved under `<topic>/papers/text/<pdf-stem>_clean.txt`
- [ ] The saved text keeps page markers and removes obvious extraction noise
- [ ] After re-checking, all survey-critical quotes and numbers still match the note

## Method Understanding

- [ ] Method overview is written in your own words, not copied from abstract/introduction
- [ ] The note distinguishes core design choices from implementation details
- [ ] At least one unablated or weakly justified design choice is identified when applicable
- [ ] Failure cases or boundary conditions are captured, not just success metrics

## Critical Reading

- [ ] Experimental design gaps are specific: benchmark coverage, baseline omissions, metric bias, or setup mismatch
- [ ] At least one limitation is framed as a research opportunity, not just a complaint
- [ ] The note separates author claims from your inference clearly

## Research Integration

- [ ] `Position in Survey` is specific enough to place the paper into a survey section/category
- [ ] `Role` is explicit: positive example / contrastive baseline / background reference
- [ ] `Reusable Elements` identifies a concrete module, mechanism, or evaluation design
- [ ] Reuse notes explain how the element might transfer, not just that it is "useful"
- [ ] Citation Tracking contains at least one meaningful follow-up paper

## Knowledge Base Readiness

- [ ] You can add or update one row in `Cross_Topic/comparison-matrix.md` using this note alone
- [ ] You can decide whether the paper adds a new gap signal or new evidence for an existing gap
- [ ] The note is specific enough that you do not need to reopen the PDF to justify those updates
- [ ] The note is specific enough that you can write a survey paragraph from it without reopening the PDF

## Decision

### Mark as Pass 2

Use `Pass 2` only if:

- [ ] All `Hard Gates` pass
- [ ] All `Re-check Against PDF` items that were triggered have passed
- [ ] At least 10 checklist items outside `Hard Gates` pass
- [ ] The note can directly support survey writing and KB updates

### Keep as Pass 1

Keep `Pass 1` if any of these is true:

- [ ] Any `Hard Gate` item fails
- [ ] Any triggered PDF re-check fails or remains ambiguous
- [ ] Core evidence still depends on paraphrase without exact location
- [ ] Research linkage is still provisional and too vague to update the KB
- [ ] You would still need to reopen the paper to explain the method, limitations, or gap value

## Common Failure Modes

### Looks complete, but is still Pass 1

- Template sections are all filled, but `Gap Signals` are mostly inference with no exact quote/data
- There is a method summary, but no clear design-choice-to-ablation mapping
- `My observed limitations` repeats the authors' limitation section in different words
- Research relation says "relevant to my topic" but does not name a section, gap, or connected paper
- The note says `Pass 2`, but key quotes cannot be confidently verified from the PDF on re-check

### Concrete ✗/✓ examples by dimension

**One-line Summary**
- ✗ "本文提出了一种新的 GUI Agent 框架，取得了较好效果。"
- ✓ "CogAgent 通过双视觉编码器（高分辨率 1120px + 低分辨率语义流），在 Mind2Web 上达到 19.4% SR，超越 GPT-4V 的 15.7%（Δ = +3.7%）。"

**Problem Setting**
- ✗ "现有方法难以处理复杂的 GUI 界面，因为分辨率不足。"（自己总结，无出处）
- ✓ **"existing LVLMs suffer from excessively low resolution… making text and icons on GUI screenshots unrecognizable"** (Section 1, p.2)；并标注作者假设：输入为单张截图，不依赖 accessibility tree。

**Core Method**
- ✗ "We propose a novel framework that leverages..."（直接照抄 abstract）
- ✓ 中文重描：CogAgent 把 GUI 理解拆成两条路径——高分辨率路径捕捉细节（小字体、图标），低分辨率路径保留语义全局信息，两路通过交叉注意力融合后由 LLM 解码动作。与"一张图进一个编码器"的传统做法的区别在于……

**Key Results**
- ✗ "在 Mind2Web 和 AITW 上优于 baseline。"
- ✓ 填写 Key Results 表格，含 Δ 列：Mind2Web SR 19.4% vs GPT-4V 15.7%，**Δ = +3.7%**；消融：去掉高分辨率编码器后 SR 下降 4.2%，是贡献最大的单一组件；同时标出哪些设计**未被消融**（潜在 gap）。

**Limitations**
- ✗ "作者指出方法对动态内容处理不足，未来工作将扩展到视频输入。"（只复述作者）
- ✓ 补充一条"我观察到的"：测试集平均步骤数 < 5，无法说明长序列表现；未与 2024 年后的 SOTA（如 AppAgent、UFO）做对比。

**Gap Signals**
- ✗ "该论文没有处理跨平台问题，是一个研究 gap。"（推断，无出处）
- ✓ **"we do not address cross-platform generalization and leave it to future work"** (Section 6, p.10) → 作者显式承认，证据等级 A；另：Android 数据占训练集 78%（Table 2, p.6），iOS 任务 SR 低 12%，暗示平台偏差可验证。

**Research Relation**
- ✗ "与本方向相关"
- ✓ "本文的双编码器设计与 Agent_Memory/03_operations.md 中的分层检索方案形成对照：本文侧重感知效率，该文档侧重记忆遗忘机制；两者可组合用于长时任务的 GUI Agent 设计。"

### Strong Pass 2 note

- Core claims are traceable to quotes, tables, and page numbers
- The note identifies what the paper proves, what it does not prove, and why that matters to your RQ
- You can update `comparison-matrix` and `gap-tracker` from the note without reopening the PDF
- You can write the paper into a survey paragraph directly from the note

---

## Pass 3 Definition

`Pass 3` = the note is fully integrated into the knowledge base. All of the following must be true:

- No unresolved placeholders remain in research-facing sections
- Connections to ≥ 2 other papers/files in the KB are established with specific relation type (complement / contrast / extend / precede)
- Each Gap signal has a stable evidence grade (A / B / C) and role in the current main line
- Citation Tracking follow-up papers have been prioritized and scheduled
- The note has been used to update `comparison-matrix` and `gap-tracker` at least once
- The note's language follows the Chinese-analysis / English-evidence split
- You can write a survey paragraph citing this paper without reopening the note more than once
