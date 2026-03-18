**题目方向：** *Visual Grounding and Spatial Understanding in Multimodal Large Language Models: Methods, Representations, and Failure Modes*

**1. Introduction**
- MLLM 从"看懂图说话"到"指出具体在哪"的演进趋势
- 为什么 grounding 和空间理解是 MLLM 走向实际任务（agent、embodied AI）的技术前提
- 本文范围：聚焦 MLLM 架构中实现 grounding 与空间理解的技术方法，不做应用综述

**2. 视觉表征：Grounding 的底层基础**
- 视觉编码器选择（ViT 变体、CNN-ViT 混合）
- 高分辨率与多尺度策略（dynamic resolution、tile-based、multi-crop）
- 视觉 token 与 LLM 的对接方式（linear proj / Q-Former / cross-attn / perceiver）
- 关键比较：不同表征策略对细粒度定位能力的影响

**3. Grounding 方法：从坐标到区域**
- 坐标预测范式（text-as-coordinate、normalized bbox token、point prediction）
- 区域级理解（region captioning、referring expression、grounded conversation）
- Segmentation 级 grounding（像素级输出，如何与 LLM 的 text decoder 结合）
- 训练策略比较：grounding 数据的构造、多任务训练、instruction tuning 对 grounding 的影响
- 代表模型横向对比（如 Kosmos-2、Shikra、Ferret、GLaMM、Qwen-VL 等）

**4. 空间关系推理**
- MLLM 的空间推理能力现状：能做什么、不能做什么
- 空间关系类型：拓扑关系、方向关系、距离/深度、遮挡
- Benchmark 与评估（VSR、What'sUp、SpatialBench 等）
- 与 grounding 的关系：空间推理是否依赖于准确的 grounding，还是可以绕过

**5. 失败模式与 Grounding 幻觉**
- Grounding 失败的分类：定位偏移、对象混淆、不存在对象的定位
- Grounding 失败如何传导为下游幻觉（看错位置 → 说错内容 → 做错动作）
- 与校准的关系：模型对自己 grounding 结果的置信度是否可靠
- 现有缓解方法（RLHF、grounding-aware training、外部验证）

**6. Discussion & Future Directions**
- 当前方法的共性瓶颈（小目标、密集场景、跨图推理）
- Grounding 能力对下游任务的意义（这里可以简短提 GUI agent 和 driving 作为例子，但不展开）
- 开放问题：统一的 grounding 评估框架、grounding 与 reasoning 的交互

---