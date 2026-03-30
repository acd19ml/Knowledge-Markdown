# Introduction {#sec:intro}

Multimodal large language models (MLLMs) [@li2023multimodal] are key building blocks towards general-purpose visual assistants [@li2022elevater], and they have become increasingly popular in the research community. Though many recent MLLMs such as LLaVA [@llava], MiniGPT-4 [@zhu2023minigpt], Otter [@li2023otter], InstructBLIP [@Instructblip], Qwen-VL [@bai2023qwen] and LLaVA-1.5 [@liu2023improved] have demonstrated impressive results on instruction-following and visual reasoning capabilities, they mostly perform vision-language alignment on image-level using image-text pairs. The lack of region-level alignment hinders them from fine-grained image understanding tasks, such as region classification, captioning and reasoning.

To enable region-level understanding in vision-language models, some recent works, *e.g.*, Kosmos-2 [@peng2023kosmos], Shikra [@chen2023shikra], PVIT [@chen2023position] and GPT4RoI [@zhang2023gpt4roi], have attempted to process bounding box-specified regions and leverage visual instruction tuning with object-level spatial features. However, directly employing the sparse bounding box as the referring input region could involve irrelevant background features and may lead to inexact region-text pair alignment for visual instruction tuning on LLM. During inference, the box-level referring input may not be able to precisely indicate the object, resulting in semantic deviation, as illustrated in Figure 1(a). Besides, these models employ a relatively low input image resolution (*e.g.*, 224$\times$`<!-- -->`{=html}224), and struggle with understanding the details of dense object regions where a much higher resolution is required for optimal performance.

Compared with coarse bounding box, using fine-grained mask as the referring input can represent objects precisely. By training with billions of high-quality masks, the recently developed SAM [@kirillov2023segment] supports using simple bounding boxes or points as prompts while demonstrating exceptional segmentation quality on zero-shot object, part or subpart. Several studies, like HQ-SAM [@ke2023segment], further enhance SAM's capability on fine-grained segmentation and generalization, making the segmentation more practical for real-world applications. However, these models cannot provide the primary semantic labels, let alone detailed semantic attributes and captions. As a result, the existing methods are limited in understanding the real-world scenes with inherent fine-grained multimodal information.

![](../images/Osprey_md_images/figs/merge_5.pdf.png){width="99.9%"}
**Figure 1.** (a) Comparisons between our mask-level Osprey and box-level understanding approaches, *e.g.*, Shikra and GPT4RoI. Osprey can achieve accurate fine-grained region understanding. (b) An example of feeding Osprey with class-agnostic masks from off-the-shelf SAM. One can see that Osprey enables the generation of semantic captions and detailed descriptions of the given image using different prompts.

In this paper, we propose **Osprey**, a novel approach designed to extend the capability of MLLMs for fine-grained pixel-wise understanding. To this end, we present a mask-aware visual extractor to capture precise visual mask features with various granularity. These visual features are then interleaved with language instructions to form the input sequence to LLM. To facilitate the use of high resolution input, we leverage the convolutional CLIP backbone [@radford2021learning] as the vision encoder. Compared to ViT-based model, convolutional CLIP generalizes well to larger input resolution with efficiency and robustness. With the above designs, Osprey is capable of achieving fine-grained semantic understanding for part-level and object-level regions, providing primary object category, detailed object attributes, and more complex scene descriptions.

To obtain fine-grained pixel-level alignment between vision and language features, we meticulously curate a large-scale mask-based region-text dataset, namely **Osprey-724K**, where the mask and text description of each region are carefully annotated. The majority of data are crafted from publicly available datasets with thoughtfully designed prompt templates to make them instruction-following, including object-level and part-level samples. It includes not only detailed descriptions and conversations but also enriched attributes information. Moreover, we empirically introduce spatial-aware and class-aware negative data mining and short-form response instructions, which further enhances the robustness and flexibility of Osprey's response. By taking advantage of visual instruction tuning, our proposed model enables new capabilities beyond box-level and image-level understanding. As shown in Figure 1(b), Osprey can generate fine-grained semantics based on the class-agnostic masks from the off-the-shelf SAM [@kirillov2023segment]. Extensive experimental results on region-based recognition, classification, and complex description&reasoning tasks demonstrate the superiority of our approach.

The contributions of this work can be summarized as follows.

- We propose a novel approach, namely Osprey, to enable MLLM the pixel-level instruction tuning capability for fine-grained and open-world visual understanding.
- We construct a large-scale instruction tuning dataset with mask-text pairs, called Osprey-724K, which contains object-level, part-level and additional instruction samples for robustness and flexibility.
- Our method, as a fine-grained visual understanding approach, outperforms the previous state-of-the-art methods on a wide range of region understanding tasks.

![](../images/Osprey_md_images/figs/dataset_5.pdf.png){width="98.0%"}
**Figure 2.** Example sample of the Osprey-724K dataset to illustrate the mask-based instruction-following data.

# Related Work {#sec:relatedwork}

**Multimodal Large Language Models.** Large language models (LLMs), such as GPT-3 [@brown2020language], Flan-T5 [@chung2022scaling], PaLM [@chowdhery2022palm] and LLaMA [@touvron2023llama], have significantly advanced the research on Natural Language Processing (NLP). Such progresses have consequently facilitated the development of multimodal language models by expanding the training data and enlarging the model size. This scale-up has led to the breakthrough application of ChatGPT [@Chatgpt]. The great successes of LLMs and MLLMs have also inspired the research on computer vision, enabling multimodal in-context learning [@alayrac2022flamingo; @li2023blip].

Recent studies have been increasingly concentrated on how to leverage pre-trained LLMs for visual instruction tuning. Prominent examples include LLaVA [@llava], MiniGPT-4 [@zhu2023minigpt], mPLUG-Owl [@ye2023mplug], Otter [@li2023otter], InstructBLIP [@Instructblip], Qwen-VL [@bai2023qwen] and LLaVA-1.5 [@liu2023improved], *etc*. The common architecture among these models involves a pre-trained visual backbone to encode visual input, an LLM to understand user instructions and generate responses, and a vision-language cross-modal connector to align the output of vision encoder with the language model. While having demonstrated promising capabilities in the image-level multimodal tasks, these models show limited performance when specific regions are required as reference.

**Region-level Image Understanding.** In the context of region-level image understanding, potential regions of interest are first located before delving into the visual understanding [@qi2023aims; @qi2023high; @li2024label; @li2024box2mask]. The Segment Anything Model (SAM) [@kirillov2023segment], which was trained with billions of high-quality masks, has demonstrated exceptional zero-shot object/part/subpart segmentation quality with simple bounding boxes and points as prompts. As the vanilla SAM cannot provide semantic labels, various approaches, like SEEM [@zou2023segment], HIPIE [@wang2023hierarchical] and Semantic SAM [@li2023semantic], extend the model to predict the semantic category for mask recognition. The primary semantic label only, however, is often insufficient for real-world applications.

Therefore, it becomes imperative to incorporate additional semantics such as color, location, and even general descriptions for scene understanding and reasoning. Besides, though some works [@lai2023lisa; @ren2023pixellm] can achieve pixel-level grounding, they cannot provide the region-based descriptions. Recent studies such as GPT4RoI [@zhang2023gpt4roi], PVIT [@chen2023position], Kosmos-2 [@peng2023kosmos], Shikra [@chen2023shikra], Ferret [@you2023ferret] and GLaMM [@rasheed2023glamm] have enabled MLLMs to achieve region-based image understanding. However, most of these methods employ the bounding box as the referring region, which could involve irrelevant image features from background and introduce inexact region-text pair alignment for visual instructions tuning on LLM. Moreover, these models only allow a small input image size, *e.g.*, 224$\times$`<!-- -->`{=html}224, which may encounter difficulties in analyzing the details of dense object regions. To address these issues, in this work we introduce a pixel-level understanding method based on LLM. Our method supports the use of input masks for region referring and accommodates larger image resolution. Additionally, we curate a comprehensive dataset comprising mask-text pairs to facilitate instruction-based learning for this task.

