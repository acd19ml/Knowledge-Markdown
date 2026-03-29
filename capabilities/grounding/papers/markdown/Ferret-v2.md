<a id="fig:intro"></a>
![](../images/Ferret-v2_md_images/figs/teaser_v2.pdf.png){width="100%"}

**Figure 1.** (a) The comparison showcases Ferret-v2's superior referring and grounding abilities over Ferret, particularly in identifying objects and texts within small regions. (b) Ferret-v2 notably exceeds Ferret's performance in tasks requiring detailed regional and global reasoning and understanding (all with 7B models).

# Introduction {#sec:intro}

Multimodal Large Language Models (MLLMs) [@koh2023grounding; @wu2023visual; @yang2023mm; @liu2023internchat; @wu2023ppt; @li2023blip; @ye2023mplug; @wu2023see; @li2023otter; @wang2023cogvlm; @gao2024sphinx; @mckinzie2024mm1] have increasingly become pivotal in the recent surge of advancements in AI, serving as foundational elements in the development of versatile general-purpose assistants. However, these methods were built on coarse image-level alignments, which suffer from fine-grained understanding (such as region description and reasoning). To this end,  @peng2023kosmos [@chen2023shikra; @you2023ferret] integrate the grounding abilities and unlock the referential ability in dialogue, *i.e.*, enable the user to point to the object or region as input, and the model response with spatial coordinates of bounding boxes. This advancement enables MLLMs to perform tasks requiring detailed visual understanding, marking significant progress in the field.

While grounding and referring MLLMs exhibit strong performance, there are still many challenges that remain unresolved. For example, the aforementioned methods use CLIP [@jiang2023clip] or its variants [@sun2023eva] as the vision encoder. As the pre-trained image encoders normally adopt a relatively low image resolution, *e.g.*, 224×224, it severely hinders fine-grained visual comprehension for MLLMs. Though some task-specific MLLMs [@lv2023kosmos; @hong2023cogagent; @ye2023mplug] have explored strategies for upscale processing, these approaches are marred by undue complexity for their own domains and cannot perform well on traditional MLLM benchmarks. Thus, the scenario prompts a critical inquiry: *how can we enhance the capabilities of MLLMs to excel in detailed vision-related tasks without compromising their proficiency in global reasoning?*

To answer this question, we explore the potential from three aspects, *i.e.*, higher-resolution scaling, multi-granularity visual encoding, and model training recipes. We choose Ferret [@you2023ferret] as the robust baseline since it has two advantages: (i) mutual benefits between referring and grounding, and (ii) more versatile referring capability (strokes, scribbles, or complex polygons). Firstly, we conduct a careful investigation into higher-resolution scaling, and evaluate the performance of two mainstream methods, "direct upsampling" [@wang2023cogvlm; @Qwen-VL] and "any resolution" [@gao2024sphinx; @liu2024llavanext], on (i) Visual detail analysis (ROC [@you2023ferret] & REC [@kazemzadeh2014referitgame]), (ii) Resolution-critical OCR tasks (TextVQA [@singh2019towards]), and (iii) Reasoning MLLM benchmarks (Ferret-Bench [@you2023ferret]). Our analysis indicates that the "any resolution" approach outperforms "direct upsampling" in harnessing image details while retaining the knowledge acquired during pre-training for efficient scaling. This positions "any resolution" as a superior strategy for tasks requiring advanced visual comprehension.

By adopting the "any resolution" method, which involves dividing the image into sub-patches for processing by the CLIP encoder, we observed that incorporating both global context and high-resolution patches into visual embeddings introduces a nuanced complexity. This is because the two types of images exhibit distinct characteristics. To mitigate this gap, we propose the integration of a DINOv2 encoder [@oquab2023dinov2]. Renowned for its proficiency in delineating finer details pertaining to local objects, DINOv2 promises to bolster the model's ability to perceive fine-grained aspects. Additionally, we employ separate MLP projectors for each vision encoder to facilitate a deeper exploration of the varying contexts presented by global and fine-grained visual information, aiming for a more comprehensive understanding and representation.

