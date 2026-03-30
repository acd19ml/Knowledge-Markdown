# Introduction {#sec:intro}

![](../images/Shikra_md_images/figures/case/teaser.pdf.png)
**Figure 1.** **Demo of Referential Dialogue (RD).** Users can point to specific areas and ask questions. In turn, Shikra will indicate the specific regions when replying, if necessary.

In recent months, Multimodal Large Language Models (MLLMs) have witnessed remarkable progress [@alayrac2022flamingo; @kosmos; @liu2023llava; @zhu2023minigpt; @li2023otter; @gao2023la_v2; @dai2023instructblip]. They bring eyes to Large Language Models (LLMs), where users can talk about the input image. However, although these models can perceive image content, they cannot engage in dialogue with users regarding the precise positions of the content. Users cannot indicate areas of interest in the image, and the models cannot provide the exact locations of the described content. Differently, as shown in Figure 1, in human daily communication, different regions or objects in the scene are often attended to, and people can speak and point to these regions for efficient information exchange. We refer to this interaction mode as Referential Dialogue (RD). If an MLLM excels in this skill, it will bring numerous exciting applications. For instance, when applied to Mixed Reality (XR) headsets like Apple Vision Pro, users can indicate anything to converse with the AI assistant, and the assistant can display the prompted area in the field of view when necessary. It can also assist visual robots in communicating with individuals by comprehending their specific reference positions, and facilitate online shopping by enabling users to inquire about items of interest in an image.

In this paper, we evolve MLLMs to open the veil of referential dialogue. We create Shikra[^1], a unified model capable of handling inputs and outputs of spatial coordinates. All coordinates, both input and output, are represented in natural-language numerical form without introducing any extra vocabularies or position encoder. The Shikra architecture comprises a vision encoder, an alignment layer, and an LLM. We do **not** introduce any pre-/post-detection modules or external plug-in models, making Shikra unified and simple. We provide several real conversations with users in Figure 2 and the appendix, where users can use it to compare the differences of multiple regions, inquire about the meaning of a thumbnail, discuss specific objects, and so on. Shikra can provide explanations when answering a question, not only verbally but also spatially.

Referential dialogue is a superset of many vision-language (VL) tasks. Shikra, skilled in RD, can naturally work on these tasks with promising performance, including Visual Question Answering (VQA), image captioning, and location-related tasks such as Referring Expression Comprehension (REC) and PointQA. We illustrate some of them in Figure 2. For more quantitative results, please refer to the experiment section. Besides, this paper also addresses intriguing questions, such as how to represent position in an image, whether previous MLLMs possess the capability to comprehend absolute positions, and whether the reasoning process with location information can assist in providing more accurate answers to questions. We hope these analysis experiments can inspire future research on MLLMs.

The main contributions of this paper are:
- It introduces the task of Referential Dialogue (RD), an essential component of everyday human communication with extensive practical applications.
- It presents Shikra, a generalist MLLM for RD that is simple and unified, **without** extra vocabularies, pre-/post-detection modules, or external plug-in models.
- It shows that Shikra handles unseen settings effortlessly and achieves promising performance on conventional VL tasks such as REC, PointQA, VQA, and Image Captioning, without task-specific finetuning.

![](../images/Shikra_md_images/figures/case/cases.pdf.png)
**Figure 2.** **Referential dialogues between real users and Shikra-7B.** The dashed box on an image represents the area referred to by the user or jointly referred to by Shikra, while the solid box represents the area solely referred to by Shikra.

# Related Works {#sec:related_work}

## Multimodal Large Language Model

Expanding large language models into multimodal versions has garnered widespread attention. Flamingo [@alayrac2022flamingo] integrates visual adaptation layers into an LLM and is trained on a large-scale interleaved image-text dataset. OpenFlamingo re-implements Flamingo and releases it to the community. Other lines include MM-GPT and Otter, which tune on carefully constructed instruction data for more user-friendly interaction, and BLIP-2, which aligns queried visual features with text using multiple vision-language losses through Q-Former. MiniGPT-4, mPLUG-OWL, VPGTrans, and InstructBLIP retain Q-Former while replacing the language model with a larger one and then tuning on carefully collected instruction data. Simpler and more direct methods also exist: FROMAGe and LLaVA directly feed visual features to the LLM using only a learnable fully connected layer. Closed-source GPT-4 also demonstrates astonishing image comprehension capabilities.

