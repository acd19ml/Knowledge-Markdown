<a id="fig:teaser"></a>
![](../images/LISA_md_images/figures/fig_teaser12_crop.pdf.png){width="100%"}

**Figure 1.** We unlock new segmentation capabilities for existing multimodal LLMs. Our model, LISA, can deal with cases involving complex reasoning and world knowledge. We also demonstrate explanatory answers in the third row and multiple segmentation masks in a single answer in the fourth row.

# Introduction {#sec:intro}

In daily life, users tend to issue direct commands like "Change the TV channel\" to instruct a robot, rather than providing explicit step-by-step instructions such as "Go to the table first, find the TV remote, and then press the button to change the channel.\" However, existing perception systems consistently rely on humans to explicitly indicate target objects or pre-define categories before executing visual recognition tasks. These systems cannot actively reason and comprehend user intention based on implicit instruction. This reasoning ability is crucial in developing next-generation intelligent perception systems and holds substantial potential for industrial applications, particularly in robotics.

In this work, we introduce a new segmentation task --- *reasoning segmentation*, which requires generating a binary segmentation mask based on an implicit query text involving *complex reasoning*. Notably, the query text is not limited to a straightforward reference (e.g., "the orange\"), but a more complicated description involving *complex reasoning* or *world knowledge* (e.g., "the food with high Vitamin C\"). To accomplish this task, the model must possess two key abilities: 1) reasoning *complex* and *implicit* text queries jointly with the image; 2) producing segmentation masks.

Inspired by the exceptional capacity of LLMs to reason and comprehend user intentions, we aim to leverage this capability of LLMs to address the aforementioned first challenge. However, while several studies [@alayrac2022flamingo; @li2023blip; @ye2023mplug; @li2023otter; @liu2023visual; @zhu2023minigpt; @liu2023improved] have integrated robust reasoning capabilities into multimodal LLMs to accommodate visual input, the majority of these models primarily concentrate on text generation tasks and still fall short in performing vision tasks that require fine-grained output formats, such as segmentation masks. This leads us to ask: can we enable multimodal LLMs with the capability to output segmentation masks?

To this end, we introduce LISA: a large **L**anguage **I**nstructed **S**egmentation **A**ssistant, a multimodal LLM capable of producing segmentation masks. Specifically, we incorporate an additional token, i.e., `<SEG>`, into the existing vocabulary. Upon generating the `<SEG>` token, its hidden embedding is further decoded into the corresponding segmentation mask. By representing the segmentation mask as an embedding, LISA acquires segmentation capabilities and benefits from end-to-end training. Remarkably, LISA demonstrates robust zero-shot abilities. Training the model solely on standard semantic segmentation and referring segmentation datasets yields surprisingly effective performance on the reasoning segmentation task. Furthermore, we find that LISA's performance can be significantly enhanced by fine-tuning on just 239 reasoning segmentation data samples. As illustrated in Figure 1, LISA can handle various scenarios involving complex reasoning and world knowledge.

In addition, to validate the effectiveness, we establish a benchmark for reasoning segmentation evaluation, called *ReasonSeg*. Comprising over one thousand image-instruction pairs, this benchmark offers persuasive evaluation metrics for the task. To align more closely with practical applications, we annotate the images from OpenImages [@OpenImages] and ScanNetv2 [@dai2017scannet] with implicit text queries that involve complex reasoning.

In summary, our contributions are as follows:

- We introduce the *reasoning segmentation* task, which necessitates reasoning based on implicit human instructions. Such reasoning capability is crucial for building a genuinely intelligent perception system.

- We present our model --- LISA, which incorporates new segmentation capabilities. It demonstrates robust zero-shot ability on the reasoning segmentation task when trained solely on reasoning-free datasets, and achieves further performance boost by fine-tuning on just 239 data samples that involve reasoning.

- We establish a reasoning segmentation benchmark, *ReasonSeg*, containing over one thousand image-instruction-mask data samples. This benchmark is essential for evaluation and encourages the community to further explore the reasoning ability for vision tasks.

<a id="fig:benchmark"></a>
![](../images/LISA_md_images/figures/fig_benchmark_v3_crop.pdf.png){width="88%"}

**Figure 2.** Examples of the annotated image-instruction-mask data samples. Left: short phrase query. Right: long sentence query.

# Related Work

## Image Segmentation

Semantic segmentation aims to assign a class label to every pixel in an image. Numerous studies [@fcn; @deconvnet; @segnet; @unet; @deeplab; @dilation; @parsenet; @pspnet; @icnet; @denseaspp; @danet; @ccnet; @psanet; @asymmetric_nonlocal; @cheng2021per; @lai2021semi; @tian2022adaptive; @tian2023learning] have proposed diverse designs (such as encoder-decoder, dilated convolution, pyramid pooling module, non-local operator, and more) to effectively encode semantic information. Research on instance segmentation [@he2017mask; @zhang2021k; @cheng2022masked] and panoptic segmentation [@kirillov2019panoptic; @xiong2019upsnet; @cheng2020panoptic; @li2021fully] has introduced various architectural innovations for instance-level segmentation, including DETR [@carion2020end]-based structures, mask attention, and dynamic convolution. In recent years, typical segmentation tasks have made significant progress and become increasingly mature. Consequently, it is imperative to develop more intelligent interaction ways for image segmentation.

The referring segmentation task [@kazemzadeh2014referitgame; @nagaraja2016modeling] enables interaction with human language, aiming to segment the target object based on a given explicit text description. Recently, @kirillov2023segment introduced SAM, trained with billions of high-quality masks, supporting bounding boxes and points as prompts while demonstrating exceptional segmentation quality. X-Decoder [@zou2023generalized] bridges vision and language, unifying multiple tasks within a single model. SEEM [@zou2023segment] further supports various human interaction methods, including text, audio, and scribble. However, these studies primarily focus on addressing multi-task compatibility and unification, neglecting the injection of new capabilities. In this work, we present LISA and it possesses reasoning ability that has not been explored yet in existing segmentors.

## Multimodal Large Language Model

Motivated by the remarkable reasoning abilities of LLMs, researchers are exploring ways to transfer these capabilities into the vision domain, developing multimodal LLMs. Flamingo [@alayrac2022flamingo] employs a cross-attention structure to attend to visual contexts, enabling visual in-context learning. Models such as BLIP-2 [@li2023blip] and mPLUG-OWL [@ye2023mplug] propose encoding image features with a visual encoder, which are then fed into the LLM alongside text embeddings. Otter [@li2023otter] further incorporates robust few-shot capabilities through in-context instruction tuning on the proposed MIMIC-IT dataset. LLaVA [@liu2023visual] and MiniGPT-4 [@zhu2023minigpt] first conduct image-text feature alignment followed by instruction tuning. @koh2023grounding also investigates image retrieval for LLMs. Moreover, numerous works [@wu2023visual; @yang2023mm; @shen2023hugginggpt; @liu2023internchat; @yang2023gpt4tools] utilize prompt engineering, connecting independent modules via API calls, but without the benefits of end-to-end training. Recently, there have been studies examining the intersection between multimodal LLMs and vision tasks. VisionLLM [@wang2023visionllm] offers a flexible interaction interface for multiple vision-centric tasks through instruction tuning but fails to fully exploit LLMs for complex reasoning. Kosmos-2 [@peng2023kosmos] constructs large-scale data of grounded image-text pairs, infusing grounding capabilities into LLMs. DetGPT [@detgpt] bridges the fixed multimodal LLM and open-vocabulary detector, enabling detection to be performed based on user instruction. GPT4RoI [@zhang2023gpt4roi] introduces spatial boxes as input and trains the model on region-text pairs. In contrast, our work aims to efficiently inject segmentation capabilities into multimodal LLMs in the manner of end-to-end training.

# Reasoning Segmentation 

## Problem Definition

The reasoning segmentation task is to output a binary segmentation mask $\mathbf{M}$, given an input image $\mathbf{x}_{img}$ and an implicit query text instruction $\mathbf{x}_{txt}$. The task shares a similar formulation with the referring segmentation task [@kazemzadeh2014referitgame], but is far more challenging. The key distinction lies in the complexity of the query text in reasoning segmentation. Instead of a straightforward phrase (e.g., "the trash can\"), the query text includes more intricate expressions (e.g., "something that the garbage should be put into\") or longer sentences (e.g., "After cooking, consuming food, and preparing for food, where can we throw away the rest of the food and scraps?\") that involve complex reasoning or world knowledge.

## Benchmark

Given the lack of quantitative evaluation, it is imperative to establish a benchmark for the reasoning segmentation task. To ensure reliable assessment, we have collected a diverse set of images from OpenImages [@OpenImages] and ScanNetv2 [@dai2017scannet], annotating them with implicit text instructions and high-quality target masks. To cover different scenarios, our text instructions consist of two types: 1) short phrases; 2) long sentences; as illustrated in Figure 2. The resulting *ReasonSeg* benchmark comprises a total of 1218 image-instruction-mask data samples. This dataset is further partitioned into three splits: `train`, `val`, and `test`, containing 239, 200, and 779 data samples, respectively. As the primary purpose of the benchmark is evaluation, the validation and testing sets include a larger number of data samples. The details of data annotation are given in the supplementary material.

