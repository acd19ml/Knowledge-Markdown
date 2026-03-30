# Introduction

Large Vision-Language Models (LVLMs) have become integral in the intersection of computer vision and natural language processing, enabling a range of applications due to their ability to generate contextually relevant textual descriptions from visual inputs. These models are characterized by their effectiveness in capturing and translating complex visual patterns into coherent linguistic representations . The evolution of LVLMs is marked by ongoing improvements in model architecture, training methodologies, and data diversity, leading to enhanced performance and application versatility. Despite these advancements, specific challenges persist, with the issue of object hallucination  being a prominent concern that impacts the reliability and applicability of LVLMs across domains.

![](../images/VCD_md_images/figs/figure1_.pdf.png)

An illustration of Visual Contrastive Decoding. The hallucinated object <em>“Surfboards"</em> is highlighted in , and it is eliminated during the generative process by contrasting with the output distribution that favors hallucinations.

Object Hallucination in this context refers to the phenomenon where LVLMs generate textual content that is semantically coherent but inconsistent with ground-truth objects in the given image. This challenge not only reveals fundamental issues of LVLMs, such as over-reliance on statistical bias  and unimodal priors , but also has direct implications for the practical deployment of LVLMs. In applications where precision and reliability of generated content are paramount, object hallucinations can lead to misinformation, misinterpretation, and subsequent erroneous decision-making. In domains like healthcare , autonomous systems , and robotics , such inaccuracies are not just undesirable but could have significant consequences. Addressing the hallucination issue is therefore essential to enhance the integrity, reliability, and broad applicability of LVLMs in various real-world scenarios.

Various approaches have been explored to curb object hallucinations in VLMs. Early works made attempts on small-scale VLMs by either performing fine-grained modality alignment  or reducing the statistical bias of object co-occurrence with data augmentation . However, the behaviors of LVLMs differ significantly from small-scale VLMs, making related methods impractical to generalize and scale up . Several recent studies address this issue by proposing hallucination-targeted datasets for fine-tuning , training a post-hoc revisor to reconstruct less hallucinatory outputs  or adapting factually augmented Reinforcement Learning from Human Feedback (RLHF) . While existing interventions for object hallucination in LVLMs have shown effectiveness, the incurred human effort and computational cost highlight a pressing need for a simpler but efficient approach.

In this work, we analyze the effect of visual uncertainty on the two primary causes of object hallucinations in LVLMs, namely statistical bias and unimodal priors (i.e., language priors). Building on the analysis above, we introduce Visual Contrastive Decoding (VCD), a training-free technique designed to mitigate object hallucination in LVLMs. As shown in Figure <a href="#fig:vcd illustration" data-reference-type="ref" data-reference="fig:vcd illustration">1</a>, VCD is grounded in the principle of contrasting output distributions from original and distorted visual inputs. Hence, it acts as a corrective mechanism and calibrates the model’s over-reliance on language priors from integrated LLMs and statistical bias of LVLMs’ pretraining corpus. In the realm of efficiency, VCD stands out due to its minimal computational overhead compared with previous studies , circumventing the need for additional training or the usage of external tools (e.g., other pretrained models). Our experiments demonstrate VCD’s effectiveness, with consistent improvements on multiple object hallucination benchmarks (e.g., up to $`+7.4`$ F1 score boost on POPE  and $`+18\%`$ improvement on MME ) across different LVLM families, including LLAVA-1.5 , InstructBLIP , and Qwen-VL . In addition, our method is also beneficial to the general perception capacities of LVLMs as evidenced by benchmarking on MME and LLaVA-Bench[^3], indicating its potential applicability beyond the scope of object hallucination mitigation.

To sum up, our main contributions are as follows:

1.  We conduct an in-depth analysis of the effect of visual uncertainty on object hallucinations in LVLMs, particularly from the aspects of statistical bias and unimodal priors.

2.  Inspired by the analysis above, we design VCD, a training-free technique that can effectively mitigate object hallucinations in LVLMs. It calibrates the model’s outputs by contrasting output distributions derived from original and distorted visual inputs, ensuring more consistent content generation.

3.  Through comprehensive experiments, we demonstrate the efficacy of the proposed VCD in alleviating object hallucination and enhancing general perception capability. Our method yields notable improvements without the need for additional training or external tools.

# Related Work

## Visual-Language Models

The development of Vision-Language Models (VLMs) has transitioned from being rooted in BERT-based language decoders for merging visual and textual data , to a notable advancement ushered by the integration of Large Language Models (LLMs) . The advent of LLMs heralded the emergence of Large Vision-Language Models (LVLMs) , characterized by enhanced capabilities and performance. In this phase, LVLMs, supported by end-to-end training techniques, demonstrated unified decoding of visual and textual tokens, marking a significant enhancement in their performances and adaptability. Recent developments have seen a focus on Visual Instruction Fine-tuning , showcasing adaptability to a variety of vision-language tasks. The methodologies adopted, ranging from integrating cross-modal alignment networks to fine-tuning LLaMA models, underscore a trend of diversification and specificity in the approach .

## Hallucination in VLMs

Prior to the advent of LLMs, the NLP community has primarily defined “hallucination" as the generation of nonsensical content or content that deviates from its sources . In the realm of VLMs, “object hallucination" is also well-documented, referring to models producing plausible outputs that include objects that do not match or are missing from images . Mitigating object hallucination in VLMs has typically involved strategies such as fine-grained contrastive learning , ROI feature fusion , and the curtailment of co-occurrence patterns via data augmentation . However, with the distinct training paradigms and model architectures that characterize traditional VLMs and contemporary LVLMs, adapting these strategies to the newer auto-regressive approaches in LVLMs poses significant challenges .

