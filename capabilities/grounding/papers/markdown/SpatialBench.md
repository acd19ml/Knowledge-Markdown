# Introduction

In daily life, human can effortlessly integrate spatial information from their surroundings, with a capability known as spatial cognition. This ability extends beyond mere object recognition, serving as a cognitive bridge between perceptual inputs and higher-level functions such as reasoning and navigation. With the rapid advancements of large language models (LLMs) , multimodal large language models (MLLMs) have recently emerged as a major step toward general-purpose visual–linguistic intelligence . By jointly aligning visual and textual modalities within a shared semantic space, MLLMs have moved beyond abstract visual representations, integrating linguistic context to interpret scenes in a more structured manner. Recent advances show that MLLMs have exhibited spatial reasoning abilities , and several benchmarks have been introduced to quantify these capabilities . However, they remain fragmented and task-oriented, often emphasizing performance on specific vision–language tasks rather than assessing spatial cognition as a structured capability. In addition, most benchmarks rely on synthetic or narrowly defined datasets, lacking the visual diversity and real-world complexity necessary to probe genuine spatial cognition. Consequently, these evaluations provide only a partial view of spatial intelligence, making it difficult to analyze cognitive processes and reveal systematic deficiencies in models.


![](../images/SpatialBench_md_images/img/parking.pdf.png)
<figcaption>In a parking lot, the vehicle must understand the relationships of surrounding objects, reason about possible events, and plan the optimal route to reach the exit.</figcaption>


To overcome these limitations, we propose a cognitively grounded evaluation framework for spatial intelligence in MLLMs. Inspired by the cognitive map theory in neuroscience, we conceptualize spatial cognition as a hierarchical process that evolves from low-level perception to high-level reasoning and decision making. Specifically, our framework decomposes spatial understanding into five progressive levels, including **observation (L1)**, **topology and relation (L2)**, **symbolic reasoning (L3)**, **causality (L4)**, and **planning (L5)**, each corresponding to distinct cognitive functions involved in human intelligence. For the example in Fig. , consider a scenario where a car leaves a parking lot. The model recognizes relevant entities and their spatial configurations (L1), then it understands topological relations such as lane connectivity and obstructions (L2) and maps visual symbols to semantic meanings and evaluates potential detour options (L3). After that, it infers causal outcomes of possible maneuvers (L4), and finally, it integrates prior reasoning to generate a coherent plan (L5). This hierarchical design provides a structured lens through which to interpret model behavior, enabling ability-oriented rather than task-oriented evaluation of spatial intelligence.

Building upon this framework, we construct a large-scale spatial video dataset named SpatialBench that grounds spatial cognition evaluation in realistic scenarios. Unlike previous synthetic or narrowly scoped datasets, our collection is captured from diverse indoor and outdoor environments, encompassing both static spatial layouts and dynamic scene evolutions that reflect the multi-level cognitive demands of spatial intelligence. To realize the five-level cognitive hierarchy, we design 15 categories of spatial reasoning tasks, each aligned with a distinct stage of spatial cognition. Each video is paired with carefully designed questions and annotations aligned with these cognitive dimensions, enabling systematic, fine-grained, and cognitively interpretable assessment for MLLMs.

Our experiments show that although current MLLMs perform well on perceptual and relational reasoning tasks, their competence declines sharply in high-level tasks. Insights from the one-shot and human benchmarks suggest that humans rely on selective, goal-oriented reasoning, while MLLMs exhibit diffuse attention to scene details, lacking a unified spatial cognition.

Our contributions are summarized as follows:

- We establish the first comprehensive and cognitively grounded framework for assessing spatial intelligence of MLLMs. Drawing inspiration from cognitive map theory, our framework hierarchically decomposes spatial cognition into five progressive levels, shifting evaluation from task-driven to ability-oriented assessment.

- We construct SpatialBench, a large-scale multimodal dataset specifically designed for evaluating spatial cognition in MLLMs. It features 15 distinct categories of spatial reasoning tasks aligned with five hierarchical cognitive levels, providing a robust foundation for systematic and scalable evaluation.

- We introduce a high-level ability-driven evaluation metric to assess spatial cognition in MLLMs. Through extensive experiments on a wide range of state-of-the-art open-source and commercial models, we uncover their strengths and limitations in spatial reasoning. We further conduct controlled human evaluations to compare human and model reasoning, offering new insights into the gap between artificial and human spatial intelligence.

# Related Works

## Multimodal Large Language Models