<a id="fig:overview"></a>
![](../images/LISA_md_images/figures/fig_overview_v7_crop.pdf.png){width="98%"}

**Figure 3.** The pipeline of LISA. Given the input image and text query, the multimodal LLM generates text output. The last-layer embedding for the `<SEG>` token is then decoded into the segmentation mask via the decoder. We use LoRA for efficient fine-tuning. The choice of vision backbone can be flexible, such as SAM or Mask2Former.

# Our Method

In this section, we first introduce the model architecture in Section 4.1. After that, we elaborate on the training data preparation and training parameters in Section 4.2.

## Architecture {#method:arch}

#### Embedding as Mask. 

Most current multimodal LLMs (such as LLaVA [@liu2023visual], Flamingo [@alayrac2022flamingo], BLIP-2 [@li2023blip], Otter [@li2023otter], etc.) support image and text as input, but they can only output text and cannot directly output fine-grained segmentation masks. VisionLLM [@wang2023visionllm] offers a solution by parsing segmentation masks as sequences of polygons, enabling the representation of segmentation masks as plain text and allowing end-to-end training within the framework of existing multimodal LLMs. However, end-to-end training with the polygon sequences introduces optimization challenges and may compromise generalization ability unless a massive amount of data and computational resources are employed. For instance, training a 7B model, VisionLLM requires $4\times 8$ NVIDIA 80G A100 GPUs and 50 epochs, which is computationally prohibitive. In contrast, it takes less than 3 days to train LISA-7B on 8 NVIDIA 24G 3090 GPUs.

