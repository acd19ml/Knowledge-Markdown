# Multimodal Large Language Models 中的 Visual Grounding 与 Spatial Understanding：方法、表征与 Failure Modes

**英文题名（与 `grounding_review.tex` 一致）**  
*Visual Grounding and Spatial Understanding in Multimodal Large Language Models: Methods, Representations, and Failure Modes*

> 本文档由 `manuscript/archive/` 下的 `grounding_review.tex` / `grounding_review_body.tex`（本地，**不提交 GitHub**）**全文**整理为中文（技术术语保留英文）。结构与小节标题与 TeX **一一对应**；表格与论断尽量逐段覆盖原文。引用键与 `grounding_review_refs.bib` 一致，便于对照。

---

## Abstract

**English（与 `grounding_review.tex` 一致）**

This literature review examines how visual grounding and spatial understanding emerge in multimodal large language models (MLLMs), and why these capabilities still fail under realistic conditions. We organize the recent literature as a capability chain: visual representations determine what spatial structure is preserved, grounding methods convert that structure into usable alignment between language and image regions, spatial reasoning builds on that alignment, and hallucination exposes the failure regime when the chain weakens. Across representative work on encoders, connectors, grounding outputs, spatial benchmarks, and hallucination mitigation, a consistent picture emerges: grounding is the intermediate capability linking multimodal perception to spatial reasoning, while current failures are driven less by a lack of fluent generation than by unstable visual anchoring. The review concludes by highlighting open problems in unified evaluation, 3D-aware reasoning, compositional spatial understanding, and calibration.

**中文**

本综述讨论 **multimodal large language models（MLLMs）** 中 **visual grounding** 与 **spatial understanding** 如何出现，以及为何在真实条件下仍会失效。我们将近期文献组织为一条 **capability chain**：**visual representations** 决定保留何种 **spatial structure**；**grounding methods** 将该结构转化为 **language** 与 **image regions** 之间可用的对齐；**spatial reasoning** 建立在该对齐之上；当链条变弱时，**hallucination** 暴露其 **failure regime**。在 **encoders**、**connectors**、**grounding outputs**、**spatial benchmarks** 与 **hallucination mitigation** 等代表性工作中，反复出现的图景是：**grounding** 是连接 **multimodal perception** 与 **spatial reasoning** 的中间能力；当前失败更多来自 **unstable visual anchoring**，而非单纯缺乏流利的 **generation**。文末强调 **unified evaluation**、**3D-aware reasoning**、**compositional spatial understanding** 与 **calibration** 等开放问题。

**Keywords:** multimodal large language models, visual grounding, spatial reasoning, hallucination, multimodal alignment

---

## 1. Introduction {#sec:introduction}

**Multimodal Large Language Models（MLLMs）** 已从 **captioning** 与 **visual question answering** 快速推进到需要精确 **spatial awareness** 的任务：定位物体、理解物体间的 **spatial relationships**、推理场景的 **3D structure**。从「描述图像里有什么」到「指明在哪里、与其他物体如何相关」，并非小幅增量，而是能力重心从通用 **visual-language interaction** 转向 **grounded perception**。**GUI agent** 必须点到正确按钮，**robotic manipulator** 必须伸向目标物体，**autonomous system** 必须判断行人是在障碍物前还是后。若无可靠的 **grounding** 与 **spatial reasoning**，MLLMs 仍是「碰巧能看见」的流利 **language generators**。

然而近期工作揭示出强烈悖论：MLLMs 能生成细致且语境合理的场景描述，却在基本 **spatial judgments** 上失败——例如哪一物体在另一物体之上、某实体是否真实存在于图像中。**Benchmarks** 显示在基础 **spatial relation** 任务上接近 **chance**（Liu et al., VSR; Kamath et al., What'sUp），**encoder** 层面对 **spatial reasoning** 关键视觉模式「视而不见」（Tong et al., Eyes Wide Shut），并持续 **hallucinate** 图像中不支持的物体、属性与关系（Li et al., POPE; Guan et al., HallusionBench）。这些失败并非孤立病理，而是更深层 **pipeline** 问题：**spatially reliable behavior** 取决于 **representation stack** 保留了何种视觉信息、该信息如何被转化为 **grounding outputs**、以及模型在后续 **reasoning** 与 **generation** 中能否保持 **visual anchoring**。

因此本文核心论断：**grounding 是连接 visual representation 与 spatial reasoning 的中间能力；hallucination 最宜理解为该 pipeline 的 failure regime。** 这一视角决定综述结构：我们不把 **visual encoders**、**grounding methods**、**spatial reasoning** 与 **hallucination** 当作彼此割裂的主题，而将其视为 **spatially grounded MLLM behavior** 之出现与崩溃的相继阶段。

### 1.1 Scope and Contributions {#subsec:intro-scope}

本综述梳理 **MLLMs 中 visual grounding 与 spatial understanding** 的近期工作，聚焦决定 **spatially grounded behavior** 是否出现的架构、表征与训练选择。范围刻意以 **capability** 为中心，而非以应用为中心：我们主要关心下游 **robotics** 或 **GUI agents** 等系统**得以成立的技术条件**，而非这些系统本身。

综述围绕四个相互关联的问题：

1. **何种 visual representations 支撑 grounding？**（第 2 节）  
   考察三阶段 **representation pipeline**：**vision encoder**、**resolution strategy**、**vision-language connector**，它们共同决定从像素到 **LLM token space** 有多少 **spatial structure** 得以保留。在代表性架构中，反复出现的发现是：**grounding** 不仅依赖更强的 **encoder**，还依赖能保留局部 **spatial detail** 的 **connectors** 与 **resolution schemes**，而非一味压缩。

2. **MLLMs 如何完成 grounding？**（第 3 节）  
   追溯 **grounding methods** 从 **coordinate prediction** 作为 **language generation**、到 **region-level grounded interaction**、再到 **segmentation-level outputs** 的演变。贯穿这些范式的是：**保持 MLLM 灵活的 text-in/text-out 接口** 与 **grounding 所需的结构化 spatial prediction** 之间的张力。

3. **MLLMs 能否推理 spatial relations？**（第 4 节）  
   综述诊断性 **benchmarks** 以及针对 **topological**、**directional**、**depth-aware** 推理的近期方法。主要结论是：**grounding** 与 **spatial reasoning** 紧密耦合；显式 **region grounding** 能显著帮助 **spatial reasoning**，但一旦任务涉及 **depth**、**distance** 或 **compositional spatial inference**，仅有 **grounding** 仍不足。

4. **grounding failures 如何表现、传播并化为 hallucination？**（第 5 节）  
   从 **grounding** 视角分析 **hallucination**：**object-existence probing**、**perturbation stress tests**、**language hallucination** 与 **visual illusion** 的诊断分离、**calibration** 与 **confidence**、以及从 **decoding-time correction** 到细粒度 **reward alignment** 的缓解策略。更广泛的含义是：**hallucination** 往往不仅是 **language-generation artifact**，而常反映 **unstable** 或被覆盖的 **grounding**。

上述四个问题共同构成 **capability chain**：**visual representation** 约束可编码的空间信息上界；**grounding methods** 决定编码结构如何成为 **words** 与 **regions** 之间的可用对齐；**spatial reasoning** 在该对齐之上进行比较、推断与规划；**failure modes** 揭示在歧义、弱证据或长文本 **generation** 下链条在何处断裂。第 6 节回到该链条，归纳共享瓶颈与开放问题。

### 1.2 Positioning Within the Literature {#subsec:intro-positioning}

若干近期综述触及相邻领域，但往往只覆盖问题的一侧。TPAMI **visual grounding** 综述（Xiao et al.）给出 broad **taxonomy of grounding tasks**，但重心仍在经典 **detection-era pipeline**，而非 **MLLM-native grounding**。通用 MLLM 综述将 **grounding** 列为众多能力之一，却未追溯其对 **encoder**、**connector**、**resolution** 的架构依赖。**Spatial reasoning** 综述与 **benchmark** 论文则常聚焦 **evaluation**，而未将性能缺口回连到上游 **representation** 与 **grounding** 选择。

本综述填补该空白：将 **grounding** 视为 **perception** 与 **reasoning** 之间的 **middle layer**。贡献并非罗列所有 **multimodal capabilities**，而是解释 **spatially grounded behavior** 如何出现、在何处失败、以及为何在看似不同的任务上失败会重复出现。因此，相较既有综述：范围更窄（聚焦 **visual grounding** 与 **spatial understanding**），但更整合——沿 **representation→failure** 的端到端链条，而非孤立讨论各阶段。

---

## 2. Visual Representations: The Foundation of Grounding {#sec:representations}

若 MLLM 欲将 **language** 锚定到具体 **image regions**，首先必须构建足够丰富的 **visual representation** 以保留细粒度 **spatial detail**。三类架构选择共同决定视觉信息到达 **language model** 时尚存多少 **spatial information**：**(i)** 从原始像素提取特征的 **vision encoder**；**(ii)** 控制 **encoder** 可见细节量的 **resolution** 与 **multi-scale strategy**；**(iii)** 将视觉特征投影到 **LLM token space** 的 **vision-language connector**。本节在八个代表性 MLLM 上逐一考察这些选择，并特别关注其对下游 **grounding** 与 **localization** 的促进或限制。

### 2.1 Vision Encoder Selection {#subsec:rep-encoders}

#### 2.1.1 Language-Supervised Encoders Dominate {#subsubsec:rep-language-supervised}

当前绝大多数 MLLM 以 **CLIP** 家族的 **Vision Transformers（ViTs）** 为视觉骨干。**LLaVA-1.5** 使用 **336 px** 的 **CLIP ViT-L/14**，仍是广泛采用的默认之一。**Qwen-VL** 采用 OpenCLIP 的更大 **ViT-bigG**；**CogVLM** 使用 **EVA2-CLIP-E**——容量更高，但仍属 **language-supervised** 范式。**LLaVA-OneVision** 改用 **SigLIP ViT-SO400M**，以 **sigmoid contrastive loss** 替代 CLIP 的 softmax **InfoNCE**，并报告下游 MLLM 性能一致提升。共同点很明确：经 **contrastive learning** 与 **language** 预对齐的 **encoder**，其特征空间已部分与 **LLM word embedding space** 匹配，因而享有显著先发优势。

#### 2.1.2 Scaling the Vision Encoder {#subsubsec:rep-scaling}

**InternVL** 挑战「约 1B 参数 **vision encoder**」的主流做法，将规模扩展至 **InternViT-6B**（约 5.9B 参数的 ViT），首次在参数规模上接近 **LLM** 组件。其 **progressive alignment**（先在约 5B **image-text pairs** 上做 **contrastive pre-training**，再做 **generative fine-tuning**）在 **perception**（ImageNet linear probing：88.2%）与 **pixel-level understanding**（ADE20K **mIoU**：58.9%，全量微调）上均取得 SOTA 级结果。这些结果暗示：**vision encoder capacity** 在既往 MLLM 中可能是被低估的约束瓶颈——多数系统将约 0.3–1.8B 的 **vision encoder** 与 7–13B 的 **LLM** 配对，导致大量 **LLM capacity** 未被充分利用。