Recent progress in Large Language Models (LLMs) has catalyzed the evolution of MLLMs, which integrate visual and linguistic modalities within a unified semantic space. By aligning image representations with textual instructions, MLLMs demonstrate remarkable capability in understanding and generating multimodal content across a wide spectrum of real-world tasks . In general, an MLLM consists of three core components: a modality encoder , a language backbone (LLM), and a modality interface that connects the two. Recently, the capability of MLLMs has expanded beyond static images to encompass video understanding . This advancement has led to the incorporation of video–language alignment during pre-training, allowing MLLMs to jointly model temporal semantics and motion dynamics within a unified multimodal framework .

## Visual-based Spatial Cognition

Visual-based spatial cognition seeks to endow MLLMs with the ability to perceive and reason about three-dimensional spatial relationships directly from visual inputs . Several benchmarks have emerged to evaluate this capability from different perspectives. VSP highlights the bottleneck of perception and reasoning in spatial planning, focusing on static scenes with picture inputs. Video-MME provides a comprehensive assessment across a range of video-related tasks involving recognition and perception. VLM4D emphasizes dynamic motion analysis, and STI-Bench examines physical reasoning by testing models’ ability to predict and estimate object motions and displacements. VSI-Bench introduces a structured benchmark comprising eight question types, each designed to probe different dimensions of spatial understanding in MLLMs. Ego-ST Bench extends this to self-centered navigation in egocentric environments. SpatialLadder presents a comprehensive dataset spanning multiple categories, covering spatial reasoning tasks from single-image understanding to video-based inference. MindCube assesses MLLMs’ ability to infer complete spatial structures from limited visual observations.

While simulation-based benchmarks like VSP offer controlled environments, they often fail to capture the physical nuances of the real world. Other real-life video based benchmarks like VSI-Bench utilize orderly and open-source indoor videos, lacking noise interference in practical application scenarios (such as outdoor robots). SpatialBench distinguishes itself by featuring diverse real-world video sequences across both indoor and outdoor settings, challenging MLLMs with complex lighting, sensor noise, and authentic 3D geometry that are absent in synthetic data. We present the differences between SpatialBench and other benchmarks in Table .

# Spatial Cognition Ability Framework

## Conceptual Foundations of Spatial Cognition

Spatial cognition encompasses the processes that enable intelligent systems to perceive, represent, and reason about spatial relationships within their environment. It involves acquiring spatial knowledge from sensory inputs, forming internal representations of space, and utilizing these representations for high-level tasks . The cognitive map theory provides a foundational opinion of how such representations are organized. Originating from behavioral studies of animals and later supported by discoveries of place cells in the hippocampal system, this theory proposes that intelligent agents construct internal, map-like structures that encode both metric and topological relations. These cognitive maps allow flexible navigation, route planning, and generalization beyond direct sensory experience. More importantly, they reveal that spatial knowledge is not a flat or static representation, but a hierarchically organized system, where low-level perceptual and motor cues are progressively abstracted into higher-order representations that integrate semantic, relational, and causal information. Building on this foundation, modern computational perspectives extend spatial cognition toward causal and multimodal understanding . This hierarchical and integrative view provides the theoretical basis for our framework, which conceptualizes spatial cognition in MLLMs as a progressive process evolving from perception to reasoning and ultimately to planning.


![](../images/SpatialBench_md_images/img/cognition.pdf.png)
<figcaption>The proposed hierarchical spatial cognitive taxonomy.</figcaption>


## Hierarchical Spatial Cognitive Taxonomy

Based on the cognitive map theory, we propose the first systematic and hierarchical framework for spatial cognition evaluation, capturing the progressive development of spatial understanding from perception to high-level reasoning. Unlike prior benchmarks that focus on isolated visual tasks, our taxonomy is ability-driven, where each level represents a distinct, measurable cognitive capacity that reflects a specific stage of spatial intelligence. This hierarchical framework delineates spatial cognition into five progressive levels, each corresponding to a fundamental stage in the transition from sensory perception to deliberative reasoning: **observation (L1)**, **topology and relation(L2)**, **symbolic reasoning (L3)**, **causality (L4)**, and **planning (L5)**. Together, these levels illustrate the progressive process by which intelligent systems transform raw perceptual information into organized spatial reasoning, as shown in Fig. .

**Observation.** The foundational level of spatial cognition is observation, where the model identifies objects and their attributes from visual inputs. This stage corresponds to the extraction of basic perceptual elements such as object category, color, shape, and size.

**Topology and relation.** This level focuses on spatial relations among entities, such as adjacency, containment, orientation, and connectivity. Rather than perceiving isolated objects, it concerns the relational structure of the environment, describing how different elements are spatially arranged and interact within a coherent scene configuration.

**Symbolic reasoning.** Spatial understanding is extended beyond geometry into semantic interpretation. The agent is expected to associate visual symbols or spatial cues (e.g., arrows, pathways) with their abstract meanings and apply rule-based reasoning to infer spatial intent or constraints.

