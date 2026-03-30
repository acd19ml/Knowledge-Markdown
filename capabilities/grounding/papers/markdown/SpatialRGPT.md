# Introduction

Understanding spatial arrangements in both 2D  and 3D  spaces is crucial for accurately interpreting complex visual environments. Despite the impressive advancements in Vision Language Models (VLMs) across a variety of tasks such as image classification , captioning , object detection , video understanding , and document parsing , etc., these models still face significant challenges with spatial reasoning. This includes difficulties  in distinguishing simple spatial concepts like "left" and "right," "above" and "below," as well as more complex relationships such as "behind" and "in front," "inside" and "outside," and "near" and "far." The ability to comprehend and reason about these spatial relationships is fundamental not only for visual understanding, but also for enabling practical applications in fields like robotics  and augmented reality , where precise spatial awareness is crucial for tasks such as navigation , manipulation , and interaction with real-world environments .

Recently, several works   has advanced VLMs’ spatial reasoning capabilities by introducing a comprehensive data generation pipeline that enables large-scale training with spatially-aware visual question answering (VQA) tasks. This approach is based on the hypothesis that the limited spatial reasoning capabilities of current VLMs are due to a lack of 3D/2D spatial knowledge in their training data. However, two critical challenges remain. First, effective spatial reasoning requires VLMs to accurately parse regional information, particularly the regions of object instances, whereas most existing VLMs are primarily designed to understand the global context of an image. When an image contains numerous instances, it becomes challenging to prompt the model to reason about the spatial relations between specific instances. This is because most VLMs function as global image parsers and do not support specifying regions for which users want to understand spatial relationships. Second, accurately perceiving spatial relations such as direction and distance cannot rely solely on RGB pixel data. Thus, the architecture needs to incorporate 3D inputs, such as depth information.

In this work, we propose SpatialRGPT, leveraging a data curation pipeline, along with a region and 3D-aware visual encoder architecture to improve the spatial reasoning capability of VLMs.

Our data pipeline automatically generates 3D, region-aware annotations from 2D images at scale by constructing a 3D scene graph for each image, where nodes represent object instances and edges denote spatial relationships. This is achieved through three scalable components: (i) open-vocabulary detection and segmentation for instance extraction, (ii) metric depth estimation, and (iii) camera calibration for projecting objects into 3D space. These scene graphs are subsequently transformed into region-aware spatial QA tasks using both template-based and large language model (LLM)-based approaches. This dual approach provides region-based VLMs with the necessary spatial knowledge and advanced reasoning capabilities to interpret complex environments. We use the collected data to train SpatialRGPT. While SpatialRGPT is designed to support region prompts, it effectively avoids the ambiguity issues found in SpatialVLM. In SpatialVLM, multiple similar objects in an image can confuse caption labels. In contrast, our pipeline naturally handles these scenarios without requiring carefully crafted rules or extensive post-processing.

Similar to RGPT , SpatialRGPT introduces a region representation module that allows region proposals to be included as additional inputs alongside the image. This approach enables the LLM to leverage both regional and global contexts, allowing the model to reason about relationships between local regions while maintaining an understanding of the overall scene. In addition, we propose a novel architecture that features a flexible “plugin” module for integrating relative-depth information into the visual encoder of existing VLMs. This design allows a pre-trained visual encoder to optionally learn additional depth representation while still functioning effectively when depth inputs are absent. Our experiments demonstrate that this design can substantially improve the spatial reasoning capabilities compared to VLMs that only use RGB images as input. Furthermore, we highlight practical applications enabled by SpatialRGPT, such as serving as a region-aware dense reward annotator and a stand-alone complex spatial reasoner. Our work has four main contributions:

1.  We present SpatialRGPT, a framework that enhances region-level spatial reasoning in VLMs by enabling effective representation of regional information and acquisition of spatial knowledge. Our novel architecture also integrates depth information flexibly, significantly improving 3D perception and analysis.

2.  To facilitate model training, we introduce a scalable data pipeline that constructs region-aware spatial reasoning QAs from existing datasets. With the pipeline, we create the Open Spatial Dataset (OSD), encompassing 8.7M spatial concepts grounded in 5M unique regions.

3.  To address the absence of a benchmark for evaluating spatial cognition in VLMs, we present SpatialRGPT-Bench, a comprehensive benchmark based on ground-truth 3D annotations that span indoor, outdoor, and simulated environments.

4.  We demonstrate downstream applications of SpatialRGPT. Leveraging SpatialRGPT’s region capabilities, we develop a region-aware dense reward annotator for robotics. Additionally, we show that SpatialRGPT can function as a stand-alone complex spatial reasoner, as well as its capacity to perform multi-hop reasoning.

# Related work

#### Spatial Reasoning via Large Language Models.

