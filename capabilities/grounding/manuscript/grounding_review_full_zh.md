# 多模态大模型中的视觉 Grounding 与空间理解：方法、表征与失效模式
*Visual Grounding and Spatial Understanding in Multimodal Large Language Models: Methods, Representations, and Failure Modes*

> 本文档由本地 `manuscript/archive/` 中的 TeX 源整理。正文以**中文叙述为主**；**grounding** 等与文献一致的术语保留英文。  
> **术语说明：** **visual grounding（视觉 grounding）** 在文献中常定义为：根据**自然语言描述**在图像中**定位对应物体或区域**（及相关的框、分割等预测）。下文用 **grounding** 专指该能力，不单译为「对齐」——「对齐」在文中仅用于表示特征匹配、图文对比学习、人类偏好学习等含义。

---

## Abstract

本综述讨论多模态大模型（MLLM）中的**视觉 grounding** 与**空间理解**如何形成，以及为何在真实场景下仍会失效。我们将文献串成一条**能力链**：视觉表征决定还能保留多少空间结构；**grounding** 方法把这种结构变成语言与图像区域之间的可用对应；空间推理建立在这种对应之上；链条变弱时，**幻觉**（hallucination）便暴露出系统的失效方式。在编码器、连接器、**grounding** 输出、空间类评测与幻觉缓解等工作中，反复出现的结论是：**grounding** 是连接「看见」与「推理空间关系」的中间环节；当前短板往往不在于话说不流利，而在于**语言与图像绑得不稳**。文末讨论统一评测、三维感知式推理、组合式空间理解与置信度校准等方向。

**Keywords:** multimodal large language models, visual grounding, spatial reasoning, hallucination, multimodal alignment

---

## 1. Introduction {#sec:introduction}

多模态大模型早已不满足于图像描述与视觉问答，而是被要求**精确定位物体**、判断**物体之间的空间关系**、理解场景的**三维结构**。从「图里有什么」到「在哪、和谁相邻」，是能力上的跃迁：从泛泛的图文交互，到**以视觉为依据的表述**。界面智能体要点中按钮，机械臂要伸向正确物体，无人系统要判断行人在障碍物前还是后——若**grounding**（按描述定位图像中的对象或区域）与**空间推理**不可靠，模型就只是「会说话、顺带看了眼图」的文本生成器。

然而近期研究揭示强烈反差：模型能写出细腻的场景描述，却在**最基本的空间判断**上频频出错（谁在上、谁在下、某物是否真的在图中）。多项基准测试表明，简单空间关系任务上表现接近随机猜测（Liu et al., VSR; Kamath et al., What'sUp）；视觉编码器对推理所需的模式近乎「视而不见」（Tong et al., Eyes Wide Shut）；还会**编造**图中没有的物体、属性或关系（Li et al., POPE; Guan et al., HallusionBench）。这些不是孤立故障，而是整条**处理流程**的问题：能否稳定地依赖视觉，取决于上游保留了什么信息、如何变成**grounding** 输出、以及后续推理与**长文本生成**时是否还能**紧扣图像**。

本文的核心观点是：**视觉 grounding 是连接「表征」与「空间推理」的中间层；幻觉最宜理解为这条链在弱化时的典型失效方式。** 因此下文不把编码器、**grounding** 方法、空间推理与幻觉当作四块互不相关的题目，而把它们看作**同一套空间相关行为**如何形成、又如何一起崩掉。

### 1.1 Scope and Contributions {#subsec:intro-scope}

本综述梳理多模态大模型中**视觉 grounding 与空间理解**的近期工作，关注架构、表征与训练如何决定模型能否**稳定地依图说话**。我们以**能力**为主线，不展开具体产品：更关心机器人、界面助手等系统**在技术上要满足什么条件**，而非系统实现细节。

全文围绕四个问题：

1. **怎样的视觉表征能支撑 grounding？**（第 2 节）  
   考察视觉编码器、分辨率与多尺度策略、图文连接器这一条线，看从像素到语言模型输入之间还能剩下多少空间结构。共识是：**grounding** 不仅靠「更大的编码器」，还要靠**少压缩局部细节**的连接器与分辨率设计。

2. **模型如何把 grounding 做出来？**（第 3 节）  
   从把坐标当文本生成、到区域级交互、再到分割级输出，方法不断变强；张力始终在于：既要保留「文本进、文本出」的灵活接口，又要能做**结构化的空间预测**。

