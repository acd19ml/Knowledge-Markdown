![](../images/MM-Spatial_md_images/figures/Teaser.png)

# Introduction

[^1]

Understanding object locations and spatial relationships in both 2D and 3D space is crucial for interpreting complex visual scenes. While multimodal large language models (MLLMs) have achieved notable success for 2D visual tasks including referring and grounding and spatial relation prediction (e.g., *“left”* vs. *“right”*, *“above”* vs. *“below”*) , they still struggle with 3D object perception tasks such as estimating 1) relative depth (*“in front”* vs. *“behind”*), 2) object distances or sizes in metric units (*“A is 2.74m away / 1.32m wide.”*), and, ultimately, 3) precise 3D bounding boxes. Yet, the ability to reason about objects in 3D scenes is not only a part of general visual comprehension, but is also foundational in domains like robotics and AR / VR, e.g., for navigation and manipulation tasks .

There have been comparatively few works on 3D object perception with MLLMs ; moreover, they only consider a subset of tasks, and do not comprehensively assess depth and multi-view inputs. To address these limitations and facilitate a more holistic exploration of 3D understanding in MLLMs, we make these contributions:

1.  We propose a new data generation pipeline that leverages high-quality 3D scene data to produce image-text QA pairs for 3D object perception. We apply this pipeline to CA-1M to generate *Cubify Anything VQA (CA-VQA)*, a new spatial understanding dataset for MLLM fine-tuning, covering diverse indoor scenes. As additional inputs, CA-VQA uniquely includes multi-view images and different types of metric depth maps, both sensor-based and SOTA monocular (estimated) depth.

2.  We release a new spatial understanding benchmark derived from CA-VQA. Compared to existing benchmarks, ours 1) includes diverse tasks (incl. relative and metric distance / size estimation and 3D grounding), 2) provides rich input signals (multi-view and depth), and 3) is less susceptible to language priors (i.e., more vision-reliant) and hence more challenging. We show that even SO­TA models such as GPT-4o struggle on our benchmark.

3.  We run extensive experiments illustrating the benefits of CA-VQA as a testbed for spatial perception research. We show that 1) we can train MM-Spatial, a generalist MLLM achieving SOTA on spatial understanding benchmarks (CV-Bench, SpatialRGPT-Bench, CA-VQA), while retaining performance on other tasks (incl. general, knowledge, text-rich); 2) using multi-view and depth inputs further enhances 3D understanding; 3) MLLMs can achieve strong monocular depth estimation via SFT. We also study the efficacy of different depth maps, the impact of full encoding vs. tool-use for leveraging depth, and indoor-to-outdoor scene generalization.


![](../images/MM-Spatial_md_images/figures/Dataset_Sample.png)
<figcaption><strong>CA-VQA Data Example.</strong> Example of a single sample from our dataset. Each reference frame has between 0-4 multi-view support frames. All frames (reference and support) come with three metric depth maps: Ground truth (FARO laser), ARKit Depth (LiDAR-fused) and Monocular (DepthPro). Each support frame contains the relative pose from the reference image, along with camera intrinsics.</figcaption>


# Related Work

## General MLLMs

MLLMs have attracted significant research focus, tracing back to Frozen  and Flamingo , with more recent works such as LLaVA  and MiniGPT-4  introducing visual instruction tuning. The rise of open-source MLLMs has led to models rivaling SOTA commercial offerings like GPT-4o on certain tasks. Notable examples include Emu2 , VILA , Idefics2/3 , and Qwen2-VL , among others.

MLLMs research has explored several fronts: ($`i`$) scaling up the pre-training data  and supervised fine-tuning data ; ($`ii`$) enhancing high-resolution image comprehension ; ($`iii`$) studying various vision encoders  and vision-language connectors ; ($`iv`$) using mixture-of-experts ; ($`v`$) extending models to region-level  and pixel-level  understanding, multi-image reasoning , UI comprehension , and video understanding , among others.

## 3D Spatial Understanding with MLLMs

To complement work on (primarily) 2D spatial relationships / reasoning , recent research has aimed to also enable 3D reasoning with MLLMs, roughly split into two directions. Firstly, works focusing on scene-level 3D understanding (i.e., scene captioning and VQA) by enabling MLLMs to process representations of entire scenes, often leveraging multiple views and depth information. This includes ScanReason , 3D-CLR , 3D-LLM , ConceptGraphs , LLaVA-3D , Scene-LLM , M3DBench , Video-3D LLM , LSceneLLM , and 3DGraphLLM .

