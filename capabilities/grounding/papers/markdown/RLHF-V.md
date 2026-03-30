# Introduction

The recent success of Multimodal Large Language Models (MLLMs) marks a significant milestone in AI research . By connecting visual signals and Large Language Models (LLMs), MLLMs show unprecedented capabilities in multimodal understanding, reasoning, and interaction . The models are typically pre-trained on large-scale image-text data to learn the foundational multimodal knowledge and capabilities  . To steer the model behavior, most MLLMs are further fine-tuned with instruction tuning (also known as supervised fine-tuning), which supervises models to clone the behavior from demonstration data, enabling MLLMs to engage users in various open-world tasks .

However, current MLLM behaviors are not well aligned with human preferences. A glaring issue is their tendency to produce *hallucinations* — responses that are not factually grounded in the associated images . This typically includes descriptions of non-existing visual contents and errors in descriptions. As shown in Figure <a href="#fig:overview" data-reference-type="ref" data-reference="fig:overview">1</a>, current MLLMs can hallucinate about objects, attributes, numbers, positions, actions, etc. Quantitatively, our human evaluation shows that the problem is prevalent among state-of-the-art MLLMs, where even the most advanced GPT-4V  contains obvious hallucinations in 45.9% responses. The problem makes existing MLLMs untrustworthy and thus impractical in real-world (especially high-stakes) applications, such as guiding visually impaired individuals  or autonomous driving systems .

![](../images/RLHF-V_md_images/figs/framework.pdf.png)

The RLHF-V framework for MLLM behavior alignment from human feedback. (1) Given the input image and prompt, we obtain outputs from MLLMs and collect human feedback in the form of fine-grained segment-level <strong>corrections</strong> on <strong>hallucinations</strong>. (2) During human preference learning, we perform dense direct preference optimization over the fine-grained correctional human feedback.

We argue that the problem arises from the lack of positive/negative human feedback in instruction-tuned models, making it challenging to learn the precise behavior boundaries to exclude hallucination. To address the problem, we propose RLHF-V, a novel framework that aligns MLLM behavior by learning from human feedback. A straightforward way is to employ the traditional Reinforcement Learning from Human Feedback (RLHF) method in state-of-the-art LLMs , which involves human annotators ranking model responses, and utilizing a reward model to guide the policy LLM learning. However, this approach is fraught with two key challenges: (1) *Annotation ambiguity*. Helpful and engaging responses about rich image content are typically long and complex, making it usually non-obvious to decide which response is preferable. As shown in Figure <a href="#fig:overview" data-reference-type="ref" data-reference="fig:overview">1</a> (responses A and B), annotators usually face dilemmas when presenting responses with respective advantages and flaws. Besides, even if labeled with a clear preference, the optimal response remains unknown (e.g., the exact time of the clock). (2) *Learning efficiency*. The coarse-grained ranking feedback makes it difficult to accurately allocate credit to the desirable behaviors. Considering the linguistic complexity and variance of responses, the desirable behavior often requires a large amount of labeled data to learn . Moreover, misallocation of credit to the non-robust bias correlated with the data usually leads to reward hacking and behavior degeneration problems .

RLHF-V addresses these challenges by introducing two key innovations: (1) At the data level, we propose to collect human feedback in the form of fine-grained segment-level corrections. As shown in Figure <a href="#fig:overview" data-reference-type="ref" data-reference="fig:overview">1</a>, we ask human annotators to directly correct the hallucinated segments from model responses, providing a clear, dense, and fine-grained human preference, as well as optimal responses. This strategy also avoids linguistic variance and non-robust bias, ensuring that the feedback is accurately allocated to the desirable behaviors, thereby enhancing learning efficiency and preventing reward hacking problems. (2) At the method level, we propose dense direct preference optimization (DDPO), a new variant of DPO  that addresses the traditional RLHF objective in an equivalent simple and efficient supervised fashion. DDPO directly optimizes the policy model against dense and fine-grained segment-level preference, where the hallucinated segments receive stronger feedback to be factually grounded.

Comprehensive experiments on five benchmarks show that, RLHF-V can substantially enhance the trustworthiness of MLLMs with promising data and computation efficiency. Using 1.4k preference data, RLHF-V significantly reduces the object hallucination rate of the base MLLM by 34.8%, surpassing the concurrent LLaVA-RLHF  trained on 10k preference data. We also show that RLHF-V achieves better robustness than the strong GPT-4V  in preventing hallucinations aroused from over-generalization.

The contribution of this work can be summarized as threefold: (1) We present RLHF-V, a novel framework that aligns MLLM behavior through fine-grained correctional human feedback. (2) We collect high-quality human preference data to provide human-aligned learning signals for MLLMs. (3) We conduct comprehensive experiments to demonstrate the effectiveness of the proposed framework, achieving state-of-the-art performance in trustworthiness among open-source MLLMs. All the code, data, and model weights are open-sourced at <https://github.com/RLHF-V/RLHF-V>.

# Human Preference Collection

The goal of human preference data is to distinguish human-preferred high-quality responses from inferior ones, providing human-aligned learning signals to steer the MLLM behaviors. We first provide an analysis of underlying factors of human preference data, based on which we motivate the human preference collection procedure of RLHF-V.

**Human Preference Data: Underlying Factors and Challenges.** Given the input $`x`$ (including the image and the prompt), denote the difference between a preferred output $`y_w`$ and an inferior output $`y_l`$ as $`Y`$. The difference $`Y`$ can be essentially decomposed into three factors:

$$
Y = Y_p + Y_s + Y_n
$$

where $`Y_p`$ is the truly preferred behavior such as being trustworthy and helpful, $`Y_s`$ denotes the shallow non-robust bias correlated with the data but unrelated to human judgment (e.g., $`y_w`$ contains more usage of specific words), and $`Y_n`$ is the random noise factor denoting the linguistic variance of natural language (e.g., different ways of expressing the same meaning). $`Y_p`$ is the factor we want to learn from the difference $`Y`$, while fitting to $`Y_s`$ can lead to reward hacking problems and thus should be avoided. The linguistic variance $`Y_n`$ does not bias the preference learning but makes the learning more difficult, demanding more labeled data to learn to the preferred factor $`Y_p`$, and thus should also be avoided if possible.

