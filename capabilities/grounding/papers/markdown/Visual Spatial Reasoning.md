# Introduction

Multimodal NLP research has developed rapidly in recent years, with substantial performance gains on tasks such as visual question answering (VQA) , vision-language reasoning or entailment , and referring expression comprehension . Existing benchmarks, such as NLVR2 and VQA , define generic paradigms for testing vision-language models (VLMs). However, as we further discuss in , these benchmarks are not ideal for probing VLMs as they typically conflate multiple sources of error and do not allow controlled analysis on specific linguistic or cognitive properties, making it difficult to categorise and fully understand the model failures. In particular, spatial reasoning has been found to be particularly challenging for current models, and much more challenging than capturing properties of individual entities , even for state-of-the-art models such as CLIP .

Another line of work generates synthetic datasets in a controlled manner to target specific relations and properties when testing VLMs, e.g., CLEVR and ShapeWorld . However, synthetic datasets may accidentally overlook challenges (such as orientations of objects which we will discuss in ), and using natural images allows us to explore a wider range of language use.

To address the lack of probing evaluation benchmarks in this field, we present VSR (Visual Spatial Reasoning), a controlled dataset that explicitly tests VLMs for spatial reasoning. We choose spatial reasoning as the focus because it is one of the most fundamental capabilities for both humans and VLMs. Such relations are crucial to how humans organise their mental space and make sense of the physical world, and therefore fundamental for a grounded semantic model .

The VSR dataset contains natural image-text pairs in English, with the data collection process explained in . Each example in the dataset consists of an image and a natural language description which states a spatial relation of two objects presented in the image (two examples are shown in and ). A VLM needs to classify the image-caption pair as either true or false, indicating whether the caption is correctly describing the spatial relation. The dataset covers 66 spatial relations and has \>10k data points, using 6,940 images from MS COCO .

Situating one object in relation to another requires a *frame of reference*: a system of coordinates against which the objects can be placed. Drawing on detailed studies of more than forty typologically diverse languages, concludes that the diversity can be reduced to three major types: intrinsic, relative, and absolute. An intrinsic frame is centred on an object, e.g., *behind the chair*, meaning at the side with the backrest. A relative frame is centred on a viewer, e.g., *behind the chair*, meaning further away from someone’s perspective. An absolute frame uses fixed coordinates, e.g., *north of the chair*, using cardinal directions. In English, absolute frames are rarely used when describing relations on a small scale, and they do not appear in our dataset. However, intrinsic and relative frames are widely used, and present an important source of variation. We discuss the impact on data collection in , and analyse the collected data in .

We test four popular VLMs, i.e., VisualBERT , LXMERT , ViLT , and CLIP on VSR, with results given in . While the human ceiling is above 95%, all four models struggle to reach 70% accuracy. We conduct comprehensive analysis on the failures of the investigated VLMs and highlight that (1) positional encodings are extremely important for the VSR task; (2) models’ by-relation performance barely correlates with the number of training examples; (3) in fact, several spatial relations that concern orientation of objects are especially challenging for current VLMs; (4) VLMs have extremely poor generalisation on unseen concepts.


![](../images/Visual_Spatial_Reasoning_md_images/images/000000259555.jpg)
![](../images/Visual_Spatial_Reasoning_md_images/images/000000080336_cropped.jpg)
<figcaption>Caption: <em>The cow is ahead of the person.</em> Label: <code>False</code>.</figcaption>


# Related Work

## Comparison with synthetic datasets

Synthetic language-vision reasoning datasets, e.g., SHAPES , CLEVR , NLVR , and ShapeWorld , enable full control of dataset generation and could potentially benefit probing of spatial reasoning capability of VLMs. They share a similar goal to us, to diagnose and pinpoint weaknesses in VLMs. However, synthetic datasets necessarily simplify the problem as they have inherently bounded expressivity. In CLEVR, objects can only be spatially related via four relationships: “left”, “right”, “behind”, and “in front of” while VSR covers 66 relations.

Synthetic data does not always accurately reflect the challenges of reasoning in the real world. For example, objects like spheres, which often appear in synthetic datasets, do not have orientations. In real images, orientations matter and human language use depends on that. Furthermore, synthetic images do not take the scene as a context into account. The interpretation of object relations can depend on such scenes (e.g., the degree of *closeness* can vary in open space and indoor scenes).

Last but not least, the vast majority of spatial relationships cannot be determined by rules. Even for the seemingly simple relationships like “left/right of”, the determination of two objects’ spatial relationships can depend on the observer’s viewpoint, whether the object has a *front*, if so, what are their orientations, etc.

## Spatial relations in existing vision-language datasets