Secondly, works focusing on object-level 3D spatial perception. Spatial-VLM and Cube-LLM both use vanilla image-based VLMs (without any explicit 3D input) to address spatial relationship and metric distance estimation (Spatial-VLM) as well as 3D grounding (Cube-LLM). SpatialRGPT and VCoder encode (relative) depth maps as additional inputs via the image encoder plus a dedicated depth connector. SpatialBot instead leverages depth maps via tool-use by training the model to query the depth value at a given coordinate. In this work we build on these ideas, and further compare the utility of depth maps collected with dedicated specialized hardware to those derived from monocular depth estimators. We also study the benefits of providing additional views (images) to the model, i.e., frames preceding the main image in the video.

We provide an overview of previous SFT datasets and benchmarks for object-centric 3D spatial understanding in , highlighting the novelty and unique characteristics of our proposed CA-VQA dataset, to be detailed next.

# Data

We build upon the Cubify Anything 1M (CA-1M) dataset, which contains exhaustive 3D bounding boxes (gravity-aligned 7-DOF boxes with yaw orientation) for every object in the ARKitScenes dataset. Additionally, we provide human-labeled annotations for each object consisting of an open-set label ($`\sim`$<!-- -->3.3k unique noun labels for $`\sim`$<!-- -->350k objects), material, primary color, and shape.

## Data Generation Pipeline

We generate QA pairs from these annotations as follows:

- **Frame Sub-sampling.** To reduce the data volume and redundancy, we sub-sample the videos at 1 FPS for the training set and at 0.1 FPS for the evaluation benchmark.

- **3D Ground Truth Processing.** For each frame, we transform the 3D boxes from world to camera space using pose $`Rt_{i}`$. In contrast to CA-1M, 1) we include all boxes visible from the current view, irrespective of distance; 2) we do not clip boxes to the visible part, but rather store amodal 3D coordinates. We also construct a point cloud based on the ground truth depth map and camera intrinsics.

- **QA Pair Generation.** Based on our 3D and semantic annotations, we automatically generate template-based QA pairs (both open-ended and multi-choice ones), without any human supervision. We consider a variety of spatial task categories, detailed in and App. . We further ensure that questions are unambiguous. For example, asking *“What is the distance to the chair?”*, is only a valid question is there is a single instance of a chair.

- **Blind Filtering.** found that many samples of multimodal benchmarks can be solved without vision input due to the strong language priors of MLLMs. To reduce such bias we follow and remove all benchmark examples which are correctly answered *blindly* by at least three out of seven judges: GPT-4 , GPT-4V , GPT-4o , Phi-3-Vision-4B , LLaVA-OneVision-7B , SpatialRGPT-VILA1.5-8B , and our MM-Spatial-3B. App.  demonstrates the effectiveness of this strategy.

Overall, we obtain $`\sim`$<!-- -->10M QA pairs over 220K frames from 2K videos for the CA-VQA training set, and $`\sim`$<!-- -->62K QA pairs over 2.6K frames from 265 videos for the evaluation benchmark. shows QA examples from CA-VQA.

## Spatial Task Categories

CA-VQA covers the spatial task categories outlined below. App.  provides further details on the QA definitions.  
**Counting** (*“How many X are there?”*). Answers are computed by counting the 3D boxes of the given object class.  
**Viewpoint-dependent** (*“Is X behind Y?”*). Answers are based on the 2D / 3D boxes and depend on the camera pose.  
**Metric regression** (*“How far away is X from Y / the camera?” “How wide / tall is X?”*) Answers to size questions are computed using the 3D bounding box. Answers to distance questions are computed based on the object point clouds; we reject samples for which the 3D boxes overlap.  
**2D referring/grounding**. We use 2D bounding boxes computed by projecting the 3D bounding boxes to image space.  
**3D referring/grounding**. We use the 3D boxes in CA-1M.  
**Binary** (e.g., *“Is X taller than Y?”*). This covers *viewpoint-dependent* and (relative) *regression* questions, as well as *object presence* questions (*“Is X present in the image?”*).  
**Multi-choice**. We also formulate multi-choice QAs covering the other categories (except for 2D / 3D grounding).

