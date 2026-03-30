

![](../images/Eyes_Wide_Shut_md_images/Figures/fig1_teaser_nohuman.pdf.png)



# Introduction

Multimodal Large Language Models (MLLMs)  have been rapidly developing in recent times. MLLMs integrate images into large language models (LLMs) and leverage the powerful abilities of LLMs , showcasing remarkable proficiency in tasks such as image understanding, visual question answering, and instruction following. In particular, the recently released GPT-4V(ision)  has pushed performance to an unprecedented level .

Beneath the advancements of these models, we find there exists a notable weakness: they still exhibit visual shortcomings, some of which are surprisingly elementary and evident (see Figure ). We ask: *Where do these problems originate? Is it a deficiency in visual modality, language understanding, or their alignment?* In this work, we suggest that these shortcomings observed in MLLMs might stem from a problem related to the **visual representations**.

At their core, most MLLMs  are built on *pretrained* vision  and language  models. These models are connected using various types of adapters  to integrate the different modalities. A natural hypothesis is that any limitation in the pretrained vision models can cascade into the downstream MLLMs that adopt them. Studies have explored a similar issue for language. For example,  demonstrate that failure patterns in the pretrained text encoder  will lead to downstream failures in text-guided generative models .

On the vision side, most open-source MLLMs  adopt the pretrained Contrastive Language-Image Pre-Training (CLIP) model  as the visual encoder. We begin by identifying failure examples that CLIP struggles to encode properly (Section ). Inspired by , we exploit the *erroneous agreements* in the embedding space. If two visually different images are encoded similarly by CLIP, then at least one of the images is likely ambiguously encoded. We call such a pair of images a *CLIP-blind* pair. To measure the visual similarity between images, we use a vision-only self-supervised encoder such as DINOv2 . In this context, *CLIP-blind* pairs are images with similar CLIP embeddings but different DINOv2 embeddings.

We discover that these CLIP-blind pairs indeed lead to errors in downstream MLLMs. With these pairs, We introduce the **M**ulti**M**odal **V**isual **P**atterns (MMVP) benchmark. This benchmark is specifically designed to inquire about differences in CLIP-blind pairs and evaluate the visual abilities of *state-of-the-art* MLLMs with straightforward questions. We evaluate a variety of open-source  and closed-source models  including GPT-4V , and conduct a user study to measure human performance. The results show that MLLM models struggle with straight-forward visual questions. Most of these models perform below the level of random guessing, with GPT-4V being the exception. Yet, even GPT-4V exhibits a considerable disparity in performance – exceeding 50% – compared to human performance.

Having identified a large number of individual failure instances in MLLMs, we continue to study the systematic visual patterns in MMVP which CLIP models struggle (Section ). We summarize nine prevalent patterns of the CLIP-blind pairs in MMVP, such as “orientation”, “counting”, and “viewpoint”, which pose significant challenges for the CLIP vision encoder. Notice that there has been significant and ongoing progress in scaling up both training data and model size for CLIP . We categorize examples from MMVP into visual patterns to systematically assess whether scaling alone can mitigate these challenges. Our findings suggest that 7 out of the 9 identified visual patterns cannot be resolved by any large-scale CLIP-based models, indicating that model/data scaling alone is not sufficient. Moreover, we identify a strong correlation between the visual patterns that challenge CLIP models and the performance of MLLMs. If CLIP struggles with a particular visual pattern, such as “orientation”, MLLMs will likely also fall short. This shows that the CLIP vision encoders could become a bottleneck in such systems.

Finally, we take a step towards improving the visual grounding of MLLMs. Since the visual shortcomings of MLLMs stem from their reliance on the CLIP model, we investigate the impact of integrating vision-centric representations into MLLMs (Section ). Specifically, we explore ways to incorporate a vision-only self-supervised model, such as DINOv2 , to enhance the visual grounding capabilities of MLLMs. We refer to these techniques as Mixture-of-Features (MoF). First, we linearly mix CLIP and DINOv2 features in different ratios, which we refer to as Additive-MoF (A-MoF). This process reveals that DINOv2 features are more effective in visual grounding, though they come at the cost of diminished instruction-following ability. To address this, we introduce Interleaved-MoF (I-MoF) that spatially mixes visual tokens from both CLIP and DINOv2 models. We find that this practice significantly enhances visual grounding while maintaining the instruction-following capabilities.