Several existing vision-language datasets with natural images also contain spatial relations (e.g., NLVR2, COCO, and VQA datasets). summarise that there are 9 prevalent linguistic phenomena/challenges in NLVR2 such as coreference, existential quantifiers, hard cardinality, spatial relations, etc., and 4 in VQA datasets . However, the different challenges are entangled in these datasets. Sentences contain complex lexical and syntactic information and can thus conflate different sources of error, making it hard to identify the exact challenge and preventing categorised analysis. extract 6 types of visual spatial relations directly from MS COCO images with annotated bounding boxes. But rule-based automatic extraction can be restrictive as most relations are complex and cannot be identified relying on bounding boxes. Recently, extract captions that contain 28 positional keywords from MS COCO and swap the keywords with their antonyms to construct a challenging probing dataset. However, the COCO captions also have the error-conflation problem. Also, the number of examples and types of relations are restricted by COCO captions.

Visual Genome also contains annotations of objects’ relations including spatial relations. However, it is only a collection of true statements and contains no negative ones, so cannot be framed as a binary classification task. It is non-trivial to automatically construct negative examples since multiple relations can be plausible for a pair of object in a given image. Relation classifiers are harder to learn than object classifiers on this dataset .

propose a benchmark called VALSE for testing VLMs’ capabilities on various linguistic phenomena. VALSE has a subset focusing on “relations” between objects. It uses texts modified from COCO’s original captions. However, it is a zero-shot benchmark without training set, containing just 535 data points. So, it is not ideal for large-scale probing on a wide spectrum of spatial relations.

## Spatial reasoning without grounding

There has also been interest in probing models’ spatial reasoning capability without visual input. For example, probe pretrained text-only models or VLMs’ spatial reasoning capabilities with text-only questions. However, a text-only dataset cannot evaluate how a model relates language to grounded spatial information. In contrast, VSR focuses on the joint understanding of vision and language input.

## Spatial reasoning as a sub-component

Last but not least, some vision-language tasks and models require spatial reasoning as a sub-component. For example, propose TVQA+, a spatio-temporal video QA dataset containing bounding boxes for objects referred in the questions. Models then need to simultaneously conduct QA while detecting the correct object of interest. propose a method for simultaneous image segmentation and prepositional phrase attachment resolution. Models have to reason about objects’ spatial relations in the visual scene to determine the assignment of prepositional phrases. However, if spatial reasoning is only a sub-component of a task, error analysis becomes more difficult. In contrast, VSR provides a focused evaluation of spatial relations, which are particularly challenging for current models.

# Dataset Creation

In this section we detail how VSR is constructed. The data collection process can generally be split into two phases (1) contrastive caption generation () and (2) second-round validation (). We then discuss annotator hiring & payment (), dataset splits (), and the human ceiling & agreement of VSR ().


![](../images/Visual_Spatial_Reasoning_md_images/images/vsr_annotation_example.pdf.png)
<figcaption>An annotation example of concepts “cat” &amp; “laptop” in contrastive caption generation. The example generates two data points for our dataset: one “True” instance when the completed caption is paired with image 2 (right) and one “False” instance when paired with image 1 (left).</figcaption>


## Contrastive Template-based Caption Generation ()

In order to highlight spatial relations and avoid annotators frequently choosing trivial relations (such as “near to”), we use a contrastive caption generation approach. Specifically, first, a pair of images, each containing two concepts of interests, would be randomly sampled from MS COCO (we use the train and validation sets of COCO 2017). Second, an annotator would be given a template containing the two concepts and is required to choose a spatial relation from a pre-defined list () that makes the caption correct for one image but incorrect for the other image. We will detail these steps and explain the rationales in the following.

#### Image pair sampling.

MS COCO 2017 contains 123,287 images and has labelled the segmentation and classes of 886,284 instances (individual objects). Leveraging the segmentation, we first randomly select two concepts (e.g., “cat” and “laptop” in ), then retrieve all images containing the two concepts in COCO 2017 (train and validation sets). Then images that contain multiple instances of any of the concept are filtered out to avoid referencing ambiguity. For the single-instance images, we also filter out any of the images with instance pixel area size $`<30,000`$, to prevent extremely small instances. After these filtering steps, we randomly sample a pair in the remaining images. We repeat such a process to obtain a large number of individual image pairs for caption generation.

#### Fill in the blank: template-based caption generation.

Given a pair of images, the annotator needs to come up with a valid caption that makes it a correct description for one image but incorrect for the other. In this way, the annotator should focus on the key difference between the two images (which should be a spatial relation between the two objects of interest) and choose a caption that differentiates the two. Similar paradigms are also used in the annotation of previous vision-language reasoning datasets such as NLVR(2) and MaRVL . To regularise annotators from writing modifiers and differentiating the image pair with things beyond accurate spatial relations, we opt for a template-based classification task instead of free-form caption writing.[^2] Besides, the template-generated dataset can be easily categorised based on relations and their categories. Specifically, the annotator would be given instance pairs as shown in .