**External benchmark templates.** We also generate examples using the QA templates proposed in CV-Bench and SpatialRGPT-Bench . This removes potential instruction following issues due to differences in QA formulations, hence allowing us to faithfully evaluate our model’s actual spatial understanding ability on those benchmarks.

## Multi-view and Metric Depth Data

visualizes the multi-view images and depth maps.

**Multi-view.** For each reference frame $`I_t`$, we sample $`N \leq 4`$ preceding support frames $`I_{t-1, ..., t-N}`$, which are triggered when camera pose $`Rt_i`$ has angular movement of $`\geq 15^{\circ}`$ or movement of $`\geq 30\text{cm}`$ from the current key frame $`Rt_b`$.

**Metric Depth.** For each frame (ref. & support), we provide:

- **Ground truth depth** acquired from a high-precision stationary FARO laser scanner, and rendered to each frame using the Barrabandi pipeline from ARKitScenes .

- **ARKit Depth** provided by the ARKit framework. It utilizes the iPad Pro’s on-device sparse LiDAR sensor and color image to produce a per-pixel dense depth map.

- **Monocular depth** generated using DepthPro , a state-of-the-art monocular metric depth estimation model.

**Depth: Chain-of-Thought (CoT) / Tool-Use.** will explore different ways to use the metric depth information. As an alternative to encoding the full 2D depth maps with the model (see ), we investigate a simpler approach that uses the individual depth values of the given objects as text. To this end, we prepare step-by-step examples involving textual GT depth in the format illustrated in . At test time, the depth values are then obtained either via 1) tool-use (see ), or 2) model prediction (CoT).

# Model


![](../images/MM-Spatial_md_images/figures/Depth_Tool-Use.png)
<figcaption>Example of leveraging depth maps via tool-use. The model predicts the objects’ 2D bounding boxes and function calls, receives the <em>tool outputs</em> (which is the median depth value within the box, marked with an <strong>×</strong>), and finally reasons about the answer.</figcaption>



![](../images/MM-Spatial_md_images/figures/Qualitative_Example.png)
<figcaption><strong>Qualitative Example.</strong> We show the predictions of various models on a challenging example from our CA-VQA benchmark. Strong commercial (2a&amp;b) and research models (2c&amp;d) fail. MM-Spatial(1a) is much better, and even more so with CoT enabled (1b), demonstrating our model’s strong object grounding (see predicted 2D boxes in the image), depth estimation, and spatial reasoning ability. Accuracy improves further when leveraging ground-truth depth via tool-use (1c), although our CoT model’s (1b) predictions are very close to that, for both the intermediate depth values and final answer; monocular estimated depth (1d) is less accurate and yields a worse result.</figcaption>


## Model Architecture

We use the MM1.5 architecture (focusing on the mobile-friendly 3B variant), comprising of a DFN-CLIP image encoder and a decoder-only LLM backbone, which are bridged via a C-Abstractor . We use an image resolution of 672×672 during fine-tuning, and further increase the effective resolution by using (static) image splitting with 4 sub-image splits (plus an overview image).

We also consider variants of our model that incorporate either multiple views or depth maps as additional inputs:

- **Multi-view.** Our model supports multi-image input, allowing us to concatenate multiple views into sequences $`I_{t-N}, ..., I_{t-1}, I_t`$. In this multi-view setting, we only apply image splitting to the reference (final) image $`I_t`$.

- **Depth: Full Encoding.** We use the image encoder to encode the normalized and colorized depth maps (i.e., replicating the depth map along the channel dimension), and introduce a separate depth connector, following SpatialRGPT . Notably, this approach is limited to using *relative* (normalized) depth. We also explore using textual *metric* depth in a purely data-driven way via Chain-of-Thought (CoT) or tool-use, see .

## Data and Training

We follow the 1) pre-training and 2) continual pre-training stages of MM1.5 . For the 3) supervised fine-tuning (SFT) stage, we start from the MM1.5 single-image SFT mixture, which includes datasets across multiple categories: *General* VQA, *Knowledge* (math, code, science), *Text-rich*, and 2D *Referring & Grounding* (VQA enriched with bounding boxes). We then add our CV-VQA data within a new *Spatial* category and select the mixture ratio based on the ablations discussed in App. . We use the same training hyperparameters as MM1.5 , with *unfrozen* image encoder and LLM. We use AXLearn for model training.

