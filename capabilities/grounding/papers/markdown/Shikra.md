# Introduction {#sec:intro}

![](../images/Shikra_md_images/figures/case/teaser.pdf.png){width="100%"}

*Demo of Referential Dialogue (RD). Users can point to specific areas and ask questions. In turn, Shikra will indicate the specific regions when replying, if necessary.*

In recent months, Multimodal Large Language Models (MLLMs) have witness remarkable progress [@alayrac2022flamingo; @kosmos; @liu2023llava; @zhu2023minigpt; @li2023otter; @gao2023la_v2; @dai2023instructblip]. They brings eyes to Large Language Models (LLMs), where users can talk about the input image. However, although these models can perceive image content, they cannot engage in dialogue with users regarding the precise positions of the content. Users cannot indicate areas of interest in the image, and the models cannot provide the exact locations of the described content. Differently, as shown in , in human daily communication, different regions or objects in the scene are often attended to, and people can speak and point to these regions for efficient information exchange. We refer to this interaction mode as Referential Dialogue (RD). If an MLLM excels in this skill, it will bring numerous exciting applications. For instance, applying it to Mixed Reality (XR) headsets like Apple Vision Pro, users can indicate anything to converse with the AI assistant. The AI assistant can display the prompt area in the field of view when necessary. It also assists visual robots in communicating with individuals by comprehending their specific reference positions. It facilitates online shopping by enabling users to inquire about items of interest in an image.

In this paper, we evolve MLLM to open the veil of referential dialogue. We create Shikra[^1], a unified model capable of handling inputs and outputs of spatial coordinates. All coordinates, both input and output, are represented in natural language numerical form without introducing any extra vocabularies or position encoder. The Shikra architecture comprises a vision encoder, an alignment layer, and a LLM. We do **not** introduce any pre-/post-detection modules or external plug-in models, making Shikra unified and simple. We provide several real conversations with users in the and , where users can use it to compare the differences of multiple regions, inquire about the meaning of the thumbnail, discuss specific objects, . Shikra can provide explanations when answering any question, not only verbally but also spatially.

Referential dialogue is a superset of many vision-language (VL) tasks. Shikra, skilled in RD, can naturally work on these tasks with promising performance, including Visual Question Answering (VQA), image captioning, and location-related tasks such as Referring Expression Comprehension (REC) and PointQA, We illustrate some of them in . For more quantitative results, please refer to . Besides, this paper also addresses intriguing questions, such as how to represent position in an image (). Do previous MLLMs possess the capability to comprehend absolute positions? (). Can the reasoning process with location information assist in providing more accurate answers to questions? (). We hope that these analysis experiment can inspire future research on MLLMs.

The main contributions of this paper are:

- This paper introduces the task of Referential Dialogue (RD), which is an essential component of everyday human communication and possesses extensive practical applications.

- We present Shikra, a generalist MLLM, for RD. Shikra is simple and unified, **without** introducing extra vocabularies, pre-/post-detection module, or external plug-in models.

- Shikra handles unseen settings effortlessly, creating diverse application scenarios. It also achieves promising performance on conventional visual language tasks such as REC, PointQA, VQA, and Image Captioning, without finetuning.

![](../images/Shikra_md_images/figures/case/cases.pdf.png){width="97%"}

*Referential dialogues between real users and Shikra-7B. The dashed box on an image represents the area referred to by the user or jointly referred to by Shikra, while the solid box represents the area solely referred to by Shikra.*

# Related Works {#sec:related_work}

## Multimodal Large Language Model