#### 2.1.3 Beyond Language Supervision: Self-Supervised and Hybrid Encoders {#subsubsec:rep-self-supervised-hybrid}

**Cambrian-1** 在受控 MLLM 训练条件下系统评估 **23 种 vision backbones**，涵盖 CLIP 变体、**DINOv2**（**self-supervised**）、**ConvNeXt**、**depth-supervised** 模型与 **diffusion-based representations**。主要发现包括：

- **Language-supervised models** 在通用、知识与 OCR 等 **benchmarks** 上一致优于 **self-supervised**，很大程度上因为 CLIP 训练数据包含大量 **text-heavy images**。
- **DINOv2** 作为最强的 **self-supervised** 模型，在 **vision-centric benchmarks**（**spatial relationship**、**depth order**）上达到有竞争力表现，有时超过较弱 CLIP 变体，说明 **SSL representations** 可捕获 **language-supervised encoders** 可能忽略的 **geometric** 与 **spatial structure**。
- **ConvNet-based architectures**（如 OpenCLIP **ConvNeXt-XXL**）因 **translation-equivariant inductive bias**，天然适合 **high-resolution processing**，在 OCR 与 **vision-centric** 任务上表现突出。
- 通过扩大 **instruction tuning** 数据（0.7M→5M）并在微调时 **unfreeze vision encoder**，**DINOv2** 与 CLIP 的差距可显著**收窄**。

这些发现与 **grounding** 直接相关：准确定位需要保留 **spatial structure**，而仅靠 **language-supervised contrastive objectives** 并不能保证这一点。

**Mini-Gemini** 采用互补的 **dual-encoder** 设计：**CLIP ViT-L** 以低分辨率编码产生 **visual queries**；**ConvNeXt-L** 对同图更高分辨率版本编码以提供丰富 **spatial candidates**。两路通过 **patch-level cross-attention**（「**patch info mining**」）交互：每个低分辨率 query 仅 attend 对应高分辨率子区域，从而在不过度增加送入 **LLM** 的 **token count** 的前提下，用细粒度细节增强 **visual tokens**。

### 2.2 High-Resolution and Multi-Scale Strategies {#subsec:rep-resolution}

对 **grounding** 而言，**resolution**  arguably 是最具影响力的单一因素。在 **224 px** 输入中仅占据少数像素的物体，对模型几乎「不可见」。表 **Resolution strategies across representative MLLMs** 汇总如下。

**Table. Resolution strategies across representative MLLMs**

| Model | Base Resolution | Strategy | Max Effective Resolution |
|--------|-----------------|----------|---------------------------|
| BLIP-2 | 224 px | Fixed | 224 px |
| LLaVA-1.5 | 336 px | Fixed（HD 变体：grid split） | 672×448 |
| Qwen-VL | 224→448 px | Stage-wise increase | 448 px |
| CogVLM | 224→490 px | Stage-wise increase | 490 px |
| InternVL | 448 px（v2：dynamic tile） | Dynamic tiling | 448×N tiles |
| LLaVA-OneVision | 384 px | AnyRes with pooling | Up to 384×36 crops |
| Cambrian-1 | 随 encoder 而异 | Multi-encoder, multi-scale | Up to 1024 px（ConvNeXt） |
| Mini-Gemini | 336 / 672 px（LR） | Dual-encoder：LR query + HR candidate | 1536 px（HR encoder） |

主要可归纳为以下范式（与 TeX 中 **Fixed / Dynamic tiling / Dual-encoder / Stage-wise** 的并列一致）：

- **Fixed resolution**：最简单。**BLIP-2** 为 **224 px**，早期 **LLaVA** 为 **336 px**。计算便宜，但严重限制细粒度感知。**LLaVA-1.5** 表明从 **224 px** 增至 **336 px** 即可在 **hallucination reduction** 上获得可测增益，说明部分曾归因于「噪声训练数据」的 **hallucinations** 实为 **perceptual resolution** 不足所致。
- **Dynamic tiling / AnyRes**：将输入切为多个 **crops**，每块以 **encoder native resolution** 处理，再合并特征图。**LLaVA-1.5-HD** 率先将图像分为最多六块 **224 px grid** 并拼接全局（下采样）上下文视图。**LLaVA-OneVision** 将其推广为 **Higher AnyRes**，用 **bilinear interpolation** 做 **token compression**，支持最多 **384×36 crops** 等配置，并按场景（单图、多图、视频）自适应 **token budget**。关键设计洞见是：**scaling resolution** 往往比单纯 **scaling token count** 更有效——有利于在 **pixel level** 保留 **spatial detail**，而非仅增加可能冗余的 **tokens**。
- **Dual / multi-encoder**：用不同尺度的独立 **encoder** 规避 **resolution–token** 权衡。**Mini-Gemini** 将低分辨率 ViT（336 或 672 px）与高分辨率 **ConvNeXt**（768 或 1536 px）配对，通过 **cross-attention** 从 HR 流挖掘 **spatial detail** 而不膨胀 **LLM input sequence**。**Cambrian-1** 组合最多四个 **encoder**（CLIP、SigLIP、ConvNeXt、DINOv2）于各自 **native resolution**，以发挥各自所长。
- **Stage-wise resolution increase**：**Qwen-VL**（**224→448**，**multi-task pre-training**）与 **CogVLM**（**224→490**，**pre-training** 最后 30K iterations）采用课程式策略：先学粗对齐，再细化 **spatial detail**，避免全程高分辨率训练的计算成本。

### 2.3 Vision-Language Connectors {#subsec:rep-connectors}

**Connector** 将视觉特征映射到 **LLM token space**；其设计直接决定保留与压缩 **spatial information** 的权衡，因而对 **grounding** 影响深远。

#### 2.3.1 Linear Projection and MLP {#subsubsec:rep-linear-mlp}

**LLaVA-1.5** 表明 **two-layer MLP** 是「**surprisingly powerful and data-efficient**」的 **connector**：仅用约 558K **pre-training** 样本与 665K **instruction tuning** 样本，即可与在数亿 **image-text pairs** 上训练的系统竞争。**MLP** 通过 **ViT patch** 与 **LLM token** 的一一对应维持 **spatial structure**——每个 **patch** 对应一个 **LLM input token**。这既利于 **grounding**，也意味着 **visual tokens** 随分辨率近似平方增长，在 **spatial detail** 与 **context length** 之间形成张力。

#### 2.3.2 Q-Former {#subsubsec:rep-q-former}

**BLIP-2** 引入 **Q-Former**（轻量 **transformer**，188M 参数，自 **BERT_base** 初始化），使用 32 个可学习 **query embeddings** 与冻结图像特征通过 **cross-attention** 交互，输出固定长度 **32×768**，与输入分辨率无关。这构成 **information bottleneck**：**queries** 被迫通过 **ITC / ITM / ITG** 三目标 **pre-training** 提取最与文本相关的视觉特征。优点是计算高效——仅 32 个 **tokens** 送入 **LLM**；缺点是 **spatial structure** 基本被丢弃：**queries** 全局 attend 整张特征图，难以精确定位。这也解释 **BLIP-2** 本身不支持 **bounding box prediction** 或 **grounding tasks**。

#### 2.3.3 Cross-Attention Resampler with Positional Encoding {#subsubsec:rep-cross-attn-resampler}

**Qwen-VL** 采用 **single-layer cross-attention module**，将视觉序列压缩为固定 **256 tokens**；关键是在 **cross-attention** 的 **query-key pairs** 中融入 **2D absolute positional encodings**，以缓解压缩过程中的位置信息损失。该设计直接支撑 **Qwen-VL** 的 **grounding**：模型可将 **bounding box coordinates** 输出为归一化文本串（格式 `(X_top_left, Y_top_left), (X_bottom_right, Y_bottom_right)` 归一化到 [0,1000)），**tokenize** 为普通文本，无需专用 **detection head**。

#### 2.3.4 Deep Fusion via Visual Expert {#subsubsec:rep-deep-fusion}

**CogVLM** 在 **LLM** 每一层 **transformer** 中增加可训练的 **visual expert module**：对 **image tokens** 使用独立 **QKV** 与 **FFN**，**text tokens** 仍用原始（冻结）**LLM 权重**。参数量翻倍，但 **FLOPs** 不变（图像与文本使用不同权重集）。**Deep fusion** 在 **grounding** 上达到 SOTA：**CogVLM-Grounding** 在 **RefCOCO val** 达 92.76%，甚至超过专用 **detection** 模型。**Ablation** 表明：**shallow alignment**（仅调 **adapter**）显著弱于 **deep fusion**，因为视觉特征需在多层中逐步变换以匹配各层深度的 **LLM internal representation**。

**Table. Ablation: impact of connector depth on CogVLM performance**

| Configuration | Trainable Params | NoCaps CIDEr | VQAv2 |
|----------------|------------------|--------------|-------|
| MLP Adapter only（shallow） | 140 M | 111.5 | 73.8 |
| Full LLM + Adapter | 6.9 B | 118.5 | 78.9 |
| Visual Expert every 4th layer | 1.7 B | 117.4 | 77.6 |
| Visual Expert every layer（full） | 6.6 B | 120.1 | 80.0 |

#### 2.3.5 Spatial Vision Aggregator (SVA) {#subsubsec:rep-sva}

**Cambrian-1** 提出 **Spatial Vision Aggregator（SVA）**，面向 **multi-encoder** 设置：**learnable 2D latent queries** 通过 **cross-attention** 与多路 **encoder** 特征交互，含两项关键创新：(1) **Spatial inductive bias**：每个 **query token** 显式与所有 **encoder feature maps** 上的 **spatial sub-region** 对齐，缓解 vanilla **resampler** 的 **global attention collapse**；(2) **Multi-layer aggregation**：在 **LLM** 中每隔 3 层插入 **cross-attention**，使 **LLM** 在处理更深表示时仍能反复访问未压缩的视觉特征。在受控比较中，**SVA** 在各类 **benchmark** 上均优于朴素拼接与标准 **resampler**，在 OCR 与图表等需高分辨率 **spatial understanding** 的任务上增益尤大；将 576 **tokens** 压到 36 时，**SVA** 比基于插值的方法或 **C-Abstractor** 保留更多 **spatial information**。

#### 2.3.6 Patch Info Mining {#subsubsec:rep-patch-info-mining}

**Mini-Gemini** 的 **connector** 通过 **dual-encoder streams** 之间的 **cross-attention** 运作：低分辨率视觉嵌入为 **queries**，高分辨率 **ConvNeXt feature map** 为 **keys/values**；每个 **query** 仅 attend 其在 HR 特征图中的空间对应子区域，在保留局部性的同时 enrich 每个 **token**。「挖掘」后的 **visual tokens** 与 LR 编码 **token count** 相同，即使 **effective resolution** 很高也能控制 **LLM input length**。