# Experiments

## Model Variants

We explore the following model variants in our study, leveraging the various input signals provided within CA-VQA:

- **MM-Spatial.** Trained on single-view RGB inputs, without depth information. This is our baseline model.

- **MM-Spatial+ Multi-view.** Trained on multi-view RGB inputs as described in . We use up to four support frames plus one reference frame. We additionally provide the camera intrinsics and pose information for each view (relative to the reference view) as JSON strings to the model (see ), interleaved with the images.

- **MM-Spatial+ Depth (Tool).** Trained on single-view RGB plus textual metric depth, with tool-use at test time, as described in . This approach relies solely on data, using the same model as **MM-Spatial**. We denote the depth source as **(Tool; GT)** for ground truth / FARO depth or **(Tool; Mon.)** for monocular depth.

- **MM-Spatial+ CoT.** Trained like **MM-Spatial+ Depth (Tool)**, but *without* using the depth tool at test time. Instead, the model predicts the metric depth values on its own based solely on the image input, producing a Chain-of-Thought (CoT) style response as in .

- **MM-Spatial+ Depth (Encoded).** Trained on single-view RGB inputs plus fully encoded depth maps, as described in . The depth source is denoted as above.

- **MM-Spatial(Blind eval).** Trained like **MM-Spatial**, but evaluated with text input only (i.e., without image input).

Some variants naturally lend themselves to combinations, e.g., **MM-Spatial+ Multi-view + CoT** is a model that sees multiple views and responds with CoT style answers.

## Overview of Benchmark Category Results

We aim to train a generalist MLLM that excels across a variety of tasks – instead of a specialist model that *only* excels at spatial reasoning. To this end, we follow MM1.5 and evaluate our models across 24 multimodal benchmarks using an internal fork of lm-eval-harness , covering the categories outlined in . To evaluate 2D and 3D *Spatial* understanding we use CV-Bench , SpatialRGPT-Bench , and our proposed CA-VQA benchmark.

shows results on aggregated metrics across the various benchmark categories. MM-Spatial significantly improves on the *Spatial* category while maintaining performance competitive with MM1.5 across the other categories, suggesting that spatial reasoning can be improved without meaningful compromise. See App.  for additional discussion. We now present an in-depth analysis of the *Spatial* results, comparing MM-Spatial with SOTA baselines. We use the full data mixture in by default; some ablations use *Specialist Models* trained only on CA-VQA.

## Results on our CA-VQA Benchmark

We assess the model variants outlined in , and also study the metric depth estimation ability of our CoT model. CA-VQA results are shown in ; a qualitative example is shown in . We make the following observations:

- **MM-Spatial vs. Baselines.** MM-Spatial-3B substantially outperforms various (much larger) top open-source and commercial models  - , incl. the SOTA GPT-4o model , demonstrating 1) their limitations in terms of spatial understanding and 2) the effectiveness of SFT on CA-VQA. Despite its focus on spatial reasoning, SpatialRGPT-VILA-1.5-8B underperforms, likely for a few reasons: 1) their OpenSpatialDataset (OSD) used for SFT leverages *axis-aligned* 3D boxes pseudo-annotated on OpenImages , resulting in significant discrepancies in spatial concept definitions (especially for metric quantities) compared to the high-quality (yaw-)*oriented* 3D boxes used for CA-VQA; see App.  for further discussion on this difference; 2) in OSD, objects are referred to via segmentation masks or 2D bounding boxes (*“How tall is Region $$
0
$$ `<mask/box>`?”*), while CA-VQA simply uses class names (*“How tall is the chair?”*); 3) SpatialRGPT is limited to using *relative* depth due to its full depth encoding approach. Finally, SpatialRGPT / OSD lacks support for 3D grounding.

- **Blind vs. Vision evaluation.** To validate our blind filtering strategy (see ) we note that GPT-4 performs poorly, whereas its vision counterpart, GPT-4V , performs better. MM-Spatial(Blind) , which is trained on similar data, also performs poorly on most tasks. While the performance on *Counting* and *Multi-choice* is still acceptable – likely due to inherent remaining biases such as the naturally skewed distribution of object counts – providing vision input still further improves performance by $`\sim`$<!-- -->15 points. App.  provides further detailed analysis of the effectiveness of our blind filtering strategy. Overall, our results suggest that our benchmark is less susceptible to a strong language prior compared to, e.g., SpatialRGPT-Bench (see ).