To this end, we propose the embedding-as-mask paradigm to infuse new segmentation capabilities into the multimodal LLM. The pipeline of our method is illustrated in Figure 3. Specifically, we first expand the original LLM vocabulary with a new token, i.e., `<SEG>`, which signifies the request for the segmentation output. Given a text instruction $\mathbf{x}_{txt}$ along with the input image $\mathbf{x}_{img}$, we feed them into the multimodal LLM $\mathcal{F}$, which in turn outputs a text response $\hat{\mathbf{y}}_{txt}$. It can be formulated as $$\begin{align}
\begin{aligned}
    \hat{\mathbf{y}}_{txt} = & \;  \mathcal{F}(\mathbf{x}_{img}, \mathbf{x}_{txt}).
\end{aligned}
\end{align}$$

When the LLM intends to generate a binary segmentation mask, the output $\hat{\mathbf{y}}_{txt}$ would include a `<SEG>` token. We then extract the LLM last-layer embedding $\tilde{\mathbf{h}}_{seg}$ corresponding to the `<SEG>` token and apply an MLP projection layer $\gamma$ to obtain $\mathbf{h}_{seg}$. Simultaneously, the vision backbone $\mathcal{F}_{enc}$ extracts the dense visual features $\mathbf{f}$ from the visual input $\mathbf{x}_{img}$. Finally, $\mathbf{h}_{seg}$ and $\mathbf{f}$ are fed to the decoder $\mathcal{F}_{dec}$ to produce the final segmentation mask $\hat{\mathbf{M}}$. The detailed structure of the decoder $\mathcal{F}_{dec}$ follows [@kirillov2023segment]. The process can be formulated as $$\begin{align}
\begin{aligned}
    \mathbf{h}_{seg} = \gamma(\tilde{\mathbf{h}}_{seg} &), \quad \mathbf{f} = \mathcal{F}_{enc}(\mathbf{x}_{img}), \\
    \hat{\mathbf{M}} = & \; \mathcal{F}_{dec}(\mathbf{h}_{seg}, \mathbf{f}).