### 2.4 Comparative Analysis: Impact on Grounding {#subsec:rep-comparative}

**Table. Architecture comparison and grounding support**

| Model | Vision Encoder | Connector | Resolution | Supports Grounding |
|--------|----------------|-----------|------------|--------------------|
| BLIP-2 | EVA-CLIP ViT-G | Q-Former（32 queries） | Fixed 224 px | No |
| LLaVA-1.5 | CLIP ViT-L/14 | 2-layer MLP | Fixed 336 px | No（无 grounding 数据） |
| InternVL | InternViT-6B | PixelShuffle + MLP | Dynamic tile 448×N | Yes（v2.0+） |
| Qwen-VL | ViT-bigG（OpenCLIP） | Cross-attn resampler（256） | 448 px | Yes（bbox as text） |
| CogVLM | EVA2-CLIP-E | Visual Expert（deep fusion） | 490 px | Yes（SOTA on RefCOCO） |
| LLaVA-OneVision | SigLIP ViT-SO400M | 2-layer MLP | AnyRes up to 384×36 | No（无 grounding 数据） |
| Cambrian-1 | Multi（SigLIP+DINOv2+ConvNeXt+CLIP） | SVA | Multi-scale up to 1024 | Evaluated（CV-Bench） |
| Mini-Gemini | CLIP ViT-L + ConvNeXt-L | Patch info mining | LR 672 + HR 1536 | Partial |

**归纳：**

1. **Grounding 需要在 connector 中保留 spatial structure。** 强 **grounding** 模型（**Qwen-VL**、**CogVLM**、**InternVL**）均使用**保留 per-patch 空间信息**（**deep fusion**、**positional-aware resampler**）或维持高 **spatial resolution** 的 **connector**；相反，**BLIP-2** 的 **Q-Former** 将信息压缩到 32 个全局 **query**，无法支持 **grounding**。
2. **Resolution 必要但不充分。** **LLaVA-OneVision** 通过 **AnyRes** 达到极高分辨率，但未包含 **grounding-specific** 训练数据，故不执行 **grounding** 任务；**Qwen-VL** 仅在 **448 px** 结合 **positional-aware compression** 与 **multi-task pre-training** 中的显式 **grounding** 数据（**GRIT**、**RefCOCO**），即可取得有竞争力的 **grounding**。
3. **Training data 与 objectives 与架构同等重要。** **CogVLM** 的 **grounding** 不仅来自 **deep fusion**，还来自将图像与约 40M **noun-phrase-to-bounding-box** 标注配对的专用 **pre-training**。**Cambrian-1** 的高 **vision-centric** 分数既来自 **multi-encoder**，也来自约 7M 样本的 **curated instruction dataset**。
4. **Self-supervised features** 在 **spatial tasks** 上可补充 **language-supervised** 特征。**Cambrian-1** 表明在 **CLIP** 系中加入 **DINOv2** 可提升 **vision-centric benchmarks**（**spatial relationship**、**depth order**），与 **grounding** 最相关。
5. **Vision encoder scale** 的不对称仍在。尽管 **InternVL** 证明 **6B vision encoder** 同时改善 **perception** 与 **pixel-level** 任务，后续多数模型（**LLaVA-OneVision**、**Cambrian-1**、**Mini-Gemini**）仍采用 0.3–1.8B **encoder** 配 7–34B **LLM**；该不对称是否限制密集或小物体场景下的 **grounding accuracy** 仍是开放问题。

### 2.5 Summary {#subsec:rep-summary}

MLLM 从 **encoder** 到 **resolution strategy** 再到 **connector** 的 **visual representation pipeline** 如同 **information funnel**，决定其 **grounding capability** 的上界。趋势包括：(a) 通过 **dynamic tiling** 或 **dual-encoder** 提高输入分辨率；(b) **connector** 显式保留 **spatial structure**，而非压缩为固定长度的全局表示；(c) 组合多种 **encoder** 范式（**language-supervised + self-supervised + ConvNet**）以捕获互补视觉属性。但**仅凭表征质量**并不能自动产生 **grounded behavior**——它只决定何种 **spatial structure** 仍可供模型使用。下一节（第 3 节）讨论 MLLM 如何将保留的结构转化为可用的 **grounding outputs**（**coordinates**、**regions**、**masks**）。

---

## 3. Grounding Methods: From Coordinates to Regions {#sec:grounding-methods}

若第 2 节问的是 MLLM 能保留多少 **spatial detail**，第 3 节则问这些细节如何被**操作化**为可用的 **grounding behavior**。近期 MLLM 文献中，**grounding methods** 沿三种表达力递增的 **output paradigms** 演进：**(i)** 作为文本生成的 **coordinates**；**(ii)** 将用户指定区域视为对话一等公民的 **region-aware interaction**；**(iii)** 将语言链接到 **pixel masks** 而非框的 **segmentation-level grounding**。贯穿这些范式的核心设计问题不仅是「如何预测位置」，而是**如何表示位置**，使其仍兼容 **next-token generation**、**instruction following** 与 **multi-task training**。参照近期 **visual grounding** 综述（Xiao et al.）的 **taxonomy**，本节聚焦从经典单框 **grounding** 向对话式、**open-vocabulary**、日益 **dense** 的 **grounding systems** 的 MLLM 时代转变。

### 3.1 Coordinate Prediction as Language Generation {#subsec:grounding-coordinates}

最早一批面向 **grounding** 的 MLLM 将定位视为 **language modeling** 的特例：若 **LLM** 能自回归生成词，或许也能自回归生成 **coordinates**。该表述的吸引力在于：无需单独 **detector head**，保留 **instruction-tuned MLLM** 统一的 text-in/text-out 接口，并可用与普通对话相同的 **next-token objective** 训练 **grounding**。

**Kosmos-2** 将 **bounding box** 每个角点离散到 **`32×32` grid** 上的 **location token**，并以类超链接格式接在对应 **text span** 之后，使 **grounding** 成为同时包含词与 **spatial tokens** 的序列预测。输入输出对称：模型既可接收框做 **referring**，也可输出框做 **grounding**；架构不变，**grounding** 完全由数据与 **tokenization** 注入。配合 **GrIT**（约 **91M images**、**115M text spans**、**137M boxes**），生成模型零样本迁移表现突出：例如 Flickr30k Entities test 上 **78.7** **R@1**、RefCOCOg test 上 **61.65** accuracy。局限在于输出绑定离散 **bins** 与 **`224×224` resolution**，继承 **quantization error**，细粒度或小物体 **grounding** 困难。

**Shikra** 保持自回归哲学，但取消专用 **coordinate vocabulary**，直接将框写为归一化自然语言数字 `[x_min, y_min, x_max, y_max]`。位置成为句中普通短语，无需额外 **tokenizer** 或 **position encoders**；对 **referential dialogue** 极灵活。**Ablation** 表明该数值表示在 **REC benchmarks** 上稳定优于「扩展词表」方案——将 **grounding** 压入 **LLM** 原生文本空间不仅更简单，往往更有效。代价是 **token efficiency**：单框展开为长数字串，**dense grounding** 或多物体输出笨重。

**NExT-Chat** 揭示 **text-as-coordinate** 范式瓶颈：**coordinates** 并非真正的 **language**，纯 **token classification** 难以支持 **masks** 等更丰富格式。其答案是 **pix2emb**：引入 **`<trigger>` token**，由其 **hidden state** 经轻量 **heads** 解码为 **bounding box** 或 **segmentation mask**；配对的 **location encoder** 将给定框映射回单一嵌入以作区域输入，**cycle loss** 保持编解码对齐。位置仍嵌入自回归对话循环，但不再仅是字面文本；可用 **L1**、**GIoU** 等标准回归损失，同时保留统一对话接口。权衡是优化更微妙：平衡 **language loss** 与 **localization loss** 难于纯 **pix2seq** 表述，**REC** 在标准 **RefCOCO** 划分上略低于 **Shikra**。

三者揭示 **coordinate modeling** 的演进：从 **discrete location tokens**（Kosmos-2）到 **plain-text numbers**（Shikra）再到 **hidden-state-triggered regression**（NExT-Chat）。**grounding** 只有部分是「语言」的：任务越像结构化 **spatial prediction** 而非普通续写，越需要将部分负担移出纯 **token generation**。

**Table. Coordinate-centric grounding paradigms in representative MLLMs**

| Model | Spatial output | Input region | Supervision | Strength | Limitation |
|--------|----------------|--------------|-------------|----------|------------|
| Kosmos-2 | Discrete location tokens on `32×32` | Box | Next-token on text + location tokens | 统一 text-box 接口，强零样本 | 量化与低分辨率瓶颈 |
| Shikra | Natural-language numbers | Point/box | Next-token on ordinary text | 架构改动极小，自然 **referential dialogue** | 坐标串冗长 |
| NExT-Chat | **`<trigger>`** hidden-state 解码 | Box encoder 的区域嵌入 | Text + box 回归 + cycle | 同框架支持 box 与 mask | 优化更难，REC 偏弱 |

### 3.2 Region-Level Understanding and Grounded Conversation {#subsec:grounding-regions}

预测 **bounding box** 只是 **grounded interaction** 的第一步；许多任务要求模型不仅输出 **coordinates**，还要**对用户指定区域推理**、比较多区域、描述歧义部分，或在对话中混用自由文本与局部指代。由此出现第二种范式转变：从「**grounding 即坐标生成**」到「**grounding 即 region-level dialogue**」。

**Shikra** 的 **Referential Dialogue** 已指向该方向：**coordinates** 可出现在文本流任意位置，模型可回答「该区域是什么」「两区域差异」等，无需单独 **region feature extractor**——框作为嵌入在语言中的符号指针。证明 **region-conditioned dialogue** 可由足够多样的 **instruction tuning** 涌现；但纯符号区域输入也有极限：稀疏框能指示 **where**，却未必携带足够视觉证据以区分占据近似外包矩形的相似形状。

**Ferret** 针对该 **failure mode**：提出 **hybrid region representation**，结合离散坐标与 **spatial-aware visual sampler** 提取的连续 **region feature**；特征来自目标区域二值 **mask**，可处理框、点、涂鸦、多边形及任意自由形状区域。洞见是：**coordinates alone** 过粗，难以刻画不规则或重叠区域的语义。辅以 **GRIT**（约 **1.1M** 样本，覆盖 region-in/text-out、text-in/region-out 与混合交互，及 GPT 辅助对话与 **negative samples**），**Ferret** 超越纯 **grounding model**，成为支持 **grounded captioning**、**region description** 与对话级 **grounding** 的区域感知助手。

**Ferret-v2** 强调 **region understanding** 根本上是 **resolution-sensitive**：**AnyRes** 缩放一致优于直接上采样，在细粒度识别、OCR、**REC**、**Ferret-Bench** 上均如此。架构上用 CLIP 全局视图 + DINOv2 局部高分辨率块并融合；并引入 **three-stage coarse-to-fine curriculum**（含 LVIS 式物体数据的中间 **dense alignment**）。将 **region grounding** 重构为 **dense local alignment** 问题，而非仅 **instruction following**；小物体 **referring/grounding** 的实证增益印证更好区域表征与更好训练课程可相互强化。

