# Introduction

Large multimodal models (LMMs) have become increasingly popular in the research community, as they are key building blocks toward general-purpose assistants. Recent studies on LMMs are converging on a central concept known as visual instruction tuning. The results are promising: LLaVA and MiniGPT-4 demonstrate impressive natural instruction-following and visual reasoning capabilities. To better understand the capability of LMMs, multiple benchmarks have been proposed. Recent works further demonstrate improved performance by scaling up the pretraining data, instruction-following data, visual encoders, or language models, respectively. The LLaVA architecture is also leveraged in different downstream tasks and domains, including region-level and pixel-level understanding, biomedical assistants, image generation, and adversarial studies.

![](../images/Visual%20Instruction%20Tuning_md_images/figs/llava_v1_5_radar.pdf.png)
![](../images/Visual%20Instruction%20Tuning_md_images/figs/bar_lmm_training_samples_transposed.pdf.png)
![](../images/Visual%20Instruction%20Tuning_md_images/figs/architecture.png)
**Figure 1.** **LLaVA-1.5** achieves SoTA on a broad range of 11 tasks (top), with high training sample efficiency (left) and simple modifications to LLaVA (right): an MLP connector and academic-task-oriented data with response formatting prompts.

However, despite many benchmarks and developments, it still remains unclear what the best recipe is to train LMMs toward the goal of general-purpose assistants. For example, LLaVA excels in conversational-style visual reasoning and even outperforms later approaches like InstructBLIP on such benchmarks, while InstructBLIP excels in traditional VQA benchmarks that demand single-word or short answers. Given the significant differences in the model architecture and training data between them, the root cause of the disparity in their capabilities remains elusive. To this end, the paper presents a systematic study to investigate the design choices of LMMs in a controlled setting. The study originates from LLaVA and builds a roadmap by carefully making effective contributions from the perspectives of the input, model, and data.

First, the paper shows that the fully connected vision-language connector in LLaVA is surprisingly powerful and data-efficient, and establishes stronger yet more feasible baselines built upon the LLaVA framework. Two simple improvements, namely an MLP cross-modal connector and incorporating academic-task-related data such as VQA, are shown to be orthogonal to the LLaVA framework and jointly lead to better multimodal understanding capabilities. In contrast to InstructBLIP or Qwen-VL, which train specially designed visual resamplers on hundreds of millions or even billions of image-text pairs, LLaVA uses one of the simplest architecture designs for LMMs and requires training only a simple projection layer on merely 600K image-text pairs. The final model finishes training in about one day on a single 8-A100 machine and achieves state-of-the-art results on a wide range of benchmarks, while using only publicly available data.

Next, the paper explores several open problems of large multimodal models. The main findings include: (1) scaling to high-resolution image inputs, where simple image gridding improves detailed perception capabilities and reduces hallucination; (2) compositional capabilities, where training on long-form language reasoning together with shorter visual reasoning improves multimodal writing; (3) data efficiency, where random downsampling of the training mixture by up to 75% does not significantly hurt performance; and (4) data scaling, where the granularity of data and the capability of the model must be balanced to improve performance without introducing artifacts such as hallucination.

In sum, the paper performs a systematic study on training large multimodal models and introduces a simple yet effective approach to balance multitask learning and effective scaling for large multimodal models. The improved baselines, LLaVA-1.5, use only *public* data, achieve state-of-the-art performance on a broad range of 11 tasks, and are significantly more data-efficient than previous approaches.

# Related Work

**Instruction-following large multimodal models (LMMs).** Common architectures include a pre-trained visual backbone to encode visual features, a pre-trained large language model (LLM) to comprehend user instructions and produce responses, and a vision-language cross-modal connector to align the vision encoder outputs to the language model. As shown in Figure 1, LLaVA is perhaps the simplest architecture for LMMs. Optionally, visual resamplers such as QFormer are used to reduce the number of visual patches. Training an instruction-following LMM usually follows a two-stage protocol: vision-language alignment pretraining on image-text pairs, followed by visual instruction tuning on multimodal instruction data.