\end{aligned}
\end{align}$$

#### Training Objectives. 

The model is trained end-to-end using the text generation loss $\mathcal{L}_{txt}$ and the segmentation mask loss $\mathcal{L}_{mask}$. The overall objective $\mathcal{L}$ is the weighted sum of these losses, determined by $\lambda_{txt}$ and $\lambda_{mask}$: $$\begin{equation}
    \mathcal{L} = \lambda_{txt} \mathcal{L}_{txt} + \lambda_{mask} \mathcal{L}_{mask}.
\end{equation}$$ Specifically, $\mathcal{L}_{txt}$ is the auto-regressive cross-entropy loss for text generation, and $\mathcal{L}_{mask}$ is the mask loss, which encourages the model to produce high-quality segmentation results. To compute $\mathcal{L}_{mask}$, we employ a combination of per-pixel binary cross-entropy (BCE) loss and DICE loss, with corresponding loss weights $\lambda_{bce}$ and $\lambda_{dice}$. Given the ground-truth targets $\mathbf{y}_{txt}$ and $\mathbf{M}$, these losses can be formulated as $$\begin{align}
\begin{aligned}
    \mathcal{L}_{txt} & = \mathbf{CE}(\hat{\mathbf{y}}_{txt}, \mathbf{y}_{txt}), \\
    \mathcal{L}_{mask} = \lambda_{bce} \mathbf{BCE}&(\hat{\mathbf{M}}, \mathbf{M})  + \lambda_{dice}\mathbf{DICE}(\hat{\mathbf{M}}, \mathbf{M}).
\end{aligned}
\end{align}$$

It is noteworthy that the proposed method endows existing multimodal LLMs with new segmentation capabilities, such that they can generate not only text but also fine-grained output formats. Also, our method is based on an end-to-end training pipeline and connects the LLM and vision modules with hidden embedding representation, which proves significantly more effective than the decoupled two-stage method as discussed in Section 5.2.

<a id="fig:data"></a>
![](../images/LISA_md_images/figures/fig_data_v3_crop.pdf.png){width="100%"}

**Figure 4.** Illustration of training data formulation from different types of data, including semantic segmentation data, referring segmentation data, and visual question answering data.

## Training {#method:training}

#### Training Data Formulation. 

As illustrated in Figure 4, our training data comprises mainly three parts, all of which are derived from widely-used public datasets. The details are as follows:

- *Semantic Segmentation Dataset.* Semantic segmentation datasets typically consist of images and the corresponding multi-class labels. During training, we randomly choose several categories for each image. To generate data that matches the format of visual question answering, we employ a question-answer template like "**`USER`**: `<IMAGE>` `Can you segment the` `{class_name}` `in this image?` **`ASSISTANT`**: `It is` `<SEG>`.\", where `{class_name}` is the chosen category, and `<IMAGE>` denotes the placeholder for tokens of image patches. The corresponding binary segmentation mask is used as the ground truth to provide mask loss supervision. During training, we also use other templates to generate the QA data to ensure data diversity, as shown in the supplementary material. We adopt ADE20K, COCO-Stuff, and LVIS-PACO part segmentation datasets.

- *Vanilla Referring Segmentation Dataset.* Referring segmentation datasets provide an input image and an explicit short description of the target object. Thus, it is easy to convert them into question-answer pairs using a template like "**`USER`**: `<IMAGE>` `Can you segment` `{description}` `in this image?` **`ASSISTANT`**: `Sure, it is` `<SEG>`.\", where `{description}` is the given explicit description. For this part, we adopt refCOCO, refCOCO+, refCOCOg, and refCLEF datasets.

- *Visual Question Answering Dataset.* To preserve the original Visual Question Answering (VQA) ability of the multimodal LLM, we also include the VQA dataset during training. We use LLaVA-Instruct-150k [@liu2023visual] for LLaVA v1 and LLaVA-v1.5-mix665k for LLaVA v1.5 [@liu2023improved].

Notably, the above datasets do not include any reasoning segmentation data sample. Instead, it only contains samples where the target objects are explicitly indicated in the query texts. Surprisingly, even without complex reasoning training data, LISA demonstrates impressive zero-shot ability on the *ReasonSeg* benchmark, as shown in Table 1. Moreover, we find that further performance boost could be yielded by finetuning the model on only 239 data samples that involve complex reasoning.