The common RLHF practices in LLMs collect human preference $`Y`$ in the form of ranking labels, indicating the overall relative quality of responses . According to the above analysis, the practice faces several key challenges: (1) *Annotation ambiguity.* It can be non-obvious to annotate which response is superior using an overall ranking label due to the fine-grained nature of $`Y_p`$, especially for complex responses. As shown in Figure <a href="#fig:overview" data-reference-type="ref" data-reference="fig:overview">1</a>, annotators usually cannot agree on assigning an overall ranking to different responses with respective advantages and flaws. We observe the issue leads to unsatisfactory annotation quality of existing RLHF data. Moreover, even if labeled with a clear preference, the optimal responses for the questions typically remain unknown. (2) *Learning efficiency.* During reinforcement learning, it can be challenging and data-demanding to precisely allocate the sparse and coarse-grained credit from $`Y`$ through the linguistic variance $`Y_n`$ to the preferred behavior $`Y_p`$. Misallocation to the non-robust bias factor $`Y_s`$ will lead models to collapse to exploit trivial rewards .

**Fine-grained Correctional Human Preference Collection.** To address the challenges, we propose to collect fine-grained human preferences in the form of segment-level corrections. As shown in Figure <a href="#fig:overview" data-reference-type="ref" data-reference="fig:overview">1</a>, given a flawed output $`y_l`$ from MLLMs, we ask human annotators to directly correct the hallucinated segments, resulting in a factually optimal output $`y_w`$. The annotation simultaneously yields a segment-level incremental preference pair ($`y_w`$, $`y_l`$). The simple procedure effectively addresses the challenges: (1) The annotation of incremental correction in segments is clearer and more operable for human labelers. (2) The dense and fine-grained feedback is directly allocated to the preferred behavior $`Y_p`$, excluding the linguistic variance $`Y_n`$ and the non-robust bias $`Y_s`$, therefore improving learning efficiency and preventing reward hacking problems. In experiments, we find that the procedure greatly improves the annotation quality and data efficiency, enabling our model to surpass concurrent models trained on an order of magnitude more labeled preference data (see Section <a href="#sec:analysis" data-reference-type="ref" data-reference="sec:analysis">4.3</a>).

In practice, we obtain a total of 1.4k prompts as input from existing instruction tuning dataset  and image description prompts generated by GPT-4, and get the responses from Muffin  for human annotation. The responses after annotation contain 64.4 words and 2.65 corrected segments on average. We observe that the corrections are diverse in hallucination types, including objects (41.2%), positions (20.3%), numbers (16.5%), attributes (10.0%), actions (5.3%) and miscellaneous types (6.8%).

# Method

We introduce the RLHF-V approach that learns the fine-grained correctional human feedback by dense direct preference optimization. In addition, we also mitigate existing sources of hallucination in MLLM training by addressing the vision-language mismatch problem.

## Dense Direct Preference Optimization

To leverage the dense and fine-grained human feedback, we present DDPO, a new variant of direct preference optimization  for directly optimizing the MLLM policy against dense human preference. The prevalent RLHF approaches involve fitting a reward model on the preference data, and then training the critique, policy and value models to maximize the reward without deviating too far from the reference model . This procedure requires training multiple LLMs with extensive sampling and training, which suffers from complex procedures and high computation cost.

Direct Preference Optimization (DPO)  solves this reinforcement learning objective in a simpler equivalent supervised fashion. Here we briefly introduce the DPO method, and refer readers to the original paper for more details. The key observation of DPO is that the reward function $`r(x, y)`$ can be analytically expressed by its optimal policy model $`\pi_* (y|x)`$ and reference model $`\pi_\text{ref} (y|x)`$, and therefore we can directly optimize the policy model under proper forms on the preference data. Specifically, the reward model $`r(x, y)`$ can be represented as:

$$
r(x, y) = \beta \log \frac{\pi_* (y|x)}{\pi_\text{ref} (y|x)} + \beta \log Z(x)
$$

where $`\beta`$ is a constant and $`Z(x)`$ is the partition function. Based on this observation, the policy model can be directly optimized on the human feedback data:

$$
\begin{aligned}
\mathcal{L} &= -\mathbb{E}_{(x, y_w, y_l)}\bigl[\log \sigma(r(x, y_w)- r(x, y_l))\bigr] \\
&=  -\mathbb{E}_{(x, y_w, y_l)}\bigl[\log \sigma(\beta\log \frac{\pi_* (y_w|x)}{\pi_\text{ref} (y_w|x)}- \beta\log \frac{\pi_* (y_l|x)}{\pi_\text{ref} (y_l|x)})\bigr],
\end{aligned}
$$

where the reference model $`\pi_\text{ref} (y|x)`$ is usually implemented by an instruction-tuned base model we want to improve, and is kept fixed during DPO training. Only the policy model $`\pi_* (y|x)`$ is updated. We note that DPO is more simple, efficient and stable in aligning MLLM behaviors compared with traditional RLHF approaches.

Leveraging dense and fine-grained segment-level feedback essentially requires the model to evaluate the reward of segment-level actions. However, DPO is designed for learning preference in the form of overall response ranking labels. Specifically, the action score of DPO is given by the likelihood of the holistic response in practice, where different segments are equally treated:

$$
\log \pi(y|x) = \sum \limits_{y_i\in y} \log p(y_i|x, y_{<i})
$$

where $`y_i`$ is the $`i`$-th token of the response $`y`$. We argue that compared with unchanged segments $`y_u`$, corrected segments $`y_c`$ more directly reveal human judgment in hallucination, and thus should contribute more to the overall action evaluation. Therefore, we propose to score the response as a weighted aggregation of the fine-grained segments:[^1]

$$
\log \pi(y|x) = \frac{1}{N} \bigl[\sum \limits_{y_i\in y_u} \log p(y_i|x, y_{<i}) + \gamma \sum \limits_{y_i \in y_c} \log p(y_i|x, y_{<i})\bigr]
$$

where $`\gamma > 1`$ is a weighting hyperprameter, and larger $`\gamma`$ means more contribution from the corrected segments. $`N = |y_u| + \gamma |y_c|`$ is a normalizing factor, preventing longer responses from getting higher scores. In this way, corrected segments are highlighted to receive stronger human preference feedback to be factually grounded. In experiments, we find that DDPO can better exploit the fine-grained human feedback, leading to more trustworthy responses.

## Mitigating Hallucination from VL Mismatch

DDPO reduces hallucination by learning from human feedback. From another cause-and-effect view, we examine the mainstream MLLM training paradigm, and identify sources of hallucinations in training MLLMs. Based on the observations, we motivate a more trustworthy training recipe.