- **Multi-view vs. Single-view.** Multi-view is consistently better (e.g.  vs.  ), suggesting that our model can successfully use additional views to improve 3D perception.

- **Multi-view vs. Single-view + Depth (Tool; GT) .** While multi-view is competitive overall, on *Regression* using GT depth is much better. This suggests that using multiple views can partially compensate if depth sensors are not available, but on tasks that most directly rely on accurate depth (i.e., *Regression*), GT depth is unmatched.

- **CoT vs. Direct Prediction.** CoT prediction consistently improves over direct prediction (e.g.  vs.  ), suggesting that the additional multi-step supervision signal (incl. 2D object grounding and depth prediction) and/or leveraging more test-time compute benefits model accuracy.

- **Depth (GT): Tool-use vs. Full Encoding.** Full depth encoding performs much worse than tool-use , and is only slightly better than the RGB-only baseline . Firsty, this highlights the effectiveness of the simple tool-use approach in utilizing *metric* depth (while full encoding can only use *relative* depth). Secondly, this indicates the difficulty of effectively encoding and interpreting full depth maps with an MLLM – the simple architecture proposed by may be too limited in this regard, suggesting that further research is required in this direction.

- **Depth (Tool): Ground Truth vs. Monocular.** Despite DepthPro being a strong monocular depth estimator, its limitations are still apparent on our benchmark, especially for metric estimation. This is particularly visible on the *Ego-Distance* task which most directly relies on accurate depth estimation: monocular depth  1) performs substantially worse than GT depth , and 2) even regresses compared to the RGB-only baseline , suggesting that our model itself can learn to accurately predict depth.

- **Depth-tool (Monocular) vs. CoT.** Our CoT approach (which requires MM-Spatial to explicitly predict depth) performs better than tool-use with monocular depth , again most noticeable on *Ego-Distance*. This again hints at MM-Spatial’s strong inherent metric depth estimation ability, which we analyze in more detail below.

**MM-Spatial’s Metric Depth Estimation Ability.** and show (quantitatively and qualitatively, respectively) that, surprisingly, our model’s monocular metric depth estimation accuracy can even rival that of the SOTA DepthPro specialist model. While DepthPro is a general-purpose depth estimation model whereas MM-Spatial is trained only on indoor scenes which aligns well with the CA-VQA benchmark[^2], these results still intriguingly suggest that MLLMs are capable of acquiring strong metric depth estimation abilities solely via data curation.

## CV-Bench Results

The CV-Bench results in demonstrate that MM-Spatial-3B significantly outperforms the much larger SOTA Cambrian-1-34B , highlighting the effectiveness of SFT on similar data. CoT and leveraging monocular (DepthPro) depth input via tool-use again further boost performance. MM-Spatial achieves almost perfect accuracy on the indoor splits of the 3D tasks, and also demonstrates strong out-of-domain generalization to the outdoor splits. Notably, MM-Spatial(Blind eval) achieves the best accuracy among all models on the 2D Object Count task, revealing a substantial bias in this benchmark. In contrast, on our CA-VQA benchmark, using vision input outperforms the blind baseline on *Counting* by $`\sim`$<!-- -->13 points.

## SpatialRGPT-Bench Results

shows SpatialRGPT-Bench results. Notably, to align with the OpenSpatialDataset (OSD) used to train SpatialRGPT, SpatialRGPT-Bench is also based on *axis-aligned* 3D boxes (AABBs), resulting in spatial concept definitions different to CA-VQA (see App. ). SpatialRGPT thus underperformed on CA-VQA, and similar issues arise when evaluating MM-Spatial on their benchmark . To enable a fair comparison of model capabilities, we thus align with the benchmark by generating *CA-VQA$`^\star`$*, a variant of CA-VQA adopting their AABB-based definitions, and train MM-Spatial on that. We also train on OSD for comparison. For MM-Spatial+ Depth we use monocular (DepthPro) metric depth via tool-use. We observe the following:

