# CS6487 Literature Review — Paper List

**选题：** Visual Grounding and Spatial Understanding in MLLMs: Methods, Representations, and Failure Modes

**总计：** 38 篇 | 精读 17 篇 | 略读 21 篇

---

## Section 2: 视觉表征 — Grounding 的底层基础（8 篇）


| #   | 论文                                                                                                         | 作者                                                | 团队/机构                                  | 发表                     | 精读  | 状态  |
| --- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | -------------------------------------- | ---------------------- | --- | --- |
| 2-1 | **Improved Baselines with Visual Instruction Tuning (LLaVA-1.5)**                                          | Haotian Liu, Chunyuan Li, Yuheng Li, Yong Jae Lee | UW-Madison + Microsoft Research        | NeurIPS 2023           | ★   | ☐   |
| 2-2 | **InternVL: Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks**         | Zhe Chen et al.                                   | Shanghai AI Lab + Tsinghua + Nanjing U | CVPR 2024 Oral         |     | ☐   |
| 2-3 | **Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond**   | Jinze Bai et al.                                  | Alibaba Cloud (通义千问)                   | arXiv 2023, 3000+ cit. |     | ☐   |
| 2-4 | **CogVLM: Visual Expert for Pretrained Language Models**                                                   | Weihan Wang et al.                                | Tsinghua (KEG Lab) + Zhipu AI          | NeurIPS 2024           |     | ☐   |
| 2-5 | **LLaVA-NeXT / LLaVA-OneVision**                                                                           | Haotian Liu et al. / Bo Li et al.                 | UW-Madison + ByteDance + NTU           | arXiv 2024             |     | ☐   |
| 2-6 | **Cambrian-1: A Fully Open, Vision-Centric Exploration of Multimodal LLMs**                                | Shengbang Tong et al.                             | NYU + Meta                             | NeurIPS 2024 Oral      | ★   | ☐   |
| 2-7 | **BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models** | Junnan Li et al.                                  | Salesforce Research                    | ICML 2023              | ★   | ☐   |
| 2-8 | **Mini-Gemini: Mining the Potential of Multi-modality Models**                                             | Yanwei Li et al.                                  | CUHK + SmartMore                       | ICML 2024              |     | ☐   |


### Section 2 技术对比维度


| 论文          | 视觉编码器                             | Connector                   | 分辨率策略                     | 支持 Grounding  |
| ----------- | --------------------------------- | --------------------------- | ------------------------- | ------------- |
| LLaVA-1.5   | CLIP ViT-L/14@336                 | 2-layer MLP                 | Fixed 336px               | ✗             |
| InternVL    | InternViT-6B                      | PixelShuffle + MLP          | Dynamic tile (448×N)      | ✓ (v2.0)      |
| Qwen-VL     | ViT-bigG (OpenCLIP)               | Cross-attn resampler        | Fixed 448 / Naive dynamic | ✓ (bbox)      |
| CogVLM      | EVA2-CLIP-E                       | Visual expert (deep fusion) | Fixed 490px               | ✓             |
| LLaVA-NeXT  | CLIP ViT-L/14                     | MLP                         | AnyRes multi-crop         | ✗             |
| Cambrian-1  | Multi (SigLIP, DINOv2, ConvNeXt…) | SVA / linear / perceiver    | Multi-scale               | ✓ (evaluated) |
| BLIP-2      | EVA-CLIP ViT-G                    | Q-Former                    | Fixed 224px               | ✗             |
| Mini-Gemini | Dual: CLIP + ConvNeXt             | Token-mining cross-attn     | Low-res + High-res        | Partial       |


### 通用综述参考


| 论文                                               | 作者                 | 团队                       | 发表                            |
| ------------------------------------------------ | ------------------ | ------------------------ | ----------------------------- |
| **A Survey on Multimodal Large Language Models** | Shukang Yin et al. | USTC + Tencent YouTu Lab | arXiv 2023 (持续更新), 1000+ cit. |