## Vision-Language Positioning Tasks

Many vision-language tasks require localization representation. **Tasks with output boxes** include REC and described object detection. **Tasks with input boxes** include Grounding Caption, Referring Expression Generation, and PointQA. **Differently**, Shikra is not only compatible with these tasks, but can also flexibly and simultaneously handle the input and output of position representation, bringing Referential Dialogue and extending new dimensions to positional tasks.

## Position Representation {#sec:pos_rep}

**Inputting** regions of interest into the model presents various approaches. Some methods directly concatenate cropped image patches with the original image as model input. Others use binary masks or Gaussian maps to emphasize the area of user interest. Some methods first encode points and boxes into positional embeddings and then add them to intermediate features or learned queries. **Outputting** regions of interest is also a highly active area, spanning anchor-based methods, one-stage coordinate regression, end-to-end detectors, and sequence-generation methods like Pix2Seq. Following Pix2Seq, several methods introduce extra coordinate vocabularies alongside language vocabularies. **Differently**, Shikra formulates position input and output as the most natural and flexible form of language, and compares this design against extra coordinate vocabularies in Table 2.

# Referential Dialogue {#sec:dialogue}

To better understand the interesting abilities of our model, we demonstrate real users' communications in Figure 1 and Figure 2. As shown in the first demo of Figure 1, the user points to two deer and inquires, "What is the difference between this deer and another deer?" When Shikra answers, it not only mentions the differences but also outputs the coordinates of the differences. The subsequent examples in Figure 2 are alike. To our knowledge, there have been no unified models that can achieve such functionality before. RD is a superset of numerous vision-language tasks. Shikra can perform most tasks that current MLLMs can, including VQA, image captioning, and multimodal dialogue. Furthermore, it handles tasks that they cannot, such as REC, REG, and PointQA. The model also demonstrates proficiency in tasks not in the training set, such as identifying similarities between two indicated objects or counting objects and providing their positions. We show more results in the appendix, and readers interested in quantitative experiments can refer to the later experiment section.

# Chessboard Test for Current MLLM {#sec:chessboard}

Can current MLLMs understand absolute spatial positions? The current MLLM models cannot directly output coordinates. Therefore, the paper designs a chessboard test that simplifies object grounding into a part-choice task. Specifically, it divides an image into a $2\times2$ chessboard and asks the model to identify which quadrant contains a queried object. The test data are constructed from LVIS, selecting 600 images per part for a total of 2,400 images across 945 categories. Using LLaVA-13B, the results are unsatisfactory and close to random selection, suggesting that prior coarse-grained vision-language alignment pre-training may be inadequate for MLLMs to capture exact spatial positions.

# Breeding Shikra {#sec:tuning}

This section introduces the birth of Shikra, including its structure design, position representation, training data construction, and training strategies.

## Architecture

We select the pre-trained ViT-L/14 of CLIP as the visual encoder and Vicuna-7/13B as our LLM. We use one fully connected layer to map the ViT output embedding $V\in\mathbb{R}^{16\times16\times1024}$ to aligned visual tokens with the correct LLM input dimension. Visual embedding can be inserted anywhere in the input sequence. During training, both the fully connected layer and the entire language model are involved. We do not introduce any vocabulary or special encoder for encoding position information, and we do not introduce additional pre-/post-detectors for points or bounding boxes. The model using Vicuna-7B is called Shikra-7B, and the one using Vicuna-13B is named Shikra-13B.

## Numerical representation of position