Recently, there has been a significant push to obtain spatial reasoning capabilities using LLMs. Initiatives  have focused on reconstructing scenes from multi-view images, such as point clouds or neural fields, and enhancing these representations with dense semantic features. The resulting 3D representation and dense features are then integrated into an LLM. However, multi-view images are not always available, and constructing a scene explicitly with dense semantic features is resource-intensive. Additionally, the modal gap between 3D representations and language often results in decreased performance. ConceptGraph  avoids directly incorporating 3D representations into LLMs. Instead, it constructs a scene graph and integrates this with the LLM. Yet, recent studies  indicate that LLMs struggle to utilize coordinate information effectively when presented in text, which can undermine their ability to understand and reason about spatial relationships. Our research is most aligned with SpatialVLM , which uses 2D VLMs to understand spatial relationships and metric distances. Unlike the above approaches, the spatial understanding is encoded implicitly. The VLM directly handles the spatial relationship problem without an explicit 3D representation or scene graph. However, SpatialVLM relies on language descriptions of objects as input, while LLMs can already resolve some spatial queries even without visual data . The responses can be inferred directly from the questions or derived from the world knowledge embedded in LLMs. This reliance on textual cues suggests that the training may not effectively teach VLMs to learn spatial reasoning from visual data. Additionally, SpatialVLM lacks the capability to specify regions precisely. This is particularly problematic in real-world scenarios where describing ambiguous locations or objects in language can be challenging.

#### Region-level Visual Language Models.

KOSMOS-2 , Shikra , MiniGPT-2 , CogVLM , SPHINX , and LLaVA  have enabled MLLMs to achieve region-based image understanding. However, these methods provide region information in textual form, such as bounding box coordinates. This method heavily depends on the language decoder to understand the position. In contrast, VisionLLM , GPT4RoI ,  , and Ferret , along with GLaMM , use spatial boxes with ROI-aligned features to map region-level features into the LLM word embedding space. However, bounding boxes can include unwanted background features, leading to inaccurate alignment between region descriptions and text, which complicates spatial reasoning. Recently, RegionGPT  and Osprey  have introduced visual spatial-aware modules that can directly extract pixel-level features. These models support using input masks that can accommodate regions of any shape. Despite these advancements, none of these approaches specifically focus on enhancing spatial reasoning at the region level in VLMs. Our framework is based on RegionGPT’s ability to process pixel-level inputs, with the aim of deepening spatial reasoning within region VLMs.

# Method

SpatialRGPT is a powerful multimodal language model adept at understanding both 2D and 3D spatial arrangements. It can process any region proposal, such as boxes or masks, and provide answers to spatial reasoning questions. While effective training dataset is the key to learn spatial-aware region representation, we introduce: (i) how to build 3D scene Graph from a single image, in Sec. , and (ii) how to facilitate visual representation learning from these scene graphs in Sec. . We propose a novel SpatialRGPT visual encoder architecture that flexibly leveraging monocular depth information into an existing 2D VLM, in Sec. , with training detail explained in Sec. .

## 3D Scene Graph from Single 2D Images

Our scene graph construction pipeline (Figure) begins with a filtering process to remove any unsuitable images (Appx.). Using open-vocabulary models, we identify and ground candidate objects, followed by lifting them into 3D space using metric depth estimation and camera calibration. We then process the point clouds (Appx. ) to construct the final 3D scene graph.

#### Open-Vocabulary Detection & Segmentation.

Segmenting objects is the initial stage of building a scene graph. Our models must satisfy two criteria: (i) object descriptions, e.g., class labels, should adhere to an open-world setting for better generalization; (ii) mask proposals need to be highly accurate, ensuring precise contour outlines. This precision is crucial, as even small deviations can lead to significant inaccuracies in the resulting 3D bounding boxes. To this end, we first employ an open-vocabulary image tagging model  to identify all the object classes present in the image. Next, we use GroundingDino , an open-vocabulary 2D detector to determine the corresponding object bounding boxes. Finally, we apply segmentation models  to refine these bounding boxes into precise masks. We do not use existing dataset annotations since they either fall short due to vocabulary limitations, or use polygon annotations  or compressed masks  for segmentation.

#### Metric Depth Estimation.

Several studies have explored the recovery of metric depth from a single image. The main challenge is to address the scale ambiguity, and one common approach  is to use relative depth along with metric heads fine-tuned on specific metric datasets. However, these methods may tend to overfit the depth scale for particular datasets such as KITTI  or NYU , which makes them less robust for in-the-wild images. Recently, Metric3Dv2  takes focal length as input and is trained end-to-end to predict metric depth and surface normals. The model is trained jointly on diverse indoor and outdoor scenes, making it less prone to overfitting to the depth distribution of specific datasets. We adopt Metric3Dv2 as our metric depth estimator and found that Metric3Dv2 together with WildCamera ’s camera intrinsic, is robust for images taken in real-world settings. Additionally, thanks to the joint depth-normal optimization training in Metric3Dv2, the recovered geometry is improved particularly around object edges.

#### Camera Calibration.