**Multimodal instruction-following data.** In NLP, studies show that the quality of instruction-following data strongly affects the resulting model. For visual instruction tuning, LLaVA pioneered the use of GPT-4 to expand COCO annotations into multimodal instruction-following data that contains conversational-style QA, detailed description, and complex reasoning. InstructBLIP incorporates academic-task-oriented VQA datasets to further enhance visual capabilities, but prior work also points out that naive data merging can overfit the model to short-answer academic tasks and degrade natural conversation quality.

# Approach

## Preliminaries

As the seminal work of visual instruction tuning, LLaVA showcases commendable proficiency in visual reasoning capabilities and surpasses even more recent models on diverse real-life visual instruction-following tasks. LLaVA uses a single linear layer to project visual features into language space and optimizes the whole LLM for visual instruction tuning. However, LLaVA falls short on academic benchmarks that typically require short-form answers and tends to answer *yes* for yes/no questions due to the lack of such data in the training distribution.

On the other hand, InstructBLIP incorporates academic-task-oriented datasets like VQA-v2 together with LLaVA-Instruct and demonstrates improved performance on VQA benchmarks. It pretrains QFormer on 129M image-text pairs and only finetunes the instruction-aware QFormer for visual instruction tuning. However, recent studies show that it does not perform as well as LLaVA on real-life visual conversation tasks. More specifically, as shown in Table 1, it can overfit to VQA training sets with short answers even on requests that require detailed responses.

## Response Format Prompting

We find that the inability to balance between short- and long-form VQA for approaches like InstructBLIP is mainly due to two factors. First, *ambiguous prompts on the response format* do not clearly indicate the desired output style, which can behaviorally bias the LLM toward short-form answers even for natural conversations. Second, *not finetuning the LLM* makes it harder for the system to learn when to produce short or long outputs, because this burden falls entirely on the smaller visual resampler.

Thus, to enable LLaVA to better handle short-form answers while addressing the issues of InstructBLIP, the paper uses a single response formatting prompt that clearly indicates the output format: *Answer the question using a single word or phrase*. When the LLM is finetuned with such prompts, LLaVA is able to properly adjust the output format according to the user’s instructions, and does not require additional processing of the VQA answers using ChatGPT. As shown in Table 2, merely including VQAv2 in training significantly improves MME performance.

<a id="tab:response_format_example"></a>
**Table 1.** Visual input example to illustrate the challenge of (a) multitask balancing and (b) different format prompts. The same image input is used.

![](../sources/Visual%20Instruction%20Tuning_source/figs/extreme_ironing.jpg)

**(a) Multitask balancing problem.** Example of InstructBLIP (Vicuna-13B) having difficulty balancing between short- and long-form answers.
- User: `Is this unusual? Please explain in detail.`
- InstructBLIP: `yes`

**(b) Different format prompts.** Comparison of how different prompts regularize the output format. The results are obtained zero-shot directly after LLaVA undergoes first-stage vision-language alignment pretraining, without second-stage visual instruction tuning.
- Normal prompt: `What is the color of the shirt that the man is wearing?`
- Response: `The man is wearing a yellow shirt.`
- Ambiguous prompt: `Q: What is the color of the shirt that the man is wearing? A:`
- Response: `The man is wearing a yellow shirt.`
- Formatting prompt: `What is the color of the shirt that the man is wearing? Answer the question using a single word or phrase.`
- Response: `Yellow.`

![](../images/Visual%20Instruction%20Tuning_md_images/figs/high_res_arch_v2.pdf.png)
**Figure 2.** **LLaVA-1.5-HD.** Scaling LLaVA-1.5 to higher resolutions by splitting the image into grids and encoding them independently. This allows the model to scale to any resolution, without performing positional embedding interpolation for ViTs. The model additionally concatenates the feature of a downsampled image to provide the LLM with global context.

Figure 2 illustrates the split-encode-merge design used for LLaVA-1.5-HD.

## Scaling the Data and Model

**MLP vision-language connector.** Improving the vision-language connector’s representation power with a two-layer MLP improves multimodal capability over the original linear projection.