- **Indoor vs. Outdoor.** While MM-Spatial trained on CA-VQA$`^\star`$ achieves strong performance, it cannot significantly outperform the SOTA . Analysis reveals that while the model excels at indoor samples , it fails to generalize to outdoor samples , particularly on the *Metric* tasks. We hypothesize that this is mainly attributed to the vast difference in metric scales between indoor and outdoor scenes, especially for object distances. We verify this with a simple *scale augmentation* approach: we generate additional *Distance* examples with scaling factors (sampled uniformly from $`[1,10]`$) applied to our underlying indoor scenes (i.e., 3D boxes and point clouds), resulting in a wider range of metric distances. We confirm that MM-Spatial trained on CA-VQA$`^\star`$ + scale aug.  substantially improves performance on the outdoor *Distance* tasks , resulting in SOTA performance overall.

- **CA-VQA$`^\star`$ vs. OSD.** Training on OSD (based on diverse OpenImages data) results in strong performance both indoor and outdoor . However, training on CA-VQA$`^\star`$ still yields significantly better indoor performance overall , suggesting that our high-quality 3D GT is more effective than OSD’s pseudo-annotations. When using CA-VQA$`^\star`$ + scale aug. , we become competitive with OSD even on outdoor *Distance*, but still lack on outdoor *Width / Height*. Combining CA-VQA$`^\star`$ with OSD results in significant improvements, emphasizing the complementary benefits of the two datasets.

- **MM-Spatial vs. SpatialRGPT.** MM-Spatial-3B outperforms the SOTA SpatialRGPT-VILA-1.5-8B with different data mixtures  - , with and without depth input (SpatialRGPT uses depth maps via full encoding).

- **Depth vs. Image-only.** Leveraging monocular *metric* depth via tool-use significantly improves performance for MM-Spatial( vs.  ). SpatialRGPT-7B benefits less from fully encoding *relative* depth ( vs.  ).

- **Blind vs. Vision evaluation.** MM-Spatial trained on OSD (Blind eval) performs well on several tasks, and GPT-4 was the prior SOTA for *Width*. This suggests that SpatialRGPT-Bench and OSD suffer from significant biases and do not probe spatial perception alone.

# Conclusion

We made several contributions towards unlocking object-centric 3D spatial understanding in MLLMs. First, we proposed a data generation pipeline, resulting in the CA-VQA SFT dataset for 3D perception tasks (incl. multi-view and depth inputs). Second, we introduced a new 3D spatial understanding benchmark, which includes tasks such as spatial relationships, metric estimation, and 3D grounding. Third, we demonstrated that our MM-Spatial model can achieve SOTA performance on spatial reasoning benchmarks, while preserving general MLLM capabilities. Lastly, we investigated how adding multi-view and depth as input modalities can further improve the model’s spatial perception ability, and demonstrated that MLLMs can acquire strong monocular depth estimation capabilities via SFT. In future work, we aim to extend our scope to outdoor scenes to complement our high-quality indoor dataset.

## Acknowledgments

We would like to thank Anshul Shah, Lin Chen, Wei Liu, Ian Fasel, Alkesh Patel, Omer Hadad, Haoxuan You, Haotian Zhang, Wentao Wu, Philipp Dufter, Sergiu Sima, Sai Aitharaju, Albert Antony, David Haldimann, Michael Emmersberger, for helpful discussions and feedback.


![](../images/MM-Spatial_md_images/figures/QA_Examples.png)
<figcaption> <strong>CA-VQA Overview.</strong> Example QA pairs from our Cubify Anything VQA (CA-VQA) dataset, aiming to unlock object-centric 3D spatial understanding in MLLMs. Using high-quality 3D ground truth annotations from CA-1M , we generate spatial perception questions across a variety of different tasks, e.g., involving <strong>relative relationships</strong>, <strong>metric measurements</strong>, and <strong>3D object bounding boxes</strong>. </figcaption>


# More Details about the CA-VQA Data

## Spatial Task Categories

We here provide more details on the different spatial task categories covered in CA-VQA, with visualizations of examples provided in .

- **Binary**.

  - **Viewpoint-Dependent**. We consider the spatial relationships *left vs. right* and *in front vs. behind* between two objects, as determined from the current camera pose / viewpoint:[^3]

    - *Left vs. Right*. We determine the answer based on the horizontal coordinates of the objects’ 2D bounding box centers.

    - *In front vs. Behind*. We determine the answer based on the distances between the camera and the objects’ 3D bounding box centers.

  - **Relative Object Size**. We determine the answer based on the objects’ *width*, *length* or *height*, as defined in **Regression** below.

  - **Object Presence**. For each sample asking about an object present in the image, we also generate a negative sample which asks about a (randomly sampled) object *not* present in the image, to ensure a uniform distribution over answers (*Yes / No*).