In general, current MLLMs learn multimodal capabilities in a supervised learning paradigm, where the model outputs are supervised against the ground-truth text associated with the image. In such a paradigm, hallucinations can be introduced by mismatches between images and text data. In practice, the mismatch can come from: (1) low-quality text in pre-training and instruction tuning data, and (2) careless image augmentation during training. We specify the issues and solutions in the following.

**Addressing Low-quality Text Influence.** Current pre-training data of MLLMs are automatically crawled from the Web , which inevitably suffers from severe noise in the text even after extensive post-processing. Supervising MLLMs against such data is essentially teaching them to hallucinate (e.g., describing elements not present in the image, or producing inconsistent descriptions with the image). Similarly, most existing visual instruction tuning datasets are generated by ChatGPT/GPT-4 according to intermediate text annotations , which inevitably introduces hallucination into instruction data. While it can be difficult to repair existing pre-training and instruction-tuning data, we find that the influence can be countered by simply post-training MLLMs on high-quality visual question-answering datasets. Intuitively, human-labeled datasets can provide accurate learning signals to calibrate model behaviors from hallucinations, and also enhance instruction-following capabilities. In our experiments, we find that simply fine-tuning the model on VQAv2  can significantly reduce the hallucination rate (see Section <a href="#sec:analysis" data-reference-type="ref" data-reference="sec:analysis">4.3</a>).

**Mitigating Untrustworthy Image Augmentation.** The vision-language mismatch can also come from the image domain. Data augmentation is widely adopted to improve the data diversity and model robustness in various multimodal models . However, we note that such augmentation must be performed with care in training MLLMs. The key problem is that some image augmentation operations can significantly change the semantics of images, which may make the augmented image inconsistent with the associated text. For example, during augmentation, random cropping can make the objects mentioned in the text absent from the image. This can make the model describe non-existing objects, with wrong numbers, and in wrong positions. In our model training, we exclude image cropping in data augmentation, which improves the trustworthiness of MLLMs (see Section <a href="#sec:analysis" data-reference-type="ref" data-reference="sec:analysis">4.3</a>).

# Experiments

In this section, we empirically investigate the effectiveness of RLHF-V in aligning MLLM behaviors. In addition to evaluating the trustworthiness and helpfulness of conversation, we also analyze the data efficiency and scalability as well as the robustness. We refer readers to the appendix for more details on benchmarks, baselines and results.

## Experimental Settings

We first introduce the experimental settings, including evaluation, baselines, and implementation details.

**Evaluation.** We evaluate the models from two perspectives, including trustworthiness reflecting the hallucination degree, and helpfulness reflecting the general interaction quality. Similar to , we find binary classification evaluation (i.e., answering yes/no)  cannot well reflect the MLLM behaviors in open-ended long-form interactions. We thus adopt benchmarks that directly evaluate the long-form responses, which are more closely related to the practical usage scenarios of MLLMs. For trustworthiness, we perform evaluation on three benchmarks:

\(1\) **Object HalBench**  is a widely adopted benchmark for assessing object hallucination in detailed image descriptions. It compares the objects in the model output with object labels exhaustively annotated for COCO images  to detect object hallucination. To improve the evaluation stability, we augment the benchmark with 8 diverse prompts for detailed image descriptions. We report the response-level hallucination rate (i.e., the percentage of responses that have hallucinations), as well as the mention-level hallucination rate (i.e., the percentage of hallucinated object mentions among all object mentions).

\(2\) **MMHal-Bench**  evaluates hallucinations and response informativeness. It employs GPT-4 to compare model output with human response and several object labels to decide the scores. In experiments, we find that GPT-4 cannot reliably detect hallucinations due to the incompleteness of MMHal-Bench text annotations. We therefore only report the informativeness score from GPT-4, and assess response-level hallucination rate by human evaluation.

\(3\) **MHumanEval.** The above evaluations are either limited to common object hallucination or dominated by short-form question answering (i.e., questions that can be sufficiently answered by a few words). To provide a more reliable and comprehensive evaluation over diverse hallucination types, we present MHumanEval benchmark, which covers both long-form image descriptions, and short-form questions. The benchmark contains 146 samples collected from Object HalBench (50) and MMHal-Bench (96). Given model responses, we ask human annotators to label the hallucinated segments and hallucination types of the segments, including objects, positions, numbers and others. We report the response-level hallucination rate on these types.

For helpfulness, we adopt two benchmarks: (1) **LLaVA Bench**  is a widely adopted benchmark for assessing multimodal conversation, detailed description and complex reasoning capabilities. It scores model output against reference response via GPT-4. (2) **VQAv2**  is a popular dataset for short-form visual question answering.