![](../images/Eyes_Wide_Shut_md_images/Figures/fig2.pdf.png)
<figcaption>Constructing MMVP benchmark via CLIP-blind pairs. <strong>Left:</strong> We start with finding CLIP-blind pairs that have similar CLIP embedding but different DINOv2 embedding. <strong>Center:</strong> We manually inspect the differences between pair-wise images and formulate questions based on the differences in the images. <strong>Right:</strong> We ask MLLMs the question alongside the CLIP-blind pair. The model receives a score only when both questions for the CLIP-blind pair are answered correctly. </figcaption>


# The Multimodal Visual Patterns (MMVP) Benchmark

Currently, the majority of open-source MLLMs  use the *off-the-shelf* CLIP vision encoders to process images. In this section, we begin by identifying CLIP-blind pairs in the CLIP model (Section ). Subsequently, we construct the Multimodal Visual Patterns-MLLM (MMVP-MLLM) benchmark using these CLIP-blind pairs (Section ). We evaluate SOTA MLLMs including GPT-4V on the benchmark (Section ) and find that all the tested models struggle with simple questions on visual details. A visualization of this process is provided in Figure .

## Finding CLIP-blind Pairs

It is challenging to directly find instances (images) that the CLIP vision encoder struggles to encode “properly”. To circumvent this issue, we extend the idea proposed in  to automatically find blind pairs in vision models. The underlying principle is simple: if two images, despite having stark visual differences, are encoded similarly by the CLIP vision encoder, then one of them is likely encoded ambiguously (See Figure  left for example). To measure the visual difference between two images, we examine the images’ representations within a reference model: a vision-only self-supervised model trained without any language guidance, e.g., DINOv2 . These models are shown to capture more visual details and information .

We take the corpus datasets, ImageNet  and LAION-Aesthetics , to collect these CLIP-blind pairs.

For each pair, we compute its CLIP embeddings using CLIP-ViT-L-14  model and their DINOv2 embeddings using DINOv2-ViT-L-14  model. We return pairs such that the cosine similarity exceeds 0.95 for CLIP embeddings and less than 0.6 for DINOv2 embeddings.

## Designing Benchmark from CLIP-blind Pairs

We introduce the Multimodal Visual Patterns (MMVP) benchmark, and a Visual Question Answering (VQA) benchmark. Utilizing the collected CLIP-blind pairs, we carefully design 150 pairs with 300 questions. For each CLIP-blind pair of images, we manually pinpoint the visual details that the CLIP vision encoder overlooks (see the middle of Figure ) and craft questions that probe these visual details, for example “Is the dog facing left or right?” (See the right of Figure  and more examples in Figure ). The primary goal is to determine whether MLLM models would fail when posed with these seemingly basic questions and overlook critical visual details. Hence, the questions are intentionally straightforward and unambiguous.


![](../images/Eyes_Wide_Shut_md_images/Figures/fig3_benchmark_wide_gemini.pdf.png)
<figcaption><strong>Examples of Questions in the MMVP benchmark.</strong> Incorrect answers are shaded in red. A model is considered correct only if it answers both questions in a pair correctly. Both leading closed-source models (GPT-4V, Gemini) and open-source models (LLaVA-1.5, InstructBLIP) fail these simple visual questions. (See Appendix  for all the questions in MMVP benchmark.)</figcaption>


## Benchmark Results

We assess the questions on *SOTA* open-source models (LLaVA-1.5 , InstructBLIP , Mini-GPT4 ) and closed-source models (GPT-4V , Gemini , Bard ) We leave details of how we access the model in Appendix . In our evaluation, each question is queried independently, eliminating any biases from chat histories. We also evaluate human performance through a user study where users are presented with 300 questions in a randomized sequence. For any given pair of images, we consider a pair of images to be correctly answered if both the questions associated with the pair are answered accurately.


![](../images/Eyes_Wide_Shut_md_images/Figures/benchmark_result_gemini.pdf.png)
<figcaption><strong>Benchmark results of current <em>SOTA</em> MLLM models and humans.</strong> We evaluate benchmark questions for current <em>SOTA</em> MLLM models and human performances through user studies. </figcaption>