**Academic task oriented data.** The model further includes additional academic-task-oriented VQA datasets for VQA, OCR, and region-level perception. With only a subset of the datasets used by InstructBLIP, LLaVA already surpasses it on all three tracked tasks in Table 2, suggesting LLaVA’s effective design. Adding region-level VQA datasets such as Visual Genome and RefCOCO further improves the model’s capability of localizing fine-grained visual details.

**Additional scaling.** The paper scales up the input image resolution to 336^2, adds GQA as an additional visual knowledge source, incorporates ShareGPT data, and scales up the LLM to 13B. Results on MM-Vet show the most significant improvement when scaling the LLM to 13B, suggesting the importance of the base LLM’s capability for visual conversations.

**LLaVA-1.5.** The final model with all modifications is denoted as LLaVA-1.5 and significantly outperforms the original LLaVA baseline.

**Computational cost.** For LLaVA-1.5, the paper uses the same pretraining dataset and roughly the same training iterations and batch size for instruction tuning as LLaVA. Due to the increased image input resolution to 336^2, LLaVA-1.5 takes about 2x as long as LLaVA: about 6 hours of pretraining and about 20 hours of visual instruction tuning using 8x A100 GPUs.

**Table 2.** **Scaling results** on data, model, and resolution. GQA, MME, and MM-Vet are used to examine short-answer VQA, output formatting, and natural visual conversations, respectively. `*` means GQA training images were observed during training.

| ID | Method change | LLM | Res. | GQA | MME | MM-Vet |
| --- | --- | --- | --- | --- | --- | --- |
| InstructBLIP baseline | InstructBLIP | 14B | 224 | 49.5 | 1212.8 | 25.6 |
| 0 | LLaVA | 7B | 224 | -- | 809.6 | 25.5 |
| 1 | +VQA-v2 | 7B | 224 | 47.0 | 1197.0 | 27.7 |
| 2 | +Format prompt | 7B | 224 | 46.8 | 1323.8 | 26.3 |
| 3 | +MLP VL connector | 7B | 224 | 47.3 | 1355.2 | 27.8 |
| 4 | +OKVQA/OCR | 7B | 224 | 50.0 | 1377.6 | 29.6 |
| 5 | +Region-level VQA | 7B | 224 | 50.3 | 1426.5 | 30.8 |
| 6 | +Scale up resolution | 7B | 336 | 51.4 | 1450.0 | 30.3 |
| 7 | +GQA | 7B | 336 | 62.0* | 1469.2 | 30.7 |
| 8 | +ShareGPT | 7B | 336 | 62.0* | 1510.7 | 31.1 |
| 9 | +Scale up LLM | 13B | 336 | **63.3*** | **1531.3** | **36.1** |

## Scaling to Higher Resolutions

In Section 3.3, the paper observes that scaling up the input image resolution improves model capability. However, the image resolution of existing open-source CLIP vision encoders is limited to 336^2, preventing support for higher resolution images by simply replacing the vision encoder. The paper therefore presents an early exploration of scaling the LMM to higher resolutions while maintaining the data efficiency of LLaVA-1.5.

Instead of positional embedding interpolation and full ViT adaptation, the method divides the image into smaller image patches of the resolution that the vision encoder was originally trained for and encodes them independently. After obtaining the feature maps of individual patches, it merges them into a single large feature map and feeds that into the LLM. To provide the LLM with global context and reduce split-encode-merge artifacts, the feature of a downsampled image is concatenated to the merged feature map. This allows scaling the input to arbitrary resolutions while maintaining the data efficiency of LLaVA-1.5. The resulting model is called LLaVA-1.5-HD.

# Empirical Evaluation

## Benchmarks

LLaVA-1.5 is evaluated on both academic-task-oriented benchmarks and recent benchmarks specifically proposed for instruction-following LMMs, totaling 12 benchmarks. Academic benchmarks include VQA-v2, GQA, VizWiz, ScienceQA-IMG, and TextVQA. More recent instruction-following benchmarks include POPE, MME, MMBench, MMBench-CN, SEED-Bench, LLaVA-Bench-in-the-Wild, and MM-Vet.