The caption template has the format of “*The `ENT1` (is) ____ the `ENT2`.*”, and the annotators are instructed to select a relation from a fixed set to fill in the slot. The copula “is” can be omitted for grammaticality. For example, for “contains” and “has as a part”, “is” should be discarded in the template when extracting the final caption.

The fixed set of spatial relations enable us to obtain the full control of the generation process. The full list of used relations are listed in . It contains 71 spatial relations and is adapted from the summarised relation table of . We made minor changes to filter out clearly unusable relations, made relation names grammatical under our template, and reduced repeated relations. In our final dataset, 66 out of the 71 available relations are actually included (the other 6 are either not selected by annotators or are selected but the captions did not pass the validation phase).

## Second-round Human Validation

In the second-round validation, every annotated data point is reviewed by at least 3 additional human annotators (validators). Given a data point (consisting of an image and a caption), the validator gives either a `True` or `False` label as shown in (the original label is hidden). In our final dataset, we exclude instances with fewer than 2 validators agreeing with the original label.

#### Design choice on reference frames.

During validation, a validator needs to decide whether a statement is true or false for an image. However, as discussed in , interpreting a spatial relation requires choosing a *frame of reference*. For some images, a statement can be both true and false, depending on the choice. As a concrete example, in , while the potted plant is on the left side from the viewer’s perspective (relative frame), the potted plant is at the right side if the bench is used to define the coordinate system (intrinsic frame).

In order to ensure that annotations are consistent across the dataset, we communicated to the annotators that, for relations such as “left”/“right” and “in front of”/“behind”, they should consider both possible reference frames, and assign the label `True` when a caption is true from either the intrinsic or the relative frame. Only when a caption is incorrect under both reference frames (e.g., if the caption is “*The potted plant is under the bench.*” for ) should a `False` label be assigned.

On a practical level, this adds difficulty to the task, since a model cannot naively rely on pixel locations of the objects in the images, but also needs to correctly identify orientations of objects. However, the task is well-defined: a model that can correctly simulate both reference frames would be able to perfectly solve this task.

From a theoretical perspective, by involving more diverse reference frames, we are also demonstrating the complexity of human cognitive processes when understanding a scene, since different people approach a scene with different frames. Attempting to enforce a specific reference frame would be methodologically difficult and result in an unnaturally restricted dataset.


![](../images/Visual_Spatial_Reasoning_md_images/images/vsr_annotation_example_v2.pdf.png)
<figcaption>A second-round validation example.</figcaption>



![](../images/Visual_Spatial_Reasoning_md_images/images/relation_distribution_v5_grey.png)
<figcaption>Relation distribution of the final dataset (sorted by frequency). Top 40 most frequent relations are included. It is clear that the relations follow a long-tailed distribution.</figcaption>



![](../images/Visual_Spatial_Reasoning_md_images/images/concept_distribution_v6.png)
<figcaption>Concept distribution. Only concepts with  &gt; 100 frequencies are included.</figcaption>


## Annotator Hiring and Organisation

Annotators were hired from <a href="prolific.co" class="uri">prolific.co</a>. We required them to (1) have at least a bachelor’s degree, (2) be fluent in English, and (3) have a $`>`$<!-- -->99% historical approval rate on the platform. All annotators were paid 12 GBP per hour.

For caption generation, we released the task with batches of 200 instances and the annotator was required to finish a batch in 80 minutes. An annotator could not take more than one batch per day. In this way we had a diverse set of annotators and could also prevent annotators from becoming fatigued. For second-round validation, we grouped 500 data points in one batch and an annotator was asked to label each batch in 90 minutes.

In total, 24 annotators participated in caption generation and 45 participated in validation. 4 people participated in both phases, which should have minimally impacted the validation quality. The annotators had diverse demographic backgrounds: they were born in 15 countries, were living in 13 countries, and had 12 nationalities. 50 annotators were born and living in the same country while others had moved to different ones. The vast majority of our annotators were residing in the UK (32), South Africa (9), and Ireland (7). The ratio for holding a Bachelor/Master/PhD as the highest degree was: 12.5%/76.6%/10.9%. Only 7 annotators were non-native English speakers while the other 58 were native speakers. 56.7% of the annotators self-identified as female and 43.3% as male.

## Dataset Splits

We split the 10,972 validated data points into train/dev/test sets in two different ways. The stats of the two splits are shown in . In the following, we explain how they are created. ***Random split*:** We split the dataset randomly into train/dev/test with a ratio of 70/10/20. ***Concept zero-shot split*:** We create another concept zero-shot split where train/dev/test have no overlapping concepts. I.e., if “dog” appears in the train set, then it does not appear in dev or test sets. This is done by randomly grouping concepts into three sets with a ratio of 50/20/30 of all concepts. This reduces the dataset size, since data poins involving concepts from different parts of the train/dev/test split must be filtered out. The concept zero-shot split is a more challenging setup since the model has to learn concepts and the relations in a compositional way instead of remembering the co-occurrence statistics of the two.