3. **模型能否推理空间关系？**（第 4 节）  
   介绍诊断性评测与拓扑、方向、深度等相关方法。结论是：**grounding** 与空间推理绑得很紧；显式 **grounding** 到区域往往有助于推理，但一旦涉及深度、距离或组合推断，仅有「指对物体/区域」仍不够。

4. **grounding 失败如何表现并变成幻觉？**（第 5 节）  
   从 **grounding** 视角看「胡说」：物体是否存在、输入扰动、语言型幻觉与视觉型错觉的区分、置信度，以及解码时修正、人类反馈与奖励学习等缓解手段。要点是：很多「幻觉」本质是 **grounding** 不稳或被生成过程冲掉。

这四个问题连成一条**能力链**：表征决定上限；**grounding** 方法决定词与区域如何对应；空间推理在对应之上展开；第 5 节的失效模式则说明歧义、弱证据或长文生成时链在哪里断。第 6 节归纳瓶颈与展望。

### 1.2 与既有综述的关系 {#subsec:intro-positioning}

近期工作有的侧重「视觉 grounding」任务分类（Xiao et al.），但重心仍在传统检测流水线，较少谈多模态大模型**原生**的 **grounding** 方式。通用多模态综述常把 **grounding** 列为一项能力，却很少追到编码器、连接器与分辨率。空间推理或基准测试论文多谈**评什么**，却很少把分数差归因到上游表征与 **grounding**。

本文把 **grounding** 放在**感知**与**推理**之间，不追求覆盖所有多模态能力，而解释**空间上靠谱的行为**如何出现、为何在多种任务上会一起翻车。范围比「全能多模态综述」窄，但把**从表征到失效**串成一条线。

---

## 2. 视觉表征：作为 grounding 的基础 {#sec:representations}

若要把语言**锚到**图像里的具体区域，首先要有足够丰富的视觉表征，以保留细粒度空间细节。三类设计共同决定「传到语言模型里时还剩多少空间信息」：**(i)** 从像素提特征的**视觉编码器**；**(ii)** 分辨率与多尺度策略（决定「能看清多细」）；**(iii)** 把视觉特征送进大语言模型输入空间的**图文连接器**。本节以八个代表性多模态大模型为例，看这些选择如何影响下游 **grounding** 与定位。

### 2.1 Vision Encoder Selection {#subsec:rep-encoders}

#### 2.1.1 语言监督编码器仍占主流 {#subsubsec:rep-language-supervised}

当前绝大多数多模态大模型以 **CLIP** 系 **Vision Transformer（ViT）** 为视觉骨干。例如 **LLaVA-1.5** 用 336 像素的 CLIP ViT-L/14；**Qwen-VL** 用 OpenCLIP 的更大 ViT-bigG；**CogVLM** 用 EVA2-CLIP-E。**LLaVA-OneVision** 则换用 SigLIP，用 sigmoid 对比损失替代 CLIP 常用的 InfoNCE，并报告下游全面提升。共同点：这些编码器都先用**图文对比学习**与语言对齐过，特征空间与词向量更接近，后续接大语言模型更省事。

#### 2.1.2 放大视觉编码器 {#subsubsec:rep-scaling}

**InternVL** 把视觉编码器做到约 **InternViT-6B**（约 59 亿参数），规模上首次接近旁边的大语言模型。训练上先在大规模图文对上对比学习，再生成式微调；在 ImageNet、ADE20K 分割等任务上表现很强。这说明：**视觉侧容量**在以往多模态系统里常被低估——很多方案用 0.3–1.8B 的视觉编码器配 7–13B 的语言模型，语言侧算力未必能充分发挥。

#### 2.1.3 Beyond Language Supervision: Self-Supervised and Hybrid Encoders {#subsubsec:rep-self-supervised-hybrid}

**Cambrian-1** 在相同训练设置下系统比较了 **23 种**视觉骨干，包括 CLIP 变体、自监督的 **DINOv2**、**ConvNeXt**、带深度监督的模型等。主要结论：

- 在通用、知识、OCR 等评测上，**语言监督**模型整体仍强于**纯自监督**，与 CLIP 类数据里「带文字的图」更多有关。
- **DINOv2** 在**偏视觉**的评测（空间关系、深度顺序等）上很强，有时超过弱 CLIP，说明自监督表征能补几何与结构信息。
- **ConvNeXt** 等卷积结构适合高分辨率，OCR 等任务上常有优势。
- 扩大指令微调数据、微调时解冻视觉编码器，可明显缩小 DINOv2 与 CLIP 的差距。

