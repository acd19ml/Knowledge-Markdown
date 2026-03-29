# An Investigation into Object Hallucination in Multi-modal Large Language Models

- Author: Your Name
- Department: xxx
- ID: 12341000

## I. Introduction

In this section, we present a comprehensive investigation into the problem of object hallucination in MLLMs, synthesizing state-of-the-art observations, comparing representative mitigation methodologies, and evaluating their underlying assumptions and trade-offs.

The advent of Multi-modal Large Language Models (MLLMs), such as LLaVA and GPT-4V, has significantly advanced the field of artificial intelligence by enabling models to understand, align, and reason over both visual and textual inputs. However, despite their remarkable capabilities in complex vision-language tasks, MLLMs suffer from a critical vulnerability known as object hallucination — a phenomenon where the model confidently generates descriptions or answers containing objects that do not actually exist in the provided image. In Li et al.'s work [1], the first systematic study on object hallucination of LVLMs is presented, introducing the POPE benchmark to quantify this severe issue.

Addressing object hallucination is fundamentally motivated by the need to deploy MLLMs in real-world, high-stakes applications. In domains such as autonomous driving, medical image analysis, and assistance for the visually impaired, a hallucinatory output (e.g., imagining a non-existent pedestrian or a false tumor) can lead to catastrophic consequences. Furthermore, recent studies reveal that these models become even more susceptible to hallucinations when facing perturbed inputs common in the real world, such as image cropping, blurring, or digital manipulation [2]. Therefore, mitigating hallucinations is not merely an academic pursuit, but a prerequisite for the safe and reliable deployment of MLLMs.

To combat this challenge, the research community has actively explored various dimensions of MLLM hallucinations. Based on our literature study, the current research can be broadly categorized into three typical directions:

- **Evaluation Benchmarks:** Moving beyond traditional and unstable metrics (e.g., CHAIR), researchers are designing robust, polling-based [1] and perturbation-aware [2] benchmarks to accurately measure the severity and boundaries of hallucinations.
- **Understanding the Causes:** Investigating the fundamental reasons behind the phenomenon. Recent works have identified that hallucinations are deeply rooted in statistical biases, such as object co-occurrence in training data and decoding uncertainty during text generation [3].
- **Mitigation Strategies:** Developing methods to reduce hallucinations without compromising the model's general capabilities. This includes post-hoc revision algorithms (e.g., LURE) [3] and defensive in-context learning strategies during the prompting stage [2].

## II. Application Setting & Failure Modes

### A. Evolution and Dilemmas of Evaluation Benchmarks

**Goals.** The primary goal of hallucination evaluation is to objectively and automatically quantify the extent to which an MLLM generates factually incorrect visual descriptions. A robust benchmark should provide standardized metrics that are scalable across different model architectures and highly aligned with human judgments.

**Design challenges.** Evaluating hallucinations is inherently difficult due to the open-ended nature of text generation. Traditional evaluation metrics rely heavily on rigid parsing rules, which struggle to adapt to the diverse linguistic styles and lengthy outputs of modern MLLMs. Furthermore, an ideal benchmark must remain stable against prompt variations and be capable of reflecting the model's reliability in noisy, real-world conditions rather than merely in idealized experimental settings.

**Related work and evolution.** Early evaluations heavily relied on metrics like CHAIR (Caption Hash Algorithm for Image Review). However, CHAIR is highly sensitive to the length of the generated text and prompt phrasing, leading to unstable and often inaccurate assessments for large models. To overcome these limitations, Li et al. [1] pioneered the POPE (Polling-based Object Probing Evaluation) benchmark. POPE innovatively transforms the complex open-ended parsing task into a simplified, polling-based binary classification problem. By prompting the model with direct Yes-or-No questions (e.g., "Is there a car in the image?"), POPE effectively isolates the hallucination issue. Furthermore, it employs three distinct probing strategies — Random, Popular, and Adversarial — to systematically force the model out of its comfort zone and expose hallucinations driven by statistical biases.

Despite the methodological leap brought by POPE, a critical reality dilemma remains: existing benchmarks typically operate in a "greenhouse" environment, evaluating models exclusively on pristine, high-quality images. In contrast, real-world visual inputs are often flawed. Recognizing this gap, Ding et al. [2] introduced Hallu-PI, the first benchmark specifically designed to assess MLLM hallucinations under perturbed inputs. By subjecting images to complex perturbations such as cropping, blurring, and image concatenation, Hallu-PI reveals that even state-of-the-art models like GPT-4V exhibit amplified hallucination rates under visual noise. This evolution highlights a crucial paradigm shift in the field: robust evaluation must not only measure a model's baseline accuracy but also strictly examine its vulnerability in complex, unpredictable real-world environments.

**Table 1. Comparison of MLLM hallucination evaluation and mitigation schemes.**

| Scheme | Focus Area | Key Mechanism |
| --- | --- | --- |
| POPE [1] | Evaluation | Polling-based binary QA |
| LURE [3] | Mitigation (Post-hoc) | Uncertainty-based revision |
| Hallu-PI [2] | Eval & Mitigation | Perturbed inputs & Def-ICL |

### B. Understanding Hallucination Causes

**Goals.** The primary goal here is to demystify the "black box" of MLLMs and identify the fundamental statistical or architectural roots of object hallucinations, moving beyond the superficial explanation of "inadequate training."

**Design challenges.** The main challenge lies in disentangling the sources of error. When an MLLM hallucinates, it is difficult to determine whether the visual encoder failed to capture the feature, the projection layer lost the visual-linguistic alignment, or the LLM component simply overrode the visual evidence with its own language priors.