Furthermore, the model is strategically trained in three stages, enhancing resolution handling while maintaining vision-language alignment in a "coarse-to-fine" manner. Initially, the model is trained on low-resolution images for efficient image-caption alignment. Subsequently, we recognize the gap that several downstream tasks demand a more accurate and thorough spatial understanding and go beyond just the broad semantics, so we specifically design the 2nd stage to align every possible local object of the image with detailed semantics with dense referring and detection data. Finally, the model undergoes visual instruction fine-tuning to better interpret user intent.

The contributions of this paper are summarized as follows: *(i)* We provide a thorough analysis of higher-resolution scaling, and found that the "any resolution" method consistently outperforms "direct upsampling". *(ii)* Based on "any resolution", we further propose multi-granularity visual encoding, where the low-resolution image is encoded via CLIP, while the high-resolution sub-patches are encoded via DINOv2. This strategy fosters a deeper understanding of both global and fine-grained visual contexts. *(iii)* Ferret-v2 is trained in a three-stage process, where an additional stage is proposed for high-resolution dense alignment before the final instruction tuning. Extensive experiments on a wide range of tasks, including referring and grounding, visual question answering, and modern MLLM benchmarks demonstrate the superiority of Ferret-v2 over existing works (see Figure 1).

# Background {#sec:background}

#### Coarse-level MLLMs.

Motivated by the advanced reasoning abilities demonstrated by LLMs [@openai2022chatgpt; @chowdhery2022palm; @touvron2023llama; @touvron2023llama2; @zhang2022opt; @wei2021finetuned], there is a growing interest in extending these skills to visual understanding, leading to the emergence of multimodal LLMs. For example, Flamingo [@alayrac2022flamingo] utilizes a cross-attention mechanism to enhance visual context awareness, enabling more sophisticated context-aware visual learning. Models such as LLaVA [@liu2023llava; @liu2023improved] and MiniGPT-4 [@zhu2023minigpt] focus on synchronizing image and text features before applying instruction tuning. Additionally, BLIP-2 [@li2023blip] and mPLUG-OWL [@ye2023mplug] offer methods for incorporating image features using a visual encoder, which is then combined with textual embeddings in the LLM architecture. Nonetheless, despite their advancements, these MLLMs, including the latest GPT-4V [@gpt-4v], are limited to producing text outputs, restricting their application in scenarios that demand rich region-level visual perception.

#### Region-level MLLMs.

In recent investigations, there has been a growing focus on the convergence of foundation models and the tasks related to dense visual perception. For example, @li2023semantic [@zou2023segment; @koh2023grounding] leverage the CLIP pre-trained foundation models to enable open-world detection, but they are unable to handle complex instructions. Differently, VisionLLM [@wang2023visionllm] combines a range of vision-centric tasks by utilizing instruction tuning with LLMs. However, it may fall short of fully harnessing the potential of LLMs for handling intricate reasoning tasks. In parallel research efforts, grounding capabilities and open-vocabularies detectors are leveraged by Kosmos-2 [@peng2023kosmos], Qwen-VL [@Qwen-VL] and DetGPT [@detgpt], enabling user-guided detection. Moreover, GPT4RoI [@zhang2023gpt4roi], Shikra [@chen2023shikra], LLaVA-G [@zhang2023llava], and Ferret [@you2023ferret] introduce spatial boxes as input and train the model using region-text pairs, offering regional image understanding. However, all the above methods utilize low-resolution image encoders and thus limit the capability of perceiving more detailed analysis.

# Methods {#sec:methods}

We first revisit the design principles of Ferret in Section 3.1 and present the investigation into higher-resolution scaling in Section 3.2. Subsequently, in Section 3.3, we delve into advancements in the model architecture, including techniques for grounding and referring at any resolution, as well as visual encoding with multiple granularities. Finally, we introduce an enhanced training method aimed at refining the model's proficiency in aligning global and local elements in Section 3.4.

<a id="sec:ferret"></a>
## A Revisit of Ferret