<a id="table:reason_seg"></a>
**Table 1.** Reasoning segmentation results on the ReasonSeg benchmark.

| Method | Val gIoU | Val cIoU | Test Short gIoU | Test Short cIoU | Test Long gIoU | Test Long cIoU | Test Overall gIoU | Test Overall cIoU |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVSeg [@liang2023open] | 28.5 | 18.6 | 18.0 | 15.5 | 28.7 | 22.5 | 26.1 | 20.8 |
| GRES [@liu2023gres] | 22.4 | 19.9 | 17.6 | 15.0 | 22.6 | 23.8 | 21.3 | 22.0 |
| X-Decoder [@zou2023generalized] | 22.6 | 17.9 | 20.4 | 11.6 | 22.2 | 17.5 | 21.7 | 16.3 |
| SEEM [@zou2023segment] | 25.5 | 21.2 | 20.1 | 11.5 | 25.6 | 20.8 | 24.3 | 18.7 |
| Grounded-SAM [@liu2023grounding] | 26.0 | 14.5 | 17.8 | 10.8 | 22.4 | 18.6 | 21.3 | 16.4 |
| LISA-7B | 44.4 | 46.0 | 37.6 | 34.4 | 36.6 | 34.7 | 36.8 | 34.1 |
| LISA-7B (ft) | 52.9 | 54.0 | 40.6 | 40.6 | 49.4 | 51.0 | 47.3 | 48.4 |
| LISA-13B | 48.9 | 46.9 | 39.9 | 43.3 | 46.4 | 46.5 | 44.8 | 45.8 |
| LISA-13B (ft) | 56.2 | 62.9 | 44.3 | 42.0 | 54.0 | 54.3 | 51.7 | 51.1 |
| LLaVA1.5-7B + OVSeg | 38.2 | 23.5 | 24.2 | 18.7 | 44.6 | 37.1 | 39.7 | 31.8 |
| LISA-7B-LLaVA1.5 | 53.6 | 52.3 | 47.1 | 48.5 | 49.2 | 48.9 | 48.7 | 48.8 |
| LISA-7B-LLaVA1.5 (ft) | 61.3 | 62.9 | 48.3 | 46.3 | 57.9 | 59.7 | 55.6 | 56.9 |
| LLaVA1.5-13B + OVSeg | 37.9 | 26.4 | 27.1 | 19.4 | 46.1 | 40.6 | 41.5 | 34.1 |
| LISA-13B-LLaVA1.5 | 57.7 | 60.3 | 50.8 | 50.0 | 54.7 | 50.9 | 53.8 | 50.8 |
| LISA-13B-LLaVA1.5 (ft) | **65.0** | **72.9** | **55.4** | **50.6** | **63.2** | **65.3** | **61.3** | **62.2** |

#### Trainable Parameters. 

To preserve the learned knowledge of the pre-trained multimodal LLM $\mathcal{F}$ (i.e., LLaVA in our experiments), we leverage LoRA [@hu2021lora] to perform efficient fine-tuning, and completely freeze the vision backbone $\mathcal{F}_{enc}$. The decoder $\mathcal{F}_{dec}$ is fully fine-tuned. Additionally, the LLM token embeddings (`embed_tokens`), the LLM head (`lm_head`), and the projection layer $\gamma$ are also trainable.

It is notable that the resulting model avoids the catastrophic forgetting of the original text generation capability and preserves the conversation ability, as verified in the supplementary material. The potential reasons are: we 1) employ LoRA fine-tuning to reduce the trainable parameters and 2) incorporate the VQA dataset during fine-tuning.

# Experiment

## Experimental Setting {#exp:setting}

#### Network Architecture.

Unless otherwise specified, we use LLaVA-7B-v1-1 or LLaVA-13B-v1-1 [@liu2023visual] as the base multimodal LLM $\mathcal{F}$, and adopt the ViT-H SAM [@kirillov2023segment] backbone as the vision backbone $\mathcal{F}_{enc}$. The projection layer of $\gamma$ is an MLP with channels of \[256, 4096, 4096\].

#### Implementation Details.