**Osprey** 进一步认为框作为区域输入常过粗：框必然包含背景杂波，削弱训练与推理中区域与文本的对齐。故以 **mask-level referring** 替代框级输入，用 **mask-aware visual extractor** 在多级特征上从精确 **mask** 池化特征；训练数据 **Osprey-724K** 含物体级描述、对话、部件属性、平衡正/负鲁棒样本与短答指令。输入粒度改变带来部件级分类、细区域描述与 **region captioning** 的显著提升：例如 RefCOCOg **region captioning** 上 **108.3** **CIDEr**，在 Ferret-Bench **referring description** 与 **reasoning** 上亦优于所对比的 MLLM。局限是依赖可用 **mask**（标注或上游 **SAM** 等）。

共同模式：**region-level grounding** 随区域不仅表示「在哪」，还表示「含何视觉内容」而改善。纯坐标对粗 **REC** 尚可，但对 **region captioning**、区域比较、部件推理与 **grounded conversation** 越来越脆。**Ferret** 与 **Osprey** 在不放弃 MLLM **instruction-following** 优势的前提下，将局部视觉特征重新引入交互循环。

### 3.3 Segmentation-Level Grounding {#subsec:grounding-segmentation}

**Bounding boxes** 仍是有损接口：近似物体范围，难以描述非矩形部件，也不便用于提及多属性、**stuff regions** 或物体部件的对话输出。第三类方法将 **grounding** 从区域级框对齐升级为 **pixel-level grounding**，输出与语言绑定的 **segmentation mask**。

**LISA** 给出简洁表述：词表增加 **`<SEG>` token**，将其最后一层 **hidden state** 解释为 **SAM-style mask decoder** 的 **prompt embedding**（**embedding-as-mask**）。**Segmentation** 可端到端纳入标准多模态 **LLM**，无需外部流水线；也避免将 **mask** 序列化为长多边形串。**Reasoning segmentation** 同时需要语义推理与 **mask** 输出；训练以语义分割、**referring segmentation**、**VQA** 为主，已展现强零样本 **reasoning segmentation**；仅在 **239 ReasonSeg samples** 上微调亦有大幅提升——说明一旦能将语言 **hidden state** 映射为 **mask prompts**，剩余缺口常在高层推理而非低层 **mask generation**。

**GLaMM** 将单物体分割推广为 **Grounded Conversation Generation（GCG）**：回复可交错普通文本与多短语链接的 **segmentation masks**。输出格式 **`<p> phrase </p><SEG>`** 将短语边界与 **mask** 直接绑定，支持 **grounded dense captions** 与 **grounded multi-turn**。**GranD**（**11M images**、**810M regions**、**7.5M unique concepts**）及 **GranD_f** 构成大规模数据引擎，使 **segmentation grounding** 成为 **dense multimodal pre-training** 问题而非狭窄 **referring segmentation**。

**NExT-Chat** 介于框级与 **mask** 级：**`<trigger>`** 嵌入可送 **box decoder** 或 **SAM-based mask decoder**，同一对话骨干支持两类输出；三阶段训练中第三阶段冻结大部分 **LMM** 仅训 **SAM** 侧投影与解码。与 **LISA/GLaMM** 相比路径更模块化，但共同点一致：一旦将位置视为 **embedding** 而非字面 **token string**，**mask prediction** 成为自然延伸。

**Pixel-level grounding** 改变输出的**语义**：框只说物体大致在哪；**mask** 可在更接近自然语言的粒度上 **ground** 属性、**stuff**、部件与关系短语——对 **embodied systems** 与视觉助手许多指令本质上是 **mask-like**（如「人行道旁的草」「红屋顶」「可按压的部件」），未必能归为单一干净矩形。

### 3.4 Training Strategies: Data Construction, Curriculum, and Multi-Task Transfer {#subsec:grounding-training}

代表性模型间的性能差异同样来自 **data design** 与 **training curriculum**。**grounding** 难以仅从通用 **image-caption alignment** 可靠涌现；必须通过显式将语言与 **spatial supervision** 耦合的数据来教授。

**模式一：自动大规模 grounding 数据构建。** Kosmos-2 的 **GrIT**、GLaMM 的 **GranD** 将网络 **image-text** 与自动标注结合，噪声相对 **RefCOCO** 类人工语料更大，但以覆盖与多样性补偿，利于学习开放词表下 **text spans** 与视觉区域的广泛关联。

**模式二：既有区域数据集的 instruction 重格式化。** Shikra、Ferret、NExT-Chat、Osprey 等将 **RefCOCO**、**Visual Genome**、**PointQA**、**Visual-7W**、**PACO-LVIS**、**VCR** 等改写为 **instruction-following** 对话，使 **grounding** 嵌入通用对话、**captioning**、推理与 **QA**，而非窄 **REC** 模板。Ferret/Osprey 还显式用 GPT 生成对话与提示多样化。

**模式三：coarse-to-fine curriculum。** Ferret-v2：图像-标题对齐学全局语义 → LVIS 式 **dense alignment** 学局部物体精度 → 最终 **instruction tuning** 学用户意图。NExT-Chat 将 **segmentation** 隔离在轻量末阶段。Osprey 分 **image-text alignment**、**mask-text alignment** 与端到端 **instruction tuning**。

**模式四：面向鲁棒性的 negative mining。** Ferret 加入空间与语义上的 **hard negatives**；Osprey 挖掘 **spatial-aware** 与 **class-aware negatives**；若干模型还加入短答指令以降低冗长与 **hallucination**。这并非次要细节：**grounding** 错误常为**对比性**错误（男人与女人、黄与蓝、邻近物体彼此混淆），**hard negatives** 直接塑造 **grounded model** 能否可靠拒绝错误定位。

**模式五：多任务迁移是双向的。** **grounding** 使下游对话更精确；通用 **vision-language** 训练也稳定 **grounding**。LISA 需 **VQA** 数据以保持对话能力；Ferret-v2 加入 OCR/VQA 式数据以在通用 MLLM **benchmarks** 上保持竞争力。

### 3.5 Comparative Analysis {#subsec:grounding-comparative}

可沿 **representation of location** 与 **granularity of output** 两轴理解前述方法；下表汇总主要权衡（对应 `grounding_review_body.tex` 中 **Table: Representative grounding models and their design trade-offs**）。

**Table. Representative grounding models and their design trade-offs**

| Model | Input representation | Output representation | Finest output granularity | Key training signal | Core advantage | Main weakness |
|--------|----------------------|------------------------|---------------------------|---------------------|----------------|---------------|
| Kosmos-2 | Text spans + discrete location tokens | Discrete location tokens | Box | Web-scale GrIT | Strong zero-shot grounding in a unified LM interface | Coarse bins and limited resolution |
| Shikra | Plain-text numbers for point/box | Plain-text numbers | Box | Reorganized public tasks + Shikra-RD | Extremely simple unified referential dialogue | Coordinate strings are verbose and box-only |
| Ferret | Hybrid coordinates + sampled region feature | Text with grounded boxes | Free-form referred region, box output | GRIT 1.1M + GPT dialogues + negatives | Supports point/box/free-form region input and strong grounded conversation | Still box-based on output side |
| Ferret-v2 | AnyRes hybrid region with CLIP + DINOv2 | Text with grounded boxes | Free-form referred region, box output | Three-stage coarse-to-fine training | Stronger small-object and high-resolution grounding | Added architectural and training complexity |
| LISA | Image + text query | `<SEG>` token decoded to mask | Mask | Segmentation + RES + VQA, then optional ReasonSeg FT | Elegant end-to-end mask output with minimal interface change | Mostly oriented to single-target mask generation |
| GLaMM | Image, optional region, text prompt | Interleaved phrase-mask output | Mask + grounded dense caption | GranD + GranD_f | Multi-phrase grounded conversation at pixel level | Heavier architecture and data pipeline |
| NExT-Chat | Image + box embedding via location encoder | `<trigger>` decoded to box or mask | Box and mask | Three-stage training with regression and cycle loss | One backbone for dialogue, detection, and segmentation | Balancing LM and localization objectives is difficult |
| Osprey | Mask-aware region tokens | Region description / reasoning text | Mask-level input, text output | Osprey-724K + multi-stage tuning | Precise mask-conditioned semantic understanding | Requires a usable upstream mask proposal |
| Grounding DINO | Image-text fusion in detector pipeline | Detector boxes + phrases | Box | Grounded pre-training + optional RefCOCO fine-tuning | Highest localization accuracy and strong open-set transfer | Not a native conversational MLLM |

**结论要点：** (1) **grounding methods** 离纯 **token generation** 越远，表达力通常越强——更丰富区域交互与 **mask** 输出往往需 **hidden-state decoding**、混合区域特征或显式 **decoder**。(2) **Region input** 与 **region output** 同等重要：输出框有用；**Ferret/Osprey** 表明更难的是**精确理解**所指区域，**mask-aware** 或混合区域表征持续改善 **region captioning** 与 **grounded reasoning**。(3) **Segmentation-level grounding** 不仅是更密的 **REC**——**LISA/GLaMM** 表明 **mask** 进入输出空间后，**grounding** 从物体定位扩展到短语级视觉解释。(4) **Accuracy** 与对话灵活性仍有权衡：**Grounding DINO** 在 **REC** 类 **benchmark** 微调后仍常强于多数 MLLM 式方法，因 **detector head** 对精确定位仍是更好工具；MLLM 以 **referential dialogue**、**grounded captioning** 等弥补部分差距，但权衡未消失。(5) **Data engineering** 决定性：**GrIT**、**GRIT**、**GranD**、**Osprey-724K**、**Shikra-RD** 等是实现 **instruction-following**、**open-vocabulary** 与鲁棒 **grounding** 的机制，方法论分歧不仅在架构，也在**可规模化合成的结构化 spatial supervision** 有多少。

### 3.6 Summary {#subsec:grounding-summary}

MLLM **grounding methods** 可读作 **spatial output vocabulary** 的稳步扩张：从 **tokenized coordinates** → **content-aware regions** → **pixel-aligned masks**。Kosmos-2 与 Shikra 确立 **grounding** 可表述为 **language generation**；Ferret/Ferret-v2 表明区域特征与分辨率缩放对 **grounded interaction** 必不可少；LISA、GLaMM、NExT-Chat 表明 **hidden-state-triggered mask decoding** 使与 **segmentation** 兼容的 **grounding** 可行；Osprey 强调 **mask-level** 区域输入对细粒度语义理解的重要性。更好 **grounding** 来自表征、输出格式、数据构建与训练课程的**联合**改进。同时也划清 **grounding** 边界：定位区域尚不等于理解区域在空间中的关系，或在长文本 **generation** 中保持视觉忠实——这两方面驱动第 4、5 节。

---