There has been a recent growing focus on the convergence of models [@zhang2023gpt4roi; @chen2023shikra; @peng2023kosmos; @lai2023lisa; @zhao2023bubogpt; @you2023ferret] and the tasks related to visual perception. Ferret [@you2023ferret] distinguishes itself from other MLLMs by excelling in spatial referring and grounding within natural images of diverse shapes and levels of detail.

To refer to various types of regions, such as points, boxes, or free-form shapes, Ferret developed a hybrid region representation, where each region is referred to by a combination of discrete coordinate tokens and continuous region features, as well as region names if available. The coordinates are normalized into the range from 0 to 999, and a point or shape is respectively expressed by \[$x, y$\] or \[$x_{\text{min}}, y_{\text{min}}, x_{\text{max}}, y_{\text{max}}$\]. The continuous region feature is extracted by a spatial-aware visual sampler that samples and aggregates features of the region. Ultimately, a region is represented by "$\langle$region_name$\rangle$ $\langle$coordinates$\rangle$ $\langle$continuous_fea$\rangle$" and fed into the model for referring, e.g., "What is in the region \[100, 50, 200, 300\] $\langle$continuous_fea$\rangle$?". To achieve grounding, Ferret generates the box coordinates right after the corresponding regions/nouns in the text response, e.g., "There is a dog \[100, 150, 300, 200\] in the figure."

Ferret encodes the image with a pre-trained visual encoder (CLIP-ViT-L/14) [@radford2021learning] and then feeds the image feature as additional tokens alongside the text input (and hybrid region representation if any) into a decoder-only language model (Vicuna [@zheng2023judging]). The training contains two stages, image-caption alignment and instruction-tuning, updated with the next-token-prediction loss.

While Ferret boasts flexibility and superior performance, it is hindered by the limitations imposed by the fixed resolution of its pre-trained encoder, which restricts its ability to fully exploit the advantages of enhanced region referring and localization accuracy. Motivated by this, we initially delve into identifying the most efficacious methods for high-resolution scaling. Subsequently, we unveil Ferret-v2, a substantial extension of the Ferret series, aimed at examining a broader and more inclusive multimodal learning framework.

## Analysis of Higher Resolution Scaling {#sec:analysis}

<a id="fig:analysis"></a>
![](../images/Ferret-v2_md_images/figs/analysis_lvis.png){width="24%"}
![](../images/Ferret-v2_md_images/figs/analysis_refcoco.png){width="24%"}
![](../images/Ferret-v2_md_images/figs/analysis_textvqa.png){width="24%"}
![](../images/Ferret-v2_md_images/figs/analysis_bench.png){width="24%"}

**Figure 2.** Performance of "direct upsampling" and "any resolution" with 448x448 image resolution in ROC, REC, TextVQA, and Ferret-Bench. `*` indicates the encoder is frozen during fine-tuning. `star` denotes vanilla Ferret with image resolution of 336x336.

For further analysis, we conduct a series of controlled experiments using different high-resolution scaling methods, *i.e.*, "direct upsampling", and "any resolution"[@liu2024llavanext]. The overall architecture and training process follows Ferret [@you2023ferret] but with a simple modification from a linear layer to a two-layer Multi-Layer Perceptron (MLP). Additionally, to enable the model to better handle short-form answers and perform on more benchmarks, we follow LLaVA 1.5 [@liu2023llava] and add additional task-oriented datasets for VQA [@antol2015vqa] and OCR to the existing GRIT [@you2023ferret], which was previously used in Ferret. To streamline our study, we choose 4 representative tasks: ROC (LVIS: box), REC (RefCOCOg), TextVQA, and Ferret-Bench, and measure the capability of the trained models comprehensively.

#### Direct upsampling *v.s.* Any resolution.