<tbody> <tr> <td rowspan="4" style="text-align: left;"><strong>Model</strong></td> <td colspan="3" style="text-align: center;"><strong>Living Room</strong></td> <td colspan="3" style="text-align: center;"><strong>Kitchen</strong></td> <td colspan="3" style="text-align: center;"><strong>Bathroom</strong></td> <td colspan="3" style="text-align: center;"><strong>Street</strong></td> <td rowspan="4" style="text-align: center;">$\overline{\Delta}$</td> </tr> <tr> <td colspan="3" style="text-align: center;">book, person, bed</td> <td colspan="3" style="text-align: center;">bottle, bowl, cup</td> <td colspan="3" style="text-align: center;">toilet, sink, bottle</td> <td colspan="3" style="text-align: center;">person, car, motorcycle</td> </tr> <tr> <td colspan="3" style="text-align: center;">chair, couch, remote</td> <td colspan="3" style="text-align: center;">person, chair, knife</td> <td colspan="3" style="text-align: center;">toothbrush, person, cup</td> <td colspan="3" style="text-align: center;">traffic light, handbag, truck</td> </tr> <tr> <td style="text-align: center;">H<sub>a</sub></td> <td style="text-align: center;">H<sub>s</sub></td> <td style="text-align: center;"><em>Δ</em></td> <td style="text-align: center;">H<sub>a</sub></td> <td style="text-align: center;">H<sub>s</sub></td> <td style="text-align: center;"><em>Δ</em></td> <td style="text-align: center;">H<sub>a</sub></td> <td style="text-align: center;">H<sub>s</sub></td> <td style="text-align: center;"><em>Δ</em></td> <td style="text-align: center;">H<sub>a</sub></td> <td style="text-align: center;">H<sub>s</sub></td> <td style="text-align: center;"><em>Δ</em></td> </tr> <tr> <td style="text-align: left;">LLaVA-1.5 </td> <td style="text-align: center;">25.2</td> <td style="text-align: center;">41.8</td> <td style="text-align: center;">+16.6</td> <td style="text-align: center;">18.9</td> <td style="text-align: center;">23.9</td> <td style="text-align: center;">+5.0</td> <td style="text-align: center;">22.4</td> <td style="text-align: center;">30.4</td> <td style="text-align: center;">+8.0</td> <td style="text-align: center;">20.6</td> <td style="text-align: center;">28.0</td> <td style="text-align: center;">+7.4</td> <td style="text-align: center;">+9.2</td> </tr> <tr> <td style="text-align: left;">LLaVA-RLHF </td> <td style="text-align: center;">23.7</td> <td style="text-align: center;">34.5</td> <td style="text-align: center;">+10.8</td> <td style="text-align: center;">13.1</td> <td style="text-align: center;">17.4</td> <td style="text-align: center;">+4.3</td> <td style="text-align: center;">18.2</td> <td style="text-align: center;">19.5</td> <td style="text-align: center;">+1.4</td> <td style="text-align: center;">18.3</td> <td style="text-align: center;">22.7</td> <td style="text-align: center;">+4.4</td> <td style="text-align: center;">+5.2</td> </tr> <tr> <td style="text-align: left;">QWEN-VL </td> <td style="text-align: center;">24.5</td> <td style="text-align: center;">34.5</td> <td style="text-align: center;">+10.0</td> <td style="text-align: center;">16.4</td> <td style="text-align: center;">20.8</td> <td style="text-align: center;">+4.4</td> <td style="text-align: center;">21.6</td> <td style="text-align: center;">17.5</td> <td style="text-align: center;"><strong>-4.1</strong></td> <td style="text-align: center;">22.5</td> <td style="text-align: center;">32.0</td> <td style="text-align: center;">+9.5</td> <td style="text-align: center;">+5.0</td> </tr> <tr> <td style="text-align: left;">RLHF-V</td> <td style="text-align: center;"><strong>5.5</strong></td> <td style="text-align: center;"><strong>8.0</strong></td> <td style="text-align: center;"><strong>+2.5</strong></td> <td style="text-align: center;"><strong>3.8</strong></td> <td style="text-align: center;"><strong>5.9</strong></td> <td style="text-align: center;"><strong>+2.1</strong></td> <td style="text-align: center;"><strong>4.1</strong></td> <td style="text-align: center;"><strong>4.0</strong></td> <td style="text-align: center;">-0.1</td> <td style="text-align: center;"><strong>2.3</strong></td> <td style="text-align: center;"><strong>4.6</strong></td> <td style="text-align: center;"><strong>+2.3</strong></td> <td style="text-align: center;"><strong>+1.7</strong></td> </tr> <tr> <td style="text-align: left;">GPT-4V </td> <td style="text-align: center;">8.2</td> <td style="text-align: center;">19.4</td> <td style="text-align: center;">+11.2</td> <td style="text-align: center;">4.6</td> <td style="text-align: center;">5.7</td> <td style="text-align: center;">+1.1</td> <td style="text-align: center;">5.9</td> <td style="text-align: center;">13.3</td> <td style="text-align: center;">+7.5</td> <td style="text-align: center;">4.2</td> <td style="text-align: center;">4.6</td> <td style="text-align: center;">+0.4</td> <td style="text-align: center;">+5.0</td> </tr> </tbody>

**Baselines.** We compare our model with state-of-the-art baselines. (1) **General baselines.** We adopt Qwen-VL-Chat , LLaVA , LLaVA 1.5 , Muffin , and InstructBLIP  as representative general baselines. These models are mostly pre-trained on large-scale multimodal data, and fine-tuned on high-quality instruction data, achieving strong performance across various multimodal tasks. (2) **Baselines tailored for hallucination problems.** LRV  is fine-tuned on 400k instruction data generated by GPT-4, and mitigates hallucination by limiting the response length. The concurrent LLaVA-RLHF  employs the strong 13B Vicuna v1.5  (fine-tuned from LLaMA-2 ) as LLM backbone. It trains the reward model on 10k human-labeled preference data, and performs proximal policy optimization  on 72k factually augmented data. (3) **Commercial Baseline.** We also include GPT-4V  as a strong reference, evaluating the gap between the open-source models and state-of-the-art commercial models.

**Implementation Details.** We implement the RLHF-V framework based on Muffin . The model uses BEiT-3  as the visual module, and 13B Vicuna v1.0  (fine-tuned from LLaMA ) as the LLM backbone. The hyperparameter $`\beta`$ is 0.5, and the weighting coefficient $`\gamma`$ is 5. We train the model with DDPO for 7 epochs, with image resolution 448, learning rate 5e-7 and batch size 32. The training of RLHF-V is computationally efficient, which takes less than 1 hour on 8 A100 GPUs in total.

![](../images/RLHF-V_md_images/figs/datascaling_subdraw_yellow_red_1127.pdf.png)

Hallucination rate and number on MHumanEval (all types) with respect to the amount of preference data. We report the results of different models trained on different RLHF data.

## Main Results

The main experimental results are reported in Table <a href="#tab:main results" data-reference-type="ref" data-reference="tab:main results"></a>, from which we observe that: (1) RLHF-V achieves state-of-the-art performance in trustworthiness among open-source models, outperforming strong general models and models tailored for hallucination. The framework significantly reduces the hallucination rate of the base model Muffin by 75.8% relative points for common objects on Object HalBench, and by 34.8% for overall objects on MHumanEval. The improvement is consistent in different granularities including response-level and mention-level hallucinations, and different hallucination types including objects, positions, and numbers. The reduction is more significant on the more challenging long-form answers on Object HalBench and MHumanEval. The results show that RLHF-V can effectively learn from fine-grained correctional human feedback to enable more trustworthy MLLM behaviors. (2) RLHF-V achieves promising performance in response helpfulness, where the results on MMHalBench, LLaVA Bench and VQAv2 are strong and comparable to the base model. This shows that RLHF-V can enhance the trustworthiness of MLLMs without sacrificing their helpfulness.

## Analysis

In this section, we conduct analyses on the framework considering the following research questions: (1) How does RLHF-V’s performance scale with feedback data amount? (2) What is the advantage of fine-grained correctional preference data over traditional overall ranking data? (3) Can RLHF-V’s data and method be adopted to enhance the trustworthiness of other MLLMs? (4) How does human feedback alleviate hallucinations intuitively?