| split       | train | dev   | test  | total  |
|:------------|:------|:------|:------|:-------|
| *random*    | 7,680 | 1,097 | 2,195 | 10,972 |
| *zero-shot* | 4,713 | 231   | 616   | 5,560  |

Statistics of the *random* & *zero-shot* splits.



## Human Ceiling and Agreement

We randomly sample 500 data points from the final random split test set of the dataset for computing human ceiling and inter-annotator agreement. We hide the labels of the 500 examples and two additional annotators are asked to label `True`/`False` for them. On average, the two annotators achieve an accuracy of 95.4% on the VSR task. We further compute the Fleiss’ kappa among the original annotation and the predictions of the two human. The Fleiss’ kappa score is 0.895, indicating near-perfect agreement according to .

# Dataset Analysis

In this section we compute some basic statistics of our collected data (), analyse where human annotators have agreed/disagreed (), and present a case study on reference frames ().


![](../images/Visual_Spatial_Reasoning_md_images/images/disagree_prob_distribution_v4_gray.png)
<figcaption>Per-relation probability of having two randomly chosen annotator disagreeing with each other (sorted from high to low). Only relations with  &gt; 20 data points are included in the figure.</figcaption>


## Basic Statistics of VSR

After the first phase of contrastive template-based caption generation (), we collected 12,809 raw data points. In the phase of the second round validation (), we collected 39,507 validation labels. Every data point received at least 3 validation labels. In 69.1% of the data points, all validators agree with the original label. 85.6% of the data points have at least $`\frac{2}{3}`$ annotators agreeing with the original label. We use $`\frac{2}{3}`$ as the threshold and exclude all instances with lower validation agreement. After excluding other instances, 10, 972 data points remained and are used as our final dataset.

Here we provide basic statistics of the two components in the VSR captions: the concepts and the relations. demonstrates the relation distribution. “touching” is most frequently used by annotators. The relations that reflect the most basic relative coordinates of objects are also very frequent, e.g., “behind”, “in front of”, “on”, “under”, “at the left/right side of”. shows the distribution of concepts in the dataset. Note that the set of concepts is bounded by MS COCO and the distribution also largely follows MS COCO. Animals such as “cat”, “dog”, “person” are the most frequent. Indoor objects such as “dining table” and “bed” are also very dominant. In , we separate the concepts that appear at `ENT1` and `ENT2` positions of the sentence and their distributions are generally similar.

## Where do annotators disagree?

While we propose using data points with high validation agreement for model evaluation and development, the unfiltered dataset is a valuable resource for understanding cognitive and linguistic phenomena. We sampled 100 examples where annotators disagree, and found that around 30 of them are caused by annotation errors but the rest are genuinely ambiguous and can be interpreted in different ways. This shows a level of intrinsic ambiguity of the task and variation among people.

Along with the validated VSR dataset, we also release the full unfiltered dataset, with annotators’ and validators’ metadata, as a second version to facilitate linguistic studies. For example, researchers could investigate questions such as where disagreement is more likely to happen and how people from different regions or cultural backgrounds might perceive spatial relations differently.

To illustrate this, the probability of two randomly chosen annotators disagreeing with each other is given for each relation in . Some of the relations with high disagreement can be interpreted in the intrinsic reference frame, which requires identifying the orientations of objects, e.g. “at the side of” and “in front of”. Other relations have a high level of vagueness, e.g., for the notion of *closeness*: “near” and “close to”. By contrast, part-whole relations, such as “has as a part”, “part of”, and in/out relations such as “within”, “into”, “outside” and “inside” have the least disagreement.

## Case Study: Reference Frames

It is known that the relative reference frame is often preferred in English, at least in standard varieties. For example, compares Standard Australian English and Aboriginal English, as spoken by school children at a school on Croker Island, investigating the use of the relations “in front of” and “behind” when describing simple line drawings of a person and a tree. Speakers of Standard Australian English were found to prefer the relative frame, while speakers of Aboriginal English were found to prefer the intrinsic frame.

Our methodology allows us to investigate reference frame usage across a wide variety of spatial relations, using a wide selection of natural images. To understand the frequency of annotators using relative vs. intrinsic frames, we label instances’ reference frames and study their distributions. The majority of examples that can be interpreted differently under different reference frames are left/right-related relations (i.e. “left/right of” and “at the left/right side of”). We find all left/right-related *true*[^3] statements and classify them into three categories: (1) intrinsic (2) relative and (3) both (the caption is correct under either intrinsic and relative frames of reference). Among the 616 instances, 68 (11%) and 518 (84%) use intrinsic and relative frames respectively, 30 (5%) can be interpreted with both frames. Since the vast majority of our annotators were native English speakers (91%), and all were university-educated, our finding is consistent with previous work suggesting that the relative frame is the most common frame in standard varieties of English.