Camera calibration includes (i) intrinsic estimation to back-project depth maps to 3D point clouds, and (ii) scene canonicalization to ensure that scene relations are described in a shared space. To estimate the camera intrinsic, we use the WildCamera model , which estimates four DoF intrinsic parameters (focal point and focal length in two dimensions). This model excels in real-world scenarios due to its scale-awareness and ability to detect image cropping. To convert the camera coordinates of the point cloud into a canonicalized geodetic coordinate system for each scene, we leverage PerspectiveFields , which provides per-pixel up-vectors and latitude values that can be transformed into camera extrinsics, such as pitch and roll. Using these, we derive a rotation matrix to convert the point cloud from camera coordinates to geodetic coordinates. We note that while SpatialVLM  uses surface segmentation (e.g., "floor," "tabletop") to identify a horizontal plane and then uses the normal axis of this plane to align the point cloud to the horizontal plane, this approach is limited by the presence of specific classes, such as floors or tables. Additionally, the plane segmentation may fail if there are not enough points for RANSAC.

#### Constructing 3D Scene Graph.

The 3D scene graph is a collection of tuples where the nodes represent specific 3D object instances, and the edges represent the spatial relationships between the nodes. Each node is defined by the object’s `class`, `width`, and `height` in metric scale. To create the node, we start by using the instance mask to deproject the object points from the depth map. Then, we perform canonicalization and denoising, and build 3D axis-aligned bounding boxes for each object. With the 3D bounding box, we calculate the width and height of the objects in real-world units. The edges represent the spatial relationships between the nodes within two types of relations: relative and metric. Relative relations contain `left`, `right`, `above`, `below`, `behind`, `front`, `wide`, `thin`, `tall`, `short`, `big`, and `small`. Metric relations include `direction`, `direct distance`, `horizontal distance`, and `vertical distance` between the two objects. We then traverse all the object nodes and use the point cloud centroids and bounding boxes to calculate their spatial relationships.

## Learning Spatial-aware VLMs from 3D Scene Graph

In this section, we discuss converting the constructed 3D scene graph into textual representations for VLM training. One simple approach is through template-based methods via predefined handcrafted instructions. However, this approach limits the diversity of instructions and hinder the model’s reasoning capabilities. Thus, we employ additional complex QAs to enhance the model’s reasoning ability. Our results in Figure  show that blending these two types of data can lead to a generalized and complex spatial reasoning model.

#### Template-based Question Answering.

These QAs serve as the foundation for learning basic spatial knowledge. We extract information about node attributes such as width and height, as well as relative and metric relations from the edge attributes. We create both qualitative and quantitative templates to generate questions and answers for each type of attribute, using entities in the form of `Region [X]`. This approach results in examples shown in the first row of Figure . We provide detailed templates for each attribute in Appx. .

#### LLM-based Complex Reasoning Question Answering.

We employ Llama3-70B to generate complex spatial reasoning questions to enhance the model’s spatial reasoning capabilities. One approach is to input the scene graph directly into the LLMs. However, LLMs struggle to utilize 3D coordinate information effectively , so we opt for an alternative approach. We first construct spatial descriptions in a language format. Similar to the template-based approach, we extract attributes from the scene graph and then construct template-based spatial descriptions based on these attributes. We combine the spatial descriptions and the region tags as inputs to the LLM. The LLM is then tasked with creating a complex reasoning question and answer that is based on the description and matches the context. Examples of LLM-generated QAs are shown in the second row of Figure . Our LLM prompts for generating QAs are provided in Appx. .

We use our automated annotation pipeline to annotate images from the OpenImages  dataset, which covers a wide range of subjects and is of high resolution. The resulting Open Spatial Dataset (OSD) contains 1M unique images and 5M open-vocabulary regions, each associated with a bounding box and segmentation mask. Furthermore, the dataset includes 8M template-based QAs and 700K LLM-based QAs.

## VLM Architecture

An overview of SpatialRGPT’s VLM architecture is shown in Figure . SpatialRGPT consists of a visual encoder (Appx. ) to encode vision features, a region-feature extractor  to obtain region-level embeddings (Appx. ), linear connectors (Appx. ) to project multi-modal embeddings into the word embedding space, and a large language model using LLaMA2-7B for language processing. In this section, we will explain why and how we incorporate depth information into SpatialRGPT, as well as how SpatialRGPT handles tokenizations.

#### Plugin Module for Relative-depth Inputs.

VLMs that learn solely from RGB pixels are ineffective for 3D perception tasks. Direct learning from 3D data, like point clouds, presents challenges due to issues with scale and diversity. To bridge this gap, we propose using relative depth maps, which can be obtained through off-the-shelf models , to provide additional depth information alongside RGB images as input to our network. Our goal is to elicit geometric reasoning capability through depth guidance. However, this goal is non-trivial. Most VLM’s visual encoders are typically only trained with text and 2D images, and simply concatenating RGB and depth features may negatively impact performance. To address this, we introduce an add-on module that seamlessly incorporates the depth information. We use the same image encoder to process the depth map and generate depth feature maps. Then, we employ an additional depth-to-language connector to project the features into the language domain. The depth connector’s weights are initialized from the RGB connector and trained only on spatial-related QAs. This flexible design allows the 2D visual encoder to leverage additional depth representation while still functioning when depth inputs are not presented, thus avoiding the need for a vast amount of training data.