Expanding the large language model to a multimodal version has garnered widespread attention. Flamingo [@alayrac2022flamingo] integrates visual adaption layers (like Perceiver) to an LLM, and trained on a large-scaled interleaved image-text dataset. OpenFlamingo [@anas2023OpenFlamingo] re-implements Flamingo and releases it to the community along with an M3C dataset. Subsequently, MM-GPT [@gong2023mmgpt], and Otter [@li2023otter] tune on carefully constructed instruction data for a more user-friendly interaction. Another genre is BLIP-2 [@li2023blip2], which align queried visual feature with text using multiple vision-language losses (model named Q-Former), and tunes a simple fully connection layer to feed the queried embedding to a frozen language model. Mini-GPT4 [@zhu2023minigpt], mPLUG-OWL [@ye2023mplug], VPGTrans [@zhang2023transfer], and InstructBLIP [@dai2023instructblip] retain Q-Former, replace language model to a larger one, and then tuning on meticulously collected instruction data. Additionally, there are simpler and more direct methods: FROMAGe [@koh2023fromge] and LLaVA [@liu2023llava] directly feed visual features to the LLM using only a learnable fully connected layer. The closed source business model GPT-4 [@openai2023gpt4] also demonstrates astonishing image comprehension capabilities. Recently, interesting works have made remarkable progress by extending LLM to audio, , KOSMOS-1 [@kosmos], X-LLM [@chen2023xllm], PandaGPT [@su2023pandagpt] and control systems like PaLM-E [@driess2023palme] and EmbodiedGPT [@mu2023embodiedgpt]

## Vision-Language Positioning Tasks

Many vision-language tasks require localization representation. **Tasks with output boxes**: Referring Expression Comprehension (REC) [@kazemzadeh2014refcoco; @mao2016refcocog] aims to localize a target object in an image described by a referring expression.

Described Object Detection [@xie2023dod] extends REC to more realistic scenarios where the object may not exist or there may be multiple objects. VQA Grounding aims to answer visual questions and associate the answers with specific visual regions or objects. **Tasks with input boxes**: Given an image and a location box, the task of Grounding Caption (GC) [@zhou2020more] is to generate a description for this location by considering the surrounding environment. Compared to GC, Referring Expression Generation (REG) [@liu2017referring] requires the generated description to indicate that it describes this region specifically, not others, making it necessary for the description to be discriminative. PointQA [@mani2020pointqa] requires a model answer for a visual question where the questioner queries a specific position in the picture. **Differently**, our model is not only compatible with the above tasks, but also can handles the input and output of position representation flexibly and simultaneously, bringing Referential Dialogue and extending new dimensions to positional tasks.

## Position Representation {#sec:pos_rep}

**Inputting** regions of interest into the model presents various approaches. Some methods [@bracha2023disclip] directly concatenate cropped image patches with the original image as model input. There are also some methods [@lin2020fca; @lin2022mmiis] that use 0/1 mask or Gaussian map input with the original image to emphasize the area of user interest. Some methods [@tancik2020fourier; @kirillov2023sam] first encode points and boxes to positional encodings then add them to intermediate features or learned queries. **Outputting** regions of interest is a highly focused technique, existing many positioning paradigms . Anchor-based methods utilize predefined sliding windows and proposal candidate regions for classification., , Fast R-CNN [@girshick2015fastrcnn]. Some one-stage methods remove anchors and directly regress four values for bounding box coordinates, , FCOS [@tian2019fcos]. Some methods adopt one-to-one label assignment to evolve object detection into an end-to-end manner, , DETR [@carion2020detr] and POTP [@wang2021end]. An interesting genre is Pix2seq [@chen2021pix2seq], which formalizes the detection task as a sequence generation task. It desires the spatial position of the image in 1,000 bins and uses a 1,000-token vocabulary to represent it. For detection, Pix2seq performs classification on the coordinate vocabulary in an auto-regressive manner. Following Pix2seq, several methods, , OFA [@wang2022ofa], Unified-IO [@lu2022unified], UniTab [@yang2022unitab], GIT [@wang2022git], and VisionLLM [@wang2023visionllm] introduce similar coordinate vocabulary alongside the language vocabulary for object detection and REC tasks. **Differently**, Shikra formulates position input/output as the most natural and flexible form of language and compare it with the extra coordinate vocabulary in .

# Referential Dialogue {#sec:dialogue}

To better understand the interesting abilities of our model, we demonstrated real users' communications in and . As shown in the first demo of , the user points to two deer, and inquires, "*What is the difference between this deer and another deer?*" When Shikra answered, she not only mention the differences but also output the coordinates of the differences. The subsequent examples in are alike. To our knowledge, there have been no unified models that can achieve such functionality before. RD is a superset of numerous vision-language tasks. Shikra can perform most tasks like current MLLM, including VQA, Image Caption, and multimodal dialogue. Furthermore, it handles tasks that they cannot, like REC, REG, and PointQA. The model demonstrates proficiency in tasks not in the training set, such as identifying similarities between two indicated objects, or counting somethings, and providing their positions. We show more results in . If you are interested in quantitative experiments, you can refer to later.