![](../images/Eyes_Wide_Shut_md_images/Figures/fig5.pdf.png)
<figcaption><strong>Examples from MMVP-VLM</strong>. MMVP-VLM consists of image pairs across nine visual patterns. The examples in the figure are from EVA01 ViT-g-14 model , one of the largest CLIP models that also fails to choose the right image given the text description.</figcaption>


#### Human study confirms questions are straightforward.

As shown in Figure , human participants accurately answer an average of 95.7% of the questions. This high accuracy rate underscores the ease of the questions. More details can be found in Appendix .

#### Current MLLMs struggle with visual details.

As shown in Figure , there is a significant performance gap between human and MLLM models, despite the latter often demonstrating impressive results . Models except GPT-4V and Gemini, scored below random guess level (25%). Most advanced GPT-4V and Gemini also face challenges in addressing basic visual grounding questions. Figures  and  provide examples of errors made by models. The outcomes suggest that irrespective of model size or training data, struggle with visual details.

We have also conducted an ablation study, such as swapping options and changing notations in the question formulation (see Appendix  for more details), to further confirm that this poor performance stems from visual incapability, not hallucination in the language models.

# Systematic Failures in CLIP

In the previous section, we identify CLIP-blind pairs and use them to find failures in MLLMs. Here, we delve deeper into these pairs to investigate (i) systematic visual patterns emerged from CLIP-blind pairs (Section ), (ii) whether these visual patterns pose challenges for CLIP-based models with massive scaling up (Section ), and (iii) the correlation between failure patterns in CLIP models and those in MLLMs (Section ).

## Visual Patterns in CLIP-blind Pairs

Having identified the CLIP-blind pairs, we summarize systematic visual patterns that the CLIP vision encoders might consistently misinterpret. It is too abstract to directly capture systematic visual patterns in the CLIP-blind pairs. Therefore, we turn to the questions and options from the MMVP benchmark. With these questions, we transform abstract visual patterns in images into clearer, language-based descriptors that are easier to categorize.

In this work, we use GPT-4  to categorize general patterns by prompting it with the following:

We identify 9 visual patterns:

|      |                                         |
|:-----|:----------------------------------------|
| **** | Orientation and Direction               |
| **** | Presence of Specific Features           |
| **** | State and Condition                     |
| **** | Quantity and Count                      |
| **** | Positional and Relational Context       |
| **** | Color and Appearance                    |
| **** | Structural and Physical Characteristics |
| **** | Text                                    |
| **** | Viewpoint and Perspective               |

These visual patterns suggest that CLIP vision encoders overly focus on high-level semantic understanding, overlooking intricate details of the visual world. Full descriptions of the visual patterns can be found in Appendix .

## The MMVP-VLM Benchmark

CLIP-based models have developed rapidly since the introduction in the first paper . We want to test whether these visual patterns still impose challenges to the more recent CLIP models , which significantly scale up in terms of training data and model size. In doing so, we introduce a new benchmark: MMVP-VLM to systematically study if CLIP models handle this visual pattern well.

We distill a subset of questions from the MMVP benchmark into simpler language descriptions and categorize them into visual patterns. To maintain a balanced number of questions for each visual pattern, we add a few questions, if needed, to ensure that each visual pattern is represented by 15 text-image pairs. Examples of pairs are shown in Figure . A pair is deemed correctly answered if the model can accurately match both image-text combinations.

We evaluate MMVP-VLM on a variety of CLIP models . These models vary in aspects like size, training data, and methodology. As evidenced in Table , increasing network size and training data only aids in identifying two visual patterns – “color and appearance” and “state and condition”. The rest of the visual patterns continue to challenge all CLIP-based models. We also find that the ImageNet-1k zero-shot accuracy is not a definitive indicator of a model’s performance regarding visual patterns. This underscores the necessity for additional evaluation metrics, such as MMVP-VLM, to accurately assess the model’s capabilities in areas beyond image classification.

## How CLIP’s Errors Affect MLLMs


![](../images/Eyes_Wide_Shut_md_images/Figures/correlation_with_gemini.pdf.png)
<figcaption><strong>CLIP and MLLM’s performance on visual patterns.</strong> If CLIP performs poorly on a visual pattern such as “ <strong></strong> orientation”, MLLMs also underperform on the visual pattern. </figcaption>