**Related work and root causes.** To systematically diagnose these errors, Zhou et al. [3] conducted a rigorous statistical analysis, revealing three pivotal factors driving object hallucination:

1. **Co-occurrence bias:** MLLMs heavily rely on habitual associations learned during training. If "keyboard" and "mouse" frequently co-occur in the training data, the model might hallucinate a "mouse" when only a "keyboard" is present.
2. **Decoding uncertainty:** Tokens corresponding to hallucinated objects typically exhibit higher uncertainty (lower probability) during the decoding phase.
3. **Object position:** Hallucinations are remarkably position-dependent, occurring much more frequently in the later segments of long generated descriptions as the model gradually loses its grounding in the visual input and begins to freely associate based on its preceding text.

## III. Conclusion and Open Questions

In summary, the phenomenon of object hallucination represents a critical bottleneck for the reliable deployment of MLLMs. As demonstrated by recent literature, while polling-based evaluations (POPE) and perturbation-aware benchmarks (Hallu-PI) have improved our ability to measure this flaw, the mitigation strategies currently rely heavily on "patches" — such as post-hoc revision (LURE) or defensive prompting — rather than fundamental structural cures.

This naturally raises several open questions for future research: Can we intrinsically solve hallucination by redesigning the modality alignment mechanism? Do current projection layers (e.g., MLPs or Q-Formers) inevitably cause visual information loss that the LLM tries to fill with hallucinations? These architectural considerations are crucial and will be further explored in the subsequent sections of our group report.

### C. Mitigation Strategies and Trade-offs

**Goals.** The objective is to design efficient algorithms or methodologies to suppress hallucinations without severely compromising the model's generalization capabilities or incurring prohibitive computational costs (e.g., retraining the entire foundation model).

**Design challenges and trade-offs.** Mitigation inherently involves trade-offs. While instruction fine-tuning can alleviate the issue, it requires high-quality, hallucination-free datasets, which are expensive to curate. Consequently, recent literature focuses on parameter-efficient or training-free solutions, which present their own sets of trade-offs:

- **Post-hoc Revision (e.g., LURE):** Building upon the discovery of decoding uncertainty, Zhou et al. [3] proposed the LVLM Hallucination Revisor (LURE). LURE acts as a post-generation editor, reconstructing descriptions by focusing on highly uncertain object tokens. Trade-offs: The distinct advantage of LURE is that it is "plug-and-play"; it can be seamlessly integrated into any existing MLLM without altering the base model's parameters. However, the trade-off is a notable increase in inference latency, as it requires a two-pass generation process (initial generation followed by revision). Furthermore, its success heavily depends on the quality of the first-pass output.
- **Defensive Prompting and In-Context Learning:** To address the vulnerability of MLLMs under complex real-world conditions, Ding et al. [2] explored training-free prompting strategies. They demonstrated that Perturbed-Reminder and Perturbed In-Context Learning (Perturbed-ICL) can significantly enhance a model's robustness against visual noise (e.g., image cropping or concatenation). Trade-offs: This approach is highly cost-effective and agile, yet it consumes the model's limited context window. Additionally, prompt-based mitigation is often highly sensitive to the exact phrasing, and its effectiveness may vary drastically across different proprietary models (e.g., GPT-4V vs. Gemini).

## References

1. Y. Li, Y. Du, K. Zhou, J. Wang, W. X. Zhao, and J. Wen, "Evaluating object hallucination in large vision-language models," in *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, 2023.
2. P. Ding, J. Wu, J. Kuang, D. Ma, X. Cao, and X. Cai, "Hallu-PI: Evaluating hallucination in multi-modal large language models within perturbed inputs," in *Proceedings of the 32nd ACM International Conference on Multimedia*, 2024.
3. Y. Zhou, C. Cui, J. Yoon, L. Zhang, Z. Deng, C. Finn, M. Bansal, and H. Yao, "Analyzing and mitigating object hallucination in large vision-language models," in *The Twelfth International Conference on Learning Representations*, 2024.

## IV. Conclusion and Open Questions

In summary, the phenomenon of object hallucination remains a critical bottleneck for the reliable and safe deployment of Multi-modal Large Language Models. Our literature review highlights a necessary paradigm shift in how this vulnerability is quantified: the community has evolved from rigid, traditional metrics to targeted, polling-based evaluations like POPE [1], and is currently advancing toward stress-testing models under complex, real-world perturbations via benchmarks like Hallu-PI [2].

Through analyzing these evaluations, we observe that the root causes of hallucinations are deeply embedded in the models' statistical learning mechanisms — specifically, co-occurrence biases and decoding uncertainties [3]. Consequently, current state-of-the-art mitigation strategies inherently involve strict trade-offs. For instance, while post-hoc revision methods such as LURE offer an agile, plug-and-play solution without the prohibitive costs of model retraining, they inevitably introduce higher inference latency. Similarly, defensive prompting strategies are cost-effective but consume valuable context windows and often suffer from prompt sensitivity.

**Open directions.** The observation that current mitigation techniques function primarily as "post-generation patches" or "prompt-level defenses" raises a fundamental open question: Can we intrinsically eradicate object hallucination by fundamentally redesigning the underlying model architecture? It is highly probable that current modality projection layers (e.g., simple MLPs or Q-Formers) cause an initial loss of fine-grained visual information, forcing the LLM component to over-rely on its language priors and "guess" the missing visual details. To address this hypothesis, the subsequent sections of our group report will dive into the structural anatomy of MLLMs. We will explore how different visual encoders and modality alignment mechanisms operate, and investigate whether architectural innovations can provide a structural cure for the hallucination problem.