# Chessboard Test for Current MLLM {#sec:chessboard}

Can the current MLLM model understand absolute spatial positions? The current MLLMs cannot directly output coordinates; thus, in this section, we designed a chessboard test, which simplifies the object grounding into a part choice task. Specifically, we divide a image into a $2\times2$ chessboard. Next, we ask, "*\<image\> Which part is \<expr\> in if the picture is divided equally into four 2 by 2 parts? Choose from: (A) Top-left (B) Top-right (C) Bottom-left (D) Bottom-right.*", where \<image\> and \<expr\> denote input image tokens and Class name. We construct test data from LVIS [@gupta2019lvis], which is a perception detection with over 1000 entry-level object categories. We choose objects that are completely within a certain part (, ambiguous positions are not considered). In total, we select 600 images per part, resulting in 2,400 images across 945 categories. We employ LLaVA-13B [@liu2023llava] for the chessboard test , but the results are unsatisfactory. We tried various instruction methods, and LLaVA should achieve an accuracy of 25.96%, which is comparable to random selection. This suggests that prior coarse-grained vision-language alignment pre-training may be inadequate for MLLMs to capture the exact spatial position of an image. We need to explore appropriate coordinate representations and finer-grained training data.

# Breeding Shikra {#sec:tuning}

This section introduces the birth of Shikra, encompassing its structure design, position representation, training data construction, and training strategies.

## Architecture

We selected the pre-trained ViT-L/14 of CLIP as visual encoder and Vicuna-7/13B as our LLM. We use one fully connected layer to map the ViT's $16\times16\times$ output embedding $\mathmat{V}\in\mathbb{R}^{16\times 16\times 1024}$ to $\mathmat{V'}\in\mathbb{R}^{256\times D}$ for modal alignment and correct input dimension of LLM. $D$ is 4,096 for Vicuna-7B and 5,120 for Vicuna-13B. Visual embedding can be inserted into anywhere of input sequence. During training, both the fully connected layer and the entire language model are involved. We do not introduce any vocabulary or special encoder for encoding position information. We have not introduced additional pre-/post-detectors for points or bounding boxes. The model using Vicuna-7B is called Shikra-7B, and the other, using Vicuna-13B, is named Shikra-13B.

## Numerical representation of position

We represent the position using numerical values in Natural Language in a highly intuitive manner. We use $[x_\text{min},y_\text{min},x_\text{max},y_\text{max}]$ to denote the bounding box and $[x_\text{center},y_\text{center}]$ to denote region center point. $x$ and $y$ is normalized according to the size of the image. We default to keeping 3 decimal places for each number. These coordinates can appear anywhere in the input and output sequence of the model. For example, User Question: "*How many other clothes in the \<image\> are of the same color as the jacket $[0.268, 0.372]$?*". Shikra reply: "*The jacket $[0.268, 0.372]$ is green. We can find a T-shirt $[0.653, 0.532]$ and cropped pants $[0.569, 0.101]$ a with same green color. So the answer is two.*" The square brackets that record coordinates naturally appear in sentences and can serve as any sentence component. Like regular text, tokenizing without discrimination.

## Instruction data construction

We utilize two types of data to train Shikra: the reorganized public datasets, and the high-quality RD data built from Flickr30K Entities [@plummer2015flickr30ke] using GPT-4 [@openai2023gpt4].

### Reorganization of public data {#sec:reorg}

We collection training data from public VQA, Image Captioning datset, and several datasets already containing positional annotation, such as RefCOCO [@kazemzadeh2014refcoco] for REC/REG, visual gemone [@krishna2017visualgenome] for grounding caption, Visual-7W [@mani2020pointqa] for PointQA. We also define new task forms, such as Spotting Captioning, which requires the model to describe the image and spots the mentioned objects or regions using points or boxes. We use Flickr30K Entities for this task. All the data used and corresponding tasks can be found in . Note that all the data used were included in the reported model results, unless stated otherwise for specific comparative experiments. Additionally, it should be mentioned that we have **excluded** images present in the test and validation data from the training data to prevent potential data leakage, despite their distinction in terms of image-text pairs.