Recent efforts have sought to navigate these complexities, with studies delving into the evaluation and detection of object hallucinations within the domain of LVLMs . For example, POPE converts the hallucination into a binary classification problem to probe the model’s awareness of whether a specific object exists in the image. Concurrently, there has been a notable push towards the development of refined datasets tailored for fine-tuning existing LVLMs , training a post-hoc revisor to detect and reconstruct less hallucinatory outputs , and adapting factually augmented RLHF . Nevertheless, existing approaches that acquire additional datasets, conduct fine-grained tuning on original or newly introduced models, or utilize other off-the-shell pretrained models can be time-consuming, labor-intensive, and computationally costly. Instead, we propose a conceptually different and training-free approach, VCD, that contrasts the output distributions with original and distorted visual inputs to calibrate the model’s over-reliance on unimodal priors and statistical bias, without utilizing external models.

# Method

## Decoding of Vision-Language Models

We consider an LVLM parametrized by $`\theta`$. The model takes as input a textual query $`{x}`$ and a visual input $`{v}`$, where $`{v}`$ provides contextual visual information to assist the model in generating a relevant response $`{y}`$ to the textual query. The response $`{y}`$ is sampled auto-regressively from the probability distribution conditioned on the query $`{x}`$ and the visual context $`{v}`$. Mathematically, this can be formulated as:
$$
\begin{equation} \begin{aligned} y_t & \sim p_\theta\left(y_t \mid {v}, {x}, {y}_{<t}\right), \\ & \propto \exp \operatorname{logit}_\theta\left(y_t \mid {v}, {x}, {y}_{<t}\right), \end{aligned} \end{equation}
$$
where $`y_t`$ denotes the token at time step $`t`$, and $`{y}_{<t}`$ represents the sequence of generated tokens up to the time step ($`t - 1`$). In the decoding phase of LVLMs, object hallucinations often emerge when probabilities are erroneously allocated to tokens that do not align with the presented visual input $`v`$. Previous studies have identified two primary causes of this problem: (1) statistical biases inherent in training data (e.g., prevalent but superficial object correlations) , and (2) over-reliance on language priors embedded within the powerful LLMs used as decoders . Our approach to mitigate object hallucinations first amplifies these undesirable behaviors with vague inputs and subsequently contrasts with them in the decoding process.

![](../images/VCD_md_images/figs/figure2_.pdf.png)

An illustration of visual uncertainty amplifying language priors. Given an image featuring a black banana among other colorful fruits, LVLMs favor more conventional banana colors—such as "<em>yellow</em>" and "<em>green</em>", with increasing visual uncertainty. The ground-truth color "<em>black</em>" diminishes in probability (<em>l</em><em>o</em><em>g</em><em>p</em>(<em>y</em>|<em>x</em>, <em>v</em><sup>′</sup>)) as the distortion escalates, making LVLMs over-reliant on the language priors from LLM pre-training that typically associate bananas with being yellow or green.

## Visual Uncertainty Amplifies Hallucinations

The fidelity of visual input is pivotal for LVLMs to accurately encode visual features and generate outputs faithfully. Yet, the introduction of uncertainty in visual inputs can tilt the equilibrium. This section delves into a comprehensive analysis aiming to validate the assumption that increased visual uncertainty can amplify the language priors and statistical biases in LVLMs, thus exacerbating object hallucination.

**Introduction of Visual Uncertainty** In this paper, we propose to adopt the most elementary method—applying a Gaussian noise mask to the original image—to introduce visual uncertainty. This method, although straightforward, provides an initial benchmark to estimate the baseline effects of visual uncertainty on model outputs. Following the forward diffusion process in image generation , the distorted image is modeled as follows:
$$
\begin{equation} \label{eq:1} \begin{aligned} &q\left({v}_t \mid {v}_{t-1}\right)=\mathcal{N}\left({v}_t ; \sqrt{1-\gamma} {v}_{t-1}, \gamma \mathbf{I}\right) \\ &q\left({v}_{T} \mid {v}_0\right)=\prod_{t=1}^T q\left({v}_t \mid {v}_{t-1}\right), \end{aligned} \end{equation}
$$
where $`v_0`$ denotes the original visual input (i.e., original image) and $`\mathbf{I}`$ refers to an identity matrix. We incrementally add a small amount of Gaussian noise for $`T`$ steps, producing a sequence of distorted images $`v_1,\dots,v_T`$. The original image $`v_0`$ gradually loses its distinguishable features as step $`t`$ goes larger, where the amount of noise added in each step is controlled by $`\gamma`$. Eventually, when $`T \rightarrow \infty`$, visual uncertainty reaches the maximum and $`v_T`$ will become indistinguishable from Gaussian noise.

**Visual Uncertainty Amplifies Language Priors** Figure <a href="#fig: language priors" data-reference-type="ref" data-reference="fig: language priors">2</a> shows that visual uncertainty can compel LVLMs to overlook visual evidence and overly exploit language priors for decision-making. However, this tendency is not entirely unexpected, as LLMs are designed to predict next-word probabilities based on vast textual corpora. When confronted with ambiguous visual stimuli, an LVLM might misinterpret these conventional, text-based predictions as a “safety net”. These priors, while generally useful, can introduce biases or assumptions that are inconsistent with the actual visual content, particularly when the visual input lacks clarity.