**Causality.** This level reflects the ability to infer spatiotemporal dependencies and predict outcomes of actions. It involves reasoning about how object movements, physical interactions, or agent behaviors lead to specific consequences, integrating physical intuition and causal understanding into reasoning.

**Planning.** It represents the highest stage of spatial cognition, where perception, relational understanding, and causal reasoning are integrated to enable deliberate, goal-oriented decision making. At this level, an agent should synthesize its spatial representations and predictive reasoning to formulate coherent action sequences or navigation strategies that adapt to dynamic environmental contexts.

Collectively, these five levels delineate a progressive and interdependent hierarchy, where foundational sensory capabilities serve as the indispensable bedrock for higher-order reasoning and planning. This structural dependency marks a significant departure from existing benchmarks, which predominantly evaluate model efficacy through the narrow lens of isolated, fragmented tasks. Rather than yielding disjointed performance metrics, our taxonomy enables researchers to pinpoint the precise developmental stage of a model’s spatial cognition and diagnose its cognitive bottlenecks. By organizing spatial understanding into this ability-driven, cumulative continuum, we provide the first systematic and cognitively grounded paradigm. It offers a unified foundation not merely for benchmarking, but for interpreting the evolutionary trajectory of spatial intelligence across MLLMs of varying architectures and scales.


![](../images/SpatialBench_md_images/img/framework.pdf.png)
<figcaption>An overview of SpatialBench.</figcaption>


# SpatialBench

## Overview

We introduce SpatialBench, as shown in Fig. , a large-scale benchmark for assessing evaluate the hierarchical spatial cognition of MLLMs using first-person videos. The dataset comprises 15 question types, each carefully mapped to one of the five cognitive levels introduced above:

- Observation (L1): object counting, object size, room size, absolute distance;

- Topology and relation (L2): appearance order, relative distance, relative direction, appearance order on self-defined route, relative counting;

- Symbolic reasoning (L3): multi-hop spatial reasoning, affordance, landmark-constrained pose localization;

- Causality (L4): spatial causal reasoning;

- Planning (L5): visual-based commands, route planning.

The SpatialBench dataset comprises 3193 question–answer pairs sourced from 117 videos captured by us in real life. The collection spans both indoor and outdoor settings and includes static as well as dynamic scenes, covering challenging real-world contexts such as city roads, forest trails, residential areas, and underground environments. Together, these recordings provide diverse temporal and spatial complexity for evaluating MLLMs’ spatial cognition ability in realistic scenarios. The detailed statistics of SpatialBench are shown in Fig. .

## Benchmark Construction

**Data Collection.** In contrast to prior benchmarks that adapt existing open-source datasets, SpatialBench is built from scratch through real-world recordings using our custom-designed sensing platform. The platform integrates a calibrated RGB camera and a 3D LiDAR sensor, which are spatially and temporally synchronized to ensure precise correspondence between visual and geometric modalities. The RGB camera continuously captures high-resolution visual streams, which serves as the basis for video question generation, while the LiDAR sensor synchronously records 3D point clouds that provide precise geometric information for size and distance related measurements. To ensure the accuracy and density of spatial data, we apply a filtering procedure to remove overly sparse or noisy point clouds. Data are collected from diverse environments, covering both indoor and outdoor settings such as offices, residential areas, city streets, and wooded regions, including both dynamic and static scenes. Each recording is conducted from a first-person perspective to preserve the egocentric characteristics essential for spatial understanding. For every video, we record standardized metadata including timestamps, scene categories, LiDAR frames, and synchronization parameters.


![](../images/SpatialBench_md_images/img/SpatialBench_Stats_Final.pdf.png)
<figcaption>The statistics of SpatialBench.</figcaption>


**Question-Answer Generation.** To ensure high-quality and semantically diverse annotations, human annotators work in pairs throughout the QA generation process. Within each pair, one annotator proposes candidate questions while the other independently reviews and validates them, checking for duplicates, ambiguous wording, and alignment with the intended cognitive level. All annotators are trained on the fifteen predefined task types, and they carefully review each video segment and propose candidate questions grounded in observed spatial relationships and scene dynamics. This collaborative review process ensures both the accuracy and relevance of the human-generated questions before they proceed to AI-assisted answer generation. For non-metric question types, we design specialized prompting templates tailored to each question category. These templates are then provided to state-of-the-art commercial models to generate corresponding answers. Along with each generated response, the model is required to output an evidence summary, including key frames and brief reasoning traces. For metric-related questions, we directly compute ground-truth answers using the LiDAR point cloud data. Precise 3D measurements are extracted through geometric fitting and spatial projection, thereby providing physically accurate ground-truth answers for all size and distance related questions. This hybrid design combines the semantic richness of human understanding, the efficiency of large model reasoning, and the geometric accuracy of sensor-derived measurements, resulting in a balanced and cognitively interpretable QA corpus.

