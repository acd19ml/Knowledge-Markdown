# Introduction {#sec:introduction}

In the field of artificial intelligence (AI) [@lecun2015deep; @minsky1961steps; @nilsson1982principles; @winston1984artificial], multimodal learning [@baltruvsaitis2018multimodal; @xu2023multimodal] that combines visual perception and natural language understanding has emerged as a pivotal approach for achieving human-like cognition in machines. At its core lies the integration of visual and linguistic cues, intending to bridge the semantic gap between image scenes and language descriptions. Visual Grounding (VG) [@refcocog-google; @refcocog-umd; @yu2016modeling] represents such a fundamental pursuit, encompassing AI models' ability to establish intrinsic connections between linguistic expressions and corresponding visual elements.

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig1_v3.pdf.png)
**Figure 1.** An illustration of visual grounding.

As depicted in Figure 1, visual grounding, also known as Referring Expression Comprehension (REC) and Phrase Grounding (PG), according to the classical definition [@deng2021transvg; @yu2018mattnet; @yang2020resc], involves *localizing a specific region within an image based on a given textual description*, and such a description is called a "*referring expression*" [@van2006building; @viethen2008use; @golland2010game; @mitchell2010natural; @mitchell2013generating; @fitzgerald2013learning; @kazemzadeh2014referitgame; @refcocog-google]. The objective of this task is to emulate the prevalent referential relationships in social conversations, equipping machines with human-like multimodal comprehension capabilities. Consequently, it has extensive applications in visual language navigation [@anderson2018navigation], human-machine dialogue [@das2017visual_dialog; @chen2023shikra], visual question answering [@fukui2016mcb; @antol2015vqa], and other related domains [@qiao2020referring].

![](../images/Towards%20Visual%20Grounding_md_images/fig/citation_and_perf_trends_revised.pdf.png)
**Figure 2.** The number of papers and performance trends of visual grounding over the past decade. The data in panel (a) are derived from an exact-match lookup on Google Scholar for the term "referring expression comprehension". The GMLLMs in panel (b) are the 7B version.

Figure 2 highlights both the growth in publication volume and the sharp performance gains that accompanied the recent pre-training and GMLLM era.

The continuous advancements in deep learning, including visual grounding, are driven by three fundamental elements: *data, algorithms, and computing power* [@duan2019artificial]. From a *data* perspective, the grounding task involves three essential types of data: `images`, `referring expressions`, and `referred bounding boxes`. However, obtaining such paired triplet data is not straightforward, despite images being more readily available among these three types.

Challenges arise when acquiring expression text and corresponding bounding boxes. First, visual grounding heavily relies on high-quality and *unambiguous* textual referring expression data. This criterion reflects the requirement that when describing an object in a complex real scene, it should be *informative, concise,* and *unambiguous* [@refcocog-google; @yu2016modeling]. Second, obtaining paired bounding boxes is also labor-intensive. These factors explain why early work focused either on Referring Expression Generation (REG) or weakly supervised settings before large-scale paired datasets became available.

From the perspective of *algorithms* and *computing power*, visual grounding has evolved together with mainstream deep learning methods and increasing computational capability. As shown in Figure 5, the development can be roughly categorized into three stages: the *preliminary stage* (before 2014), the *early stage* (2014-2020), and the *surge stage* (2021-present). Starting from 2021, LSTM- and CNN-based methods gradually gave way to Transformer-based and pre-training-based paradigms. From 2023 onward, Grounding Multimodal Large Language Models (GMLLMs) [@you2023ferret] rapidly emerged.

Although visual grounding has witnessed significant advancements over the past decade, it has also accumulated several challenges. These include ambiguous setting definitions, limited benchmarks that no longer match emerging LLM-era requirements, and the lack of a recent systematic review that unifies the field after the surge of multimodal pre-training and grounding-oriented LLMs.

**Survey pipeline.** As illustrated in Figure 4, this survey first reviews the historical development of visual grounding, then covers essential background information, definitions, evaluation criteria, and related research domains, before systematically reviewing methods under seven settings and finally discussing challenges and future directions.

**Contributions.**
- This survey systematically tracks and summarizes the development of visual grounding over the last decade, especially the work from the last five years.
- It organizes the various experimental settings in visual grounding and provides clearer definitions to support fairer comparison.
- It compiles recent datasets and benchmark trends to help motivate future benchmark design.
- It summarizes current research challenges and highlights promising future directions.
- It aims to serve as a comprehensive entry point for both beginners and established researchers in visual grounding.