Besides the overall trend, the use of reference frames can vary with the circumstances. Related patterns have been studied in cognitive science. For example, find a three-way interaction between linguistic cues, spatial configurations in an image, and a person’s own preferences on reference frames.

We investigated whether reference to a person in the image might influence how annotators comprehend the scene. 198 out of the 616 instances involve “person” in the caption. And out of the 198 human-involved instances, 32 (16%) use an intrinsic frame and 154 (78%) use a relative frame (12, i.e. 6%, can be interpreted with both frames), while the proportions were 9% and 87% for instances not involving “person”. This is a statistically significant difference (using two-tailed Fisher’s exact test, $`p{=}0.0054`$ if ignoring both-frame cases, and $`p{=}0.0045`$ if grouping both-frame and intrinsic cases). In other words, this suggests that the involvement of a human can more likely prompt the use of the intrinsic frame.

# Experiments

In this section, we test VLMs on VSR. We first introduce baselines and experimental configurations in , then experimental results and analysis in . Then we discuss the role of frame of reference using experiments in and finally conduct sample efficiency analysis in .

## Baselines and Experiment Configurations

#### Baselines.

For finetuning-based experiments, we test three popular VLMs: VisualBERT [^4], LXMERT [^5], ViLT [^6]. All three models are stacked Transformers that take image-text pairs as input. The difference mainly lies in how or whether they encode the position information of objects. We report only finetuned results but not direct inferences from off-the-shelf checkpoints since some of their pretraining objectives are inconsistent with the binary classification task of VSR, thus requiring additional engineering.

We additionally test the alt text pretrained dual-encoder CLIP as an off-the-shelf baseline model (no finetuning).[^7] We follow to construct negation or antonym of each individual relation. E.g., “facing” $`\rightarrow`$ “facing away from” and “ahead of” $`\rightarrow`$ “not ahead of”. For each sample, we compare the embedding similarity of the image-caption pair and that of the negated caption. If the original pair has a higher probability then the model prediction is `True`, otherwise `False`. We call this method CLIP (w/ prompting). We only report direct prompting results without finetuning since CLIP finetuning is expensive.

#### Experimental configurations.

We save checkpoints every 100 iterations and use the best-performing checkpoint on dev set for testing. All models are run three times using three random seeds. All models are trained with AdamW optimiser . The hyperparameters we used for training the three VLMs are listed in .



| model      |  lr  | batch size | epoch | token length |     |     |     |
|:-----------|:----:|:----------:|:-----:|:------------:|:---:|:---:|:---:|
| VisualBERT | 2e-6 |     32     |  100  |      32      |     |     |     |
| LXMERT     | 1e-5 |     32     |  100  |      32      |     |     |     |
| ViLT       | 1e-5 |     12     |  30   |     max      |     |     |     |

A listing of hyperparameters used for all VLMs (“lr”: learning rate).



## Experimental Results



![](../images/Visual_Spatial_Reasoning_md_images/images/performance_by_relation_random_split_v4.png)
<figcaption>random split</figcaption>


![](../images/Visual_Spatial_Reasoning_md_images/images/performance_by_relation_zeroshot_split_feb_20_v1.png)
<figcaption>zero-shot split</figcaption>

<figcaption>Performance (accuracy) by relation on the random (upper) and zero-shot (lower) split test sets. Relation order sorted by frequency (high to low from left to right). Only relations with more than 15 and 5 occurrences on the random and zero-shot tests respectively are shown. </figcaption>





<caption>Model performance on VSR test set. CLIP is applied without finetuning but with carefully engineered prompts while the other three smaller models are finetuned on the training set.</caption>
<thead>
<tr>
<th style="text-align: left;">model↓</th>
<th style="text-align: center;">random split</th>
<th style="text-align: center;">zero-shot split</th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">human ceiling</td>
<td colspan="2" style="text-align: center;">95.4</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">CLIP (w/ prompting)</td>
<td style="text-align: center;">56.0</td>
<td style="text-align: center;">54.5</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">VisualBERT</td>
<td style="text-align: center;">55.2<sub>±1.4</sub></td>
<td style="text-align: center;">51.0<sub>±1.9</sub></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">ViLT</td>
<td style="text-align: center;"><strong>69.3</strong><sub>±0.9</sub></td>
<td style="text-align: center;"><strong>63.0</strong><sub>±0.9</sub></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">LXMERT</td>
<td style="text-align: center;"><strong>70.1</strong><sub>±0.9</sub></td>
<td style="text-align: center;">61.2<sub>±0.4</sub></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>




In this section, we provide both quantitative and qualitative results of the four baselines. Through analysing the failure cases of the models, we also highlight the key abilities needed to solve this dataset.