**Visual Uncertainty Amplifies Statistical Bias** The construction of most vision-language pretraining datasets is predominantly based on MSCOCO , which inherently suffers from an unbalanced object distribution and biased object correlations. Previous works point out that LVLMs, trained on such data, may inherit those statistical biases to generate descriptions with hallucinated objects. To further examine the hypothesis that visual uncertainty may amplify statistical biases from pretraining, we designed two targeted experiments to verify (1) if LVLMs hallucinate frequent objects more with distorted visual inputs and (2) if LVLMs are more prone to hallucinate objects that frequently co-occur with ground-truth objects in the image with distorted visual inputs. Figure <a href="#fig:bias" data-reference-type="ref" data-reference="fig:bias">3</a> shows an evident tendency that LVLMs are more prone to hallucinate frequent and co-occurring objects, attributing to the imbalanced object distributions and spurious object correlations inherited from the training data.

## Visual Contrastive Decoding

### Contrasting the Predictions

Our observations in the previous section reveal that visual uncertainty not only amplifies reliance on language priors but also makes LVLMs more likely to be biased by superficial object correlations present in pretraining datasets, leading to more severe hallucinations. In light of this, we introduce Visual Contrastive Decoding (VCD). VCD is formulated to counteract the statistical biases and language priors in LVLMs by contrasting model outputs generated from original and distorted visual inputs. This is achieved without necessitating additional training or external pretrained models, making VCD a cost-effective and efficient solution.

Specifically, given a textual query $`{x}`$ and a visual input $`{v}`$, the model generates two distinct output distributions: one conditioned on the original $`{v}`$ and the other on the distorted visual input $`{v'}`$, which is derived by applying pre-defined distortions (i.e., Gaussian noise mask) to $`{v}`$. Then, a new contrastive probability distribution is computed by exploiting the differences between the two initially obtained distributions. The new contrastive distribution $`p_{vcd}`$ is formulated as:
$$
\begin{equation} \label{eq:3} \begin{gathered} p_{vcd}\left(y \mid v, v', x\right) =\operatorname{softmax}\left[ (1+\alpha) \operatorname{logit}_\theta\left(y \mid v, x\right) \right.\\ \left.-\alpha \operatorname{logit}_\theta\left(y \mid v', x\right)\right], \end{gathered} \end{equation}
$$
where larger $`\alpha`$ values indicate a stronger amplification of differences between the two distributions ($`\alpha=0`$ reduces to regular decoding). From the adjusted output distribution $`p_{vcd}`$, we can apply various sampling strategies, such as nucleus sampling  and beam search .

Essentially, VCD serves as a corrective mechanism, reducing hallucinations by contrasting against a distribution predisposed to favoring them. Alternatively, VCD can also be interpreted as a form of contrastive ensemble that differentiates between the logits of $`p_\theta\left(y \mid v, x\right)`$ and $`p_\theta\left(y \mid v', x\right)`$. This method echoes the contrastive objective commonly employed in image generation. For instance, classifier-free diffusion models estimate diffusion noise using $`(1+\alpha)\epsilon_\theta(x,c)-\alpha\epsilon_\theta(x)`$, where $`c`$ serves as a controlling factor. In the realm of text generation, several studies have also exploited contrastive decoding for more faithful generation .

![](../images/VCD_md_images/figs/bias_.pdf.png)

The left subfigure shows the correlation between frequent objects in MSCOCO and their propensity to be hallucinated in the validation set. Objects with a higher occurrence rate in the dataset are more likely to be hallucinated by LVLMs under distorted visual scenarios. The right subfigure charts three objects that often appear alongside "<em>dining table</em>", where they are also more frequently hallucinated when presented with distorted visual inputs.

### Adaptive Plausibility Constraints