**Scaling feedback data leads to promising results.** We report the hallucination rate and numbers of hallucinated segments on MHumanEval under different amounts of feedback data in Figure <a href="#fig:data_scaling" data-reference-type="ref" data-reference="fig:data_scaling">2</a>. We observe that the hallucination rate and number of RLHF-V show a significant and rapid decrease as the data amount grows. This shows that fine-grained correctional human feedback provides effective and efficient learning signals for MLLM behavior alignment. Based on this tendency, we expect better performance can be achieved with an increasing amount of feedback data. We leave this for future work.

**Fine-grained correctional human feedback enables better learning efficiency.** To quantify the advantage of fine-grained correctional human feedback, we replace our data with the 2.2k human preference data on hallucination from LLaVA-RLHF, which gives overall ranking labels following common RLHF practices. From the experimental results in Figure <a href="#fig:data_scaling" data-reference-type="ref" data-reference="fig:data_scaling">2</a>, we observe that model equipped with our data shows a more significant and rapid reduction in hallucination rate and number. Notably, using only 200 preference data, our model achieves comparable hallucination rate to the model that uses an order of magnitude more labeled data from LLaVA-RLHF. The superior data efficiency is due to (1) better data quality since label ambiguity is minimized, and (2) more direct feedback on hallucinated segments, excluding non-robust bias and linguistic variance.

**RLHF-V generalizes to enhance other MLLMs.** To investigate the generalization capability of the framework, we adopt RLHF-V’s data and approach to align the behavior of LLaVA , a representative and widely used MLLM. Experimental results show that RLHF-V effectively reduces the hallucination count of LLaVA by 13.8 relative points, as well as the hallucination rate by 5.9 relative points. We also apply RLHF-V to stronger base models and build the OmniLMM-12B  which achieves new SoTA results on multiple hallucination benchmarks. For example, OmniLMM-12B exhibits only 4.5% mention-level hallucination on the Object HalBench. Moreover, OmniLMM-12B also shows leading performance among comparable-sized models on multiple benchmarks (1637 on MME-Perception , 71.1 on SeedBench-I ). The results demonstrate that RLHF-V is applicable across different MLLMs to improve trustworthiness.

**RLHF-V reduces hallucination from correlation and over-generalization.** LLMs possess rich world knowledge and strong generalization capabilities. Without proper positive/negative human feedback, MLLMs can over-generalize to produce highly correlated and plausible concepts, which leads to hallucinations. For example, a prevalent hallucination case observed across different MLLMs is claiming the presence of *person* as long as they see an image of *street*. To quantify the problem, we select a set of representative scenes $`\{\textit{living room}, \textit{kitchen}, \textit{bathroom}, \textit{street}\}`$. For each scene, we identify the corresponding images in COCO by lexically matching the captions with the scene name. Then we obtain the top 10 frequent objects in the scene from the COCO object annotations. We compare the response-level hallucination rate for these objects (1) on average across all test samples, and (2) on samples under the target scene. Models prone to over-generalization will expect a significant increase in the hallucination rate ($`\Delta`$).

From the experimental results in Table <a href="#tab:scene" data-reference-type="ref" data-reference="tab:scene"></a>, we observe that: (1) All models including GPT-4V show a substantial increase in the hallucination rate, which demonstrates the over-generalization hypothesis. (2) RLHF-V exhibits the smallest change in the hallucination rate, which is even more robust than GPT-4V. The reason for the robustness is that RLHF-V provides crucial positive/negative fine-grained correctional human feedback for MLLMs, which helps to learn clear behavior boundaries between reasonable generalizations and over-generalizations. (3) RLHF-V achieves the lowest hallucination rates for these common objects both on average and especially under common scenes. This makes RLHF-V preferable in practical real-world applications.

**Ablation Study.** To investigate the contribution of each component, we perform an ablation study. From the experimental results in Table <a href="#tab:ablation" data-reference-type="ref" data-reference="tab:ablation"></a>, we can observe that: (1) Learning human feedback with vanilla DPO leads to performance degrades, showing the advantage of DDPO in exploiting the fine-grained human preference. (2) Fine-tuning on VQAv2 leads to a significant reduction in hallucination rates compared with the base model. This reveals the value of traditional human-annotated datasets from a new perspective of hallucination mitigation. (3) Including untrustworthy data augmentation (i.e., image cropping) in training hurts the performance on both hallucination and VQAv2. This shows that careless data augmentation can be a double-edged sword in training MLLMs.

![](../images/RLHF-V_md_images/figs/case.pdf.png)

Qualitative results of different models on short-form QA and long-form QA. <strong>Correct answers</strong>, <strong>unreasonable extensions</strong> and <strong>hallucinations</strong> are highlighted in color respectively.

**Case Study.** To provide an intuitive understanding and comparison of different models, we provide qualitative results in Figure <a href="#fig:case" data-reference-type="ref" data-reference="fig:case">3</a>. We show cases in two representative scenarios: (1) Short-form QA (i.e., questions that can be sufficiently answered in a few words). Our model typically maintains a good balance between helpfulness, engagement and clarity. In comparison, LLaVA-RLHF is usually far more engaging, introducing lengthy extensions however that can be less reasonable or relevant. (2) Long-form QA (i.e., questions that require long text to answer). We observe that MLLMs are significantly more prone to hallucinations in long-form QA, since it typically requires more comprehensive capabilities from multiple perspectives. For example, InstructBLIP and LLaVA-RLHF can confidently describe non-existing objects in a large proportion of their responses, whereas RLHF-V introduces significantly fewer hallucinations while delivering a comparable amount of effective information. We refer readers to the appendix for more qualitative results.

# Related Work

**Multimodal Large Language Models.** Recent trends in multimodal learning have witnessed the success of building MLLMs by connecting visual encoders with powerful LLMs . The current MLLM training paradigm typically involves two stages: (1) Pretraining. Models are pretrained on large-scale image-text pairs  or interleaved data  to learn the semantic mapping between visual and text signals. (2) Instruction Tuning. To enable the model with instruction-following capability, MLLMs are further fine-tuned on visual instruction data, including collections of existing human-annotated datasets , and generated data from ChatGPT/GPT-4 . Despite the success, current MLLMs suffer from serious hallucination problems . Notably, even after extensive efforts, GPT-4V has still been found to be prone to hallucinations, making basic factual errors confidently . The problem undermines practical applications of MLLMs especially in high-stakes scenarios, which has recently drawn increasing attention from the community.