#### Tokenization and Prompt Format.

We generate multi-turn conversation data following  for each image and make the image the initial input for the first instruction, providing contextual information. Specifically, we incorporate a prefix prompt: “`<image>`$`\backslash`$`n`". The `<image>` is a special token that acts as a placeholder, which would be replaced by the image-level embedding from the vision encoder. When specific mask regions are mentioned in the user input, we use special tokens `<region>` and `<depth>` as placeholders. Each region token will be substituted with the corresponding region RGB embedding and depth embedding. All image-level, region-level RGB/depth tokens and text tokens are interleaved and fed as the input to the LLM for an auto-regressive generation.

## Training and Inference Paradigm

SpatialRGPT training includes three stages : (i) Connector Feature Alignment, (ii) Visual Language Pre-training, and (iii) Visual Instruction-tuning. During the first stage, CC3M image-caption pairs are used to pretrain the RGB connector as . In the second stage, the visual language corpus from MMC4  and COYO  is used to pretrain the LLM and the RGB connector. The RGB connector and LLM parameters are then frozen, with only the depth connector trainable and pre-trained on our OSD dataset. Finally, at stage three, we fine-tune the pre-trained model on visual language instruction-following datasets, using a combination of the instruction tuning dataset from , region-level instruction tuning data , and our OSD dataset. Detailed data blend of the visual instruction data is in Appx. . For training region-level data and our OSD, we randomly sample from different modalities (e.g., box, mask) for each sample to ensure the model is versatile to the input modality. At inference time, SpatialRGPT can take both boxes or masks as input. For the results shown in the main paper, if the segmentation is available, we use the mask; if not, we use the box provided and apply SAM to segment the corresponding mask.

# Experiments

We evaluate the effectiveness of our proposed SpatialRGPT in three aspects: (1) spatial reasoning benchmarks (Section ), (2) standard vision-language benchmarks (Section ), and (3) real-world applications (Section ).

## 3D Spatial Reasoning Benchmarks

Currently, there are no visual-language benchmarks that specifically focus on VLM’s ability to understand 3D spatial concepts like metric distance or size differences between objects. Recently, SpatialVLM created a spatial reasoning VQA benchmark using human labelers to annotate spatial information on 2D images, but this benchmark is not publicly available. To address this gap, we develop SpatialRGPT-Bench, a spatial reasoning VQA benchmark using data from both urban (nuScenes , KITTI ) and indoor (SUNRGBD , ARKitScenes ) environments, as well as simulated scenes (Hypersim ). These datasets cover various potential applications and include diverse object types, enhancing our benchmark’s thoroughness. We use preprocessed 3D cuboids for each object from Omni3D , all positioned within a unified 3D camera coordinate system and categorized by object classes. With these 3D cuboid annotations, we developed a conversational benchmark using our data generation pipeline. This benchmark comprises 657 qualitative and 749 quantitative VQA pairs, covering 88 distinct classes. All the samples come from the validation or test splits of the original datasets and are unseen by SpatialRGPT during the training phase. Please see Appx.  for statistics and examples of SpatialRGPT-Bench.

We consider three categories of models as baselines:

**Blind LLMs w/ Language Referral.** The blind  LLM model relies solely on text and generates answers using only the content of the question. To enhance this approach, we prepend the object class to each question. This method serves as a baseline to gauge how much spatial reasoning can be derived from purely existing world knowledge. We choose GPT-4 to represent this baseline, as it is the most advanced model for encapsulating comprehensive world knowledge.

**VLMs w/ Language Referral.** The setup is similar to the blind LLMs but includes access to visual content, which could allow the model to answer better than a blind LLM. We employ current state-of-the-art VLMs, GPT-4V and LLaVA-v1.6-34B , as baselines for this category.

**Region-aware VLMs.** This category explores models with region-level capabilities similar to our method. The models do not receive any language captions or object class information related to the region of interest; they rely solely on their visual processing capabilities. We equip GPT-4V  and LLaVA-v1.6-34B with Set of Marks (SoM)  to enable region-referring capabilities. Additionally, we include KOSMOS-2 , a VLM capable of taking bounding box inputs to reference objects, and RegionVILA (RegionGPT  with VILA  pre-training). RegionVILA-7B also serves as an ablation baseline to our method; it shares the same model architecture as our SpatialRGPT-7B$`_(rgb)`$ variant but is trained without our specialized spatial VQA dataset.