After analyzing the visual patterns that CLIP models struggle with, we pose the following question: Is there a correlation between the underperformance of CLIP and MLLMs’ visual incapability? To explore this, we categorize questions from MMVP into these visual patterns summarized and calculate each MLLM’s performance on these patterns.

In Figure , we plot CLIP’s performance and MLLMs’ performance for each visual pattern. When the CLIP vision encoder underperforms on a certain visual pattern, the MLLM tends to exhibit similar shortcomings. Open-source models such as LLaVA 1.5  and InstructBLIP  that explicitly use the CLIP vision encoder display a strong correlation in performance.

Further, we calculate the Pearson Correlation Coefficient between the CLIP model and MLLM’s performance on each visual pattern. Results show that LLaVA 1.5 and InstructBLIP all possess a coefficient score greater than 0.7. This high score indicates a strong correlation that weaknesses in visual pattern recognition in the CLIP model are transferred to MLLMs. More details on the Pearson Correlation Coefficient can be found in Appendix .

# Mixture-of-Features (MoF) for MLLM


![](../images/Eyes_Wide_Shut_md_images/Figures/fig7.pdf.png)
<figcaption><strong>Different Mixture-of-Feature (MoF) Strategies in MLLM.</strong> <em>Left</em>: Standard MLLM that uses CLIP as <em>off-the-shelf</em> pretrained vision encoder; <em>Middle</em>: Additive-MoF (A-MoF) MLLM: Linearly mixing CLIP and DINOv2 features before the adapter; <em>Right</em>: Interleaved-MoF (I-MoF MLLM) Spatially interleaving CLIP visual tokens and DINOv2 visual tokens after the adapter. </figcaption>


Based on our exploration in earlier sections, a natural question arises: *If open-sourced MLLM’s visual shortcomings come from the CLIP vision encoder, how do we build a more competent visual encoder?* In this section, we take initial steps to answer the question by studying Mixture-of-Features (MoF). We start with additive MoF that mixes CLIP features and vision-only SSL model features. Results show that each encoder presents unique advantages and limitations when employed as the pretrained model in MLLM (Section ). We subsequently propose Interleaved MoF that integrates the features from both CLIP and SSL into MLLM to enhance visual grounding without compromising the model’s ability to follow instructions (Section ).

## Experiment Setting

We adopt LLaVA  as the framework to study visual encoders in MLLM. LLaVA uses a pretrained CLIP encoder and trains an adapter to align visual tokens with language tokens in the LLM. (See left side of Figure ). We use DINOv2  as the vision-only SSL model in our work because it is currently the most scalable vision-only model. Our exploration includes the use of two visual encoders: CLIP-ViT-L-14 and DINOV2-ViT-L-14 . To ensure consistent and fair comparisons, we train and finetune our model with the same experiment setting in LLaVA. We include the additional experimental details in Appendix .

## Additive MoF

We add a pretrained DINOv2 encoder into MLLM and mix the CLIP pretrained encoder with it. We use a coefficient $`\alpha`$ to control the portion of CLIP features and $`1-\alpha`$ to control the amount of DINOv2 features and *linearly* add them together (See middle part of Figure  for visualization).

We evaluate the model’s visual grounding ability by the MMVP proposed earlier in Section  and the model’s instruction-following capability by LLaVA benchmark introduced in . Initially, we conduct five experiments where we linearly transition from using 100% CLIP features to 100% DINOv2 features. In these tests, the DINOv2 feature proportions are set at $`\{0.00, 0.25, 0.50, 0.75, 1.00\}`$. To further verify the observed trends, we introduce two additional experiments with DINOv2 proportions of $`\{0.625, 0.875\}`$. Our findings, presented in Table , reveal two insights:

1.  As the proportion of DINOv2 features increases, MLLM exhibits a decline in its instruction-following capability. Notably, there is a sharp decrease when the DINOv2 proportion reaches 87.5%.

2.  A higher proportion of DINOv2 features enhances the model’s visual grounding capability, but this advantage diminishes when the DINOv2 proportion surpasses 0.75, at which point instruction-following is notably impaired.

Hence, if we were to add DINOv2 features or completely replace CLIP with DINOv2, it would result in a trade-off between visual grounding and instruction-following. A higher proportion of DINOv2 features improves the model’s visual perception at the expense of its ability to follow linguistic instructions, while CLIP features enhance language comprehension but reduce visual grounding.

