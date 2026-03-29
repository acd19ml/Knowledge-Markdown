# Introduction

Large language models (LLMs) largely promote the development of artificial general intelligence (AGI) systems with their impressive capabilities in open-world language tasks, and their model scale and performance are still increasing at a fast pace. Vision large language models (VLLMs) , which leverage LLMs, have also achieved significant breakthroughs, enabling sophisticated vision-language dialogues and interactions. However, the progress of vision and vision-language foundation models, which are also crucial for VLLMs, has lagged behind the rapid growth of LLMs.

<img src="../images/InternVL_md_images/figure/sota.pdf.png" style="width:100.0%"  />
**Figure 2.** **Comparison results on various generic visual-linguistic tasks**, including image classification, video classification, image-text retrieval, image captioning, and multi-modal dialogue. The proposed InternVL achieves the best performance on all these tasks. Note that only the models trained on public data are included. “IN" is an abbreviation for ImageNet .

To bridge vision models with LLMs, existing VLLMs commonly employ lightweight “glue" layers, such as QFormer or linear projection , to align features of vision and language models. Such alignment contains several limitations: (1) *Disparity in parameter scales.* The large LLMs  now boosts up to 1000 billion parameters, while the widely-used vision encoders of VLLMs are still around one billion. This gap may lead to the under-use of LLM’s capacity. (2) *Inconsistent representation.* Vision models, trained on pure-vision data or aligned with the BERT series , often exhibit representation inconsistencies with LLMs. (3) *Inefficient connection.* The “glue” layers are usually lightweight and randomly initialized, which may not capture the rich cross-modal interactions and dependencies that are crucial for multi-modal understanding and generation.

These limitations reveal a large gap in both parameter scale and feature representation ability between the vision encoder and the LLM. To bridge this gap, *our inspiration lies in elevating the vision encoder to align with the parameter scale of the LLM and subsequently harmonizing their representations.* However, the training of such large-scale models necessitates a vast amount of image-text data obtained from the Internet. The significant heterogeneity and quality variations within this data pose considerable challenges to the training process. To enhance the efficacy of the training, generative supervision is considered as a complementary approach to contrastive learning, as depicted in Figure 1. This strategy aims to provide additional guidance to the model during training. Yet, the suitability of low-quality data for generative training remains a concern. Besides, how to effectively represent the users’ commands and align the representations between the vision encoder and LLM is another open question.

To address these issues, we formulate the *InternVL, a large-scale vision-language foundation model, which aligns the representation of the scaled-up vision encoder with the LLM and achieves state-of-the-art performance on various visual and vision-language tasks.* As shown in Figure 1 (c), InternVL has three key designs: (1) *Parameter-balanced vision and language components*: It includes a vision encoder scaled up to 6 billion parameters and an LLM middleware with 8 billion parameters, where the middleware functions as a substantial “glue” layer to reorganize visual features based on user commands. Unlike prior vision-only (Figure 1 (a)) or dual-tower (Figure 1 (b)) structures, our vision encoder and middleware offer flexible combinations for both contrastive and generative tasks. (2) *Consistent representations*: To maintain the consistency of representations between the vision encoder and LLM, we employ a pre-trained multilingual LLaMA , to initialize the middleware and align the vision encoder with it. (3) *Progressive image-text alignment*: We leverage image-text data from diverse sources, ensuring training stability through a progressive alignment strategy. This strategy initiates contrastive learning on large-scale noisy image-text data and subsequently transitions to generative learning on fine-grained data. This approach ensures a consistent enhancement of model performance and task scope.

These designs endow our model with several advantages: (1) *Versatile.* It functions as a standalone vision encoder for perception tasks, or collaborates with the language middleware for vision-language tasks and multi-modal dialogue systems. The language middleware bridges the gap between the vision encoder and the LLM decoder. (2) *Strong.* By leveraging the training strategy, large-scale parameters, and web-scale data, our model has a powerful representation that helps to achieve state-of-the-art results on various vision and vision-language tasks, as shown in Figure 1. (3) *LLM-friendly.* Due to the aligned feature space with LLMs, our model can smoothly integrate with existing LLMs, such as LLaMA series , Vicuna , and InternLM . These features distinguish our model from the previous approaches and establish a leading vision-language foundation model for various applications.

In summary, our contribution has three folds:

\(1\) We present a large-scale vision-language foundation model—InternVL, which aligns the large-scale vision encoder with LLMs for the first time. The model demonstrates strong performance on a wide range of generic visual-linguistic tasks, including visual perception tasks, vision-language tasks, and multi-modal dialogue.

\(2\) We introduce a progressive image-text alignment strategy for the efficient training of large-scale vision-language foundation models. This strategy maximizes the utilization of web-scale noisy image-text data for contrastive learning and fine-grained, high-quality data for generative learning.

\(3\) We extensively compare the proposed model with the current state-of-the-art vision foundation models and VLLMs. The results indicate that InternVL achieves leading performance on a broad range of generic visual-linguistic tasks, including image classification (ImageNet), semantic segmentation (ADE20K), video classification (Kinetics), image-text retrieval (Flickr30K & COCO), video-text retrieval (MSR-VTT), and image captioning (COCO & Flickr30K & NoCaps). Meanwhile, it is also effective for multi-modal dialogue (MME & POPE & Tiny LVLM).

# Related Work

<img src="../images/InternVL_md_images/figure/arch.pdf.png" style="width:90.0%"  />
**Figure 3.** **The training strategy of the proposed InternVL model.** It consists of three progressive stages, including vision-language contrastive training, vision-language generative training, and supervised fine-tuning. These stages effectively leverage public data from diverse sources, ranging from noisy image-text pairs on the web to high-quality caption, VQA, and multi-modal dialogue datasets.

## Vision Foundation Models

The past decade has witnessed significant development in foundation models within the field of computer vision. Starting with the pioneering AlexNet , a variety of convolutional neural networks (CNNs) have emerged, continuously refreshing the ImageNet benchmark . In particular, the introduction of residual connections  effectively addressed the problem of vanishing gradients. This breakthrough led to an era of “big & deep" neural networks, signifying that, with adequate training and data, larger and deeper models can achieve better performance. In other words, scaling up matters.

In recent years, ViT  has opened up new possibilities for network architectures in the computer vision field. ViT and its variants have significantly increased their capacity and excelled in various important visual tasks. In the LLM era, these vision foundation models often connect with LLMs through some lightweight “glue” layers . However, a gap exists as these models primarily derive from visual-only datasets like ImageNet or JFT , or are aligned with the BERT series using image-text pairs, lacking direct alignment with LLMs. Additionally, the prevalent vision models employed to connect with LLMs are still limited to around 1 billion parameters , which also constrains the performance of VLLMs.

## Large Language Models

Large language models (LLMs) have revolutionized the field of artificial intelligence, enabling natural language processing tasks that were previously thought exclusive to humans . The emergence of GPT-3  brought a significant leap in capabilities, particularly in few-shot and zero-shot learning, highlighting the immense potential of LLMs. This promise was further realized with the advancements of ChatGPT and GPT-4 . The progress in the field has been further accelerated by the emergence of open-source LLMs, including the LLaMA series , Vicuna , InternLM , MOSS , ChatGLM , Qwen , Baichuan , and Falcon , among others . However, in real scenarios, interactions are not limited to natural language. The vision modality can bring additional information, which means more possibilities. Therefore, exploring how to utilize the excellent capabilities of LLMs for multi-modal interactions is poised to become the next research trend.

## Vision Large Language Models

Recent advancements have seen the creation of vision large language models (VLLMs) , which aim to enhance language models with the capability to process and interpret visual information. Flamingo  uses the visual and language inputs as prompts and shows remarkable few-shot performance for visual question answering. Subsequently, GPT-4 , LLaVA series  and MiniGPT-4 have brought in visual instruction tuning, to improve the instruction-following ability of VLLMs. Concurrently, models such as VisionLLM , KOSMOS-2 , and Qwen-VL have improved VLLMs with visual grounding capabilities, facilitating tasks such as region description and localization. Many API-based methods  have also attempted to integrate vision APIs with LLMs for solving vision-centric tasks. Additionally, PaLM-E  and EmbodiedGPT  represent advanced efforts in adapting VLLMs for embodied applications, significantly expanding their potential applications. These works showcase that VLLMs have achieved significant breakthroughs. However, the progress of vision and vision-language foundation models, equally essential for VLLMs, has not kept pace.

# Proposed Method

## Overall Architecture

As depicted in Figure 2, unlike traditional vision-only backbones  and dual-encoder models , the proposed InternVL is designed with a vision encoder InternViT-6B and a language middleware QLLaMA. Specifically, InternViT-6B is a vision transformer with 6 billion parameters, customized to achieve a favorable trade-off between performance and efficiency. QLLaMA is a language middleware with 8 billion parameters, initialized with a multilingual-enhanced LLaMA . It could provide robust multilingual representation for image-text contrastive learning, or serve as a bridge to connect the vision encoder and the off-the-shelf LLM decoder.

To align the two large-scale components with substantial gaps in modalities and structures, we introduce a progressive alignment training strategy. The training strategy is conducted progressively, beginning with contrastive learning on large-scale noisy data, and gradually moving towards generative learning on exquisite and high-quality data. In this way, we ensure the effective organization and full utilization of web-scale image-text data from a variety of sources. Then, equipped with the aligned vision encoder and language middleware, our model functions like a Swiss Army knife. It boasts a flexible composition that can be adapted for a wide array of generic visual-linguistic tasks. These tasks range from visual perception and image/video-text retrieval to image captioning, visual question answering, and multi-modal dialogue, among others.

<div id="tab:model_config">

| name                | width | depth |  MLP  | \#heads | \#param (M) |
|:--------------------|:-----:|:-----:|:-----:|:-------:|:-----------:|
| ViT-G               | 1664  |  48   | 8192  |   16    |    1843     |
| ViT-e               | 1792  |  56   | 15360 |   16    |    3926     |
| EVA-02-ViT-E        | 1792  |  64   | 15360 |   16    |    4400     |
| ViT-6.5B            | 4096  |  32   | 16384 |   32    |    6440     |
| ViT-22B             | 6144  |  48   | 24576 |   48    |    21743    |
| InternViT-6B (ours) | 3200  |  48   | 12800 |   25    |    5903     |

**Architecture details of the InternViT-6B model.**
<img src="../images/InternVL_md_images/figure/internvl_c_g.pdf.png" style="width:100.0%"  />
**Figure 4.** **Different ways to use InternVL.** By flexibly combining the vision encoder and the language middleware, InternVL can support various vision-language tasks, including contrastive tasks, generative tasks, and multi-modal dialogue.

## Model Design

**Large-Scale Vision Encoder: InternViT-6B.** We implement the vision encoder of InternVL with vanilla vision transformer (ViT) . To match the scale of LLMs, we scale up the vision encoder to 6 billion parameters, resulting in the InternViT-6B model. To obtain a good trade-off between accuracy, speed, and stability, we conduct a hyperparameter search for InternViT-6B. We vary the model depth within {32, 48, 64, 80}, the head dimension within {64, 128}, and the MLP ratio within {4, 8}. The model width and the head number are calculated based on the given model scale and other hyperparameters.

We employ contrastive learning on a 100M subset of the LAION-en dataset to measure the accuracy, speed, and stability of InternViT-6B variants with different configurations. We report the following findings: (1) *Speed.* For different model settings, when computation is not saturated, the models with smaller depths exhibit faster speed per image. However, as the GPU computation is fully utilized, the speed difference becomes negligible; (2) *Accuracy.* With the same number of parameters, the depth, head dimension, and MLP ratio have little impact on the performance. Based on these findings, we identified the most stable configuration for our final model, as shown in Table 1.

**Language Middleware: QLLaMA.** The language middleware QLLaMA is proposed to align visual and linguistic features. As shown in Figure 2, QLLaMA is developed based on the pre-trained multilingual LLaMA , and newly added 96 learnable queries and cross-attention layers (1 billion parameters) that are randomly initialized. This manner allows QLLaMA to smoothly integrate visual elements into the language model, thereby enhancing the coherence and effectiveness of the combined features.

Compared to recently popular approaches  that use lightweight “glue” layers, such as QFormer  and linear layers  to connect vision encoder and LLMs, our method has three advantages: (1) By initializing with the pre-trained weights of , QLLaMA can transform image tokens generated by InternViT-6B into the representation that is aligned with the LLMs; (2) QLLaMA has 8 billion parameters for vision-language alignment, which are 42 times larger than the QFormer. Therefore, even with a frozen LLM decoder, InternVL can achieve promising performance on multi-modal dialogue tasks. (3) It can also be applied to contrastive learning, providing a powerful text representation for image-text alignment tasks, such as zero-shot image classification and image-text retrieval.

**“Swiss Army Knife” Model: InternVL.** By flexibly combining the vision encoder and the language middleware, InternVL can support various vision or vision-language tasks.

\(1\) *For visual perception tasks*, the vision encoder of InternVL, InternViT-6B, can be used as the backbone for vision tasks. Given an input image $`I\in\mathbb{R}^{H\times W\times 3}`$, our model can generate a feature map $`F\in \mathbb{R}^{H/14\times W/14\times D}`$ for dense prediction tasks, or work with global average pooling and linear projection to make image classification.

<div id="tab:stage1_data">


**Table 2.** **Details of the training data for InternVL in stage 1 and stage 2.** Among them, LAION-en , LAION-multi , COYO , and Wukong  are web-scale image-text pairs data. LAION-COCO  is a synthetic dataset with high-quality captions from LAION-en. CC12M , CC3M , SBU  are academic caption datasets. “Multi" means multilingual. 
<tbody>
<tr>
<td style="text-align: left;"></td>
<td colspan="2" style="text-align: center;">characteristics</td>
<td colspan="2" style="text-align: center;">stage 1</td>
<td colspan="2" style="text-align: center;">stage 2</td>
</tr>
<tr>
<td style="text-align: left;">dataset</td>
<td style="text-align: center;">language</td>
<td style="text-align: center;">original</td>
<td style="text-align: center;">cleaned</td>
<td style="text-align: center;">remain</td>
<td style="text-align: center;">cleaned</td>
<td style="text-align: center;">remain</td>
</tr>
<tr>
<td style="text-align: left;">LAION-en </td>
<td rowspan="6" style="text-align: center;">English</td>
<td style="text-align: center;">2.3B</td>
<td style="text-align: center;">1.94B</td>
<td style="text-align: center;">84.3%</td>
<td style="text-align: center;">91M</td>
<td style="text-align: center;">4.0%</td>
</tr>
<tr>
<td style="text-align: left;">LAION-COCO </td>
<td style="text-align: center;">663M</td>
<td style="text-align: center;">550M</td>
<td style="text-align: center;">83.0%</td>
<td style="text-align: center;">550M</td>
<td style="text-align: center;">83.0%</td>
</tr>
<tr>
<td style="text-align: left;">COYO </td>
<td style="text-align: center;">747M</td>
<td style="text-align: center;">535M</td>
<td style="text-align: center;">71.6%</td>
<td style="text-align: center;">200M</td>
<td style="text-align: center;">26.8%</td>
</tr>
<tr>
<td style="text-align: left;">CC12M </td>
<td style="text-align: center;">12.4M</td>
<td style="text-align: center;">11.1M</td>
<td style="text-align: center;">89.5%</td>
<td style="text-align: center;">11.1M</td>
<td style="text-align: center;">89.5%</td>
</tr>
<tr>
<td style="text-align: left;">CC3M </td>
<td style="text-align: center;">3.0M</td>
<td style="text-align: center;">2.6M</td>
<td style="text-align: center;">86.7%</td>
<td style="text-align: center;">2.6M</td>
<td style="text-align: center;">86.7%</td>
</tr>
<tr>
<td style="text-align: left;">SBU </td>
<td style="text-align: center;">1.0M</td>
<td style="text-align: center;">1.0M</td>
<td style="text-align: center;">100%</td>
<td style="text-align: center;">1.0M</td>
<td style="text-align: center;">100%</td>
</tr>
<tr>
<td style="text-align: left;">Wukong </td>
<td style="text-align: center;">Chinese</td>
<td style="text-align: center;">100M</td>
<td style="text-align: center;">69.4M</td>
<td style="text-align: center;">69.4%</td>
<td style="text-align: center;">69.4M</td>
<td style="text-align: center;">69.4%</td>
</tr>
<tr>
<td style="text-align: left;">LAION-multi </td>
<td style="text-align: center;">Multi</td>
<td style="text-align: center;">2.2B</td>
<td style="text-align: center;">1.87B</td>
<td style="text-align: center;">85.0%</td>
<td style="text-align: center;">100M</td>
<td style="text-align: center;">4.5%</td>
</tr>
<tr>
<td style="text-align: left;">Total</td>
<td style="text-align: center;">Multi</td>
<td style="text-align: center;">6.03B</td>
<td style="text-align: center;">4.98B</td>
<td style="text-align: center;">82.6%</td>
<td style="text-align: center;">1.03B</td>
<td style="text-align: center;">17.0%</td>
</tr>
</tbody>