Table 3 summarizes the academic-task-oriented benchmark results.

**Table 3.** **Comparison with SoTA methods on academic-task-oriented datasets.** LLaVA-1.5 achieves the best performance on 4/5 benchmarks and ranks second on the other. `*` means the training images or annotations of that dataset were observed during training. `†` means the method includes in-house data that is not publicly accessible.

| Method | LLM | Image size | Pretrain | Finetune | VQAv2 | GQA | VisWiz | SciQA-IMG | TextVQA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BLIP-2 | Vicuna-13B | 224^2 | 129M | - | 65.0 | 41.0 | 19.6 | 61.0 | 42.5 |
| InstructBLIP | Vicuna-7B | 224^2 | 129M | 1.2M | -- | 49.2 | 34.5 | 60.5 | 50.1 |
| InstructBLIP | Vicuna-13B | 224^2 | 129M | 1.2M | -- | 49.5 | 33.4 | 63.1 | 50.7 |
| Shikra | Vicuna-13B | 224^2 | 600K | 5.5M | 77.4* | -- | -- | -- | -- |
| IDEFICS-9B | LLaMA-7B | 224^2 | 353M | 1M | 50.9 | 38.4 | 35.5 | -- | 25.9 |
| IDEFICS-80B | LLaMA-65B | 224^2 | 353M | 1M | 60.0 | 45.2 | 36.0 | -- | 30.9 |
| Qwen-VL | Qwen-7B | 448^2 | 1.4B† | 50M† | 78.8* | 59.3* | 35.2 | 67.1 | **63.8*** |
| Qwen-VL-Chat | Qwen-7B | 448^2 | 1.4B* | 50M† | 78.2* | 57.5* | 38.9 | 68.2 | 61.5* |
| **LLaVA-1.5** | Vicuna-7B | 336^2 | **558K** | **665K** | 78.5* | 62.0* | 50.0 | 66.8 | 58.2 |
| **LLaVA-1.5** | Vicuna-13B | 336^2 | **558K** | **665K** | **80.0*** | **63.3*** | **53.6** | **71.6** | 61.3 |
| **LLaVA-1.5-HD** | Vicuna-13B | 448^2 | **558K** | **665K** | **81.8*** | **64.7*** | **57.5** | 71.0 | 62.5 |
| Specialist SOTA: PaLI-X-55B | -- | -- | -- | -- | 86.1* | 72.1* | 70.9* | -- | 71.4* |

## Results

LLaVA-1.5 achieves the best overall performance on 12 benchmarks despite using much smaller pretraining and instruction-tuning datasets than many competing methods. LLaVA-1.5 significantly outperforms LLaVA on all instruction-following LMM benchmarks. It is also encouraging that LLaVA-1.5 achieves this with one of the simplest architectures, academic-scale compute, and public datasets.

Table 4 summarizes the instruction-following benchmark results.

**Table 4.** **Comparison with SoTA methods on benchmarks for instruction-following LMMs.** LLaVA-1.5 achieves the best overall performance.