## Interleaved MoF

We propose interleaved MoF to leverage advantages from both CLIP and DINOv2 embeddings to enhance image representation. An image concurrently passes into CLIP and DINOv2 encoders, and the resulting embeddings are individually processed by adapters. We take the processed features from CLIP and DINOv2 and interleave them while maintaining their original spatial order. We then feed the interleaved features to LLM (See right part of Figure ).



| method | res | \#tokens | MMVP | LLaVA | POPE |
|:---|:--:|:--:|:---|:---|:---|
| LLaVA | 224$`^2`$ | 256 | 5.5 | 81.8 | 50.0 |
| LLaVA | 336$`^2`$ | 576 | 6.0 | 81.4 | 50.1 |
| LLaVA + I-MoF | 224$`^2`$ | 512 | 16.7**(+10.7)** | 82.8 | 51.0 |
| LLaVA$`^{1.5}`$ | 336$`^2`$ | 576 | 24.7 | 84.7 | 85.9 |
| LLaVA$`^{1.5}`$ + I-MoF | 224$`^2`$ | 512 | 28.0**(+3.3)** | 82.7 | 86.3 |

**Empirical Results of Interleaved MoF.** Interleaved MoF improves visual grounding while maintaining same level of instruction following ability.



We summarize the results in Table . Under the LLaVA setting, interleave MoF significantly enhances visual grounding, with a 10.7% increase observed in MMVP, without compromising the model’s ability to follow instructions. This experiment is replicated with the LLaVA-1.5 setting and under various image resolution settings, yielding similar enhancements in performance. We also evaluate on POPE  which is designed to test hallucination in visual grounding. Interleaved-MoF also shows consistent improvement against the original LLaVA models. Merely increasing the image resolution, and consequently, the number of tokens does not boost visual grounding capabilities. Instead, it is the interleaving of MoF between vision-only SSL models and VLM models that leads to improved performance in visual grounding tasks. We conduct more experiments using MAE or MoCoV3 as vision-only SSL models in I-MoF and show similar improvements in visual grounding tasks in Appenfix . We also evaluated Interleaved MoF on additional benchmarks such as MM-Bench  and GQA , finding that Interleaved MoF achieves similar performance on these benchmarks. Please refer to Appendix for more results on these benchmarks.

# Related Works

**Multimodal LLMs.** We study the limitations of Multimodal LLMs  and explore possible ways to improve these models. Multimodal LLMs build from pretrained Large Language Models  and CLIP vision encoder . These systems then use an adapter, such as MLPs , Q-Former , and gated attention , to integrate the pretrained CLIP vision encoder into LLMs. More recently, instructBLIP , LLaVA-1.5  highlight the importance of high-quality training data. Yet, there is a scarcity of research focusing on the impact of visual encoders, which is an important gap our work aims to address through a systematic study.

**Evaluating Multimodal LLMs.** MMVP assesses MLLMs using a set of simple yet critical Visual Question Answering (VQA) questions constructed from CLIP-blind pairs. Previous benchmarks such as TextVQA , VQAv2 , and GQA  have centered on traditional VQA queries. Recently, there are works like MM-Vet , POPE , and MM-Bench  designed to specifically evaluate multimodal LLMs including hallucination, reasoning, and robustness. The previous benchmarks and evaluations have shown that Multimodal LLMs can suffer from hallucination , catastrophic forgetting  and lack of robustness . In taking a step back to the fundamentals, our work uncovers that even the most advanced multimodal LLMs, such as GPT-4V , Gemini , Bard , and LLaVA-1.5 , are not immune to stumbling over elementary visual questions. We also identified part of the problem as being the incapable visual encoder.

**Visual Encoders.** MMVP-VLM provides a detailed analysis of the visual capabilities of various CLIP variants . These models mostly follow the method proposed in that uses contrastive loss to train on large volumes of image-text pairs. They differ in training data , training recipes , and objective functions . Nonetheless, our studies show that all of these CLIP variants struggle with simple visual patterns such as “orientation”, “count”, “presence of specific features”, . Another line of research focuses on vision-only self-supervised learning (SSL). This category includes contrastive SSL  and mask-based SSL . SLIP  explores the synergy between CLIP and contrastive SSL, but focusing primarily on standard classification tasks. In fact, a common practice to evaluate the quality of these vision models is through linear probing or fine-tuning on ImageNet  . Although current evaluation methods provide a basic level of assessment on representation quality, our findings indicate a growing detachment from the needs of recent use cases. As demonstrated in the MoF experiments in Section , the CLIP vision model and the vision-only SSL models learn complementary features. However, the linear probing accuracy on ImageNet alone provides a limited understanding of feature utility in MLLMs. This observation suggests the need for more diverse evaluations  in visual representation learning, to better align with current and emerging applications.