For uniformity in our experiment, we standardize on a target resolution of 448[^1], which is upscaled from 336 as the vision encoder's pre-training resolution for both scaling methods to ensure identical image tokens are input into the LLMs. In the case of "direct upsampling", positional embedding interpolation is applied, and the CLIP encoder is adjusted to this new resolution during the fine-tuning phase. For "any resolution", we predefined a set of resolutions to support up to six grids[^2]. Given an image, we first select the optimal resolution by prioritizing fitting the original image's aspect ratio and size as closely as possible while minimizing wasted resolution, and we resize the input image to the optimal resolution and split the image into these grids. All image patches are encoded by the CLIP encoder separately, and their features are input into LLMs as image tokens. We trained the models using both frozen and unfrozen encoder configurations.

As highlighted in Figure 2, our comparative analysis revealed that the "any resolution" scaling method not only demonstrated significant improvements across all tasks over the vanilla Ferret but also outshined the "direct upsampling" approach. Another interesting observation is that in "any resolution", updating the vision encoder always brings a boost over freezing it, whereas in "direct upsampling", freezing the vision encoder is sometimes even better (as shown in the TextVQA result). As for the reason behind those findings, we hypothesize that "direct upsampling" forces the ViT to adapt to a higher resolution, which brings much longer token lengths deviated from its pre-training data. However, the scale of fine-tuning data is usually much smaller than the pre-training data of the vision encoder (1.3M vs. 400M in our setting), which disturbs its pre-training knowledge. On the contrary, "any resolution" crops the high-resolution image into patches, and the vision encoder processes local patches in a similar token length to its pre-training procedure. Overall, "any resolution" has proved to be a more optimal strategy that balances leveraging high-resolution images and preserving valuable pre-training knowledge for effective scaling.

<a id="sec:model_arch"></a>
## Model Architecture {#sec:model_arch}

<a id="fig:diagram"></a>
![](../images/Ferret-v2_md_images/figs/diagram_v1.pdf.png){width="100%"}

**Figure 3.** Overview of the proposed Ferret-v2 model architecture.

#### Multi-Granularity Visual Encoding.

After devoting to the "any resolution" scaling method, yet another problem arises naturally: there is a granularity difference between global low-resolution image $I_g$ and local split image patches $\{I_{l1}, I_{l2}, ..., I_{lN}\}$, i.e., the global image $I_g$ sees the entire scene but in a coarse resolution, while each local patch $I_{li}$ can see only a part of the scene but in precise detail.

To deal with this issue, we explore encoding those two types of images with distinct visual encoders. Specifically, we choose CLIP [@radford2021learning] to encode global images and DINOv2 [@oquab2023dinov2] to encode local split patches. Our motivation behind this comes from the difference in their pre-training paradigms. The image-text contrastive objective used in CLIP enables these models to capture image-level semantics from captions but tends to neglect the rich pixel-level details due to the limited fine-grained information in the guided captions. DINOv2, trained with self-supervision objectives of both image-level and patch-level, can capture more detailed information about local objects such as shape or texture and therefore possess fine-grained perception abilities. Furthermore, we employ separate MLP projectors for the dual vision encoders, aiming to differentiate and learn the diverse underlying contexts for global and fine-grained visual information: $$\begin{align}
& F_g = \text{CLIP}(I_g) ;  \quad \; \; \; \; F_{li} = \text{DINO}(I_{li}), & I_{li} \in \{I_{l1}, I_{l2}, ..., I_{lN}\} \\
& H_g = \text{MLP}_g(F_g) ;  \quad H_{li} = \text{MLP}_l(F_{li}). &
\end{align}$$

Then, the feature maps of local patches are merged into a large feature map according to its original arrangement and then flattened into a sequence of image features. The global image's feature map is also flattened. Two sequences are connected and input into LLM as visual "tokens".

#### Any resolution Referring.