这些与 **grounding** 直接相关：定位要保留空间结构，而仅靠「图文对比」目标并不保证学到足够几何信息。

**Mini-Gemini** 用**双编码器**：低分辨率一路用 CLIP ViT 产生查询，高分辨率一路用 ConvNeXt 提供细节，两路在 patch 级做交叉注意力（论文称 patch info mining），在**不大幅增加**送入语言模型的序列长度前提下增强视觉 token。

### 2.2 High-Resolution and Multi-Scale Strategies {#subsec:rep-resolution}

对 **grounding** 任务而言，**输入分辨率**往往是最敏感的因素之一：在 224 像素输入里只占极少数像素的物体，模型几乎「看不见」。下表汇总各代表模型的分辨率策略。

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

主要可归纳为以下范式：

- **固定分辨率**：最简单。**BLIP-2** 用 224 像素，早期 **LLaVA** 用 336 像素。算力省，但细粒度差。**LLaVA-1.5** 表明仅从 224 提到 336，就能**明显减少**幻觉式描述，说明不少「数据噪声」问题，其实是**看得不够细**。
- **动态切块 / AnyRes**：把图切成多块，每块用编码器原生分辨率处理，再合并特征。**LLaVA-1.5-HD** 等将图像分成多块网格并加全局视图；**OneVision** 等进一步支持多裁剪、对词元做压缩，并按单图/多图/视频等场景控制序列长度。经验上：**提高分辨率**往往比**盲目加长序列**更有效。
- **双编码器或多编码器**：用不同尺度两路编码，缓解「分辨率 vs 序列长度」矛盾。**Mini-Gemini** 低分辨率 ViT 配高分辨率 ConvNeXt；**Cambrian-1** 可组合多路骨干，各取所长。
- **分阶段提高分辨率**：**Qwen-VL**、**CogVLM** 等在预训练中先低分辨率再抬高，先学粗粒度 grounding 再细化，避免全程高分辨率训练太贵。

### 2.3 图文连接器 {#subsec:rep-connectors}

连接器把视觉特征送进大语言模型的输入空间；**保留多少位置信息、压缩多少**，直接决定 grounding 质量。

#### 2.3.1 线性层与 MLP {#subsubsec:rep-linear-mlp}

**LLaVA-1.5** 表明两层 MLP 就很好用：用较少数据也能与海量图文预训练的系统竞争。做法是让 **ViT 的每个 patch 对应语言模型侧的一个词元**，空间结构保留得好，但**词元数随分辨率近似平方涨**，细节与上下文长度之间要权衡。

#### 2.3.2 Q-Former {#subsubsec:rep-q-former}

**BLIP-2** 的 **Q-Former** 用 32 个可学习查询与图像特征做交叉注意力，输出固定长度向量，**与分辨率无关**。这是典型的**信息瓶颈**：算力省，但空间结构被冲掉，**难以精确定位**，所以 **BLIP-2** 本身不好直接做框预测或 **grounding** 任务。

#### 2.3.3 带位置编码的交叉注意力压缩 {#subsubsec:rep-cross-attn-resampler}

**Qwen-VL** 用一层交叉注意力把视觉序列压到固定长度，**但在注意力里加入二维位置编码**，减轻压缩丢位置信息的问题。因此可以把**边界框坐标**写成归一化数字串，当普通文本输出，无需单独接检测头。

#### 2.3.4 视觉专家（深层融合）{#subsubsec:rep-deep-fusion}

**CogVLM** 在语言模型每一层为图像词元加**视觉专家**（独立注意力与前馈层），文本仍走原权重。**CogVLM-Grounding** 在 RefCOCO 等上很强，甚至超过专用检测模型。**消融**表明：只训浅层适配器，远不如**层层融合**——视觉特征需要逐层变换才能与语言内部表示对齐。

**Table. Ablation: impact of connector depth on CogVLM performance**

| Configuration | Trainable Params | NoCaps CIDEr | VQAv2 |
|----------------|------------------|--------------|-------|
| MLP Adapter only（shallow） | 140 M | 111.5 | 73.8 |
| Full LLM + Adapter | 6.9 B | 118.5 | 78.9 |
| Visual Expert every 4th layer | 1.7 B | 117.4 | 77.6 |
| Visual Expert every layer（full） | 6.6 B | 120.1 | 80.0 |

#### 2.3.5 空间视觉聚合器 SVA {#subsubsec:rep-sva}