# Osprey-724K Dataset {#sec:dataset}

In this section, we present Osprey-724K, an instruction dataset with mask-text pairs, containing around 724K multimodal dialogues to encourage MLLMs for fine-grained pixel-level image understanding. Specifically, Osprey-724K consists of *object-level* and *part-level* mask-text instruction data, which are created based on the publicly available datasets. To make the data instruction-following, we leverage GPT-4 to generate the high-quality mask-text pairs using carefully designed prompt templates. Additionally, to enhance the robustness and flexibility of the response, we introduce the negative sample mining method with short-form response formatting prompt. An example sample of Osprey-724K is shown in Figure 2, and the detailed statistics and distributions of our Osprey-724K dataset are illustrated in Table 1 and Figure 3, respectively.

<a id="tab:osprey-724k"></a>
**Table 1.** Data statistics of Osprey-724K.

| Type | Form | Raw Data | GPT-4 | #Samples |
| --- | --- | --- | --- | ---: |
| Object-level | Descriptions | COCO/RefCOCO/RefCOCO+/ | Yes | 70K |
| Object-level | Conversations | RefCOCOg/LLaVA-115K | Yes | 127K |
| Part-level | Categories | PACO-LVIS | Yes | 99K |
| Part-level | Attributes | PACO-LVIS | Yes | 207K |
| Robustness & Flexibility | Positive/Negative | COCO/RefCOCO/RefCOCO+/ | No | 64K/64K |
| Robustness & Flexibility | Short-Form | RefCOCOg/LLaVA-115K/LVIS | Yes | 99K |

![](../images/Osprey_md_images/figs/bing_data4_11.png){width="98.0%"}
**Figure 3.** Data distribution of Osprey-724K.

<a id="object-level"></a>
# Object-level Instructions {#object-level}
For an image with $N$ object regions, we make full use of its image-level and object-level captions based on the publicly datasets with mask annotations, such as COCO [@lin2014microsoft], RefCOCO [@refcoco_data], RefCOCO+ [@refcoco_data] and RefCOCOg [@refcoco_g]. However, these captions are plain and short with few semantic context, which are insufficient to train an MLLM.

To mitigate this issue, we curate a data processing pipeline to generate fine-grained region-based instruction data, including the object category, object type, object action, location, color, status, . Firstly, we employ the detailed description in LLaVA-115K [@llava] as the image-level description for the COCO images. Secondly, we leverage the language-only GPT-4 to create instruction-following data to generate the visual content of each object region with diversity. Specifically, we make full use of the bounding boxes and brief region captions, where each box encodes the object concept and its spatial location in the scene.

The short captions collected from RefCOCO [@refcoco_data], RefCOCO+ [@refcoco_data] and RefCOCOg [@refcoco_g] typically describe the specific regions from various perspectives. Based on these information, we employ GPT-4 to generate two types of data, , region level *Detailed Description* and *Conversation* samples. Please refer to the *Appendix* for the detailed prompts for GPT-4. Finally, we collect 197K unique object-level mask-region instruction-following samples in total.

# Part-level Instructions
To capture the part-level knowledge, we leverage the PACO-LVIS [@ramanathan2023paco] dataset, which encompasses 456 object-specific part classes distributed among 75 object categories. In specific, PACO-LVIS comprises 55 different attributes, including 29 colors, 10 patterns&markings, 13 materials and 3 levels of reflectance.

By taking consideration of these information, we employ GPT-4 to construct the instruction-following data via a question-and-answer (QA) formatting dialogue. Please refer to the *Appendix* for detailed prompts. This straightforward approach enhances the diversity in part categories and attributes. In total, we obtain 306K part mask-region instruction-following samples.

![](../images/Osprey_md_images/figs/framework_v6.pdf.png){width="99.9%"}
**Figure 4.** **Overview of Osprey.** The left shows the overall model architecture and the right illustrates the detailed image encoder and mask-aware visual extractor. With the input image, referring mask regions and input language, the corresponding tokenization can be carried out. The interleaved mask features and language embedding sequence are then transmitted to a large language model (LLM) to achieve the nuanced semantic understanding.

# Robustness and Flexibility
**Robustness.** Previous studies have shown that MLLMs suffer from the object hallucination issue [@li2023evaluating]. That is, objects that frequently appear in visual instructions or co-occur with other objects are susceptible to being erroneously hallucinated. To bolster the robustness of MLLM for accurate region understanding, we further construct positive/negative instruction samples. In specific, we formulate queries to inquire whether a given region belongs to a particular category, and anticipate responses with "`Yes/No`\". The positive/negative samples are devised equally to ensure balance.

Negative sample mining intends to find spatial-aware and class-aware negative samples. The former enables the model to identify object-specific categories spatially nearest to a given object. For the latter, negative categories are selected based on high semantic similarities to the target class name, where SentenceBert [@reimers2019sentence] is employed to calculate the semantic similarity. Empirically, one category is randomly chosen from the top-8 semantically similar candidates to enhance diversity of the negative categories. We apply this scheme to LVIS [@gupta2019lvis], a large-vocabulary dataset containing around 1,200 object categories with mask annotations.

**Flexibility.** To improve the response flexibility of MLLMs based on user's instructions, we add the short-form response instructions, covering categories, colors, types, locations or quantities of a specific object region. We employ GPT-4 to generate the instruction samples using the same publicly available datasets as discussed in Sec. [3.1](#object-level), expecting that GPT-4 can produce a concise response consisting of a single word or phrase.

However, we observe that conventional dialogue-based prompts do not explicitly indicate the desirable output format, potentially resulting in the overfitting of an LLM to short-form answers. This issue has been acknowledged in previous works [@Instructblip; @liu2023improved] on image-level understanding. To tackle this challenge, we adopt to append the short-form response prompt explicitly at the end of questions when soliciting brief answers.

# Method of Osprey {#sec:method}

# Model Architecture
The architecture overview of Osprey is shown in Figure 4. Osprey consists of an image-level vision encoder, a pixel-level mask-aware visual extractor and a large language model (LLM). Given an image, the referring mask regions and the input language, we perform tokenization and conversion to obtain embeddings. The interleaved mask features and language embedding sequences are then sent to the LLM to obtain the fine-grained semantic understandings.

# Convolutional CLIP Vision Encoder
The vision encoder in the majority of MLLMs [@llava; @zhu2023minigpt; @zhang2023gpt4roi; @chen2023shikra; @you2023ferret] is exemplified with the ViT-based CLIP model [@radford2021learning; @dosovitskiy2020image], which adopts an image resolution of 224$\times$`<!-- -->`{=html}224 or 336$\times$`<!-- -->`{=html}336. However, such a resolution makes it difficult to achieve fine-grained image understanding with pixel-level representations, especially in small regions. Increasing the input image resolution is hindered by the computational burden associated with the global attention in ViT architecture.