# Background {#sec:background}

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig_definition.pdf.png)
**Figure 3.** A future-oriented definition of generalized grounding.

**Overview.** In this section, we provide a comprehensive definition of visual grounding, discuss the corresponding evaluation metrics, and introduce several closely related research domains.

**Figure 4.** Overview of the paper structure, detailing Chapter 1 to Chapter 4 and Appendix Chapter A2 to A4.

- Section 1: Introduction and development history
- Section 2: Background, including concept definition, evaluation metrics, box representation, and related domains
- Section 3: Methods review across fully supervised, weakly supervised, semi-supervised, unsupervised, zero-shot, multi-task, and generalized grounding settings
- Appendix A2: Datasets and benchmarks
- Appendix A3: Applications
- Appendix A4: Advanced topics
- Section 4: Challenges and outlook
- Section 5: Conclusion

## Concept Definition {#subsec:definition}

We provide three grounding-related concept definitions.

- **Classical Visual Grounding.** Based on the literature from the past decade, this is the widely accepted narrow definition. Specifically, *Visual Grounding (VG) or Referring Expression Comprehension (REC) involves localizing a specific region within an image based on a given textual description*. When the descriptive text consists of only a few short words, it is often referred to as Phrase Grounding (PG). Current literature commonly associates PG with ReferIt Game and Flickr30k Entities, while REC is used more often for RefCOCO/+/g.
- **Generalized Visual Grounding.** Traditional VG assumes that a sentence refers to exactly one object, which is not applicable to many real-world scenarios. Following recent work [@he2023grec; @liu2023gres; @xie2024described; @hu2023beyond], this survey uses *Generalized Visual Grounding (GVG)* or *Generalized Referring Expression Comprehension (GREC)* to denote grounding tasks that may involve one, multiple, or no target objects, as illustrated in Figure 3. This concept is also referred to as *Described Object Detection (DOD)* in some work.

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig_timeline.pdf.png)
**Figure 5.** A chronological overview of representative research progress in fully supervised visual grounding from the perspective of the technical roadmap.

- **Phrase Localization.** Phrase Localization (PL), also known in some contexts as Phrase Grounding, is defined as identifying and localizing all entities mentioned in a textual phrase within an image [@plummer2015flickr30k; @wang2016structured; @plummer2017phrase]. Unlike REC, PL typically requires NLP parsing to extract noun chunks and then pair them with detected proposals. Because later grounding research moved toward end-to-end subject grounding, this survey does not treat PL as a separate major track.

## Evaluation Metrics {#subsec:evaluation_metric}

We denote the learned grounding model as $\mathcal{M}_{g}$. For any given image $\mathcal{I}\in\mathbb{R}^{3\times H\times W}$ and text $\mathcal{T}\in\mathbb{R}^{L_t}$ pairs, a set of predicted bounding boxes $\hat{\bm{B}}=\{\hat{\mathscr{B}}_i\}_{i=0}^k$ can be obtained through the grounding model:

$$
\hat{\bm{B}}= \mathcal{M}_g(\mathcal{I}, \mathcal{T}),
$$

where $H$ and $W$ denote the height and width of the image, $L_t$ represents the length of the text tokens, $\hat{\mathscr{B}}_i = (\hat{x}_i,\hat{y}_i,\hat{w}_i,\hat{h}_i)$ denotes each predicted box, and $k = {0, 1, 2, ...}$ is the number of target objects. Specifically, when $k = 1$, it belongs to the classical grounding setting; when $k = 0$, $\hat{\bm{B}}$ is an empty set.

- **Classical Visual Grounding.** At the individual-sample level, the standard metric is *Intersection over Union* (IoU, also called Jaccard overlap) [@giou] between the predicted grounding box $\hat{\mathcal{B}}$ and the ground-truth box $\mathcal{B}=(x,y,w,h)$.
- **Generalized Visual Grounding.** Under GVG, evaluation becomes more challenging. Recent work [@he2023grec] recommends using `Precision@(F1=1, IoU>=0.5)` for multi-object grounding and `N-acc` for no-target grounding. These metrics reflect whether the set of predicted boxes exactly matches the target situation rather than only measuring overlap for a single box.

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig_box.pdf.png)
**Figure 6.** The representations of the bounding box in grounding.