**Annotation Verification.** We implement a multi-step verification protocol to ensure the reliability of the generated annotations. For L1 and L2 questions, multiple leading models independently generate answers, and the consistency of these responses is evaluated. Questions with fully consistent model outputs are provisionally approved, but a subset of these automatically approved answers is further subject to human spot-checking to guarantee overall quality. Any discrepancies detected, whether during consistency checks or spot audits, trigger full human review. For question beyond L3, all annotations undergo mandatory human verification due to their higher cognitive complexity. The human review process follows a fixed checklist including: whether the evidence frames display key entities, whether multi-model outputs have been correctly interpreted, and whether answers conform to the predefined question schema. Annotations that are modified or rejected during the first review are subsequently evaluated by an additional annotator. This annotator examines the evidence summaries, the explanations and supporting screenshots submitted by the human reviewers, and also inspects the video and the question directly. Based on this comprehensive review, this annotator determines the final annotation. The verification protocol used ensures that all QA annotations are accurate, consistent, auditable, and reproducible, providing a trustworthy foundation for evaluation.

# Evaluation on SpatialBench

## Setup

**Models.** We evaluate a diverse set of MLLMs to comprehensively assess their spatial cognitive abilities. Our benchmark covers both proprietary and open-source models with support for video understanding. For proprietary models, we include leading systems such as Gemini , GPT , and Claude-Sonnet. For open-source models, we evaluate representative families including Qwen , GLM , MiniMax , and ERNIE , encompassing variants across a broad range of architectures, parameter sizes (7B–235B), and training paradigms, enabling a systematic comparison of how different modeling strategies influence spatial cognition performance in SpatialBench.

**Metrics.** Following , we adopt evaluation metrics tailored to the answer type. Specifically, tasks in SpatialBench are categorized into Multiple-Choice Answer (MCA) and Numerical Answer (NA) formats. For MCA tasks, we employ accuracy (ACC) as the primary evaluation metric , which measures the proportion of exactly matched answers between the model’s predictions and the ground-truth labels. While for NA tasks, where answers involve continuous numerical values, we adopt the mean relative accuracy (MRA) metric , defined as:
``` math
\begin{equation}
    \text{MRA}=\frac{1}{10}\sum_{\theta\in\Omega}\mathbb{I}(\frac{|y'-y|}{y}<1-\theta),
\end{equation}
```
where $`y'`$ and $`y`$ are the model’s prediction and ground truth, respectively, and $`\theta`$ is the confidence threshold from a thresholds set $`\Omega=\{0.5,0.55,...,0.95\}`$.

**Overall Score.** We propose a high-level capability–oriented overall score to integrate performance across the five hierarchical cognitive levels. To emphasize higher-level reasoning while preserving balance, we assign adaptive weights to each level:
``` math
\begin{equation}
    C_i = F_iS_i, \quad F_i = \alpha D_i + 0.1(1-\alpha)E_i,\ i=1,...,5,
\end{equation}
```
where $`S_i`$ is the standard deviation of model scores, $`D_i`$ is the category’s question proportion, and $`\alpha`$ controls the trade-off between baseline and adaptive weights and $`E_i`$ is non-negative variables to be optimized with $`\sum_{i=1}^5 E_i=10`$. Under the monotonicity constraint $`C_{i+1}>C_i`$ the target is to minimize
``` math
\begin{equation}
    \text{Var}(C_{i+1}-C_i) - k\sum_{j=1}^5 C_j^2,
\end{equation}
```
yielding complexity-aware overall scores. $`\alpha \ \text{and}\  k`$ will be fixed manually. Finally, the overall score is computed as $`\sum_{i=1}^{5} C_iM_i`$, where $`M_i`$ is the average rating on each level.

## Benchmarking MLLM Performance

Table and Table presents the model performance on SpatialBench across five hierarchical levels. Gemini-2.5-pro occupy the top of the ranking and show substantially higher overall scores than any other models. This gap is most pronounced on high-level tasks such as symbolic reasoning, causality, and planning. Nevertheless, several open-source series (e.g., Qwen variants) reach competitive performance on lower and mid levels, indicating that open models can achieve strong perceptual and relational understanding with carefully designed training paradigms. For open-source models, a clear correlation appears between model scale and average performance: larger models generally achieve higher overall scores, showing that scale remains an important factor. However, size alone does not guarantee better performance. Within the same model family, different versions (such as instruction-tuned vs. thinking mode) can show clear performance gaps. This suggests that architectural design and the integration strategy for visual and linguistic information plays a crucial role in spatial cognitive ability.


![](../images/SpatialBench_md_images/img/Radar.pdf.png)
<figcaption>Comparison of models across spatial cognitive levels.</figcaption>