To alleviate the above issue, we introduce the convolutional CLIP model, *e.g.*, ResNet [@he2016deep] and ConvNeXt [@liu2022convnet], as the vision encoder. The CNN-based convolutional CLIP has empirically demonstrated promising generalization capabilities across various input resolutions compared to ViT-based CLIP model, for example, in the open-vocabulary segmentation tasks [@yu2023convolutions]. Such a design allows for efficient training and fast inference without sacrificing performance. Additionally, multi-scale feature maps generated by the CNN-based CLIP vision encoder can be directly utilized for the subsequent feature extraction on each object region. In our implementation, we choose the ConvNeXt-Large CLIP model as the vision encoder and adopt the output at "res4" stage as the image-level features.

<a id="mask-sampler"></a>
# Mask-Aware Visual Extractor {#mask-sampler} In contrast to previous region-based approaches [@zhang2023gpt4roi; @peng2023kosmos; @chen2023position; @chen2023shikra; @rasheed2023glamm] using sparse bounding boxes as the referring input, Osprey adopts the fine-grained representations using detailed mask regions. To capture pixel-level features of each object region, we propose a Mask-Aware Visual Extractor, which not only encodes the mask-level visual features but also gathers the spatial position information of each region $\mathbf{R}_{i}$. To this end, we first adopt the mask-pooling operation $\mathcal{MP}$ [@xu2023open] based on multi-level image features $\mathbf{Z}(x)$ from the output of the vision encoder $\mathbf{Z}$. For each single-level feature $\mathbf{Z}(x)_j$, we pool all the features that fall inside the mask region $\mathbf{R}_{i}$ as follows: $$\begin{equation}
{V_{ij}} = \mathcal{MP}({\mathbf{R}_{i}}, \mathbf{Z}(x)_{j}).
\end{equation}$$ Then, to encode the features across multiple levels, we pass each feature $V_{ij}$ through a linear projection layer $\mathbf{P}_j$ to generate the region-level embeddings with the same dimension, and perform summation to fuse multi-level features. We further employ an MLP layer $\sigma$ to adapt and produce the visual mask token ${t}_i$ as follows: $$\begin{equation} {t_i} = \sigma (\sum\limits_{j=1}^4 {\mathbf{P}_j ({V_{ij}})}).
\end{equation}$$ To preserve the spatial geometry of the object region, we utilize the binary mask ${\mathbf{M}^{H\times W}} \in \{ 0,1\}$ for each object region to encode the pixel-level position relationship. We first resize each $\mathbf{M}_i$ to 224$\times$`<!-- -->`{=html}224, and then flatten and project it to generate the spatial token ${s_i}$. Finally, we incorporate the visual mask token and its corresponding spatial token as the embeddings for each mask region.

# Tokenization for LLM Model
As illustrated in Figure 4, we feed the image into a pre-trained visual encoder, ConvNeXt-Large CLIP model, to extract the image-level embeddings. For textual information, we tokenize the text sequence using the pre-trained LLM's tokenizer and project them into text embeddings. As for mask-based region, we define a special token as a placeholder `<region>`, which is substituted with the mask token $t$ along with spatial token $s$, denoted by `<mask>` `<position>`. When referring to an object region in the text input, the `<region>` is appended after its region name, like "`region1`\" or "`region2`\".

In this way, the mask regions can be well mixed with texts to form complete sentences with the same tokenization space. In addition to the user instructions, we incorporate a prefix prompt: "`<image>`$\backslash$`n This provides an overview of the picture.`\" The `<image>` is a special token that acts as a placeholder, which would be replaced by the image-level embedding from the vision encoder. All of image-level and region-level visual tokens and text tokens are interleaved and fed into LLM to comprehend the image and user instructions with different object regions. We employ Vicuna [@chiang2023vicuna], which is a decoder-only LLM instruction-tuned on top of LLaMA [@touvron2023llama], as our LLM.

# Training
The training process of our Osprey model consists of three stages, which are all supervised by minimizing a next-token prediction loss [@llava; @zhu2023minigpt; @zhang2023gpt4roi].

**Stage 1: Image-Text Alignment Pre-training.** With the use of convolutional CLIP vision encoder, *i.e.*, ConvNeXt-Large, we first train the image-level feature and language connector for image-text feature alignment. At this stage, Osprey includes a pre-trained vision encoder, a pretrained LLM and an image-level projector. Following LLaVA-1.5 [@liu2023improved], we adopt an MLP as the vision-language connector to improve the multimodal capabilities of the model. The filtered CC3M data introduced in LLaVA [@liu2023improved] are employed as the training data, and only the image-level projector is trained at this stage. The vision encoder and LLM are frozen.

