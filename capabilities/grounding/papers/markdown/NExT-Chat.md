# Introduction {#sec:intro}

Recently, large language models (LLMs) have shown spreading influence in different areas, among which large multimodal models (LMMs) is one of the most attractive area. Researchers try to equip LLMs with visual perception modules resulting in LMMs [@huang2023kosmos1; @zhu2023minigpt4; @zhang2023vpgtrans; @li2023blip2] that can describe the visual content and answer visual questions. However, these LMMs are limited to holistic image understanding without the ability to conduct region-level reasoning, for example, locating the referred objects in the conversation.

To enable region-level understanding, current solutions [@peng2023kosmos2; @wang2023visionllm; @chen2023shikra] utilize the pix2seq [@chen2021pix2seq] paradigm where the object coordinates are converted to LLM understandable text tokens (, $[x_1, y_1, x_2, y_2]$). Consequently, LMMs can output object coordinates as part of a normal next token prediction problem. However, the pix2seq paradigm is limited to discrete coordinate outputs and struggles to provide other fine-grained formats, such as segmentation masks.

To address these limitations, we propose the pix2emb paradigm, which can accommodate different location formats. The key idea is to model all location information as embeddings, which can be decoded into the target formats by corresponding decoders. Specifically, we introduce two new tokens, `<trigger>` and `<loc>`, where the `<trigger>` serve as a trigger for localization and `<loc>` act as a placeholder for objects' location embeddings. During the text generation, the `<trigger>` triggers the location decoding, where the hidden states of `<trigger>` can be used for both detection and segmentation, as depicted in Figure 1. Then, the predicted or provided object location will be encoded into the embedding of the `<loc>` token for object referring. In addition to supporting flexible output formats, the pix2emb modeling also allows for the use of existing localization practices. While the pix2seq paradigm can only frame the detection task as a token classification problem, the embedding-based paradigm formulates the localization task as a regression problem, enabling the adoption of established practices such as L1 loss, IoU loss and GIoU loss.

Building upon the proposed pix2emb method, we introduce a new LMM named NExT-Chat. NExT-Chat is designed to handle various conversation scenarios, including visual grounding (Figure 3), region caption (Figure 5), and grounded image caption (Figure 6). Thanks to the incorporation of LLM, NExT-Chat is also capable of handling scenarios that requires grounded reasoning. By providing an extensive array of examples, we effectively demonstrate NExT-Chat's remarkable proficiency in understanding various components, including background elements, minute objects, and associating the objects with related knowledge. Moreover, we validate our NExT-Chat on various datasets. On the POPE-Random dataset, NExT-Chat achieves an impressive accuracy of 87.7, surpassing Shikra's 86.9. In referring expression segmentation (RES), it attains an average cIoU of 68.9, outperforming LISA's 67.9. Moreover, NExT-Chat achieves a remarkable 79.6 in CIDEr score for RefCOCOg region captioning, significantly exceeding Kosmos-2's 62.3.

To summarize, our contributions can be listed as follows:

- *Effective Method*. We propose the pix2emb method, which can accommodate different output formats such as bounding boxes and segmentation masks.

- *NExT-Chat Model*. Based on the proposed pix2emb method, we build NExT-Chat that can unify the chat, region input, detection and segmentation in a single LMM.

- *Experiments and Demos*. We provide abundant qualitative and quantitative results to showcase the effectiveness of our proposed method.

# Related Works

## LMM

Large multimodal models (LMMs) are typically built on large language models (LLMs) and equipped with visual perception modules to enable the multimodal perception ability, which can generate captions or answer questions based on the given multimodal content. Flamingo [@alayrac2022flamingo] tries to extract vision information by a pre-trained vision backbone with a resampler, and incorporate them into the text features with a cross-attention mechanism. Instead of using cross-attention layers, BLIP-2 [@li2023blip2] and Kosmos [@huang2023kosmos1] directly feed the visual features into the LLMs as soft prompts. Following BLIP-2, MiniGPT-4 [@zhu2023minigpt4] and VPGTrans [@zhang2023vpgtrans] build LMMs with transfer learning, and significantly reduce the training cost. For example, VPGTrans can use only around 10% GPU hours with non-degenerated performances compared with training a new LMM from scratch. When considering the training paradigm, researchers find that a small scale instruction tuning can better align the LMM with the expected output format. MiniGPT-4 [@zhu2023minigpt4] fine-tunes its model with less than 5,000 self-instruct image-text pairs and turns the model into better conversation robot. Different from MiniGPT-4's self-instruct, LLaVA [@liu2023llava] generate the instruction tuning data with the text-only GPT-4 models by feeding the visual information as text sentences. Otter [@li2023otter; @li2023mimicit] further propose a MIMIC-IT dataset that can turn the LMM into better in-context learners. LLaVA-1.5 proposes to further fine-tune the model on human annotated datasets, which can alleviate the image-level hallucination [@liu2023hallusionbench]. However, these LMMs [@alayrac2022flamingo; @liu2023aligning; @liu2023llava] can only take the whole image/video as input and output text, and are incapable of handling region understanding tasks.