We represent position using numerical values in natural language in a highly intuitive manner. We use `[x_min, y_min, x_max, y_max]` to denote a bounding box and `[x_center, y_center]` to denote a region center point. `x` and `y` are normalized according to the size of the image, and we default to keeping three decimal places for each number. These coordinates can appear anywhere in the input and output sequence of the model. The square brackets that record coordinates naturally appear in sentences and can serve as any sentence component, like regular text tokenized without discrimination.

## Instruction data construction

Shikra is trained with two types of data: reorganized public datasets, and high-quality RD data built from Flickr30K Entities using GPT-4.

### Reorganization of public data {#sec:reorg}

We collect training data from public VQA and image captioning datasets, as well as several datasets already containing positional annotation, such as RefCOCO for REC/REG, Visual Genome for grounding caption, and Visual-7W for PointQA. We also define new task forms, such as Spotting Captioning, which requires the model to describe the image and spot the mentioned objects or regions using points or boxes. All the training data are listed in Table 8. Note that all the data used were included in the reported model results unless stated otherwise for specific comparative experiments. Additionally, we **exclude** images present in test and validation sets from the training data to prevent potential data leakage, despite their distinction in terms of image-text pairs.

### Generated data {#sec:gendata}

The existing publicly available data are not sufficient to train an MLLM skilled in RD, as they lack CoT data with positional annotations, natural communication data with positional annotations, and similar signals. We resort to GPT-4 to obtain high-quality RD annotations from Flickr30K Entities. Flickr30K Entities has five descriptions for each image, and the mentioned objects appearing in the image are labeled using bounding boxes. Although the API of GPT-4 temporarily **cannot** see images, we explain the format of the bounding boxes to GPT-4 and ask it to understand the image through these five sentences and boxes. Next, we require GPT-4 to design QA pairs, where the questions must be answerable from known information. In this way, we generate 5,922 QA pairs, where coordinate information may appear in both questions and answers. The dataset will continue expanding in the future, and the paper refers to it as Shikra-RD.

### Task prompts

We construct variable task templates for different tasks. For instance, for spotting captioning, we can use prompts that ask the model to provide a description of the image and include coordinates for each mentioned object; for PointQA, prompts that ask it to answer a visual question while referring to a given point; and for REC, prompts that directly request the bounding-box coordinates of an expression. More templates are summarized in Table 9. It should be noted that we cannot use an invariant task template for a specific type of task, because in that case the model cannot flexibly accept user instructions. To solve this problem, we first describe the purpose of specific tasks, write a sample template, and then have GPT-4 rewrite it in rich language, expanding it into hundreds of variations that convey the same meaning. During training, we randomly choose from them.

## Tuning details

Shikra is trained in two stages. In the first stage, we train it on the reorganized VL dataset for 100,000 steps, around 1.5 epochs. In the second stage, we raise the sampling ratio to 50% on LLaVA-Instruct-150K and our generated RD data. In both stages, we freeze the visual encoder and tune all parameters in the LLM. We adopt AdamW as the optimizer and cosine annealing as the learning-rate scheduler, with an initial learning rate of `2e-5` and a global batch size of 64. All training runs on 8 NVIDIA A100 GPUs. It takes around 100 hours for stage-one training and 20 hours for stage-two training.

# Experiment and Analysis {#sec:experiment}

<a id="tab:clevr"></a>
**Table 1.** **Comparing different forms of CoTs.** Q, A, C, and $\text{C}^\text{Point}$ denote the **Q**uestion, final **A**nswer, **C**hain of thoughts, and **C**hain of thoughts with **P**ointing.

| Q→A | Q→CA | Q→C^Point A |
| --- | --- | --- |
| 88.07 | 80.68 | 93.97 |

## Grounding CoT or verbal CoT? {#sec:clevr}

The process of providing reasoning before giving an answer is called Chain of Thoughts (CoT), which provides explanatory reasoning during model judgments. However, CoT often suffers from hallucinations. In this section, the paper investigates whether CoT with position annotations can reduce hallucinations and improve model performance. This type of CoT is referred to as Grounding CoT (GCoT). Three toy settings are trained on CLEVR: direct Question→Answer, Question→CoT→Answer, and Question→GCoT with center-point annotation→Answer. Table 1 shows that using only verbal CoT decreases performance, while GCoT with positional annotations improves performance over both baselines.