## Representation of the Grounding Box {#subsec:representation_of_box}

The representation of grounding boxes in dataset storage, data preprocessing, and model result output exhibits significant variations. As depicted in Figure 6, multiple representations are commonly employed, including $(x_{1},y_{1},w,h)$, $(x_{c},y_{c},w,h)$, and $(x_1,y_1,x_2,y_2)$ formats. The prevailing approach for representing the output box is often through the normalized $(x_1,y_1,x_2,y_2)$ format, *i.e.* $\mathcal{B}_{norm}=(x_1/W,y_1/H,x_2/W,y_2/H)$.

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig_setting_v2.pdf.png)
**Figure 7.** Mainstream settings in visual grounding. Specific definitions of each setting are provided in Section 3.

Figure 7 summarizes the mainstream settings in visual grounding. In addition, the output of grounding coordinates is a highly regarded technique, encompassing various position paradigms. Early anchor-based methods use predefined sliding windows and candidate regions for classification, selecting the proposal with the highest similarity to output the grounding coordinates. Conversely, current end-to-end approaches directly regress the bounding box coordinates using four numerical values. More recent pre-trained and MLLM-based methods also explore coordinate tokenization schemes to unify grounding with sequence generation.
# Methods: A Survey {#sec:method_survey}

**Overview.** To better facilitate the understanding of the current research status of grounding, this section classifies and reviews existing methods according to their experimental settings, with particular emphasis on those developed within the past five years. Figure 7 gives a concise definition of the commonly used settings.

The main settings discussed in this survey are:
- **Fully Supervised Setting.** Train or fine-tune the grounding model using image-text-box triplets.
- **Weakly Supervised Setting.** Train using only image-text pairs without explicit grounding boxes.
- **Semi-supervised Setting.** Combine complete labeled triplets with incomplete or unlabeled image data.
- **Unsupervised Setting.** Learn grounding from unlabeled images with the assistance of other models or priors.
- **Zero-shot Setting.** Evaluate grounding ability on novel classes or without specific grounding fine-tuning.
- **Multi-task Setting.** Learn grounding jointly with related tasks such as REG or RES.
- **Generalized Visual Grounding.** Extend grounding to one-target, multi-target, and no-target cases.

## Fully Supervised Setting {#subsec:fully_sup}

Fully Supervised Visual Grounding (FSVG) is currently the most extensively studied setting. The literature in this setting can be understood through three perspectives: the technical roadmap, the classification of framework architectures, and the benchmark results under several subdivision settings.

### The Technical Roadmap {#subsubsec:road_map}

As depicted in Figure 5, the advancement of visual grounding is closely connected to the evolution of deep learning algorithms and exhibits several paradigm shifts. The representative routes can be grouped into traditional CNN-based methods, Transformer-based methods, VLP-based transfer methods, grounding-oriented pre-training methods, and GMLLM-based methods.

![](../images/Towards%20Visual%20Grounding_md_images/fig/two_or_one_stage.pdf.png)
**Figure 8.** A comparison of two-stage and one-stage pipeline.

**A. Traditional CNN-based Methods (From 2014).** Early visual grounding methods usually encoded images with CNNs and sentences with GRU/LSTM-based language models. Two major transitions took place in this period.

- **From two-stage to one-stage.** As shown in Figure 8, early methods first generated region proposals and then performed region-text matching. This two-stage design benefited from the detection pipeline of the time but suffered from high computational cost, proposal quality bottlenecks, and difficulty in injecting language guidance into region extraction. Later one-stage methods removed explicit proposal extraction and incorporated language information directly into dense prediction or regression pipelines.
- **From GRU/LSTM to attention mechanisms.** In the language branch and the cross-modal fusion branch, the dominant paradigm shifted from CNN-GRU/LSTM combinations to attention-based modules. Attention improved token-level image-text interaction and enabled richer cross-modal reasoning than single-vector sentence representations.

**B. Traditional Transformer-based Methods (From 2021).** With the introduction of Transformer backbones in NLP and computer vision, grounding models started to use Transformer modules for visual encoding and cross-modal fusion. Representative work in this stage includes TransVG, which reformulated grounding as a regression problem with a learned region token, and a series of language-guided visual grounding methods that explicitly modulated visual encoding with linguistic cues.