We use GPT-4 to evaluate the response for each model; please see Appx.  for details. For qualitative QAs, GPT-4 scores the alignment between the model’s response and the correct answer as 0 or 1. For quantitative QAs, GPT-4 standardizes numerical values across units into meters; we then calculate accuracy and error metrics. We present the results in Table . The upper rows of the table show accuracy (correct vs incorrect or failed to answer) for qualitative QAs. The lower rows report on quantitative QAs, detailing their success rate (answers within $`\pm`$<!-- -->25$`\%`$ of the ground truth value) and the absolute relative error . We exclude answers that failed to produce a numerical response from the relative error calculations. The results show that SpatialRGPT significantly outperforms baselines in terms of success rate for qualitative QAs and maintains the lowest error rate for quantitative QAs. Interestingly, we found that blind LLMs and VLMs with language referrals achieved commendable success rates for quantitative QAs, especially for questions related to width and height. This suggests that LLMs can accurately answer specific spatial questions using their extensive world knowledge. Additionally, our SpatialRGPT-7B variant demonstrates improved performance over the SpatialRGPT-7B$`_(rgb)`$ variant, especially in scenarios where relative depth information can be used to resolve ambiguities, such as distinguishing between behind/front, wide/thin, and estimating distances.

## Public Vision-language Benchmarks

#### General Benchmarks.

In this section, we evaluate whether integrating spatial VQA data and depth information affects performance on other VQA tasks. We compared our models with VILA-1.5-3B, which is trained on general VQA datasets. As shown in Table , our variants performed similarly to the baselines and slightly better on the VQA-v2 and MMVet datasets. These results align with findings from , indicating that VLMs generally underperform on spatial reasoning tasks but can improve with specific spatial VQA training without compromising general VQA performance.

#### Region & Spatial Benchmarks.

We follow the evaluation protocol from RegionGPT  and report object classification results using ground-truth boxes on the COCO-2017 validation set. As shown in Table , SpatialRGPT outperforms the baselines, demonstrating its strong region cognition capabilities. We further evaluate SpatialRGPT on BLINK ’s Relative Depth Benchmark. This benchmark is particularly challenging as it assesses point-level depths, while both the point-level region input and point-level questions were not specifically included in the training of SpatialRGPT. We use bounding boxes to mark the target points and evaluate the test set online with the EvalAI server. As shown in Table , SpatialRGPT significantly outperforms the state-of-the-art, achieving over 20% accuracy gain compared to GPT-4V-Turbo. Our model demonstrated strong performance, highlighting its ability to generalize to new tasks without explicit training.


![](../images/SpatialRGPT_md_images/figures/appendix/multi-hop-1.pdf.png) 
<figcaption> Examples of SpatialRGPT performing multi-hop reasoning.</figcaption>


## Real-world Applications

#### Complex Spatial Reasoning.

In this application, we aim to explore whether SpatialRGPT can function as a complex spatial reasoner on its own. Unlike the system mentioned in , which uses GPT-4 to handle reasoning tasks and employs VLM solely for answering basic spatial queries, SpatialRGPT directly integrates these capabilities. We provide examples in Figure , where we compare SpatialRGPT’s responses to those from GPT-4V using real-world samples. Our model demonstrates the ability to address complex spatial questions based on its own spatial knowledge. This suggests that SpatialRGPT has developed a robust representation of spatial learning and that this knowledge has effectively generalized to enhance its intrinsic language reasoning abilities.

#### Multi-hop Reasoning.

In Figure , we show examples of SpatialRGPT handling multi-hop reasoning. In the upper left sample, the model first identifies what’s to the right of Region $$
0
$$ (a single apple), finds the basket there, determines what’s inside the basket, and then provides spatial details about the object inside. Even though our training data doesn’t specifically include such multi-hop tasks, SpatialRGPT can still manage them effectively. This indicates that the model has developed a strong understanding of spatial relationships.

#### Region-aware Dense Reward Annotator.

Recently, has shown that VLMs can function as dense reward annotators for robotics tasks by specifying tasks in natural language and having the model annotate rewards for each frame in a trajectory. However, this approach can be constrained by the language’s ambiguity, especially when multiple identical objects are present or when targeting a small, specific region in a scene, which can be difficult to describe precisely with language alone. Given that SpatialRGPT is equipped with region-aware capabilities, we can directly specify the regions of interest. To study this application, we conducted a real robot experiment. Specifically, we defined two regions using bounding boxes (one for the fingertip and one for a green cube) and tasked SpatialRGPT to annotate rewards using the distance between the two regions. The results, shown in Figure , indicate that the estimated distance between the fingertip and its target cube decreased monotonically as the fingertip moved towards its goal. Also, our depth variant performs slightly better than the RGB variant. This demonstrates SpatialRGPT’s effectiveness as a region-aware dense reward annotator, offering a more precise and efficient alternative to language-only approaches.

# Discussion

#### Conclusion.