Fig. illustrates the average performance of several representative models across the five cognitive levels. It can be observed that a cross the board, observation and topology tasks are relatively easier for MLLMs. Most models achieve substantially higher scores on tasks such as object counting, size and distance estimation, and simple topological queries. By contrast, higher-level abilities remain challenging for models, including symbolic reasoning, causality, and visual planning. On these tasks, average performance drops noticeably and variance between models increases. This pattern suggests that while current MLLMs can reliably extract visual evidence and reason about basic relations, they struggle to (a) convert perceptual inputs into robust symbolic rules, (b) infer causal or dynamic consequences accurately, and (c) generate multi-step and convincing plans for a given objective.


![](../images/SpatialBench_md_images/img/example.pdf.png)
<figcaption>The differences of thinking processes between MLLM and human.</figcaption>


## One-Shot Evaluation

In-context learning is a critical capability for MLLMs, reflecting their ability to leverage minimal examples for reasoning. To evaluate this, we perform a one-shot assessment: for each task, a single annotated example comprising a QA pair, reasoning explanation, and key frames is provided. Models are then asked to answer a test question from the same task, enabling examinations on how effectively they can generalize spatial reasoning from limited guidance.

We select several representative models from the one-shot evaluation, including two proprietary models: Gemini-2.5-pro (the best-performing) and GPT-5-chat-latest (the weakest), as well as a strong open-source model Qwen3-VL-235B-A22B-Instruct. Gemini-2.5-pro shows a decline in performance, primarily across the intermediate cognitive levels. In contrast, GPT-5-chat-latest and Qwen3-VL demonstrate substantial improvements. Although these models still trail Gemini in absolute scores, their performance under prompting approaches that of the previously strongest model. This result indicates that even lower-performing models can rapidly enhance specific spatial reasoning abilities when given minimal in-context guidance, highlighting the potential of one-shot prompting to boost MLLMs’ higher-level cognitive capabilities. The results suggest that some powerful models, such as Gemini 2.5 Pro, can reason efficiently and accurately from context on their own, performing better than when given human-guided prompts. This indicates that their built-in contextual understanding is particularly well-suited for spatial intelligence tasks. By contrast, GPT‑5 appears comparatively weaker in intrinsic spatial logic, yet achieves more advanced spatial intelligence by leveraging the GPT series’ steadily improving linguistic capabilities . Similarly, Qwen3-VL, which demonstrates strong text-based reasoning skills , benefits from one-shot prompting in a way comparable to GPT‑5, highlighting the role of linguistic reasoning in enhancing spatial cognition under minimal guidance.

## Benchmarking Human Performance

To quantify the gap between MLLMs and human-level intelligence across cognitive dimensions, we conduct a human benchmark experiment. In this experiment, 33 human participants are presented with SpatialBench, and they provide answers directly without guidance, allowing us to measure their unaided spatial reasoning and planning abilities. The results in Table and Table indicate that human achieve near-perfect performance across nearly all tasks with an overall score of 96.40. Humans perform particularly well on higher-level tasks: symbolic reasoning, causality, and planning, and all achieve essentially 100% accuracy, while even lower-level observation and topology tasks maintain strong performance. Across all levels, humans exhibit not only higher absolute accuracy but also more consistent performance, reflecting robust generalization and contextual understanding that MLLMs have yet to fully achieve. These findings underscore the substantial gap that still exists between human and machine spatial intelligence. While MLLMs show promising abilities in extracting visual information and reasoning about simple topological relations, they remain far from matching human performance in tasks that require integrating high-level reasoning. This test thus provides a clear target for future model development, highlighting the need to enhance multi-step reasoning and context-sensitive planning in MLLMs.

Fig. shows an example of the differences between Gemini and human. The human focuses on the key directional cue: the turning path of the white Volvo, and quickly eliminates irrelevant options based on spatial orientation, demonstrating strong goal-directed and spatially grounded reasoning. In contrast, Gemini describes the entire scene in a more exhaustive but unfocused manner, mentioning many vehicles and areas without identifying the crucial spatial relationship. This suggests that while MLLMs can recognize objects and describe scenes accurately, they often lack selective attention and directional understanding, leading them to infer by association rather than by reasoning about movement and geometry.

## Key Insights from Evaluation