\(2\) *For contrastive tasks*, as shown in Figure 3 (a) (b), we introduce two inference modes: **InternVL-C** and **InternVL-G**, using the vision encoder or the combination of InternViT and QLLaMA to encode visual features. Specifically, we apply attention pooling to the visual features of InternViT or the query features of QLLaMA, to calculate the global visual feature $`I_{f}`$. Besides, we encode text as $`T_{f}`$ by extracting the feature from the `[EOS]` token of QLLaMA. By computing similarity scores between $`I_{f}`$ and $`T_{f}`$, we support various contrastive tasks such as image-text retrieval.

\(3\) *For generative tasks*, unlike QFormer , QLLaMA inherently has promising image captioning abilities thanks to its scaled-up parameters. The queries of QLLaMA reorganize the visual representations from InternViT-6B and play as the prefix texts for QLLaMA. The subsequent text tokens are generated one by one sequentially.

\(4\) *For multi-modal dialogue*, we introduce **InternVL-Chat**, leveraging InternVL as the visual component to connect with LLMs. For this purpose, we have two distinct configurations. One option is to employ the InternViT-6B independently, as shown in Figure 3 (c). The alternative is to employ the complete InternVL model concurrently, as illustrated in Figure 3 (d).

<div id="tab:stage3_data">

| task          | \#samples | dataset                           |
|:--------------|:---------:|:----------------------------------|
| Captioning    |   588K    | COCO Caption , TextCaps           |
|               |           | VQAv2 , OKVQA , A-OKVQA ,         |
|               |   1.1M    | IconQA , AI2D , GQA               |
|               |           | OCR-VQA , ChartQA , DocVQA ,      |
|               |           | ST-VQA , EST-VQA , InfoVQA ,      |
| OCR           |   294K    | LLaVAR                            |
| Grounding     |   323K    | RefCOCO/+/g , Toloka              |
| Grounded Cap. |   284K    | RefCOCO/+/g                       |
|               |           | LLaVA-150K , SVIT , VisDial ,     |
|               |   1.4M    | LRV-Instruction , LLaVA-Mix-665K  |

**Details of the training data for InternVL in stage 3.** We collect a wide range of high-quality instruction data, totaling approximately 4 million samples. For a fair comparison, we only use the training split of these datasets.
## Alignment Strategy

As shown in Figure 2, the training of InternVL consists of three progressive stages, including vision-language contrastive training, vision-language generative training, and supervised fine-tuning. These stages effectively leverage public data from diverse sources, ranging from noisy image-text pairs on the web to high-quality caption, VQA, and multi-modal dialogue datasets.

**Vision-Language Contrastive Training.** In the first stage, we conduct contrastive learning to align InternViT-6B with a multilingual LLaMA-7B on web-scale, noisy image-text pairs. The data are all publicly available and comprise multilingual content, including LAION-en , LAION-multi , LAION-COCO , COYO , Wukong , etc. We use the combination of these datasets and filter out some extremely low-quality data to train our model. As summarized in Table 2, the original dataset contains 6.03 billion image-text pairs, and 4.98 billion remains after cleaning. More details about data preparation will be provided in the supplementary materials.

During training, we adopt the LLaMA-7B to encode the text as $`T_{f}`$, and use InternViT-6B to extract the visual feature $`I_{f}`$. Following the objective function of CLIP , we minimize a symmetric cross-entropy loss on the similarity scores of image-text pairs in a batch. This stage allows InternVL to excel on contrastive tasks like zero-shot image classification and image-text retrieval, and the vision encoder of this stage can also perform well on visual perception tasks like semantic segmentation.

**Vision-Language Generative Training**. In the second stage of training, we connect InternViT-6B with QLLaMA and adopt a generative training strategy. Specifically, QLLaMA inherits the weights of LLaMA-7B in the first stage. We keep both InternViT-6B and QLLaMA frozen and only train the newly added learnable queries and cross-attention layers with filtered, high-quality data. Table 2 summarizes the datasets for the second stage. It can be seen that we further filtered out data with low-quality captions, reducing it from 4.98 billion in the first stage to 1.03 billion.

Following the loss function of BLIP-2 , the loss in this stage is computed as the sum of three components: image-text contrastive (ITC) loss, image-text matching (ITM) loss, and image-grounded text generation (ITG) loss. This enables the queries to extract powerful visual representations, and further align feature space with LLMs, attributable to the effective training objectives and the utilization of our large-scale, LLM-initialized QLLaMA.

<div id="tab:img_cls">

| method | \#param | IN-1K | IN-ReaL | IN-V2 | IN-A | IN-R | IN-Ske | avg. |
|:---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| OpenCLIP-H  | 0.6B | 84.4 | 88.4 | 75.5 | $`-`$ | $`-`$ | $`-`$ | $`-`$ |
| OpenCLIP-G  | 1.8B | 86.2 | 89.4 | 77.2 | 63.8 | 87.8 | 66.4 | 78.5 |
| DINOv2-g  | 1.1B | 86.5 | 89.6 | 78.4 | 75.9 | 78.8 | 62.5 | 78.6 |
| EVA-01-CLIP-g  | 1.1B | 86.5 | 89.3 | 77.4 | 70.5 | 87.7 | 63.1 | 79.1 |
| MAWS-ViT-6.5B  | 6.5B | 87.8 | – | – | – | – | – | – |
| ViT-22B$`^*`$  | 21.7B | 89.5 | 90.9 | 83.2 | 83.8 | 87.4 | $`-`$ | $`-`$ |
| InternViT-6B (ours) | 5.9B | **88.2** | **90.4** | **79.9** | **77.5** | **89.8** | **69.1** | **82.5** |

**Linear evaluation on image classification.** We report the top-1 accuracy on ImageNet-1K and its variants . $`^*`$ViT-22B uses the private JFT-3B dataset .
<div class="subtable">

0.47

<div id="tab:sem_seg">

| method | \#param | crop size | $`1/16`$ | $`1/8`$ | $`1/4`$ | $`1/2`$ | $`1`$ |
|:---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| ViT-L  | 0.3B | 504$`^2`$ | 36.1 | 41.3 | 45.6 | 48.4 | 51.9 |
| ViT-G  | 1.8B | 504$`^2`$ | 42.4 | 47.0 | 50.2 | 52.4 | 55.6 |
| ViT-22B  | 21.7B | 504$`^2`$ | 44.7 | 47.2 | 50.6 | 52.5 | 54.9 |
| InternViT-6B (ours) | 5.9B | 504$`^2`$ | **46.5** | **50.0** | **53.3** | **55.8** | **57.2** |

**Semantic segmentation on ADE20K.** Results show that InternViT-6B has better pixel-level perceptual capacity.
<div class="subtable">

0.47

<div id="tab:sem_seg">

| method | decoder | \#param (train/total) | crop size | mIoU |  |
|:---|:--:|:--:|:--:|:--:|:--:|
| OpenCLIP-G<sub>frozen</sub>  | Linear | 0.3M / 1.8B | 512$`^2`$ | 39.3 |  |
| ViT-22B<sub>frozen</sub>  | Linear | 0.9M / 21.7B | 504$`^2`$ | 34.6 |  |
| InternViT-6B<sub>frozen</sub> (ours) | Linear | 0.5M / 5.9B | 504$`^2`$ | **47.2** |  |
| ViT-22B<sub>frozen</sub>  | UperNet | 0.8B / 22.5B | 504$`^2`$ | 52.7 |  |
| InternViT-6B<sub>frozen</sub> (ours) | UperNet | 0.4B / 6.3B | 504$`^2`$ | **54.9** |  |
| ViT-22B  | UperNet | 22.5B / 22.5B | 504$`^2`$ | 55.3 |  |
| InternViT-6B (ours) | UperNet | 6.3B / 6.3B | 504$`^2`$ | **58.9** |  |

**Semantic segmentation on ADE20K.** Results show that InternViT-6B has better pixel-level perceptual capacity.
**Supervised Fine-tuning.** To demonstrate the benefits of InternVL in creating multi-modal dialogue systems, we connect it with an off-the-shelf LLM decoder (, Vicuna  or InternLM ) through an MLP layer, and conduct supervised fine-tuning (SFT). As detailed in Table 3, we collect a wide range of high-quality instruction data, totaling approximately 4 million samples. For non-dialogue datasets, we follow the method described in for conversion. Owing to the similar feature space of QLLaMA and LLMs, we can achieve robust performance even when freezing the LLM decoder, choosing to train just the MLP layer or both the MLP layer and QLLaMA. This approach not only expedites the SFT process but also maintains the original language capabilities of the LLMs.
<div class="subtable">

0.53

| method | IN-1K | IN-A | IN-R | IN-V2 | IN-Sketch | ObjectNet | $`\Delta`$$`\downarrow`$ | avg. |
|:---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| OpenCLIP-H  | 78.0 | 59.3 | 89.3 | 70.9 | 66.6 | 69.7 | 5.7 | 72.3 |
| OpenCLIP-g  | 78.5 | 60.8 | 90.2 | 71.7 | 67.5 | 69.2 | 5.5 | 73.0 |
| OpenAI CLIP-L+  | 76.6 | 77.5 | 89.0 | 70.9 | 61.0 | 72.0 | 2.1 | 74.5 |
| EVA-01-CLIP-g  | 78.5 | 73.6 | 92.5 | 71.5 | 67.3 | 72.3 | 2.5 | 76.0 |
| OpenCLIP-G  | 80.1 | 69.3 | 92.1 | 73.6 | 68.9 | 73.0 | 3.9 | 76.2 |
| EVA-01-CLIP-g+  | 79.3 | 74.1 | 92.5 | 72.1 | 68.1 | 75.3 | 2.4 | 76.9 |
| MAWS-ViT-2B  | 81.9 | – | – | – | – | – | – | – |
| EVA-02-CLIP-E+  | 82.0 | 82.1 | 94.5 | 75.7 | 71.6 | 79.6 | 1.1 | 80.9 |
| CoCa$`^*`$  | 86.3 | 90.2 | 96.5 | 80.7 | 77.6 | 82.7 | 0.6 | 85.7 |
| LiT-22B$`^*`$  | 85.9 | 90.1 | 96.0 | 80.9 | $`-`$ | 87.6 | $`-`$ | $`-`$ |
| InternVL-C (ours) | **83.2** | **83.8** | **95.5** | **77.3** | **73.9** | **80.6** | **0.8** | **82.4** |
<div class="subtable">

0.42

| method               |    EN    |    ZH    |    JP    |    AR    |    IT    |   avg.   |
|:---------------------|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| M-CLIP               |  $`-`$   |  $`-`$   |  $`-`$   |  $`-`$   |   20.2   |  $`-`$   |
| CLIP-Italian         |  $`-`$   |  $`-`$   |  $`-`$   |  $`-`$   |   22.1   |  $`-`$   |
| Japanese-CLIP-ViT-B  |  $`-`$   |  $`-`$   |   54.6   |  $`-`$   |  $`-`$   |  $`-`$   |
| Taiyi-CLIP-ViT-H     |  $`-`$   |   54.4   |  $`-`$   |  $`-`$   |  $`-`$   |  $`-`$   |
| WuKong-ViT-L-G       |  $`-`$   |   57.5   |  $`-`$   |  $`-`$   |  $`-`$   |  $`-`$   |
| CN-CLIP-ViT-H        |  $`-`$   |   59.6   |  $`-`$   |  $`-`$   |  $`-`$   |  $`-`$   |
| AltCLIP-ViT-L        |   74.5   |   59.6   |  $`-`$   |  $`-`$   |  $`-`$   |  $`-`$   |
| EVA-02-CLIP-E+       |   82.0   |   3.6    |   5.0    |   0.2    |   41.2   |  $`-`$   |
| OpenCLIP-XLM-R-B     |   62.3   |   42.7   |   37.9   |   26.5   |   43.7   |   42.6   |
| OpenCLIP-XLM-R-H     |   77.0   |   55.7   |   53.1   |   37.0   |   56.8   |   55.9   |
| InternVL-C (ours)    | **83.2** | **64.5** | **61.5** | **44.9** | **65.7** | **64.0** |