<a id="fig:method"></a>
![The overall framework of NExT-Chat. The image and given bounding boxes are encoded by image and box encoders respectively. During decoding, the hidden states of the `<trigger>` are fed into box and mask decoders, enabling object detection and segmentation.](../images/NExT-Chat_md_images/figs/method1.pdf.png){width="80%"}

**Figure 1.** The overall framework of NExT-Chat. The image and given bounding boxes are encoded by image and box encoders respectively. During decoding, the hidden states of the `<trigger>` are fed into box and mask decoders, enabling object detection and segmentation.

## LMM for Region Reasoning

GPT4ROI [@zhang2023gpt4roi] proposes to encode the regions as features and thus can accept the region as input. Pix2seq [@chen2021pix2seq] first propose to represent object bounding box coordinates as text tokens and thus the language model can output the object locations in a token classification manner. However, pix2seq only validate its idea on traditional object detection tasks. UniTab [@yang2022unitab] and PEVL [@yao2022pevl] further extend the idea to vision&language tasks like visual grounding [@yu2016refcoco; @mao2016refcocog]. Following this line, Vision-LLM [@wang2023visionllm] and Kosmos-2 [@peng2023kosmos2] recently applies the token classification concept to LMMs. Take Kosmos-2 as an example, it discretize the whole image into 32$\times$`<!-- -->`{=html}32 bins, which can be used to represent the points lying in it. Additional 32$\times$`<!-- -->`{=html}32 tokens are introduced to the LLM's vocabulary for either coordinates input or output. Thus, the LMM can achieve the region-level reasoning. Shikra [@chen2023shikra] point out that introducing too much new tokens will inevitably increase the training difficulties. Thus, Shikra propose to reuse the LLM's original vocabulary and turn the box coordinates into normalized numerical values with certain precision like $[0.111, 0.111, 0.333, 0.333]$. Although avoiding introducing too much new tokens, it requries roughly 26 tokens to represent each bounding box, which is ineffective. Different from these works, we do not formulate the object localization problem as a token classification problem. Our NExT-Chat introduces an `<trigger>` token as the trigger for location decoding, and then use the hidden states to decode the bounding boxes and the segmentation masks.

# Method

In this section, we present the NExT-Chat framework, starting with an introduction to the overall LMM architecture (Section 3.1), followed by a description of the pix2emb method (Section 3.2). Additionally, we provide details on the training process (Section 3.3).

## LMM Architecture {#sec:arch}

For the LMM architecture, we adopt a LLaVA-like architecture. Specifically, we employ a CLIP ViT-L/14@336px [@radford2021clip] as the vision encoder. The input image is converted into 24$\times$`<!-- -->`{=html}24 patch embeddings and then projected to the same dimension as the word embeddings of the LLM. These patch embeddings serve as visual tokens. Then, the visual tokens will be fed into a decoder-only LLM for conditional text generation. Regarding the selection of LLMs, we opt for the recently released Vicuna-1.5 model [@zheng2023vicuna].

## Pix2Emb Method {#sec:method_emb}

**Detection.** To model the object location as output, we introduce a special token, denoted as `<trigger>`, which serves to trigger the localization. As depicted in Figure 1, the LMM is trained to generate the `<trigger>` token before predicting the locations. Then, the embedding $\mathbf{t} \in \mathcal{R}^n$ of `<trigger>` is then passed to the *Box Decoder* $\mathcal{F}$ for regression. Mathematically, this can be expressed as follows: $$\begin{equation}
    \mathbf{b} = \mathcal{F}(\mathbf{t}),
\end{equation}$$ where $\mathbf{b} \in \mathcal{R}^4$ represents the predicted bounding box coordinates in the format $[x_0, y_0, x_1, y_1]$.