**Cambrian-1** 提出 **SVA**，面向多编码器：用可学习的二维查询与多路特征交互，**强调每个查询对应一块空间区域**，减轻「全局注意力」把空间冲掉的问题；并在语言模型中每隔几层再插交叉注意力，让深层仍能访问较完整的视觉信息。强压缩时（例如 576 词元压到 36）比简单插值更省空间信息。

#### 2.3.6 Patch 信息挖掘 {#subsubsec:rep-patch-info-mining}

**Mini-Gemini** 连接器在双编码器之间做交叉注意力：低分辨率为查询，高分辨率为键值，**每个查询只看对应空间子区域**，在**不增加序列长度**的前提下增强细节。

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

1. **Grounding 依赖连接器里是否保留空间结构。** **Qwen-VL**、**CogVLM**、**InternVL** 等要么层层融合、要么带位置感知的压缩，**BLIP-2** 式 32 个全局查询则很难支持精细 **grounding**。
2. **分辨率高不等于具备 grounding 能力。** **OneVision** 分辨率很高，但若没有 grounding 数据，仍不会做框任务；**Qwen-VL** 在适中分辨率下配合 grounding 数据与多任务预训练，仍能取得强 **grounding** 表现。
3. **数据与目标与架构同样重要。** 例如 **CogVLM** 除架构外，还有大规模「名词短语—框」预训练；**Cambrian-1** 也依赖大规模指令数据。
4. **自监督骨干**（如 **DINOv2**）可补空间关系、深度顺序等，**Cambrian-1** 等有实证。
5. **视觉编码器与语言模型规模**仍常不对称：大语言模型配小视觉编码器是否限制密集场景与小物体，仍是开放问题。

### 2.5 小结 {#subsec:rep-summary}

从编码器、分辨率到连接器，这条链路像**漏斗**，决定 grounding **理论上**能好到什么程度。趋势是：提高分辨率（切块或双编码器）、连接器少吞掉空间结构、多种骨干互补。但**表征好**不等于**输出一定足够 ground**，只决定「还能用什么空间信息」。下一节讨论：如何把保留的结构变成**坐标、区域、分割**等可用输出。

---

## 3. Grounding 方法：从坐标到区域 {#sec:grounding-methods}

第 2 节问「还能保留多少空间细节」；第 3 节问这些细节如何变成**可用的 grounding 行为**。近年工作大致沿三条越来越强的输出形式：**(i)** 把坐标当文本生成；**(ii)** 让用户框选区域参与多轮对话；**(iii)** 把语言与**像素级 mask** 绑定，而不仅是矩形框。核心难点不只是「预测在哪」，而是**位置怎么表示**，才能既兼容「下一个词」式生成，又便于指令微调与多任务。本节从单框经典设定，写到对话式、开放词表、越来越密的 grounding 系统。

### 3.1 Coordinate Prediction as Language Generation {#subsec:grounding-coordinates}

最早一批面向 **grounding** 的 MLLM 将定位视为 **language modeling** 的特例：若 **LLM** 能自回归生成词，或许也能自回归生成 **coordinates**。该表述的吸引力在于：无需单独 **detector head**，保留 **instruction-tuned MLLM** 统一的 text-in/text-out 接口，并可用与普通对话相同的 **next-token objective** 训练 **grounding**。

**Kosmos-2** 将 **bounding box** 每个角点离散到 **`32×32` grid** 上的 **location token**，并以类超链接格式接在对应 **text span** 之后，使 **grounding** 成为同时包含词与 **spatial tokens** 的序列预测。输入输出对称：模型既可接收框做 **referring**，也可输出框做 **grounding**；架构不变，**grounding** 完全由数据与 **tokenization** 注入。配合 **GrIT**（约 **91M images**、**115M text spans**、**137M boxes**），生成模型零样本迁移表现突出：例如 Flickr30k Entities test 上 **78.7** **R@1**、RefCOCOg test 上 **61.65** accuracy。局限在于输出绑定离散 **bins** 与 **`224×224` resolution**，继承 **quantization error**，细粒度或小物体 **grounding** 困难。

**Shikra** 保持自回归哲学，但取消专用 **coordinate vocabulary**，直接将框写为归一化自然语言数字 `[x_min, y_min, x_max, y_max]`。位置成为句中普通短语，无需额外 **tokenizer** 或 **position encoders**；对 **referential dialogue** 极灵活。**Ablation** 表明该数值表示在 **REC benchmarks** 上稳定优于「扩展词表」方案——将 **grounding** 压入 **LLM** 原生文本空间不仅更简单，往往更有效。代价是 **token efficiency**：单框展开为长数字串，**dense grounding** 或多物体输出笨重。