**Behavior Alignment for LLMs.** Aligning language agent behaviors with human preference has emerged as a promising research direction . Pivotal approaches in LLMs include instruction tuning (or supervised fine-tuning) and RLHF . While supervised fine-tuning is suitable for basic behavior alignment , due to the mismatch between likelihood maximization objective and human preference, it may introduce or amplify hallucination . Therefore, RLHF is widely accepted for further behavior and preference alignment , where proximal policy optimization (PPO)  is recognized as the major technique. Later adaptations attempt to stabilize the optimization process  and enclose more fine-grained signals . However, RLHF has rarely been explored in MLLMs to align model behaviors with humans.

**Reducing Hallucination for MLLMs.** Some preliminary efforts have been made to alleviate hallucination problems in MLLMs. LRV  generates instruction data with negative responses, and mitigates hallucination by limiting the response length. However, limiting the response length does not essentially address the problem, and also undermines the response helpfulness. VIGC  iteratively refines the instruction data for better instruction tuning. Woodpecker  proposes to post-edit hallucinations by merging the output of MLLMs and a more accurate expert VQA model using GPT-3.5. The post-editing procedure involves external tools and LLMs much larger than the target MLLM online in multiple stages, which leads to high inference costs and delays. Gunjal   distinguishes the inaccurate parts in responses via human annotation, and internally discourages the hallucinated parts by direct preference optimization. However, the positive behaviors for hallucinated parts are unknown, making the human feedback not complete enough to learn the behavior boundary. The concurrent LLaVA-RLHF  employs the traditional RLHF approach  on MLLMs, and augments the reward model with rich additional text descriptions. It is therefore similarly challenged with label ambiguity, learning efficiency, and complex training. In comparison, RLHF-V presents the first fine-grained correctional human feedback learning framework for behavior alignment, and systematically addresses different hallucination sources in training MLLMs, achieving strong performance in trustworthiness.

# Conclusion

Hallucination is a critical problem preventing practical applications of MLLMs in real-world scenarios. In this work, we present RLHF-V, a novel framework that enhances the trustworthiness of MLLMs by behavior alignment from fine-grained correctional human feedback. Comprehensive experimental results show that our model achieves state-of-the-art performance in trustworthiness especially in challenging long-form responses while maintaining strong helpfulness. In this work, we collect correctional feedback from human annotators. In future, with the progress of more trustworthy and capable MLLMs, we will explore collecting accurate preferences from MLLMs, which can facilitate large-scale preference learning for stronger behavior alignment. Besides, we note that the framework of RLHF-V can potentially also help reduce the hallucinations in LLMs, which we will explore in future.

# Contributions

The authors’ contributions can be outlined as follows:

- In initializing the project, Yuan Yao and Tianyu Yu design the framework to collect correctional human feedback. Tianyu Yu devise the DDPO algorithm. Zhiyuan Liu, Hai-Tao Zheng, Maosong Sun and Tat-Seng Chua offer invaluable guidance in project design.

- In data collection, Taiwen He, Haoye Zhang, Tianyu Yu and Yuan Yao take charge of the annotation process to ensure the data quality.

- In model training and evaluation, Tianyu Yu implements the training framework. Tianyu Yu, Haoye Zhang and Yuan Yao design the evaluation framework. Tianyu Yu and Haoye Zhang implement the evaluation codebase.

- In paper writing, Yuan Yao and Tianyu Yu write the paper. Haoye Zhang, Taiwen He, Yifeng Han, Ganqu Cui, Zhiyuan Liu, Hai-Tao Zheng, Maosong Sun and Tat-Seng Chua offer suggestions to polish the writing.

- For public usability, Tianyu Yu, Yifeng Han, Jinyi Hu and Yuan Yao promote the open-source project.

- Throughout the project, Zhiyuan Liu, Hai-Tao Zheng, Maosong Sun and Tat-Seng Chua provide invaluable guidance and advice.

# Zoom-in Study regarding GPT-4V

We perform a zoom-in study of RLHF-V concerning GPT-4V to provide a better understanding of their behaviors.

## Hallucination Patterns

We conduct a comparative analysis of the responses generated by RLHF-V and GPT-4V, and have the following key observations:

\(1\) Compared with RLHF-V, GPT-4V tends to describe more details in the images and elaborate more on the interrelations among them. Quantitatively, we utilize ChatGPT to extract all the object mentions in the responses of GPT-4V, and find that the average number per response is 2.1 times larger than RLHF-V. We mainly attribute this to the higher resolution (7.6 times larger than RLHF-V)  and the more powerful LLM backbone .

\(2\) GPT-4V’s hallucinations are more concentrated in some responses. In HumanEval, the hallucination rates of GPT-4V on *Object* and *Position* are comparable to RLHF-V. However, in the comprehensive *ALL* metric, the hallucination rate is 17.3% lower than RLHF-V. To better understand the reasons behind this phenomenon, we conduct a thorough analysis of the evaluation results. We observe that different types of hallucinations in GPT-4V are often concentrated in a small subset of responses, while contributing to hallucination rates across multiple subcategories. Quantitatively, we sort the responses of each model by the hallucination count in descending order, and plot the curve of hallucination count ratio vs hallucination response ratio. From the results in Figure <a href="#fig:hall_accumulation" data-reference-type="ref" data-reference="fig:hall_accumulation">4</a>, we can see that the top 45.6% hallucinated responses of GPT-4V contribute to 75% hallucination counts. In comparison, the top 64.6% hallucinated responses of RLHF-V contribute to 75% hallucinations. We refer readers to Section <a href="#sec:cases" data-reference-type="ref" data-reference="sec:cases">8</a> for more qualitative results.

## Distillation against GPT-4V

Upon observing GPT-4V’s superior fine-grained image perception and text generation capabilities, an intuitive question is, will it be beneficial to distill GPT-4V capabilities through visual instruction tuning? To this end, we collect 1.2k visual instruction data about long-form image descriptions from GPT-4V. We then use the response generated by GPT-4V to fine-tune our model. We observe that the average number of object mentions in the model response significantly increases by 1.8 times compared with the origin model. However, this can be a double-edged sword: as shown in Table <a href="#tab:gpt4_distill" data-reference-type="ref" data-reference="tab:gpt4_distill">1</a>, the hallucination rate significantly increases as well.

The results are consistent with the hypothesis of : “If we supervise the model against instruction data that far exceeds its own foundational capabilities, we are essentially teaching the model to hallucinate." Specifically, our model learns to produce more details and the interrelationship among them through distillation against GPT-4V, while the fundamental capabilities of the model are not enough for this demand. As a result, the hallucination problem is remarkably exacerbated. The results show that visual instruction data (or distillation target) is not the stronger the better, but rather should match the foundational capability of the model.