| Method | POPE rand | POPE pop | POPE adv | MME | MMBench en | MMBench cn | SEED all | SEED img | SEED vid | LLaVA-Wild | MM-Vet |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BLIP2-14B | **89.6** | 85.5 | 80.9 | 1293.8 | -- | -- | 46.4 | 49.7 | 36.7 | 38.1 | 22.4 |
| InstructBLIP-8B | -- | -- | -- | -- | 36.0 | 23.7 | 53.4 | 58.8 | 38.1 | 60.9 | 26.2 |
| InstructBLIP-14B | 87.7 | 77.0 | 72.0 | 1212.8 | -- | -- | -- | -- | -- | 58.2 | 25.6 |
| Shikra-13B | -- | -- | -- | -- | 58.8 | -- | -- | -- | -- | -- | -- |
| IDEFICS-9B | -- | -- | -- | -- | 48.2 | 25.2 | -- | 44.5 | -- | -- | -- |
| IDEFICS-80B | -- | -- | -- | -- | 54.5 | 38.1 | -- | 53.2 | -- | -- | -- |
| Qwen-VL | -- | -- | -- | -- | 38.2 | 7.4 | 56.3 | 62.3 | 39.1 | -- | -- |
| Qwen-VL-Chat | -- | -- | -- | 1487.5 | 60.6 | 56.7 | 58.2 | 65.4 | 37.8 | -- | -- |
| LLaVA-7B | 76.3 | 72.2 | 70.1 | 809.6 | 38.7 | 36.4 | 33.5 | 37.0 | 23.8 | 62.8 | 25.5 |
| **LLaVA-1.5-7B** | 87.3 | 86.1 | 84.2 | 1510.7 | 64.3 | 58.3 | 58.6 | 66.1 | 37.3 | 65.4 | 31.1 |
| **LLaVA-1.5-13B** | 87.1 | **86.2** | **84.5** | **1531.3** | **67.7** | **63.6** | **61.6** | **68.2** | **42.7** | **72.5** | **36.1** |
| **LLaVA-1.5-13B-HD** | 87.5 | **86.4** | **85.0** | 1500.1 | **68.8** | 61.9 | **62.6** | **70.1** | 41.3 | 72.0 | **39.4** |

<a id="tab:tricky_example"></a>
**Table 5.** LLaVA-1.5 can detect and answer tricky questions when prompted to verify the question.

![](../sources/Visual%20Instruction%20Tuning_source/figs/fig_tricky_waikiki.jpg)
- User: If there are factual errors in the question, point it out; if not, proceed to answering the question. What’s happening in the desert?
- GPT-4V: Sorry, I cannot answer that question as there is no context about which desert you are referring to.
- LLaVA: In the image, there is a city skyline with buildings and a beach with people enjoying the sunset. The scene is set in a desert, which is unusual for a beach setting.
- LLaVA-1.5: There are no deserts in the image. The image features a beach with palm trees, a city skyline, and a large body of water.

<a id="tab:constrait_json"></a>
**Table 6.** LLaVA-1.5 can extract information from the image and answer following the required format, despite a few errors compared with GPT-4V.

![](../sources/Visual%20Instruction%20Tuning_source/figs/ima_cardholder.jpg)
- User: Please read the text in this image and return the information in the following JSON format. If the information is not available in the image, put `"N/A"` instead.
- Required format: `{"class": xxx, "DLN": xxx, "DOB": xxx, "Name": xxx, "Address": xxx, "EXP": xxx, "ISS": xxx, "SEX": xxx, "HGT": xxx, "WGT": xxx, "EYES": xxx, "HAIR": xxx, "DONOR": xxx}`
- GPT-4V: `{"class": "C", "DLN": "1234568", "DOB": "08/31/1977", "Name": "Ima Cardholder", "Address": "2570 24th Street, Anytown, CA 95818", "EXP": "08/31/2014", "ISS": "08/31/2011", "SEX": "F", "HGT": "5-05", "WGT": "125 lbs", "EYES": "BRN", "HAIR": "BRN", "DONOR": "VETERAN"}`
- LLaVA: `{"class": "Driver License", "DLN": "CA123 456 789", "DOB": "01/01/1990", "Name": "Amy", "Address": "Anytown, CA", "EXP": "08/31/2023", "ISS": "Veteran", "SEX": "F", "HGT": "5'5", "WGT": "130", "EYES": "Brown", "HAIR": "Brown", "DONOR": "Unknown"}`
- LLaVA-1.5: `{"class": "C", "DLN": "1132456789", "DOB": "08/23/1971", "Name": "Ima Cardholder", "Address": "Anytown, State, Zip", "EXP": "08/23/2014", "ISS": "California", "SEX": "F", "HGT": "5'5", "WGT": "123", "EYES": "Brown", "HAIR": "Brown", "DONOR": "N/A"}`