---

## Section 3: Grounding 方法 — 从坐标到区域（10 篇）


| #    | 论文                                                                                         | 作者                     | 团队/机构                                | 发表                    | 精读  | 状态  |
| ---- | ------------------------------------------------------------------------------------------ | ---------------------- | ------------------------------------ | --------------------- | --- | --- |
| 3-1  | **Kosmos-2: Grounding Multimodal Large Language Models to the World**                      | Zhiliang Peng et al.   | Microsoft Research                   | ICLR 2024             | ★   | ☐   |
| 3-2  | **Shikra: Unleashing Multimodal LLM's Referential Dialogue Magic**                         | Keqin Chen et al.      | SenseTime + Beihang + SJTU           | arXiv 2023, 500+ cit. |     | ☐   |
| 3-3  | **Ferret: Refer and Ground Anything Anywhere at Any Granularity**                          | Haoxuan You et al.     | Apple + Columbia University          | ICLR 2024 Spotlight   | ★   | ☐   |
| 3-4  | **Ferret-v2: An Improved Baseline for Referring and Grounding with Large Language Models** | Haoxuan You et al.     | Apple + Columbia University          | arXiv 2024            |     | ☐   |
| 3-5  | **GLaMM: Pixel Grounding Large Multimodal Model**                                          | Hanoona Rasheed et al. | MBZUAI + ANU + CMU + Google          | CVPR 2024             |     | ☐   |
| 3-6  | **LISA: Reasoning Segmentation via Large Language Model**                                  | Xin Lai et al.         | CUHK + Sun Yat-sen + SmartMore       | CVPR 2024 Oral        | ★   | ☐   |
| 3-7  | **Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection** | Shilong Liu et al.     | IDEA Research + Tsinghua + Microsoft | ECCV 2024             |     | ☐   |
| 3-8  | **NExT-Chat: An LMM for Chat, Detection and Segmentation**                                 | Ao Zhang et al.        | NUS + Tsinghua                       | ICML 2024             |     | ☐   |
| 3-9  | **Osprey: Pixel Understanding with Visual Instruction Tuning**                             | Yuqian Yuan et al.     | Zhejiang U + Ant Group + Microsoft   | CVPR 2024             |     | ☐   |
| 3-10 | **Towards Visual Grounding: A Survey**                                                     | Linhui Xiao et al.     | CASIA + 鹏城实验室                        | IEEE TPAMI 2025       | ★   | ☐   |


### Section 3 按子章节覆盖


| Skeleton 子章节                                                  | 对应论文                                                                                         |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 坐标预测范式 (text-as-coordinate / bbox token / point)              | Kosmos-2 (location tokens), Shikra (text-as-number), NExT-Chat (pix2emb)                     |
| 区域级理解 (region captioning / referring / grounded conversation) | Ferret (任意粒度 region), Shikra (referential dialogue), Ferret-v2                               |
| Segmentation 级 grounding (像素级输出)                              | LISA (embedding-as-mask + SAM), GLaMM (pixel grounding + GCG), Osprey (mask-aware extractor) |
| 训练策略 (数据构造 / 多任务 / instruction tuning)                        | GLaMM (GranD 7.5M), Ferret (GRIT 1.1M), Kosmos-2 (GrIT), Osprey (724K)                       |
| 代表模型横向对比                                                      | 全部 9 个模型 + Grounding DINO 作为检测骨干                                                             |
| 综述参考                                                          | Towards Visual Grounding (TPAMI 2025)                                                        |


### Section 3 模型横向对比表