<a id="tab:numer"></a>
**Table 2.** **Comparing different position representations.** `Vocab.` means using extra vocabularies to represent coordinates; `Numerical` means directly using numerals in natural language.

| Dataset | Split | Vocab. | Numerical |
| --- | --- | --- | --- |
| RefCOCO | val | 81.03 | 81.47 |
| RefCOCO | test-A | 86.94 | 87.40 |
| RefCOCO | test-B | 70.91 | 73.25 |
| RefCOCO+ | val | 72.32 | 74.30 |
| RefCOCO+ | test-A | 81.78 | 83.29 |
| RefCOCO+ | test-B | 59.95 | 63.08 |
| RefCOCOg | val-u | 72.81 | 75.69 |
| RefCOCOg | test-u | 73.78 | 75.52 |

## Location tokens or just numbers? {#sec:loc}

Several methods introduce extra coordinate vocabularies to represent positions for object detection in spatially discretized images. In contrast, Shikra represents coordinates naturally and intuitively using numbers directly. Which form is better? The paper trains two toy Shikra models using the two different representations with REC data; their performance is recorded in Table 2, where using numbers directly achieves better results. Numerical representation also keeps the model elegant without modifying vocabularies for localization tasks, though it requires more tokens for dense objects.

## Quantitative results on conventional tasks {#sec:experiment_vltask}

Shikra excels in Referential Dialogue and can be seamlessly integrated into a wide range of vision-language tasks, particularly those related to positioning. To demonstrate positioning capability, the paper examines the REC task and compares Shikra with both generalist VL models and specialist SOTAs. Table 5 shows that Shikra achieves promising performance among generalist models.

<a id="tab:experiment_v7w"></a>
**Table 3.** **Comparing pointQA capabilities on Visual-7W.** Visual-7W features a "which box" setting requiring the model to select one matching box from four options. Accuracy (%) is used for evaluation.

| Zhu et al. | Hu et al. | 12-in-1 | 12-in-1* | Shikra |
| --- | --- | --- | --- | --- |
| 56.10 | 72.53 | 82.75 | 83.35 | 85.33 |

Correspondingly, to quantitatively evaluate understanding of position inputs, the paper evaluates the model on two PointQA datasets: LookTwice-QA and Visual7W. Shikra achieves SOTA performance in all these settings, as shown in Table 3 and Table 4.

<a id="tab:twiceqa"></a>
**Table 4.** **Comparing pointQA capabilities on LookTwice-QA.** Pronoun, Superclass (Super cls.), and Class indicate different levels of referential clarity in the question. Accuracy (%) is reported using Shikra-13B.

| Type | Point: Mani et al. | Point: Shikra | Box: Mani et al. | Box: Shikra |
| --- | --- | --- | --- | --- |
| Pronoun | 56.5 | 70.0 | 60.2 | 70.3 |
| Super cls. | 59.1 | 70.2 | 59.8 | 71.4 |
| Class | 62.8 | 71.8 | 61.4 | 72.3 |

<a id="tab:rec"></a>
**Table 5.** **Results on standard REC task.** Shikra is compared against both generalist VL models without finetuning and specialist localization models.