According to the formation of the contrastive distribution $`p_{vcd}`$ in Equation <a href="#eq:3" data-reference-type="ref" data-reference="eq:3"></a>, a challenge may arise as it penalizes the model’s entire output behaviors influenced by distorted visual inputs. However, this is not universally correct – the output distributions with distorted visual inputs can still uphold fundamental linguistic standards and common sense reasoning. Indiscriminate penalization could inaccurately punish these valid outputs and promote the generation of implausible tokens. To address this issue, we follow to implement an adaptive plausibility constraint that is contingent upon the confidence level associated with the output distribution with original visual inputs:
$$
\begin{equation} \label{eq:5} \begin{gathered} \begin{aligned} & \mathcal{V}_{\text {head }}\left(y_{<t}\right)= \{y_t \in \mathcal{V}:  \\ &p_{\theta}\left(y_t \mid v,x,y_{<t}\right) \geq \beta \max _w p_{\theta}\left(w \mid v,x,y_{<t}\right)\}, \end{aligned} \\ \begin{aligned} p_{vcd}\left(y_t \mid v, v', x\right) = 0, \text{ if } y_t \notin \mathcal{V}_{\text {head }}\left(y_{<t}\right), \end{aligned} % \begin{aligned} % & \log p_{vcd}\left(y \mid v, v', x\right) \\ % & = \begin{cases}\log \frac{\left(1+\alpha\right) \cdot p_\theta\left(y \mid v, x\right) }{\alpha \cdot p_\theta\left(y \mid v', x\right)}, & \text { if } y_i \in \mathcal{V}_{\text {head }}\left(y_{<i}\right), \\ % -\inf , & \text { otherwise. }\end{cases} % \end{aligned} \end{gathered} \end{equation}
$$
where $`\mathcal{V}`$ is the output vocabulary of LVLMs and $`\beta`$ is a hyperparameter in $`[0,1]`$ for controlling the truncation of the next token distribution. Larger $`\beta`$ indicates more aggressive truncation, keeping only high-probability tokens.

Combining the visual contrastive decoding and the adaptive plausibility constraint, we obtain the full formulation:
$$
\begin{equation} \begin{gathered} y_t \sim \operatorname{softmax}\left[(1+\alpha) \operatorname{logit}_\theta\left(y_t \mid v, x, y_{<t}\right)\right. \\ \left.-\alpha \operatorname{logit}_\theta\left(y_t \mid v', x, y_{<t}\right)\right],\\ {subject \ to} \ y_t \in \mathcal{V}_{\text {head }}\left(y_{<t}\right) \end{gathered} \end{equation}
$$
Incorporating adaptive plausibility constraints refines the contrastive distribution, bolstering confidence in straightforward decisions. This ensures that when the model is highly confident in its outputs associated with the original inputs, the candidate pool is streamlined, often retaining a singular token with high probability. Such an approach effectively neutralizes potential adverse effects of VCD, preventing it from inadvertently promoting the generation of implausible tokens and maintaining the integrity of the generated content.

# Experiments

This section details our assessment of the proposed Visual Contrastive Decoding across various LVLMs.

## Experimental Settings

**Datasets & Evaluation Metrics**

**POPE**, the Polling-based Object Probing Evaluation , presents a streamlined approach to assess object hallucination. Within this benchmark, LVLMs are queried to answer if a specific object exists in the given image. The ratio between queries probing existent objects and non-existent objects is balanced (i.e.,$`50`$% vs. $`50`$%). It encompasses three sampling settings: *random, popular, and adversarial*, each distinct in constructing negative samples. In the *random* setting, objects absent from the image are chosen randomly. The *popular* setting selects missing objects from a high-frequency pool, while in the *adversarial* setting, co-occurring objects not present in the image are prioritized. The POPE benchmark aggregates data from three distinct sources: MSCOCO , A-OKVQA , and GQA . It involves $`500`$ images from each dataset under each sampling setting and formulates $`6`$ questions per image, culminating in a total of $`27,000`$ query-answer pairs from the development sets of these datasets[^4]. The evaluation pivots on four key metrics: Accuracy, Precision, Recall, and the F1 score.

**MME** serves as an extensive benchmark tailored to assess LVLMs across multiple dimensions. It comprises ten perception-related subtasks and four cognition-focused ones. Following , except for adapting the whole dataset, we additionally leverage the existence and count subsets for object-level hallucination evaluation, and the position and color subsets for attribute-level hallucination assessment. Performance is quantified via the combined metric of accuracy and accuracy+ as the official implementation[^5].

**LLaVA-Bench**[^6] features a collection of $`24`$ images, accompanying $`60`$ questions that span a range of contexts including indoor and outdoor scenes, memes, paintings, and sketches. This dataset is crafted to assess the capability of LVLMs in tackling more challenging tasks and their adaptability to new domains. We conduct case studies on this dataset to qualitatively demonstrate the effectiveness of our proposed VCD.

**LVLM Baselines** We evaluate the effectiveness of our VCD on three state-of-the-art LVLMs. Concretely, we apply our VCD to LLaVA-1.5 and InstructBLIP, which employ Vicuna 7B as language decoder , and Qwen-VL, built on top of Qwen 7B backbone . For a more convincing comparison, we report the averaged results as well as the standard deviation over $`5`$ runs on POPE and MME benchmarks.

**Implementation Details** Throughout our experiments, we set $`\alpha = 1`$, $`\beta = 0.1`$, and $`\gamma = 0.1`$ unless explicitly stated otherwise. For a consistent comparative analysis, our baseline decoding strategy employs direct sampling (i.e., denoted as “Regular" in all experimental tables), where the next token is directly sampled from the post-softmax distribution[^7]. Conversely, instances labeled as“VCD" in the decoding column of all experimental tables refer to our proposed Visual Contrastive Decoding strategy, which also directly samples from the modified post-softmax distribution after applying VCD. Comprehensive parameter configurations can be found in Supplementary Materials.

## Experimental Results

![](../images/VCD_md_images/figs/chart1_1_.pdf.png)

MME full set results on LLaVA-1.5. VCD leads to consistent enhancement in LVLMs’ perception capacities while preserving their recognition competencies.

**Results on POPE** Experimental results on POPE under the random, popular, and adversarial settings are summarized in Table <a href="#tab:pope" data-reference-type="ref" data-reference="tab:pope"></a>. A notable observation is the robust effect of our proposed VCD. Specifically, under different sampling settings, the performances of our VCD consistently surpass the baseline results by large margins (up to +5.8 accuracy and +7.4 F1) on all of the LVLMs. This suggests its pivotal role in counteracting statistical biases and language priors in LVLMs, thereby reducing instances of object hallucination. In addition, all LVLMs display a clear performance degradation as we move from the *random* setting to *popular* and experience a further decline while moving to the *adversarial* setting. This trend verifies our hypothesis that statistical biases inherent in LVLMs substantially contribute to the object hallucination problem. In a more detailed model-specific analysis, VCD demonstrates varied effects across different LVLMs. For LLaVA-1.5 and Qwen-VL, the F1 score elevation is predominantly driven by a recall boost (e.g., up to $`10`$ points), showcasing its enhanced ability to accurately detect object presences. Conversely, InstructBLIP’s F1 score improvement is largely due to improved precision, signifying its enhanced capability to accurately filter out false positives. This highlights VCD’s ability to accentuate distinct attributes of various model architectures in binary decision scenarios of POPE.

![](../images/VCD_md_images/figs/case_.pdf.png)

Illustration of hallucination correction by our proposed VCD with two samples from LLaVA-Bench. Hallucinated objects from LVLM’s regular decoding are highlighted in .

**Results on MME Hallucination Subset** The MME subset evaluations extend beyond POPE’s scope, encompassing both object-level and attribute-level hallucinations. Results in Table <a href="#tab:mme" data-reference-type="ref" data-reference="tab:mme"></a> show that implementing VCD leads to a uniform enhancement in addressing object-level hallucinations for all models. Additionally, VCD demonstrates an overall positive impact on attribute-level *Color* scores, contributing to substantial overall performance gains. These improvements emphasize VCD’s strength in addressing the embedded statistical bias and language priors of LVLMs, thus bringing a positive impact on a broader range of hallucination challenges. In contrast, the *Position* score is relatively low across four metrics, with minimal uplift from VCD, suggesting the relatively weak ability of LVLMs in position reasoning.

**Results on MME Full Set** As shown in Figure <a href="#chart:mme" data-reference-type="ref" data-reference="chart:mme">4</a>, we also include the evaluation of VCD on MME Full Set to assess its impact on the general capability of LVLMs. With all models exhibiting comparable performance trajectories, we present the results of LLaVA-1.5 as a representative[^8]. The implementation of VCD leads to a consistent enhancement in perception-based tasks, while the original recognition competencies of the LVLMs are preserved. This may be attributed to VCD’s reduction of statistical bias and language priors, which improves LVLMs’ general perception capacities by ensuring a visually grounded analysis.

## Further Discussions

![](../images/VCD_md_images/figs/noisy_prior_.pdf.png)

Performance of LLaVA-1.5 on the POPE benchmark across varying noise levels with regular decoding. We visualize the distorted visual inputs subjected to different levels of Gaussian noise at the bottom.

**Effect of Visual Uncertainty on Hallucinations** We further study how the object hallucination of LLaVA-1.5 changes along with visual uncertainty. Figure <a href="#fig: noisy_prior" data-reference-type="ref" data-reference="fig: noisy_prior">6</a> depicts a clear performance drop on the POPE benchmark with the increase of noise steps, suggesting that the object hallucination will become more severe as visual uncertainty goes larger. This observation aligns with our previous findings in Section <a href="#subsec: observation" data-reference-type="ref" data-reference="subsec: observation">3.2</a> that visual uncertainty will exacerbate object hallucination issues in LVLMs’ generative process. Our proposed VCD emerges as a correction mechanism by contrasting model outputs with original and distorted visual inputs.

**GPT-4V Aided Evaluation of Open-Ended Generation** Beyond the “Yes-or-No" question format employed in our POPE and MME evaluations, we extend our analysis to open-ended captioning tasks in the LLaVA-Bench using the recently released LVLM, GPT-4V[^9], following [^10]. Results in Table <a href="#tab:gpt4v" data-reference-type="ref" data-reference="tab:gpt4v"></a> show consistent improvements in VCD over regular decoding. The observed enhancement in accuracy points to VCD’s ability to mitigate hallucinations effectively. Simultaneously, VCD’s counteraction of statistical biases and language priors enhances the perceptual capabilities of LVLMs, as evidenced by the marked improvement in the detailedness of the responses.

**Case Study on LLaVA-Bench** Figure <a href="#fig:case study" data-reference-type="ref" data-reference="fig:case study">5</a> demonstrates two case studies on how, given identical prompts and images, regular decoding can yield object hallucinations influenced by the statistical bias and language priors inherent during pretraining. For instance, in the displayed examples, objects such as “*dining table*" and “*fork*", which often co-occur with the likely ground-truth object “*chair*", are hallucinated. In contrast, the implementation of VCD notably mitigates these hallucination issues and simultaneously preserves the coherence and informativeness of the output text. Due to the page limit, please refer to Supplementary Materials for more cases and ablation studies[^11].

# Conclusion and Limitation

In this paper, we tackle the object hallucination issue in LVLMs. We conducted an in-depth analysis of how visual uncertainty influences hallucinations, particularly from the aspect of statistical biases and language priors. Our findings indicate that visual uncertainty amplifies these factors, contributing to more hallucinations. In light of this, we introduced Visual Contrastive Decoding (VCD), a novel, training-free method that employs contrastive distributions to calibrate the model’s output without the usage of external tools. Our extensive experiments across multiple benchmarks and LVLM families confirm VCD’s efficacy in reducing hallucinations and also demonstrate its potential to enhance the overall perception capabilities of LVLMs.

**Limitation** While this study employs a basic Gaussian noise approach to introduce visual uncertainty, more fine-grained techniques, like object-level blurring, hold the potential for improved outcomes. In addition, our focus was limited to LVLMs processing images and text, not encompassing their emerging applications in video understanding. Future research directions include exploring diverse image distortion methods and extending the Visual Contrastive Decoding (VCD) framework to a broader range of LVLMs.

# Detailed Experimental Settings

In all experimental setups, the hyper-parameters $`\gamma`$, $`\alpha`$ and $`\beta`$, as specified in Equations <a href="#eq:1" data-reference-type="ref" data-reference="eq:1"></a>, <a href="#eq:3" data-reference-type="ref" data-reference="eq:3"></a> and <a href="#eq:5" data-reference-type="ref" data-reference="eq:5"></a>, are fixed at values of $`0.1`$, $`1`$ and $`0.1`$, respectively. For the total number of noise steps $`T`$ delineated in Equation <a href="#eq:1" data-reference-type="ref" data-reference="eq:1"></a>, we set a value of $`500`$ for experiments involving the MME and LLaVA-Bench, while for those evaluating on POPE, the $`T`$ value is set at $`999`$.

# Ablation Studies

For the Ablation Studies section, the default configuration for hyper-parameters $`\alpha`$, $`\beta`$, and $`\delta`$ is set to $`1`$, $`0.1`$, and $`500`$, respectively. These values are retained across all experiments unless an individual study specifies an alternative parameter adjustment for investigation. Across all the experiments, we use LLaVA-1.5 as the representative LVLM baseline to demonstrate the effect of tuning different hyper-parameters.

## Effect of Total Noise Steps $`T`$

Figure <a href="#tab:ablation1" data-reference-type="ref" data-reference="tab:ablation1"></a> presents an ablation study examining the impact of varying noise levels, denoted as $`\delta`$, using the LLaVA-1.5 model on the MME benchmark. In alignment with the experimental configuration, MME is subdivided into three subsets: hallucination, perception, and recognition. The hallucination subset includes tasks related to *Existence*, *Count*, *Position*, and *Color*, while the perception subset encompasses these and additional perception-focused tasks. The recognition subset, conversely, involves tasks that challenge LVLMs’ cognitive reasoning abilities.

The study reveals a pronounced sensitivity to different $`\delta`$ values within the hallucination subset, where optimal noise levels correlate with substantially enhanced overall scores. In the realm of perception tasks, a surpassing of a specific noise threshold ($`\delta > 500`$) showcases VCD’s capability to consistently yield improvements. For recognition tasks, VCD maintains steady performance across the spectrum of tested noise values.

## Effect of $`\alpha`$ in Visual Contrastive Decoding 

Table <a href="#tab:ablation2" data-reference-type="ref" data-reference="tab:ablation2"></a> demonstrates the outcomes of an ablation study focusing on $`\alpha`$, which modulates the level of amplification between output distributions from original and distorted visual inputs, as formulated in Equation <a href="#eq:3" data-reference-type="ref" data-reference="eq:3"></a>. The study observes minimal variance in the aggregate scores across the three MME subsets as $`\alpha`$ ranges from $`0.25`$ to $`1.0`$, showcasing a uniform improvement over regular decoding. This consistency evidences the efficacy and stability of the contrastive decoding strategy across a spectrum of $`\alpha`$ settings.

## Effect of $`\beta`$ in Adaptive Plausible Constraint 

Table <a href="#tab:ablation3" data-reference-type="ref" data-reference="tab:ablation3"></a> presents the results of an ablation study on $`\beta`$, which controls the adaptive plausible constraint in Equation <a href="#eq:5" data-reference-type="ref" data-reference="eq:5"></a>, where larger $`\beta`$ indicates more aggressive truncation, keeping only high-probability tokens. The table illustrates that a $`\beta`$ value of $`0`$, implying no constraint, results in suboptimal performance, which validates our rationale for implementing this constraint: the output distribution with distorted visual inputs can still uphold fundamental linguistic standards and common sense reasoning. Indiscriminate penalization could inadvertently sanction these valid outputs and promote the generation of implausible tokens. As $`\beta`$ increases, improvements in total scores across the hallucination and perception subsets are observed, highlighting the constraint’s critical role in reducing hallucinations and improving LVLMs’ perception capacities.

## Effect of Different Sampling Strategies

<thead> <tr> <th style="text-align: left;">Sampling Strategy</th> <th style="text-align: center;">w. VCD</th> <th style="text-align: center;">Accuracy</th> <th style="text-align: center;">Precision</th> <th style="text-align: center;">Recall</th> <th style="text-align: center;">F1 Score</th> </tr> </thead> <tbody> <tr> <td rowspan="2" style="text-align: left;">Top P</td> <td style="text-align: center;">No</td> <td style="text-align: center;">84.91<sub>±0.25</sub></td> <td style="text-align: center;">94.73<sub>±0.30</sub></td> <td style="text-align: center;">73.93<sub>±0.52</sub></td> <td style="text-align: center;">83.05<sub>±0.32</sub></td> </tr> <tr> <td style="text-align: center;">Yes</td> <td style="text-align: center;"><strong>87.82</strong><sub>±0.66</sub></td> <td style="text-align: center;">91.17<sub>±0.57</sub></td> <td style="text-align: center;">83.76<sub>±0.87</sub></td> <td style="text-align: center;"><strong>87.31</strong><sub>±0.72</sub></td> </tr> <tr> <td rowspan="2" style="text-align: left;">Top K</td> <td style="text-align: center;">No</td> <td style="text-align: center;">83.04<sub>±0.16</sub></td> <td style="text-align: center;">91.84<sub>±0.15</sub></td> <td style="text-align: center;">72.53<sub>±0.44</sub></td> <td style="text-align: center;">81.05<sub>±0.24</sub></td> </tr> <tr> <td style="text-align: center;">Yes</td> <td style="text-align: center;"><strong>87.49</strong><sub>±0.56</sub></td> <td style="text-align: center;">91.09<sub>±0.53</sub></td> <td style="text-align: center;">83.11<sub>±0.71</sub></td> <td style="text-align: center;"><strong>86.92</strong><sub>±0.60</sub></td> </tr> <tr> <td rowspan="2" style="text-align: left;">Greedy</td> <td style="text-align: center;">No</td> <td style="text-align: center;">87.10<sub>±0.00</sub></td> <td style="text-align: center;">97.33<sub>±0.00</sub></td> <td style="text-align: center;">76.29<sub>±0.00</sub></td> <td style="text-align: center;">85.54<sub>±0.00</sub></td> </tr> <tr> <td style="text-align: center;">Yes</td> <td style="text-align: center;"><strong>88.49</strong><sub>±0.28</sub></td> <td style="text-align: center;">91.78<sub>±0.28</sub></td> <td style="text-align: center;">84.56<sub>±0.44</sub></td> <td style="text-align: center;"><strong>88.02</strong><sub>±0.30</sub></td> </tr> <tr> <td rowspan="2" style="text-align: left;"> <tbody> <tr> <td style="text-align: left;">Top K+Temperature 0.7</td> </tr> </tbody> </td> <td style="text-align: center;">No</td> <td style="text-align: center;">85.17<sub>±0.12</sub></td> <td style="text-align: center;">94.82<sub>±0.12</sub></td> <td style="text-align: center;">74.40<sub>±0.35</sub></td> <td style="text-align: center;">83.38<sub>±0.17</sub></td> </tr> <tr> <td style="text-align: center;">Yes</td> <td style="text-align: center;"><strong>87.94</strong><sub>±0.51</sub></td> <td style="text-align: center;">91.21<sub>±0.49</sub></td> <td style="text-align: center;">83.98<sub>±0.60</sub></td> <td style="text-align: center;"><strong>87.45</strong><sub>±0.54</sub></td> </tr> <tr> <td rowspan="2" style="text-align: left;"> <tbody> <tr> <td style="text-align: left;">Top K+Temperature 1.5</td> </tr> </tbody> </td> <td style="text-align: center;">No</td> <td style="text-align: center;">79.28<sub>±0.22</sub></td> <td style="text-align: center;">86.48<sub>±1.12</sub></td> <td style="text-align: center;">69.42<sub>±0.91</sub></td> <td style="text-align: center;">77.01<sub>±0.22</sub></td> </tr> <tr> <td style="text-align: center;">Yes</td> <td style="text-align: center;"><strong>86.97</strong><sub>±0.50</sub></td> <td style="text-align: center;">90.96<sub>±0.64</sub></td> <td style="text-align: center;">82.09<sub>±0.41</sub></td> <td style="text-align: center;"><strong>86.30</strong><sub>±0.51</sub></td> </tr> </tbody>

Table <a href="#tab:ablation4" data-reference-type="ref" data-reference="tab:ablation4"></a> presents an ablation study on various sampling strategies conducted on the POPE-*Random* dataset using LLaVA-1.5. In addition to the direct sampling approach discussed in the main paper, this experiment includes four additional sampling strategies: Top P sampling (specifically, $`p=0.9`$), Top K sampling (specifically, $`k=50`$), Greedy decoding, and Top K sampling with temperature normalization ($`k=50, temp=1.5/0.7`$). The results indicate that applying VCD, irrespective of the sampling strategy employed, consistently contributes to hallucination mitigation and an enhancement of the general performance capabilities of LVLMs. This consistency underscores the versatility and effectiveness of VCD across different sampling strategies in the context of LVLMs.

## Effect of VCD when LVLMs Scale Up

Our evaluation extends to larger 13B variants of the LLaVA-1.5 and InstructBLIP models[^12], assessing the scalability of our proposed VCD across different LVLM magnitudes. Table <a href="#tab: pope_upscale" data-reference-type="ref" data-reference="tab: pope_upscale"></a> reveals that the 7B and 13B variants of LLaVA-1.5 and InstructBLIP exhibit comparable performances across POPE settings (e.g., $`81.33`$ and $`81.49`$ F1 scores for LLaVA-1.5 7B and 13B in *Random* setting), suggesting that increasing the model parameters does not inherently resolve hallucination issues, thereby underscoring the pertinence of addressing this challenge. Crucially, VCD consistently boosts performance in all POPE configurations, reaffirming its robustness independent of model scale.

# Detailed Experimental Results on MME

In Table <a href="#tab:mme_perception" data-reference-type="ref" data-reference="tab:mme_perception"></a>, we present the performance of three LVLM baselines on the perception-related tasks of the MME benchmark. The baselines exhibit consistent performance patterns, and the deployment of VCD uniformly improves their perceptual competencies. This improvement is likely a consequence of VCD’s capability to diminish statistical biases and language priors, thus recalibrating the LVLMs to favor visual information over pre-existing biases and priors.

<div class="tabular">

@llllll\|l@ Model & Decoding & & & & & & Regular & $`106.43_{\pm 9.04}`$ & $`\textbf{72.50}_{\pm 15.51}`$ & $`\textbf{95.50}_{\pm 12.80}`$ & $`78.50_{\pm 22.12}`$ & $`352.93_{\pm 27.98}`$ & VCD & $`\textbf{111.29}_{\pm 7.06}`$ & $`68.50_{\pm 16.64}`$ & $`89.50_{\pm 5.97}`$ & $`\textbf{84.00}_{\pm 25.35}`$ & $`\textbf{353.29}_{\pm 36.19}`$ & Regular & $`109.86_{\pm 10.31}`$ & $`\textbf{60.00}_{\pm 6.37}`$ & $`83.00_{\pm 11.91}`$ & $`\textbf{67.50}_{\pm 10.16}`$ & $`\textbf{320.36}_{\pm 26.00}`$ & VCD & $`\textbf{114.39}_{\pm 5.83}`$ & $`54.00_{\pm 9.62}`$ & $`\textbf{85.00}_{\pm 7.29}`$ & $`64.50_{\pm 7.37}`$ & $`317.89_{\pm 11.59}`$ & Regular & $`79.57_{\pm 6.81}`$ & $`62.86_{\pm 11.23}`$ & $`55.00_{\pm 10.75}`$ & $`70.00_{\pm 10.75}`$ & $`267.43_{\pm 10.42}`$ & VCD & $`\textbf{109.71}_{\pm 7.31}`$ & $`\textbf{66.00}_{\pm 16.45}`$ & $`\textbf{69.00}_{\pm 11.54}`$ & $`\textbf{74.50}_{\pm 20.26}`$ & $`\textbf{319.21}_{\pm 20.60}`$

</div>

Furthermore, Table <a href="#tab:mme_recognition" data-reference-type="ref" data-reference="tab:mme_recognition"></a> showcases the LVLMs’ performances on recognition-related tasks within the MME benchmark. The results indicate that the application of VCD, while alleviating hallucination issues and augmenting perceptual capabilities, does not compromise the inherent reasoning abilities of LVLMs, as evidenced by the stable overall recognition scores.

# More Case Studies

![](../images/VCD_md_images/figs/case_hallu_.pdf.png)

More examples from LLaVA-Bench of our proposed VCD for hallucination corrections. Hallucinated objects from LVLM’s regular decoding are highlighted in .

![](../images/VCD_md_images/figs/case_general_.pdf.png)

More examples from LLaVA-Bench of our proposed VCD for enhanced general perception and recognition capacities.

Additional case studies on the LLaVA-bench are presented to illustrate the effectiveness of our approach across different LVLMs. Figure <a href="#fig:case_hallu" data-reference-type="ref" data-reference="fig:case_hallu">7</a> provides further instances of hallucination corrections by our method. Meanwhile, Figure <a href="#fig:case_general" data-reference-type="ref" data-reference="fig:case_general">8</a> offers supplemental examples of the enhancements brought by our proposed VCD in bolstering the general perception and recognition abilities of LVLMs.

<div class="minipage">

<div class="tcolorbox">

|  |
|:---|
|  |
| **Description:** |
| AI that scores image description accuracy and detailedness. |
| **Instructions:** |
| You are an AI designed to evaluate and score the performance of two AI assistants in describing a given image. Your primary focus is on the accuracy and detailedness of their descriptions. You will assess the accuracy by checking for hallucinations - any part of the description that is inconsistent with the image content. For detailedness, you will consider how rich the response is in necessary details, excluding any hallucinated parts. You will provide scores on a scale from 1 to 10 for each assistant separately, based on these criteria. After scoring, you will offer an explanation for your evaluation, ensuring it is free from bias and not influenced by the order of presentation of the responses. |
|  |
| Input format: |
|  |
| Assistant 1 |
| {Response 1} |
| End of Assistant 1 |
|  |
| Assistant 2 |
| {Response 2} |
| End of Assistant 2 |
|  |
| Output format: |
|  |
| Accuracy: |
| Scores of the two answers: |
| Reason: |
|  |
| Detailedness: |
| Scores of the two answers: |
| Reason: |
|  |

</div>

</div>

![](../images/VCD_md_images/figs/gpt4_evaluator_case_.pdf.png)

Case illustrating the evaluation of GPT-4V in open-ended generation task. “Assistant 1” and “Assistant 2” correspond to “visual contrastive decoding” and “regular decoding”.

# Prompt and Case for GPT-4V Aided Evaluation

To evaluate open-ended generation, we utilize GPT-4V to assess the accuracy and detailedness of LVLMs’ responses. The specific configurations are detailed in Table <a href="#tab:prompt_evaluation" data-reference-type="ref" data-reference="tab:prompt_evaluation"></a>. Additionally, an illustrative evaluation case is presented in Figure <a href="#fig: gpt4_evaluator_case" data-reference-type="ref" data-reference="fig: gpt4_evaluator_case">9</a>.

[^1]: Equal contribution. Sicong Leng is under the joint PhD program between Alibaba and NTU.

[^2]: Correspondence: `xinting.lx@alibaba-inc.com`.

[^3]: <https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild>

[^4]: Given the absence of ground-truth object annotations in A-OKVQA and GQA, SEEM  is applied for image segmentation and object identification.

[^5]: <https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models/tree/Evaluation>

[^6]: <https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild>

[^7]: Optimization of $`\alpha`$, $`\beta`$, $`T`$, and applying other sampling strategies as detailed in the ablation studies in Supplementary Materials may yield better results. The current settings serve as a constant baseline to demonstrate the efficacy of our approach.

[^8]: Comprehensive results for all three LVLMs on the MME full set are provided in Supplementary Materials.

[^9]: <https://openai.com/research/gpt-4v-system-card>

[^10]: The prompt used for evaluation and an evaluation case is provided in Supplementary Materials.

[^11]: Ablation studies in Supplementary Materials include effects of total noise steps $`T`$, hyper-parameters $`\alpha`$, $`\beta`$, and effect of VCD on larger LVLM variants and with other sampling strategies.

[^12]: Qwen-VL lacks larger variants.