**Ambiguities in Embedding Models.** Our work exploits CLIP-blind pairs within the CLIP vision embedding space to generate examples of failures in CLIP models and subsequently MLLMs. This concept has ties to previous research focused on documenting failure modes in text embedding models . More recently, , and study the binding problems CLIP faces in processing text queries, noting that CLIP models treat text input as a bag of words. examines the implications for downstream text-guided generative models. suggests image captioners as promising alternatives to CLIP for improving attribute binding. Our work focuses on the visual patterns.

# Discussion

Circling back to the very first question we ask: is vision good enough for language? Perhaps not yet, as our study shows that vision models might become a bottleneck in multimodal systems. MLLMs fail in simple questions because their pre-trained CLIP vision encoders overlook crucial visual details in images, and systematically fail to sort important visual patterns. Yet, CLIP-type models remain the most scalable and widely used vision models today. Contrary to the popular belief that data and model scaling is a panacea, our research demonstrates that scaling alone does not rectify the inherent deficiencies in CLIP models.

Our study reveals that popular visual representation learning models – vision-and-language models and vision-only self-supervised learning models – excel in different aspects. The distinction in their capabilities go beyond conventional benchmarks such as linear probing or zero-shot accuracy on ImageNet. Although a carefully designed Mixture-of-Features approach could alleviate visual limitations and utilize the strengths of these two learning paradigms, it is necessary to develop new evaluation metrics to facilitate the development of new visual representation learning algorithms. We hope our work can motivate further innovation in vision models.

**Acknowledgements.** We thank Penghao Wu, Muzi Tao, Erik Jones, Michael Psenka, Daniel Yeh, Druv Pai, Chen Sun for helpful discussions and feedback. This work was supported in part through the NYU IT High Performance Computing resources, services, and staff expertise. This research is also supported by Intel, Google TRC program, the Google Cloud Research Credits program with the award GCP19980904, and an Amazon Research Award Fall 2023. The authors thank hyperbolic labs for supporting part of the experiments. All experiments and data processing were performed at NYU.

# Experiment Details

#### Hyperparameters.

In this work, we adopt the same set of hyperparameters as LLaVA  and LLaVA-1.5 . We use Vicuna-13b-v1.3  in LLaVA experiments and Vicuna-13b-v1.5  in LLaVA-1.5 experiments. We show the training hyperparameters for LLaVA and LLaVA-1.5 experiments in Table . All experiments are conducted using a maximum of 8 Nvidia A100 GPUs.




<caption>Hyperparameters for MoF training on LLaVA and LLaVA-1.5.</caption>
<tbody>
<tr>
<td rowspan="2" style="text-align: left;">Hyperparameter</td>
<td colspan="2" style="text-align: center;">LLaVA</td>
<td colspan="2" style="text-align: center;">LLaVA-1.5</td>
</tr>
<tr>
<td style="text-align: center;">Stage 1</td>
<td style="text-align: center;">Stage 2</td>
<td style="text-align: center;">Stage 1</td>
<td style="text-align: center;">Stage 2</td>
</tr>
<tr>
<td style="text-align: left;">batch size</td>
<td style="text-align: center;">128</td>
<td style="text-align: center;">128</td>
<td style="text-align: center;">256</td>
<td style="text-align: center;">128</td>
</tr>
<tr>
<td style="text-align: left;">lr</td>
<td style="text-align: center;">1e-3</td>
<td style="text-align: center;">2e-5</td>
<td style="text-align: center;">2e-3</td>
<td style="text-align: center;">2e-5</td>
</tr>
<tr>
<td style="text-align: left;">lr schedule decay</td>
<td style="text-align: center;">cosine</td>
<td style="text-align: center;">cosine</td>
<td style="text-align: center;">cosine</td>
<td style="text-align: center;">cosine</td>
</tr>
<tr>
<td style="text-align: left;">lr warmup ratio</td>
<td style="text-align: center;">0.03</td>
<td style="text-align: center;">0.03</td>
<td style="text-align: center;">0.03</td>
<td style="text-align: center;">0.03</td>
</tr>
<tr>
<td style="text-align: left;">weight decay</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: left;">epoch</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">1</td>
</tr>
<tr>
<td style="text-align: left;">optimizer</td>
<td colspan="4" style="text-align: center;">AdamW </td>
</tr>
<tr>
<td style="text-align: left;">DeepSpeed stage</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">3</td>
</tr>
</tbody>