**C. VLP-based Transfer Methods (From 2021).** CLIP and other VLP models provided naturally aligned cross-modal representations, which significantly changed grounding transfer. Methods such as CLIP-VG and HiVG leveraged these pre-trained models and then adapted them with fusion modules, multi-level feature bridges, or PEFT strategies such as LoRA, prompts, and adapters.

**D. Grounding-oriented Pre-training Methods (From 2020).** Another major route is to bring grounding directly into pre-training. MDETR reformulated detection as modulated detection, while GLIP and related models used grounded language-image pre-training to build region-level fine-grained cross-modal representations. Multi-task pre-training methods such as OFA, UniTAB, and related approaches further broadened this direction.

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig_full_sup_model_arch.pdf.png)
**Figure 9.** Classification of typical framework architectures for visual grounding when using pre-trained models.

**E. Grounding Multimodal LLMs (From 2023).** Figure 9 also highlights the rise of GMLLM-style architectures. These methods map visual information into the feature space of large language models and formulate grounding as an auto-regressive multimodal reasoning problem. Representative methods include Shikra, Ferret, Grounding-GPT, and LION. Their rise is closely tied to the broader success of LLMs, visual instruction tuning, and multimodal alignment.

### The Classification of Framework Architectures {#subsubsec:model_arch}

Since 2020, the widely adopted paradigm of "pre-training and fine-tuning" has driven rapid development in visual grounding. Broadly speaking, current grounding architectures can be divided into five types, as illustrated in Figure 9:

- **2+1 structure.** Separate visual and language encoding followed by a fusion encoder.
- **2+2 structure.** DETR-like architectures with query anchors and richer decoder structures.
- **Two-encoder structure.** Remove bulky fusion modules for higher efficiency.
- **One-tower structure.** Use modality-shared feature spaces to reduce integration overhead.
- **GMLLM structure.** Map visual tokens into an LLM space and perform grounding through language-style generation.

### Benchmark Results {#subsubsec:benchmark_result}

Under the fully supervised setting, recent work is commonly compared under four subdivision settings: single-dataset fine-tuning with unimodal pre-trained close-set detectors, single-dataset fine-tuning with self-supervised VLP models, dataset-mixed intermediate pre-training, and fine-tuning based on GMLLMs. A key observation is that RefCOCO/+/g remains dominant as the benchmark family, but its headroom is shrinking, which motivates stronger datasets and more careful evaluation protocols.

## Weakly supervised setting {#subsec:weakly_sup}

Weakly Supervised Visual Grounding (WSVG) aims to learn region-query correspondences solely from image-text pairs without box annotations. Existing methods can be divided into two groups.

### Proposal-based Methods

Most proposal-based WSVG methods frame grounding as a region-text ranking problem on top of proposals from an external detector. Representative techniques include:
- sentence reconstruction strategies, which use reconstruction losses to strengthen proposal-text matching;
- contrastive learning methods, which optimize positive and negative region-text correspondences;
- relation-aware refinement methods, which leverage scene structure and context cues;
- pseudo-labeling methods, which synthesize intermediate supervision; and
- one-stage variants that try to remove proposal bottlenecks.

### VLP-based WSVG Transfer

A later line of work uses VLP models such as CLIP, ALBEF, and X-VLM to enhance cross-modal alignment in weakly supervised settings. These methods either improve proposal ranking directly with VLP features or exploit cross-modal attention maps and Grad-CAM-style localization to derive pseudo grounding evidence.

## Semi-supervised setting {#subsec:semi-sup_setting}

Semi-Supervised Visual Grounding (SSVG) enhances model performance by combining limited labeled data with unlabeled data. Typical ideas include pseudo-label generation, self-training, curriculum learning, and teacher-student distillation. Compared with weakly supervised grounding, this setting remains relatively underexplored.

## Unsupervised Setting {#subsec:unsup_setting}

Unsupervised Visual Grounding (USVG) further reduces dependence on labeled data. Early approaches explored unpaired image-query or image-box matching, but these introduced substantial ambiguity. More recent methods such as Pseudo-Q and CLIP-VG instead generate pseudo-language labels or pseudo grounding supervision and then refine the model through self-training.

## Zero-shot Setting {#subsec:zero-shot}

To improve domain generalization beyond the limits of training categories or grounding supervision, the zero-shot setting has become increasingly important. Existing work can be roughly grouped into four categories.