<tbody>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: center;"></td>
<td colspan="6" style="text-align: center;">Flickr30K (English, 1K test set) </td>
<td colspan="6" style="text-align: center;">COCO (English, 5K test set) </td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: center;">multi-</td>
<td colspan="3" style="text-align: center;">Image → Text</td>
<td colspan="3" style="text-align: center;">Text → Image</td>
<td colspan="3" style="text-align: center;">Image → Text</td>
<td colspan="3" style="text-align: center;">Text → Image</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">method</td>
<td style="text-align: center;">lingual</td>
<td style="text-align: center;">R@1</td>
<td style="text-align: center;">R@5</td>
<td style="text-align: center;">R@10</td>
<td style="text-align: center;">R@1</td>
<td style="text-align: center;">R@5</td>
<td style="text-align: center;">R@10</td>
<td style="text-align: center;">R@1</td>
<td style="text-align: center;">R@5</td>
<td style="text-align: center;">R@10</td>
<td style="text-align: center;">R@1</td>
<td style="text-align: center;">R@5</td>
<td style="text-align: center;">R@10</td>
<td style="text-align: center;">avg.</td>
</tr>
<tr>
<td style="text-align: left;">Florence </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">90.9</td>
<td style="text-align: center;">99.1</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">76.7</td>
<td style="text-align: center;">93.6</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">64.7</td>
<td style="text-align: center;">85.9</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">47.2</td>
<td style="text-align: center;">71.4</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
</tr>
<tr>
<td style="text-align: left;">ONE-PEACE </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">90.9</td>
<td style="text-align: center;">98.8</td>
<td style="text-align: center;">99.8</td>
<td style="text-align: center;">77.2</td>
<td style="text-align: center;">93.5</td>
<td style="text-align: center;">96.2</td>
<td style="text-align: center;">64.7</td>
<td style="text-align: center;">86.0</td>
<td style="text-align: center;">91.9</td>
<td style="text-align: center;">48.0</td>
<td style="text-align: center;">71.5</td>
<td style="text-align: center;">79.6</td>
<td style="text-align: center;">83.2</td>
</tr>
<tr>
<td style="text-align: left;">OpenCLIP-H </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">90.8</td>
<td style="text-align: center;">99.3</td>
<td style="text-align: center;">99.7</td>
<td style="text-align: center;">77.8</td>
<td style="text-align: center;">94.1</td>
<td style="text-align: center;">96.6</td>
<td style="text-align: center;">66.0</td>
<td style="text-align: center;">86.1</td>
<td style="text-align: center;">91.9</td>
<td style="text-align: center;">49.5</td>
<td style="text-align: center;">73.4</td>
<td style="text-align: center;">81.5</td>
<td style="text-align: center;">83.9</td>
</tr>
<tr>
<td style="text-align: left;">OpenCLIP-g </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">91.4</td>
<td style="text-align: center;">99.2</td>
<td style="text-align: center;">99.6</td>
<td style="text-align: center;">77.7</td>
<td style="text-align: center;">94.1</td>
<td style="text-align: center;">96.9</td>
<td style="text-align: center;">66.4</td>
<td style="text-align: center;">86.0</td>
<td style="text-align: center;">91.8</td>
<td style="text-align: center;">48.8</td>
<td style="text-align: center;">73.3</td>
<td style="text-align: center;">81.5</td>
<td style="text-align: center;">83.9</td>
</tr>
<tr>
<td style="text-align: left;">OpenCLIP-XLM-R-H </td>
<td style="text-align: center;">✓</td>
<td style="text-align: center;">91.8</td>
<td style="text-align: center;">99.4</td>
<td style="text-align: center;">99.8</td>
<td style="text-align: center;">77.8</td>
<td style="text-align: center;">94.1</td>
<td style="text-align: center;">96.5</td>
<td style="text-align: center;">65.9</td>
<td style="text-align: center;">86.2</td>
<td style="text-align: center;">92.2</td>
<td style="text-align: center;">49.3</td>
<td style="text-align: center;">73.2</td>
<td style="text-align: center;">81.5</td>
<td style="text-align: center;">84.0</td>
</tr>
<tr>
<td style="text-align: left;">EVA-01-CLIP-g+ </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">91.6</td>
<td style="text-align: center;">99.3</td>
<td style="text-align: center;">99.8</td>
<td style="text-align: center;">78.9</td>
<td style="text-align: center;">94.5</td>
<td style="text-align: center;">96.9</td>
<td style="text-align: center;">68.2</td>
<td style="text-align: center;">87.5</td>
<td style="text-align: center;">92.5</td>
<td style="text-align: center;">50.3</td>
<td style="text-align: center;">74.0</td>
<td style="text-align: center;">82.1</td>
<td style="text-align: center;">84.6</td>
</tr>
<tr>
<td style="text-align: left;">CoCa </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">92.5</td>
<td style="text-align: center;">99.5</td>
<td style="text-align: center;">99.9</td>
<td style="text-align: center;">80.4</td>
<td style="text-align: center;">95.7</td>
<td style="text-align: center;">97.7</td>
<td style="text-align: center;">66.3</td>
<td style="text-align: center;">86.2</td>
<td style="text-align: center;">91.8</td>
<td style="text-align: center;">51.2</td>
<td style="text-align: center;">74.2</td>
<td style="text-align: center;">82.0</td>
<td style="text-align: center;">84.8</td>
</tr>
<tr>
<td style="text-align: left;">OpenCLIP-G </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">92.9</td>
<td style="text-align: center;">99.3</td>
<td style="text-align: center;">99.8</td>
<td style="text-align: center;">79.5</td>
<td style="text-align: center;">95.0</td>
<td style="text-align: center;">97.1</td>
<td style="text-align: center;">67.3</td>
<td style="text-align: center;">86.9</td>
<td style="text-align: center;">92.6</td>
<td style="text-align: center;">51.4</td>
<td style="text-align: center;">74.9</td>
<td style="text-align: center;">83.0</td>
<td style="text-align: center;">85.0</td>
</tr>
<tr>
<td style="text-align: left;">EVA-02-CLIP-E+ </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">93.9</td>
<td style="text-align: center;">99.4</td>
<td style="text-align: center;">99.8</td>
<td style="text-align: center;">78.8</td>
<td style="text-align: center;">94.2</td>
<td style="text-align: center;">96.8</td>
<td style="text-align: center;">68.8</td>
<td style="text-align: center;">87.8</td>
<td style="text-align: center;">92.8</td>
<td style="text-align: center;">51.1</td>
<td style="text-align: center;">75.0</td>
<td style="text-align: center;">82.7</td>
<td style="text-align: center;">85.1</td>
</tr>
<tr>
<td style="text-align: left;">BLIP-2<sup>†</sup> </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">97.6</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">89.7</td>
<td style="text-align: center;">98.1</td>
<td style="text-align: center;">98.9</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C (ours)</td>
<td style="text-align: center;">✓</td>
<td style="text-align: center;">94.7</td>
<td style="text-align: center;">99.6</td>
<td style="text-align: center;">99.9</td>
<td style="text-align: center;">81.7</td>
<td style="text-align: center;">96.0</td>
<td style="text-align: center;">98.2</td>
<td style="text-align: center;">70.6</td>
<td style="text-align: center;">89.0</td>
<td style="text-align: center;">93.5</td>
<td style="text-align: center;">54.1</td>
<td style="text-align: center;">77.3</td>
<td style="text-align: center;">84.6</td>
<td style="text-align: center;">86.6</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G (ours)</td>
<td style="text-align: center;">✓</td>
<td style="text-align: center;">**95.7**</td>
<td style="text-align: center;">**99.7**</td>
<td style="text-align: center;">**99.9**</td>
<td style="text-align: center;">**85.0**</td>
<td style="text-align: center;">**97.0**</td>
<td style="text-align: center;">**98.6**</td>
<td style="text-align: center;">**74.9**</td>
<td style="text-align: center;">**91.3**</td>
<td style="text-align: center;">**95.2**</td>
<td style="text-align: center;">**58.6**</td>
<td style="text-align: center;">**81.3**</td>
<td style="text-align: center;">**88.0**</td>
<td style="text-align: center;">**88.8**</td>
</tr>
<tr>
<td colspan="15" style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">method</td>
<td style="text-align: center;"></td>
<td colspan="6" style="text-align: center;">Flickr30K-CN (Chinese, 1K test set) </td>
<td colspan="6" style="text-align: center;">COCO-CN (Chinese, 1K test set) </td>
<td style="text-align: center;">avg.</td>
</tr>
<tr>
<td style="text-align: left;">WuKong-ViT-L </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">76.1</td>
<td style="text-align: center;">94.8</td>
<td style="text-align: center;">97.5</td>
<td style="text-align: center;">51.7</td>
<td style="text-align: center;">78.9</td>
<td style="text-align: center;">86.3</td>
<td style="text-align: center;">55.2</td>
<td style="text-align: center;">81.0</td>
<td style="text-align: center;">90.6</td>
<td style="text-align: center;">53.4</td>
<td style="text-align: center;">80.2</td>
<td style="text-align: center;">90.1</td>
<td style="text-align: center;">78.0</td>
</tr>
<tr>
<td style="text-align: left;">R2D2-ViT-L </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">77.6</td>
<td style="text-align: center;">96.7</td>
<td style="text-align: center;">98.9</td>
<td style="text-align: center;">60.9</td>
<td style="text-align: center;">86.8</td>
<td style="text-align: center;">92.7</td>
<td style="text-align: center;">63.3</td>
<td style="text-align: center;">89.3</td>
<td style="text-align: center;">95.7</td>
<td style="text-align: center;">56.4</td>
<td style="text-align: center;">85.0</td>
<td style="text-align: center;">93.1</td>
<td style="text-align: center;">83.0</td>
</tr>
<tr>
<td style="text-align: left;">Taiyi-CLIP-ViT-H </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">60.0</td>
<td style="text-align: center;">84.0</td>
<td style="text-align: center;">93.3</td>
<td style="text-align: center;">−</td>
</tr>
<tr>
<td style="text-align: left;">AltCLIP-ViT-H </td>
<td style="text-align: center;">✓</td>
<td style="text-align: center;">88.9</td>
<td style="text-align: center;">98.5</td>
<td style="text-align: center;">99.5</td>
<td style="text-align: center;">74.5</td>
<td style="text-align: center;">92.0</td>
<td style="text-align: center;">95.5</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
</tr>
<tr>
<td style="text-align: left;">CN-CLIP-ViT-H </td>
<td style="text-align: center;">×</td>
<td style="text-align: center;">81.6</td>
<td style="text-align: center;">97.5</td>
<td style="text-align: center;">98.8</td>
<td style="text-align: center;">71.2</td>
<td style="text-align: center;">91.4</td>
<td style="text-align: center;">95.5</td>
<td style="text-align: center;">63.0</td>
<td style="text-align: center;">86.6</td>
<td style="text-align: center;">92.9</td>
<td style="text-align: center;">69.2</td>
<td style="text-align: center;">89.9</td>
<td style="text-align: center;">96.1</td>
<td style="text-align: center;">86.1</td>
</tr>
<tr>
<td style="text-align: left;">OpenCLIP-XLM-R-H </td>
<td style="text-align: center;">✓</td>
<td style="text-align: center;">86.1</td>
<td style="text-align: center;">97.5</td>
<td style="text-align: center;">99.2</td>
<td style="text-align: center;">71.0</td>
<td style="text-align: center;">90.5</td>
<td style="text-align: center;">94.9</td>
<td style="text-align: center;">70.0</td>
<td style="text-align: center;">91.5</td>
<td style="text-align: center;">97.0</td>
<td style="text-align: center;">66.1</td>
<td style="text-align: center;">90.8</td>
<td style="text-align: center;">96.0</td>
<td style="text-align: center;">87.6</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C (ours)</td>
<td style="text-align: center;">✓</td>
<td style="text-align: center;">90.3</td>
<td style="text-align: center;">98.8</td>
<td style="text-align: center;">99.7</td>
<td style="text-align: center;">75.1</td>
<td style="text-align: center;">92.9</td>
<td style="text-align: center;">96.4</td>
<td style="text-align: center;">68.8</td>
<td style="text-align: center;">92.0</td>
<td style="text-align: center;">96.7</td>
<td style="text-align: center;">68.9</td>
<td style="text-align: center;">91.9</td>
<td style="text-align: center;">96.5</td>
<td style="text-align: center;">89.0</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G (ours)</td>
<td style="text-align: center;">✓</td>
<td style="text-align: center;">**92.9**</td>
<td style="text-align: center;">**99.4**</td>
<td style="text-align: center;">**99.8**</td>
<td style="text-align: center;">**77.7**</td>
<td style="text-align: center;">**94.8**</td>
<td style="text-align: center;">**97.3**</td>
<td style="text-align: center;">**71.4**</td>
<td style="text-align: center;">**93.9**</td>
<td style="text-align: center;">**97.7**</td>
<td style="text-align: center;">**73.8**</td>
<td style="text-align: center;">**94.4**</td>
<td style="text-align: center;">**98.1**</td>
<td style="text-align: center;">**90.9**</td>
</tr>
</tbody>

# Experiments

## Implementation Details

**Stage 1.** In this stage, the image encoder InternViT-6B is randomly initialized , and the text encoder LLaMA-7B is initialized with the pre-trained weights from . All parameters are fully trainable.

**Stage 2.** In this stage, InternViT-6B and QLLaMA inherit their weights from the first stage, while the new learnable queries and cross-attention layers in QLLaMA are randomly initialized. Benefiting from the powerful representations learned in the first stage, we keep both InternViT-6B and QLLaMA frozen and only train the new parameters.

**Stage 3.** At this stage, we have two different configurations. One is to use InternViT-6B separately, as shown in Figure 3 (c). The other is to use the entire InternVL model simultaneously, as shown in Figure 3 (d). More details will be provided in the supplementary materials.

## Visual Perception Benchmarks

First of all, we validate the visual perception capabilities of InternViT-6B, the most core component of InternVL.

**Transfer to Image Classification.** We evaluate the quality of visual representation produced by InternViT-6B using the ImageNet-1K dataset. Following common practices , we adopt the linear probing evaluation, training a linear classifier while keeping the backbone frozen. In addition to the ImageNet-1K validation set, we also report performance metrics on several ImageNet variants , to benchmark the domain generalization capability. As shown in Table 4, InternViT-6B achieves a very significant improvement over previous state-of-the-art methods on linear probing. To our knowledge, this represents the currently best linear evaluation results without the JFT dataset .

**Transfer to Semantic Segmentation.** To investigate the pixel-level perceptual capacity of InternViT-6B, we conduct extensive experiments of semantic segmentation on the ADE20K  dataset. Following ViT-22B , we begin with few-shot learning experiments, fine-tuning the backbone with a linear head on a limited dataset. As indicated in Table 5, InternViT-6B consistently outperforms ViT-22B across five experiments with varying proportions of training data. Additionally, Table 5 presents our further verification in three distinct settings, including linear probing, head tuning , and full-parameter tuning. Notably, in the case of linear probing, InternViT-6B attains 47.2 mIoU, a substantial +12.6 mIoU improvement over ViT-22B. These results underscore the strong out-of-the-box pixel-level perceptual capacity of our InternViT-6B.

<div id="tab: zs_video">


**Table 8.**  **Comparison of zero-shot video classification results on Kinetics 400/600/700.** We report the top-1 accuracy and the mean of top-1 and top-5 accuracy. “#F" denotes the number of frames. 
<tbody>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: center;"></td>
<td colspan="2" style="text-align: center;">K400 </td>
<td colspan="2" style="text-align: center;">K600 </td>
<td colspan="2" style="text-align: center;">K700 </td>
</tr>
<tr>
<td style="text-align: left;">method</td>
<td style="text-align: center;">#F</td>
<td style="text-align: center;">top-1</td>
<td style="text-align: center;">avg.</td>
<td style="text-align: center;">top-1</td>
<td style="text-align: center;">avg.</td>
<td style="text-align: center;">top-1</td>
<td style="text-align: center;">avg.</td>
</tr>
<tr>
<td style="text-align: left;">OpenCLIP-g </td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">63.9</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">64.1</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">56.9</td>
</tr>
<tr>
<td style="text-align: left;">OpenCLIP-G </td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">65.9</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">66.1</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">59.2</td>
</tr>
<tr>
<td style="text-align: left;">EVA-01-CLIP-g+ </td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">66.7</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">67.0</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">60.9</td>
</tr>
<tr>
<td style="text-align: left;">EVA-02-CLIP-E+ </td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">69.8</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">69.3</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">63.4</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C (ours)</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">**65.9**</td>
<td style="text-align: center;">**76.1**</td>
<td style="text-align: center;">**65.5**</td>
<td style="text-align: center;">**75.5**</td>
<td style="text-align: center;">**56.8**</td>
<td style="text-align: center;">**67.5**</td>
</tr>
<tr>
<td style="text-align: left;">ViCLIP </td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">64.8</td>
<td style="text-align: center;">75.7</td>
<td style="text-align: center;">62.2</td>
<td style="text-align: center;">73.5</td>
<td style="text-align: center;">54.3</td>
<td style="text-align: center;">66.4</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C (ours)</td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">**69.1**</td>
<td style="text-align: center;">**79.4**</td>
<td style="text-align: center;">**68.9**</td>
<td style="text-align: center;">**78.8**</td>
<td style="text-align: center;">**60.6**</td>
<td style="text-align: center;">**71.5**</td>
</tr>
</tbody>