As shown in , the best-performing models on the random split are LXMERT and ViLT, reaching around 70% accuracy while VisualBERT is just slightly better than the chance level. On the zero-shot split, all models’ performance decline substantially and the best model ViLT only obtains 63.0% accuracy. The off-of-the-shelf CLIP model obtains around 55% on both sets, indicating its weaknesses in spatial reasoning echoing ’s findings. Overall, these results lag behind the human ceiling by more than 25% and highlight that there is very substantial room for improving current VLMs.

#### Explicit positional information matters.

Both LXMERT and ViLT outperform VisualBERT by large margins ($`>`$<!-- -->10%) on both splits. This is expected since LXMERT and ViLT encode explicit positional information while VisualBERT does not. LXMERT has position features as part of the input which encodes the relative coordinates of objects within the image. ViLT slices an image into patches (instead of object regions) and uses positional encodings to signal the patches’ relative positions. VisualBERT, however, has no explicit position encoding. also highlight the importance of positional encodings of VLMs, which agrees with our observations.

#### Random split vs. zero-shot split.

It is worth noting that the performance gap between the random and zero-shot splits is large. As we will show in , the underlying cause is not likely to be the number of training examples, but rather that concept zero-shot learning is fundamentally a challenging task. The gap suggests that disentangling representations of concepts and relations is challenging for current models.

#### Sensitiveness to random seeds.

Model performance varies by about one to two percentage points. These fluctuations illustrate the importance of always reporting the average performance of multiple runs to make sure the conclusion is reliable.



![](../images/Visual_Spatial_Reasoning_md_images/images/000000134738.jpg)
<figcaption>Caption: <em>The hair drier is facing away from the person</em>. Label: <code>False</code>.</figcaption>


![](../images/Visual_Spatial_Reasoning_md_images/images/000000434410.jpg)
<figcaption>Caption: <em>The bench is in front of the person</em>. Label: <code>True</code>.</figcaption>

<figcaption>LXMERT failed on both examples.</figcaption>


#### Performance by relation.

We give performance by relation for all three finetuned models on both random and zero-shot splits in . The order from left to right is sorted by the frequency of relations in the dataset (within each split). Interestingly, there does not seem to be any correlation between performance and frequency of the relation, hinting that specific relations are hard not due to an insufficient number of training examples but because they are fundamentally challenging for current VLMs. Any relation that requires recognising orientations of objects seems to be hard, e.g., “facing”, “facing away from”, “parallel to” and “at the back of”. As an example, LXMERT failed on the two examples in which require understanding the front of a hair drier and a person respectively. In this regard, left-right relations such as “at the left/right side of” and “left/right of” are difficult because the intrinsic reference frame requires understanding the orientation of objects. As an example, in , all three models predicted `False`, but in the intrinsic frame (i.e., from the bench’s point of view), the potted plant is indeed at the right.



![](../images/Visual_Spatial_Reasoning_md_images/images/performance_by_meta_cat_random_split_v4.png)
<figcaption>random split</figcaption>


![](../images/Visual_Spatial_Reasoning_md_images/images/performance_by_meta_cat_zeroshot_split_feb_20_v1.png)
<figcaption>zero-shot split</figcaption>

<figcaption>Performance by categories of relations, on the random and zero-shot split test sets. For legend information, see .</figcaption>


To get a more high-level understanding of the relations’ performance, we group model performance by the categories of : “Adjacency”, “Directional”, “Orientation”, “Projective”, “Proximity”, “Topological” and “Unallocated” (also shown in ). The results are shown in . “Orientation” is the worst performing group on the random split, and on average all models’ performances are close to the chance level. When comparing random and zero-shot splits, performance has declined to some extent for almost all categories and models. The decrease in “Proximity” is particularly drastic across all models – it declined from close to 75% accuracy in random split to chance level in zero-shot split. “Proximity” contains relations such as “close to”, “near” and “far from”. We believe it is due to the fact that the notion of proximity is relative and very much dependent on the nature of the concept and its frequent physical context. E.g., for a “person” to be “near” an indoor concept such as “oven” is very different from a person being “near” a frequent outdoor object such as “train” or “truck”. Since the zero-shot split prevents models from seeing test concepts during training, the models have a poor grasp of what counts as “close to” or “far from” for these concepts, thus generalising poorly.

#### Other Errors.

While certain relations are intrinsically hard, we have observed other types of errors that are not bounded to specific relations. Here we give a few examples. Some instances require complex reasoning. In , the model needs to recognise that both the cow and the back of the car are in the car’s side mirror and also infer the relative position of the back of the car and the cow. It is perhaps no surprise that two of the three models predicted wrongly. Some other examples require common sense. E.g., in , we can infer the person and the cow’s moving direction and can then judge if the cow is ahead of the person. LXMERT failed on this example. In (right), the model needs to infer that the main body of the cat is hidden behind the laptop. Interestingly, all three models predicted this example correctly.