- **Counting**. We determine the answer by simply counting the number of bounding boxes present in the image for a given object class. We also generate negative samples with (randomly sampled) objects not present in the image (i.e., such that the correct answer is 0).

- **Multi-choice**. This covers questions across the other spatial task categories, except for 2D and 3D grounding. We randomize the order of the options, obtaining the incorrect options as follows:

  - **Regression (Metric Estimation)**. We compute three wrong options with either 10% increments deviating from the real answer, or 5cm, whichever value is larger.

  - **Counting**. We always ensure that 0 is an option (i.e., object is not present). We then randomly sample (additional) wrong options among the non-zero integers within $`[\text{GT}-3, \text{GT}+3]`$ (where GT is the correct answer), s.t. the total number of options is 4.

  - **2D / 3D Referring**. We randomly sample three wrong object classes.

- **Regression (Metric Estimation)**.

  - **Egocentric Distance**. The distance between the camera and the *closest* point of the object’s point cloud.

  - **Object Distance**. We consider both (minimum) distance and center distance between two objects:

    - *(Minimum) Distance*. The distance between the *closest* points of the two objects’ point clouds (i.e., minimum point distance).

    - *Center Distance*. The distance between the *center* points of the two objects’ 3D bounding boxes.

  - **Object Size**. We consider the 3D dimensions *width*, *length* and *height*, defined as follows:

    - *Width.* The length of the *larger* horizontal edge of the object’s 3D bounding box (i.e., $`\max(x_\text{len}, z_\text{len})`$).

    - *Length.* The length of the *shorter* horizontal edge of the object’s 3D bounding box (i.e., $`\min(x_\text{len}, z_\text{len})`$)

    - *Height.* The length of the vertical edge of the object’s 3D bounding box (i.e., $`y_\text{len}`$).

- **2D Grounding**. We use the 2D bounding box obtained from projecting the object’s 3D bounding box into 2D image space.

- **3D Grounding**. We directly use the 3D bounding boxes provided in CA-1M .


![](../images/MM-Spatial_md_images/figures/Spatial_Category_Examples_1.png)
<figcaption>Examples of CA-VQA data samples from the Binary, Counting and Multi-choice categories.</figcaption>



![](../images/MM-Spatial_md_images/figures/Spatial_Category_Examples_2.png)
<figcaption>Examples of CA-VQA data samples from the Regression (Metric Estimation) and 2D Grounding categories.</figcaption>


## Depth: Chain-of-Thought (CoT) / Tool-Use

We prepare multi-step CoT responses involving depth for questions within the *Binary* (only “behind vs. in front”) and *Regression (Metric Estimation)* categories, as the ground truth answers for those rely on depth information. We also did preliminary experiments with *3D Grounding* samples, but found that performance does not improve / even slightly regresses there, so we did not include any such samples in the final dataset.[^4]

The sequence format of the samples is illustrated in , involving the target objects’ 2D bounding boxes and depth values and the final (original) answer. We use the GT depth maps for generating the training examples, extracting the median depth value within the object’s 2D bounding box[^5]. At test time, we then consider two alternative approaches for obtaining the depth values:

- **Model prediction (CoT)**. We let the model predict the depth values (called *CoT* in the experiments). As the model was trained on sequences involving the ground truth depth values, the models learn to predict depth. Our experiments reveal the accuracy of the resulting depth estimates.

- **Tool-use**. We allow the model to leverage a given depth map via tool-use. I.e., for a function call of the form $`\text{Depth}(bbox) \rightarrow`$ we extract the median depth value within the 2D bounding box, insert the depth value into the sequence, and then let the model continue its prediction to arrive at the final answer (see ).

# Optimal Data Mixture for MM-Spatial

We aim to build a generalist MLLM that excels across a variety of diverse tasks – as opposed to a specialist that *only* excels at spatial understanding. To this end, we identify the mixture weight for the new spatial data that achieves the best performance trade-off between the spatial vs. all other benchmark categories: general, knowledge, text-rich, 2D referring & grounding. Investigating the effect of adding a new model capability is particularly relevant for models with limited capacity, such as the 3B model we consider.