#### Pretrain Datasets.

We use the same dataset for both LLaVA and LLaVA-1.5 experiments. For LLaVA experiments, stage 1 uses CC595k  and stage 2 uses LLaVA 158k  instruction data; For LLaVA-1.5 experiments, stage 1 uses CC595k  and stage 2 uses DataMix 665k  proposed in .

# MMVP Benchmark

We provide more details on the MMVP benchmark.

## Details of evaluating SOTA models

We access GPT-4V through ChatGPT in October and November 2023. We also evaluate Gemini-Pro through Vertex AI API in December 2023. We use the official checkpoints for InstructBLIP . We access mini-GPT4 ,[^1] LLaVA and LLaVA-1.5  through their playgrounds. We test Bard  using the official website in September and October 2023. Moreover, we test new-Bing through new-Bing chat creative mode and GPT-4V in September 2023.

## Questions in MMVP Benchmark

We present more examples in MMVP at the end in Figures , , .

## Ablation Studies

To further verify that MLLMs make mistakes in MMVP due to their incapable visual grounding instead of hallucination in the language model . We conduct additional ablation experiments on the format and notations of VQA questions and options in MMVP. We choose GPT-4V to do these experiments, as it is currently the best model.

#### Swapping options

The first experiment swaps the two options in the MMVP benchmark. For example, we change the question from “Are the butterfly’s wings closer to being open or closed? (a) Open (b) Closed” to “Are the butterfly’s wings closer to being open or closed? (a) Closed (b) Open”.

Empirically, we find that GPT-4V obtains a 40.3% accuracy on the option swapping in our study, as opposed to the original 38.7%. We observe that a few questions are answered differently, while the majority remain the same. This further suggests that the visual incapabilities are in the vision encoder rather than in alignment or the LLMs.

#### Changing notations in the options

We conducted an ablation study to assess the impact of altering notations. For example, we changed “(a) Closed (b) Open” to “(1) Closed (2) Open”. The results are comparable to the original findings, achieving a performance of 37.3%, closely matching the original 38.7%. The study further suggests that the core challenge in MLLMs is their inherent visual incapability, rather than hallucinations in the language model.

## Human Study Details

In this study, we ask four participants to volunteer in our study. An example user interface for labeling is shown in Figure . We collect their responses and calculate the average score as the human-level performance.


![](../images/Eyes_Wide_Shut_md_images/Figures/user_interface.pdf.png)
<figcaption><strong>Example of user study interface.</strong> The questions in the user study are randomly shuffled to avoid any potential bias. Users choose answers for the VQA questions as well as potential concerns for the VQA question. </figcaption>


# CLIP-MLLM Failure Correlation

#### Correlation between CLIP and MLLM models.

We compute the Pearson Correlation between the CLIP model and MLLMs and show results in Table . Notably, both open-source models – LLaVA and InstructBLIP – exhibit remarkably high Pearson Correlation, exceeding 0.7. This finding indicates a strong correlation between the errors made by the CLIP model and those made by MLLMs. Bard also displays a very high correlation. This suggests that some of the most advanced closed-source models are also affected by the visual limitations in the CLIP models.



|             | LLaVA-1.5 | InstructBLIP | Bard | Gemini | GPT-4 |
|:-----------:|:---------:|:------------:|:----:|:------:|:-----:|
| Correlation |    0.87   |     0.71     | 0.79 |  0.72  | 0.31  |

Pearson Correlation between the CLIP model and MLLMs. Open-source models that explicitly use CLIP-based models are highlighted in gray.