In our NExT-Chat model, the box decoder consists of a 2-layer MLP. To supervise the location output, we employ a joint loss function comprising of the L1 loss and the GIoU loss [@rezatofighi2019giou] during training: $$\begin{equation}
    {\cal L}_{det} = \alpha{\cal L}_1(\mathbf{b}, \mathbf{b}_{gt})+\beta\text{GIoU}(\mathbf{b}, \mathbf{b}_{gt}),
\end{equation}$$ where $\mathbf{b}_{gt}$ represents the ground truth coordinates, and $\alpha=2$, $\beta=0.8$ follows the ratio utilized in DETR [@carion2020detr].

**Segmentation.** Similar to the detection process, we utilize the hidden states $\mathbf{t}$ of the `<trigger>` as input for the mask head. Inspired by LISA [@lai2023lisa], we use SAM [@kirillov2023sam] as our mask head, which also additionally takes the original image as input. To ensure compatibility between the hidden states and SAM, we first project the hidden states to match the dimension of SAM's prompt embedding using a linear projector. Subsequently, the projected hidden states are fed as the prompt embedding to SAM. For improved performance, we also encode the detected bounding boxes into a prompt embedding with SAM's prompt encoder and concatenate it with the projected embedding. To train the mask output, we follow the practice outlined in lightning-SAM[^1]: $$\begin{equation}
    {\cal L}_{seg} = \text{IoU}(\mathbf{m}, \mathbf{m}_{gt})+\text{D}(\mathbf{m}, \mathbf{m}_{gt}) + \beta \text{F}(\mathbf{m}, \mathbf{m}_{gt}),
\end{equation}$$ where $\text{IoU}$, $\text{D}$, and $\text{F}$ are IoU Loss, Dice Loss, and Focal Loss separately. $\beta$ is set to 20 in our experiments.

<a id="fig:cyc_loss"></a>
![Cycle loss utilized to bind box encoder and decoder training.](../images/NExT-Chat_md_images/figs/cyc_loss.png){width="90%"}

**Figure 2.** Cycle loss utilized to bind box encoder and decoder training.

**Location as Input.** In addition to the location output, it is essential to incorporate location as input as well. To be consistent with the location output modeling, we also use a single embedding to represent the location information. Therefore, the output location embedding can also serve as the input embedding. Consequently, we introduce another 2-layer MLP, referred to as the location encoder $\mathcal{G}$. In order to simplify the problem, we convert all location formats into bounding boxes $b$ and subsequently transform them into embeddings $\mathbf{t} \in \mathbb{R}^n$ suitable for the LLM. The location encoder can be supervised through the standard text generation loss ${\cal L}_{text}$. For instance, when inquiring about the relationship between bounding box $\mathbf{b}_1$ and $\mathbf{b}_2$, the location encoder is compelled to provide precise information.

However, we observe that the location encoder cannot be effectively trained solely through indirect supervision from ${\cal L}_{text}$. As a result, we introduce an additional cycle loss to facilitate the training of the encoder in conjunction with the decoder. As illustrated in Figure 2(a), a bounding box will be encoded and then decoded, where two bounding boxes are asked to be the same. Similarly, the hidden states of `<trigger>` will also be used to calculate the cycle loss (Figure 2(b)). Formally, the $L_{cyc}$ is defined as: $$\begin{equation}
    {\cal L}_{cyc} = {\cal L}_1(\mathbf{b}, \mathcal{F}(\mathcal{G}(\mathbf{b}))) + {\cal L}_2(\mathbf{t}, \mathcal{G}(\mathcal{F}(\mathbf{t}))),
\end{equation}$$ where $\mathbf{b}$ and $\mathbf{t}$ are provided bounding box and predicted embedding respectively. Additionally, ${\cal L}_1$ and ${\cal L}_2$ correspond to the L1 Loss and L2 Loss, respectively.

## Training Process {#sec:method_training}

We employ a three-stage training process, consisting of pre-training, instruction tuning, and segmentation training, to train our model. The idea is to train the bounding box decoding ability for the first two stages and then extend to segmentation with a lightweight training.