Our evaluation reveals several critical limitations in the spatial cognition of current MLLMs. First, models inherently struggle to reconstruct and maintain continuous spatial scenes from dynamic visual inputs. Poor-performing models frequently misinterpret relative directions or confuse sequential positions, while even advanced models make notable errors in continuous scene tracking and discerning subtle geometric relations. This highlights a fundamental vulnerability in capturing long-range spatial dependencies. Second, our findings empirically validate that spatial cognition in MLLMs is strictly hierarchical and tightly coupled: success in higher-order reasoning is fundamentally bottlenecked by accurate lower-level perception. Performance precipitously declines as cognitive complexity increases, with most models exhibiting cascading failures from the third level onward. To bridge these gaps, future work should leverage high-quality datasets structured with progressive cognitive tasks, incorporate explicit spatial representations, such as scene graphs or 3D geometric priors, and adopt advanced training paradigms, including curriculum learning and agent-based interactive environments, to intrinsically promote multi-step reasoning and long-horizon planning. Furthermore, establishing closed-loop feedback mechanisms, where high-level reasoning and planning errors are utilized to iteratively refine low-level perceptual modules, could significantly mitigate the risk of cascading spatial hallucinations.

# Conclusion

In this work, we introduce SpatialBench, a comprehensive benchmark built upon a five-level hierarchical spatial cognition framework that progressively evaluates MLLMs from low-level observation to high-level planning. This layered design reflects the cognitive progression from perception to decision-making, enabling a more interpretable and fine-grained diagnosis of multimodal spatial intelligence. Experimental results show that while modern MLLMs demonstrate strong perception and relational reasoning, their abilities in symbolic abstraction, causal inference, and spatial planning remain limited. SpatialBench establishes a principled foundation for hierarchical evaluation and future development of spatially grounded intelligence in MLLMs.

# Mathematical Modeling of Overall Score

To provide a unified measure of a model’s spatial cognitive competence, we introduce an overall score that integrates performance across all five hierarchical cognitive levels. The goal of this metric is not merely to average accuracy, but to construct a complexity-aware evaluation that reflects the progressively demanding nature of spatial cognition. Lower levels mainly involve perceptual and geometric understanding, while higher levels require abstract reasoning, causal inference, and planning. A meaningful overall score must therefore (1) preserve the relative importance of each cognitive level, (2) emphasize higher-level reasoning without overwhelming lower-level contributions, and (3) maintain fairness across categories with different question counts and variances.

To achieve these goals, we design a weighting mechanism that adaptively adjusts each level’s contribution based on its intrinsic difficulty and score distribution. Instead of manually assigning fixed weights, we formulate an optimization-driven approach that learns monotonic, complexity-aligned weights while controlling the imbalance between levels. This results in an overall metric that is interpretable, robust to distributional differences across task categories, and sensitive to a model’s true cognitive progression rather than raw accuracy alone.

To formalize the construction of our overall score, we assign adaptive weights to the five cognitive levels ($`i=1,2,3,4,5`$ corresponding to Observation through Planning). Our goal is to encourage higher performance on more complex cognitive abilities while preserving a balanced contribution across levels.

We begin by computing, for each level, the empirical standard deviation
``` math
\begin{equation}
   S_i,\ i=1,2 ... 5,
\end{equation}
```
which reflects the intrinsic difficulty and discriminative range of that category. This quantity is paired with the category’s question proportion (i.e., its initial weight)
``` math
\begin{equation}
   D_i,\ i=1,2 ...5,
\end{equation}
```
serving as the baseline weighting factor. To introduce controlled adaptivity, we adjust these baseline weights through
``` math
\begin{equation}
   F_i=\alpha D_i+0.1(1-\alpha )E_i,
\end{equation}
```
where $`\alpha`$ is a manually chosen hyperparameter governing the balance between the baseline distribution $`D_i`$ and the optimized adjustment $`E_i`$. The resulting effective weight for each category is then
``` math
\begin{equation}
   C_i=F_iS_i,\ i=1,2 ... 5,
\end{equation}
```
which we require to increase monotonically with cognitive complexity.

To obtain a smooth hierarchy of difficulty, we further aim to make the increments between adjacent levels as uniform as possible. This leads to the following constrained nonlinear optimization problem:

``` math
\begin{equation}
   \begin{aligned}
       \min \  & f = \text{Var}\ ( C_{i+1} - C_i ) - k\sum_{j=1}^5 C_j^2, \quad i=1,2,3,4 \\
       \text{(P)} \quad &
       \begin{cases}
           C_{i+1} - C_i > 0,\ i=1,2,3,4\\
           \sum_{j=1}^5 E_j = 10\\
           E_i \ge 0,\ i=1,2 ...5
       \end{cases}
   \end{aligned},
\end{equation}
```
where the parameter $`k`$ expresses the preference for maintaining the original baseline separation prescribed by the standard deviations $`S_i`$. Solving Problem (P) yields a set of complexity-aware weights $`C_i`$, which are subsequently combined with the per-level average model ratings to produce the final overall score.