| 模型             | 坐标表示方式                        | 输入粒度                   | 输出粒度                | 训练数据规模               |
| -------------- | ----------------------------- | ---------------------- | ------------------- | -------------------- |
| Kosmos-2       | Special location tokens       | Image + text           | Bbox (text)         | GrIT (91M)           |
| Shikra         | Plain-text numbers            | Image + text + bbox    | Bbox (text)         | Instruction data     |
| Ferret         | Hybrid spatial sampler        | Point / box / scribble | Bbox (text)         | GRIT (1.1M)          |
| GLaMM          | Text + mask decoder           | Image + text + region  | Bbox + seg mask     | GranD (7.5M)         |
| LISA           | `<SEG>` token → SAM           | Image + text           | Seg mask            | 239 reasoning seg.   |
| NExT-Chat      | Pix2emb (location embeddings) | Image + text + region  | Bbox + seg mask     | Multi-task           |
| Osprey         | Mask-aware visual extractor   | Image + pixel mask     | Text (region desc.) | 724K mask-text       |
| Grounding DINO | Detection head                | Image + text prompt    | Bbox                | O365 + GoldG + Cap4M |


---

## Section 4: 空间关系推理（10 篇）


| #   | 论文                                                                                                  | 作者                    | 团队/机构                      | 发表                | 精读  | 状态  |
| --- | --------------------------------------------------------------------------------------------------- | --------------------- | -------------------------- | ----------------- | --- | --- |
| 4-1 | **Visual Spatial Reasoning (VSR)**                                                                  | Fangyu Liu et al.     | Cambridge + Google         | TACL 2023         |     | ☐   |
| 4-2 | **What's "Up" with Vision-Language Models? Investigating Their Struggle with Spatial Reasoning**    | Amita Kamath et al.   | UCLA + Allen AI (AI2)      | EMNLP 2023        |     | ☐   |
| 4-3 | **SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning Capabilities**                 | Boyuan Chen et al.    | Google DeepMind + Stanford | CVPR 2024         | ★   | ☐   |
| 4-4 | **SpatialRGPT: Grounded Spatial Reasoning in Vision Language Models**                               | An-Chieh Cheng et al. | NVIDIA + UC San Diego      | NeurIPS 2024      | ★   | ☐   |
| 4-5 | **Cambrian-1 / CV-Bench**                                                                           | Shengbang Tong et al. | NYU + Meta                 | NeurIPS 2024 Oral | ★   | ☐   |
| 4-6 | **Eyes Wide Shut? Exploring the Visual Shortcomings of Multimodal LLMs**                            | Shengbang Tong et al. | NYU + Meta                 | CVPR 2024         | ★   | ☐   |
| 4-7 | **SpatialBench: Benchmarking MLLMs for Spatial Cognition**                                          | —                     | 多校联合                       | arXiv 2025        |     | ☐   |
| 4-8 | **An Empirical Analysis on Spatial Reasoning Capabilities of Large Multimodal Models (Spatial-MM)** | Fatemeh Shiri et al.  | Monash U + U of Queensland | EMNLP 2024        |     | ☐   |
| 4-9 | **MM-Spatial: Exploring 3D Spatial Understanding in Multimodal LLMs**                               | Erik Daxberger et al. | Apple ML Research          | ICCV 2025         |     | ☐   |


### Section 4 空间关系类型覆盖矩阵


| 论文                    | 拓扑  | 方向  | 距离/深度 | 遮挡  | 与 Grounding 关联 | 类型             |
| --------------------- | --- | --- | ----- | --- | -------------- | -------------- |
| VSR                   | ✓   | ✓   |       |     |                | Benchmark      |
| What'sUp              |     | ✓   |       |     |                | Benchmark      |
| SpatialVLM            |     |     | ✓     |     | ✓              | Method         |
| SpatialRGPT           | ✓   | ✓   | ✓     |     | ✓              | Method + Bench |
| CV-Bench (Cambrian-1) | ✓   |     | ✓     |     | ✓              | Benchmark      |
| Eyes Wide Shut        | ✓   | ✓   |       |     |                | Analysis       |
| SpatialBench          | ✓   | ✓   | ✓     | ✓   |                | Benchmark      |
| Spatial-MM            | ✓   | ✓   |       |     | ✓              | Benchmark      |
| MM-Spatial            |     |     | ✓     | ✓   | ✓              | Method + Bench |