### Generated data {#sec:gendata}

The existing publicly available data is not sufficient to train an MLLM skilled in RD, as they lack CoT data with positional annotations, natural communication data with positional annotations, . We resort to GPT-4 to obtain high-quality RD annotations from Flickr30K Entities. Flickr30K Entities has five descriptions for each image. These mentioned objects appearing in the image will be labeled using bounding box. Although the API of GPT-4 temporarily **cannot** see images, we explained the format of the bounding boxes to GPT-4 and asked it to understand the image through these five sentences and boxes. Next, we require GPT-4 to design Q&A pairs. When designing problems, these questions must be able to determine answers from known information. In this way, we generated 5,922 QA pairs, where coordinate information may appear in both questions and answers. The dataset will continue expanding in the future. You can refer to it as Shikra-RD.

### Task prompts

We construct variable task templates for different tasks. For instance, for the spottingS caption task, we can use "*Can you provide a description of the image \<image\> and include the coordinates* \[x0,y0,x1,y1\] *for each mentioned object?*" where \<image\> represents the visual tokens. For PointQA, we can use "*Referring to point \<objs\> in image \<image\>, give a direct answer to '\<question\>'*" where \<objs\> denotes the coordinates of the region and \<question\> represents the question from the source dataset. For REC, "*In \<image\>, I need the bounding box coordinates of \<expr\>.*" where \<expr\> is the expression. More templates for different tasks can be found in the Appendix.

It should be noted that we cannot use an invariant task template for a specific type of task. In this case, the model cannot flexibly accept user instructions. To solve this problem, we first describe the purpose of specific tasks, write a sample template, and then have GPT-4 rewrite it in rich language, expanding it into hundreds of variations to convey the same meaning. During training, we can randomly choose from them. We provide details on some generated task templates in the .

## Tuning details

Shikra is trained in two stages. In the first stage, we train it on the reorganized VL dataset () for 100,000 steps (around 1.5 epoch); In the second stage, we raise the sampling ratio to 50% on LLaVA-Instruct-150K [@liu2023llava] and our generated RD data (). In both stages, we freeze the visual encoder and tune all parameters in LLM. We adopt AdamW [@DBLP:conf/iclr/LoshchilovH19adamw] as the optimizer and cosine annealing scheduler [@DBLP:conf/iclr/LoshchilovH17cos] as learning rate scheduler with an initial learning rate of 2e-5 and global batch size of 64. All training runs on 8 NVIDIA A100 GPUs. It takes around 100h for stage one training and 20h for stage two.

# Experiment and Analysis {#sec:experiment}