We adopt 8 NVIDIA 24G 3090 GPUs for training. The training scripts are based on deepspeed [@rasley2020deepspeed] engine. We use AdamW [@loshchilov2017decoupled] optimizer with the learning rate and weight decay set to 0.0003 and 0, respectively. We also adopt WarmupDecayLR as the learning rate scheduler, where the warmup iterations are set to 100. The weights of the text generation loss $\lambda_{txt}$ and the mask loss $\lambda_{mask}$ are set to $1.0$ and $1.0$, respectively, and those of the bce loss $\lambda_{bce}$ and the dice loss $\lambda_{dice}$ are set to $2.0$ and $0.5$, respectively. Besides, the batch size per device is set to 2, and the gradient accumulation step is set to 10. During training, we select at most 3 categories for each image in semantic segmentation datasets.

#### Datasets.

As mentioned in Section 4.2, our training data is mainly composed of three types of datasets: (1) For the semantic segmentation dataset, we use ADE20K [@zhou2017scene] and COCO-Stuff [@caesar2018coco]. Besides, to enhance the segmentation result for some part of an object, we also use part semantic segmentation datasets, including PACO-LVIS [@ramanathan2023paco], PartImageNet [@he2022partimagenet], and PASCAL-Part [@chen2014detect]; (2) For the referring segmentation dataset, we use refCLEF, refCOCO, refCOCO+ [@kazemzadeh2014referitgame], and refCOCOg [@mao2016generation]; (3) For the visual question answering (VQA) dataset, we use the datasets of LLaVA-Instruct-150k for LLaVA v1 [@liu2023visual] and LLaVA-v1.5-mix665k for LLaVA v1.5 [@liu2023improved]. In order to avoid data leakage, we exclude the COCO samples whose images are present in the refCOCO(+/g) validation sets during training. Furthermore, we surprisingly find that by fine-tuning the model on only 239 ReasonSeg data samples, the model's performance can be further boosted.

#### Evaluation Metrics.

We follow most previous works on referring segmentation [@kazemzadeh2014referitgame; @mao2016generation] to adopt two metrics: gIoU and cIoU. gIoU is defined by the average of all per-image Intersection-over-Unions (IoUs), while cIoU is defined by the cumulative intersection over the cumulative union. Since cIoU is highly biased toward large-area objects and it fluctuates too much, gIoU is preferred.

<a id="table:refer_seg"></a>
**Table 2.** Vanilla referring segmentation results on refCOCO, refCOCO+, and refCOCOg.

| Method | RefCOCO val | RefCOCO testA | RefCOCO testB | RefCOCO+ val | RefCOCO+ testA | RefCOCO+ testB | RefCOCOg val(U) | RefCOCOg test(U) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MCN [@luo2020multi] | 62.4 | 64.2 | 59.7 | 50.6 | 55.0 | 44.7 | 49.2 | 49.4 |
| VLT [@ding2021vision] | 67.5 | 70.5 | 65.2 | 56.3 | 61.0 | 50.1 | 55.0 | 57.7 |
| CRIS [@wang2022cris] | 70.5 | 73.2 | 66.1 | 62.3 | 68.1 | 53.7 | 59.9 | 60.4 |
| LAVT [@yang2022lavt] | 72.7 | 75.8 | 68.8 | 62.1 | 68.4 | 55.1 | 61.2 | 62.1 |
| ReLA [@liu2023gres] | 73.8 | 76.5 | 70.2 | **66.0** | **71.0** | 57.7 | 65.0 | 66.0 |
| X-Decoder [@zou2023generalized] | - | - | - | - | - | - | 64.6 | - |
| SEEM [@zou2023segment] | - | - | - | - | - | - | 65.7 | - |
| LISA-7B | 74.1 | 76.5 | 71.1 | 62.4 | 67.4 | 56.5 | 66.4 | 68.5 |
| LISA-7B (fine-tuned on ReferSeg) | **74.9** | **79.1** | **72.3** | 65.1 | 70.8 | **58.1** | **67.9** | **70.6** |


## Reasoning Segmentation Results {#exp:reasonseg}

The reasoning segmentation results are shown in Table 1. It is worth noting that existing works fail to handle the task, but our model can accomplish the task involving complex reasoning with more than $20\%$ gIoU performance boost. As mentioned before, the reasoning segmentation task is essentially different from the referring segmentation task in that it requires the model to possess *reasoning ability* or access *world knowledge*. Only by truly understanding the query, can the model do well in the task. The existing works have no proper way to understand an implicit query, but our model exploits multimodal LLMs to reach the goal.