**NExT-Chat** 揭示 **text-as-coordinate** 范式瓶颈：**coordinates** 并非真正的 **language**，纯 **token classification** 难以支持 **masks** 等更丰富格式。其答案是 **pix2emb**：引入 **`<trigger>` token**，由其 **hidden state** 经轻量 **heads** 解码为 **bounding box** 或 **segmentation mask**；配对的 **location encoder** 将给定框映射回单一嵌入以作区域输入，**cycle loss** 保持编解码一致（encoder–decoder consistency）。位置仍嵌入自回归对话循环，但不再仅是字面文本；可用 **L1**、**GIoU** 等标准回归损失，同时保留统一对话接口。权衡是优化更微妙：平衡 **language loss** 与 **localization loss** 难于纯 **pix2seq** 表述，**REC** 在标准 **RefCOCO** 划分上略低于 **Shikra**。

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

**Osprey** 进一步认为框作为区域输入常过粗：框必然包含背景杂波，削弱训练与推理中的 region–text **grounding**。故以 **mask-level referring** 替代框级输入，用 **mask-aware visual extractor** 在多级特征上从精确 **mask** 池化特征；训练数据 **Osprey-724K** 含物体级描述、对话、部件属性、平衡正/负鲁棒样本与短答指令。输入粒度改变带来部件级分类、细区域描述与 **region captioning** 的显著提升：例如 RefCOCOg **region captioning** 上 **108.3** **CIDEr**，在 Ferret-Bench **referring description** 与 **reasoning** 上亦优于所对比的 MLLM。局限是依赖可用 **mask**（标注或上游 **SAM** 等）。

共同模式：**region-level grounding** 随区域不仅表示「在哪」，还表示「含何视觉内容」而改善。纯坐标对粗 **REC** 尚可，但对 **region captioning**、区域比较、部件推理与 **grounded conversation** 越来越脆。**Ferret** 与 **Osprey** 在不放弃 MLLM **instruction-following** 优势的前提下，将局部视觉特征重新引入交互循环。

### 3.3 Segmentation-Level Grounding {#subsec:grounding-segmentation}

**Bounding boxes** 仍是有损接口：近似物体范围，难以描述非矩形部件，也不便用于提及多属性、**stuff regions** 或物体部件的对话输出。第三类方法将 **grounding** 从区域级框预测升级为 **pixel-level grounding**，输出与语言绑定的 **segmentation mask**。

**LISA** 给出简洁表述：词表增加 **`<SEG>` token**，将其最后一层 **hidden state** 解释为 **SAM-style mask decoder** 的 **prompt embedding**（**embedding-as-mask**）。**Segmentation** 可端到端纳入标准多模态 **LLM**，无需外部流水线；也避免将 **mask** 序列化为长多边形串。**Reasoning segmentation** 同时需要语义推理与 **mask** 输出；训练以语义分割、**referring segmentation**、**VQA** 为主，已展现强零样本 **reasoning segmentation**；仅在 **239 ReasonSeg samples** 上微调亦有大幅提升——说明一旦能将语言 **hidden state** 映射为 **mask prompts**，剩余缺口常在高层推理而非低层 **mask generation**。

**GLaMM** 将单物体分割推广为 **Grounded Conversation Generation（GCG）**：回复可交错普通文本与多短语链接的 **segmentation masks**。输出格式 **`<p> phrase </p><SEG>`** 将短语边界与 **mask** 直接绑定，支持 **grounded dense captions** 与 **grounded multi-turn**。**GranD**（**11M images**、**810M regions**、**7.5M unique concepts**）及 **GranD_f** 构成大规模数据引擎，使 **segmentation grounding** 成为 **dense multimodal pre-training** 问题而非狭窄 **referring segmentation**。

**NExT-Chat** 介于框级与 **mask** 级：**`<trigger>`** 嵌入可送 **box decoder** 或 **SAM-based mask decoder**，同一对话骨干支持两类输出；三阶段训练中第三阶段冻结大部分 **LMM** 仅训 **SAM** 侧投影与解码。与 **LISA/GLaMM** 相比路径更模块化，但共同点一致：一旦将位置视为 **embedding** 而非字面 **token string**，**mask prediction** 成为自然延伸。

**Pixel-level grounding** 改变输出的**语义**：框只说物体大致在哪；**mask** 可在更接近自然语言的粒度上 **ground** 属性、**stuff**、部件与关系短语——对 **embodied systems** 与视觉助手许多指令本质上是 **mask-like**（如「人行道旁的草」「红屋顶」「可按压的部件」），未必能归为单一干净矩形。