::: {#tab:clevr}
   Q$\rightarrow$A   Q$\rightarrow$CA   Q$\rightarrow$$\text{C}^\text{Point}$A
  ----------------- ------------------ ----------------------------------------
      1-3 88.07           80.68                         93.97

  : **Comparing different forms of CoTs.** We train three toy models of Shikra-7B (without using additional datasets) on the CLEVR dataset. Q, A, C, and $\text{C}^\text{Point}$ denote the **Q**uestion, final **A**nswer, **C**hain of thoughts, and **C**hain of thoughts with **P**ointing.
:::

[]{#tab:clevr label="tab:clevr"}

::: {#tab:numer}
  Dataset   Split     Vocab.   Numerical
  --------- -------- -------- -----------
  1-4       val       81.03      81.47
            test-A    86.94      87.40
            test-B    70.91      73.25
  1-4       val       72.32      74.30
            test-A    81.78      83.29
            test-B    59.95      63.08
  1-4       val-u     72.81      75.69
            test-u    73.78      75.52

  : **Comparing different position representations.** We implement Shikra-7B in two different representation forms and train two toy models solely on RefCOCO, RefCOCO+/g, and Visual Genome for controllable comparison. Vocab. means to use extra vocabularies to represent coordinates, like [@chen2021pix2seq; @wang2022ofa], and Numerical means to directly use numerals in natural language to express coordinates.
:::

[]{#tab:numer label="tab:numer"}

## Grounding CoT or verbal CoT? {#sec:clevr}

The process of providing reasoning before giving an answer is called Chain of the thoughts (CoT), which provides good explanatory during model judgments. However, CoT often suffer from hallucinations [@zhang2023mmcot], which often do not improve the performance of the final answer. Current MLLMs are also suffer from serious visual hallucination [@li2023obj_Hallucination]. In this section, we investigate whether CoT with position annotations can reduce hallucinations and improve model performance. In this paper, we refer to this type of CoT as Grounding CoT (GCoT). We train our Shikra-7B (without pre-training) on CLEVR [@johnson2017clevr] in three settings: 1) Only use Question and Answer (Q$\rightarrow$A); 2) Use Question, CoT, and answer (Q$\rightarrow$CA); 3) Use GCoT with Center Point annotation and answer (Q$\rightarrow$$\text{C}^\text{Point}$A). We record they performance in . Using only CoT to train the model (Q$\rightarrow$CA) and requiring a reasoning process before the final answer decreases performance compared to direct answering setting (Q$\rightarrow$A). In the Q$\rightarrow$$\text{C}^\text{Point}$A setting, we ask the model to provide CoT along with center points $[x_\text{center},y_\text{center}]$ for each mentioned object. Performance improved by 13 points compared to Q$\rightarrow$CA and 5.9 points compared to Q$\rightarrow$A, indicating that training with positional annotations suppresses visual hallucination. This is a preliminary attempt at GCoT, and it is a promising direction worth exploring.

## Location tokens or just numbers? {#sec:loc}

::: table*
:::

::: {#tab:experiment_v7w}
   @zhu2016v7w   @hu2017v7w_method1   @lu202012in1   @lu202012in1\*   Shikra
  ------------- -------------------- -------------- ---------------- --------
    1-5 56.10          72.53             82.75           83.35        85.33

  : **Comparing pointQA capabilities on the Visual-7W** [@zhu2016v7w]. Visual-7W features a 'which box' setting, requiring the model to select one matching box from four options based on the given description. Accuracy (%) is used for evaluation.
:::

[]{#tab:experiment_v7w label="tab:experiment_v7w"}

::: {#tab:twiceqa}
+:------------+:----------------:+:------:+:----------------:+:------:+
| Type        | Point                     | Box                       |
+-------------+------------------+--------+------------------+--------+
| Model       | @mani2020pointqa | Shikra | @mani2020pointqa | Shikra |
+-------------+------------------+--------+------------------+--------+
| 1-5 Pronoun | 56.5             | 70.0   | 60.2             | 70.3   |
+-------------+------------------+--------+------------------+--------+
| Super cls.  | 59.1             | 70.2   | 59.8             | 71.4   |
+-------------+------------------+--------+------------------+--------+
| Class       | 62.8             | 71.8   | 61.4             | 72.3   |
+-------------+------------------+--------+------------------+--------+

: **Comparing pointQA capabilities on the LookTwice-QA** [@mani2020pointqa], where the models are asked to answer question based on the input point/box. Pronoun, Superclass (Super cls.), and Class indicate different levels of referential clarity in the question, , "How many of these \[$\varnothing$/fruits/apples\] \<obj\>?\" We use Shikra-13B and Accuracy (%) for evaluation.
:::

[]{#tab:twiceqa label="tab:twiceqa"}

::: table*
+------------+--------+----------+--------------+-------------+--------+------------+----------+---+
| Datasets   | Shikra | Kosmos-1 | Flamingo-80B | Flamingo-9B | BLIP-2 | Unified-IO | VPGTrans |   |
+:===========+:======:+:========:+:============:+:===========:+:======:+:==========:+:========:+:=:+
| 1-1(lr)2-8 | 83.27  | 51.0     | 56.3         | 51.8        | 65.2   | 77.9       | 65.2     |   |
|            |        |          |              |             |        |            |          |   |
| VQAv2      |        |          |              |             |        |            |          |   |
+------------+--------+----------+--------------+-------------+--------+------------+----------+---+
| OK-VQA     | 53.77  |          | 50.6         | 44.7        | 45.9   | 54.0       | 45.9     |   |
+------------+--------+----------+--------------+-------------+--------+------------+----------+---+

[]{#tab:vqa label="tab:vqa"}
:::

::: table*
  Datasets                Shikra      Kosmos-1   Flamingo-9B   Flamingo-80B   GIT    Unified-IO   VisionLLM
  ---------------------- -------- -- ---------- ------------- -------------- ------ ------------ -----------
  1-1(lr)2-9 Flickr30k                  67.1                                  49.6               
  COCO Cap                              84.7        79.4           84.3                126.8        114.2

[]{#tab:captioning label="tab:captioning"}
:::

::: table*
[]{#tab:vl label="tab:vl"}
:::

::: table*
:::

For detect object in autoregressive model, several methods [@chen2021pix2seq; @wang2022ofa] introduce extra vocabularies (, \<bin_0\>, $\cdots$, \<bin_1000\>) to represent coordinates for object detection in spatially discretized images, as described in . In contrast, Shikra represents coordinates naturally and intuitively, using numbers directly. Which form is better? We train two toy Shikra using two different representations with REC data, they performance is recorded in , where using numbers directly achieves better results. Aside from performance, our simple-designed coordinate numerical representation makes the model more elegant without modifying vocabularies for localization tasks. Users can freely control the precision of numerical representation (number of digits after the decimal separator) without retraining vocabularies. However, it also has drawbacks. Compared to using extra vocabularies, numerical representation requires more tokens to represent coordinates, leading to increased computational costs when predicting dense objects. In this paper, we still prefer numerical representation, but future research can choose the appropriate method based on their pros and cons.

## Quantitative results on conventional tasks {#sec:experiment_vltask}

Our Shikra excels in Referential Dialogue, facilitating seamless integration into a wide range of vision-language (VL) tasks, particularly those related to positioning. Here, we present the quantitative results for these tasks.

To demonstrate the positioning capability of our model, we examine the REC task, in which models are ask to ground the object described with an expression. As shown in , we compare our method with generalist VL models that perform multiple tasks without finetuning. We also compare our method with Specialist SOTAs, including localization specialist models and generalist/foundation models that perform specific finetunes on localization-related tasks. In this setting, we instruct Shikra to provide the coordinates of the objects referred to by the expression. For an example, we use "*I'd like to know the exact coordinates of \<expr\> in the photo \<image\>.*", where \<expr\> represents the expression and \<image\> represents the input image. More instructions can be found in . The experimental results demonstrate that Shikra achieves promising performance compared to other generalist models.

Correspondingly, to quantitatively evaluate our model's understanding of position inputs, we evaluated our model on two types PointQA datasets, LookTwice-QA of [@mani2020pointqa] and Visual7W (PointQA Setting) of [@zhu2016v7w]. LookTwice-QA asks models to answer questions about the region specified by the user, either by center point or box, with the distinction that these questions necessitate comprehending the user-designated area first, and then observing the entire image to answer. For instance, "*How many of these* \[Pronoun/Superclass/Class\] *\<obj\>?*", where \<obj\> denotes the coordinates of input point or box and \[Pronoun/Superclass/Class\] represents language instructions with different clarity levels (, \[$\varnothing$/fruits/apples\]). Visual7W also provides a setting for point QA, where models are given a question and four box options, and should choose one as the answer.' Our Shikra achieves the SOTA performance in all these settings.

Additionally, we assess our model on conventional VL tasks in , such as VQA and Image Captioning, which do not necessitate coordinates in their input or output. The experimental results show that we achieved promising results on most datasets. We also evaluated the performance of our method in POPE evalution pipeline [@li2023obj_Hallucination], and the results are recorded in . Our method has achieved results comparable to InstrutBLIP[@dai2023instructblip] and far surpasses recent popular MLLMs. It's worth noting that these task configurations are just some subsets of Referential Dialogue. We hope readers can appreciate the more intriguing capabilities of Shikra in and .

# Limitations {#sec:limitations}

Shikra only supports English and is not user-friendly for non-English speakers. Making Shikra multilingual in the future is valuable. Shikra is unsuitable for dense object detection and segmentation tasks. Exploring improved coordinate representations for these tasks is also interesting. Shikra, like most LLMs, may produce harmful and counterfactual responses.

# Conclusion {#sec:conclusion}

Our study unveiled the critical gap in MLLMs' ability to understand and engage in referential dialogue, an integral aspect of human communication. To address this, we introduced Shikra, a unified, straightforward model designed to comprehend and output spatial coordinates in natural language. Our approach does not necessitate extra vocabularies, position encoders, or external plug-ins, preserving the model's simplicity. It was proved that Shikra performs notably well on a variety of conventional vision-language tasks, while offering swathes of exciting applications such as aiding AI assistants in Mixed Reality headsets or facilitating precise communication in online shopping scenery.

[]{#sec:appendix label="sec:appendix"}

# Details of All Training Data {#sec:train_data}

::: table*
  **Task**             **Dataset**
  -------------------- -----------------------------------------------------------
  1-2 Captioning       LLaVA-Pretraining
  1-2 Soptting Cap.    Flickr30K Entities
  1-2 Grounding Cap.   Visual Genome
  1-2 REG              RefCOCO, RefCOCO+, RefCOCOg
  1-2 REC              RefCOCO, RefCOCO+, RefCOCOg, Visual Genome
  1-2 VQA              VQAv2
  1-2 PointQA          PointQA-Local/Twice, Visual-7W ('which box' subset)
  1-2 Dialogue         LLaVA-Instruct-150K\*
  1-2 RD               VCR, Shikra-RD (Generated data from Flickr30K Entities)\*

[]{#tab:all_data label="tab:all_data"}
:::

We listed all training data in . The asterisk indicates that this data is only used in the second training stage. We removed the images from the training set that are the same as those in the testing or validation set to prevent potential data leakage.

# Examples of Task Prompts {#sec:task_temp}

::: table*
[]{#tab:task_temp label="tab:task_temp"}
:::

We list some task prompts used by Shikra during training in . For every task listed, there are hundreds. These prompts are generated by GPT-4 with carefully designed instructions. We randomly selected three prompts for readers' better understanding. Note that during inference, there is no need to confine oneself to these forms. Users can express their needs in natural language, creating diverse and engaging task formats.

# More Conversations with Shikra {#sec:more_cases}

We provide additional dialogue records of Shikra-7B in this section. For instance, we showcase RD results in , VQA (Q$\rightarrow$$\text{C}^\text{Box}$A) in , and Spotting Captioning in . We also include examples of traditional VL task forms, like OCR in , REC in , REG in , and PointQA in . Furthermore, and demonstrates that our input and output can handle points and boxes, just tell Shikra what to do.

![](../images/Shikra_md_images/figures/case/shikra_case_2.pdf.png){width="97%"}

*Referential Dialogue using Shikra-7B. The dashed box on an image represents the area referred to by the user or jointly referred to by Shikra, while the solid box represents the area solely referred to by Shikra.*

![](../images/Shikra_md_images/figures/case/shikra_case_3.pdf.png){width="70%"}

*Q→C^Box A using Shikra-7B. It asks models to generate a grounded explanation for the answer.*

![](../images/Shikra_md_images/figures/case/shikra_case_4.pdf.png){width="60%"}

*OCR using Shikra-7B. We do not have explicit OCR datasets in Shikra training.*

![](../images/Shikra_md_images/figures/case/shikra_case_5.pdf.png){width="96%"}

*Spotting Captioning using Shikra-7B. The task requires the model to describe the image and spot the mentioned objects or regions using points or boxes.*

![](../images/Shikra_md_images/figures/case/shikra_case_6.pdf.png){width="100%"}

*Referring Expression Generation (REG) using Shikra-7B. The purpose of REG is to generate a unique description for a specified location.*

![](../images/Shikra_md_images/figures/case/shikra_case_7.pdf.png){width="100%"}

*Referring Expression Comprehension (REC) using Shikra-7B. The task aims to localize a target object in an image described by a referring expression.*

![](../images/Shikra_md_images/figures/case/shikra_case_8.pdf.png){width="97%"}

*PointQA using Shikra-7B. The task asks models to answer questions about the region specified by the user, either by center point or box.*

![](../images/Shikra_md_images/figures/case/shikra_case_9.pdf.png){width="97%"}

*PointQA-V7W using Shikra-7B. PointQA-V7W provides a setting for point QA, where models are given a question and four box options, and should choose one as the answer.*

[^1]: Shikra is a hunter's companion, capable of understanding human language and gesture instructions, and locating and capturing prey in the wild.