<tbody>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">visual</td>
<td style="text-align: left;">glue</td>
<td style="text-align: left;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">train.</td>
<td colspan="3" style="text-align: center;">image captioning</td>
<td colspan="4" style="text-align: center;">visual question answering</td>
<td colspan="2" style="text-align: center;">dialogue</td>
</tr>
<tr>
<td style="text-align: left;">method</td>
<td style="text-align: left;">encoder</td>
<td style="text-align: left;">layer</td>
<td style="text-align: left;">LLM</td>
<td style="text-align: center;">Res.</td>
<td style="text-align: center;">PT</td>
<td style="text-align: center;">SFT</td>
<td style="text-align: center;">param</td>
<td style="text-align: center;">COCO</td>
<td style="text-align: center;">Flickr</td>
<td style="text-align: center;">NoCaps</td>
<td style="text-align: center;">VQA<sup>v2</sup></td>
<td style="text-align: center;">GQA</td>
<td style="text-align: center;">VizWiz</td>
<td style="text-align: center;">VQA<sup>T</sup></td>
<td style="text-align: center;">MME</td>
<td style="text-align: center;">POPE</td>
</tr>
<tr>
<td style="text-align: left;">InstructBLIP </td>
<td style="text-align: left;">EVA-g</td>
<td style="text-align: left;">QFormer</td>
<td style="text-align: left;">Vicuna-7B</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">129M</td>
<td style="text-align: center;">1.2M</td>
<td style="text-align: center;">188M</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">82.4</td>
<td style="text-align: center;">123.1</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">49.2</td>
<td style="text-align: center;">34.5</td>
<td style="text-align: center;">50.1</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
</tr>
<tr>
<td style="text-align: left;">BLIP-2 </td>
<td style="text-align: left;">EVA-g</td>
<td style="text-align: left;">QFormer</td>
<td style="text-align: left;">Vicuna-13B</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">129M</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">188M</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">71.6</td>
<td style="text-align: center;">103.9</td>
<td style="text-align: center;">41.0</td>
<td style="text-align: center;">41.0</td>
<td style="text-align: center;">19.6</td>
<td style="text-align: center;">42.5</td>
<td style="text-align: center;">1293.8</td>
<td style="text-align: center;">85.3</td>
</tr>
<tr>
<td style="text-align: left;">InstructBLIP </td>
<td style="text-align: left;">EVA-g</td>
<td style="text-align: left;">QFormer</td>
<td style="text-align: left;">Vicuna-13B</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">129M</td>
<td style="text-align: center;">1.2M</td>
<td style="text-align: center;">188M</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">82.8</td>
<td style="text-align: center;">121.9</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">49.5</td>
<td style="text-align: center;">33.4</td>
<td style="text-align: center;">50.7</td>
<td style="text-align: center;">1212.8</td>
<td style="text-align: center;">78.9</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-Chat (ours)</td>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">QLLaMA</td>
<td style="text-align: left;">Vicuna-7B</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">1.0B</td>
<td style="text-align: center;">4.0M</td>
<td style="text-align: center;">64M</td>
<td style="text-align: center;"> 141.4<sup>*</sup></td>
<td style="text-align: center;">89.7</td>
<td style="text-align: center;">120.5</td>
<td style="text-align: center;"> 72.3<sup>*</sup></td>
<td style="text-align: center;"> 57.7<sup>*</sup></td>
<td style="text-align: center;">44.5</td>
<td style="text-align: center;">42.1</td>
<td style="text-align: center;">1298.5</td>
<td style="text-align: center;">85.2</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-Chat (ours)</td>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">QLLaMA</td>
<td style="text-align: left;">Vicuna-13B</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">1.0B</td>
<td style="text-align: center;">4.0M</td>
<td style="text-align: center;">90M</td>
<td style="text-align: center;"> 142.4<sup>*</sup></td>
<td style="text-align: center;">89.9</td>
<td style="text-align: center;">123.1</td>
<td style="text-align: center;"> 71.7<sup>*</sup></td>
<td style="text-align: center;"> 59.5<sup>*</sup></td>
<td style="text-align: center;">54.0</td>
<td style="text-align: center;">49.1</td>
<td style="text-align: center;">1317.2</td>
<td style="text-align: center;">85.4</td>
</tr>
<tr>
<td style="text-align: left;">Shikra </td>
<td style="text-align: left;">CLIP-L</td>
<td style="text-align: left;">Linear</td>
<td style="text-align: left;">Vicuna-13B</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">600K</td>
<td style="text-align: center;">5.5M</td>
<td style="text-align: center;">7B</td>
<td style="text-align: center;"> 117.5<sup>*</sup></td>
<td style="text-align: center;">73.9</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;"> 77.4<sup>*</sup></td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
</tr>
<tr>
<td style="text-align: left;">IDEFICS-80B </td>
<td style="text-align: left;">CLIP-H</td>
<td style="text-align: left;">Cross-Attn</td>
<td style="text-align: left;">LLaMA-65B</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">1.6B</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">15B</td>
<td style="text-align: center;"> 91.8<sup>*</sup></td>
<td style="text-align: center;">53.7</td>
<td style="text-align: center;">65.0</td>
<td style="text-align: center;">60.0</td>
<td style="text-align: center;">45.2</td>
<td style="text-align: center;">36.0</td>
<td style="text-align: center;">30.9</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
</tr>
<tr>
<td style="text-align: left;">IDEFICS-80B-I </td>
<td style="text-align: left;">CLIP-H</td>
<td style="text-align: left;">Cross-Attn</td>
<td style="text-align: left;">LLaMA-65B</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">353M</td>
<td style="text-align: center;">6.7M</td>
<td style="text-align: center;">15B</td>
<td style="text-align: center;"> 117.2<sup>*</sup></td>
<td style="text-align: center;">65.3</td>
<td style="text-align: center;">104.5</td>
<td style="text-align: center;">37.4</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">26.0</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
</tr>
<tr>
<td style="text-align: left;">Qwen-VL </td>
<td style="text-align: left;">CLIP-G</td>
<td style="text-align: left;">VL-Adapter</td>
<td style="text-align: left;">Qwen-7B</td>
<td style="text-align: center;">448</td>
<td style="text-align: center;">1.4B<sup>†</sup></td>
<td style="text-align: center;">50M<sup>†</sup></td>
<td style="text-align: center;">9.6B</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">85.8</td>
<td style="text-align: center;">121.4</td>
<td style="text-align: center;"> 78.8<sup>*</sup></td>
<td style="text-align: center;"> 59.3<sup>*</sup></td>
<td style="text-align: center;">35.2</td>
<td style="text-align: center;">63.8</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
</tr>
<tr>
<td style="text-align: left;">Qwen-VL-Chat </td>
<td style="text-align: left;">CLIP-G</td>
<td style="text-align: left;">VL-Adapter</td>
<td style="text-align: left;">Qwen-7B</td>
<td style="text-align: center;">448</td>
<td style="text-align: center;">1.4B<sup>†</sup></td>
<td style="text-align: center;">50M<sup>†</sup></td>
<td style="text-align: center;">9.6B</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">81.0</td>
<td style="text-align: center;">120.2</td>
<td style="text-align: center;"> 78.2<sup>*</sup></td>
<td style="text-align: center;"> 57.5<sup>*</sup></td>
<td style="text-align: center;">38.9</td>
<td style="text-align: center;">**61.5**</td>
<td style="text-align: center;">1487.5</td>
<td style="text-align: center;">–</td>
</tr>
<tr>
<td style="text-align: left;">LLaVA-1.5 </td>
<td style="text-align: left;">CLIP-L<sub>336</sub></td>
<td style="text-align: left;">MLP</td>
<td style="text-align: left;">Vicuna-7B</td>
<td style="text-align: center;">336</td>
<td style="text-align: center;">558K</td>
<td style="text-align: center;">665K</td>
<td style="text-align: center;">7B</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;"> 78.5<sup>*</sup></td>
<td style="text-align: center;"> 62.0<sup>*</sup></td>
<td style="text-align: center;">50.0</td>
<td style="text-align: center;">58.2</td>
<td style="text-align: center;">1510.7</td>
<td style="text-align: center;">85.9</td>
</tr>
<tr>
<td style="text-align: left;">LLaVA-1.5 </td>
<td style="text-align: left;">CLIP-L<sub>336</sub></td>
<td style="text-align: left;">MLP</td>
<td style="text-align: left;">Vicuna-13B</td>
<td style="text-align: center;">336</td>
<td style="text-align: center;">558K</td>
<td style="text-align: center;">665K</td>
<td style="text-align: center;">13B</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;"> 80.0<sup>*</sup></td>
<td style="text-align: center;"> 63.3<sup>*</sup></td>
<td style="text-align: center;">53.6</td>
<td style="text-align: center;">61.3</td>
<td style="text-align: center;">1531.3</td>
<td style="text-align: center;">85.9</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-Chat (ours)</td>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">MLP</td>
<td style="text-align: left;">Vicuna-7B</td>
<td style="text-align: center;">336</td>
<td style="text-align: center;">558K</td>
<td style="text-align: center;">665K</td>
<td style="text-align: center;">7B</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;"> 79.3<sup>*</sup></td>
<td style="text-align: center;"> 62.9<sup>*</sup></td>
<td style="text-align: center;">52.5</td>
<td style="text-align: center;">57.0</td>
<td style="text-align: center;">1525.1</td>
<td style="text-align: center;">86.4</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-Chat (ours)</td>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">MLP</td>
<td style="text-align: left;">Vicuna-13B</td>
<td style="text-align: center;">336</td>
<td style="text-align: center;">558K</td>
<td style="text-align: center;">665K</td>
<td style="text-align: center;">13B</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;"> 80.2<sup>*</sup></td>
<td style="text-align: center;"> 63.9<sup>*</sup></td>
<td style="text-align: center;">54.6</td>
<td style="text-align: center;">58.7</td>
<td style="text-align: center;">1546.9</td>
<td style="text-align: center;">87.1</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-Chat (ours)</td>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">QLLaMA</td>
<td style="text-align: left;">Vicuna-13B</td>
<td style="text-align: center;">336</td>
<td style="text-align: center;">1.0B</td>
<td style="text-align: center;">4.0M</td>
<td style="text-align: center;">13B</td>
<td style="text-align: center;"> **146.2**<sup>*</sup></td>
<td style="text-align: center;">**92.2**</td>
<td style="text-align: center;">**126.2**</td>
<td style="text-align: center;"> **81.2**<sup>*</sup></td>
<td style="text-align: center;"> **66.6**<sup>*</sup></td>
<td style="text-align: center;">**58.5**</td>
<td style="text-align: center;">**61.5**</td>
<td style="text-align: center;">**1586.4**</td>
<td style="text-align: center;">**87.6**</td>
</tr>
</tbody>

<div id="tab: zs_cap">

| method            | glue layer | LLM decoder    |   COCO    | Flickr30K |  NoCaps   |
|:------------------|:-----------|:---------------|:---------:|:---------:|:---------:|
| Flamingo-9B       | Cross-Attn | Chinchilla-7B  |   79.4    |   61.5    |     –     |
| Flamingo-80B      | Cross-Attn | Chinchilla-70B |   84.3    |   67.2    |     –     |
| KOSMOS-2          | Linear     | KOSMOS-1       |     –     |   66.7    |     –     |
| PaLI-X-55B        | Linear     | UL2-32B        |     –     |     –     | **126.3** |
| BLIP-2            | QFormer    | Vicuna-13B     |     –     |   71.6    |   103.9   |
| InstructBLIP      | QFormer    | Vicuna-13B     |     –     |   82.8    |   121.9   |
| Shikra-13B        | Linear     | Vicuna-13B     |     –     |   73.9    |     –     |
| ASM               | QFormer    | Husky-7B       |     –     | **87.7**  |   117.2   |
| Qwen-VL           | VL-Adapter | Qwen-7B        |     –     |   85.8    |   121.4   |
| Qwen-VL-Chat      | VL-Adapter | Qwen-7B        |     –     |   81.0    |   120.2   |
| Emu               | QFormer    | LLaMA-13B      |   112.4   |     –     |     –     |
| Emu-I             | QFormer    | LLaMA-13B      |   117.7   |     –     |     –     |
| DreamLLM          | Linear     | Vicuna-7B      |   115.4   |     –     |     –     |
| InternVL-G (ours) | Cross-Attn | QLLaMA         | **128.2** |   79.2    |   113.7   |

**Comparison of zero-shot image captioning.** QLLaMA inherently possesses promising zero-shot captioning capabilities thanks to its scaled-up parameters and datasets.
## Vision-Language Benchmarks

In this section, we evaluate the inherent capabilities of InternVL on various vision-language tasks.

**Zero-Shot Image Classification.** We conduct thorough validation of the zero-shot image classification capability of InternVL-C. As depicted in Table 6, InternVL-C attains leading performance on various ImageNet variants  and ObjectNet . Compared to EVA-02-CLIP-E+ , it exhibits stronger robustness to distribution shift, manifesting in a more consistent accuracy across ImageNet variants. Additionally, as shown in Table 6, our model showcases robust multilingual capabilities, outperforming competing models  on the multilingual ImageNet-1K benchmark.

**Zero-Shot Video Classification.** Following previous methods , we report the top-1 accuracy and the mean of top-1 and top-5 accuracy on Kinetics-400/600/700 . As shown in Table 7, when sampling only a single center frame in each video, our method achieves an average accuracy of 76.1%, 75.5%, and 67.5% on the three datasets, surpassing EVA-02-CLIP-E+  by +6.3, +6.2, and +4.1 points, respectively. Additionally, when uniformly sampling 8 frames in each video, we obtain at least 3.3 points of improvement compared to the single-frame setting, outperforming ViCLIP  trained using web-scale video data. In summary, InternVL-C exhibits remarkable generalization capabilities in video classification.

**Zero-Shot Image-Text Retrieval.** InternVL exhibits a powerful multilingual image-text retrieval capability. In Table 7, we evaluate these capabilities in English using the Flickr30K  and COCO  datasets, as well as in Chinese using the Flickr30K-CN  and COCO-CN . Additionally, we leverage the XTD dataset to evaluate the multilingual image-text retrieval capability across 8 languages (see supplementary materials). In summary, InternVL-C achieves state-of-the-art performance across most retrieval metrics, and with the second stage of pre-training, InternVL-G further enhances zero-shot image-text retrieval performance. These improvements in retrieval tasks suggest a more effective alignment between visual and linguistic features, through additional image encoding using the language middleware–QLLaMA.

**Zero-Shot Image Captioning.** Benefiting from vision-language generative training on a vast collection of high-quality image-text pairs, our QLLaMA possesses promising capability in zero-shot image captioning. As shown in Table 8, QLLaMA surpasses other models in zero-shot performance on the COCO Karpathy test set . It also achieves comparable results to current state-of-the-art models on both the Flickr30K Karpathy test  and the NoCaps val set . When InternVL is linked with an LLM (, Vicuna-7B/13B ) and subjected to SFT, a notable enhancement in zero-shot performance is observed for both Flickr30K and NoCaps, as shown in Table 9.

## Multi-Modal Dialogue Benchmarks

Beyond the traditional multi-modal tasks, the emergence of ChatGPT  has led to a growing focus on evaluating the performance of multi-modal models in real usage scenarios, specifically within the realm of multi-modal dialogue. We conducted testing of InternVL-Chat models on two prominent multi-modal dialogue benchmarks, including MME  and POPE . MME is a comprehensive benchmark that includes 14 sub-tasks focusing on the model’s perception and cognition capabilities. POPE is a popular dataset used to evaluate object hallucination. As shown in Table 9, it clearly demonstrates that our models exhibit superior performance compared with previous methods, under the condition of fair trainable parameter counts.

## Ablation Study

**Hyperparameters of InternViT-6B.** As discussed in Section <a href="#sec:model_design" data-reference-type="ref" data-reference="sec:model_design">3.2</a>, we explored variations in model depth {32, 48, 64, 80}, head dimension {64, 128}, and MLP ratio {4, 8}, resulting in 16 distinct models. In selecting the optimal model, we initially narrowed down our focus to 6 models, chosen based on their throughput, as listed in Table 9. These models underwent further evaluation using contrastive learning on a 100M subset of LAION-en  over 10K iterations. For the experimental setup, the primary difference was the use of a randomly initialized text encoder from CLIP-L , in order to speed up the training. For the sake of accuracy, inference speed, and training stability, we ultimately chose variant 3 as the final InternViT-6B.

<div id="tab:ablation_model_config">

| name      | width | depth |  MLP  | \#heads | \#param | FLOPs | throughput  | zs IN |
|:----------|:-----:|:-----:|:-----:|:-------:|:-------:|:-----:|:-----------:|:-----:|
| variant 1 | 3968  |  32   | 15872 |   62    |  6051M  | 1571G | 35.5 / 66.0 | 65.8  |
| variant 2 | 3200  |  48   | 12800 |   50    |  5903M  | 1536G | 28.1 / 64.9 | 66.1  |
| variant 3 | 3200  |  48   | 12800 |   25    |  5903M  | 1536G | 28.0 / 64.6 | 66.2  |
| variant 4 | 2496  |  48   | 19968 |   39    |  5985M  | 1553G | 28.3 / 65.3 | 65.9  |
| variant 5 | 2816  |  64   | 11264 |   44    |  6095M  | 1589G | 21.6 / 61.4 | 66.2  |
| variant 6 | 2496  |  80   | 9984  |   39    |  5985M  | 1564G | 16.9 / 60.1 | 66.2  |

**Comparison of hyperparameters in InternViT-6B.** The throughput (img/s) and GFLOPs are measured at 224$`\times`$<!-- -->224 input resolution, with a batch size of 1 or 128 on a single A100 GPU. Flash Attention and bf16 precision are used during testing. “zs IN" denotes the zero-shot top-1 accuracy on the ImageNet-1K validation set . The final selected model is marked in gray.
<div id="tab:ablation_component">