Notably, we also make a comparison with the vanilla two-stage method (LLaVA1.5 + OVSeg). Specifically, the two-stage method refers to first using a multimodal LLM (e.g., LLaVA v1.5) to generate a text output for the input query, and then adopting a referring or open-vocabulary segmentation model (e.g., OVSeg) to generate the segmentation mask. If the intermediate text output remains too long and exceeds the input token length limit of OVSeg, we use GPT-3.5 to further summarize. More details can be found in the supplementary material. The results in Table 1 show that our model outperforms the two-stage method significantly. We explain that the potential reasons are: 1) Our model is trained end-to-end, while the two-stage method is completely decoupled; 2) The two-stage method relies on text as an intermediary to transmit information, while our model utilizes the hidden embedding that is more expressive.

Another finding is that LISA-13B outperforms the 7B counterpart substantially, especially on the long-query scenarios, which indicates that the current performance bottleneck may still lie in understanding the query text, and a stronger multimodal LLM (e.g., LLaVA v1.5 [@liu2023improved]) leads to even better results.

## Vanilla Referring Segmentation Results {#exp:referseg}

To show that our model is also competent in the vanilla referring segmentation task, we make a comparison with existing state-of-the-art methods in Table 2. We evaluate the methods on refCOCO, refCOCO+, refCOCOg validation and testing sets. Our model achieves state-of-the-art results across various referring segmentation benchmarks.

## Ablation Study {#exp:ablation}

In this section, we conduct an extensive ablation study to reveal the contribution of each component. Unless otherwise specified, we report the metrics of gIoU and cIoU of LISA-7B on the validation set.

<a id="table:vision_backbone"></a>
**Table 3.** Ablation study on the design choice of vision backbone. `ft` denotes fine-tuning on the ReasonSeg training set.