### 3.4 Training Strategies: Data Construction, Curriculum, and Multi-Task Transfer {#subsec:grounding-training}

代表性模型间的性能差异同样来自 **data design** 与 **training curriculum**。**Grounding** 难以仅从通用 **image-caption alignment** 可靠涌现；必须通过显式将语言与 **spatial supervision** 耦合的数据来教授。

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

**结论要点：** (1) **grounding 方法** 离纯 **token generation** 越远，表达力通常越强——更丰富区域交互与 **mask** 输出往往需 **hidden-state decoding**、混合区域特征或显式 **decoder**。(2) **Region input** 与 **region output** 同等重要：输出框有用；**Ferret/Osprey** 表明更难的是**精确理解**所指区域，**mask-aware** 或混合区域表征持续改善 **region captioning** 与 **grounded reasoning**。(3) **Segmentation-level grounding** 不仅是更密的 **REC**——**LISA/GLaMM** 表明 **mask** 进入输出空间后，**grounding** 从物体定位扩展到短语级视觉解释。(4) **Accuracy** 与对话灵活性仍有权衡：**Grounding DINO** 在 **REC** 类 **benchmark** 微调后仍常强于多数 MLLM 式方法，因 **detector head** 对精确定位仍是更好工具；MLLM 以 **referential dialogue**、**grounded captioning** 等弥补部分差距，但权衡未消失。(5) **Data engineering** 决定性：**GrIT**、**GRIT**、**GranD**、**Osprey-724K**、**Shikra-RD** 等是实现 **instruction-following**、**open-vocabulary** 与鲁棒 **grounding** 的机制，方法论分歧不仅在架构，也在**可规模化合成的结构化 spatial supervision** 有多少。

### 3.6 Summary {#subsec:grounding-summary}

MLLM 的 **grounding** 方法可读作 **spatial output vocabulary** 的稳步扩张：从 **tokenized coordinates** → **content-aware regions** → **pixel-aligned masks**。Kosmos-2 与 Shikra 确立 **grounding** 可表述为 **language generation**；Ferret/Ferret-v2 表明区域特征与分辨率缩放对 **grounded interaction** 必不可少；LISA、GLaMM、NExT-Chat 表明 **hidden-state-triggered mask decoding** 使与 **segmentation** 兼容的 **grounding** 可行；Osprey 强调 **mask-level** 区域输入对细粒度语义理解的重要性。更强 **grounding** 来自表征、输出格式、数据构建与训练课程的**联合**改进。同时也划清 **grounding** 的边界：定位区域尚不等于理解区域在空间中的关系，或在长文本 **generation** 中保持视觉忠实——这两方面驱动第 4、5 节。

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

**Grounding 是空间推理的必要条件。** **SpatialRGPT** 等区域感知方法表明：当模型显式锚定到相关物体或区域时，**spatial QA** 更可靠。**Spatial-MM** 得到类似结论：**bounding boxes** 与 **scene-graph** 式结构有帮助，因为许多错误发生在「正式推理」之前——在识别**哪些实体应进入比较**的阶段就已出错。

**Grounding 不是空间推理的充分条件。** **CV-Bench**、**SpatialVLM**、**MM-Spatial** 均表明：仅靠准确的 **2D localization** 无法解决 **depth**、**distance** 或 **occlusion**；一旦任务需要度量或 **3D** 判断，模型需要的不仅是 **region alignment**，而是**几何结构**。

最有生产力的解释是：**grounding** 与 **spatial reasoning** 构成**依赖链**而非单一合并技能。**grounding** 提供相关实体与区域；**空间推理**在其上进行关系与几何推断。这也澄清了向下一节的过渡：即使模型能定位区域并回答部分空间问题，在 **open-ended generation** 中仍可能失去 **visual anchoring**，产生流利但**弱支持**的主张。

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

**1. Unsupported object claims（不支持的物体断言）。** 即 **POPE** 研究的典型 **object hallucination**：模型断言图像中**不存在**的物体。用 grounding 的话说，即语言被绑定到**不存在的 referent**。**LRV-Instruction** 表明：当 **training data** 以**正样本指令**为主时，当前 MLLM 特别容易陷入此类失败——模型被鼓励像「被查询实体总存在」那样作答。