**Table 12.**  **Ablation studies of using InternVL to build multi-modal dialogue system.** V-7B and V-13B denote Vicuna-7B/13B , respectively. “IViT-6B” represents our InternViT-6B. 
<tbody>
<tr>
<td style="text-align: left;">visual</td>
<td style="text-align: left;">glue</td>
<td rowspan="2" style="text-align: left;">LLM</td>
<td rowspan="2" style="text-align: center;">dataset</td>
<td style="text-align: center;">dialogue</td>
<td style="text-align: center;">caption</td>
<td colspan="3" style="text-align: center;">visual question answering</td>
</tr>
<tr>
<td style="text-align: left;">encoder</td>
<td style="text-align: left;">layer</td>
<td style="text-align: center;">MME</td>
<td style="text-align: center;">NoCaps</td>
<td style="text-align: center;">OKVQA</td>
<td style="text-align: center;">VizWiz$\rm_{val}$</td>
<td style="text-align: center;">GQA</td>
</tr>
<tr>
<td style="text-align: left;">EVA-E</td>
<td style="text-align: left;">MLP</td>
<td style="text-align: left;">V-7B</td>
<td style="text-align: center;">665K </td>
<td style="text-align: center;">970.5</td>
<td style="text-align: center;">75.1</td>
<td style="text-align: center;">40.1</td>
<td style="text-align: center;">25.5</td>
<td style="text-align: center;">41.3</td>
</tr>
<tr>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">MLP</td>
<td style="text-align: left;">V-7B</td>
<td style="text-align: center;">665K </td>
<td style="text-align: center;">1022.3</td>
<td style="text-align: center;">80.8</td>
<td style="text-align: center;">42.9</td>
<td style="text-align: center;">28.3</td>
<td style="text-align: center;">45.8</td>
</tr>
<tr>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">QLLaMA</td>
<td style="text-align: left;">V-7B</td>
<td style="text-align: center;">665K </td>
<td style="text-align: center;">1227.5</td>
<td style="text-align: center;">94.5</td>
<td style="text-align: center;">51.0</td>
<td style="text-align: center;">38.4</td>
<td style="text-align: center;">57.4</td>
</tr>
<tr>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">QLLaMA</td>
<td style="text-align: left;">V-7B</td>
<td style="text-align: center;">Ours</td>
<td style="text-align: center;">1298.5</td>
<td style="text-align: center;">120.5</td>
<td style="text-align: center;">51.8</td>
<td style="text-align: center;">44.9</td>
<td style="text-align: center;">57.7</td>
</tr>
<tr>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">QLLaMA</td>
<td style="text-align: left;">V-13B</td>
<td style="text-align: center;">Ours</td>
<td style="text-align: center;">1317.2</td>
<td style="text-align: center;">123.1</td>
<td style="text-align: center;">55.5</td>
<td style="text-align: center;">55.7</td>
<td style="text-align: center;">59.5</td>
</tr>
</tbody>

**Consistency of Feature Representation.** In this study, we validate the consistency of the feature representation of InternVL with off-the-shelf LLMs. We adopt a minimalist setting, conducting a single-stage SFT using only the LLaVA-Mix-665K  dataset. Moreover, only the MLP layers are trainable, thereby confirming the inherent alignment level among features from various vision foundation models and LLMs. The results are shown in Table 10. We observed that compared to EVA-E , our InternViT-6B achieves better performance under this simple setup. Additionally, it is noteworthy that performance across all three tasks saw significant improvement when using QLLaMA as the “glue layer". These significant improvements clearly delineate that *the feature representation of InternVL is more consistent with the off-the-shelf LLM.*

# Conclusion

In this paper, we present InternVL, a large-scale vision-language foundation model that scales up the vision foundation model to 6 billion parameters and is aligned for generic visual-linguistic tasks. Specifically, we design a large-scale vision foundation model InternViT-6B, progressively align it with an LLM-initialized language middleware QLLaMA, and leverage web-scale image-text data from various sources for efficient training. It bridges the gap between vision foundation models and LLMs, and demonstrates proficiency in a wide range of generic visual-linguistic tasks, such as image/video classification, image/video-text retrieval, image captioning, visual question answering, and multi-modal dialogue. We hope this work could contribute to the development of the VLLM community.

# Acknowledgement

We thank Shenglong Zhang, Beitong Zhou, Xinyue Zhang, Dongxing Shi, Weigao Sun, Xingcheng Zhang, and Zhifeng Yue for their contributions to the optimization of the training framework. We thank Zhenhang Huang for his assistance in data preparation.

# Supplementary Materials

## More Experiments

**Zero-Shot Image Classification on 20 Datasets.** In this section, we expand our examination to showcase the effectiveness and robustness of InternVL in 20 different zero-shot image classification benchmarks. As indicated in Table 16, InternVL registers an average performance of 78.1% across all 20 benchmarks. This performance notably exceeds that of the previously leading method, EVA-02-CLIP-E+ , by a margin of 1.0 points. This underscores that, beyond ImageNet  and its variants, InternVL possesses robust generalization capabilities across a variety of different domains in zero-shot image classification.

**Zero-Shot Image-Text Retrieval on XTD.** Table 11 reports the results of InternVL on the multilingual image-text retrieval dataset XTD , spanning eight languages. As can be seen, InternVL-C achieves an average recall@10 score of 95.1% across these languages. The second stage model, InternVL-G, further improves retrieval performance. It attains the highest scores in each individual language and establishes a new record for average performance at 96.6%.

**Zero-Shot Video Retrieval.** In Table 12, we present our results of zero-shot video-text retrieval on the MSR-VTT dataset  using our InternVL models, InternVL-C and InternVL-G. In the 1-frame setting, we select a single central frame from each video. In the 8-frame setting, we uniformly extract 8 frames from each video, treat them as independent images for encoding, and then average the embeddings. The results showcase consistent improvement across various metrics such as R@1, R@5, R@10, and the average score. Importantly, both models exhibit promising outcomes in single-frame and multi-frame configurations, with InternVL-G achieving slightly higher performance than InternVL-C, especially in the multi-frame setting. These results underscore the effectiveness of QLLaMA in harmonizing visual and linguistic features.

**Fine-tuned Image-Text Retrieval.** In Table 13, we report the fine-tuned image-text retrieval results of InternVL, on both the English and Chinese versions of the Flickr30K dataset . The specific hyperparameters for fine-tuning are shown in Table 18. As can be seen, our models obtain competitive performance, with InternVL-G-FT marginally surpassing InternVL-C-FT in both datasets. Notably, in the highly challenging Flickr30K-CN, both models show a promising ability to handle cross-lingual retrieval tasks. These results demonstrate the effectiveness of our language middleware, especially in the retrieval tasks.

**Tiny LVLM.** Tiny LVLM is an ability-level benchmark for evaluating the performance of multimodal dialogue models. It provides a systematic assessment of five categories of multimodal capabilities, including visual perception, visual knowledge acquisition, visual reasoning, visual commonsense, and object hallucination. We report our results on Tiny LVLM in Table 14.

## More Ablation Studies

<div id="tab: zs_xtd">

| method | EN | ES | FR | ZH | IT | KO | RU | JP | avg. |
|:---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| mUSE m3  | 85.3 | 78.9 | 78.9 | 76.7 | 73.6 | 67.8 | 76.1 | 70.7 | 76.0 |
| M-CLIP  | 92.4 | 91.0 | 90.0 | 89.7 | 91.1 | 85.2 | 85.8 | 81.9 | 88.4 |
| MURAL  | $`-`$ | 92.9 | $`-`$ | 89.7 | 91.8 | 88.1 | 87.2 | $`-`$ | $`-`$ |
| AltCLIP  | 95.4 | 94.1 | 92.9 | 95.1 | 94.2 | 94.4 | 91.8 | 91.7 | 93.7 |
| OpenCLIP-XLM-R-B  | 95.8 | 94.4 | 92.5 | 91.8 | 94.4 | 86.3 | 89.9 | 90.7 | 92.0 |
| OpenCLIP-XLM-R-H  | 97.3 | 96.1 | 94.5 | 94.7 | 96.0 | 90.2 | 93.9 | 94.0 | 94.6 |
| InternVL-C (ours) | 97.3 | 95.7 | 95.1 | 95.6 | 96.0 | 92.2 | 93.3 | 95.5 | 95.1 |
| InternVL-G (ours) | **98.6** | **97.7** | **96.5** | **96.7** | **96.9** | **95.1** | **94.8** | **96.1** | **96.6** |

**Comparison of zero-shot multilingual image-text retrieval performance on the XTD dataset.** Multiple languages include English (EN), Spanish (ES), French (FR), Chinese (ZH), Italian (IT), Korean (KO), Russian (RU), and Japanese (JP). We follow M-CLIP  to report the recall@10 on Image-to-Text.
<div id="tab: video zs retrieval">


**Table 14.** **Comparison of zero-shot video-text retrieval performance on MSR-VTT.** “#F" denotes the number of frames. <sup>†</sup> These models are trained with temporal attention layers. 
<tbody>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: center;"></td>
<td colspan="6" style="text-align: center;">MSR-VTT (1K test set) </td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: center;"></td>
<td colspan="3" style="text-align: center;">Video → Text</td>
<td colspan="3" style="text-align: center;">Text → Video</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">method</td>
<td style="text-align: center;">#F</td>
<td style="text-align: center;">R@1</td>
<td style="text-align: center;">R@5</td>
<td style="text-align: center;">R@10</td>
<td style="text-align: center;">R@1</td>
<td style="text-align: center;">R@5</td>
<td style="text-align: center;">R@10</td>
<td style="text-align: center;">avg.</td>
</tr>
<tr>
<td style="text-align: left;">OpenAI CLIP-L </td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">27.8</td>
<td style="text-align: center;">49.4</td>
<td style="text-align: center;">58.0</td>
<td style="text-align: center;">29.0</td>
<td style="text-align: center;">50.5</td>
<td style="text-align: center;">59.2</td>
<td style="text-align: center;">45.7</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C (ours)</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">35.3</td>
<td style="text-align: center;">56.6</td>
<td style="text-align: center;">66.6</td>
<td style="text-align: center;">37.5</td>
<td style="text-align: center;">60.9</td>
<td style="text-align: center;">**70.9**</td>
<td style="text-align: center;">54.6</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G (ours)</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">**36.6**</td>
<td style="text-align: center;">**58.3**</td>
<td style="text-align: center;">**67.7**</td>
<td style="text-align: center;">**39.1**</td>
<td style="text-align: center;">**61.7**</td>
<td style="text-align: center;">70.7</td>
<td style="text-align: center;">**55.7**</td>
</tr>
<tr>
<td style="text-align: left;">OpenAI CLIP-L </td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">26.6</td>
<td style="text-align: center;">50.8</td>
<td style="text-align: center;">61.8</td>
<td style="text-align: center;">30.7</td>
<td style="text-align: center;">54.4</td>
<td style="text-align: center;">64.0</td>
<td style="text-align: center;">48.1</td>
</tr>
<tr>
<td style="text-align: left;">Florence </td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">37.6</td>
<td style="text-align: center;">63.8</td>
<td style="text-align: center;">72.6</td>
<td style="text-align: center;">–</td>
</tr>
<tr>
<td style="text-align: left;">InternVideo<sup>†</sup> </td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">39.6</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">40.7</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">–</td>
</tr>
<tr>
<td style="text-align: left;">UMT-L<sup>†</sup> </td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">38.6</td>
<td style="text-align: center;">59.8</td>
<td style="text-align: center;">69.6</td>
<td style="text-align: center;">42.6</td>
<td style="text-align: center;">64.4</td>
<td style="text-align: center;">73.1</td>
<td style="text-align: center;">58.0</td>
</tr>
<tr>
<td style="text-align: left;">LanguageBind<sup>†</sup> </td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">40.9</td>
<td style="text-align: center;">66.4</td>
<td style="text-align: center;">75.7</td>
<td style="text-align: center;">44.8</td>
<td style="text-align: center;">70.0</td>
<td style="text-align: center;">78.7</td>
<td style="text-align: center;">62.8</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C (ours)</td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">40.2</td>
<td style="text-align: center;">63.1</td>
<td style="text-align: center;">74.1</td>
<td style="text-align: center;">44.7</td>
<td style="text-align: center;">68.2</td>
<td style="text-align: center;">78.4</td>
<td style="text-align: center;">61.5</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G (ours)</td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">**42.4**</td>
<td style="text-align: center;">**65.9**</td>
<td style="text-align: center;">**75.4**</td>
<td style="text-align: center;">**46.3**</td>
<td style="text-align: center;">**70.5**</td>
<td style="text-align: center;">**79.6**</td>
<td style="text-align: center;">**63.4**</td>
</tr>
</tbody>

<div class="subtable">

1

<div id="tab: finetune retrieval">


**Table 15.** **Comparison of fine-tuned image-text retrieval performance.** We evaluate English and Chinese image-text retrieval using Flickr30K  and Flickr30K-CN , with separate fine-tuning for each to prevent data leakage. 
<tbody>
<tr>
<td style="text-align: left;"></td>
<td colspan="6" style="text-align: center;">Flickr30K (English, 1K test set) </td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td colspan="3" style="text-align: center;">Image → Text</td>
<td colspan="3" style="text-align: center;">Text → Image</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">method</td>
<td style="text-align: center;">R@1</td>
<td style="text-align: center;">R@5</td>
<td style="text-align: center;">R@10</td>
<td style="text-align: center;">R@1</td>
<td style="text-align: center;">R@5</td>
<td style="text-align: center;">R@10</td>
<td style="text-align: center;">avg.</td>
</tr>
<tr>
<td style="text-align: left;">ALIGN </td>
<td style="text-align: center;">95.3</td>
<td style="text-align: center;">99.8</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">84.9</td>
<td style="text-align: center;">97.4</td>
<td style="text-align: center;">98.6</td>
<td style="text-align: center;">96.0</td>
</tr>
<tr>
<td style="text-align: left;">FILIP </td>
<td style="text-align: center;">96.6</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">87.1</td>
<td style="text-align: center;">97.7</td>
<td style="text-align: center;">99.1</td>
<td style="text-align: center;">96.8</td>
</tr>
<tr>
<td style="text-align: left;">Florence </td>
<td style="text-align: center;">97.2</td>
<td style="text-align: center;">99.9</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">87.9</td>
<td style="text-align: center;">98.1</td>
<td style="text-align: center;">−</td>
<td style="text-align: center;">−</td>
</tr>
<tr>
<td style="text-align: left;">BLIP </td>
<td style="text-align: center;">97.4</td>
<td style="text-align: center;">99.8</td>
<td style="text-align: center;">99.9</td>
<td style="text-align: center;">87.6</td>
<td style="text-align: center;">97.7</td>
<td style="text-align: center;">99.0</td>
<td style="text-align: center;">96.9</td>
</tr>
<tr>
<td style="text-align: left;">OmniVL </td>
<td style="text-align: center;">97.3</td>
<td style="text-align: center;">99.9</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">87.9</td>
<td style="text-align: center;">97.8</td>
<td style="text-align: center;">99.1</td>
<td style="text-align: center;">97.0</td>
</tr>
<tr>
<td style="text-align: left;">BEiT-3 </td>
<td style="text-align: center;">97.5</td>
<td style="text-align: center;">99.9</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">89.1</td>
<td style="text-align: center;">98.6</td>
<td style="text-align: center;">**99.3**</td>
<td style="text-align: center;">97.4</td>
</tr>
<tr>
<td style="text-align: left;">ONE-PEACE </td>
<td style="text-align: center;">97.6</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">89.6</td>
<td style="text-align: center;">98.0</td>
<td style="text-align: center;">99.1</td>
<td style="text-align: center;">97.4</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C-FT (ours)</td>
<td style="text-align: center;">97.2</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">88.5</td>
<td style="text-align: center;">98.4</td>
<td style="text-align: center;">99.2</td>
<td style="text-align: center;">97.2</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G-FT (ours)</td>
<td style="text-align: center;">**97.9**</td>
<td style="text-align: center;">**100.0**</td>
<td style="text-align: center;">**100.0**</td>
<td style="text-align: center;">**89.6**</td>
<td style="text-align: center;">**98.6**</td>
<td style="text-align: center;">99.2</td>
<td style="text-align: center;">**97.6**</td>
</tr>
<tr>
<td colspan="7" style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">method</td>
<td colspan="6" style="text-align: center;">Flickr30K-CN (Chinese, 1K test set) </td>
<td style="text-align: center;">avg.</td>
</tr>
<tr>
<td style="text-align: left;">Wukong-ViT-L </td>
<td style="text-align: center;">92.7</td>
<td style="text-align: center;">99.1</td>
<td style="text-align: center;">99.6</td>
<td style="text-align: center;">77.4</td>
<td style="text-align: center;">94.5</td>
<td style="text-align: center;">97.0</td>
<td style="text-align: center;">93.4</td>
</tr>
<tr>
<td style="text-align: left;">CN-CLIP-ViT-H </td>
<td style="text-align: center;">95.3</td>
<td style="text-align: center;">99.7</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">83.8</td>
<td style="text-align: center;">96.9</td>
<td style="text-align: center;">98.6</td>
<td style="text-align: center;">95.7</td>
</tr>
<tr>
<td style="text-align: left;">R2D2-ViT-L </td>
<td style="text-align: center;">95.6</td>
<td style="text-align: center;">99.8</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">84.4</td>
<td style="text-align: center;">96.7</td>
<td style="text-align: center;">98.4</td>
<td style="text-align: center;">95.8</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C-FT (ours)</td>
<td style="text-align: center;">96.5</td>
<td style="text-align: center;">99.9</td>
<td style="text-align: center;">100.0</td>
<td style="text-align: center;">85.2</td>
<td style="text-align: center;">97.0</td>
<td style="text-align: center;">98.5</td>
<td style="text-align: center;">96.2</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G-FT (ours)</td>
<td style="text-align: center;">**96.9**</td>
<td style="text-align: center;">**99.9**</td>
<td style="text-align: center;">**100.0**</td>
<td style="text-align: center;">**85.9**</td>
<td style="text-align: center;">**97.1**</td>
<td style="text-align: center;">**98.7**</td>
<td style="text-align: center;">**96.4**</td>
</tr>
</tbody>