Results are shown in . MM-Spatial maintains similar performance as the MM1.5 baseline across most task categories, while significantly improving on the Spatial category. This suggests that our model can successfully adopt the new spatial understanding capability without regressing on all the other capabilities, resulting in a generalist MLLM. The data mixture ratio of 2:1 (spatial:general) provides a good performance trade-off and is used for MM-Spatial throughout. We also consider a spatial *Specialist Model* that is trained on CA-VQA only; however, this model provides only a small improvement on the spatial category, while regressing substantially on all other benchmark categories. We use specialist models for some of our ablations to speed up experimentation. shows the detailed result breakdowns across the different task categories, compared to SOTA models.

# Results on Further Benchmark Categories

We here present a more detailed analysis of MM-Spatial compared with SOTA baselines across the different benchmark categories. Results on general and knowledge benchmarks are shown in , results on text-rich benchmarks are shown in , and results on 2D referring & grounding benchmarks are shown in . Overall, we observe that our MM-Spatial model maintains a level of performance similar to the vanilla MM1.5 baseline. This suggests that our model is able to successfully adopt the new spatial understanding capability without sacrificing performance on all the other model capabilities, resulting in a generalist MLLM.

# Analysis of Blind Filtering Procedure

analyses the effectiveness of our blind filtering procedure outlined in in ensuring that our CA-VQA benchmark becomes more reliant on vision input. This is in contrast to some of the tasks from the other spatial understanding benchmarks we consider (CV-Bench and SpatialRGPT-Bench), where we found that blind models can perform very strongly and even rival models with vision input in some cases (see ). Hence, these benchmarks would likely also benefit from blind filtering.

# Axis-aligned vs. Oriented 3D Boxes

emphasizes the fundamental difference between axis-aligned (AABB) and oriented (OBB) 3D bounding boxes and how they affect the resulting object dimensions. This provides an indication of the misalignment issues arising when evaluating a model trained on data based on OBB ground truth (i.e., MM-Spatial, which is based on the gravity-aligned 7-DOF yaw-oriented 3D bounding boxes from CA-1M) on a benchmark based on AABB ground truth (i.e., SpatialRGPT-Bench) and vice versa (i.e., evaluating SpatialRGPT on CA-VQA), as seen in .


![](../images/MM-Spatial_md_images/figures/AABB_vs_OBB.png)
<figcaption>Comparative visualization of axis-aligned vs. oriented 3D bounding boxes, taken from the SpatialRGPT paper . The object dimensions computed from AABBs can differ substantially from those computed from OBBs, depending on the object’s rotation. For sake of illustration, assume that the sofa is 2m wide and 0.8m deep. We then obtain the following altered object dimensions when using an AABB instead of an OBB, at different yaw rotation angles (i.e., considering 7-DOF bounding boxes that are gravity-aligned / parallel to the ground, as in CA-1M / CA-VQA): width ≈ 2.1m and depth ≈ 1.7m with 30<sup>∘</sup> rotation; width ≈ 1.7m and depth ≈ 2.1m with 60<sup>∘</sup> rotation; and width = 0.8m and depth = 2m with 90<sup>∘</sup> rotation (i.e., “full” rotation resulting in swapped dimensions).</figcaption>


[^1]: $`^\dagger`$Equal contribution. E-Mail: `edaxberger@<company>.com`

[^2]: Note that DepthPro’s training data mixture includes ARKitScenes (which CA-VQA and thus MM-Spatial’s training data is based upon), so this is not a zero-shot evaluation for either model.

[^3]: Note that we do not consider *above vs. below* to avoid ambiguity: “above” could either refer to 2D image space (i.e., the 2D bounding box of A is above that of B), or to 3D space, where the latter can be ambiguous as well (i.e., do we just require that the 3D bounding box of A is located higher in terms of vertical dimension, or do we also require that A is located directly above B in terms of horizontal dimensions – the latter might best match with how humans colloquially define “above”).

[^4]: We hypothesize that 3D grounding is too complex of a task to benefit from the simple depth information provided in the multi-step CoT answers, and that the model might just get confused. We leave a more comprehensive study of how to benefit 3D grounding with CoT for future work.

[^5]: We also did preliminary experiments with other ways to extract a single depth value from the depth map within the 2D bounding box, such as the value at the center of the box or percentiles other than the median, but did not see significant improvements over using the median, which we found to be a robust choice.