#### Correlation between ImageNet-1k and MMVP performance.

 We plot the ImageNet-1k Zero-shot accuracy against MMVP-VLM average performance in Figure . For models with ImageNet-1k Zero-shot accuracy below 80, a higher Zero-shot accuracy tends to indicate improved MMVP performance. However, in models with superior ImageNet-1k Zero-shot performance, this trend does not necessarily hold for MMVP-VLM accuracy. This distinction accentuates the value of MMVP-VLM as an evaluation metric, which probes into visual patterns such as orientation – aspects that are pivotal for downstream tasks and go beyond what is captured by ImageNet accuracy alone.


![](../images/Eyes_Wide_Shut_md_images/Figures/correlation_in1kmmvp.pdf.png)
<figcaption><strong>Correlation between ImageNet-1k Zero-shot and MMVP-VLM average.</strong> The area of each bubble corresponds to the model’s number of parameters. A higher ImageNet-1k zero-shot performance does not necessarily imply superior performance in MMVP-VLM.</figcaption>


# Visual Patterns for CLIP

Here, we provide the full description of visual patterns that pose challenges to all CLIP-based models.

- **Orientation and Direction**: Questions about the direction something is facing or moving, such as the direction the dog or duck is facing, or the orientation of the school bus.

- **Presence of Specific Features**: Questions that focus on the existence or non-existence of certain elements or features in the image.

-  **State and Condition**: Questions that pertain to the state or condition of an object, such as whether a flag is blowing in the wind or if the ground is wet.

- **Quantity and Count**: Questions about the number of objects or features present in the image.

-  **Positional and Relational Context**: This aspect refers to the model’s ability to understand the position and relationship of objects or elements within an image in relation to each other and their surroundings.

-  **Color and Appearance**: Questions regarding the color of certain objects or elements.

-  **Structural and Physical Characteristics**: This category involves the model’s ability to identify and analyze the physical attributes and structural features of objects in an image.

-  **Text**: Questions related to text or symbols present in the image.

- **Viewpoint and Perspective**: Questions concerning the perspective from which the photo was taken.

# More Benchmark Results

## Different vision-only backbones

Here, we conduct extra experiments to study MoF involving MAE  or MoCoV3  instead of DINOv2; See Table . In Table , we observe that with MAE/MoCov3, there is a consistent improvement in visual grounding ability, as shown in the MMVP and POPE benchmarks.



| method | SSL Model | res | \#tokens | MMVP | POPE |  |
|:---|:--:|:--:|:--:|:---|:---|:---|
| LLaVA$`^{1.5}`$ | None | 336$`^2`$ | 576 | 24.7 | 85.9 |  |
| LLaVA$`^{1.5}`$ + I-MoF | MoCov3 | 224$`^2`$ | 512 | 26.7**(+2.0)** | 86.1 |  |
| LLaVA$`^{1.5}`$ + I-MoF | MAE | 224$`^2`$ | 512 | 27.3**(+2.6)** | 86.1 |  |
| LLaVA$`^{1.5}`$ + I-MoF | DINOv2 | 224$`^2`$ | 512 | 28.0**(+3.3)** | 86.3 |  |

Results of Interleaved MoF with different vision-only SSL model



## Scaling up to larger resolution

We conduct additional experiments on Interleaved-MoF that further scale up the resolution to 336 and evaluate on more benchmarks. The summarized results in Table  reveal that Interleaved-MoF achieves comparable performance on most benchmarks while demonstrating improvements in benchmarks focused on visual grounding. We also observe that MMVP are more sensitive to the model’s visual capabilities, underscoring the significance of our benchmark in assessing visual proficiency.


![](../images/Eyes_Wide_Shut_md_images/Figures/more_examples_I.pdf.png)
<figcaption><strong>More examples of questions in the MMVP benchmark (Part I).</strong></figcaption>



![](../images/Eyes_Wide_Shut_md_images/Figures/more_examples_II.pdf.png)
<figcaption><strong>More examples of questions in the MMVP benchmark (Part II).</strong></figcaption>



![](../images/Eyes_Wide_Shut_md_images/Figures/more_examples_III.pdf.png)
<figcaption><strong>More examples of questions in the MMVP benchmark (Part III).</strong></figcaption>


[^1]: To circumvent response hallucination in mini-GPT4 we prefix our questions with “Please only choose an option to answer the question below without explanation: ”