| method |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|:---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| OpenAI CLIP-L+  | 94.9 | 74.4 | 79.0 | 87.2 | 68.7 | 33.4 | 34.5 | 79.3 | 41.0 | 56.0 | 61.5 | 49.1 | 78.6 | 93.9 | 52.4 | 93.8 | 70.7 | 65.4 | 99.4 | 78.1 | 69.6 |
| EVA-01-CLIP-g  | 98.3 | 88.7 | 62.3 | 87.7 | 74.2 | 32.4 | 28.6 | 91.7 | 50.0 | 61.3 | 73.6 | 52.2 | 74.5 | 93.5 | 49.1 | 94.2 | 58.4 | 70.3 | 98.9 | 83.2 | 71.2 |
| OpenCLIP-g  | 98.2 | 84.7 | 71.9 | 88.1 | 74.1 | 44.6 | 30.9 | 94.0 | 51.0 | 68.7 | 64.7 | 55.8 | 81.0 | 92.4 | 49.7 | 93.9 | 56.7 | 69.6 | 98.9 | 81.6 | 72.5 |
| OpenCLIP-H  | 97.4 | 84.7 | 72.9 | 85.0 | 75.2 | 42.8 | 30.0 | 93.5 | 52.9 | 67.8 | 72.7 | 52.0 | 80.1 | 92.7 | 58.4 | 94.5 | 64.3 | 70.5 | 98.5 | 77.7 | 73.2 |
| EVA-02-CLIP-L+  | 98.9 | 89.8 | 64.3 | 89.5 | 74.8 | 37.5 | 33.6 | 91.6 | 45.8 | 64.5 | 71.4 | 51.0 | 77.2 | 94.2 | 57.6 | 94.2 | 64.6 | 69.8 | **99.7** | 82.7 | 72.6 |
| EVA-01-CLIP-g+  | 99.1 | 90.1 | 71.8 | 88.1 | 74.3 | 39.4 | 30.8 | 90.7 | 52.6 | 67.3 | 73.2 | 56.0 | 79.7 | 93.7 | 66.5 | 94.8 | 58.6 | 71.4 | 99.5 | 82.9 | 74.0 |
| OpenCLIP-G  | 98.2 | 87.5 | 71.6 | 86.4 | 74.5 | 49.7 | 33.8 | 94.5 | 54.5 | 69.0 | 70.0 | **59.5** | 81.5 | 93.1 | 62.5 | 95.2 | 65.2 | 72.6 | 98.5 | 80.7 | 74.9 |
| EVA-02-CLIP-E  | 99.3 | 92.5 | 76.7 | 89.0 | **76.5** | 47.9 | 34.7 | 94.4 | 56.3 | 68.2 | 77.6 | 55.1 | 82.5 | 95.2 | 67.1 | 95.6 | 61.1 | 73.5 | 99.2 | 83.0 | 76.3 |
| EVA-02-CLIP-E+  | 99.3 | 93.1 | 74.7 | **90.5** | 75.1 | **54.1** | **35.7** | **94.6** | 58.1 | 68.2 | 75.8 | 58.6 | 84.5 | 94.9 | **67.7** | 95.8 | 61.4 | **75.6** | 99.2 | **85.6** | 77.1 |
| InternVL-C (ours) | **99.4** | **93.2** | **80.6** | 89.5 | 76.0 | 52.7 | 34.1 | 94.2 | **72.0** | **70.7** | **79.4** | 56.2 | **86.1** | **95.3** | 65.5 | **96.0** | **67.9** | 74.2 | 99.5 | 80.0 | **78.1** |
<div id="tab: tiny_lvlm">

| method               | LLM         |  VR  |  VP  | VKA  |  VC  |  OH  |  Overall  |
|:---------------------|:------------|:----:|:----:|:----:|:----:|:----:|:---------:|
| MiniGPT-4            | Vicuna-7B   | 37.6 | 37.8 | 17.6 | 49.0 | 50.7 |   192.6   |
| LLaVA                | Vicuna-7B   | 41.6 | 38.3 | 18.7 | 49.4 | 49.0 |   197.0   |
| VisualGLM            | ChatGLM-6B  | 37.3 | 36.3 | 46.9 | 37.6 | 54.0 |   211.9   |
| Otter                | Otter-9B    | 41.6 | 37.0 | 15.1 | 52.4 | 74.0 |   216.4   |
| LLaMA-Adapter-V2     | LLaMA-7B    | 43.5 | 46.8 | 22.3 | 56.0 | 60.7 |   229.2   |
| Lynx                 | Vicuna-7B   | 52.2 | 65.8 | 17.6 | 57.4 | 86.3 |   279.2   |
| BLIP-2               | FlanT5xl    | 44.9 | 49.0 | 64.1 | 44.0 | 82.7 |   284.7   |
| InstructBLIP         | Vicuna-7B   | 46.7 | 48.0 | 61.7 | 59.2 | 85.0 |   300.6   |
| LLaVA-1.5            | Vicuna-7B   | 55.6 | 49.0 | 57.0 | 57.2 | 88.3 |   307.2   |
| Qwen-VL-Chat         | Qwen-7B     | 62.4 | 54.5 | 55.1 | 54.8 | 90.0 |   316.8   |
| Bard                 | Bard        | 64.2 | 57.0 | 68.1 | 59.6 | 70.7 |   319.6   |
| InternLM-XComposer   | InternLM-7B | 55.8 | 53.8 | 64.1 | 61.8 | 87.0 |   322.5   |
| InternVL-Chat (ours) | Vicuna-13B  | 56.4 | 52.3 | 68.0 | 62.0 | 89.0 | **327.6** |

**Evaluation of Tiny LVLM test set.** Here we report five categories of multimodal capabilities, including visual reasoning (VR), visual perception (VP), visual knowledge acquisition (VKA), visual commonsense (VC), and object hallucination (OH).
**Compatibility with Other LLM.** In this experiment, we test the compatibility of InternVL with LLMs other than Vicuna . The experimental setup used here is the same as in Table 9 of the main paper. As shown in Table 15, InternLM-7B achieves slightly better performance than Vicuna-7B . This indicates that our InternVL exhibits promising compatibility with various LLMs.

**Efficiency Analysis.** In this study, we analyze the computational efficiency of InternVL in encoding image-text pairs. The entire encoding process consists of two parts: image encoding and text encoding. The analysis covered two models (InternVL-C and InternVL-G) and their performance across three different image sizes (224, 336, and 448). The results are shown in Table 16.

From these results, we find that: (1) As the image size increases, the encoding time also significantly increases, leading directly to a decrease in frame rate; (2) InternVL-G slightly increased the encoding time due to the introduction of QLLaMA for secondary image encoding, but it still maintains a reasonable frame rate across all image sizes; (3) Even though we scale up the text encoder, the additional cost of text encoding is not significant, as the main time expenditure lies in image encoding. In summary, when choosing between InternVL-C and InternVL-G, one should weigh the trade-off between computational efficiency and potential performance improvements based on specific requirements. Additionally, these results were measured using PyTorch with Flash Attention and bf16 precision, and there is still considerable room for optimization, such as using model quantization and TensorRT.

<div id="tab:compatibility_with_other_llm">


**Table 18.** **Compatibility with other LLM.** Here we use InternLM  as an example to verify the compatibility of InternVL with LLMs other than Vicuna . The experimental settings used here are the same as in Table 9 of the main paper. 
<tbody>
<tr>
<td style="text-align: left;">visual</td>
<td style="text-align: left;">glue</td>
<td style="text-align: left;"></td>
<td colspan="4" style="text-align: center;">visual question answering</td>
<td colspan="2" style="text-align: center;">dialogue</td>
</tr>
<tr>
<td style="text-align: left;">encoder</td>
<td style="text-align: left;">layer</td>
<td style="text-align: left;">LLM</td>
<td style="text-align: center;">VQA<sup>v2</sup></td>
<td style="text-align: center;">GQA</td>
<td style="text-align: center;">VizWiz</td>
<td style="text-align: center;">VQA<sup>T</sup></td>
<td style="text-align: center;">MME</td>
<td style="text-align: center;">POPE</td>
</tr>
<tr>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">MLP</td>
<td style="text-align: left;">Vicuna-7B</td>
<td style="text-align: center;">79.3</td>
<td style="text-align: center;">62.9</td>
<td style="text-align: center;">52.5</td>
<td style="text-align: center;">57.0</td>
<td style="text-align: center;">1525.1</td>
<td style="text-align: center;">86.4</td>
</tr>
<tr>
<td style="text-align: left;">IViT-6B</td>
<td style="text-align: left;">MLP</td>
<td style="text-align: left;">InternLM-7B</td>
<td style="text-align: center;">79.7</td>
<td style="text-align: center;">63.2</td>
<td style="text-align: center;">53.1</td>
<td style="text-align: center;">58.0</td>
<td style="text-align: center;">1532.8</td>
<td style="text-align: center;">86.4</td>
</tr>
</tbody>

<div id="tab:ablation_efficiency">


**Table 19.** **Efficiency analysis of InternVL for encoding image-text pairs.** The total time to encode an image-text pair includes both the image encoding part and the text encoding part. We measure the time cost with a batch size of 128 on a single A100 GPU. Flash Attention  and bf16 precision are used during testing. 
<tbody>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: center;">image</td>
<td colspan="2" style="text-align: center;">encode image (ms)</td>
<td style="text-align: center;">encode text (ms)</td>
<td style="text-align: center;">total</td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: left;">method</td>
<td style="text-align: center;">size</td>
<td style="text-align: center;">InternViT-6B</td>
<td style="text-align: center;">QLLaMA</td>
<td style="text-align: center;">QLLaMA</td>
<td style="text-align: center;">time</td>
<td style="text-align: center;">FPS</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">15.5</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">4.9</td>
<td style="text-align: center;">20.4</td>
<td style="text-align: center;">48.9</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C</td>
<td style="text-align: center;">336</td>
<td style="text-align: center;">35.2</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">4.9</td>
<td style="text-align: center;">40.1</td>
<td style="text-align: center;">24.9</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-C</td>
<td style="text-align: center;">448</td>
<td style="text-align: center;">66.9</td>
<td style="text-align: center;">–</td>
<td style="text-align: center;">4.9</td>
<td style="text-align: center;">71.8</td>
<td style="text-align: center;">13.9</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G</td>
<td style="text-align: center;">224</td>
<td style="text-align: center;">15.5</td>
<td style="text-align: center;">8.2</td>
<td style="text-align: center;">4.9</td>
<td style="text-align: center;">28.6</td>
<td style="text-align: center;">35.0</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G</td>
<td style="text-align: center;">336</td>
<td style="text-align: center;">35.2</td>
<td style="text-align: center;">10.3</td>
<td style="text-align: center;">4.9</td>
<td style="text-align: center;">50.4</td>
<td style="text-align: center;">19.8</td>
</tr>
<tr>
<td style="text-align: left;">InternVL-G</td>
<td style="text-align: center;">448</td>
<td style="text-align: center;">66.9</td>
<td style="text-align: center;">12.8</td>
<td style="text-align: center;">4.9</td>
<td style="text-align: center;">84.6</td>
<td style="text-align: center;">11.8</td>
</tr>
</tbody>

## Detailed Training Settings

**Settings of Stage 1.** As shown in Table 17, in this stage, the image encoder InternViT-6B is randomly initialized using the BEiT’s initialization method , and the text encoder LLaMA-7B is initialized with the pre-trained weights from , a multilingual LLaMA-7B. All parameters are fully trainable. We employ the AdamW optimizer  with $`\beta_{1}=0.9`$, $`\beta_{2}=0.95`$, weight decay at 0.1, and a cosine learning rate schedule starting at 1e-3 and 1e-4 for the image and text encoders, respectively. We adopt a uniform drop path rate of 0.2. The training involves a total batch size of 164K across 640 A100 GPUs, extending over 175K iterations to process about 28.7 billion samples. To enhance efficiency, we initially train at a 196$`\times`$<!-- -->196 resolution, masking 50% of image tokens , and later switch to 224$`\times`$<!-- -->224 resolution without masking for the final 0.5 billion samples.

**Settings of Stage 2.** In this stage, InternViT-6B and QLLaMA inherit their weights from the first stage, while the learnable queries and cross-attention layers in QLLaMA are randomly initialized. Benefiting from the powerful encoding capabilities learned in the first stage, we keep both InternViT-6B and QLLaMA frozen and only train the newly added parameters. The input images are processed at a resolution of 224$`\times`$<!-- -->224. For optimization, the AdamW optimizer  is employed with $`\beta_{1}=0.9`$, $`\beta_{2}=0.98`$, weight decay set at 0.05, and a total batch size of 20K. The training extends over 80K steps across 160 A100 GPUs, inclusive of 2K warm-up steps, and is governed by a cosine learning rate schedule with a peak learning rate of 5e-5. More detailed training settings are listed in Table 17.

<div id="tab:train_cfg_stage1_stage2">

| config | stage 1 | stage 2 |
|:---|:--:|:--:|
| image enc. weight init. | random init.  | from stage 1 |
| text enc. weight init. | from  | from stage 1 |
| image enc. peak learning rate | 1e-3 | frozen |
| text enc. peak learning rate | 1e-4 | frozen |
| cross attn peak learning rate | – | 5e-5 |
| learning rate schedule | cosine decay | cosine decay |
| optimizer | AdamW  | AdamW  |
| optimizer hyper-parameters | $`\beta_{1}`$, $`\beta_{2}`$ = 0.9, 0.95 | $`\beta_{1}`$, $`\beta_{2}`$ = 0.9, 0.98 |
| weight decay | 0.1 | 0.05 |
| input resolution | 196$`^2`$ $`\rightarrow`$ 224$`^2`$ | 224$`^2`$ |
| patch size | 14 | 14 |
| total batch size | 164K | 20K |
| warm-up iterations | 5K | 2K |
| total iterations | 175K | 80K |
| samples seen | 28.7B | 1.6B |
| drop path rate  | uniform (0.2) | 0.0 |
| data augmentation | random resized crop | random resized crop |
| numerical precision | DeepSpeed bf16  | DeepSpeed bf16  |
| trainable / total parameters | 13B / 13B | 1B / 14B |
| GPUs for training | 640$`\times`$A100 (80G) | 160$`\times`$A100 (80G) |