We introduce SpatialRGPT, a novel framework designed to enhance the spatial reasoning capabilities of Vision Language Models (VLMs). By integrating a region representation module and a flexible plugin for depth information, SpatialRGPT allows VLMs to effectively perceive spatial arrangement at both local and global scopes. Our data curation pipeline facilitates the learning of 3D spatial knowledge from scene graphs, while SpatialRGPT-Bench provides a comprehensive benchmark for evaluating spatial cognition across diverse environments. The results demonstrate significant improvements in spatial reasoning tasks while showcasing the model’s ability to reason complex spatial relations and perform as dense reward annotators for robotic applications.

#### Limitations.

One limitation of our work is the use of Axis-Aligned Bounding Boxes (AABBs), which can result in inaccuracies in label representation. A more accurate alternative is oriented bounding boxes (OBBs), but implementing them requires precise object pose estimation, which remains challenging due to the lack of open-world solutions. The most accurate approach would be human labeling , although this requires significant effort. We leave these for future work.

#### Acknowledgement.

This work was supported, in part, by the Qualcomm Innovation Fellowship.

# Ablation Study on Augmented SpatialRGPT-Bench

We conduct additional experiments by augmenting and rephrasing both questions and answers in SpatialRGPT-Bench using GPT-4. The results are shown in Table . The results show that SpatialRGPT consistently outperforms the baseline models, even when the questions and answers are different from the training data.

# Ablation Study on Metric-Scale Width and Height Data

We conduct an ablation study to see if adding width and height data affects other types of questions. As shown in Table , adding this data slightly improved the accuracy for questions about size (like big/small, tall/short, wide/thin) but slightly worsened the accuracy for questions about the distance between objects (horizontal and vertical). This suggests that information about object size helps with size-related questions but might make distance measurements less clear.

# Ablation Study on Bounding Box Types

We conduct an ablation study to examine the effect of using axis-aligned bounding boxes (AABB) versus PCA-based oriented bounding boxes (OBB). For this study, we use human-labeled OBBs from the Omni3D test set as the ground truth. We then compare the mean-square error of the width and height measurements for AABBs and PCA-based OBBs labeled by our 3D scene graph pipeline. The results are shown in Table . PCA-based OBB often lacks accuracy due to the incomplete and noisy nature of point clouds captured from a single view.

# Ablation Study on Different Input Modalities

As mentioned in Section , SpatialRGPT can take both boxes and masks as input during the inference phase. In this study, we aimed to test the impact of box and mask inputs on our SpatialRGPT-Bench. We presented the results in Table , where we observed a slight drop in performance when using boxes, but in general, the performance was very close. This suggests that the random modality strategy used during training is effective.

# Statistics and Samples of SpatialRGPT-Bench

Figure  presents key statistics from our SpatialRGPT-Bench, including counts for QA categories, data sources, and objects. We categorize the QA data into 12 distinct types, evenly divided between relative relationships and metric measurements. Notably, some datasets, such as SUNRGBD, emphasize close-object scenarios. To reduce bias, we source our data from a diverse range of datasets following . We also show six samples from our SpatialRGPT-Bench in Figure .


![](../images/SpatialRGPT_md_images/figures/appendix/bench_stats_combined.pdf.png)
<figcaption> SpatialRGPT-Bench statistics. Left: Category count and source count. Right: Object count.</figcaption>



![](../images/SpatialRGPT_md_images/figures/appendix/bench_samples.pdf.png)
<figcaption> Samples in SpatialRGPT-Bench.</figcaption>


# Implementation Details for Data Pipeline

In this section, we aim to provide a detailed implementation of our data annotation pipeline and intermediate results obtained through each component.

## Filtering.

Recent VLMs often benefit from the broad capabilities gained through training with large-scale 2D image datasets  . However, many images in these datasets are unsuitable for developing spatial reasoning QA. For instance, some images may be computer screenshots, paintings, collages, or simply a piece of text. Similar to SpatialVLM , we use a CLIP-based open-vocabulary classification model  to identify and exclude these unsuitable images. We follow the labeling used in SpatialVLM but have made a few adaptations to better suit the data distribution of the OpenImage  dataset. We show the labels we use in Listing . With this process, we filtered out 700K samples from the 1.7M OpenImage samples.

```
positive_labels = [
    "a DSLR photo of an indoor scene", 
    "a DSLR of an outdoor scene", 
    "an iphone photo of an indoor scene", 
    "an iphone photo of an outdoor scene", 
]

negative_labels = [
    "a close up shot of a single object", 
    "a product displayed in front of a white back ground",
    "a painting", 
    "a collage of images",
    "a screenshot of graphics user interface", 
    "a piece of text"
]

```

## Metric Depth Estimation

As stated in the main paper, we choose Metric3Dv2 as our metric depth estimator. We have observed that Metric3Dv2 and WildCamera’s camera intrinsic perform well on images taken in natural environments. In this section, we present the predicted normal maps from the depth model on OpenImages. These normal maps can be viewed as a proxy to estimate the quality of the reconstructed geometry’s edges.