**Stage 2: Mask-Text Alignment Pre-training.** At this stage, we load the weights trained in Stage 1, and add the Mask-Aware Visual Extractor introduced in Sec. [4.1.2](#mask-sampler) to capture pixel-level region features. Only the Mask-Aware Visual Extractor is trained in this stage to align mask-based region features with language embeddings. We collect short text and pixel-level mask pairs from the publicly available object-level datasets (COCO [@lin2014microsoft], RefCOCO [@refcoco_data], RefCOCO+ [@refcoco_data]) and part-level datasets (Pascal Part [@chen2014detect], Part Imagenet [@he2022partimagenet]), then transform them into instruction-following data to train the model.

**Stage 3: End-to-End Fine-tuning.** At this stage, we keep the vision encoder weights fixed and finetune the image-level projector, mask-based region feature extractor and LLM model of Osprey. We focus on extending the capability of Osprey to accurately follow user instructions and tackle complex pixel-level region understanding tasks. At this stage, we utilize our curated Osprey-724K dataset. Besides, Visual Genome (VG) [@krishna2017visual] and Visual Commonsense Reasoning (VCR) [@vcr_data] datasets are employed to add more multiple region understanding data. The bounding box annotations are available in VG, while mask-based ones are not. Hence, we employ HQ-SAM [@ke2023segment] to generate high-quality masks with the corresponding box prompts for the VG dataset. After this stage, Osprey is capable of understanding the complex scenarios based on the user instructions and pixel-level mask regions.

# Experiments {#sec:experiment}

# Implementation Details
The AdamW [@loshchilov2016sgdr] is used as the optimizer and the cosine annealing scheduler [@loshchilov2017decoupled] is used to adjust learning rate. At the first training stage, we set the batch size to 128 and the learning rate to 1$\times$`<!-- -->`{=html}10$^{-3}$ for one epoch. At the second stage, we decrease the learning rate to 2$\times$`<!-- -->`{=html}10$^{-5}$ with a batch size of 4 and train for two epochs. At the final stage, the learning rate is further reduced to 1$\times$`<!-- -->`{=html}10$^{-5}$ with a batch size of 4 for two epochs.

The maximum length of sequence in LLM is set to 2,048. All training is conducted on four NVIDIA A100 GPUs with 80GB memory. We leverage the DeepSpeed framework [@deepspeed] for efficient large-scale model training. The training of the three stages costs 7, 15, and 48 hours, respectively. The input image size is set to 512 $\times$ 512. All the training datasets are aggregated into a single dataloader to ensure the representational integrity. In the training process, the image and its corresponding mask-based instruction/response pairs are randomly selected from each dataset.

# Experimental Results
To evaluate the effectiveness of our proposed Osprey, we conduct experiments to demonstrate its capabilities of pixel-level region-based recognition, classification, and complex description&reasoning across various representative tasks. Figure 5 shows some visual examples to better illustrate the effectiveness of Osprey. In Figure 6, visual results are showcased based on the mask regions obtained from the off-the-self SAM [@kirillov2023segment] in "segment everything\" mode.

# Open-Vocabulary Segmentation The primary goal of this task is to generate mask-based region recognition with the explicit category [@ding2023open_ICML; @xu2023open; @yu2023convolutions]. To this end, we utilize a prompt like "`Can you give me a short description of <region>? Using a short phrase.`" The ground-truth (GT) mask regions are adopted for model inference to assess the open-vocabulary recognition performance. Based on the sentence-based response of MLLMs, we calculate the semantic similarity between the output and vocabulary list of each dataset using Sentence-BERT [@reimers2019sentence]. The category with the highest similarity is chosen as the final result.

**Table 2.** Recognition performance on open-vocabulary panoptic segmentation (PQ), instance segmentation (AP) and semantic segmentation (mIoU) upon the validation sets of Cityscapes and ADE20K-150. The ground truth box/mask is used for performance evaluation.

| Method | Type | Cityscapes PQ | Cityscapes AP | Cityscapes mIoU | ADE20K-150 PQ | ADE20K-150 AP | ADE20K-150 mIoU |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP-ConvNeXt-L | Mask | 22.53 | 12.07 | 23.06 | 36.86 | 39.38 | 28.74 |
| CLIP-Surgery-ViT-L | Mask | 27.24 | 28.35 | 21.92 | 26.55 | 29.70 | 21.42 |
| Kosmos-2 | Box | 12.09 | 9.81 | 13.71 | 6.53 | 4.33 | 5.40 |
| Shikra-7B | Box | 17.80 | 11.53 | 17.77 | 27.52 | 20.35 | 18.24 |
| GPT4RoI-7B | Box | 34.70 | 21.93 | 36.73 | 36.32 | 26.08 | 25.82 |
| Ferret-7B | Mask | 35.57 | 26.94 | 38.40 | 39.46 | 29.93 | **31.77** |
| **Osprey-7B (Ours)** | Mask | **50.64** | **29.17** | **49.78** | **41.89** | **41.24** | 29.63 |

Table 2 compares Osprey with state-of-the-art region-based MLLM methods on Cityscapes [@cordts2016cityscapes] and ADE20K-150 [@zhou2017scene] datasets. Most of these approaches employ the GT bounding box as the input referring region. As Ferret [@you2023ferret] can support free-form input, we adopt the fine-grained mask as its input region to precisely reflect the object. Besides, we leverage the large-scale pretrained vision-language model CLIP [@radford2021learning] with ConvNeXt-L [@liu2022convnet] and CLIP-Surgery-ViT-L [@li2023clip] as vision encoder, and adopt the input mask region and mask-pooling operation [@xu2023open] to extract visual features for each object. The input image resolution of these CLIP-based methods is set to 512$\times$`<!-- -->`{=html}512, ensuring a fair comparison. On Cityscapes, our Osprey surpasses previous methods by a large margin (*e.g.*, +15.94% PQ, +7.24% AP and +13.05% mIoU against box-level GPT4RoI, +15.07% PQ, +2.23% AP and +11.38% mIoU against mask-level Ferret). On ADE20K-150, Osprey achieves highly competitive performance, obtaining 41.89% PQ, 41.24% AP and 29.63% mIoU, respectively.

# Referring Object Classification In this task, the model needs to classify the object in a specific region of an image. We use two semantic relevance metrics, *Semantic Similarity* (SS) and *Semantic IoU* (S-IOU) [@conti2023vocabulary], to evaluate the classification capability of a model. SS measures the similarity of predicted/GT labels in a semantic space, while S-IOU reflects the overlap of words. We conduct experiments on the validation set of object-level LVIS [@gupta2019lvis] and part-level PACO [@ramanathan2023paco] datasets, and use a prompt like "`What is the category of <region>? Using only one word or phrase.`" Specifically, we randomly sample 1K images with 4,004 objects from LVIS dataset, and sample 1K images with 4,263 objects from PACO dataset for evaluation.

**Table 3.** Semantic similarity and IoU results of referring object classification on *object-level* LVIS and *part-level* PACO. SS/S-IoU denotes Semantic Similarity/IoU, respectively.

| Method | LVIS SS | LVIS S-IoU | PACO SS | PACO S-IoU |
| --- | ---: | ---: | ---: | ---: |
| LLaVA-1.5 | 48.95 | 19.81 | 42.20 | 14.56 |
| Kosmos-2 | 38.95 | 8.67 | 32.09 | 4.79 |
| Shikra-7B | 49.65 | 19.82 | 43.64 | 11.42 |
| GPT4RoI-7B | 51.32 | 11.99 | 48.04 | 12.08 |
| Ferret-7B | 63.78 | 36.57 | 58.68 | 25.96 |
| **Osprey-7B (Ours)** | **65.24** | **38.19** | **73.06** | **52.72** |

We compare our method with image-, box- and mask-level approaches [@liu2023improved; @peng2023kosmos; @chen2023shikra; @zhang2023gpt4roi; @you2023ferret], and report the results in Table 3. As for image-level LLaVA-1.5 [@liu2023improved], we adopt the box-based cropped image region as its input. On LVIS [@gupta2019lvis], which has more than 1,200 object categories, our Osprey obtains 65.24% SS and 38.19% S-IoU, outperforming the state-of-the-art method by 1.46% and 1.62%, respectively. In particular, Osprey significantly outperforms previous MLLMs on PACO, achieving 73.06% SS and 52.72% S-IoU. It surpasses Ferret by 14.38% SS and 26.76% S-IoU, demonstrating its strong fine-grained part-level classification and understanding capability.

![](../images/Osprey_md_images/figs/referring_vis.pdf.png){width="96.0%"}
**Figure 5.** Visual examples of Osprey on the input mask-based referring regions.

# Referring Description and Reasoning
**Detailed Description.** We evaluate the instruction-following detailed description capabilities of each model. The input prompt for inference is selected randomly from the detailed-description instruction list in the appendix. Motivated by [@llava], we leverage GPT-4 to comprehensively measure the quality of generated responses from the model to the input referring regions. Specifically, we randomly sample 80 images from the validation set of RefCOCOs [@refcoco_data; @refcoco_g] for detailed region description. We generate the questions and obtain GPT-4's answers using the instruction generation pipeline outlined in Sec. [3.1](#object-level). GPT-4 assesses both the precision of referring understanding and the correctness of semantics. The rating score ranges from 1 to 10, with higher scores indicating better performance.

To gauge the effectiveness of MLLMs, we calculate the ratio of the predicted answer score to that of GPT-4 and present it as a percentage.

**Table 4.** Detailed region description performance evaluated by GPT-4 on the validation set of RefCOCOs. `*` denotes the model trained with an additional part of the 665K data mixture used in LLaVA-1.5 in Stage 3.

| Method | Detailed Description |
| --- | ---: |
| LLaVA-1.5 | 71.11 |
| Kosmos-2 | 40.89 |
| Shikra-7B | 40.97 |
| GPT4RoI-7B | 49.97 |
| Osprey-7B (Ours) | 77.54 |
| **Osprey-7B* (Ours)** | **83.78** |

As shown in Table 4, Osprey achieves 77.54% accuracy, significantly outperforming GPT4RoI by 27.57%. It is worth mentioning that we adopt the box-cropped region as the image-level input for LLaVA-1.5, which yields an accuracy of 71.11%, more than 6% lower than Osprey. With the additional image-level data used in LLaVA-1.5, Osprey attains 83.78% accuracy and performs the best.

**Table 5.** Results on Ferret-Bench. We use box as the input region due to the lack of mask annotations on Ferret-Bench.

| Ferret-Bench | Osprey-7B* | Ferret-7B | Kosmos-2 | Shikra-7B |
| --- | ---: | ---: | ---: | ---: |
| Referring Description | **72.2** | 68.7 | 51.8 | 46.0 |
| Referring Reasoning | **67.8** | 67.3 | 33.7 | 41.6 |

**Ferret-Bench.** We further conduct experiments on Ferret-Bench [@you2023ferret] to evaluate the capabilities of both referring description and referring reasoning. Notably, we adopt box as the input region due to the lack of mask annotations on Ferret-Bench. Results are summarized in Table 5. One can see that Osprey-Chat achieves the best performance in both Referring Description and Referring Reasoning tasks with accuracy of 72.2% and 67.8%, outperforming the state-of-the-art method by 3.5% and 0.5%, respectively.

**Table 6.** Results on the object hallucination benchmark across three evaluation settings of the POPE benchmark.

| Sampling | Metric | Osprey-7B* | Ferret-7B | Shikra-7B | LLaVA-1.5 | InstructBLIP | MiniGPT4 | MM-GPT | mPLUG-Owl |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Random | Accuracy | 89.47 | **90.24** | 86.90 | 88.73 | 88.57 | 79.67 | 50.10 | 53.97 |
| Random | Precision | 93.40 | 97.72 | 94.40 | 88.89 | 84.09 | 78.24 | 50.05 | 52.07 |
| Random | Recall | 84.93 | 83.00 | 79.26 | 88.53 | 95.13 | 82.20 | 100.00 | 99.60 |
| Random | F1 Score | 88.97 | 89.76 | 86.19 | 88.71 | 89.27 | 80.17 | 66.71 | 68.39 |
| Random | Yes (%) | 45.47 | 43.78 | 43.26 | 49.80 | 56.57 | 52.53 | 99.90 | 95.63 |
| Popular | Accuracy | **87.83** | 84.90 | 83.97 | 85.83 | 82.77 | 69.73 | 50.00 | 50.90 |
| Popular | Precision | 89.94 | 88.24 | 87.55 | 83.91 | 76.27 | 65.86 | 50.00 | 50.46 |
| Popular | Recall | 85.20 | 80.53 | 79.20 | 88.67 | 95.13 | 81.93 | 100.00 | 99.40 |
| Popular | F1 Score | 87.50 | 84.21 | 83.16 | 86.22 | 84.66 | 73.02 | 66.67 | 66.94 |
| Popular | Yes (%) | 47.37 | 45.63 | 45.23 | 52.83 | 62.37 | 62.20 | 100.00 | 98.57 |
| Adversarial | Accuracy | **85.33** | 82.36 | 83.10 | 72.10 | 65.17 | 79.20 | 50.00 | 50.67 |
| Adversarial | Precision | 85.43 | 83.60 | 85.60 | 74.69 | 65.13 | 61.19 | 50.00 | 50.34 |
| Adversarial | Recall | 85.20 | 80.53 | 79.60 | 88.34 | 95.13 | 82.93 | 100.00 | 99.33 |
| Adversarial | F1 Score | 85.31 | 82.00 | 82.49 | 80.94 | 77.32 | 70.42 | 66.67 | 66.82 |
| Adversarial | Yes (%) | 49.87 | 48.18 | 46.50 | 59.14 | 73.03 | 67.77 | 100.00 | 98.67 |

As shown in Table 6, Osprey remains competitive on random sampling and surpasses prior methods under the more challenging popular and adversarial settings.

**Table 7.** Region captioning performance evaluated on the validation set of RefCOCOg.

| Method | Type | METEOR | CIDEr |
| --- | --- | ---: | ---: |
| GRIT | Box | 15.2 | 71.6 |
| Kosmos-2 | Box | 14.1 | 62.3 |
| GLaMM | Box | 16.2 | 105.0 |
| **Osprey-7B (Ours)** | Mask | **16.6** | **108.3** |

Table 7 shows that Osprey achieves the best METEOR and CIDEr scores among the compared region captioning methods.

**Table 8.** Comparisons with various vision encoders on open-vocabulary segmentation and referring object classification.

| Method | Cityscapes PQ | ADE PQ | LVIS SS | LVIS S-IoU | PACO SS | PACO S-IoU |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ViT-L | 38.58 | 38.86 | 60.89 | 31.02 | 70.23 | 48.57 |
| ConvNeXt-B | 48.49 | 41.94 | 64.52 | 37.02 | 72.86 | 51.62 |
| **ConvNeXt-L** | **50.64** | **42.50** | **65.24** | **38.19** | **73.06** | **52.72** |

Table 8 reports that the ConvNeXt-L backbone yields the strongest overall performance across both segmentation and referring classification tasks.

![](../images/Osprey_md_images/figs/sam_vis_5.pdf.png){width="97.0%"}
**Figure 6.** Visual results of Osprey based on the class-agnostic masks from off-the-self SAM. With the pixel-level mask regions and task-specific prompts, the semantic understanding results are obtained, including (a) open-vocabulary categories, (b) short descriptions, and (c) detailed descriptions. Zoom-in for better view.

**Table 9.** Comparisons across various input image sizes of ConvNeXt-based CLIP vision encoder on LVIS. Speed is measured by the number of input mask-text pairs processed per second during model inference.

| Input | #Image Tokens | Speed | SS | S-IoU |
| --- | ---: | ---: | ---: | ---: |
| 224 | 196 | **6.0** | 53.20 | 26.12 |
| 336 | 441 | 5.8 | 56.70 | 28.90 |
| 512 | 1024 | 3.5 | 65.24 | 38.19 |
| 800 | 2500 | 1.9 | **68.29** | **42.66** |

**Various Input Image Sizes.** We extend to explore the influence of varying input sizes on our ConvNeXt-based CLIP vision encoder in Osprey. Table 9 presents the experimental results on the referring object classification task. The results demonstrate that Osprey exhibits superior performance as the input size increases. Specifically, when the input size is set to 800$\times$`<!-- -->`{=html}800, Osprey attains its peak performance with 68.29% SS and 42.66% S-IoU. However, it is noteworthy that as the input size increases, the number of tokens also rises significantly, adding computational overhead to LLM. With the input size of 800$\times$`<!-- -->`{=html}800, the number of image tokens is 2,500 and 1.9 mask-text pairs are processed per second during inference, representing the slowest speed among the evaluated models. To strike a balance between performance and computational cost, we have opted for a 512$\times$`<!-- -->`{=html}512 input image size in Osprey.

# Conclusion
In this paper, we presented Osprey, a novel approach to incorporate pixel-level mask region references into language instructions, significantly enhancing MLLMs for fine-grained visual understanding. By incorporating a Mask-Aware Visual Extractor and leveraging a convolutional CLIP backbone, we enabled Osprey the capability of region-based image understanding. To facilitate the fine-grained pixel-level alignment between vision and language, we deliberately curated the Osprey-724K dataset, which comprised 724K mask-based region-text pairs.

Trained on the Osprey-724K dataset, our Osprey model demonstrated superior performance on various region understanding tasks, setting new state-of-the-arts. It is expected that our Osprey-724K dataset and Osprey model can facilitate the advancement of MLLMs for visual region understanding in real-world applications.

# Acknowledgments {#acknowledgments .unnumbered} This work is supported by National Natural Science Foundation of China under Grants (62376244).

# Appendix {#appendix .unnumbered}

# More Experiments

## Additional Main Results
**Effectiveness of Osprey-724K.** To validate the effectiveness of Osprey-724K dataset, we retrain the GPT4ROI model [@zhang2023gpt4roi] and conduct experiments on open-vocabulary segmentation, referring object classification and detailed region description tasks. The results are presented in Table 10. It can be seen that the re-trained GPT4RoI model with Osprey-724K significantly outperforms the original one, especially on part-level region classification and Detailed Description tasks, where we observe impressive improvement of +20.89% SS and +15.33%. These results underscore the superior quality of our Osprey-724K dataset.

<a id="tab:gpt4roi"></a>
**Table 10.** Performance comparison between the original GPT4RoI model and the re-trained one with Osprey-724K.

| GPT4RoI | Cityscapes PQ | ADE PQ | LVIS SS | LVIS S-IoU | PACO SS | PACO S-IoU | Detailed Description |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Original | 34.70 | 36.32 | 51.32 | 11.99 | 48.04 | 12.08 | 49.97 |
| **Re-trained** | **37.31** | **38.12** | **58.91** | **29.56** | **68.93** | **46.28** | **65.30** |

## More Ablation Studies
### Single-level vs. Multi-level Mask Features
To explore the effects of multi-scale features in Mask-Aware Visual Extractor, we carry out experiments on open-vocabulary segmentation and referring object classification tasks. A comparison between single-level and multi-level features is performed. We utilize the output of the vision encoder at the `res4` stage to represent single-level features. As shown in Table 11, multi-level mask features in Osprey significantly outperform single-level mask features in model training.

<a id="tab:single_vs_multi"></a>
**Table 11.** Comparison between single-level and multi-level mask features in Osprey model training.

| Method | Cityscapes PQ | ADE PQ | LVIS SS | LVIS S-IoU | PACO SS | PACO S-IoU |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Single-level | 46.28 | 38.03 | 62.46 | 34.25 | 68.42 | 46.38 |
| **Multi-level** | **50.64** | **42.50** | **65.24** | **38.19** | **73.06** | **52.72** |

### Comparisons on Vision Encoders
To investigate the impact of ViT-based and ConvNeXt-based CLIP vision encoders across varying input sizes, we conduct experiments on open-vocabulary panoptic segmentation using ViT-Surgery-L [@li2023clip] and ConvNeXt-L [@liu2022convnet] models. All experimental results are obtained by directly employing CLIP as a mask classifier with ground truth masks. Table 12 reports the comparison results.

<a id="tab:vit_convnext"></a>
**Table 12.** Panoptic segmentation comparisons (PQ) using different vision encoders with different input sizes on ADE20K-150. The ground truth mask is used for evaluation.

| CLIP Vision Encoder | 224 | 448 | 672 | 896 | 1120 |
| --- | ---: | ---: | ---: | ---: | ---: |
| ViT-Surgery-L | **26.52** | 28.15 | 27.26 | 25.18 | 24.61 |
| **ConvNeXt-L** | 23.35 | **34.36** | **40.57** | **43.04** | **43.33** |

### Impacts of Short-form Prompt and Positive/Negative Data
We conduct experiments to evaluate the impacts of short-form prompt and positive/negative samples on our Osprey-724K dataset. As depicted in Table 13, Osprey trained with both short-form prompt and positive/negative samples attains 65.24% SS and 38.19% S-IoU on the object-level LVIS dataset, bringing an improvement of +8.83% and +12.54% over the model trained without short-form prompt data. On the part-level PACO dataset, the Osprey model trained with only short-form prompt achieves +22.80% SS and +29.43% S-IoU improvements over that without short-form prompt. Regarding the inclusion of positive/negative samples, Osprey trained with them attains +1.69% SS and +1.49% S-IoU over the model trained without them on object-level LVIS. On part-level PACO, +1.47% SS and +2.33% S-IoU improvements are obtained.

<a id="tab:robustness"></a>
**Table 13.** Performance comparisons with and without short-form prompt and positive/negative samples on *object-level* LVIS and *part-level* PACO.

| Method | LVIS SS | LVIS S-IoU | PACO SS | PACO S-IoU |
| --- | ---: | ---: | ---: | ---: |
| w/o Short-form | 56.41 | 25.65 | 50.26 | 23.29 |
| w/o Pos./Neg. | 63.55 | 36.70 | 71.59 | 50.39 |
| **Osprey-724K** | **65.24** | **38.19** | **73.06** | **52.72** |

## More Qualitative Results
We present additional visual examples to highlight the pixel-level semantic understanding performance with the input referring mask-based regions. Figure 7 displays more visual cases involving unusual scenes, such as the "catcher's face mask", "bottle cap", "ladder step", and "rim of a plate". Osprey is capable of generating accurate semantic predictions with robust capabilities in these challenging scenarios.

![](../images/Osprey_md_images/figs/more_vis_6.pdf.png){width="99.0%"}
**Figure 7.** Visual examples of Osprey on the input mask-based referring regions.

## More Details of Osprey-724K
### Example Illustrations
We provide several examples to illustrate the instruction-following data in our Osprey-724K dataset, including the object-level and short-form response instruction-following data in Table 14, the part-level instruction-following data in Table 15, and the robustness data in Table 16.

<a id="tab:object_example"></a>
**Table 14.** One example illustrating the **object-level and short-form response instruction-following data** in Osprey-724K. The reference image is shown below; the top blocks are the contexts used to prompt GPT-4, and the bottom blocks are three response types.

![](../images/Osprey_md_images/figs/example_pic.png)

#### Context type 1: Image-level description
The image presents a lively market scene with a group of people buying fruits and bags. There are multiple individuals in the market, all browsing through the fresh produce available. A significant variety of fruits are showcased in the market, including bananas, oranges, and apples. Bananas can be seen in several groups, with some green and yellow bananas occupying different areas of the market. Meanwhile, oranges and apples are displayed in smaller sections among the fruits. In addition to fruits, handbags are also being sold at the market, attracting the attention of the customers. Overall, the market bustles with activity as people gather around the fresh fruits and bags, contemplating their purchases.

#### Context type 2: Boxes
- `person: [0.507,0.409,0.698,0.740]`
- `person: [0.243,0.496,0.558,0.746]`
- `person: [0.196,0.422,0.395,0.708]`
- `orange: [0.761,0.537,0.820,0.569]`
- `orange: [0.809,0.553,0.841,0.570]`
- `orange: [0.841,0.552,0.868,0.571]`
- `banana: [0.671,0.814,0.770,0.887]`
- `banana: [0.599,0.703,0.820,0.817]`
- `banana: [0.885,0.829,0.941,0.893]`
- `apple: [0.811,0.584,0.851,0.603]`
- `apple: [0.873,0.568,0.900,0.586]`
- `apple: [0.778,0.580,0.819,0.601]`
- `handbag: [0.473,0.110,0.607,0.201]`
- `handbag: [0.491,0.202,0.611,0.267]`
- `handbag: [0.583,0.105,0.696,0.204]`

#### Context type 3: Mask region captions
- `<region1>` `(person: [0.507,0.409,0.698,0.740])`: gray shirt wearing glasses; woman with gray shirt standing next to man; woman in gray shirt facing camera on right; the woman in the grey shirt with a watch on her wrist; a short haired woman in jeans shopping.
- `<region2>` `(person: [0.243,0.469,0.558,0.746])`: the lady with the blue shirt; the back of an older woman with her hair in a barrette with a blue jacket on; navy blue shirt; woman back in blue; a woman is wearing blue sweater.
- `<region3>` `(person: [0.196,0.422,0.395,0.708])`: a woman in glasses shops in an open air fruit market; a woman in a gray coat and scarf.

#### Response type 1: mask region description
- `<region1>`: In another part of the market, a short-haired woman in a gray shirt and jeans is shopping. She seems to be looking directly at camera. A noticeable detail is the watch worn on her wrist. This lady, who is also wearing glasses, is standing next to a man.
- `<region2>`: An older woman is visible, her back facing us. She's donning a navy blue sweater. Her hair, neatly fastened with a barrette, adds a note of detail to her appearance.
- `<region3>`: Another woman, clad in a gray coat and scarf, is seen shopping in the open-air fruit market. This woman, similarly wearing glasses, appears to be engrossed in the selection of fresh produce.

#### Response type 2: conversation
- Question 1: Can you describe the woman in `<region1>` and what she is doing?
  Answer 1: The woman in `<region1>` is wearing a gray shirt, jeans, and glasses. She has short hair and a watch on her wrist. She is shopping in the lively market, browsing through the fresh produce, such as fruits and bags.
- Question 2: What can you tell me about the woman in `<region2>`?
  Answer 2: The woman in `<region2>` is wearing a navy blue shirt or sweater. She has her back towards the camera, with her hair styled in a barrette. She appears to be an older woman, also browsing through the market, looking at the various items for sale.
- Question 3: How would you compare the person in `<region1>` and the person in `<region2>`?
  Answer 3: The person in `<region2>` is positioned on the left side of the image, facing away from the camera. On the other hand, the person in `<region1>` is located more towards the center-right of the image, facing the camera. Both individuals are wearing different colored shirts, with the person in `<region2>` wearing a blue shirt and the person in `<region1>` wearing a gray shirt.
- Question 4: Is there anything notable about the person in `<region3>`?
  Answer 4: The person in `<region3>` is described as a woman wearing a gray coat and scarf. They are wearing glasses and seem to be shopping in the open-air fruit market, providing an indication of the bustling activity taking place in the scene.
- Question 5: Based on the image, how would you describe the overall atmosphere of the market?
  Answer 5: The market has a bustling and lively atmosphere. There's a sense of excitement and energy as people gather around the fresh fruits and bags for sale. The variety of items available, as well as the interactions among customers, contribute to the vibrant ambience of the market scene.

#### Response type 3: short-form response
- Question 1: What color is the shirt of the woman in `<region1>`? Answer 1: Gray.
- Question 2: What accessories does the woman in `<region1>` wear? Answer 2: Glasses.
- Question 3: What color is the woman's sweater in `<region2>`? Answer 3: Blue.
- Question 4: What is the woman in `<region2>` wearing on her head? Answer 4: Barrette.
- Question 5: How is the woman in `<region3>` dressed? Answer 5: In a gray coat and scarf.
- Question 6: What type of market is shown in the image? Answer 6: Fruit market.

<a id="tab:part_example"></a>
**Table 15.** One example illustrating the **part-level instruction-following data** in Osprey-724K. The top block shows the attributes of each mask region used to prompt GPT-4, and the bottom block shows representative question-answer pairs.

![](../images/Osprey_md_images/figs/paco_example.jpg)
![](../images/Osprey_md_images/figs/spoon_thing_w.png)
![](../images/Osprey_md_images/figs/spoon_part_w.png)

#### Context
- `<region1>` spoon: dark grey, plain, metal, opaque
- `<region2>` bowl: dark green, plain, ceramic, opaque
- `<region3>` spoon:tip: dark grey, plain, metal, opaque
- `<region4>` spoon:bowl: light grey, plain, metal, opaque
- `<region5>` spoon:neck: dark grey, plain, metal, opaque
- `<region6>` spoon:handle: dark grey, plain, metal, opaque
- `<region7>` bowl:inner body: dark green, plain, ceramic, opaque
- `<region8>` bowl:rim: dark green, plain, ceramic, opaque

#### Response type
- Question: What's in `<region1>`? Answer: Spoon.
- Question: What is the color of `<region2>`? Answer: Dark green.
- Question: Tell me about the color of the tip of spoon in `<region3>`. Answer: Dark grey.
- Question: What's the category of `<region4>`? Answer: Bowl of a spoon.
- Question: What is the color of `<region5>`? Answer: Dark grey.
- Question: Is the handle of spoon plain in `<region6>`? Answer: Yes.
- Question: What is the reflectance of `<region7>`? Answer: Opaque.
- Question: What's the material of `<region8>`? Answer: Ceramic.

<a id="tab:robustness_data_example"></a>
**Table 16.** Two examples showing **robustness data** in Osprey-724K based on the categories of LVIS.

#### Example 1
![](../images/Osprey_md_images/figs/lvis1.jpg)

- Ground truth:
  `<region1>`: sock
  `<region2>`: sock
- Question: Is the category of `<region1>` calf?
  Answer: No, it isn't.
- Question: Soccer ball is the category of `<region2>`, right?
  Answer: Not at all.

#### Example 2
![](../images/Osprey_md_images/figs/lvis2.jpg)

- Ground truth:
  `<region1>`: spoon
  `<region2>`: soup
  `<region3>`: soup
- Question: Does this area `<region1>` belong to category fork?
  Answer: This is not so.
- Question: The category of `<region2>` is soup, right?
  Answer: Yes, it is.
- Question: Does the category salad accurately describe this region `<region3>`?
  Answer: No, there is no salad in the region.

### Details on Task Prompt
Different prompt templates are used for training the Osprey model based on different instruction-following data. The question templates are randomly selected from the corresponding lists. Table 17, Table 18, Table 19, and Table 20 show the prompt construction patterns. Table 21, Table 22, and Table 23 list the concrete instruction templates.

<a id="tab:prompt_description"></a>
**Table 17.** The prompt used to generate the **detailed region description** in Osprey-724K.

```text
messages = [
  {
    "role": "system",
    "content": """You are an AI visual assistant that can analyze a single image. You receive a detailed description/several descriptions of this image. In addition, most object locations within the image are given, along with detailed coordinates. These coordinates are in the form of bounding boxes, represented as (x1, y1, x2, y2) with floating numbers ranging from 0 to 1. These values correspond to the top left x, top left y, bottom right x, and bottom right y.

Your role is to give a detailed description of each special region in the image. Instead of directly mentioning the bounding box coordinates, utilize this data to explain each region using natural language. Include details like object category, object type, object color, attributes of the object, object locations, object state and other attributes.

When using the information from the image and object region captions and coordinates, directly explain the region, and do not mention that the information source is the caption or the bounding box. Always answer as if you are directly looking at each region. Provide a direct answer without mentioning "this region". The answer template is: "<region1>: ..." """
  }
]

for sample in fewshot_samples:
  messages.append({"role": "user", "content": sample["context"]})
  messages.append({"role": "assistant", "content": sample["response"]})

messages.append({"role": "user", "content": "\n".join(query)})
```

<a id="tab:prompt_conversation"></a>
**Table 18.** The prompt used to generate the **conversation response** data in Osprey-724K.

```text
messages = [
  {
    "role": "system",
    "content": """You are an AI visual assistant, and you are seeing several object regions in a single image. What you see are provided with a detailed description for the whole image and each object region in this image, describing you are looking at. Answer all questions as you are seeing the image. The location of each object region is given in the form of bounding boxes, represented as (x1, y1, x2, y2) with floating numbers ranging from 0 to 1.

Design a conversation between you and a person asking about each object region of this image. The answers should be in a tone that a visual AI assistant is seeing the image and answering the question. Ask diverse questions and give corresponding answers. All the regions given should be mentioned in the questions, when referring to each region, use <region1>, <region2>, etc.

Include questions asking about the visual content of each object region in the image, including object category, object type, object color, object actions, object locations, relative positions between objects and other attributes. Only include questions that have definite answers and do not ask about uncertain details. Provide detailed answers when answering complex questions."""
  }
]

for sample in fewshot_samples:
  messages.append({"role": "user", "content": sample["context"]})
  messages.append({"role": "assistant", "content": sample["response"]})

messages.append({"role": "user", "content": "\n".join(query)})
```

<a id="tab:prompt_shortform"></a>
**Table 19.** The prompt used to generate the **short-form response** data in Osprey-724K.

```text
messages = [
  {
    "role": "system",
    "content": """You are an AI visual assistant, and you are seeing several object regions in a single image. What you see are provided with a detailed description for the whole image and each object region in this image, describing you are looking at. Answer all questions as you are seeing the image.

Design a conversation between you and a person asking about each object region of this image. The answers must be in one word or one phrase. Ask diverse questions and give corresponding answers. All the regions given should be mentioned in the questions, when referring to each region, use <region1>, <region2>, etc.

Include questions asking about the visual content of each object region in the image, including object category, object type, object color, object actions, object locations, relative positions between objects and other attributes. Only include questions that have definite answers. Do not ask any question that cannot be answered with one word or phrase.

Most importantly, the answer must be in one word or short phrase."""
  }
]

for sample in fewshot_samples:
  messages.append({"role": "user", "content": sample["context"]})
  messages.append({"role": "assistant", "content": sample["response"]})

messages.append({"role": "user", "content": "\n".join(query)})
```

<a id="tab:prompt_paco"></a>
**Table 20.** The prompt used to generate the **part-level attributes** instruction data in Osprey-724K.

```text
messages = [
  {
    "role": "system",
    "content": """You are an AI visual assistant that can analyze a single image. There are some regions in this image, each region is an object or a part of the object. You receive a short description with some words, separated by commas, for the common attributes of each region, which may contain category name, color, pattern and markings, material and reflectance. If a region is a part of an object, the category name is described as "object:part", like "person:body".

According to each description, design a conversation between you and a person asking about each region of this photo. The answers should be in a tone that a visual AI assistant is seeing the image and answering the question. Ask diverse questions and give corresponding answers.

Include diverse questions asking about the attributes of each region including category, part category, color, pattern and markings, material and reflectance. Each region must involve 1-2 questions, when referring to each region, use <region1>, <region2>, etc. Answer the question using as few words as possible (single or two words). Only include questions that have definite answers."""
  }
]

for sample in fewshot_samples:
  messages.append({"role": "user", "content": sample["context"]})
  messages.append({"role": "assistant", "content": sample["response"]})

messages.append({"role": "user", "content": "\n".join(query)})
```

<a id="tab:concise_describe_instructions"></a>
**Table 21.** The list of instruction templates for detailed mask-region description used in Osprey.

1. "Can you provide me with a detailed description of the region in the picture marked by `<region>`?"
2. "I'm curious about the region represented by `<region>` in the picture. Could you describe it in detail?"
3. "What can you tell me about the region indicated by `<region>` in the image?"
4. "I'd like to know more about the area in the photo labeled `<region>`. Can you give me a detailed description?"
5. "Could you describe the region shown as `<region>` in the picture in great detail?"
6. "What details can you give me about the region outlined by `<region>` in the photo?"
7. "Please provide me with a comprehensive description of the region marked with `<region>` in the image."
8. "Can you give me a detailed account of the region labeled as `<region>` in the picture?"
9. "I'm interested in learning more about the region represented by `<region>` in the photo. Can you describe it in detail?"
10. "What is the region outlined by `<region>` in the picture like, please? Could you give me a detailed description?"
11. "Please describe the region `<region>` in the image in detail."
12. "Can you offer a thorough analysis of the region `<region>` in the image?"
13. "Could you elaborate on the region highlighted by `<region>` in the picture provided?"
14. "Please share more information about the zone emphasized with `<region>` in the photo."
15. "Can you share a comprehensive rundown of the region denoted by `<region>` in the presented image?"
16. "I'd like to know more about the region highlighted by `<region>` in the picture provided."
17. "Work through the important details of the area `<region>` in the image."
18. "Illustrate the area represented by `<region>` through a descriptive explanation."
19. "Examine the region `<region>` closely and share its details."

<a id="tab:brief_describe_instructions"></a>
**Table 22.** The list of instruction templates for brief mask-region description used in Osprey.

1. "Please give me a short description of region `<region>`."
2. "Can you give me a short description of `<region>`?"
3. "Can you provide me with a short description of the region in the picture marked by `<region>`?"
4. "I'm curious about the region represented by `<region>` in the picture. Could you describe it in few words?"
5. "What can you tell me about the region indicated by `<region>` in the image in few words?"
6. "I'd like to know more about the area in the photo labeled `<region>`. Can you give me a concise description?"
7. "Could you describe the region shown as `<region>` in the picture concisely?"
8. "Please provide me with a brief description of the region marked with `<region>` in the image."
9. "Can you give me a brief introduction of the region labeled as `<region>` in the picture?"
10. "I'm interested in knowing the region represented by `<region>` in the photo. Can you describe it in several words?"
11. "What is the region outlined by `<region>` in the picture like? Could you give me a streamlined description?"
12. "I'd like to know more about the area in the photo labeled `<region>`. Can you give me a simple description?"
13. "Could you describe the region shown as `<region>` in the picture in several words?"
14. "Please provide me with a simple description of the region marked with `<region>` in the image."
15. "Please describe the region `<region>` in the image concisely."
16. "Can you offer a simple analysis of the region `<region>` in the image?"
17. "Please share some information about the zone emphasized with `<region>` in the photo."
18. "Can you share a simple rundown of the region denoted by `<region>` in the presented image?"
19. "Work through the important attributes of the area `<region>` in the image."

<a id="tab:lvis-instructions"></a>
**Table 23.** The list of instruction templates for the mask-region positive/negative categories used in Osprey.

1. "`<category>` is the category of `<region>`, right?"
2. "Is the category of `<region>` `<category>`?"
3. "Does this area `<region>` belong to category `<category>`?"
4. "Is `<category>` the appropriate classification for this area `<region>`?"
5. "Does category `<category>` accurately describe this region `<region>`?"
6. "The category of `<region>` is `<category>`, right?"
7. "Is this area `<region>` classified under category `<category>`?"
8. "Is it correct to say this area `<region>` falls into category `<category>`?"
9. "Is the classification of this region `<region>` aligned with category `<category>`?"

## Discussion on Types of Input Region
Osprey can handle various input instructions of referring region, including point, box and scribble types, which can be considered as free-form masks. Our Mask-Aware Visual Extractor is compatible with these inputs. Compared to these coarse types, fine-grained masks can more precisely represent objects, achieving pixel-level alignment for accurate semantic understanding. Besides, some efficient SAM-based models, like EfficientSAM [@xiong2023efficientsam] and EdgeSAM [@zhou2023edgesam], have been developed to make the acquisition of masks faster with lower cost. Representative comparisons are shown in Figure 8.

![](../images/Osprey_md_images/figs/compare_1.pdf.png){width="92.0%"}
**Figure 8.** Qualitative comparisons with previous region-level and image-level approaches [@peng2023kosmos; @chen2023shikra; @zhang2023gpt4roi; @liu2023improved]. The same prompt is adopted to obtain the detailed descriptions, which is selected randomly from Table 21. Our method showcases more accurate region-level semantic understanding with fine-grained details.