Mathematically, the original formulation introduces strict inequality constraints
``` math
\begin{equation}
    C_{j+1}-C_{j}>0, \ j=1,2,3,4,
\end{equation}
```
which renders the feasible region
``` math
\begin{equation}
    \{(E_i)\ |\ C_{j+1}-C_{j}>0\}
\end{equation}
```
an open set in Euclidean space. As a result, the constraint set is not compact and is incompatible with the standard form required by many numerical optimization solvers; specifically, it does not contain the closed and bounded simplex
``` math
\begin{equation}
    \{(E_i)\ |\ \sum_{j=1}^5 E_j=10,\ E_i\ge 0\}.
\end{equation}
```
Rather than transforming the problem into a fully standardized form, which would introduce unnecessary complications and yield no practical benefit, we relax the strict inequalities to non-strict ones and solve the following modified program:
``` math
\begin{equation}
   \begin{aligned}
       \min \  & f = \text{Var}\ ( C_{i+1} - C_i ) - k\sum_{j=1}^5 C_j^2, \quad i=1,2,3,4 \\
       (\text{P})' \quad &
       \begin{cases}
           C_{i+1} - C_i \ge 0,\ i=1,2,3,4\\
           \sum_{j=1}^5 E_j = 10\\
           E_i \ge 0,\ i=1,2 ...5
       \end{cases}
   \end{aligned}.
\end{equation}
```
The relaxation makes the feasible set closed and compatible with standard numerical solvers, while preserving the essential structural constraint that higher-level categories should not receive smaller weights than lower ones. After solving $`\text{P})'`$, we simply discard degenerate solutions in which
``` math
\begin{equation}
    C_i=C_{i+1},\ \exists\ i \in \{1,2,3,4\},
\end{equation}
```
since such solutions violate the intended strictly increasing hierarchy of cognitive complexity. This procedure is computationally effective and fully adequate for our application, as the optimization landscape naturally favors non-degenerate solutions when $`k`$ is chosen appropriately.

The new constraint set is now in standard form. Since both
``` math
\begin{equation}
\begin{aligned}
    & \{(E_i)\ |\ C_{j+1}-C_{j}>0, \ j=1,2,3,4\} \ \ \text{and}\\
    & \sum_{j=1}^5 E_j=10,\ E_i\ge 0\}
\end{aligned}
\end{equation}
```
are closed subsets of the Euclidean space, and their intersection (our new feasible region) is also closed.

Recall that $`F_i=\alpha D_i+0.1(1-\alpha )E_i`$ which is continuous in each $`E_i`$, Consequently, $`C_i=F_iS_i`$ is also continuous since $`S_i`$ is constant. Therefore,
``` math
\begin{equation}
    f_{sum}=\sum_{j=1}^5C_j^2
\end{equation}
```
is continuous as well. Let $`\mathbf{E}=(E_1,E_2,...E_5)`$, since each $`C_i`$ is a continuous function of $`\mathbf{E}`$, define
``` math
\begin{equation}
    g_i(\mathbf{E})=C_{i+1}(\mathbf{E})-C_i(\mathbf{E}), i=1,2,3,4,
\end{equation}
```
which is continuous in $`\mathbf{E}`$. Their linear combination
``` math
\begin{equation}
    \bar{g}(\mathbf{E})=\frac{1}{4}\sum_{i=1}^4 g_i(\mathbf{E})
\end{equation}
```
remains continuous. Thus,
``` math
\begin{equation}
    f_{var}=\text{Var}\ (g_i(\mathbf{E}))=\frac{1}{4}\sum_{i=1}^4(g_i(\mathbf{E})-\bar{g}(\mathbf{E}))^2
\end{equation}
```
is also continuous because it is constructed from addition and squaring of continuous functions. Hence,
``` math
\begin{equation}
    f=f_{var}-f_{sum}
\end{equation}
```
is a continuous function of $`\mathbf{E}`$.

By the Extreme Value Theorem, any continuous function on a closed and bounded feasible region must attain its minimum. Therefore, problem $`\text{P})'`$ admits at least one global minimizer under the new constraint formulation.

To numerically solve the nonlinear programming problem, we employ the `scipy.optimize.minimize` function in Python. We evaluate multiple combinations of $`(\alpha,k)`$, and observe that $`(\alpha,k)=(0.4,0.01)`$ yields a particularly favorable optimum. Under this setting, the optimizer returns
``` math
\begin{equation}
    (E_i)=(0,0,1.4911,3.8347,4.6742),
\end{equation}
```
achieving
``` math
\begin{equation}
    \text{Var}\ (C_{i+1}-C_i)=0.0264,
\end{equation}
```
which is substantially lower than the variance obtained when $`\alpha=0`$, where the optimal solution becomes
``` math
\begin{equation}
    (E_i)=\frac{2}{3}(1,2,3,4,5)
\end{equation}
```
with
``` math
\begin{equation}
    \text{Var}\ (C_{i+1}-C_i)=0.0968.
\end{equation}
```
Moreover, the chosen parameter setting effectively resolves the initial undesirable ordering issue observed when $`\alpha=1`$, where the resulting sequence satisfies
``` math
\begin{equation}
    C_4<C_5<C_1<C_3<C_2,
\end{equation}
```
violating the monotonicity condition. In contrast, $`(\alpha,k)=(0.4,0.01)`$ produces a monotone and well-behaved solution consistent with our design constraints.