| Model type | Model | RefCOCO val | test-A | test-B | RefCOCO+ val | test-A | test-B | RefCOCOg val-u | test-u | GRIT refexp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Generalist w/o finetuning | GPV-2 | - | - | - | - | - | - | - | - | 51.50 |
| Generalist w/o finetuning | OFA-L* | 79.96 | 83.67 | 76.39 | 68.29 | 76.00 | 61.75 | 67.57 | 67.58 | 61.70 |
| Generalist w/o finetuning | Unified-IO | - | - | - | - | - | - | - | - | 78.60 |
| Generalist w/o finetuning | OFASys | - | 80.10 | - | - | - | - | - | - | - |
| Generalist w/o finetuning | VisionLLM-H | - | 86.70 | - | - | - | - | - | - | - |
| Generalist w/o finetuning | **Shikra-7B** | 87.01 | 90.61 | 80.24 | 81.60 | 87.36 | 72.12 | 82.27 | 82.19 | 69.34 |
| Generalist w/o finetuning | **Shikra-13B** | 87.83 | 91.11 | 81.81 | 82.89 | 87.79 | 74.41 | 82.64 | 83.16 | 69.03 |
| Specialist / finetuned | G-DINO-L | 90.56 | 93.19 | 88.24 | 82.75 | 88.95 | 75.92 | 86.13 | 87.02 | - |
| Specialist / finetuned | UNINEXT-H | 92.64 | 94.33 | 91.46 | 85.24 | 89.63 | 79.79 | 88.73 | 89.37 | - |
| Specialist / finetuned | ONE-PEACE | 92.58 | 94.18 | 89.26 | 88.77 | 92.21 | 83.23 | 89.22 | 89.27 | - |

Additionally, the paper assesses the model on conventional VL tasks such as VQA and image captioning, which do not require coordinates in their input or output. These results are shown in Table 6. The POPE object hallucination evaluation is summarized in Table 7.

<a id="tab:vl"></a>
**Table 6.** **Comparing generalist models on VQA and Image Captioning.** For VQA, the paper evaluates SOTA generalist models and Shikra-13B on VQAv2 and OK-VQA following the normalization rules. For image captioning, results are reported in CIDEr on Flickr30k and COCO. The paper abbreviates Flamingo as `FM`.

| Dataset group | Dataset | Shikra | FM-80B | FM-9B | Kosmos-1 | BLIP-2 | Unified-IO | VPGTrans | VisionLLM |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VQA | VQAv2 val | 75.33 | - | - | - | 65.2 | - | 65.2 | - |
| VQA | VQAv2 dev | 77.36 | 56.3 | 51.8 | 51.0 | 65.0 | 77.9 | - | - |
| VQA | VQAv2 std | 77.51 | - | - | - | - | - | - | - |
| VQA | OK-VQA | 47.16 | 50.6 | 44.7 | - | 45.9 | 54.0 | 45.0 | - |
| Caption | Flickr30k | 73.9 | 67.2 | 61.5 | 67.1 | - | - | - | - |
| Caption | COCO | 117.5 | 84.3 | 79.4 | 84.7 | - | 122.3 | - | 114.2 |

<a id="tab:pope_results"></a>
**Table 7.** **Object hallucination benchmark using the POPE evaluation pipeline.** Accuracy denotes the accuracy of predictions. Precision signifies the true positive samples among the predicted positives. Recall indicates the correct identification of all true positive samples. `Yes` represents the probability of the model outputting a positive answer. Except for Shikra, the other results are reported from the cited POPE source paper.

**Random subset**

| Metric | Shikra | InstructBLIP | MiniGPT-4 | LLaVA | MM-GPT | mPLUG-Owl |
| --- | --- | --- | --- | --- | --- | --- |
| Accuracy | 86.90 | 88.57 | 79.67 | 50.37 | 50.10 | 53.97 |
| Precision | 94.40 | 84.09 | 78.24 | 50.19 | 50.05 | 52.07 |
| Recall | 79.27 | 95.13 | 82.20 | 99.13 | 100.00 | 99.60 |
| F1-Score | 86.19 | 89.27 | 80.17 | 66.64 | 66.71 | 68.39 |
| Yes | 43.26 | 56.57 | 52.53 | 98.77 | 99.90 | 95.63 |

**Popular subset**

| Metric | Shikra | InstructBLIP | MiniGPT-4 | LLaVA | MM-GPT | mPLUG-Owl |
| --- | --- | --- | --- | --- | --- | --- |
| Accuracy | 83.97 | 82.77 | 69.73 | 49.87 | 50.00 | 50.90 |
| Precision | 87.55 | 76.27 | 65.86 | 49.93 | 50.00 | 50.46 |
| Recall | 79.20 | 95.13 | 81.93 | 99.27 | 100.00 | 99.40 |
| F1-Score | 83.16 | 84.66 | 73.02 | 66.44 | 66.67 | 66.94 |
| Yes | 45.23 | 62.37 | 62.20 | 99.40 | 100.00 | 98.57 |