The hybrid region representation introduced in Ferret has proved effective and versatile in handling various types of referring such as point, box, scribble, etc. What lies at the core of it is the extraction of continuous region features, which is performed by a Spatial-Aware Visual Sampler. However, directly feeding global image features into the visual sampler may not be sufficient to recognize the small referred objects in high-resolution images. Inspired by our previous findings about the visual granularity difference, we further propose to integrate the best of both global semantics and local details for more precise referring. To be more specific, after obtaining the encoded features of global image $H_g$ and local patches $\{H_{l1}, H_{l2}, ..., H_{lN}\}$, we first merge the feature maps of local patches into a large feature map following their original spatial arrangement, and the global image feature map is upsampled via interpolation to align the size of the merged feature map. $$\begin{align}
H_l' &= \text{Concat}\{H_{l1}, H_{l2}, ..., H_{lN}\} & (H_{li} \in \mathbb{R}^{w_l \times h_l \times c}, H_l' \in \mathbb{R}^{nw_l \times mh_l \times c}, n \times m = N) \\
H_g' &= \text{Upsample}(H_g) & (H_g\in \mathbb{R}^{w_g \times h_g \times c}, H_g'\in \mathbb{R}^{nw_l \times mh_l \times c})
\end{align}$$ Then, we fuse the two processed feature maps by adding them channel-wise: $H_a = H_l' + H_g'$, and obtain a high-resolution feature map with strong semantics and local awareness. The $H_a$ is input into a spatial-aware visual sampler [@you2023ferret] to extract continuous region features. Then the continuous feature is combined with discrete coordinates as a hybrid region representation to refer to any region in the image, as shown in Figure 3.

#### Any resolution Grounding.

By combining visual embeddings from both global image and local sub-patches, our model can more effectively uncover visual details from high resolution and bridge the semantics. Without specific adaptation, our framework aligns seamlessly with the grounding design in Ferret; therefore, similarly, we delineate the output coordinate regions through an intuitive numerical representation and employ the LLM as the principal mechanism for deciphering the intrinsic correlations.

## Training Paradigm {#sec:train_pipeline}

<a id="sec:train_pipeline"></a>
![](../images/Ferret-v2_md_images/figs/pretrain_stage.png){width="100%"}

*Model Training Paradigm. The model is trained in a "coarse-to-fine" manner. `snowflake` denotes that the module is frozen.*

#### Stage I: Image-Caption Alignment.

Feature alignment before fine-tuning has been widely utilized to achieve better training efficiency. We adopt this strategy to connect the pre-trained CLIP encoder with the LLM using 1.4M image-text pairs, converted to instruction-following data by  @chen2023sharegpt4v. The low-resolution image encoder and LLM parameters remain frozen, with only the projector trainable. Without any referring in these image-text pairs, the visual sampler does not participate in the training of Stage I.

#### Stage II: High-resolution Dense Alignment.

Although the previous image-caption alignment is effective in bridging vision and LLM in coarse semantics, there still exists a severe gap between the image-caption alignment and the instruction tuning stage. Many downstream tasks, such as referring, grounding, OCR, etc., require a more precise and comprehensive spatial perception of the image, beyond solely coarse semantics.

To alleviate the above mentioned issue, we propose a novel pre-training stage aiming at high-resolution dense alignment. Specifically, instead of aligning the entire image with a global caption, this stage aligns every possible local object of the image with detailed semantics. Correspondingly, two types of tasks and input data are designed. (1) ***Dense Referring***: given the image, the input question refers to regions of all objects one by one and asks about their categories; the model is required to output the predicted classes accordingly. An example is *"**Question:** Please classify the objects in the following locations. 1: $\langle$region_1$\rangle$, 2: $\langle$region_2$\rangle$, \.... **Answer:** Here are the categories: 1: cat, 2: dog, \..."*. (2) ***Dense Detection:*** Given the image, the input question asks to localize all the objects. To reduce randomness and incorporate spatial awareness, we forge the answer to list objects in a certain order, such as raster scan order (from top to bottom, left to right). An example is *"**Question:** Please localize visible objects in the image in a raster scan order. **Answer:** The objects are: 1: cat $\langle$coordinate_1$\rangle$, 2: dog $\langle$coordinate_2$\rangle$, \..."*. To ensure efficient learning of the fine-grained semantics, we collect data from densely annotated object dataset - LVIS [@gupta2019lvis]. On average, each sample includes around 10 object locations, whereas in the instruction tuning stage, referring and grounding datasets mostly have only one or two object locations mentioned per sample.