**Training settings of InternVL’s stage 1 and stage 2.** “196$`^2`$ $`\rightarrow`$ 224$`^2`$" means we initially train at a 196$`\times`$<!-- -->196 resolution, and later switch to 224$`\times`$<!-- -->224 resolution for the final 0.5 billion samples, for higher training efficiency.
<div id="tab:train_cfg_ft_retrieval">

| config | retrieval fine-tuning |
|:---|:--:|
| image-text data |        Flickr30K  / Flickr30K-CN         |
| peak learning rate | 1e-6 |
| layer-wise lr decay rate | InternViT-6B (0.9), QLLaMA (0.9) |
| learning rate schedule | cosine decay |
| optimizer | AdamW  |
| optimizer hyper-parameters | $`\beta_{1}`$, $`\beta_{2}`$ = 0.9, 0.999 |
| weight decay | 0.05 |
| input resolution | 364$`^2`$ |
| patch size | 14 |
| total batch size | 1024 |
| warm-up iterations | 100 |
| training epochs | 10 |
| drop path rate  | 0.3 |
| data augmentation | random resized crop & flip |
| numerical precision | DeepSpeed bf16  |
| trainable / total parameters       | 14B / 14B |
| GPUs for training | 32$`\times`$A100 (80G) |

**Training settings of retrieval fine-tuning.** We fine-tune InternVL on Flickr30K and Flickr30K-CN separately.
**Settings of Stage 3.** At this stage, we have two different configurations. One is to use InternViT-6B separately, as shown in Figure 3 (c). The other is to use the entire InternVL model simultaneously, as shown in Figure 3 (d).

\(1\) InternVL-Chat (w/o QLLaMA): For this setup, we follow the training recipes of LLaVA-1.5 . We use the same hyperparameters and datasets for supervised fine-tuning, we first train the MLP layers with the LGS-558K dataset, and then train the LLM with the LLaVA-Mix-665K dataset, both for one epoch.

(2) InternVL-Chat (w/ QLLaMA): For this more advanced setup, we also conducted the training in two steps. We first train the MLP layers with our custom SFT dataset and then fine-tune the LLM with it. Due to the expansion of the dataset, we increased the batch size to 512.

**Settings of Retrieval Fine-tuning.** In this experiment, all parameters of InternVL are set to be trainable. We conduct separate fine-tuning on the Flickr30K and Flickr30K-CN . Following common practice , a 364$`\times`$<!-- -->364 resolution is adopted for fine-tuning. To avoid over-fitting, we apply a layer-wise learning rate decay of 0.9 to both InternViT-6B and QLLaMA, along with a drop path rate of 0.3 for InternViT-6B. The AdamW optimizer is utilized, with a total batch size of 1024, for fine-tuning the InternVL model across 10 epochs. For more detailed training settings, please refer to Table 18.

<div id="tab:train_cfg_in_linear">

| config                       |           ImageNet linear probing            |
|:-----------------------------|:--------------------------------------------:|
| peak learning rate           |                     0.2                      |
| learning rate schedule       |                 cosine decay                 |
| optimizer                    |                     SGD                      |
| optimizer momentum           |                     0.9                      |
| weight decay                 |                     0.0                      |
| input resolution             |                  224$`^2`$                   |
| patch size                   |                      14                      |
| total batch size             |                     1024                     |
| warm-up epochs               |                      1                       |
| training epochs              |                      10                      |
| data augmentation            |          random resized crop & flip          |
| GPUs for training            |            8$`\times`$A100 (80G)             |

**Training settings of ImageNet linear probing.**
<div id="tab:train_cfg_ade20k">

| config                     | linear probing / head tuning / full tuning |
|:---------------------------|:------------------------------------------:|
| peak learning rate         |                    4e-5                    |
| layer-wise lr decay rate   |                – / – / 0.95                |
| learning rate schedule     |              polynomial decay              |
| optimizer                  |                   AdamW                    |
| optimizer hyper-parameters | $`\beta_{1}`$, $`\beta_{2}`$ = 0.9, 0.999  |
| weight decay               |             0.0 / 0.05 / 0.05              |
| input resolution           |                 504$`^2`$                  |
| patch size                 |                     14                     |
| total batch size           |                     16                     |
| warm-up iterations         |                    1.5K                    |
| total iterations           |                    80K                     |
| drop path rate             |              0.0 / 0.0 / 0.4               |
| data augmentation          |       default augmentation in MMSeg        |
| numerical precision        |              DeepSpeed bf16                |
| GPUs for training          |           8$`\times`$A100 (80G)            |

**Training settings of ADE20K semantic segmentation.** We list the hyperparameters for three different configurations, including linear probing, head tuning, and full-parameter tuning.
<img src="../images/InternVL_md_images/figure/stage1_2_datasets.pdf.png" style="width:100.0%"  />
**Figure 5.** **Panoramic overview of the datasets used in InternVL’s stage 1 and stage 2.** During the training of stage 1 and stage 2, we utilize web-scale image-text data from a variety of sources to train our InternVL model, as shown in (a). To assess InternVL’s capabilities in handling generic visual-linguistic tasks, we conducted extensive validations across a range of tasks and datasets, including (b) image classification, (c) video classification, (d) image-text retrieval, (e) video-text retrieval, (f) image captioning, and (g) semantic segmentation.

**Settings of ImageNet Linear Probing.** We follow the common practices of linear probing in previous methods . Specifically, we employ an additional BatchNorm to normalize the pre-trained backbone features during training. Besides, we concatenate the average-pooled patch token features with the class token. The linear head is trained using the SGD optimizer for 10 epochs on ImageNet-1K , with a total batch size of 1024, a peak learning rate of 0.2, 1 epoch warm-up, and no weight decay. Data augmentation involves random-resized-crop and flip. For more training details, please see Table 19.

**Settings of ADE20K Semantic Segmentation.** In Table 20, we have listed the hyperparameters for three different configurations in ADE20K semantic segmentation, including linear probing, head tuning, and full-parameter tuning.

## Data Preparation for Pre-training

**Training Data for Stage 1 & Stage 2.** During the first and second stages, we employed a vast collection of image-text pair data (see Figure 4 (a)), such as LAION-en , LAION-multi , LAION-COCO , COYO , Wukong , among others . A detailed introduction to these datasets is provided in Table 24.

**Training Data Cleaning for Stage 1 & Stage 2.** To fully utilize web-scale image-text data, we adopted different data filtering strategies in stage 1 and stage 2.

\(1\) Stage 1: In the first stage, we applied only minor data filtering, thus retaining the vast majority of the data. We considered six factors: CLIP similarity, watermark probability, unsafe probability, aesthetic score, image resolution, and caption length, to remove extreme data points and avoid disrupting training stability. Additionally, we removed data that was duplicated with ImageNet-1K/22K , Flickr30K , and COCO to ensure the reliability of our zero-shot evaluations. Due to download failures and the use of our data filtering pipeline, the total amount of data retained in the first stage was 4.98 billion.

\(2\) Stage 2: In the second stage, we implemented a more stringent data filtering strategy. With generative supervision included, we deleted most of the low-quality data based on the captions, mainly considering the length, completeness, readability, and whether they were gibberish or boilerplate (like menus, error messages, or duplicate text), contained offensive language, placeholder text, or source code. We retained only 1.03 billion entries.

**Testing Datasets for Image Classification.** We conducted extensive validation on image classification tasks (see Figure 4 (b)), including the linear probing performance of InternViT-6B and the zero-shot performance of InternVL-C. These datasets used are listed in Table 24.

**Testing Datasets for Video Classification.** As shown in Figure 4 (c), to evaluate the capabilities of video classification, we utilize the following Kinetics datasets: Kinetics 400 , Kinetics 600 , and Kinetics 700 .

**Testing Datasets for Image-Text Retrieval.** We use five datasets (see Figure 4 (d)) to evaluate InternVL’s zero-shot, multilingual image-text retrieval capabilities. A detailed introduction to these datasets is provided in Table 25.

**Testing Dataset for Video-Text Retrieval.** As shown in Figure 4 (e), we use the MSR-VTT dataset to evaluate our InternVL in zero-shot video-text retrieval.

**Testing Dataset for Image Captioning.** As illustrated in Figure 4 (f), we use three image captioning datasets to test our InternVL model. A detailed introduction to these datasets is provided in Table 26.

**Testing Dataset for Semantic Segmentation.** We use the ADE20K dataset to study the pixel-level perceptual capacity of InternViT-6B, as shown in Figure 4 (g). A detailed introduction to this dataset is provided in Table 26.

## Data Preparation for SFT

**Training Data for SFT.** In this stage, we collect a wide range of high-quality instruction data. For non-dialogue datasets, we follow the method described in for conversion. A detailed introduction is provided in Table 27.

**Testing Datasets for SFT.** We validate the effectiveness of our supervised fine-tuned InternVL-Chat models on three tasks, including image captioning, visual question answering, and multi-modal dialogue. There datasets are listed in Table 28. For most of these datasets, we employ the same response formatting prompt as for LLaVA-1.5 .

<thead>
<tr>
<th style="text-align: left;">dataset</th>
<th style="text-align: left;">introduction</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: left;">*Training Data for Stage 1 &amp; Stage 2.*</td>
</tr>
<tr>
<td style="text-align: left;">LAION-en </td>
<td style="text-align: left;">LAION-en is a part of the LAION-5B dataset, containing 2.32 billion English-only image-text pairs.</td>
</tr>
<tr>
<td style="text-align: left;">LAION-multi </td>
<td style="text-align: left;">LAION-multi is another segment of LAION-5B, featuring 2.26 billion image-text pairs across more than 100 languages, and is ideal for multilingual studies.</td>
</tr>
<tr>
<td style="text-align: left;">Laion-COCO </td>
<td style="text-align: left;">Laion-COCO comprises 663 million synthetic captions for web images, generated using a blend of BLIP-L/14  and CLIP models .</td>
</tr>
<tr>
<td style="text-align: left;">COYO </td>
<td style="text-align: left;">COYO-700M is a large-scale dataset that contains 747 million image-text pairs as well as many other meta-attributes to increase the usability to train various models. It follows a similar strategy to previous vision-language datasets, collecting many informative pairs of alt-text and its associated image in HTML documents.</td>
</tr>
<tr>
<td style="text-align: left;">Wukong </td>
<td style="text-align: left;">Wukong is a large-scale Chinese image-text dataset for benchmarking different multi-modal pre-training methods. It contains 100 million Chinese image-text pairs from the web.</td>
</tr>
<tr>
<td style="text-align: left;">CC3M </td>
<td style="text-align: left;">This dataset consists of approximately 3 million images, each annotated with a caption.</td>
</tr>
<tr>
<td style="text-align: left;">CC12M </td>
<td style="text-align: left;">CC12M is a dataset with 12 million image-text pairs. It is larger and covers a much more diverse set of visual concepts than the CC3M .</td>
</tr>
<tr>
<td style="text-align: left;">SBU </td>
<td style="text-align: left;">The SBU Captioned Photo Dataset is a collection of over 1 million images with associated text descriptions extracted from Flicker.</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">*Testing Datasets for Image Classification.*</td>
</tr>
<tr>
<td style="text-align: left;">ImageNet-1K </td>
<td style="text-align: left;">A large-scale dataset commonly used in image classification, consisting of over 1 million images across 1K different classes.</td>
</tr>
<tr>
<td style="text-align: left;">ImageNet-ReaL </td>
<td style="text-align: left;">It contains ImageNet val images augmented with a new set of “re-assessed" labels. These labels are collected using an enhanced protocol, resulting in multi-label and more accurate annotations.</td>
</tr>
<tr>
<td style="text-align: left;">ImageNet-V2 </td>
<td style="text-align: left;">A dataset created to test the robustness of models trained on ImageNet-1K, containing new test images collected following the original methodology.</td>
</tr>
<tr>
<td style="text-align: left;">ImageNet-A </td>
<td style="text-align: left;">It consists of real-world, unmodified, and naturally occurring examples that are misclassified by ResNet models . It’s designed to highlight the challenges of adversarial examples in natural settings.</td>
</tr>
<tr>
<td style="text-align: left;">ImageNet-R </td>
<td style="text-align: left;">A set of images labeled with ImageNet labels obtained by collecting art, cartoons, deviantart, graffiti, embroidery, graphics, origami, paintings, patterns, plastic objects, plush objects, sculptures, sketches, tattoos, toys, and video game renditions of ImageNet classes. It has renditions of 200 ImageNet classes resulting in 30K images.</td>
</tr>
<tr>
<td style="text-align: left;">ImageNet-Sketch </td>
<td style="text-align: left;">It consists of 51K images, approximately 50 images for each of the ImageNet classes. It is constructed using Google Image queries with the standard class name followed by “sketch of".</td>
</tr>
<tr>
<td style="text-align: left;">ObjectNet </td>
<td style="text-align: left;">ObjectNet is a crowd-sourced test set of 50K images featuring objects in unusual poses and cluttered scenes, designed to challenge recognition performance. It includes controls for rotation, background, and viewpoint, and covers 313 object classes, with 113 overlapping with ImageNet .</td>
</tr>
<tr>
<td style="text-align: left;">Multilingual IN-1K </td>
<td style="text-align: left;">An adaptation of ImageNet-1K supporting multilingual annotations, facilitating research in cross-lingual image classification.</td>
</tr>
<tr>
<td style="text-align: left;">CIFAR-10/100 </td>
<td style="text-align: left;">It comprises 60K 32×32 images in 10 classes (CIFAR-10) or 100 classes (CIFAR-100).</td>
</tr>
<tr>
<td style="text-align: left;">MNIST </td>
<td style="text-align: left;">A classic dataset containing 70K 28×28 gray-scale images of handwritten digits.</td>
</tr>
<tr>
<td style="text-align: left;">Caltech-101 </td>
<td style="text-align: left;">The dataset comprises images of objects from 101 classes and a background clutter class, each labeled with a single object. It contains about 40 to 800 images per class, totaling approximately 9K images.</td>
</tr>
<tr>
<td style="text-align: left;">SUN397 </td>
<td style="text-align: left;">The SUN397 or Scene UNderstanding (SUN) is a dataset for scene recognition consisting of 397 categories with 109K images.</td>
</tr>
<tr>
<td style="text-align: left;">FGVC Aircraft </td>
<td style="text-align: left;">The dataset contains 10K images of aircraft, with 100 images for each of 102 different aircraft model variants, most of which are airplanes.</td>
</tr>
<tr>
<td style="text-align: left;">Country-211 </td>
<td style="text-align: left;">It is a dataset released by OpenAI, designed to assess the geolocation capability of visual representations. It filters the YFCC100M  dataset to find 211 countries that have at least 300 photos with GPS coordinates. OpenAI built a balanced dataset with 211 categories, by sampling 200 photos for training and 100 photos for testing, for each country.</td>
</tr>
<tr>
<td style="text-align: left;">Stanford Cars </td>
<td style="text-align: left;">This dataset consists of 196 classes of cars with a total of 16K images, taken from the rear. The data is divided into almost a 50-50 train/test split with 8K training images and 8K testing images.</td>
</tr>
</tbody>