**Stage 1.** During this stage, we perform pre-training using a mixture of data from various sources, including Flickr30K Entities [@plummer2015flickr30k], Visual Genome [@krishna2017vg], RefCOCO [@yu2016refcoco], RefCOCO+ [@yu2016refcoco], RefCOCOg [@mao2016refcocog], VQAv2 [@antol2015vqa], PointQA [@mani2020pointqa], Visual7W [@zhu2016visual7w], and VCR [@zellers2019vcr]. The model is trained with a batch size of 64 and a learning rate of 2e-5 for 65k steps. During this pre-training stage, the entire language model with the box decoder, is trained while keeping the image encoder frozen. The training loss is formulated as: $$\begin{equation}
    {\cal L}_{s1} = {\cal L}_{text} + {\cal L}_{det} + {\cal L}_{cyc}.
\end{equation}$$ For NExT-Chat 7B model, the stage-1 training uses 8 A100 (80G) GPUs for around 59 hours.

**Stage 2.** In the second stage, we further fine-tune the model using data from VQAv2, RefCOCO, Flickr30K Entities, LLaVA-instruct, VG grounded captioning, VCR, and Shikra-RD [@chen2023shikra]. The batch size is reduced to 64, and the learning rate is set to 2e-5. The loss is the same with stage-1's loss. For NExT-Chat 7B model, the stage-2 training uses 8 A100 (80G) GPUs for around 10 hours.

**Stage 3.** After the two stages training, the model is equipped with the ability to engage in dialogue and perform image localization. To prevent catastrophic forgetting, we keep most of the parameters frozen during the segmentation training. Specifically, we only train the linear projector between the LMM and SAM, as well as the decoder of SAM. The loss for the stage-3 is: $$\begin{equation}
    {\cal L}_{s3} = {\cal L}_{seg}.
\end{equation}$$ Thanks to the small amount of training parameters, the training can be done in 3 hours with 8 A100 (80G) GPUs. This training is performed using the referring segmentation splits of RefCOCO, RefCOCO+, and RefCOCOg datasets.

# Experiment

<a id="tab:pope_results"></a>
**Table 1.** *Image Hallucination:* comparison between our NExT-Chat and current SOTA models on the POPE benchmark for image hallucination diagnosis.

<a id="tab:res"></a>
**Table 2.** *RES:* comparison between our NExT-Chat and baselines on RES. The evaluation metric is **cIoU**.

<a id="tab:rec"></a>
**Table 3.** *REC:* comparison between our NExT-Chat and baselines on REC. The evaluation metric is **Acc@0.5**. `*` refers to the specialist or fine-tuned methods.