### Grounding Novel Objects and Unseen Noun Phrases {#subsubsec:traditional_zsg}

This line studies grounding on novel categories or unseen noun phrases. ZSGNet introduced a practical split-based formulation, and later work such as MMKG and TransCP explored knowledge-enhanced or prototype-based reasoning for novel-object grounding.

### Open Vocabulary Visual Grounding {#subsubsec:ovvg}

Open Vocabulary Grounding (OVG) is a special case of zero-shot learning where the model can rely on broad vocabularies acquired during pre-training. CLIP-based methods and GMLLMs are especially natural fits for this setting.

Figure 10 contrasts the classical zero-shot grounding formulation with the broader open-vocabulary grounding setting.

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig_ovg.pdf.png)
**Figure 10.** Concepts comparison of zero-shot grounding and open-vocabulary grounding with the fully supervised setting in visual grounding.

### Finetuning-free for Pre-trained Model with Proposals

These methods use pre-trained models with strong generalization and cross-modal alignment, but without grounding-specific fine-tuning. They typically rely on detected proposals and then perform detection-then-matching, as in ReCLIP, GroundVLP, and related methods.

### Direct Grounding without Fine-tuning and Proposals

These methods rely on pre-training with fine-grained detection or grounding data so that they already exhibit grounding capability at inference time. Representative examples include Grounding DINO and KOSMOS-2.

## Multi-task Setting {#subsec:multi-task_setting}

Grounding can also be learned jointly with other tasks.

### REC and REG Multi-task Setting {#subsec:rec_and_reg}

REC and REG are naturally cycle-consistent. Joint models exploit this relationship to improve both grounding and referring expression generation.

### REC and RES Multi-task Setting {#subsec:rec_and_res}

REC and RES are often treated as complementary tasks, with shared backbones and separate heads or collaborative training objectives.

### Grounding with Other Tasks

Grounding also supports broader multimodal tasks such as grounded VQA, retrieval, and large-scale multi-task pre-training.

## Generalized Visual Grounding {#subsec:grec}

Generalized Visual Grounding (GVG or GREC) extends traditional grounding beyond the single-target assumption to cover one-target, multi-target, and no-target cases. Compared with traditional grounding, GVG is more realistic and application-oriented, but it introduces additional challenges in task formulation, dataset construction, and evaluation.

# Challenges and Outlook {#sec:future_direction}

## Challenges {#subsec:challenge}

Current grounding research still faces several major limitations:
- **Dataset limitations.** Existing datasets are becoming saturated, remain relatively small, and often fail to support complex reasoning or GMLLM evaluation.
- **Task definition limitations.** The strong assumption that exactly one object must be referred to does not match real-world scenarios.
- **Video scenarios.** Static-image grounding is much more mature than grounding in video streams.
- **Grounding scaling.** Large-scale grounded pre-training is constrained by the scarcity of open, high-quality, region-level data.
- **Application limitations.** Many practical deployment scenarios remain only lightly explored.

## Future Directions {#subsec:future_direction}

Promising future directions include:
- new evaluation benchmarks with larger category diversity, larger scale, stronger reasoning demands, and better alignment with generalized grounding;
- universal multimodal grounding across text, speech, gestures, multi-device settings, and multi-turn interaction;
- generalized video object grounding for surveillance, transportation, and embodied intelligence;
- self-supervised grounding pre-training that reduces reliance on fine-grained region labels; and
- broader general-AI applications that treat grounding as a core capability rather than an isolated benchmark task.

# Conclusion {#sec:conclusion}

This survey systematically tracks and summarizes the development of visual grounding over the past decade. It reviews the historical evolution of the field, organizes the major settings and their definitions, summarizes methods and datasets, highlights applications and advanced topics, and identifies key challenges and future directions. The goal is to provide both beginners and experienced researchers with a comprehensive entry point into the visual grounding literature.

# Appendices {#appendices .unnumbered}

# Methods: Supplementary Material
Due to space limitations in the main text, the full table of representative fully supervised methods during the surge stage is deferred to the appendix.

# Datasets and Benchmarks {#sec:datasets_and_benchmarks}
**Overview.** Datasets have had a profound impact on the development of grounding. Beyond the methods review, this survey also organizes the major datasets for classical grounding, generalized grounding, GMLLM-oriented grounding, and broader universal grounding scenarios.

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig_refcoco_sample.pdf.png)
**Figure 11.** Examples of expression text in RefCOCO/+/g datasets.