![](../images/RLHF-V_md_images/figs/hall_accumulation_fig.pdf.png)

Distribution of hallucination segments over different responses. GPT-4V hallucinations are more concentrated on a smaller subset of the responses. Hall.: Hallucination.

# Qualitative Results

We provide more qualitative results in this section to facilitate a more intuitive understanding and comparison of different models. Based on the qualitative results, we have the following observations:

\(1\) RLHF-V typically exhibits less hallucination in both short-form QA and long-form QA scenarios, compared with open-source models such as LLaVA-RLHF and InstructBLIP, as shown in Figure <a href="#fig:case_1" data-reference-type="ref" data-reference="fig:case_1">5</a>, <a href="#fig:case_2" data-reference-type="ref" data-reference="fig:case_2">6</a>, <a href="#fig:case_5" data-reference-type="ref" data-reference="fig:case_5">7</a>, and <a href="#fig:case_5-2" data-reference-type="ref" data-reference="fig:case_5-2">8</a>.

\(2\) GPT-4V is more descriptive regarding details in images as shown in Figure <a href="#fig:case_2" data-reference-type="ref" data-reference="fig:case_2">6</a>, <a href="#fig:case_5-2" data-reference-type="ref" data-reference="fig:case_5-2">8</a>, <a href="#fig:case_3" data-reference-type="ref" data-reference="fig:case_3">9</a> and <a href="#fig:case_4" data-reference-type="ref" data-reference="fig:case_4">10</a>. For example, in Figure <a href="#fig:case_3" data-reference-type="ref" data-reference="fig:case_3">9</a>, GPT-4V mentions *black dots* across each *tile* while RLHF-V does not describe these details.

\(3\) RLHF-V is more resistant to the over-generalization problem as shown in Figure <a href="#fig:case_3" data-reference-type="ref" data-reference="fig:case_3">9</a> and Figure <a href="#fig:case_4" data-reference-type="ref" data-reference="fig:case_4">10</a>. In Figure <a href="#fig:case_3" data-reference-type="ref" data-reference="fig:case_3">9</a>, GPT-4V falsely mentions objects which are highly related to the scene while not shown in the image such as *exhaust*, *hood*, and *bottle*.

<caption>Experimental results of distillation against GPT-4V. MHB: MMHal-Bench, GPT-4V distil.: instruction-tune the model using responses generated by GPT-4V.</caption> <thead> <tr> <th style="text-align: left;"><strong>Model</strong></th> <th colspan="4" style="text-align: center;"><strong>HumanEval</strong>↓</th> <th style="text-align: center;"><strong>MHB</strong>↓</th> </tr> </thead> <tbody> <tr> <td style="text-align: left;">2-5 (lr)6-6</td> <td style="text-align: center;">Obj.</td> <td style="text-align: center;">Pos.</td> <td style="text-align: center;">Num.</td> <td style="text-align: center;">All</td> <td style="text-align: center;">Resp.</td> </tr> <tr> <td style="text-align: left;">Muffin </td> <td style="text-align: center;">33.6</td> <td style="text-align: center;">16.4</td> <td style="text-align: center;">26.0</td> <td style="text-align: center;">74.7</td> <td style="text-align: center;">68.8</td> </tr> <tr> <td style="text-align: left;">RLHF-V</td> <td style="text-align: center;"><strong>21.9</strong></td> <td style="text-align: center;"><strong>7.5</strong></td> <td style="text-align: center;"><strong>14.4</strong></td> <td style="text-align: center;"><strong>55.5</strong></td> <td style="text-align: center;"><strong>52.1</strong></td> </tr> <tr> <td style="text-align: left;">w/ GPT-4V distil.</td> <td style="text-align: center;">45.2</td> <td style="text-align: center;">10.3</td> <td style="text-align: center;">20.6</td> <td style="text-align: center;">75.3</td> <td style="text-align: center;">62.5</td> </tr> </tbody>

# Implementation Details

We provide more implementation details in this section for better reproducibility. Benefiting from the high efficiency of training, we make all parameters trainable during the training process, which costs merely less than 1 hour on 8 A100 GPUs in total. We empirically find that adopting a longer warm-up (10% training steps) can make the training more stable and consequently apply this setting for all experiments in this paper. As for data collection, besides the prompts obtained from , we also use image description prompts generated by GPT-4 during the annotation process which are listed in Table <a href="#tab:gpt4_anno_prompt" data-reference-type="ref" data-reference="tab:gpt4_anno_prompt"></a>.

# Evaluation Details

We introduce more evaluation details, including baseline models and evaluation benchmarks.

<div class="minipage">

<div class="tcolorbox">

- Identify and describe each object in the image in detail.

- Describe the key features of the image in great detail.

- What are the main elements in this image? Describe them thoroughly.

- Explain what’s happening in the image with as much detail as possible.

- Detail the image’s components with particular focus on each entity.

- Provide an intricate description of every entity in the image.

- What are the main objects or subjects in the image? Please describe them in detail.

- What is the setting or environment in which the image takes place?

- How do the elements in the image relate to each other in terms of positioning or composition?

- Explain the elements of the image with thorough attention to detail.

- Explain the image’s various components in depth.

- What are the key features you observe in the image?

- Can you point out the details that make this image unique?

- Itemize the elements you identify in the image and describe them thoroughly.

- Convey the specifics of the image with meticulous attention to detail.

- Tell me what catches your eye in the image, and describe those elements in depth.

</div>

</div>

<div class="minipage">

<div class="tcolorbox">

- Provide a thorough description of the given image.

- What is this photo about? Please answer in great detail.

- Provide a thorough description of the given picture.

- Explain the narrative or story that the image seems to convey, detailing each part that contributes to it.

- Please provide a detailed description of the image. Describe the visual elements, colors, shapes, textures, and any objects or people present along with the overall mood or atmosphere portrayed in the image.

- Please provide a detailed description of the image, including its visual elements, such as colors, shapes, textures, objects, and people.

- Provide an intricate description of the image, capturing its visual elements, including colors, shapes, textures, objects, and any people present.

- Compose a detailed account of the image, encompassing its visual characteristics, like colors, shapes, textures, objects, and any human subjects, by paying careful attention to the specifics.

</div>

</div>

<div class="minipage">

<div class="tcolorbox">

You are an expert in image objects extraction according to a question answer pair. We asked an examiner to answer a question about a picture.

\[Start of Question\]

\<image\> {question}

\[End of Question\]

\[Start of Examiner’s Answer\]

{answer}

\[End of Examiner’s Answer\]