**Global context.** For higher resolution, the method pads and resizes the image to a single image of 224^2 and concatenates it with the high-resolution features to provide a global context. Ablation on a 7B model shows that the global context effectively boosts performance on all three validation benchmarks. The corresponding metrics are summarized in Table 7.

<a id="tab:ablation_global_context"></a>
**Table 7.** Ablation on global context.

| Setting | GQA | MME | MM-Vet |
| --- | --- | --- | --- |
| high-res patch only | 62.9 | 1425.8 | 31.9 |
| +global context | 63.8 (+0.9) | 1497.5 (+71.0) | 35.1 (+3.2) |

## Emerging Properties

**Format instruction generalization.** Although LLaVA-1.5 is trained with only a limited number of format instructions, it generalizes to others. VizWiz, for example, requires the model to output `Unanswerable` when the provided content is insufficient. The response format prompt effectively instructs the model to do so, improving from 11.1% to 67.8% on unanswerable questions. Qualitative examples are shown in Table 5 and Table 6.

**Multilingual multimodal capability.** Though LLaVA-1.5 is *not* finetuned for multilingual multimodal instruction following at all, it is still capable of following multilingual instructions. This is partly due to multilingual language instructions in ShareGPT. The paper also reports that LLaVA-1.5 outperforms Qwen-VL-Chat by +7.3% on MMBench-CN, despite not being finetuned on Chinese multimodal instructions.

## Ablation on LLM Choices

Figure 3 visualizes the relative performance of different base LLM choices across benchmarks.

![](../images/Visual%20Instruction%20Tuning_md_images/figs/llava_v1_5_radar_llm_ablate.pdf.png)
**Figure 3.** **Ablation on LLM choices.** Data points represent the relative performance of the best performing variant for each dataset.

The paper studies two families of LLMs and their contribution to the final multimodal capability: LLaMA-based (Vicuna-v1.1, Vicuna-v1.3) and LLaMA-2-based (Vicuna-v1.5, LLaMA-2-Chat). The findings suggest that stronger base language models and instruction-tuned multilingual data both matter for final multimodal performance.

Figure 4 visualizes how performance changes under random subsampling of the training mixture.

![](../images/Visual%20Instruction%20Tuning_md_images/figs/llava_v1_5_radar_data_ablate.pdf.png)
**Figure 4.** **Ablation on data efficiency.** Data points represent the relative performance of the best performing variant for each dataset.

# Open Problems in LMMs

Given the successful scaling of LLaVA-1.5, the paper conducts additional studies on open problems in LMMs using the model design and data mixture of LLaVA-1.5.

## Data Efficiency

Despite the efficiency of LLaVA-1.5 relative to approaches like InstructBLIP, training still roughly doubles compared with the original LLaVA. The paper therefore studies random subsampling of the training mixture with sampling ratios from 0.1 to 0.5. Surprisingly, with only 50% of the samples, the model still maintains more than 98% of full-dataset performance, suggesting room for further improvement in data efficiency.

## Rethinking Hallucination in LMMs

Hallucination is an important issue for both LLMs and LMMs. The paper finds that hallucination in LLaVA-style models is significantly reduced when the input resolution is scaled to higher resolutions such as 448^2. This suggests that some hallucination previously blamed on noisy supervision may instead stem from insufficient perceptual resolution.

## Compositional Capabilities

The paper demonstrates interesting compositional capabilities in LLaVA-1.5: a model trained on a set of tasks independently can generalize to tasks that require combinations of those capabilities without explicit joint training. Additional academic-task-oriented datasets improve the visual groundedness of responses, while ShareGPT improves long-form and multilingual conversation quality.

# Conclusion

In this paper, the authors take a step toward demystifying the design of large multimodal models and propose a simple, effective, and data-efficient baseline, LLaVA-1.5. In addition, they explore open problems in visual instruction tuning, scale LMMs to higher resolutions, and present findings on hallucination and compositional capabilities. These improved and reproducible baselines are intended to serve as a reference for future research in open-source LMMs.