::: {#table:vision_backbone}
       Vision Backbone         gIoU       cIoU
  ------------------------- ---------- ----------
     Mask2Former-Swin-L        42.4       38.8
        SAM (w/ LoRA)          41.5       37.3
             SAM               44.4       46.0
   Mask2Former-Swin-L (ft)     50.7       52.3
      SAM w/ LORA (ft)         51.8       51.9
          SAM (ft)           **52.9**   **54.0**

  : Ablation study on the design choice of vision backbone. 'ft' denotes finetuning on ReasonSeg training set.
:::

<a id="fig:vis_comp"></a>
![](../images/LISA_md_images/figures/fig_vis_comp_crop.pdf.png){width="95%"}

**Figure 5.** Visual comparison among LISA and existing related methods.

<a id="table:ablation"></a>
**Table 4.** Ablation study on SAM pre-trained weight and rephrasing.

::: {#table:ablation}
   Exp. ID   Pre-train~SAM~ $\gamma$   rephrasing     gIoU       cIoU
  --------- ------------------------- ------------ ---------- ----------
      1                                               35.9       44.6
      2                                               50.7       51.1
      3                                             **52.9**   **54.0**

  : Ablation study on SAM pre-trained weight and rephrasing.
:::

#### Design Choices of Vision Backbone.

We emphasize that vision backbones other than SAM are also applicable in our framework. In Table 3, we notice that SAM performs the best, potentially because of the massive high-quality data used in its pre-training phase. Further, we also find that with the Mask2Former backbone, our framework still achieves a decent performance on the reasoning segmentation task, significantly outperforming previous works such as X-Decoder [@zou2023generalized]. This reveals the fact that the design choice of vision backbone is flexible and not limited to SAM.

#### SAM LoRA Fintuning.

We also investigate the effectiveness of applying LoRA on the SAM backbone. In Table 3, we note that the performance of LoRA fine-tuned SAM backbone is inferior to that of the frozen one. A potential reason is that fine-tuning impairs the generalization ability of the original SAM model.

#### SAM Pre-trained Weight.

To demonstrate the contribution of SAM pre-trained weight, we make a comparison between Experiments 1 and 3 in Table 4. Without being initialized with SAM pre-trained weight, the vision backbone is trained from scratch. This causes the performance to fall substantially behind that of the baseline model.

::: tabular
c \| c c c \| c \| c \| c \| c c \*ID & & \*ReferSeg & \*VQA & \*ReasonSeg & \*gIoU & \*cIoU\

  & ADE20K & COCO-Stuff & PartSeg &   &   &   &   &  \

1 & & & & & & & 48.9 & 53.5\
2 & & & & & & & 48.5 & 50.8\
3 & & & & & & & 46.7 & 50.9\
4 & & & & & & & 46.6 & 46.7\
5 & & & & & & & 30.4 & 20.4\

6 & & & & & & & 47.7 & 51.1\

7 & & & & & & & 44.4 & 46.0\

8 & & & & & & & **52.9** & **54.0**\
:::

#### Instruction Rephrasing by GPT-3.5.

When fine-tuning the model on the reasoning segmentation data samples, we rephrase the text instruction by GPT-3.5 (the details are shown in the supplementary material), and randomly choose one. The comparison between Experiments 2 and 3 in Table 4 shows that the performance is increased by 2.2% gIoU and 2.9% cIoU. This result verifies the effectiveness of such data augmentation.

#### Contribution of All Types of Training Data.

<a id="table:ablation_training_data"></a>
**Table 5.** Contribution of each type of training data to the final performance.

| ID | ADE20K | COCO-Stuff | PartSeg | ReferSeg | VQA | ReasonSeg | gIoU | cIoU |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  | Check | Check | Check | Check | Check | 48.9 | 53.5 |
| 2 | Check |  | Check | Check | Check | Check | 48.5 | 50.8 |
| 3 | Check | Check |  | Check | Check | Check | 46.7 | 50.9 |
| 4 |  |  | Check | Check | Check | Check | 46.6 | 46.7 |
| 5 |  |  |  | Check | Check | Check | 30.4 | 20.4 |
| 6 | Check | Check | Check |  | Check | Check | 47.7 | 51.1 |
| 7 | Check | Check | Check | Check | Check |  | 44.4 | 46.0 |
| 8 | Check | Check | Check | Check | Check | Check | **52.9** | **54.0** |


In Table 5, we show the contribution of each type of data to the performance. We find that in Exp. 5, we do not use any semantic segmentation dataset, and the performance drops a lot. We conjecture that semantic segmentation datasets provide a large amount of ground-truth binary masks for training, since a multi-class label can induce multiple binary masks.

<a id="table:ablation_reasonseg_data"></a>
**Table 6.** Results on the ReasonSeg test set with different reasoning-segmentation training splits.

::: {#table:ablation_reasonseg_data}
  ----------------- ----------------- ---------- ----------
  Training splits    \# data samples     gIoU       cIoU
  train                    239           51.7       51.1
  train + val              439         **54.0**   **54.9**
  ----------------- ----------------- ---------- ----------

  : Results on the ReasonSeg test set.
:::

We also notice that adding more reasoning segmentation data samples during training leads to better results. In Table 6, we also add the ReasonSeg val set (200 data samples) during fine-tuning, and it yields better performance in both gIoU and cIoU metrics. This indicates that more reasoning segmentation training samples are beneficial at this moment.

## Qualitative Results {#exp:qualitative}

As depicted in Figure 5, we provide a visual comparison with existing related works, including the model for open-vocabulary semantic segmentation (OVSeg), referring segmentation (GRES), and the generalist models for segmentation (X-Decoder and SEEM). These models fail to handle the displayed cases with various errors, while our approach produces accurate and high-quality segmentation results. More illustrations are given in the supplementary material.

# Conclusion

In this work, we have proposed a new segmentation task---*reasoning segmentation*. Also, we have introduced an evaluation benchmark *ReasonSeg*, which comprises over one thousand data samples. Finally, we have presented our model --- LISA. It injects segmentation capabilities into current multimodal LLMs and performs surprisingly effectively on the reasoning segmentation task. We hope our work can shed new light on the direction of combining LLMs and vision tasks in the future.

# Acknowledgements {#acknowledgements .unnumbered}

This work is supported in part by the Research Grants Council under the Areas of Excellence scheme grant AoE/E-601/22-R and the Shenzhen Science and Technology Program under No. KQTD20210811090149095.

[^1]: Equal Contribution

[^2]: Corresponding Author ([ tianzhuotao@hit.edu.cn]( tianzhuotao@hit.edu.cn)).