Figure 11 shows representative expression styles from RefCOCO/+/g, which became the dominant benchmark family for a large part of the literature. The most influential classical datasets include RefCOCO/+/g, ReferIt Game, and Flickr30k. More recent datasets expand to generalized grounding, grounding-oriented multimodal LLM benchmarks, and broader scenarios such as multi-image or gigapixel-scale grounding.

# Applications {#sec:application}
**Overview.** Visual grounding is not only important as a standalone referring task; it also affects a wider family of multimodal problems.

Representative application directions include grounded object detection, video object grounding, referring expression counting, remote sensing visual grounding, medical visual grounding, 3D visual grounding, speech-based grounding, robotic and multimodal agent systems, and industrial applications.

# Advanced Topics {#sec:advanced_topics}
**Overview.** Several techniques recur across grounding settings and are worth discussing independently.

![](../images/Towards%20Visual%20Grounding_md_images/fig/fig_nlp_parser.pdf.png)
**Figure 12.** Illustration of language structure parsing. The results are obtained by Stanford CoreNLP ([https://corenlp.run/](https://corenlp.run/)).

## Language Structure Parsing in Visual Grounding {#subsec:nlp_parser}

As illustrated in Figure 12, language structure parsing helps expose subjects, predicates, objects, and attributes in grounding expressions, which can then guide proposal matching and relation reasoning.

## Spatial Relations and Graph Neural Networks {#subsec:graph_neural_network}

Graph-based methods model interactions among candidate regions and help resolve ambiguity by incorporating spatial relations and scene structure.

## Modular Grounding {#subsec:modular_grounding}

Modular grounding decomposes an expression into components such as subject, relation, and attribute, and then matches each component to visual evidence through dedicated modules.

[^1]: <https://github.com/linhuixiao/OneRef>.
<a id="fig:definition"></a>
<a id="fig:grounding"></a>
<a id="fig:model_arch"></a>
<a id="fig:nlp_parser"></a>
<a id="fig:one_or_two_stage"></a>
<a id="fig:paper_structure"></a>
<a id="fig:perf_trend"></a>
<a id="fig:refcoco/+/g"></a>
<a id="fig:setting"></a>
<a id="fig:timeline"></a>
<a id="fig:zsg_def"></a>
<a id="sec:background"></a>
<a id="sec:conclusion"></a>
<a id="sec:future_direction"></a>
<a id="sec:introduction"></a>
<a id="sec:method_survey"></a>
<a id="subsec:challenge"></a>
<a id="subsec:definition"></a>
<a id="subsec:evaluation_metric"></a>
<a id="subsec:fully_sup"></a>
<a id="subsec:future_direction"></a>
<a id="subsec:graph_neural_network"></a>
<a id="subsec:grec"></a>
<a id="subsec:modular_grounding"></a>
<a id="subsec:multi-task_setting"></a>
<a id="subsec:nlp_parser"></a>
<a id="subsec:realted_domain"></a>
<a id="subsec:rec_and_reg"></a>
<a id="subsec:rec_and_res"></a>
<a id="subsec:representation_of_box"></a>
<a id="subsec:semi-sup_setting"></a>
<a id="subsec:unsup_setting"></a>
<a id="subsec:weakly_sup"></a>
<a id="subsec:zero-shot"></a>
<a id="subsubsec:benchmark_result"></a>
<a id="subsubsec:model_arch"></a>
<a id="subsubsec:ovvg"></a>
<a id="subsubsec:road_map"></a>
<a id="subsubsec:traditional_zsg"></a>
<a id="tab:dataset_st"></a>
<a id="tab:full_sota_main"></a>
<a id="tab:model_arch"></a>
<a id="tab:other_ref_datasets"></a>
<a id="tab:rec_sota"></a>
<a id="tab:two_and_one_stage_result"></a>
<a id="tab:weakly_sup"></a>
<a id="tab:zero-shot"></a>

## Caption Normalization Notes

**Figure 1.**

**Figure 2.**

**Figure 3.**

**Figure 4.**

**Figure 5.**

**Figure 6.**

**Figure 7.**

**Figure 8.**

**Figure 9.**

**Figure 10.**

**Figure 11.**

**Figure 12.**