## 4. Spatial Relation Reasoning {#sec:spatial-reasoning}

第 3 节处理「物体在哪」；本节问更难的问题：「物体间 **spatial relationship** 是什么？」**Spatial reasoning**（理解杯在桌上、人在车左、一栋楼比另一栋更近等）是 **embodied** 任务中 **grounded interaction** 的前提，却仍是当前 MLLM 最弱能力之一。本节综述暴露这些失败的诊断 **benchmarks** 与旨在改进的近期方法，按四类关系组织：**topological**、**directional**、**distance/depth**、**occlusion**。

### 4.1 The State of Spatial Reasoning: Systematic Failures {#subsec:spatial-failures}

在讨论方法之前，有必要先确立问题严重程度：两个早期 **benchmark** 表明，**spatial reasoning** 对多模态模型不仅「难」，而且在统计意义上**极不可靠**。

**Visual Spatial Reasoning（VSR）** 构建超过 **10,000** 自然 **image–statement pairs**，涵盖从语言学文献归纳的 **66** 类 **spatial relations**。每例为真/假判断，例如「the dog is behind the woman」。两项设计使其具有诊断性：(1) 使用 **COCO** 真实照片，而非合成布局；(2) 区分 **intrinsic reference frames**（由参照物**本征朝向**定义）与 **relative reference frames**（由**观者视角**定义）。2023 年，表现最好的模型准确率仍低于 **70%**，远低于人类约 **95.4%** 的天花板。更令人担忧的是，需要 **perspective-taking** 的空间介词（如 *in front of*、*behind*）显著难于基于拓扑的关系（如 *on*、*inside*），说明失败不仅是 **object detection**，而是 **spatial representation** 本身（Liu et al., VSR）。

**What'sUp** 将问题压到最简：给定两物体，判断谁 **above** 或 **below** 另一物体。研究评估 18 个 **vision-language models**（含 **BLIP-2**、**LLaVA**、**InstructBLIP**、**GPT-4V** 等），在难度递增的三类 **benchmark** 上测试：

- **What'sUp-A**：受控合成图像，白底上的简单几何形状或物体。
- **COCO-Spatial**：**spatially unambiguous** 物体对的自然 **COCO** 图像。
- **GQA-Spatial**：来自 **GQA** 的真实场景图，问题由 **scene graphs** 导出。

**结果普遍很差：没有受测模型在所有三个 benchmark 上稳定超过 chance；** 在 **spatial data** 上微调也仅带来有限且不一致的改进。**LAION-400M** 大规模语料统计显示：**spatial prepositions** 在 **image-text pairs** 中出现比例不足 0.2%——模型几乎在「空间贫乏」的数据上训练。该 **data scarcity** 发现与第 2 节所述架构瓶颈**互补地**解释 **spatial reasoning** 失败（Kamath et al., What'sUp）。

#### Encoder-Level Explanations {#subsubsec:spatial-encoder-explanations}

**Eyes Wide Shut** 将失败上溯至 **vision encoder**：**CLIP-blind pairs**（人眼可辨而 **CLIP embedding** 几乎相同）识别出 **CLIP** 系统性编码不足的九类视觉模式：**orientation**、**direction**、**counting**、**color**、**appearance**、**state**、**text**、**shape**、**spatial relations**。**MMVP** 上即使 **GPT-4V** 仅约 38.7%；放大 **CLIP** 变体仍无法解决其中 7 类缺陷。**Mixture-of-Features（MoF）**（CLIP + **DINOv2** 融合或交错）将 **MMVP** 从 24.7% 提升至 36.7%，与 **Cambrian-1** 在 **vision-centric spatial benchmarks** 上 **DINOv2** 优势的结论一致：**language-supervised encoders alone** 不足以支撑 **spatial understanding**。

### 4.2 Taxonomy of Spatial Relations {#subsec:spatial-taxonomy}

九篇文献 collectively 覆盖四类关系，下表为各工作与关系类型及类型的对应（✓ 表示覆盖；**Grounding Link** 列表示与 **grounding** 的显式联系）。

**Table. Spatial relation coverage across Section 4 papers**

| Paper | Topological | Directional | Distance / Depth | Occlusion | Grounding Link | Type |
|--------|-------------|-------------|------------------|-----------|----------------|------|
| VSR | ✓ | ✓ | | | | Benchmark |
| What'sUp | | ✓ | | | | Benchmark |
| SpatialVLM | | | ✓ | | ✓ | Method |
| SpatialRGPT | ✓ | ✓ | ✓ | | ✓ | Method + Bench |
| CV-Bench | ✓ | | ✓ | | ✓ | Benchmark |
| Eyes Wide Shut | ✓ | ✓ | | | | Analysis |
| SpatialBench | ✓ | ✓ | ✓ | ✓ | | Benchmark |
| Spatial-MM | ✓ | ✓ | | | ✓ | Benchmark |
| MM-Spatial | | | ✓ | ✓ | ✓ | Method + Bench |

**Topological relations**（on, in, against, attached to, near）描述物体如何连接或包含，为最常见测试类别。**Directional relations**（左/右、上/下、前/后）看似简单，What'sUp 表明连 **above/below** 也不可靠；**reference frame problem** 与 **Spatial-MM** 的人 vs 相机视角分析均显示视角依赖关系更难。**Distance and depth relations**（更近/更远、度量距离估计）需从单目图像理解 **3D structure**。**Occlusion**（部分遮挡、完全遮挡、重叠）研究最少，**SpatialBench** 与 **MM-Spatial** 涉及；需 **3D scene understanding** 而非表面模式匹配。

### 4.3 Benchmarks and Evaluation {#subsec:spatial-benchmarks}

标准 **VQA** 不足以测 **spatial understanding**。**SpatialBench** 等采用**分层认知**（5 个层次）；评估从纯 **qualitative relations** 走向需估计 **depth/distance** 的 **quantitative spatial reasoning**；**Spatial-MM**、**MM-Spatial** 等通过 **language shortcuts** 过滤，减少「无需真视觉」即可答对的情况。

**Table. Comparison of spatial reasoning benchmarks**

| Benchmark | Source | Scale | Relation types | Answer format | Ground truth | Key design feature |
|-----------|--------|-------|----------------|---------------|--------------|---------------------|
| VSR | COCO photos | 10,119 pairs | 66 spatial relations | True/False | Human annotation | Intrinsic vs relative frame distinction |
| What'sUp | Synthetic + COCO + GQA | 3 sub-benchmarks | Above/below | MCQ | Controlled layout | Difficulty ladder; corpus frequency analysis |
| CV-Bench | COCO + Omni3D | 2,638 examples | 2D spatial, count, depth, distance | MCQ | 3D annotations | Converted from classic CV tasks to VQA format |
| SpatialBench | 117 real-world videos | 3,193 QA pairs | 5 cognitive levels | MCQ | LiDAR ground truth | Hierarchical cognition framework |
| Spatial-MM | Synthetic + COCO | 2,310 questions | Topological, directional | MCQ + open-ended | Scene graphs + human | Human vs camera perspective split |
| SpatialRGPT-Bench | Indoor/outdoor scenes | 1,406 QA pairs | Topological, directional, distance | Qualitative + quantitative | Depth maps + 3D estimation | Region-level spatial questions |

空间 **benchmark** 的激增反映学界已认识到：标准 **VQA** **evaluation** 不足以检验 **spatial understanding**。上表对比本节涉及的主要 **benchmark** 家族。有三类设计转向尤其重要。第一，领域正从**单一二元判断**走向**分层评估**：**SpatialBench** 将 **spatial cognition** 显式组织为五个层次，并显示随任务变得更 **compositional**，性能急剧下降。第二，评估从纯 **qualitative relations**（如 **above/below**）走向 **quantitative spatial reasoning**——模型须估计 **depth** 或 **distance**，而非仅分类介词（SpatialVLM；SpatialRGPT）。第三，较新 **benchmark** 越来越多地试图控制 **language shortcuts**，过滤掉无需真实视觉即可答对的样本（**Spatial-MM**、**MM-Spatial**）。综合而言，**spatial reasoning** 已不能再被窄化为某一类 **VQA subtask**；它必须同时作为**感知性、几何性与组合性**能力来测试。

### 4.4 Methods: Endowing MLLMs with Spatial Reasoning {#subsec:spatial-methods}

面对上述失败证据，自然的问题是：**spatial reasoning** 能否被教会？**SpatialVLM**、**SpatialRGPT**、**MM-Spatial** 三条路线策略不同，但共享一点洞见：**spatial understanding** 必须超越 **2D image–text pairs**。

#### SpatialVLM（数据驱动）{#subsubsec:spatial-spatialvlm}

**SpatialVLM** 直接回应 What'sUp 所揭示的 **data scarcity**：若 **spatial prepositions** 在爬取的 **captions** 中稀少，**spatial training data** 应**合成**而非仅靠采集。论文构建自动化流水线：

1. **Open-vocabulary object detection**：识别并标注图像中的物体。
2. **Metric depth estimation**（现成单目深度模型）：将 **2D scene** 提升为近似 **3D**。
3. **Semantic segmentation**：细化物体边界。
4. **Spatial VQA generation**：由 **LLM** 在重建的 **3D layout** 条件下，生成关于物体间 **spatial relations** 的问答对。

在互联网规模上运行该流水线，得到约 **10 million images** 与 **2 billion spatial QA pairs**——比此前任何数据集的 **spatial** 训练数据多**数量级**。经该数据微调的 **multimodal model** 同时获得 **qualitative spatial reasoning**（相对位置判断）与 **quantitative spatial reasoning**（度量距离估计）。关键的是，论文展示 **chain-of-thought reasoning** 可涌现：当问「椅子是否近到让人能坐下？」时，模型先估计距离，再与功能标准比较。该能力在机器人应用中得到展示：微调后的模型可作为 **robot planning** 的 **spatial reward annotator**（Chen et al., SpatialVLM）。

**局限**：依赖单目 **depth estimation**，对 **outdoor** 场景与远距离物体引入系统误差；合成 **spatial data** 主要覆盖距离与相对位置，**topological** 与 **occlusion** 关系未覆盖。

#### SpatialRGPT（区域感知 3D 推理）{#subsubsec:spatial-spatialrgpt}

**SpatialRGPT** 同时弥补第 3 节 **coordinate-based grounding** 与 **SpatialVLM** 的缺口：如何对**任意用户指定区域之间**推理 **spatial relations**，**而非**仅对检测到的物体中心。关键洞见：当 **grounded** 在 **region-level representations** 而非图像级或点级特征时，**spatial reasoning** 会显著更精确。

方法含三部分：

1. **3D Scene Graph Construction**：从单张 **2D image**，结合 **open-vocabulary detection**、**metric depth estimation** 与 **SAM segmentation**，重建 **3D scene**；每个物体表示为带位置、范围与深度的 **3D bounding volume**。
2. **Depth Plugin Module**：不修改 **vision encoder**，而引入轻量 **depth adapter**，将**度量深度**作为 **auxiliary input** 注入 **MLLM**，在避免重训骨干的同时提供 **CLIP-based encoders** 所缺的 **3D awareness**。
3. **Open Spatial Dataset（OSD）**：合成训练语料，含 **8.7 million** **spatial relation concepts**、覆盖 **5 million** **object regions**，关系类型含 **topological**（in, on, against）、**directional**（left, right, above, below）与 **metric distance**。