Assume that the answer is correct, please identify all visible objects that are directly shown in the image. Please following the instructions in below:

1\. You should only mention objects that are explicitly mentioned in the examiner’s answer.

2\. You should only extract the object names without the attributes of the objects.

3\. You should not include the properties of the object, like the color, material, etc. as part of the object name in your result.

4\. Make your answer precise. Present the results in a JSON list format: \[“object_1”, ..., “object_n”\].

5\. You should return an empty JSON list () if no visible objects can be found.

</div>

</div>

## Baselines

We compare with a series of state-of-the-art baselines:

- **LLaVA**: LLaVA  constructs 150K multimodal instructions based on the COCO dataset by asking GPT-4 to generate multi-turn dialogues for each image.

- **Muffin**: Muffin  propose to reformulate pre-trained vision-language models as the bridge toward large language models. The model is firstly pre-trained on 180M image-text pairs and then fine-tuned on their proposed UniMM-Chat instruction dataset consisting of 1.1M multimodal instructions.

- **LRV**: LRV  is fine-tuned on 400K instruction data generated by GPT-4, and mitigates hallucination by limiting the response length.

- **LLaVA-RLHF**: The concurrent LLaVA-RLHF employs the strong 13B Vicuna 1.5  (fine-tuned from LLaMA-2) as LLM backbone. It first trains the model with 122K instructions from VQAv2 , A-OKVQA  and Flickr30k to improve the foundational capabilities of the model. It then trains the reward model on 10K human-labeled preference data, and performs proximal policy optimization  on 72K factually augmented data.

- **InstructBLIP**: InstructBLIP  constructs a multimodal instruction tuning dataset based on 26 public datasets by apply pre-defined templates to directly formulate these datasets into a unified format. They also devise a novel instruction-aware Q-Former and train the model on the proposed dataset.

- **Qwen-VL-Chat**: Qwen-VL-Chat   utilizes a large ViT with 1.9B parameters initialized from OpenCLIP’s bigG  as image encoder. It is pre-trained on 1.4B image-text pairs and fine-tuned on more than 50M high-quality multimodal instructions.

- **LLaVA 1.5**: LLaVA 1.5  also employs the strong 13B Vicuna 1.5 (fine-tuned from LLaMA-2) as LLM backbone. It is pre-trained on 558K selected image-text pairs and fine-tuned on 665K multimodal instructions with elaborately designed training strategies.

## Benchmarks

We introduce additional details about the benchmarks we used for evaluation.

- **Object HalBench**: Object HalBench  is a widely adopted benchmark for assessing object hallucination in detailed image descriptions. To improve the evaluation stability, we augment the benchmark with 8 diverse prompts for detailed image descriptions during evaluation, where 4 instructions are adopted from  and the other 4 instructions are generated by GPT-4. We confirm that there is no overlap between the evaluation instructions and the training instructions. Detailed instructions are listed in Table <a href="#tab:obj_hall_bench" data-reference-type="ref" data-reference="tab:obj_hall_bench"></a>. Following , we randomly sample 300 images from the validation set of COCO  to form the evaluation image set. Regarding metrics, the response-level hallucination rate is the number of responses with object hallucinations divided by the number of responses that introduce COCO objects, while the mention-level hallucination rate is the number of falsely mentioned COCO objects in the generated responses divided by the total number of mentioned COCO objects. During evaluation, we first generate descriptions on images from the benchmark and then leverage ChatGPT to extract the mentioned objects in these responses which are further used to calculate the final scores following. Unlike which detects object mentions by exact-match, we find ChatGPT can perform the extraction with both better precision and recall and consequently apply this setting during evaluation. The full prompt we used to conduct such extraction is shown in Table <a href="#tab:chair_extraction" data-reference-type="ref" data-reference="tab:chair_extraction"></a>.

- **MMHal-Bench**: MMHal-Bench  evaluates hallucinations and response informativeness. It consists of 96 images from the validation and test sets of OpenImages . Each image in this benchmark is annotated with a brand new question and the image-question pairs cover 12 common object meta-categories from COCO.

- **HumanEval**: The above evaluations are either limited to common object hallucination or dominated by short-form question answering (i.e., questions that can be sufficiently answered by a few words). To provide a more reliable and comprehensive evaluation over diverse hallucination types, we present HumanEval benchmark, which covers both long-form image descriptions, and short-form questions. The benchmark contains 146 samples collected from Object HalBench (50) and MMHal-Bench (96). Given model responses, we ask human annotators to label the hallucinated segments and hallucination types of the segments, including objects, positions, numbers and others. We report the response-level hallucination rate on these types.

- **LLaVA Bench**: LLaVA Bench  is a widely adopted benchmark for assessing multimodal conversation, detailed description and complex reasoning capabilities. It consists of 30 image-question pairs for the aforementioned three capabilities respectively and scores model output against reference response via GPT-4.

- **VQAv2**: VQAv2  is a dataset for short-form visual question answering. The test-dev set of VQAv2 consists of 107K image-question pairs which covers a diverse range of capabilities.

![](../images/RLHF-V_md_images/figs/appendix_case_final1_2.pdf.png)

Qualitative results of different models. <strong>Correct answers</strong> and <strong>hallucinations</strong> are highlighted in color respectively.

![](../images/RLHF-V_md_images/figs/appendix_case_final2_2.pdf.png)

Qualitative results of different models. <strong>Hallucinations</strong> are highlighted in color.

![](../images/RLHF-V_md_images/figs/appendix_case_final5-1_2.pdf.png)

Qualitative results of different models. <strong>Unreasonable reasoning and extensions</strong> and <strong><em>scene related hallucinations</em></strong> are highlighted in color respectively.

![](../images/RLHF-V_md_images/figs/appendix_case_final5_part2_2.pdf.png)

Qualitative results of different models (continued figure). <strong>Unreasonable reasoning and extensions</strong> are highlighted in color.

![](../images/RLHF-V_md_images/figs/appendix_case_final3_2.pdf.png)

Qualitative results of different models. <strong>Hallucinations</strong> and <strong><em>scene related hallucinations</em></strong> are highlighted in color respectively.

![](../images/RLHF-V_md_images/figs/appendix_case_final4_3.pdf.png)

Qualitative results of different models. <strong>Hallucinations</strong> and <strong><em>scene related hallucinations</em></strong> are highlighted in color respectively.

[^1]: For denotation simplicity, without confusion we also use $`y_u`$ and $`y_c`$ to denote the set of tokens in unchanged and corrected segments respectively.