---

## Section 5: 失败模式与 Grounding 幻觉（10 篇）


| #    | 论文                                                                                                                                  | 作者                    | 团队/机构                          | 发表               | 精读  | 状态      |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------------------ | ---------------- | --- | ------- |
| 5-1  | **Evaluating Object Hallucination in Large Vision-Language Models (POPE)**                                                          | Yifan Li et al.       | RUC + PKU                      | EMNLP 2023       |     | ☑ 笔记待生成 |
| 5-2  | **Hallu-PI: Evaluating Hallucination in MLLMs within Perturbed Inputs**                                                             | Peng Ding et al.      | Nanjing U (NJUNLP)             | ACM MM 2024      |     | ☑ 笔记已完成 |
| 5-3  | **Analyzing and Mitigating Object Hallucination in Large Vision-Language Models (LURE)**                                            | Yiyang Zhou et al.    | UNC Chapel Hill + Stanford     | ICLR 2024        |     | ☑ 笔记已完成 |
| 5-4  | **HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in LVLMs**                  | Tianrui Guan et al.   | UMD (Tianyi Lab) + ByteDance   | CVPR 2024        | ★   | ☐       |
| 5-5  | **Mitigating Hallucination in Large Multi-Modal Models via Robust Instruction Tuning (LRV-Instruction)**                           | Fuxiao Liu et al.     | UMD                            | ICLR 2024        |     | ☐       |
| 5-6  | **OPERA: Alleviating Hallucination in Multi-Modal LLMs via Over-Trust Penalty and Retrospection-Allocation**                       | Qidong Huang et al.   | Shanghai AI Lab + CUHK         | CVPR 2024 **Highlight** | ★   | ☐       |
| 5-7  | **Mitigating Object Hallucinations in LVLMs through Visual Contrastive Decoding (VCD)**                                            | Sicong Leng et al.    | Alibaba DAMO + NTU             | CVPR 2024 **Highlight** |     | ☐       |
| 5-8  | **RLHF-V: Towards Trustworthy MLLMs via Behavior Alignment from Fine-grained Correctional Human Feedback**                        | Tianyu Yu et al.      | Tsinghua (THUNLP) + NUS       | CVPR 2024        | ★   | ☐       |
| 5-9  | **Woodpecker: Hallucination Correction for Multimodal Large Language Models**                                                       | Shaohan Huang et al.  | USTC (VITA-MLLM)               | Sci. China Info. Sci. 2024 | ★   | ☐       |
| 5-10 | **ViGoR: Improving Visual Grounding of Large Vision Language Models with Fine-Grained Reward Modeling**                             | Siming Yan et al.     | Amazon Science + UT Austin     | ECCV 2024        |     | ☐       |


### Section 5 按子章节覆盖


| Skeleton 子章节                              | 对应论文                                                              |
| ----------------------------------------- | ----------------------------------------------------------------- |
| 5a. 失败分类（定位偏移、对象混淆、不存在对象）                 | POPE, HallusionBench, LRV-Instruction                            |
| 5b. 传导机制（看错位置 → 说错内容 → 做错动作）              | OPERA (attention 传导), VCD (统计偏差), HallusionBench (illusion vs hallucination) |
| 5c. 校准与置信度（模型对 grounding 结果的自信度是否可靠）       | RLHF-V (trustworthiness alignment), ViGoR (fine-grained reward)  |
| 5d. 缓解方法（RLHF / grounding-aware / 外部验证）  | LURE (post-hoc), Hallu-PI (defensive prompting), LRV-Instruction (robust IT), VCD (contrastive decoding), RLHF-V (RLHF), Woodpecker (external verification), ViGoR (grounding-aware reward) |


### Section 5 缓解方法对比矩阵