In terms of the model, we take a pre-trained DINOv2 as the visual encoder for local patches, in addition to the CLIP encoder for global images, as mentioned in Section 3.3. The projector after CLIP is inherited from the image-caption alignment stage, and we further add a separate projector after DINOv2, whose weights are initialized from the CLIP's projector for stability. Then we freeze two vision encoders and LLMs, and only update the two projectors as well as the visual sampler in this alignment stage, with the next-token-prediction loss.

#### Stage III: Intent-Enhanced Instruction Tuning.

After the second stage of pre-training, the model acquires the capability for a comprehensive global understanding of images, alongside the ability to identify and narrate objects of interest using free-form texts and visually referred regions obtained flexibly. Our aim is to enhance the model's adherence to user instructions while maintaining its high-resolution visual perception abilities. To achieve this, we render the encoders, projectors, region samplers, and the LLM itself trainable. For training, we utilize the GRIT dataset [@you2023ferret] and incorporate additional task-specific datasets for VQA [@antol2015vqa] and OCR [@singh2019towards; @sidorov2020textcaps] from LLaVA 1.5 [@liu2023llava]. Furthermore, we identified two additional strategies that contribute to enhanced performance: (i) Data Unification: To facilitate the model's seamless transition from a global understanding based on plain texts to a regional comprehension utilizing hybrid representations, we employ an open-vocabulary object detector, GLIPv2 [@zhang2022glipv2], to localize groundable nouns in the text on VQA datasets, and a public OCR model [@mmocr2021] to get text bounding boxes on OCR datasets. (ii) Task Generalization: In order to diminish ambiguity across tasks that necessitate referring and grounding capabilities and those that do not, we adopt a method similar to LLaVA 1.5, which involves appending the prompt, *"Include the coordinates for each mentioned object."*, to further clarify task requirements.

# Experiments

## Referring and Grounding Tasks

<a id="tab:refer"></a>
**Table 1.** Results of ROC on three different referring types, including point, box, and free-form shape. `×` means no such capability.

| Models | LVIS Point | LVIS Box | LVIS Free-form | SA-refer Point | SA-refer Box | SA-refer Free-form |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Random Guess | 50 | 50 | 50 | 50 | 50 | 50 |
| Kosmos-2 | × | 60.25 | × | × | 53.97 | × |
| Shikra-7B | 57.82 | 67.71 | × | 54.15 | 56.82 | × |
| GPT4-ROI | × | 61.76 | × | × | 55.02 | × |
| CogVLM-17B | × | 79.62 | × | × | 61.77 | × |
| SPHINX-2k | 72.83 | 82.97 | × | 61.21 | 63.39 | × |
| Ferret-7B | 67.94 | 79.42 | 69.77 | 61.91 | 62.99 | 57.74 |
| Ferret-v2-7B (Ours) | **74.55** | **86.59** | **76.13** | **68.38** | **68.83** | **62.07** |
| Ferret-13B | 68.35 | 80.46 | 70.98 | 63.16 | 63.35 | 58.02 |
| Ferret-v2-13B (Ours) | **75.09** | **87.74** | **76.35** | **67.38** | **69.49** | **62.58** |

<a id="tab:gpt4"></a>
**Table 2.** Results on the proposed Ferret-Bench via GPT4-as-a-Judge evaluation.

| Models | Referring Description | Referring Reasoning | Grounding in Conversation | Avg. |
| --- | ---: | ---: | ---: | ---: |
| LLaVA | 41.4 | 31.7 | 28.8 | 34.0 |
| Kosmos-2 | 51.8 | 33.7 | 48.4 | 44.6 |
| Shikra-7B | 46.0 | 41.6 | 50.1 | 45.9 |
| CogVLM-17B | 67.1 | 67.6 | 51.7 | 62.1 |
| Osprey-7B | 72.2 | 67.8 | -- | -- |
| SPHINX-2k | 55.6 | 70.2 | **66.4** | 64.0 |
| Ferret-7B | 68.7 | 67.3 | 57.5 | 64.5 |
| Ferret-v2-7B (Ours) | **79.9** | **81.7** | **65.2** | **75.6** |
| Ferret-13B | 70.6 | 68.7 | 59.7 | 66.3 |
| Ferret-v2-13B (Ours) | **79.6** | **79.4** | **65.7** | **74.9** |