::: {#tab:reg_cap}
+--------------------------------------+---------------------+
| Methods                              | RefCOCOg            |
+:=====================================+:========:+:========:+
| 2-3                                  | CIDEr    | METEOR   |
+--------------------------------------+----------+----------+
| GRIT [@wu2022grit]                   | 71.6     | **15.2** |
+--------------------------------------+----------+----------+
| Kosmos-2 [@peng2023kosmos2] (0-shot) | 60.3     | 12.2     |
+--------------------------------------+----------+----------+
| Kosmos-2 [@peng2023kosmos2] (2-shot) | 62.2     | 13.8     |
+--------------------------------------+----------+----------+
| Kosmos-2 [@peng2023kosmos2] (4-shot) | 62.3     | 14.1     |
+--------------------------------------+----------+----------+
| ASM [@wang2023allseeing]             | 41.9     | 13.6     |
+--------------------------------------+----------+----------+
| NExT-Chat (**ours**)                 | **79.6** | 12.0     |
+--------------------------------------+----------+----------+
|                                      |          |          |
+--------------------------------------+----------+----------+

: **Region Captioning**: comparison between our NExT-Chat and baselines on RefCOCOg.
:::

<a id="tab:reg_cap"></a>
**Table 4.** *Region Captioning:* comparison between our NExT-Chat and baselines on RefCOCOg.

In this section, we begin by conducting a rigorous evaluation to validate the effectiveness of our pix2emb approach in a fair comparison setting. Following that, we demonstrate the potential of our NExT-Chat model by presenting a wide range of qualitative results from different scenarios. Finally, we provide quantitative results to compare the performance of our NExT-Chat model with the current SOTA methods on the image-level hallucination, referring expression segmentation, referring expression detection and region-level caption tasks.

## Applications across Different Scenarios {#sec:exp_demp}

In this section, we present qualitative results that showcase the capabilities of our NExT-Chat model across various scenarios.

**Visual Grounding.** As shown in Figure 3, we can see that our NExT-Chat accurately detects and segments the queried objects, such as the bears and the sky in the background. To ensure that our model is not biased towards specific objects, we test it with different queries to find all four bears individually. Our model successfully localizes each bear based on the given queries. Additionally, our model showcases reasoning abilities through challenging grounding problems. For instance, in Figure 4, our model accurately localizes the remote in response to the query "Where is the object to control the TV in image?" It also localizes the boat based on understanding the given object location input.

**Region Captioning.** To evaluate the effectiveness of our NExT-Chat model for region input, we conducted experiments where the model generates descriptions based on given bounding boxes. As depicted in Figure 5, our model consistently produces accurate descriptions specifically tailored to the provided regions, without being influenced by the overall image content or salient regions. We observed this behavior consistently across different examples. Notably, in the second row of Figure 5, our model demonstrates the ability to accurately recognize and describe small objects such as flags, as well as background objects like trees. This demonstrates the robustness and effectiveness of our model in generating region-based captions.

**Grounded Captioning.** Another compelling application of our NExT-Chat model is its ability to describe images by referencing specific objects present within them. Figure 6 demonstrates that our model can accurately identify and describe the major 2 or 3 objects in an image, effectively organizing them into coherent sentences. By incorporating object references, our model demonstrates a reduced tendency to generate captions containing non-existent objects. This highlights the model's capability to generate more accurate and contextually grounded image descriptions.

**Reasoning.** In addition to its demonstrated ability in single-turn and concise response generation, our NExT-Chat model also possesses the capability for generating detailed explanations in response to given questions. As illustrated in the third example of Figure 7, our model exhibits the ability to infer the occupation of the man in the image by analyzing contextual cues such as his uniform and the horse he is riding. This inference is supported by the model's ability to localize relevant regions within the image. Furthermore, for each hypothesis regarding the man's occupation, our model provides detailed descriptions of the potential duties associated with that occupation. This showcases the model's capacity for nuanced reasoning and comprehensive explanation generation.

# Comparison with SOTAs

In this study, we evaluate our NExT-Chat model by comparing it with current state-of-the-art (SOTA) models on various tasks including image-level hallucination diagnose (POPE dataset [@li2023pope]), referring detection, referring segmentation and region-level captioning (RefCOCOg).

## Hallucination

**Experimental Setup.** For a comprehensive evaluation, we benchmarked our NExT-Chat model against current state-of-the-art (SOTA) LMMs including Shikra [@chen2023shikra], InstructBLIP, MiniGPT-4 [@zhu2023minigpt4], LLaVA [@liu2023llava], MM-GPT [@gong2023mmgpt] and mPLUG-OWL [@ye2023mplug] on the POPE dataset [@li2023pope].

**Results.** The results, presented in Table 1, demonstrate that our NExT-Chat model exhibits competitive performance compared with existing SOTA models. Notably, our model achieves the the best performance for the random and popular splits and achieve the second best performance of the adversatrial split. These findings indicate that our NExT-Chat model is competent in generating accurate responses, thus positioning it among the top-performing models in the field.

## Referring Expression Segmentation

**Experimental Setup.** To rigorously assess our model's proficiency in generating segmentation masks guided by natural language instructions, we use the referring expression segmentation (RES) splits of RefCOCO, RefCOCO+, and RefCOCOg. As for baselines, we choose both the LMM based method (LISA [@lai2023lisa]) and non-LMM based methods including MCN [@luo2020mcn], VLT [@ding2021vlt], CRIS [@wang2022cris], LAVT [@yang2022lavt], GRES [@liu2023gres], X-Decoder [@zou2023xdecoder] and SEEM [@zou2023seem]. cIoU metric is employed to evaluate different methods.

**Results.** As demonstrated in Table 2, NExT-Chat exhibits superior or comparable cIoU scores relative to all baseline models. In comparison with non-LMM based methods, our approach consistently achieves either the highest or second-highest performance across various dataset splits, with the sole exception being the RefCOCO+ val set. Against LMM-based methods, specifically the LISA-7B model, NExT-Chat demonstrates enhanced performance in six dataset splits, notably achieving a substantial 4.5-point improvement in the RefCOCO+ testA split. It is noteworthy that NExT-Chat is trained with a significantly smaller dataset, comprising only 127k object segmentation masks, in stark contrast to baselines such as LISA, which utilize datasets more than an order of magnitude larger. These results underscore the efficiency of our training paradigm in substantially reducing the dependency on extensive and costly segmentation annotation datasets.

## Referring Expression Comprehension

**Experimental Setup.** In addition to the segmentation ability, we also validate the detection ability of our method. Concretely, we adopt the REC splits of RefCOCO, RefCOCO+, and RefCOCOg. As for baselines, we first include the LMM method (pix2seq): VisionLLM-H [@wang2023visionllm], and Shikra [@chen2023shikra] We also include the non-LLM based methods: MAttNet [@yu2018mattnet], OFA-L [@wang2022ofa], UniTab [@yang2022unitab], G-DINO-L [@liu2023gdino] and etc, where the models with `*` mark in Table 3 refer to the specialist and fine-tuned methods.

**Results.** First of all, our NExT-Chat can achieve excellent REC results and can even beat a series of fine-tuned methods like VILLA [@gan2020villa], UNITER [@chen2020uniter] and TranVG [@deng2021transvg] on all of the splits. There is also an interesting phenomenon that our NExT-Chat is slightly lower than Shikra-7B even with a similar data recipe for detection training. We hypothesize the reasons are that: (1) it is difficult to seek a perfect balance between the LM loss and localization loss, where the pix2seq methods do not suffer from this problem. (2) LLM is not pre-trained on the regression tasks and will potentially increase the training difficulty. However, we believe that incorporating the regression tasks in the LMM will be necessary, especially for targets like embodied AI.

## Region Caption

**Experiment Setup.** In addition to the region output, we also validate the model's ability of taking regions as input. The RefCOCOg is adopted, where each model is asked to describe the given region. The CIDEr and METEOR are applied as the evalution metrics. For the baselines, we choose GRIT [@wu2022grit], Kosmos-2 [@peng2023kosmos2] and ASM [@wang2023allseeing].

**Results.** As shown in Table 4, our model is capable of achieving the best performance on CIDEr across all of the baselines, which shows superiority of our NExT-Chat. Especially for Kosmos-2, we can beat the version with 4-shot examples.

# Conclusion

In this paper, we present a novel location modeling method called pixel2emb, which utilizes embeddings to achieve multiple location output formats, such as bounding boxes and segmentation masks. Through comprehensive exploratory experiments, we demonstrate the effectiveness of the proposed pix2emb method. Additionally, we train a LMM named NExT-Chat, which significantly broadens the range of application scenarios for LMMs. Our NExT-Chat exhibits the ability to handle diverse tasks, including visual grounding, region captioning, grounded captioning and complex question reasoning. In the future, we will continue to enhance the model's ability on conducting better detection and segmentation. Another promising direction is to extend the NExT-Chat model to multimodal agent which can handle complex tasks that requires region understanding.

# Limitation

In the training procedure, our dataset primarily comprises individual image inputs, resulting in a limitation of our NExT-Chat model when it comes to handling multiple image inputs. Furthermore, the absence of sufficient training data from diverse domains hinders the model's ability to generate accurate predictions in tasks involving medical and satellite image analysis.

# Author Contributions {#author-contributions .unnumbered}

Ao Zhang initializes the project, conducts experiments and writes the main part of the paper. Wei Ji and Yuan Yao proof read the paper. Tat-Seng Chua, Zhiyuan Liu and Yuan Yao provides valuable suggestions on the paper structure, experiment design and paper revision.

<a id="fig:demo_grd"></a>
![](../images/NExT-Chat_md_images/figs/demo/demo_grd.pdf.png){width="100%"}

**Figure 3.** Visual grounding examples of NExT-Chat.

<a id="fig:demo_grd_cplex"></a>
![Hard visual grounding examples of NExT-Chat.](../images/NExT-Chat_md_images/figs/demo/demo_grd_complex.pdf.png){width="100%"}

**Figure 4.** Hard visual grounding examples of NExT-Chat.

<a id="fig:demo_region_cap"></a>
![](../images/NExT-Chat_md_images/figs/demo/demo_region_cap.pdf.png){width="100%"}

**Figure 5.** Region captioning examples of NExT-Chat.

<a id="fig:demo_grd_cap"></a>
![](../images/NExT-Chat_md_images/figs/demo/demo_grd_cap.pdf.png){width="100%"}

**Figure 6.** Grounded captioning examples of NExT-Chat.

<a id="fig:demo_reason"></a>
![](../images/NExT-Chat_md_images/figs/demo/demo_reason.pdf.png){width="100%"}

**Figure 7.** Reasoning examples of NExT-Chat.

[^1]: <https://github.com/luca-medeiros/lightning-sam/tree/main>