**2. Misgrounded attributes and relations（错置的属性与关系）。** 模型可能找对物体，却在颜色、计数、位置、动作或关系上出错。**Hallu-PI** 显式将 **hallucination** 扩展到 **perturbation** 下的属性与关系错误。**LRV-Instruction** 也表明：**hallucination** 不仅是「不存在的物体」；操纵**已存在物体**的属性或高层知识，有时比简单拒答**更难**。

**3. Prior-dominated answers（先验主导的回答）。** **HallusionBench** 区分 **visual illusion** 与 **language hallucination**：后者指模型从**参数记忆**或**语言先验**而非实际图像作答；在编辑图像或**知识密集型**问题上尤其明显——模型重复「通常成立」之事，而非「视觉上成立」之事。从 **grounding** 视角，模型不仅是「看错」，而是**不再把图像当作决定性证据**。

**4. Visually induced misinterpretation（视觉诱导的误读）。** **HallusionBench** 的第二类 **visual illusion** 指相反失败：模型**确实尝试**使用图像，却从中提取错误信息。对 grounding 综述而言这很关键：**并非所有 hallucination 都来自语言先验**；部分源于弱感知判别、差的几何阅读，或无法正确解析编辑图、图表式输入或强错觉刺激。

**5. Robustness under degraded evidence（退化证据下的鲁棒性失败）。** **Hallu-PI** 表明：在裁剪、拼接、模糊或**误导性 prompt** 下，**hallucination** 率上升。未必是全新错误类型，但揭示**条件性**：即便在干净数据上看似 **grounded**，一旦 **visual evidence** 变得部分、嘈杂或结构上具有干扰性，**grounding** 仍可能崩溃。

该 **taxonomy** 是跨论文综合，而非某一 **benchmark** 的封闭标签集；其用处在于将 **hallucination** 文献与更广泛的 **grounding pipeline** 衔接起来。核心问题不仅是回答是否错误，而是**语言与视觉证据之间的绑定**以何种方式、在何处断裂。

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

**OPERA** 在 **token** 层面解释这种漂移：在 **self-attention** 中反复出现 **knowledge aggregation** 或 **partial over-trust**——后续 **tokens** 过度依赖邻近摘要式 **tokens**，对序列前端的原始 **visual tokens** 依赖减弱。由于当前 MLLM 常把 **image tokens** 放在上下文**前部**，长 **generation** 会随时间**削弱**视觉证据。用 grounding 的话说：回复**起始于** **visually anchored**，随后**越来越多地**由**已生成文本**中介。

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

近期第 5 节文献**大幅拓宽**了 MLLM 中 **「hallucination」** 的含义。**POPE** 稳定探测**不支持的物体断言**；**Hallu-PI** 表明这些失败在扰动下**恶化**；**LURE** 将 **hallucination** 与 **co-occurrence bias**、不确定性与**位置**联系起来；**HallusionBench** 分离 **language hallucination** 与 **visual illusion**；**LRV-Instruction** 表明**平衡负监督**重要；**OPERA** 与 **VCD** 表明 **inference-time decoding** 可**部分**对抗先验驱动 **generation**；**RLHF-V** 与 **ViGoR** 将可信性框定为**细粒度 grounding / 偏好对齐**问题；**Woodpecker** 展示**外部验证**闭环的潜力。

对本综述而言，主结论是：**hallucination** 应读作 **grounding** 的 **failure regime**。模型可能因从未学会拒绝无支持断言**而**失去 **grounding**；可能因 **visual uncertainty** **放大**先验；可能因长 **decoding** **偏离**早期 **image tokens**；也可能因 **grounding** 监督信号过粗**无法**教可靠 **abstention**。这也澄清未来工作的开放问题：强 **MLLM** 不仅要**能生成** **grounded outputs**，还要在 **generation** 全程**对 grounding 的限度保持校准**。

---

## 6. Discussion and Future Directions {#sec:discussion}

前几节沿 **capability chain** 展开，而非孤立任务列表：**visual representations** 决定保留何种 **spatial structure**；**grounding 方法** 决定该结构如何转化为 **language** 与 **image regions** 之间的可用对应；**spatial reasoning** 建立在该 **grounding** 之上；**hallucination** 则在链条变弱时暴露 **failure regime**。本节综合跨阶段**共享瓶颈**，并给出对领域现状的**总体判断**。

### 6.1 Shared Bottlenecks Across the Pipeline {#subsec:discussion-bottlenecks}

尽管所综述方法多样，**pipeline** 几乎每一阶段都反复出现三类瓶颈。