#### Referring.

Ferret-v2's enhanced understanding of referential queries is evident in its ability to interpret the semantics of specified regions within an image accurately. This is particularly assessed through the task of Referring Object Classification (ROC), where the model is tasked with identifying the object in a region mentioned in a query. Initially, like Ferret, we utilize the validation split of the LVIS dataset, covering more than 1,000 object categories with a majority being "in-domain" images. To further demonstrate Ferret-v2's improved ability to reference smaller objects, we compile an "in-the-wild" evaluation set using partial images from SA-1B [@kirillov2023segment] and corresponding human annotations of objects from AS-human  [@wang2023all], which contains high-resolution images, open-vocabulary objects and precise masks. In total, we manually verified 700+ high-quality samples with in-the-wild objects and called it SA-refer. As shown in Table 1, Ferret-v2 significantly outperforms previous models on LVIS and sets up a new benchmark not fully realized in prior Ferret, primarily contributing to high-resolution scaling. SPHINX also uses high-resolution input images; however, on more challenging tasks for SA-refer, Ferret-v2 still outperforms it, indicating the benefits of our special design for any resolution referring.

#### Grounding.

<a id="tab:flickr_refcoco"></a>
**Table 3.** Performance comparison (Acc@0.5) on the REC (RefCOCO, RefCOCO+, RefCOCOg) and phrase grounding (Flickr30k Entities) tasks. `*` indicates that the method is specifically fine-tuned in the second stage.

Visual grounding aims to ground language queries into aligned image regions. We experiment on the sub-tasks of referring expression comprehension (REC) with three renowned benchmarks: RefCOCO [@lin2014microsoft], RefCOCO+ [@yu2016modeling], and RefCOCOg  [@mao2016generation], and phrase grounding with Flickr30k Entities dataset [@plummer2015flickr30k]. As evidenced in Table 3, Ferret-v2 enables the use of high-resolution input images, leading to significant improvements over Ferret [@you2023ferret]. Besides, Ferret-v2 outperforms most state-of-the-art models, including specialist model G-DINO-L [@liu2023grounding] and other generalist models, which adopt even larger input image sizes. Our 7B model can achieve comparable results to CogVLM-Grounding [@wang2023cogvlm], which utilizes a 4B vision model and a 6B connection module. These results demonstrate the competitive capability of Ferret-v2 for visual grounding.

#### Ferret-Bench.

Ferret-Bench [@you2023ferret] is carefully designed to evaluate and benchmark the fine-grained capability of multimodal conversational models, particularly in their ability to refer to, describe, and reason about specific regions within images, thereby facilitating a more structured evaluation of models' referring and grounding capabilities in a multimodal context. We use Ferret-Bench to compare Ferret with previous models, including LLaVA [@liu2023llava], Shikra [@chen2023shikra], Kosmos-2 [@peng2023kosmos], and Osprey [@yuan2023osprey]. Results are summarized in Table 2. Ferret-v2 demonstrates superior performance in all types of tasks, indicating the strong spatial understanding and commonsense reasoning capability of the model.

## Modern MLLM Benchmarks

<a id="tab:results"></a>
**Table 4.** Comparison with SoTA methods on 10 benchmarks. Ferret-v2 achieves comparable performance with others. `*` means the training images of the datasets are observed during training.