**SpatialRGPT** 在 **region-level spatial reasoning** 上显著优于开源 **MLLMs** 与 **GPT-4V**。在 **SpatialRGPT-Bench** 上，**qualitative spatial questions** 达 **81.0%**（**GPT-4V** 为 **56.3%**），相对最佳基线的**绝对度量距离误差**降低逾 **70%**。这表明：通过共享 **3D representation** 将 **grounding（区域识别）** 与 **spatial reasoning（区域间关系估计）** **连接**，比将二者视为独立能力更有效（Cheng et al., SpatialRGPT）。

#### MM-Spatial（多视角 3D）{#subsubsec:spatial-mmspatial}

**MM-Spatial** 进一步利用 **multi-view geometry**，而非仅单目深度。借助 **Cubify Anything**（从随意拍摄的多视角图像重建 **textured 3D meshes**），从约 **220,000 video frames** 得到几何准确的 **3D scenes**，并生成大规模 **CA-VQA**（约 **10M spatial QA pairs**）。

两项技术创新：

1. **Multi-view + metric depth inputs**：模型同时接收 **RGB** 与来自 **multi-view stereo** 的 **metric depth maps**，比单一单目深度估计提供更可靠的 **3D geometry**。
2. **CoT depth estimation**：训练模型执行 **chain-of-thought depth reasoning**——先估计被查询物体的深度，再回答空间问题。该显式推理步骤使 **spatial inference** 可解释，且深度估计精度**出人意料地**接近专用单目深度模型。

**MM-Spatial-3B** 在 **CV-Bench** 与 **SpatialRGPT-Bench** 上均达 SOTA，尽管 **LLM backbone** 仅约 **3B** 参数，说明高质量 **3D-grounded** 训练数据可补偿较小模型规模。另引入 **tool-use paradigm**：推理时若缺深度图，可调用外部单目深度估计器，将 **depth estimation** 视为可调用的 **tool** 而非必须内化的能力（Daxberger et al., MM-Spatial）。

### 4.5 The Grounding–Spatial Reasoning Interface {#subsec:spatial-interface}

本综述的一个核心问题是：**spatial reasoning** 应被视为 **grounding** 的延伸，还是独立能力？证据给出清晰但**有条件**的答案。

**Grounding 是 spatial reasoning 的必要条件。** **SpatialRGPT** 等区域感知方法表明：当模型显式锚定到相关物体或区域时，**spatial QA** 更可靠。**Spatial-MM** 得到类似结论：**bounding boxes** 与 **scene-graph** 式结构有帮助，因为许多错误发生在「正式推理」之前——在识别**哪些实体应进入比较**的阶段就已出错。

**Grounding 不是 spatial reasoning 的充分条件。** **CV-Bench**、**SpatialVLM**、**MM-Spatial** 均表明：仅靠准确的 **2D localization** 无法解决 **depth**、**distance** 或 **occlusion**；一旦任务需要度量或 **3D** 判断，模型需要的不仅是 **region alignment**，而是**几何结构**。

最有生产力的解释是：**grounding** 与 **spatial reasoning** 构成**依赖链**而非单一合并技能。**Grounding** 提供相关实体与区域；**spatial reasoning** 在其上进行关系与几何推断。这也澄清了向下一节的过渡：即使模型能定位区域并回答部分空间问题，在 **open-ended generation** 中仍可能失去 **visual anchoring**，产生流利但**弱支持**的主张。

### 4.6 Summary {#subsec:spatial-summary}

**Spatial relation reasoning** 仍是当前 MLLM 的关键短板；失败可追溯至 **data scarcity**、**encoder** 局限与缺少显式几何结构。下表（对应 TeX **Table: Summary of spatial reasoning challenges and solutions**）归纳主要挑战与对策。**总体趋势**：**spatial reasoning** 正从 **2D pattern matching** 走向显式 **3D scene understanding**，从图像级判断走向 **region-grounded compositional inference**。最成功的路径（尤其 **SpatialRGPT** 与 **MM-Spatial**）**不取代 grounding** 而**建立在其上**。同时，更强的 **spatial reasoning** 并不保证可信 **generation**：模型仍可能偏离图像、过度依赖先验，或以高置信度陈述无视觉支持的关系——这正是第 5 节 **hallucination**、**miscalibration** 与不可靠多模态输出的衔接点。

**Table. Summary of spatial reasoning challenges and solutions**