| 论文              | 方法类型            | 需要训练  | 外部工具          | 核心机制                           |
| --------------- | --------------- | ----- | ------------- | ------------------------------ |
| LURE            | Post-hoc 修正     | 轻量    | ✗             | 基于 decoding uncertainty 的输出修订   |
| Hallu-PI        | Defensive prompting | ✗     | ✗             | Perturbed-ICL / Perturbed-Reminder |
| LRV-Instruction | Robust Instruction Tuning | ✓ (FT) | ✗             | 400K 正负样本 instruction 数据        |
| OPERA           | Decoding 策略      | ✗     | ✗             | Over-trust penalty + rollback    |
| VCD             | Decoding 策略      | ✗     | ✗             | 原始 vs 扭曲视觉输入的分布对比              |
| RLHF-V          | RLHF            | ✓ (RL) | ✗             | Segment-level correctional feedback |
| Woodpecker      | 外部验证管线          | ✗     | Grounding DINO + BLIP-2 | 5 阶段：提取→提问→视觉验证→事实校验→纠正 |
| ViGoR           | Reward modeling  | ✓ (RL) | ✗             | Fine-grained visual grounding reward |


---

## 精读优先队列


| 优先级 | 论文                            | Section | 理由                                         |
| --- | ----------------------------- | ------- | ------------------------------------------ |
| 1   | Cambrian-1                    | 2 + 4   | 消融实验最系统，直接定义视觉表征对比框架，兼含 CV-Bench           |
| 2   | Kosmos-2                      | 3       | 定义了 MLLM grounding 的 text-as-coordinate 范式 |
| 3   | Ferret                        | 3       | 任意粒度 grounding 的完整方案，ICLR Spotlight        |
| 4   | LISA                          | 3       | Segmentation-level grounding 代表，CVPR Oral  |
| 5   | TPAMI Visual Grounding Survey | 3       | 最新综述，快速建立 Section 3 全景认知                   |
| 6   | SpatialVLM                    | 4       | 空间推理增强方法，Google DeepMind                   |
| 7   | SpatialRGPT                   | 4       | 连接 grounding 与空间推理的桥梁论文                    |
| 8   | Eyes Wide Shut                | 4       | 视觉短板分析，揭示编码器对空间信息的缺陷                       |
| 9   | LLaVA-1.5                     | 2       | MLLM 标准 baseline，connector 设计的起点           |
| 10  | BLIP-2                        | 2       | Q-Former 原始提出，connector 对比必引               |
| 11  | Grounding DINO                | 3       | 检测骨干基线，理解 grounding pipeline               |
| 12  | What'sUp                      | 4       | 揭示 VLM 基础空间判断的系统性失败                        |
| 13  | VSR                           | 4       | 空间关系理解的标准 benchmark                        |
| 14  | HallusionBench                | 5       | 首个区分 visual illusion vs language hallucination 的诊断框架，CVPR 2024 |
| 15  | OPERA                         | 5       | 揭示 attention 传导→幻觉机制，CVPR 2024 Highlight    |
| 16  | RLHF-V                        | 5       | Fine-grained RLHF 对齐 MLLM 可信度，CVPR 2024     |
| 17  | Woodpecker                    | 5       | 唯一 grounding-based 外部验证管线，5 阶段纠正流程          |


---

## 进度追踪

- [x] Section 2 论文精读（3 篇）
- [x] Section 2 论文略读（5 篇）
- [x] Section 3 论文精读（4 篇）
- [x] Section 3 论文略读（6 篇）
- [x] Section 4 论文精读（4 篇）
- [x] Section 4 论文略读（5 篇）
- [x] Section 2 撰写
- [x] Section 3 撰写
- [x] Section 4 撰写
- [x] Section 1 Introduction 撰写
- [x] Section 6 Discussion 撰写
- [ ] Section 5 论文精读（4 篇新增：HallusionBench, OPERA, RLHF-V, Woodpecker）
- [ ] Section 5 论文略读（3 篇新增：LRV-Instruction, VCD, ViGoR）
- [ ] Section 5 重写（统一风格）
- [ ] 全文整合与横向对比表
- [ ] Presentation slides