![](../images/Visual_Spatial_Reasoning_md_images/images/000000512796.jpg)
<figcaption>Caption: <em>The cow is at the back of the car</em>. Label: <code>True</code>. LXMERT and VisualBERT predicted <code>False</code>.</figcaption>



![](../images/Visual_Spatial_Reasoning_md_images/images/vsr_sample_efficiency_feb_20.pdf.png)
<figcaption>Sample efficiency analysis: model performance under different amounts of training data (100-shot, 25%, 50%, 75% and 100% of training set). Results on both the random and zero-shot split test sets are shown. As training data increases, the performance plateaus on both sets but the flattening trend is more obvious on the zero-shot split.</figcaption>


## Case Study on Reference Frames

As discussed in , different frames of reference can be used in natural language and it would be helpful to understand whether our models recognise them. We argue that the task of identifying frame of reference itself is very hard for current models. However, learning to recognise frames of reference helps the task of visual spatial reasoning.

Firstly, we conduct a case study on left/right-related relations. We additionally label the reference frames of all true statements containing any of the left/right-related relations. We exclude all data points that can be interpreted in both intrinsic and relative frames to slightly reduce the complexity of the task. Then we finetune a ViLT checkpoint to predict the reference frame based on the true statement and the image. The model’s performance on test set is shown in the upper half of . We can see that reference frame prediction is an extremely hard task for the model. This is presumably because it requires taking into account a 3D viewpoint and simulating transformations between different viewpoints.

Secondly, we use this model trained with reference frame labels to initialise the VSR task model and further finetune it on the VSR task (only the left/right relations). The test results are shown in the lower part of .[^8] We see a clear positive transfer from reference frame prediction task to the VSR task. This suggests that learning to recognise reference frames can indeed help downstream visual spatial reasoning. This makes sense since simulating the transformation of intrinsic/relative frames could be an intermediate reasoning step in detecting whether a statement is true/false.




<caption>ViLT model performance on the reference frame prediction task (upper half; we report macro-averaged Precision/Recall/F1 since the binary classification task is imbalanced); and VSR task using original pretrained checkpoint or the reference frame prediction task trained checkpoint (accuracy reported).</caption>
<thead>
<tr>
<th colspan="4" style="text-align: center;"><em>Reference frame prediction task</em></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">model↓</td>
<td style="text-align: center;">Precision</td>
<td style="text-align: center;">Recall</td>
<td style="text-align: center;">F1</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">ViLT</td>
<td style="text-align: center;">59.2<sub>±3.7</sub></td>
<td style="text-align: center;">59.7<sub>±5.8</sub></td>
<td style="text-align: center;">56.9<sub>±4.4</sub></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td colspan="4" style="text-align: center;"><em>VSR task (left/right subset)</em></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">model↓</td>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">Accuracy</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">ViLT</td>
<td colspan="2" style="text-align: center;">54.2<sub>±0.6</sub></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">ViLT + rf_trained</td>
<td colspan="2" style="text-align: center;"><strong>59.2</strong><sub>±1.8</sub></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>




## Sample Efficiency

In order to understand the correlation between model performance and the number of training examples, we conduct sample efficiency analysis on VSR. The results are plotted in . For the minimum resource scenario, we randomly sample 100 shots from the training sets of each split. Then we gradually increase the number of training examples to be 25%, 50% and 75% of the whole training sets. Both LXMERT and ViLT have a reasonably good few-shot capability and can be quite performant with 25% of training data. LXMERT, in particular, reaches above 55% accuracy with 100 shots on both splits. The zero-shot split is substantially harder and most models appear to have already plateaued at around 75% of the training set. For the random split, all models are increasing performance with more data points, though improvement slows down substantially for LXMERT and ViLT after 75% of training data. The fact that LXMERT has the best overall few-shot capability may be suggesting that LXMERT’s pretrained object detector has a strong inductive bias for the VSR dataset as it does not need to learn to recognise concept boundaries and classes from scratch. However, this advantage from LXMERT seems to fade away as the number of training examples increases.

# Conclusion and Future Directions

We have presented Visual Spatial Reasoning (VSR), a controlled probing dataset for testing vision-language models (VLMs)’ capabilities of recognising and reasoning about spatial relations in natural image-text pairs. We made a series of linguistic observations on the variability of spatial language when collecting VSR. We highlighted the diverse use of reference frames among annotators, and also the ambiguous nature of certain spatial relations. We tested four popular VLMs on VSR, and found they perform more than 25% below the human ceiling. On a more challenging concept zero-shot split, the tested VLMs struggled to reach 60% accuracy and their performance plateaued even with increased training examples. Among the finetuning-based VLMs, ViLT and LXMERT outperformed VisualBERT, and we pointed out that the explicit positional information in the former two models is crucial in the task. CLIP with prompt engineering achieved slightly better than random performance, suggesting poor capability in spatial reasoning. We also performed a by-relation analysis and found that the models’ performances on certain relations have little correlation with the number of training examples, and certain relations are inherently more challenging. We identified orientation as the most difficult category of relations for VLMs. Proximity is another challenging category, especially in the zero-shot setup as this relation is highly concept-dependent. We hope the task serves as a useful tool for testing and probing future VLMs.