**Limitations.** Despite the promising results demonstrated by LLaVA-1.5, it still has limitations including prolonged training for high-resolution images, lack of multiple-image understanding, limited problem-solving capabilities in certain fields, and occasional hallucination.

**Acknowledgements.** This work was supported in part by NSF CAREER IIS2150012, and by multiple IITP grants funded by the Korea government.

# Appendix

This appendix is organized as follows.
- In Section 7, the paper shows implementation details for LLaVA-1.5-HD, data and prompts, and hyperparameters.
- In Section 8, it presents more qualitative results for response format prompts and compositional capabilities.
- In Section 9, it discusses limitations in more detail.

# Implementation Details

## LLaVA-1.5-HD

### Preprocessing

**Overview.** CLIP-ViT-L-14 (224^2) is used as the base image encoder. The input image is padded and resized to a target resolution, split into 224^2 grids, encoded patch-wise, and merged back into a single feature map. A fixed-resolution image feature is additionally concatenated to provide global context.

**Target resolution selection.** The method supports up to six grids (1x1, 1x2, 1x3, 1x4, 1x5, 1x6, 2x2, 2x3, and transposes), allowing a maximum resolution of 672x448 or 448x672. The selection aims to preserve detail while remaining resource efficient.

**Postprocessing.** The method removes padding-only features, appends row-end tokens to preserve shape information, and flattens the final image feature map before sending it into the language model.

### Training

Since the visual features are computed at the original 224^2 resolution that the vision encoder is trained on, the method does not perform additional pretraining for the visual projectors and instead directly performs visual instruction tuning on higher-resolution images.

## Data

The final training mixture contains VQA, OCR, region-level VQA, visual conversation, and language conversation data. The paper uses several efficiency-oriented preprocessing strategies such as merging QA pairs from the same image, truncating long ShareGPT conversations, augmenting A-OKVQA by choice count, sampling OCRVQA and Visual Genome more selectively, and separating language-only and vision-language batches.

All data splits are concatenated together and sampled with the same probability. The response formatting prompts of the final instruction-following data mixture are summarized in Table 8, and the evaluation-time prompts are summarized in Table 9.

**Table 8.** **Instruction-following Data Mixture** of LLaVA-1.5.

| Data | Size | Response formatting prompts |
| --- | --- | --- |
| LLaVA | 158K | -- |
| ShareGPT | 40K | -- |
| VQAv2 | 83K | Answer the question using a single word or phrase. |
| GQA | 72K | Answer the question using a single word or phrase. |
| OKVQA | 9K | Answer the question using a single word or phrase. |
| OCRVQA | 80K | Answer the question using a single word or phrase. |
| A-OKVQA | 66K | Answer with the option’s letter from the given choices directly. |
| TextCaps | 22K | Provide a one-sentence caption for the provided image. |
| RefCOCO | 48K | Randomly choose between a short region description and a region-format prompt. |
| VG | 86K | Provide the bounding box coordinate of the region this sentence describes. |
| Total | 665K | -- |

**Table 9.** **Response format prompt** for evaluation.

| Data | Response formatting prompts |
| --- | --- |
| LLaVA-Bench, MM-Vet | -- |
| VQAv2, GQA, TextVQA, MME, POPE | Answer the question using a single word or phrase. |
| ScienceQA, MMBench, SEED-Bench | Answer with the option’s letter from the given choices directly. |
| VizWiz | When the provided information is insufficient, respond with `Unanswerable`. Answer the question using a single word or phrase. |

## Hyperparameters

The latest Vicuna v1.5 is used as the base LLM. LLaVA-1.5 uses the same set of hyperparameters as the original LLaVA, except that it halves the pretraining learning rate because of the MLP projection layer.

Table 10 summarizes the pretraining and finetuning hyperparameters.

**Table 10.** Hyperparameters of LLaVA-1.5.

| Hyperparameter | Pretrain | Finetune |
| --- | --- | --- |
| batch size | 256 | 128 |
| lr | 1e-3 | 2e-5 |
| lr schedule | cosine decay | cosine decay |
| lr warmup ratio | 0.03 | 0.03 |
| weight decay | 0 | 0 |
| epoch | 1 | 1 |
| optimizer | AdamW | AdamW |
| DeepSpeed stage | 2 | 3 |