| Challenge | Evidence | Proposed solution | Limitation |
|-----------|----------|-------------------|------------|
| Data scarcity | < 0.2% of LAION captions contain spatial prepositions (What'sUp) | Synthetic data pipelines (SpatialVLM: 2B QA pairs; OSD: 8.7M concepts) | Synthetic data may not capture real-world spatial complexity |
| CLIP spatial blindness | 9 visual patterns systematically absent from CLIP (Eyes Wide Shut) | MoF (CLIP + DINOv2); multi-encoder (Cambrian-1) | DINOv2 fusion helps but does not fully resolve all patterns |
| No 3D awareness | Monocular 2D features lack depth information | Depth plugin (SpatialRGPT); multi-view 3D (MM-Spatial); CoT depth | Monocular depth is noisy; multi-view requires additional input |
| Flat evaluation | VQA benchmarks miss spatial nuance | Hierarchical benchmarks (SpatialBench 5 levels); quantitative splits; bias filtering | Benchmarks still largely static; dynamic/interactive spatial reasoning untested |
| Grounding disconnect | Models answer spatial questions without localizing objects | Region-aware MLLMs (SpatialRGPT); bbox/scene-graph augmentation (Spatial-MM) | Requires reliable upstream region proposals |

---

## 5. Failure Modes and Grounding Hallucination {#sec:failure-modes}

第 3、4 节表明 MLLM 已能 increasingly **localize regions**，并在若干设定下 **reason about spatial relations**。第 5 节追问：当 **grounding** 弱、不稳定或在 **generation** 中被**覆盖**时会发生什么？近期 **hallucination** 研究明确：**问题不限于**明显编造的物体。模型可能从 **parametric memory** 而非图像作答、误读视觉模式、在弱证据下过度肯定，或在保持流利语言的同时偏离图像所能支持的内容。换言之，**hallucination** 往往被理解为 **grounding** 的 **failure regime**，而非与 **grounding** 无关的孤立现象（Li et al., POPE; Ding et al., Hallu-PI; Zhou et al., LURE; Guan et al., HallusionBench）。

文献已从简单 **object-existence probing** 快速扩展：**perturbation stress tests**、**language hallucination** 与 **visual illusion** 的诊断分离、**LRV-Instruction** 式数据驱动的鲁棒 **instruction tuning**、**OPERA** / **VCD** 等 **decoding-time** 干预、**RLHF-V** 的细粒度人类修正、**Woodpecker** 式外部验证流水线，以及 **ViGoR** 的 **reward-based** **visual grounding** 改进。综合这些研究，**grounding failure** 宜沿四个相互关联的问题组织：**何种环节失败**、**如何检测**、**为何在生成中传播**、**哪一层干预最有效**。

### 5.1 A Grounding-Centered Taxonomy of Failure {#subsec:failure-taxonomy}

综合第 5 节所涉论文，宜将 **hallucination** 视为在不同感知与 **generation** 阶段出现的 **grounding failures** 家族，而非单一错误类型。

**1. Unsupported object claims（不支持的物体断言）。** 即 **POPE** 研究的典型 **object hallucination**：模型断言图像中**不存在**的物体。用 **grounding** 语言说，即语言被绑定到**不存在的 referent**。**LRV-Instruction** 表明：当 **training data** 以**正样本指令**为主时，当前 MLLM 特别容易陷入此类失败——模型被鼓励像「被查询实体总存在」那样作答。

**2. Misgrounded attributes and relations（错置的属性与关系）。** 模型可能找对物体，却在颜色、计数、位置、动作或关系上出错。**Hallu-PI** 显式将 **hallucination** 扩展到 **perturbation** 下的属性与关系错误。**LRV-Instruction** 也表明：**hallucination** 不仅是「不存在的物体」；操纵**已存在物体**的属性或高层知识，有时比简单拒答**更难**。

**3. Prior-dominated answers（先验主导的回答）。** **HallusionBench** 区分 **visual illusion** 与 **language hallucination**：后者指模型从**参数记忆**或**语言先验**而非实际图像作答；在编辑图像或**知识密集型**问题上尤其明显——模型重复「通常成立」之事，而非「视觉上成立」之事。从 **grounding** 视角，模型不仅是「看错」，而是**不再把图像当作决定性证据**。

**4. Visually induced misinterpretation（视觉诱导的误读）。** **HallusionBench** 的第二类 **visual illusion** 指相反失败：模型**确实尝试**使用图像，却从中提取错误信息。对 **grounding** 综述而言这很关键：**并非所有 hallucination 都来自语言先验**；部分源于弱感知判别、差的几何阅读，或无法正确解析编辑图、图表式输入或强错觉刺激。

**5. Robustness under degraded evidence（退化证据下的鲁棒性失败）。** **Hallu-PI** 表明：在裁剪、拼接、模糊或**误导性 prompt** 下，**hallucination** 率上升。未必是全新错误类型，但揭示**条件性**：即便在干净数据上看似 **grounded**，一旦 **visual evidence** 变得部分、嘈杂或结构上具有干扰性，**grounding** 仍可能崩溃。

该 **taxonomy** 是跨论文综合，而非某一 **benchmark** 的封闭标签集；其用处在于将 **hallucination** 文献与更广泛的 **grounding pipeline** 对齐。核心问题不仅是回答是否错误，而是**语言与视觉证据之间的绑定**以何种方式、在何处断裂。

### 5.2 Benchmarks and Diagnostic Frameworks {#subsec:failure-benchmarks}

**Evaluation methodology** 的演进清晰：早期工作问模型是否提及不存在物体；新 **benchmarks** 追问错误在 **perturbation** 下是否持续、模型是否偏向回答「是」、答案是否**内部一致**，以及失败来自先验还是感知。

**POPE** 是稳定度量 **object hallucination** 的转折点：不依赖脆弱字符串匹配的 **free-form caption**，而将评估转为平衡的 **Yes/No polling**（如「图像中是否有椅子？」）。三种负采样：**Random**、**Popular**、**Adversarial**（后者用**常共现**物体作 **hard negatives**）。该设计揭示若干 MLLM 的强 **over-affirmation** 倾向，并在不依赖 **caption** 风格的前提下使 **hallucination** 可测。

**Hallu-PI** 将评估从干净图像扩展到 **perturbed inputs**；七种扰动场景含模糊、噪声、天气效果、数字伪影、裁剪、图像拼接与 **prompt misleading**；目标从物体存在性扩展到属性与关系。对 **grounding** 分析而言：**robustness** 不仅应在标准照片上测，也应在削弱或转移注意力的视觉与 **prompt** 条件下测。

**HallusionBench** 在本组中最具诊断性：约 **1,129** 手工 **VQA pairs**、**346 figures**，含人工编辑图像；用 **aAcc**（答案级）、**fAcc**（图级一致性）、**qAcc**（问题级一致性）评估；并含 **Yes/No Bias**、**Consistency** 与 **Diagnostic** 测试，将失败分为 **language hallucination**、**visual illusion** 与混合/不确定。因而能区分**从先验作答**与**误读图像**。

**LRV-Instruction** 中的 **GAVIE** 提供互补视角：在**无固定人工金标答案**的情况下，对输出同时打 **accuracy** 与 **relevancy** 分。**Hallucination** 缓解不应与「变短、变回避」混淆——系统可通过少说废话来「降低幻觉」；**GAVIE** 显式检验：忠实度提升是否仍保持 **instruction following**。

**Table. Representative benchmarks and diagnostic tools for Section 5**

| Benchmark / framework | Main target | Task format | What it adds beyond earlier work | Main limitation |
|------------------------|-------------|-------------|-----------------------------------|-----------------|
| POPE | Unsupported object claims | Balanced Yes/No polling | Stable existence probing under random, popular, and adversarial negatives | Focuses mainly on object existence |
| Hallu-PI | Hallucination under degraded inputs | Generative + discriminative | Perturbation stress test; covers existence, attributes, and relations | Smaller, stress-test-style benchmark |
| HallusionBench | Prior-vs-perception failure diagnosis | Handcrafted VQA control pairs | Separates language hallucination from visual illusion; adds bias and consistency tests | Narrower than broad web-scale usage distributions |
| GAVIE in LRV-Instruction | Accuracy plus instruction following | Open-ended evaluation with GPT-4 assistance | Distinguishes hallucination reduction from degraded task compliance | Relies on evaluator model judgments |

在这些 **benchmarks** 上，一个模式**始终**成立：**hallucination** 在**防止模型躲在冗长或风格变化背后**时**最容易**被暴露。另一个模式是：**可靠性**不仅取决于**正确性**，还取决于**拒答行为**、**一致性**以及在**证据被改变**下的**鲁棒性**。

### 5.3 How Grounding Failure Propagates During Generation {#subsec:failure-propagation}

近期工作越来越多地从 **benchmark** 构造转向**机制**分析；共同结论是：**hallucination** 通常不是随机 **decoding** 事故，而是**弱视觉证据被语言侧捷径逐步取代**的过程。

**LURE** 用统计方法识别 **object hallucination** 的三类驱动因素：**co-occurrence bias**（与真实物体共现的物体更易被 **hallucinate**）、**decoding uncertainty**、**object position**（**hallucinated** 提及常出现在低置信 **decoding** 步与生成描述的后段）。这表明 **hallucination** 常在模型到达语义上**似 plausible** 但视觉上**弱支持**的片段时产生，且模型选择**继续生成**而非**弃权**。

**OPERA** 在 **token** 层面解释这种漂移：在 **self-attention** 中反复出现 **knowledge aggregation** 或 **partial over-trust**——后续 **tokens** 过度依赖邻近摘要式 **tokens**，对序列前端的原始 **visual tokens** 依赖减弱。由于当前 MLLM 常把 **image tokens** 放在上下文**前部**，长 **generation** 会随时间**削弱**视觉证据。用 **grounding** 话说：回复**起始于** **visually anchored**，随后**越来越多地**由**已生成文本**中介。

**VCD** 补充以 **visual uncertainty** 为中心的因果叙事：**当图像被扰动**时，**MLLMs** 更易回退到语言先验与数据集级统计偏置；高频或共现物体在噪声输入下更常被 **hallucinate**。弱感知**并非**仅增加随机性，而是**系统性**推模型走向其**已预期**的物体与属性。

**HallusionBench** 从诊断角度强化同一点：若模型对**本应反转答案**的编辑图仍给相同答案，失败**不是**简单误分类，而是**参数记忆压倒了真实视觉证据**；若模型随编辑改变答案但**仍从编辑图提取错误信息**，则更接近 **visual illusion**。这解释为何**部分干预**应针对先验，**另一部分**应针对感知。

**Hallu-PI** 表明该传播对**输入条件**高度敏感：裁剪、拼接、误导 **prompt** 都会增加模型 **attend** 错误场景区域或用语言侧猜测解决歧义的概率。从 **grounding** 看，这些扰动暴露：**word–region binding** 一旦场景偏离「干净、居中、单图」设定，**仍非常脆弱**。

**统一机制**：**hallucination** 出现在 **grounding signal** 相对 **prior signal** **变弱**之时。弱化可来自噪声输入、长自回归链、弱负监督或偏训练分布；症状相同：**流利文本不再被图像所能严格支持的内容所约束**。

### 5.4 Calibration, Confidence, and Trustworthy Alignment {#subsec:failure-calibration}

第 5 节多篇论文不只检测错误答案，还追问更硬的问题：**模型是否知道自身 grounding 何时弱？** 这本质上是 **calibration** 问题。

**POPE** 与 **HallusionBench** 给出最简证据：**POPE** 显示许多 MLLM 存在极端 **Yes-bias**——在平衡设定下仍**过度肯定**物体存在；**HallusionBench** 表明某些模型**问题级**准确率可优于随机，但**图对或图级一致性**仍很差，因为答案**不稳定或系统有偏**。二者均说明 **confidence** 与真实视觉支持**错配**。

**LRV-Instruction** 在**数据层面**应对：许多 MLLM 的 **instruction tuning** 以**正样本**为主，模型**学会服从**强于**学会拒绝**。提出的约 **400K** 数据集同时含**正**与**负**指令；负样本覆盖**不存在物体操纵**、**存在物体操纵**与**知识操纵**，并含陈述与疑问形式。概念上这是 **calibration** 干预：教模型**有时必须说不**、反驳 **prompt**，或**显式指出不一致**。

**RLHF-V** 在**对齐层面**应对：不收集粗粒度整句排序，而要求标注者对 **hallucinated spans** 做**片段级修正**，并用 **Dense Direct Preference Optimization（DDPO）** 训练，使**局部**修正获得更强学习信号。效果：降低标签歧义（期望行为在**局部**明确）；更直接教模型**grounded** 与 **ungrounded** 文本之间的**行为边界**。论文还指出：**hallucination** 可因**低质量文本监督**甚至训练时**粗心图像裁剪**而加剧——再次将 **hallucination** 框定为**监督与视觉证据不匹配**。

**ViGoR** 采用相关但不同的 **reward modeling** 视角：收集**逐句人类评分**，并与 **Grounding DINO** 式存在性检查等**自动 reward** 流结合，用于 **rejection sampling** 与监督式 refinement。相对粗粒度 **reward model**，**ViGoR** 承认长描述可能**句级混合** **grounded** 与 **hallucinated** 内容，故在**短语或句子**粒度上评估忠实度——这与 **grounded generation** 中「校准」的正确单元**往往**是**短语/句**而非整段回答**一致**。

从综述角度，**RLHF-V** 与 **ViGoR** 指向同一结论：**MLLM** 的 **calibration** 难以仅靠**更大模型**解决；关键在于训练与对齐是否提供**足够稠密**的反馈，使模型学会在证据**缺失**、**模糊**或与图像**矛盾**时如何表现。

### 5.5 Mitigation Strategies and Trade-offs {#subsec:failure-mitigation}

**缓解**文献几乎覆盖 **MLLM pipeline** 的每一层：**prompt**、**decoding**、**事后修订**、**外部验证**、**instruction tuning**、**reward alignment**。没有单一层在所有设定下均最优；各层在成本、通用性与忠实度之间权衡不同。

**Prompt-time 防御（Hallu-PI）。** **Perturbed-Reminder** 与 **Perturbed-ICL** 提醒模型注意扰动输入，或提供**鲁棒行为**的 **in-context** 示例。优点：无训练、易部署；缺点：**不**改善内部 **grounding**，主要把模型推向更谨慎行为，**仍**依赖 **prompt** 形式与 **context** 预算。

**Decoding-time 修正（OPERA、VCD）。** 二者均在**推理时**干预，但机制不同：**OPERA** 惩罚与**过度信任摘要 token** 相关的 **self-attention** 模式，并可通过 **retrospection-reallocation** 回滚 **decoding**；**VCD** 对比**原图**与**distorted** 视觉输入下的 **next-token** 分布，并结合 **adaptive plausibility constraint**，压低**过于兼容先验驱动解码**的输出。优点：无需重训；局限：只能**引导**现有模型，**无法**修复底层 **visual-language representation**。

**Post-hoc 修订（LURE）。** 训练轻量 **hallucination revisor**，基于不确定性与位置感知 **masking** 改写疑似 **hallucinatory** 描述。实用且 **model-agnostic**，但依赖**已有缺陷**的首遍输出，并增加延迟。

**外部验证与修正（Woodpecker）。** 五阶段流水线：**key concept extraction** → **question formulation** → **visual knowledge validation** → **visual claim generation** → **hallucination correction**。具体使用 **GPT-3.5** 级语言推理 + **Grounding DINO** 做物体级验证 + **BLIP-2-FlanT5-XXL** 做属性级 **VQA**。优点：**可解释**，修正后的回答可**绑定**到 **bounding-box** 证据；代价：管线复杂、多模型、且依赖各专家模型的强弱（更难位置推理时尤甚）。

**Data-centric 鲁棒 instruction tuning（LRV-Instruction）。** 在**更早**阶段改变 **instruction tuning** 所学分布；平衡正负指令同时改善**鲁棒性**与**拒答**能力。比 **prompting** 或事后编辑**更根本**，但需重训，且**合成负样本**质量至关重要。

**Preference 与 reward 对齐（RLHF-V、ViGoR）。** 直接以细粒度 **reward** 塑造行为：**RLHF-V** 用人类修正 + **DDPO**；**ViGoR** 结合人类句级反馈与检测器奖励 + **rejection sampling**。比纯数据调参**更直接**瞄准可信性，但需专门反馈管线，并可能继承 **reward** 源的盲点——**ViGoR** 指出基于检测器的自动奖励对**物体存在**最强，对 **stuff regions**、属性与布局**较弱**。

**Table. Main mitigation strategies reviewed in Section 5**

| Method | Intervention layer | Main mechanism | Strength | Main limitation |
|--------|-------------------|----------------|----------|-----------------|
| Hallu-PI | Prompting | Perturbed-Reminder / Perturbed-ICL | Training-free and cheap | Prompt-sensitive; does not improve internal grounding |
| LURE | Post-hoc revision | Uncertainty- and position-aware rewriting | Model-agnostic and practical | Extra pass; repairs only after generation |
| LRV-Instruction | Instruction tuning | Balanced positive/negative instructions | Improves rejection behavior at training time | Requires retraining; quality depends on synthetic data |
| OPERA | Decoding | Over-trust penalty + retrospection | No extra training; targets long-form drift | Limited by the base model's representation quality |
| VCD | Decoding | Contrast original vs distorted-image distributions | Training-free; effective across multiple MLLM families | Depends on distortion design and decoding hyperparameters |
| RLHF-V | Alignment | Segment-level corrections + DDPO | Data-efficient trustworthiness alignment | Requires human correction data |
| Woodpecker | External verification | Detector/VQA-backed correction pipeline | Interpretable and evidence-linked | Heavy pipeline; relies on external experts |
| ViGoR | Reward modeling | Fine-grained human + automatic rewards | Improves grounding while preserving detail | Automatic rewards are uneven across error types |

**干预越早**越可能重塑默认行为，但训练与数据成本越高；**prompt/decoding/post-hoc** 便宜模块化，但多在 **base grounding** 已弱后补偿。

### 5.6 Summary {#subsec:failure-summary}

近期第 5 节文献**大幅拓宽**了 MLLM 中 **「hallucination」** 的含义。**POPE** 稳定探测**不支持的物体断言**；**Hallu-PI** 表明这些失败在扰动下**恶化**；**LURE** 将 **hallucination** 与 **co-occurrence bias**、不确定性与**位置**联系起来；**HallusionBench** 分离 **language hallucination** 与 **visual illusion**；**LRV-Instruction** 表明**平衡负监督**重要；**OPERA** 与 **VCD** 表明 **inference-time decoding** 可**部分**对抗先验驱动 **generation**；**RLHF-V** 与 **ViGoR** 将可信性框定为**细粒度对齐**问题；**Woodpecker** 展示**外部验证**闭环的潜力。

对本综述而言，主结论是：**hallucination** 应读作 **grounding** 的 **failure regime**。模型可能因从未学会拒绝无支持断言**而**失去 **grounding**；可能因 **visual uncertainty** **放大**先验；可能因长 **decoding** **偏离**早期 **image tokens**；也可能因对齐信号过粗**无法**教可靠 **abstention**。这也澄清未来工作的开放问题：强 **MLLM** 不仅要**能生成** **grounded outputs**，还要在 **generation** 全程**对 grounding 的限度保持校准**。

---

## 6. Discussion and Future Directions {#sec:discussion}

前几节沿 **capability chain** 展开，而非孤立任务列表：**visual representations** 决定保留何种 **spatial structure**；**grounding methods** 决定该结构如何转化为 **language** 与 **image regions** 之间的可用对齐；**spatial reasoning** 建立在该对齐之上；**hallucination** 则在链条变弱时暴露 **failure regime**。本节综合跨阶段**共享瓶颈**，并给出对领域现状的**总体判断**。

### 6.1 Shared Bottlenecks Across the Pipeline {#subsec:discussion-bottlenecks}

尽管所综述方法多样，**pipeline** 几乎每一阶段都反复出现三类瓶颈。

**小物体与细粒度细节。** **Resolution** 仍是**结构性**约束。第 2 节表明低分辨率输入会在 **grounding** 开始之前就**抹掉**小物体；第 3 节表明 **coordinate-based grounding** 继承这些早期表征决策带来的**量化**与 **token budget** 权衡；第 4 节进一步表明，涉及**小、远或部分可见**物体的 **spatial judgments** 往往触发**最陡**的性能跌落。含义一致：当前 MLLM 仍偏**场景级**理解，一旦 **grounding** 或 **reasoning** 需要**子区域**精度，**仍脆弱**。

**密集与杂乱场景。** 多数 **benchmarks** 与训练集仍偏向**相对干净**、**物体数量少**的场景。在杂乱环境中，**多种弱点会同时作用**：**encoder** 模糊相邻物体、**box-level grounding** 难以处理**重叠**与**小范围**，**spatial reasoning** 面临**潜在物体关系**的组合爆炸。这也是**强 benchmark 表现**不自动转化为**真实世界 spatial 行为**的原因之一。

**跨图像与时间推理。** 所综述方法**绝大多数**针对**单张图像**；而许多实际 **grounding** 问题需要跨帧跟踪 **spatial state**、跨时间比较视角，或将多视角整合为单一连贯场景模型。**MM-Spatial** 中的 **multi-view geometry** **部分**回应这一点，但**时间上的 spatial reasoning** 仍**欠发展**。当前 MLLM 仍更多为**静态感知**优化，而非**动态 spatial understanding**。

### 6.2 The Grounding–Reasoning Interaction {#subsec:discussion-grounding-reasoning}

本综述最清晰的结论之一是：**grounding** 与 **spatial reasoning** **既非同一**也**非独立**。

**Grounding 是 reasoning 的必要条件。** **SpatialRGPT** 等区域感知方法表明：当模型显式锚定到相关物体或区域时，**spatial reasoning** **显著**改善。更一般地，许多 **spatial reasoning** 失败**部分**是**识别失败**：若模型尚未定位**哪两个物体**应进入关系比较，就无法对二者关系做正确推断。

**但 grounding 不是 reasoning 的充分条件。** 精确定位**不保证**对 **depth**、**distance**、**occlusion** 或多步 **spatial composition** 的成功判断。**SpatialVLM** 与 **MM-Spatial** 均表明：一旦任务超越 **2D region alignment**，常需显式 **3D** 或 **depth-aware** 监督。在此意义上，**grounding** 提供推理的**实体**，但**不提供**完整**几何**。

**失败在阶段间级联。** 最有用的综合是**级联视角**：部分失败始于 **encoder**（相关 **spatial information** 表征弱）；部分始于 **grounding**（错定位区域或在长文 **generation** 中丢失局部证据）；部分始于 **reasoning**（已有正确区域但缺乏关系或几何机制）；第 5 节增加**最后阶段**：链条已弱时，模型仍可能产生**流利且高置信**的语言，将上游 **spatial** 错误转化为下游 **hallucination**。

该级联视角反对**窄补丁式**修复：仅加强某一环节（如更强 **decoder** 或事后 **hallucination** 补丁），若更早阶段的 **visual grounding** 仍不稳定，**增益常有限**。

### 6.3 Downstream Significance {#subsec:discussion-significance}

这些能力的**实践重要性**很直接。**GUI agent** 必须识别精确视觉目标、推理布局、并判断界面状态是否如预期变化。**Robot** 必须定位相关物体、估计**可行动**的 **spatial relations**，并在杂乱、**occlusion** 与视角变化下保持鲁棒。两类场景中，限制因素**很少**是通用语言流利度，而是语言能否**持续**、**可靠地**锚定**有视觉支持**的 **spatial structure**。

因此 **grounding** 不应被视为小众 **benchmark** 技能。它是多模态系统能否从**描述性助手**走向**可信 agents** 的**操作基底（operational substrate）**。

### 6.4 Open Problems {#subsec:discussion-open-problems}

以下四个开放问题对下一阶段领域发展**尤为关键**。

**1. Unified grounding evaluation。** 当前 **evaluation** 仍分散在 **box-level REC**、**segmentation**、**region description**、**spatial QA**、**hallucination stress tests** 等之间。需要更统一的框架：在**输出粒度**、**场景复杂度**与**鲁棒性条件**下，用共同的「**visually justified behavior**」概念贯穿评估。

**2. Closing the 2D–3D gap。** 近期最强的 **spatial reasoning** 系统往往依赖显式 **depth** 估计或 **multi-view** 监督。开放问题是：**MLLM** 能否**仅从 2D 数据**内化更丰富的 **3D structure**，抑或对鲁棒 **depth/distance-aware reasoning** 而言，**显式几何监督**仍将长期必要。

**3. Spatial reasoning under composition and scale。** 多数 **benchmarks** 仍聚焦**成对**或**短形式** **spatial judgments**；真实任务需要对**多物体**的组合推理、**传递推断**，以及在多种 **spatial scales** 上依赖上下文的判断。将 **grounding** 从「找到该区域」扩展到「跟踪该**结构化场景**」仍是重大挑战。

**4. Calibration and confidence in grounding。** 第 5 节暗示：当前 **MLLM** 的核心弱点**不仅**在于**会 hallucinate**，还在于**常常不知道**自身 **grounding** 何时弱。对高风险部署而言，可靠的 **uncertainty** 估计、**abstention** 与 **confidence calibration** 可能与**原始准确率**同等重要。

### 6.5 Concluding Remarks {#subsec:discussion-conclusion}

基于此处综述的文献，可归纳三条**更宏观**的判断。

第一，**grounding 是连接 multimodal perception 与 spatial reasoning 的中间能力。** 它不只是众多下游任务之一，而是**视觉结构**得以用于**语言引导的行动与推断**所必经的层次。

第二，**当前 MLLM 的主要弱点较少在于缺乏流利 generation，而在于缺乏 stable visual anchoring。** 模型往往能**令人印象深刻地**描述场景，但从 **encoder** 表征到 **grounded reasoning** 的链条在小物体、杂乱、深度歧义、扰动与长文 **generation** 下**仍脆**。

第三，**未来进展不太可能来自任何单一干预层。** 更好的 **encoder**、更丰富的 **grounding** 输出、更强的 **spatial** 监督、改进的 **decoding** 与更细粒度对齐**都重要**，但其效果**只有**在**整条 capability chain** 上被**联合**考虑时才**compound**。

领域因此处于重要**转折点**：**visual grounding** 与 **spatial understanding** 在 **MLLM** 中**已非缺席**，但也**远未解决**。下一步进展取决于将 **grounded perception**、**spatial reasoning** 与 **calibration** 视为**同一多模态系统**中**紧密耦合**的性质，而非彼此独立的插件。

---

## 附录：源文件与引用

- **LaTeX 主文件**：`capabilities/grounding/manuscript/archive/grounding_review.tex`（含 **Abstract** 与 **Keywords**；目录已加入 `.gitignore`，仅本地保留）
- **正文**：`.../archive/grounding_review_body.tex`（**§1–§6** 与小节 `\label{...}` 与本 Markdown 标题对应）
- **参考文献**：`.../archive/grounding_review_refs.bib`（`\citep{...}` 键与 TeX 正文一致）

**覆盖说明**：本文件已包含 **Abstract**（中英）、**Keywords**、**第 1–6 节**及全部 **subsubsection** 主题；**longtable** 均已转为 Markdown 表格；第 4 节 **SpatialVLM / SpatialRGPT / MM-Spatial** 与第 5 节 **taxonomy / propagation / mitigation** 等与 `grounding_review_body.tex` **逐段对齐补全**。编译 PDF 时仍以 `\bibliography{grounding_review_refs}` 为准。

如需 **arXiv** 链接对照，可参见同目录 **`citation_arxiv_links.md`**（与本中文版一并提交仓库）。

原按节草稿 **`section1_draft.md`–`section6_draft.md`** 位于 **`manuscript/archive/`**（见该目录下 `README.md`），与 LaTeX 源同为本地归档，**不推送 GitHub**。