In future work, we plan to more extensively investigate whether large-scale pretrained dual-encoders such as CLIP , ALIGN and LiT can properly recognise spatial relations, especially in the finetuning setup. A comparison of dual- and cross-encoders’ performance on each spatial relation might guide future model design. Recently, proposed ultra-large-scale VLMs. It would be interesting to see if VLMs have better spatial reasoning capability when scaled up. Another direction is extending VSR to cover more languages and cultures and test multilingual VLMs. Along the same line, since we have also collected the metadata of annotators, the VSR corpus can be used as a resource for investigating research questions such as: How is “space” described among different dialects of English? How is “space” perceived among different populations? We hope that the annotation process of VSR can also serve as a basis for future cross-lingual and cross-cultural sociolinguistic research.

# Acknowledgements

We thank the TACL reviewers and the action editor for their thoughtful comments. We thank Qian Wang and Rongtian Ye for helping trial the annotation scheme; Zihao Fu for helping set up the annotation server. The project is funded by Cambridge Language Sciences Incubator Fund. FL is supported by Grace & Thomas C.H. Chan Cambridge Scholarship.

# Appendix

#### Genuinely ambiguous annotation instances.

As mentioned in the main text, we analysed 100 examples with high disagreement among annotators and found that the majority of the case are truly ambiguous and cannot be assigned a definitive True/False label. Here we show two concrete examples. In , we can infer that the keyboard is horizontally lower than the cat. However, the keyboard is not right under the cat’s body (but a bit in front of the cat). The ambiguity results from the semantics of the word “below” which can mean both (1) horizontally lower (but not necessarily right under) and also (2) right under. In , if seat surface is viewed as the main body of the chair, we can infer that the sandwich is indeed above the chair. However, it is not above all parts of the chair (it is no higher than the backrest of the chair). This case depends on a person’s subjective understanding of what counts as “above the chair” and is thus also intrinsically ambiguous.


![](../images/Visual_Spatial_Reasoning_md_images/images/000000575911.jpg)
<figcaption>Caption: <em>The keyboard is below the cat</em>.</figcaption>



![](../images/Visual_Spatial_Reasoning_md_images/images/000000044682.jpg)
<figcaption>Caption: <em>The sandwich is above the chair</em>.</figcaption>


While we have excluded such cases in the standard VSR train/val/test split to ensure the dataset has human consensus, we also release the raw dataset without excluding these ambiguous cases for researchers who are interested in studying them further.

#### Relations included and excluded.

Our used set of relations is adapted from . In , we copy their original table for reference. We also list the exact modifications we made on top of the original table in . The major reasons for excluding relations are: (1) rarely used in describing spatial information of images (e.g., “north of”), (2) repeated with other relations (e.g., “front of” and “in front of”). In order to convert relations into templates, we also inserted some words to make them grammatical. We included several additional relations since we found them very frequent in MS COCO (e.g., “at the edge of” and “touching”).

#### Screenshots of the annotation interface.

We use the open-sourced label studio (<a href="labelstud.io" class="uri">labelstud.io</a>) for managing our annotation tasks. Two screenshots are shown in (caption generation) and (validation).


![](../images/Visual_Spatial_Reasoning_md_images/images/screenshot_annotation_interface2.png)
<figcaption>A screenshot of the annotation interface.</figcaption>



![](../images/Visual_Spatial_Reasoning_md_images/images/screenshot_validation_interface1.png)
<figcaption>A screenshot of the validation interface.</figcaption>


[^1]: Data and code: [github.com/cambridgeltl/visual-spatial-reasoning](https://github.com/cambridgeltl/visual-spatial-reasoning).

[^2]:  propose a zero-shot probing benchmark of similar spirit for *verb* understanding. All captions are simplified as subject-verb-object triplets.

[^3]: According to our guideline, false statements are interpreted as false under both frames.

[^4]: [huggingface.co/uclanlp/visualbert-nlvr2-coco-pre](https://huggingface.co/uclanlp/visualbert-nlvr2-coco-pre)

[^5]: [huggingface.co/unc-nlp/lxmert-base-uncased](https://huggingface.co/unc-nlp/lxmert-base-uncased)

[^6]: [huggingface.co/dandelin/vilt-b32-mlm](https://huggingface.co/dandelin/vilt-b32-mlm)

[^7]: [huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K](https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K)

[^8]: Note that the reference frame train/dev/test sets are derived from the VSR task split – so no data leakage is possible from train to dev and test sets even after the intermediate pretraining.