Ferret has demonstrated remarkable regional reasoning capabilities; however, it falls short of academic benchmarks that typically demand tasks-oriented datasets. For Ferret-v2, we specifically include pseudo-labeled VQA and OCR datasets and also append the special prompt, as mentioned in Section 3.4. This strategic enhancement progressively narrows the gap between task-specific region-level analyses and broader, more generalized tasks, thereby extending Ferret-v2's applicability to encompass both fine-grained and coarse-grained tasks. As presented in Table 4, we benchmark Ferret-v2 against existing MMLMs across a comprehensive suite of 10 benchmarks: VQA$^\text{v2}$[@antol2015vqa], TextVQA (aka.VQA$^\text{T}$) [@singh2019towards], GQA [@hudson2019gqa], POPE [@li2023evaluating], MME$^\text{P}$ [@chang2023survey], SEED [@li2023seed], LLaVA$^\text{C}$ and LLaVA$^\text{W}$ [@liu2023llava], MM-Vet [@yu2023mm], Obj-Hal [@yu2023rlhf]). Our models achieve on-par performance with the latest state-of-the-art models, particularly excelling in tasks such as VQAv2, GQA, POPE, etc., which demand precise spatial information for accurate responses.

# Ablation Studies

In all the ablation studies below, we follow Section 3.2 and primarily focusing our evaluation on the disparate models' performance across the dimensions of referring, grounding, OCR, and reasoning.

<a id="tab:ablate_anyres"></a>
**Table 5.** Ablation study on any resolution grounding and referring.

| Resolution | LVIS | SA | REC | TextVQA | Ferret-Bench |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fixed Res. | 68.4 | 61.9 | 86.8 | 54.2 | 71.1 |
| + AnyRes. Ground | 72.2 | 67.7 | 88.3 | 60.2 | 72.2 |
| + AnyRes. Refer | 73.0 | 67.8 | 88.5 | 60.7 | 72.6 |

<a id="tab:ablate_granularity"></a>
**Table 6.** Ablation study on the effectiveness of the multi-granularity visual encoding and Stage II pre-training.

| Model | LVIS | SA | REC | TextVQA | Ferret-Bench |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP | 73.0 | 67.8 | 88.5 | 60.7 | 72.6 |
| + DINOv2 | 73.8 | 68.0 | 89.1 | 61.3 | 75.3 |
| + Stage II | **74.6** | **68.4** | **89.3** | **61.7** | **75.6** |

#### Any Resolution Grounding and Referring.

We conduct an ablation study on any resolution grounding and referring. As illustrated in Table 5, accommodating any resolution markedly enhances task performance that necessitates a comprehensive understanding of higher-resolution details. By integrating the best of both global semantics and local details for more precise improved precision in referring tasks across both LVIS and SA datasets. Furthermore, this integration modestly enhances grounding capabilities, suggesting that grounding and referring can derive mutual benefits within our proposed framework.

#### Multi-Granularity Visual Encoding and Stage-II Pre-training.

Our initial ablation study focuses on incorporating an additional DINOv2 encoder for the encoding of high-resolution patches. We utilize the projector weights from Stage I of CLIP for initialization, followed by fine-tuning in Stage III. As demonstrated in Table 6, the exclusive employment of visual granularity encoding significantly enhances both referring and grounding performance. Furthermore, the introduction of an intermediate Stage II in the pre-training process yields improvements across all evaluated metrics.

# Conclusions

We present Ferret-v2, a significant upgrade of the vanilla Ferret model. It features advanced capabilities in handling any resolution referring and grounding, multi-granularity visual encoding, and a novel three-stage training pipeline. These improvements enable Ferret-v2 to excel in processing and understanding images with higher resolution and finer detail. Like most MLLMs, Ferret-v2 may produce harmful and counterfactual responses.

# Acknowledgment {#acknowledgment .unnumbered}

The authors would like to thank Yizhe Zhang, Yanghao Li, Liangchen Song, and Keen You for valuable guidance, suggestions, and feedback. Additional thanks go to Jiaming Hu, Mingfei Gao for supporting large-scale training. The baseline models used in our experiments are based on the open-source code released in the GitHub repository; we acknowledge all the authors who made their code public, which tremendously accelerates our project progress.

[^1]: The number of tokens is dynamic given different input image resolutions, but the maximum number of tokens is 1280. We chose 448 with computational overhead in mind.

[^2]: We use grid configurations of {1x1, 1x2, 1x3, 1x4, 1x5, 1x6, 2x2, 2x3, and their transpose}.