<thead>
<tr>
<th style="text-align: left;">dataset</th>
<th style="text-align: left;">introduction</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: left;">*Testing Datasets for Image Classification.*</td>
</tr>
<tr>
<td style="text-align: left;">Birdsnap </td>
<td style="text-align: left;">Birdsnap is a large bird dataset consisting of 49,829 images from 500 bird species with 47,386 images used for training and 2,443 images used for testing. Due to broken links, we are only able to download 1,845 out of the 2,443 testing images.</td>
</tr>
<tr>
<td style="text-align: left;">DTD </td>
<td style="text-align: left;">The Describable Textures Dataset (DTD) contains 5,640 texture images in the wild. They are annotated with human-centric attributes inspired by the perceptual properties of textures.</td>
</tr>
<tr>
<td style="text-align: left;">Eurosat </td>
<td style="text-align: left;">This dataset is based on Sentinel-2 satellite images covering 13 spectral bands and consisting of 10 classes with 27K labeled and geo-referenced samples.</td>
</tr>
<tr>
<td style="text-align: left;">FER2013 </td>
<td style="text-align: left;">This dataset includes around 30K RGB facial images, categorized into seven expressions: angry, disgust, fear, happy, sad, surprise, and neutral.</td>
</tr>
<tr>
<td style="text-align: left;">Flowers-102 </td>
<td style="text-align: left;">It is consistent with 102 flower categories commonly occurring in the United Kingdom. Each class consists of between 40 and 258 images.</td>
</tr>
<tr>
<td style="text-align: left;">Food-101 </td>
<td style="text-align: left;">The Food-101 dataset consists of 101 food categories with 750 training and 250 test images per category, making a total of 101K images.</td>
</tr>
<tr>
<td style="text-align: left;">GTSRB </td>
<td style="text-align: left;">The German Traffic Sign Recognition Benchmark (GTSRB) contains 43 classes of traffic signs, split into 39,209 training images and 12,630 test images.</td>
</tr>
<tr>
<td style="text-align: left;">Pets </td>
<td style="text-align: left;">The Oxford-IIIT Pet Dataset is a 37-category pet dataset with roughly 200 images for each class created by the Visual Geometry Group at Oxford.</td>
</tr>
<tr>
<td style="text-align: left;">Rendered SST2 </td>
<td style="text-align: left;">This dataset is used to evaluate the model’s capability on optical character recognition. It was generated by rendering sentences in the Standford Sentiment Treebank v2 dataset.</td>
</tr>
<tr>
<td style="text-align: left;">Resisc45 </td>
<td style="text-align: left;">This is a dataset for remote sensing scene classification. It contains 31,500 RGB images divided into 45 scene classes, each class containing 700 images.</td>
</tr>
<tr>
<td style="text-align: left;">STL10 </td>
<td style="text-align: left;">The STL-10 dataset, inspired by CIFAR-10 , includes 10 classes with 500 training and 800 test color images each, sized 96×96 pixels.</td>
</tr>
<tr>
<td style="text-align: left;">VOC2007 </td>
<td style="text-align: left;">The Pascal VOC 2007 dataset focuses on recognizing objects in realistic scenarios and contains 20 object classes across 9,963 images with 24,640 labeled objects. The data has been divided into 50% for training/validation and 50% for testing. Following common practice, we conduct zero-shot image classification by cropping images to isolate objects using bounding boxes.</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">*Testing Datasets for Video Classification.*</td>
</tr>
<tr>
<td style="text-align: left;">Kinetics 400 </td>
<td style="text-align: left;">A large-scale dataset containing around 400 human action classes with at least 400 video clips for each class, sourced from YouTube.</td>
</tr>
<tr>
<td style="text-align: left;">Kinetics 600 </td>
<td style="text-align: left;">An expansion of Kinetics 400, this dataset includes 600 action classes and provides an increased diversity in video representation.</td>
</tr>
<tr>
<td style="text-align: left;">Kinetics 700 </td>
<td style="text-align: left;">The latest in the series, Kinetics 700 offers an even broader range with 700 action categories, further challenging the robustness of retrieval models.</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">*Testing Datasets for Image-Text Retrieval.*</td>
</tr>
<tr>
<td style="text-align: left;">COCO </td>
<td style="text-align: left;">The COCO Caption dataset contains diverse images with detailed captions, widely used for image-text retrieval and image captioning tasks.</td>
</tr>
<tr>
<td style="text-align: left;">COCO-CN </td>
<td style="text-align: left;">COCO-CN is a bilingual image description dataset enriching COCO with manually written Chinese sentences and tags. The new dataset can be used for multiple tasks including image tagging, captioning, and retrieval, all in a cross-lingual setting.</td>
</tr>
<tr>
<td style="text-align: left;">Flickr30K </td>
<td style="text-align: left;">This dataset comprises 31,000 images sourced from Flickr, each annotated with five captions, making it suitable for image-text retrieval.</td>
</tr>
<tr>
<td style="text-align: left;">Flickr30K-CN </td>
<td style="text-align: left;">Flickr30K-CN offers Chinese captions for the images, enabling studies in cross-lingual and multi-modal retrieval tasks.</td>
</tr>
<tr>
<td style="text-align: left;">XTD </td>
<td style="text-align: left;">A newly developed 1K multilingual test set, featuring COCO images annotated in various languages.</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">*Testing Dataset for Video-Text Retrieval.*</td>
</tr>
<tr>
<td style="text-align: left;">MSR-VTT </td>
<td style="text-align: left;">This is a large-scale dataset for open-domain video captioning and video-text retrieval, comprising 10,000 video clips across 20 categories. Each clip is annotated with 20 English sentences, totaling about 29,000 distinct words in all captions. The standard division of the dataset allocates 6,513 clips for training, 497 for validation, and 2,990 for testing purposes.</td>
</tr>
</tbody>


<thead>
<tr>
<th style="text-align: left;">dataset</th>
<th style="text-align: left;">introduction</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: left;">*Testing Datasets for Image Captioning.*</td>
</tr>
<tr>
<td style="text-align: left;">COCO </td>
<td style="text-align: left;">We use the Karpathy test set for testing.</td>
</tr>
<tr>
<td style="text-align: left;">Flickr30K </td>
<td style="text-align: left;">We use the Karpathy test set for testing.</td>
</tr>
<tr>
<td style="text-align: left;">NoCaps </td>
<td style="text-align: left;">NoCaps stands out for testing models’ capabilities in open-ended caption generation, using images that go beyond the training data’s domain. We report the performance on the NoCaps val set.</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">*Testing Dataset for Semantic Segmentation.*</td>
</tr>
<tr>
<td style="text-align: left;">ADE20K </td>
<td style="text-align: left;">ADE20K contains more than 20K scene-centric images exhaustively annotated with pixel-level objects and object parts labels. There are a total of 150 semantic categories, which include stuffs like sky, road, grass, and discrete objects like person, car, bed. We report the performance on the ADE20K val set.</td>
</tr>
</tbody>


<thead>
<tr>
<th style="text-align: left;">dataset</th>
<th style="text-align: left;">introduction</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: left;">*Training Data for SFT.*</td>
</tr>
<tr>
<td style="text-align: left;">COCO Caption </td>
<td style="text-align: left;">It contains over 0.5 million captions describing over 110K images. Following common practice, we use the Karpathy training set for training. We transform it into a dialogue dataset using the response formatting prompt: “Provide a one-sentence caption for the provided image."</td>
</tr>
<tr>
<td style="text-align: left;">TextCaps </td>
<td style="text-align: left;">TextCaps contains 145K captions for 28K images. It challenges a model to recognize text, relate it to its visual context, and decide what part of the text to copy or paraphrase. OCR tokens are used during training. We transform it into a dialogue dataset using the response formatting prompt: “Provide a one-sentence caption for the provided image."</td>
</tr>
<tr>
<td style="text-align: left;">VQAv2 </td>
<td style="text-align: left;">VQAv2, the second version of the VQA dataset, features open-ended questions related to images. Answering these questions demands a grasp of vision, language, and common sense. We convert it into a dialogue dataset using the prompt: “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">OKVQA </td>
<td style="text-align: left;">A dataset with over 14K questions requiring external knowledge for answers, focusing on knowledge-based visual question answering. We transform it into a dialogue dataset using the response formatting prompt: “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">A-OKVQA </td>
<td style="text-align: left;">An augmented successor of OKVQA  and contains 25K questions requiring a broad base of commonsense and world knowledge to answer. We transform it into a dialogue dataset using the response formatting prompt: “Answer with the option’s letter from the given choices directly."</td>
</tr>
<tr>
<td style="text-align: left;">IconQA </td>
<td style="text-align: left;">A dataset with 107K questions across three sub-tasks, focusing on abstract diagram recognition and comprehensive visual reasoning. We convert it into a dialogue dataset using these prompts: “Answer with the option’s letter from the given choices directly." and “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">AI2D </td>
<td style="text-align: left;">AI2D features over 5K grade school science diagrams with rich annotations and 15K multiple-choice questions for diagram understanding research. We convert it into a dialogue dataset using the prompt: “Please answer the question based on the options mentioned before."</td>
</tr>
<tr>
<td style="text-align: left;">GQA </td>
<td style="text-align: left;">GQA is a large-scale dataset with more than 110K images and 22 million questions, combining real images with balanced question-answer pairs for visual reasoning. We transform it into a dialogue dataset using the prompt: “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">OCR-VQA </td>
<td style="text-align: left;">The OCR-VQA dataset contains 207,572 images of book covers and more than 1 million question-answer pairs about these images. We convert it into a dialogue dataset using the response formatting prompt: “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">ChartQA </td>
<td style="text-align: left;">ChartQA is a dataset for question answering about charts, focusing on visual and logical reasoning. It comprises 9.6K human-written questions and 23.1K questions generated from human-written chart summaries. We convert it using the prompt: “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">DocVQA </td>
<td style="text-align: left;">The DocVQA dataset consists of 50,000 questions defined on over 12,000 document images. We convert it into a dialogue dataset using the prompt: “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">ST-VQA </td>
<td style="text-align: left;">The ST-VQA dataset contains a total of 31,791 questions over 23,038 images. The training set alone consists of 26,308 questions based on 19,027 images. We convert it into a dialogue dataset using the response formatting prompt: “Answer the question using a single word or phrase."</td>
</tr>
</tbody>


<thead>
<tr>
<th style="text-align: left;">dataset</th>
<th style="text-align: left;">introduction</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: left;">*Training Data for SFT.*</td>
</tr>
<tr>
<td style="text-align: left;">EST-VQA </td>
<td style="text-align: left;">The EST-VQA dataset provides questions, images, and answers, but also a bounding box for each question that indicates the area of the image that informs the answer. We convert it into a dialogue dataset using the response formatting prompt: “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">InfoVQA </td>
<td style="text-align: left;">This dataset includes a diverse collection of infographics with natural language questions and answers. It focuses on reasoning over document layout, textual content, graphical elements, and data visualizations. We convert it into a dialogue dataset using the prompt: “Answer the question using a single word or phrase."</td>
</tr>
<tr>
<td style="text-align: left;">LLaVAR </td>
<td style="text-align: left;">The LLaVAR dataset advances visual instruction tuning for Large Language Models by focusing on text-rich images. It incorporates 422K images processed with OCR and 16K GPT-4 generated conversations, enhancing text-based VQA performance and human interaction capabilities in diverse scenarios. Note that, we only use the 20K high-quality data for fine-tuning of LLaVAR.</td>
</tr>
<tr>
<td style="text-align: left;">RefCOCO </td>
<td style="text-align: left;">A mixed dataset of RefCOCO , RefCOCO+, and RefCOCO-g . We convert it into a dialogue dataset following LLaVA-1.5 .</td>
</tr>
<tr>
<td style="text-align: left;">Toloka </td>
<td style="text-align: left;">The TolokaVQA dataset comprises images with associated textual questions, each marked with a bounding box indicating the visual answer. It’s sourced from a licensed subset of the COCO dataset and labeled on the Toloka platform. We convert it into a dialogue dataset following LLaVA-1.5 .</td>
</tr>
<tr>
<td style="text-align: left;">LLaVA-150K </td>
<td style="text-align: left;">This is a set of GPT-generated multi-modal instruction-following data, constructed for visual instruction tuning and building large multi-modal models towards GPT-4 vision/language capability. It includes 158K unique language-image instruction-following samples.</td>
</tr>
<tr>
<td style="text-align: left;">SVIT </td>
<td style="text-align: left;">This dataset includes 3.2 million visual instruction tuning data, with 1.6M conversation QA pairs, 1.6M complex reasoning QA pairs, and 106K detailed image descriptions. It is designed to improve multi-modal performance in visual perception, reasoning, and planning. For this dataset, we merge the QA pairs from the same training image into a single conversation.</td>
</tr>
<tr>
<td style="text-align: left;">VisDial </td>
<td style="text-align: left;">A dataset based on the COCO images, featuring dialogues created by two Amazon Mechanical Turk workers. One plays the ‘questioner’, seeing only an image’s text description, and the other, the ‘answerer’, sees the image. They engage in a 10-round Q&amp;A session about the image.</td>
</tr>
<tr>
<td style="text-align: left;">LRV-Instruction </td>
<td style="text-align: left;">The LRV-Instruction dataset is designed to combat hallucination in large multi-modal models. It comprises 120K GPT-4-generated visual instructions for 16 vision-and-language tasks, including both positive and negative instructions for robust tuning. Negative instructions focus on Nonexistent and Existent Element Manipulation. This dataset helps improve accuracy and consistency in multi-modal tasks.</td>
</tr>
<tr>
<td style="text-align: left;">LLaVA-Mix-665K </td>
<td style="text-align: left;">LLaVA-Mix-665K is an instruction-following dataset mixed from 10 academically oriented datasets.</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">*Testing Dataset for SFT (Image Captioning).*</td>
</tr>
<tr>
<td style="text-align: left;">COCO </td>
<td style="text-align: left;">Karpathy test set is used for testing. The prompt is: “Provide a one-sentence caption for the provided image.”</td>
</tr>
<tr>
<td style="text-align: left;">Flickr30K </td>
<td style="text-align: left;">Karpathy test set is used for testing. The prompt is: “Provide a one-sentence caption for the provided image.”</td>
</tr>
<tr>
<td style="text-align: left;">NoCaps </td>
<td style="text-align: left;">NoCaps val set is used for testing. The prompt is: “Provide a one-sentence caption for the provided image.”</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">*Testing Dataset for SFT (Visual Question Answering).*</td>
</tr>
<tr>
<td style="text-align: left;">VQAv2 </td>
<td style="text-align: left;">VQAv2 test-dev set is used for testing. The prompt is: “Answer the question using a single word or phrase.”</td>
</tr>
<tr>
<td style="text-align: left;">GQA </td>
<td style="text-align: left;">GQA test-balanced set is used. The prompt is: “Answer the question using a single word or phrase.”</td>
</tr>
<tr>
<td style="text-align: left;">VizWiz </td>
<td style="text-align: left;">VizWiz test-dev set is used for testing. The prompt is: “When the provided information is insufficient, respond with ‘Unanswerable’. Answer the question using a single word or phrase.”</td>
</tr>
<tr>
<td style="text-align: left;">TextVQA </td>
<td style="text-align: left;">TextVQA val set is used for testing. The prompt is: “Answer the question using a single word or phrase.”</td>
</tr>
<tr>
<td colspan="2" style="text-align: left;">*Testing Dataset for SFT (Multi-Modal Dialogue).*</td>
</tr>
<tr>
<td style="text-align: left;">MME </td>
<td style="text-align: left;">MME is a comprehensive evaluation benchmark for multi-modal large language models. It measures both perception and cognition abilities on a total of 14 subtasks, including existence, count, position, color, poster, celebrity, scene, landmark, artwork, OCR, commonsense reasoning, numerical calculation, text translation, and code reasoning. The prompt for this dataset is: “Answer the question using a single word or phrase.”</td>
</tr>
<tr>
<td style="text-align: left;">POPE </td>
<td style="text-align: left;">POPE is a popular dataset used to evaluate object hallucination. The response formatting prompt used for this dataset is: “Answer the question using a single word or phrase.”</td>
</tr>
</tbody>

[^1]: $`\dagger`$ This work is done when they are interns at Shanghai AI Laboratory;  corresponding author (daijifeng@tsinghua.edu.cn)

## Caption Normalization Notes

**Figure 1.**

**Table 1.**

**Table 3.**

**Table 4.**

**Table 5.**

**Table 6.**

**Table 7.**

**Table 9.**

**Table 10.**

**Table 11.**

**Table 13.**

**Table 16.**

**Table 17.**

**Table 20.**

**Table 24.**

**Table 25.**

**Table 26.**

**Table 27.**

**Table 28.**

For completeness, Figure 5 is retained for numbering consistency.