![](../images/SpatialRGPT_md_images/figures/appendix/depth_normal.pdf.png)
<figcaption> Predicted normal maps using Metric3Dv2 and WildCamera.</figcaption>


## Point Cloud Processing

Here, we detailed how we process the point clouds into scene graphs.

#### Canonicalization.

Our canonicalization method is straightforward. After obtaining the pitch and roll through PerspectiveFields, we transform the point cloud into a canonicalized space using the inverse of the rotation matrix. Figure  illustrates the successful alignment of the ground surface with the z-axis angle after canonicalization. This process ensures that the axis-aligned bounding box accurately represents the vertical information of the objects, such as height and vertical distance. Our simple yet effective approach liberates our method from surface segmentation and RANSAC. We have empirically found this procedure robust for most natural images taken by cameras in real-world conditions.


![](../images/SpatialRGPT_md_images/figures/appendix/cano.pdf.png)
<figcaption> Canonicalization Results.</figcaption>


#### Denoising and constructing axis-aligned bounding box.

The point clouds obtained from single-view depth may contain noise. Following , we carry out several denoising steps based on the approach to filter out outliers and unwanted points, thereby improving the robustness and accuracy of the bounding box. Initially, we eliminate statistical outliers from the object points and then downsample the data to a lower resolution. Subsequently, we use DBSCAN to further remove noise. If the points of an object are fewer than ten after DBSCAN clustering, we exclude that object area. Finally, we employ Open3D to create axis-aligned bounding boxes for each object. The pseudocode for our denoising process is as in Listing .

```
def process_pcd(pcd):
    scale = norm(pcd).std * 3.0 + 1e-6
    [pcd, _] = pcd.remove_statistical_outlier(nb_neighbors=10, std_ratio=1.2)
    pcd = pcd.voxel_down_sample(voxel_size=max(0.01, scale/40))
    pcd = pcd_denoise_dbscan(
        pcd, eps=0.2, min_points=10 
    )
    return pcd
]
```

## Open Spatial Dataset QA Templates

We provide samples for each category of QA in the templates that we use to generate QAs mentioned in Section .

```
distance_template_questions = [
    "What is the distance between [A] and [B]?",
    "How far away is [A] from [B]?",
    "Can you provide the distance measurement between [A] and [B]?",
]
distance_template_answers = [
    "[A] and [B] are [X] apart.",
    "A distance of [X] exists between [A] and [B].",
    "[A] and [B] are [X] apart from each other.",
]
left_predicate_questions = [
    "Is [A] to the left of [B] from the viewer's perspective?",
    "Does [A] appear on the left side of [B]?",
    "Can you confirm if [A] is positioned to the left of [B]?",
]
left_true_responses = [
    "Yes, [A] is to the left of [B].",
    "Indeed, [A] is positioned on the left side of [B].",
    "Correct, you'll find [A] to the left of [B].",
]
left_false_responses = [
    "No, [A] is not to the left of [B].",
    "In fact, [A] is to the right of [B].",
    "Incorrect, [A] is not on the left side of [B].",
]
direction_questions = [
    "If you are at [A], where will you find [B]?"
]
direction_responses = [
    "[B] is roughly at [X] o'clock from [A].", 
    "[A] will find [B] around the [X] o'clock direction."
]
```

## LLM Prompts for Complex QA

# Implementation Details for SpatialRGPT Architecture

## Visual Backbone.

We adopt a pre-trained OpenAI CLIP-L model  as the visual backbone. We use 336$`\times`$<!-- -->336 image resolutions to include more visual details for the model, which can help with vision language tasks that require fine-grained details  and are beneficial for region-level representations .

## Region-feature Extractor.

We adopt the region feature extraction technique in . To begin with, we use a feature refinement module consisting of a 2-layer deconvolution network designed to upscale the original feature map. Then, we employ MaskPooling to extract and average the refined features from the masked area. Note that we also employ a separate feature refinement module for the depth feature. Similar to the projector, the weight for the depth feature refinement module is initialized from the RGB feature refinement module.

## Multi-modal Connector

To bridge representations from various modalities (e.g., image to language, depth to language), we employ a simple linear layer. Following the approach suggested in , using a straightforward connector helps the LLM to concentrate more on processing visual inputs, thereby enhancing generalization. We implement two separate connectors, one for image embeddings and another for depth embeddings, to ensure that each modality is handled distinctly. This separation prevents the mixing of modalities, which could otherwise compromise the effectiveness of the model.

# Implementation Details for Training SpatialRGPT

## Instruction Tuning Data

Here, we list the instruction tuning data we use in addition to the OSD dataset. Includes general instruction tuning datasets from LLAVA-1.5 , LAN-style instructions from VILA  (listed in Table ) and the region-level instruction tuning data from  (listed in Table ) that we use in stage three of the training.