**Adversarial subset**

| Metric | Shikra | InstructBLIP | MiniGPT-4 | LLaVA | MM-GPT | mPLUG-Owl |
| --- | --- | --- | --- | --- | --- | --- |
| Accuracy | 83.10 | 72.10 | 65.17 | 49.70 | 50.00 | 50.67 |
| Precision | 85.60 | 65.13 | 61.19 | 49.85 | 50.00 | 50.34 |
| Recall | 79.60 | 95.13 | 82.93 | 99.07 | 100.00 | 99.33 |
| F1-Score | 82.49 | 77.32 | 70.42 | 66.32 | 66.67 | 66.82 |
| Yes | 46.50 | 73.03 | 67.77 | 99.37 | 100.00 | 98.67 |

# Limitations {#sec:limitations}

Shikra only supports English and is not user-friendly for non-English speakers. Making Shikra multilingual in the future is valuable. Shikra is unsuitable for dense object detection and segmentation tasks. Exploring improved coordinate representations for these tasks is also interesting. Shikra, like most LLMs, may produce harmful and counterfactual responses.

# Conclusion {#sec:conclusion}

Our study unveils the critical gap in MLLMs' ability to understand and engage in referential dialogue, an integral aspect of human communication. To address this, we introduce Shikra, a unified, straightforward model designed to comprehend and output spatial coordinates in natural language. Our approach does not require extra vocabularies, position encoders, or external plug-ins, preserving the model's simplicity. It is shown that Shikra performs notably well on a variety of conventional vision-language tasks, while offering swathes of exciting applications such as aiding AI assistants in Mixed Reality headsets or facilitating precise communication in online shopping scenarios.

# Details of All Training Data {#sec:train_data}

<a id="tab:all_data"></a>
**Table 8.** **All training data used by Shikra.** The asterisk indicates that this data is only used in the second stage.

| Task | Dataset |
| --- | --- |
| Captioning | LLaVA-Pretraining |
| Spotting Cap. | Flickr30K Entities |
| Grounding Cap. | Visual Genome |
| REG | RefCOCO, RefCOCO+, RefCOCOg |
| REC | RefCOCO, RefCOCO+, RefCOCOg, Visual Genome |
| VQA | VQAv2 |
| PointQA | PointQA-Local/Twice, Visual-7W (`which box` subset) |
| Dialogue | LLaVA-Instruct-150K* |
| RD | VCR, Shikra-RD (generated data from Flickr30K Entities)* |

The asterisk indicates data that are only used in the second training stage. The authors removed images from the training set that also appear in testing or validation sets to prevent data leakage.

# Examples of Task Prompts {#sec:task_temp}

<a id="tab:task_temp"></a>
**Table 9.** **Examples of task templates used by Shikra on different types of training data.** The placeholders are as follows: `<image>` is the input image, `<objs>` denotes center points or boxes of user-specified locations, `<question>` is a VQA question, and `<expr>` is the expression in REC.

**Captioning**
- `Describe this image <image> as simply as possible.`
- `What is the content of the image <image>? Please answer in short sentences.`
- `Summarize the content of the photo <image>.`

**Spotting Captioning**
- `Can you provide a description of the image <image> and include the coordinates [x0,y0,x1,y1] for each mentioned object?`
- `Please explain what's happening in the photo <image> and give coordinates [xmin,ymin,xmax,ymax] for the items you reference.`
- `How would you describe the contents of the image <image>? Please provide the positions of mentioned objects in square brackets.`

**Grounding Captioning**
- `Can you give me a description of the region <objs> in image <image>?`
- `Describe what's happening within the coordinates <objs> of the given image <image>.`
- `What does the area <objs> within the given visual <image> contain?`

**REG**
- `For the given image <image>, can you provide a unique description of the area <objs>?`
- `In the photo <image>, how would you describe the selected area <objs> uniquely?`
- `Can you provide a description for the region <objs> in the image <image> such that it sets it apart from others?`