# Case Study


![](../images/SpatialBench_md_images/img/conclusion.pdf.png)
<figcaption>Case study on causal reasoning in dynamic scenes. This example shows that weaker MLLMs fail to construct a coherent scene, while stronger ones reconstruct the static layout but lose continuity when the camera changes direction.</figcaption>



![](../images/SpatialBench_md_images/img/case.pdf.png)
<figcaption>Failure case illustrating egocentric direction misinterpretation. Although the camera is defined as facing the whiteboard, the model confuses recorder-view and agent-view directions, leading to the incorrect prediction (“Left”).</figcaption>


To further illustrate the challenges of video-based spatial reasoning, we analyze a representative failure case from the causal reasoning category, and the results are shown in Figure . The question asks where a white Volvo S60 would most likely pass if it turns right and continues straight. While the ground truth is option D, the two evaluated MLLMs exhibit markedly different behaviors. MLLM1 demonstrates strong perceptual grounding: it accurately identifies the Volvo, reconstructs the forward scene layout, and reasons about nearby landmarks such as a black Mercedes and empty parking spots. However, its reasoning deteriorates once the camera performs a U-turn, causing the model to implicitly assume that the camera’s motion still reflects the Volvo’s hypothetical trajectory; this misalignment leads it to break the continuity of the reconstructed scene and misinterpret the spatial ordering. In contrast, MLLM2 fails much earlier and provides only a superficial description. It implicitly treats the camera’s viewing direction as the Volvo’s movement direction, confusing left/right relations and ultimately selecting an incorrect parking area. Human annotators, however, easily recognize that options A–C lie in the opposite direction of a right turn, and that the Volvo would naturally drive toward the black Mercedes, making D the only plausible answer. This case reveals a critical limitation: weaker models struggle to form any coherent scene representation, while stronger models can reconstruct static layouts but fail to maintain spatial consistency across continuous camera motion. Even when stable landmarks (e.g., the covered car) exist to support scene continuity, current models do not reliably leverage them. Overall, this example demonstrates that successful causal reasoning in dynamic scenes fundamentally depends on robust 3D scene reconstruction and continuity tracking—capabilities that remain insufficiently developed in existing MLLMs.

# Egocentric Reasoning Breakdown

We further examine two representative failure cases involving egocentric direction reasoning in both indoor and outdoor environments. For the indoor case shown in Figure , the task requires determining the relative direction of an AC control panel from the perspective of a robot standing on top of the projector and facing the whiteboard. While the ground truth is Backward, the model incorrectly predicts Left. A close inspection of the reasoning trace reveals that although the model correctly identifies the projector, the whiteboard, and the AC control panel within the room, it fails at the final spatial transformation: converting absolute room layout into the camera’s egocentric frame. The model implicitly adopts the recorder’s viewing direction as the reference frame, causing a systematic rotation of its inferred directions. As a result, the AC control panel which lies behind the camera when facing the whiteboard is erroneously mapped to its left. This case highlights a broader weakness: even when object localization is accurate, current MLLMs often conflate scene-centric, camera-centric, and agent-centric coordinate systems. Such confusion leads to consistent directional inversion or orthogonal errors, especially in indoor scenes where multiple frames provide shifting viewpoints. Strengthening explicit frame-of-reference reasoning remains essential for achieving reliable spatial understanding.

For the outdoor case in Figure , the model again fails to correctly align the robot’s egocentric perspective with the scene layout observed from the recorder’s view. Although the model successfully identifies the motorcycle and the black Mercedes, it misinterprets the orientation of the robot after moving “onto the road.” Because it interprets the forward direction based on the camera’s viewpoint rather than the robot’s own heading, the model incorrectly assumes that the robot should turn left to move down the road. This perspective confusion leads to a reversed decision in the route-planning step, causing the model to select “turn left” instead of the correct “turn right.” The error highlights the model’s difficulty in maintaining consistent egocentric orientation during multi-step spatial navigation.


![](../images/SpatialBench_md_images/img/caseoutside.pdf.png)
<figcaption>Failure case illustrating route-planning direction misinterpretation. Although the robot’s forward orientation is clearly defined after moving onto the road, the model confuses recorder-view and agent-view directions, leading to the incorrect prediction (“Left”).</figcaption>