# Qualitative Results

## Response Format Prompts

The appendix provides additional examples of LLaVA-1.5 generalizing to different unseen response format prompts.

Table 11 shows qualitative examples of response granularity and format switching.

**Table 11.** Qualitative examples of response granularity and format switching.

<a id="tab:format_prompt_generalization"></a>
![](../sources/Visual%20Instruction%20Tuning_source/figs/extreme_ironing.jpg)
- User: `What is the color of the shirt that the man is wearing? Answer the question using a single word or phrase.`
- LLaVA-1.5: `Yellow.`
- User: `Is this unusual? Please explain briefly with a short sentence.`
- LLaVA-1.5: `Yes, it is unusual to see a man ironing clothes while standing on the back of a moving car.`
- User: `Is this unusual? Please explain in detail.`
- LLaVA-1.5: Gives a long explanation that the man is ironing clothes while standing on the back of a moving yellow SUV and why the situation is unusual and potentially dangerous.
- User: `What is unusual about this image? Answer briefly with a single sentence.`
- LLaVA-1.5: `A man is ironing clothes in the back of a car.`
- User: `Give a more detailed explanation.`
- LLaVA-1.5: Gives a more detailed multi-sentence explanation of the same scene.

**Table 12.** Compositional visual writing examples after including ShareGPT data.

<a id="tab:visual_writing_task"></a>
![](../sources/Visual%20Instruction%20Tuning_source/figs/hawaii_view.jpeg)
- User: `Compose an engaging travel blog post about a recent trip to this place, highlighting cultural experiences and must-see attractions.`
- LLaVA: Produces a shorter and less visually grounded travel narrative centered on Honolulu and Waikiki.
- LLaVA-1.5: Produces a more detailed and visually grounded multi-day travel blog with specific attractions, cultural experiences, and stronger narrative structure.

![](../images/Visual%20Instruction%20Tuning_md_images/figs/multilingual.pdf.png)
**Figure 5.** **Compositional capability: multilingual visual conversation.** LLaVA-1.5 generalizes to multilingual visual conversations when training on visual instruction-following data (English only) together with text-only ShareGPT data (multilingual). However, there can still be errors in some languages, such as Korean.

## Compositional Capabilities

As shown in Figure 5, LLaVA-1.5 is capable of participating in multilingual visual conversations and adapting its output language based on the user’s input, even though it has not been trained on multilingual visual instruction data. The paper hypothesizes that this is an emerging compositional capability learned from visual conversations and multilingual ShareGPT text.

Additionally, as shown in Table 12, LLaVA-1.5 is able to produce more detailed and visually grounded responses in writing tasks with visual inputs than the original LLaVA.

Table 13 shows a constrained prompt-generation example for Stable Diffusion style output.

**Table 13.** Example prompts for anime-style constrained generation.

<a id="tab:anime_prompt_generation"></a>
![](../sources/Visual%20Instruction%20Tuning_source/figs/cartoon_image.jpg)
- User: `Here's a formula for a Stable Diffusion image prompt: a cartoon-style image of [adjective] [subject] [haircut] [clothing] [doing action], [color scheme], detailed, trending on artstation. Generate the prompt for this image.`
- LLaVA-1.5: `A cartoon-style image of a young girl with a bob haircut, wearing a white kimono, holding a stuffed animal and posing for a picture, with a pink and white color scheme, detailed, and trending on artstation.`

# Limitations

Despite the promising results demonstrated by LLaVA-1.5, several limitations remain. First, using full image patches can prolong each training iteration. Second, LLaVA-1.5 is not yet capable of processing multiple images due to the lack of corresponding instruction-following data and context-length constraints. Third, although it can follow complex instructions, its problem-solving capability remains limited in certain domains. Finally, despite significantly reduced hallucination, it can still occasionally disseminate misinformation and should be used cautiously in critical applications such as medicine.