**Q→A**
- `I want to know the answer to '<question>'. Refer to the image <image> and give a clear response.`
- `Answer this question directly after referring to the image <image>: <question>`
- `Examine the image <image> and provide a brief answer for '<question>'`

**Q→CA**
- `Having a look at image <image>, can you tell me the answer to my question '<question>' and the logic leading to it?`
- `Please answer the following question '<question>' based on the image <image>, and describe your thought process.`
- `Upon analyzing the image <image>, please find the answer to my question '<question>' and provide a detailed explanation.`

**Q→C^Point A**
- `Analyze the image <image> and answer '<question>'. Include your reasoning process and mark center points of related objects as [cx, cy].`
- `Based on <image>, please respond to '<question>'. Include your thought process and note involved objects using [cx, cy] for their center points.`
- `While observing image <image>, kindly answer '<question>'. Elaborate on your reasoning process and tag any object center points involved [x,y].`

**Q→C^Box A**
- `<question> Please offer your reasoning process, and provide bounding boxes of mentioned objects within square brackets. Here is the picture <image>.`
- `Please explain your reasoning and provide bounding boxes, denoted by square brackets, for the objects mentioned in the picture <image>. <question>`
- `Consider the image <image>, and then provide a well-reasoned answer to the question '<question>'. Don't forget to mark relevant object locations using [x0,y0,x1,y1].`

**REC**
- `In the given <image>, could you find and tell me the coordinates of <expr>?`
- `I need the coordinates of <expr> in <image>, can you please assist me with that?`
- `Locate <expr> in <image> and provide its coordinates, please.`

# More Conversations with Shikra {#sec:more_cases}

The paper provides additional dialogue records of Shikra-7B in this section. It showcases RD results in Figure 3, VQA (`Q→C^Box A`) in Figure 4, Spotting Captioning in Figure 6, OCR in Figure 5, REC in Figure 8, REG in Figure 7, and PointQA variants in Figure 9 and Figure 10.

![](../images/Shikra_md_images/figures/case/shikra_case_2.pdf.png)
**Figure 3.** **Referential Dialogue using Shikra-7B.** The dashed box on an image represents the area referred to by the user or jointly referred to by Shikra, while the solid box represents the area solely referred to by Shikra.

![](../images/Shikra_md_images/figures/case/shikra_case_3.pdf.png)
**Figure 4.** **Q→C^Box A using Shikra-7B.** It asks models to generate a grounded explanation for the answer.

![](../images/Shikra_md_images/figures/case/shikra_case_4.pdf.png)
**Figure 5.** **OCR using Shikra-7B.** The paper notes that explicit OCR datasets are not used in Shikra training.

![](../images/Shikra_md_images/figures/case/shikra_case_5.pdf.png)
**Figure 6.** **Spotting Captioning using Shikra-7B.** The task requires the model to describe the image and spot the mentioned objects or regions using points or boxes.

![](../images/Shikra_md_images/figures/case/shikra_case_6.pdf.png)
**Figure 7.** **Referring Expression Generation (REG) using Shikra-7B.** The purpose of REG is to generate a unique description for a specified location.

![](../images/Shikra_md_images/figures/case/shikra_case_7.pdf.png)
**Figure 8.** **Referring Expression Comprehension (REC) using Shikra-7B.** The task aims to localize a target object in an image described by a referring expression.

![](../images/Shikra_md_images/figures/case/shikra_case_8.pdf.png)
**Figure 9.** **PointQA using Shikra-7B.** The task asks models to answer questions about the region specified by the user, either by center point or box.

![](../images/Shikra_md_images/figures/case/shikra_case_9.pdf.png)
**Figure 10.** **PointQA-V7W using Shikra-7B.** PointQA-V7W provides a setting for point QA where models are given a question and four box options and should choose one as the answer.

[^1]: Shikra is a hunter's companion, capable of understanding human language and gesture instructions, and locating and capturing prey in the wild.