**小物体与细粒度细节。** **Resolution** 仍是**结构性**约束。第 2 节表明低分辨率输入会在 **grounding** 开始之前就**抹掉**小物体；第 3 节表明 **coordinate-based grounding** 继承这些早期表征决策带来的**量化**与 **token budget** 权衡；第 4 节进一步表明，涉及**小、远或部分可见**物体的 **spatial judgments** 往往触发**最陡**的性能跌落。含义一致：当前 MLLM 仍偏**场景级**理解，一旦 **grounding** 或 **reasoning** 需要**子区域**精度，**仍脆弱**。

**密集与杂乱场景。** 多数 **benchmarks** 与训练集仍偏向**相对干净**、**物体数量少**的场景。在杂乱环境中，**多种弱点会同时作用**：**encoder** 模糊相邻物体、**box-level grounding** 难以处理**重叠**与**小范围**，**spatial reasoning** 面临**潜在物体关系**的组合爆炸。这也是**强 benchmark 表现**不自动转化为**真实世界 spatial 行为**的原因之一。

**跨图像与时间推理。** 所综述方法**绝大多数**针对**单张图像**；而许多实际 **grounding** 问题需要跨帧跟踪 **spatial state**、跨时间比较视角，或将多视角整合为单一连贯场景模型。**MM-Spatial** 中的 **multi-view geometry** **部分**回应这一点，但**时间上的 spatial reasoning** 仍**欠发展**。当前 MLLM 仍更多为**静态感知**优化，而非**动态 spatial understanding**。

### 6.2 The Grounding–Reasoning Interaction {#subsec:discussion-grounding-reasoning}

本综述最清晰的结论之一是：**grounding** 与 **spatial reasoning** **既非同一**也**非独立**。

**Grounding 是推理的必要条件。** **SpatialRGPT** 等区域感知方法表明：当模型显式锚定到相关物体或区域时，**spatial reasoning** **显著**改善。更一般地，许多 **spatial reasoning** 失败**部分**是**识别失败**：若模型尚未定位**哪两个物体**应进入关系比较，就无法对二者关系做正确推断。

**但 grounding 不是 reasoning 的充分条件。** 精确定位**不保证**对 **depth**、**distance**、**occlusion** 或多步 **spatial composition** 的成功判断。**SpatialVLM** 与 **MM-Spatial** 均表明：一旦任务超越 **2D region alignment**，常需显式 **3D** 或 **depth-aware** 监督。在此意义上，**grounding** 提供推理所依赖的**实体**，但**不提供**完整**几何**。

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

第三，**未来进展不太可能来自任何单一干预层。** 更好的 **encoder**、更丰富的 **grounding** 输出、更强的 **spatial** 监督、改进的 **decoding** 与更细粒度的偏好/人类反馈对齐（如 RLHF）**都重要**，但其效果**只有**在**整条 capability chain** 上被**联合**考虑时才**compound**。

领域因此处于重要**转折点**：**visual grounding** 与 **spatial understanding** 在 **MLLM** 中**已非缺席**，但也**远未解决**。下一步进展取决于将 **grounded perception**、**spatial reasoning** 与 **calibration** 视为**同一多模态系统**中**紧密耦合**的性质，而非彼此独立的插件。

---

## 附录：源文件与引用

- **LaTeX 主文件**：`capabilities/grounding/manuscript/archive/grounding_review.tex`（含 **Abstract** 与 **Keywords**；目录已加入 `.gitignore`，仅本地保留）
- **正文**：`.../archive/grounding_review_body.tex`（**§1–§6** 与小节 `\label{...}` 与本 Markdown 标题对应）
- **参考文献**：`.../archive/grounding_review_refs.bib`（`\citep{...}` 键与 TeX 正文一致）

**覆盖说明**：本文件已包含 **Abstract**（中英）、**Keywords**、**第 1–6 节**及全部 **subsubsection** 主题；**longtable** 均已转为 Markdown 表格；第 4 节 **SpatialVLM / SpatialRGPT / MM-Spatial** 与第 5 节 **taxonomy / propagation / mitigation** 等与 `grounding_review_body.tex` **逐段对应补全**。编译 PDF 时仍以 `\bibliography{grounding_review_refs}` 为准。

如需 **arXiv** 链接对照，可参见同目录 **`citation_arxiv_links.md`**（与本中文版一并提交仓库）。

原按节草稿 **`section1_draft.md`–`section6_draft.md`** 位于 **`manuscript/archive/`**（见该目录下 `README.md`），与 LaTeX 源同为本地归档，**不推送 GitHub**。