## Hyperparameters

Please refer to VILA’s paper on the implementation of the hyperparameters used in the first two stages. For pre-training the depth connector, we use a maximum learning rate set at 1e-4, with a weight decay of 0 and a warm-up ratio of 0.03. The connector is trained with a batch size of 32 for one epoch. In the instruction fine-tuning stage, the maximum learning rate is reduced to 5e-5, and the batch size is adjusted to 16. All other hyperparameters remain the same as in the pre-training stage.

# Experimental Setting and Details

## Experiments Compute Resources

#### Open Spatial Dataset.

Our Open Spatial Dataset uses images from OpenImages, which contains a total of 1.7 million images. Our data preprocessing pipeline was tested on a system with 8 GPUs. The filtering process for 1.7 million images takes 4 hours and results in 1 million samples. The camera calibration and metric depth estimation each took around 4 hours. Note that the depth estimation requires our estimated camera intrinsics as input, so these two processes cannot be parallelized. The open-vocabulary detection and segmentation process takes 8 hours. As the process involves sequential operations, we did not specifically optimize it for parallelization. For LLM-based QA synthesis, we employ LLama3-70b using sglang backend, which takes 12 hours. In general, the total time required to convert OpenImages into 3D scene graphs is within a day, and constructing the QAs takes another half.

#### SpatialRGPT Training.

The first two stages of Spatial RGPT are inherited from VILA , which is trained on 16 A100 GPU nodes, with each node having 8 GPUs. The training times for each stage of the 7B model are as follows: connector initialization takes 4 hours, visual language pre-training takes 30 hours. The depth connector is further pre-trained using 2 A100 GPU nodes, taking 4 hours. The final visual instruction-tuning is also experimented on 2 A100 GPU nodes, taking 12 hours.

#### SpatialRGPT-Bench.

The SpatialRGPT-Bench dataset is created from ground truth 3D cuboids and human-annotated labels. Masks only need to be generated when bounding boxes are provided. We use SAM-HQ in our data pipeline to convert the bounding boxes into masks, which takes approximately 4 hours to process 10,000 samples. After this, we synthesize QA and randomly select 1,500 samples. Subsequently, we conduct human verification to filter out incorrect annotations, which takes a day to complete.

# Benchmark Evaluation Details

Our benchmark poses a challenge in evaluation due to the possibility of multiple correct answers in different units. Typically, human trials, like those used by , could handle this but are often too slow and costly, mainly as our benchmarks include over a thousand samples. As an alternative, we employ GPT-4  to assess correctness. The evaluation process involves providing a question, the correct answer, and the model’s response to the LLM. For qualitative questions, GPT-4 determines if the model’s response aligns with the correct answer by assigning a score of 0 or 1. For quantitative questions, GPT-4 extracts numerical values from both the correct answer and the model’s response, converting them to the same unit (such as meters). We then measure the accuracy and error of the model’s response based on this standardized unit. We provide prompts we use in Table  and Table .

# More Discussion on Limitations

For the most accurate object detection, oriented bounding boxes (OBB) are preferred over axis-aligned bounding boxes (AABB). As illustrated in Figure , the dimensions obtained from AABBs can differ from those obtained with OBBs. There are two methods to compute an OBB. A simple method involves calculating the OBB using Principal Component Analysis (PCA) of the object’s convex hull, which provides an approximate minimal bounding box. However, this approximation often lacks accuracy due to the incomplete and noisy nature of point clouds captured from a single view. Furthermore, this method still cannot handle extreme cases when objects are partially elevated (see Appdx ). The most precise method involves determining the OBB based on the object’s pose, which is currently challenging due to limitations in obtaining accurate object poses. Future improvements could include integrating available pose estimation approaches. However, currently, there are no open-vocabulary solutions for object pose estimation, so this remains an area for future research. Another direction, explored in subsequent work (e.g., Q-Spatial Bench ), addresses this limitation by leveraging human labeling.


![](../images/SpatialRGPT_md_images/figures/appendix/limitation_aabb.pdf.png)
<figcaption> Different types of bounding box.</figcaption>


# Broader Impacts

SpatialRGPT serves as a general-purpose visual assistant, similar to other VLMs. It offers potential benefits and risks due to its integration of LLMs. SpatialRGPT shares similar concerns with LLMs, such as output hallucinations, inherited biases from base models, and energy consumption during upscaling. Evaluating SpatialRGPT’s performance is also challenging, particularly in accurately measuring the spatial information. This is an area for future enhancement, especially in the field of robotics, which values safety. Despite these challenges, releasing SpatialRGPT to the research community would be beneficial, as it would foster further development and improvement of robotics applications.

# Licenses

1.  The training data we use, OpenImages , is released under `Apache License 2.0`.

2.  Our paper contain images from Unsplash , which is released under `Unsplash License`, allowing use of photos for free, including for commercial purposes, without attributing the photographer or Unsplash.
