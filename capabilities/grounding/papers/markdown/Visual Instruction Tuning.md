# Introduction

Large multimodal models (LMMs) have become increasingly popular in the research community, as they are the key building blocks towards general-purpose assistants . Recent studies on LMMs are converging on a central concept known as visual instruction tuning . The results are promising, LLaVA  and MiniGPT-4  demonstrate impressive results on natural instruction-following and visual reasoning capabilities. To better understand the capability of LMMs, multiple benchmarks  have been proposed. Recent works further demonstrate improved performance by scaling up the pretraining data , instruction-following data , visual encoders , or language models , respectively. The LLaVA architecture is also leveraged in different downstream tasks and domains, including region-level  and pixel-level  understanding, biomedical assistants , image generation , adversarial studies .

<p><img src="../images/Visual%20Instruction%20Tuning_md_images/figs/llava_v1_5_radar.pdf.png"  /><br />
<img src="../images/Visual%20Instruction%20Tuning_md_images/figs/bar_lmm_training_samples_transposed.pdf.png" style="height:31mm"  /> <img src="../images/Visual%20Instruction%20Tuning_md_images/figs/architecture.png" style="height:31mm" alt="image" /><br />
</p>
**Figure 1.** **LLaVA-1.5** achieves SoTA on a broad range of 11 tasks (Top), with high training sample efficiency (Left) and simple modifications to LLaVA (Right): an MLP connector and including academic-task-oriented data with response formatting prompts.

However, despite many benchmarks and developments, it still remains unclear what the best recipe is to train LMMs towards the goal of general-purpose assistants. For example, LLaVA  excels in conversational-style visual reasoning and even outperforms later approaches like InstructBLIP  on such benchmarks , while InstructBLIP excels in traditional VQA benchmarks that demands single-word or short answers. Given the significant differences in the model architecture and training data between them, the root cause of the disparity in their capabilities remains elusive, despite conjectures : the amount of training data, the usage of resamplers like Qformer , . To this end, we present the first systematic study to investigate the design choices of LMMs in a controlled setting. Our study originates from LLaVA and builds a road map by carefully making effective contributions from the perspectives of the input, model, and data.

First, we unveil that the fully-connected vision-language connector in LLaVA is surprisingly powerful and data-efficient, and we establish stronger and more feasible baselines built upon the LLaVA framework. We report that two simple improvements, namely, an MLP cross-modal connector and incorporating academic task related data such as VQA, are orthogonal to the framework of LLaVA, and when used with LLaVA, lead to better multimodal understanding capabilities. In contrast to InstructBLIP  or Qwen-VL , which trains specially designed visual resamplers on hundreds of millions or even billions of image-text paired data, LLaVA uses one of the simplest architecture design for LMMs and requires only training a simple fully-connected projection layer on merely 600K image-text pairs. Our final model can finish training in $`\sim`$<!-- -->1 day on a single 8-A100 machine and achieves state-of-the-art results on a wide range of benchmarks. Moreover, unlike Qwen-VL  that includes in-house data in training, LLaVA utilizes only publicly available data.

Next, we delve into an early exploration of other open problems of large multimodal models. Our findings include: (1) Scaling to high-resolution image inputs. We show that LLaVA’s architecture is versatile in scaling to higher resolutions by simply dividing images into grids and maintains its data efficiency; with the increased resolution, it improves the model’s detailed perception capabilities and reduces hallucination. (2) Compositional capabilities. We find that large multimodal models are capable of generalizing to compositional capabilities. For example, training on long-form language reasoning together with shorter visual reasoning can improve the model’s writing capability for multimodal questions. (3) Data efficiency. We show that randomly downsampling LLaVA’s training data mixture by up to 75% does not significantly decrease the model’s performance, suggesting that the possibility of a more sophisticated dataset compression strategy can further improve LLaVA’s already efficient training pipeline. (4) Data scaling. We provide empirical evidence for the scaling of data granularity in conjunction with the model’s capability is crucial for an improved capability without introducing artifacts like hallucination.

In sum, we perform a systematic study on the training of large multimodal models, and introduce a simple yet effective approach to balance the multitask learning and effective scaling for large multimodal models. Our improved baselines, LLaVA-1.5, uses only *public* data, achieves the state-of-the-art on a broad range of 11 tasks, and is significantly more data-efficient than previous approaches. By rethinking the conventional approaches and exploring the open problems in visual instruction tuning, we pave the way for more robust and capable systems for LMMs. We hope these improved and easily-reproducible baselines will provide a reference for future research in open-source LMMs.

# Related Work

**Instruction-following large multimodal models (LMMs).** Common architectures include a pre-trained visual backbone to encode visual features, a pre-trained large language model (LLM) to comprehend the user instructions and produce responses, and a vision-language cross-modal connector to align the vision encoder outputs to the language models. As shown in Figure 1, LLaVA  is perhaps the simplest architecture for LMMs. Optionally, visual resamplers (Qformer ) are used to reduce the number of visual patches . Training an instruction-following LMM usually follows a two-stage protocol. First, the vision-language alignment pretraining stage leverages image-text pairs to align the visual features with the language model’s word embedding space. Earlier works utilize relatively few image-text pairs ($`\sim`$<!-- -->600K  or $`\sim`$<!-- -->6M ), while some recent works pretrain the vision-language connector for a specific language model on a large amount of image-text pairs (129M  and 1.4B ), to maximize the LMM’s performance. Second, the visual instruction tuning stage tunes the model on visual instructions , to enable the model to follow users’ diverse requests on instructions that involve the visual contents. Dealing with higher resolution with grids in LMM are studied in con-current works .

**Multimodal instruction-following data.** In NLP, studies show that the quality of instruction-following data largely affects the capability of the resulting instruction-following models . For visual instruction tuning, LLaVA  is the pioneer to leverage text-only GPT-4 to expand the existing COCO  bounding box and caption dataset to a multimodal instruction-following dataset that contains three types of instruction-following data: conversational-style QA, detailed description, and complex reasoning. LLaVA’s pipeline has been employed to expand to textual understanding , million-scales , and region-level conversations . InstructBLIP  incorporates academic-task-oriented VQA datasets to further enhance the model’s visual capabilities. Conversely, identifies that such naive data merging can result in models that tend to overfit to VQA datasets and thus are unable to participate in natural conversations. The authors further propose to leverage the LLaVA pipeline to convert VQA datasets to a conversational style. While this proves effective for training, it introduces added complexities in data scaling. However, in NLP, the FLAN family  shows that adding a large number of academic language tasks for instruction tuning can effectively improve the generalization ability. In light of this, we consider investigating the root cause of the inability to balance between natural conversations and academic tasks in multimodal models.

# Approach

## Preliminaries

As the seminal work of visual instruction tuning, LLaVA  showcases commendable proficiency in visual reasoning capabilities, surpassing even more recent models on diverse benchmarks  for real-life visual instruction-following tasks. LLaVA uses a single linear layer to project the visual features to language space, and optimizes the whole LLM for visual instruction tuning. However, LLaVA falls short on academic benchmarks that typically require short-form answers (single-word), and tends to answer *yes* for yes/no questions due to the lack of such data in the training distribution.

On the other hand, InstructBLIP  is the pioneer to incorporate academic-task-oriented datasets like VQA-v2  along with LLaVA-Instruct , and demonstrates improved performance on VQA benchmarks. It pretrains Qformer  on 129M image-text pairs and only finetunes the instruction-aware Qformer for visual instruction tuning. However, recent studies  show that it does not perform as well as LLaVA on engaging in real-life visual conversation tasks. More specifically, as shown in Table 1, it can overfit to VQA training sets with short-answers, even on requests that require detailed responses.

<div class="subtable">
<div class="subtable">
## Response Format Prompting

We find that the inability  to balance between short- and long-form VQA for approaches like InstructBLIP , which leverages instruction following data that includes both natural responses and short-answers, is mainly due to the following reasons. First, *ambiguous prompts on the response format*. For example, *Q: {Question} A: {Answer}*. Such prompts do not clearly indicate the desired output format, and can overfit an LLM behaviorally to short-form answers even for natural visual conversations. Second, *not finetuning the LLM*. The first issue is worsened by InstructBLIP only finetuning the Qformer for instruction-tuning. It requires the Qformer’s visual output tokens to control the length of the LLM’s output to be either long-form or short-form, as in prefix tuning , but Qformer may lack the capability of properly doing so, due to its limited capacity compared with LLMs like LLaMA.

Thus, to enable LLaVA to better handle short-form answers while addressing the issues of InstructBLIP, we propose to use a single response formatting prompt that clearly indicates the output format. It is appended at the end of VQA questions when promoting short answers: *Answer the question using a single word or phrase*. We find that when the LLM is *finetuned* with such prompts, LLaVA is able to properly adjust the output format according to the user’s instructions (see Table 1), and does not require additional processing of the VQA answers using ChatGPT , which further enables scaling to various data sources. As shown in Table 2, by merely including VQAv2  in training, LLaVA’s performance on MME significantly improves (1323.8 *vs* 809.6) and outperforms InstructBLIP by 111 points.

<p><img src="../images/Visual%20Instruction%20Tuning_md_images/figs/high_res_arch_v2.pdf.png"  /><br />
</p>
**Figure 2.** **LLaVA-1.5-HD.** Scaling LLaVA-1.5 to higher resolutions by splitting the image into grids and encoding them independently. This allows the model to scale to any resolution, without performing positional embedding interpolation for ViTs. We additionally concatenate the feature of a downsampled image to provide the LLM with a global context.

## Scaling the Data and Model

**MLP vision-language connector.** Inspired by the improved performance in self-supervised learning by changing from a linear projection to an MLP , we find that improving the vision-language connector’s representation power with a two-layer MLP can improve LLaVA’s multimodal capabilities, compared with the original linear projection.

**Academic task oriented data.** We further include additional academic-task-oriented VQA datasets for VQA, OCR, and region-level perception, to enhance the model’s capabilities in various ways, as shown in Table 2. We first include four additional datasets that are used in InstructBLIP: open-knowledge VQA (OKVQA , A-OKVQA ) and OCR (OCRVQA , TextCaps ). A-OKVQA is converted to multiple choice questions and a specific response formatting prompt is used: *Answer with the option’s letter from the given choices directly*. With only a subset of the datasets InstructBLIP uses, LLaVA already surpasses it on all three tasks in Table 2, suggesting LLaVA’s effective design. Furthermore, we find further adding region-level VQA datasets (Visual Genome , RefCOCO ) improves the model’s capability of localizing fine-grained visual details.

**Additional scaling.** We further scale up the input image resolution to 336$`^2`$ to allow the LLM to clearly “see” the details of images, by swapping the vision encoder to CLIP-ViT-L-336px (the highest resolution available for CLIP). In addition, we add the GQA dataset as an additional visual knowledge source. We also incorporate ShareGPT  data and scale up the LLM to 13B as in . Results on MM-Vet shows the most significant improvement when scaling the LLM to 13B, suggesting the importance of the base LLM’s capability for visual conversations.

**LLaVA-1.5.** We denote this final model with all the modifications as LLaVA-1.5 (the last two rows in Table 2), which achieves an impressive performance that significantly outperforms the original LLaVA .

**Computational cost.** For LLaVA-1.5, we use the same pretraining dataset, and keep the training iterations and batch size roughly the same for instruction tuning as LLaVA . Due to the increased image input resolution to 336$`^2`$, the training of LLaVA-1.5 is $`\sim`$<!-- -->2$`\times`$ as long as LLaVA: $`\sim`$<!-- -->6 hours of pretraining and $`\sim`$<!-- -->20 hours of visual instruction tuning, using 8$`\times`$ A100s.
## Scaling to Higher Resolutions

In Section 3.3, we observe the advantage that scaling up the input image resolution improves the model’s capabilities. However, the image resolution of the existing open source CLIP vision encoders is limited to 336$`^2`$, preventing the support of higher resolution images by simply replacing the vision encoder as we did in Section 3.3. In this section, we present an early exploration of scaling the LMM to higher resolutions, while maintaining the data efficiency of LLaVA-1.5.

When using ViT  as the vision encoder, to scale up the resolution, previous approaches mostly choose to perform positional embedding interpolation  and adapt the ViT backbone to the new resolution during finetuning. However, this usually requires the model to be finetuned on a large-scale image-text paired dataset , and limits the resolution of the image to a fixed size that the LMM can accept during inference.

Instead, as shown in Figure 2, we overcome this by dividing the image into smaller image patches of the resolution that the vision encoder is originally trained for, and encode them independently. After obtaining the feature maps of individual patches, we then combine them into a single large feature map of the target resolution, and feed that into the LLM. To provide the LLM with the global context and to reduce the artifact of the split-encode-merge operation, we additionally concatenate the feature of a downsampled image to the merged feature map. This allows us to scale the input to any arbitrary resolution and maintain the data efficiency of LLaVA-1.5. We call this resulting model LLaVA-1.5-HD.

# Empirical Evaluation

## Benchmarks

We evaluate LLaVA-1.5 on a collection of both academic-task-oriented benchmarks and recent benchmarks specifically proposed for instruction-following LMMs, totalling 12 benchmarks. For academic-task-oriented benchmarks, VQA-v2  and GQA  evaluate model’s visual perception capabilities on open-ended short answers. VizWiz  contains 8,000 images to evaluate model’s zero-shot generalization on visual questions asked by visually impaired people. Following InstructBLIP , the image subset of ScienceQA  with multiple choice are used to evaluate the zero-shot generalization on scientific question answering. TextVQA  contains text-rich visual question answering.

For recent benchmarks proposed for instruction-following LMMs, POPE  evaluates model’s degree of hallucination on three sampled subsets of COCO : random, common, and adversarial and we report the F1 score on all three splits. Other benchmarks evaluate the model’s capabilities on a wide range of domains and applications, with different response formats. MME-Perception  evaluates model’s visual perception with yes/no questions. MMBench  evaluates model’s answer robustness with all-round shuffling on multiple choice answers. MMBench-CN  is the Chinese-translated version of MMBench. SEED-Bench  evaluates model’s performance on both images and videos with multiple choice, and we sample the frame in the middle to evaluate the accuracy on videos. LLaVA-Bench-in-the-Wild  and MM-Vet  evaluate model’s capabilities in engaging in visual conversations on a diverse range of tasks, and evaluates the correctness and the helpfulness of the response with GPT-4 evaluation.

<div class="minipage">

<a id="tab:tricky_example"></a>

**Table 1.** Auto-restored caption placeholder for `tab:tricky_example`.

## Results

We show that LLaVA-1.5 achieves the best overall performance on 12 benchmarks, despite using magnitudes smaller pretraining and instruction tuning data compared with other methods . LLaVA-1.5 significantly outperforms LLaVA on all benchmarks for instruction-following LMMs. Note that it is challenging to evalute the original LLaVA on academic datasets like VQA-v2  that demand open-ended short answers.

When we continue to scale up the image resolution to 448$`^2`$ with LLaVA-1.5-HD, it further improves the overall performance on all benchmarks, especially on tasks that require perception of details in the images (OCR in MM-Vet, detailed description in LLaVA-Bench-in-the-Wild ). Moreover, we find that adding the global context effectively recovers the model from the split-and-merge artifacts and guides the model to more easily locate the relevant regions from the high-resolution features (see appendix).

It is encouraging that *LLaVA-1.5 achieves the best performance with the simplest architecture, academic compute and public datasets, and yields a fully-reproducible and affordable baseline for future research*. The results also suggest that visual instruction tuning plays an important role in improving an LMM’s capabilities, and raises questions upon the common belief that LMMs require significant amount of vision-language alignment pretraining , despite that the vision encoders (CLIP , OpenCLIP , EVA-CLIP , ) are already pretrained on web-scale image-text paired data. LLaVA-1.5 (even the 7B model) outperforms 80B IDEFICS , a Flamingo-like LMM with billions of trainable parameters for cross-modal connection. This also makes us rethink the benefits of the vision samplers and the necessity of the additional large-scale pretraining, in terms of multimodal instruction-following capabilities.

<div class="minipage">

<a id="tab:constrait_json"></a>

**Table 2.** Auto-restored caption placeholder for `tab:constrait_json`.

**Global context.** For higher resolution, we pad and resize the image to a single image of 224$`^2`$, and concatenate it with the high resolution features to provide a global context. Ablation on a 7B model shows that the global context effectively boosts performance on all three validation benchmarks.
The corresponding ablation metrics are summarized in Table 3.

<a id="tab:ablation_global_context"></a>

**Table 3.** Auto-restored caption placeholder for `tab:ablation_global_context`.


## Emerging Properties

**Format instruction generalization.** Although LLaVA-1.5 is only trained with a limited number of format instructions, it generalizes to others. First, VizWiz  requires the model to output “Unanswerable” when the provided content is insufficient to answer the question, and our response format prompt (see Appendix) effectively instructs the model to do so (11.1% $`\rightarrow`$ 67.8% on unanswerable questions). We additionally present qualitative examples on instructing LLaVA-1.5 to verify tricky questions (Figure 5), respond in a constrained JSON format (Figure 6), and more in appendix.
**Figure 6.** Example of constrained JSON response formatting.

**Multilingual multimodal capability.** Though LLaVA-1.5 is *not* finetuned for multilingual multimodal instruction following *at all* (all visual instructions including VQA are in English), we find that it is capable of following multilingual instructions. This is partly due to the multilingual language instructions in ShareGPT . Although ShareGPT does not contain images in its instructions, the model learns from this dataset the behavior of adaptively responding with the language that corresponds to the user’s request. We empirically show that this behavior is transferred to visual conversations. We also quantitatively evaluate the model’s generalization capability to Chinese on MMBench-CN , where the questions of MMBench are converted to Chinese. Notably, LLaVA-1.5 outperforms Qwen-VL-Chat by +7.3% (63.6% vs 56.7%), despite Qwen being finetuned on Chinese multimodal instructions while LLaVA-1.5 is not.

## Ablation on LLM Choices

<p><img src="../images/Visual%20Instruction%20Tuning_md_images/figs/llava_v1_5_radar_llm_ablate.pdf.png"  /><br />
</p>
**Figure 3.** **Ablation on LLM choices**. Data points represent the relative performance of the best performing variant for each dataset.

In NLP, findings  suggest that the capability of the base LLM can affect its instruction-tuned successors. In this section, we explore two families of LLMs and study their contribution to the final model’s multimodal capability: LLaMA-based (Vicuna-v1.1, Vicuna-v1.3) and LLaMA-2-based (Vicuna-v1.5, LLaMA-2-Chat). Vicuna-v1.3 and Vicuna-v1.5 use the same $`\sim`$<!-- -->150K ShareGPT  data (2$`\times`$ that used in v1.1). Unlike Vicuna series that is only trained with supervised instruction finetuning (SFT), LLaMA-2-Chat is further optimized with reinforcement-learning from human-feedback (RLHF). We visualize the relative performance of these variants in Figure 3.

First, we find that Vicuna-v1.5 achieves the best overall performance, and LLaMA-2-based models generally perform better than LLaMA-1-based, suggesting the importance of the base language model. This is further evidenced by the results on MMBench-CN : despite Vicuna-v1.3 and v1.5 using the same ShareGPT data for instruction tuning, the performance in generalization to Chinese of Vicuna-v1.3 is significantly worse than v1.5.

Second, language instruction-tuning matters on specific capabilities that are required by each dataset. For example, although LLaMA-2-Chat and Vicuna-v1.5 achieves almost the same performance on MMBench, the generalization to MMBench-CN  of LLaMA-2-Chat is worse than Vicuna-v1.5, which is partly due to that the most SFT/RLHF data of LLaMA-2-Chat is in English and does not contain as many multilingual data as in ShareGPT. Furthermore, TextVQA requires both the model’s capability of identifying the text characters in the images, and also processing the noisy outputs from the OCR engine; such noise *may* be more commonly observed in the ShareGPT data, which is collected in-the-wild from daily usage of ChatGPT.

<p><img src="../images/Visual%20Instruction%20Tuning_md_images/figs/llava_v1_5_radar_data_ablate.pdf.png"  /><br />
</p>
**Figure 4.** **Ablation on data efficiency.** Data points represent the relative performance of the best performing variant for each dataset.

# Open Problems in LMMs

Given the successful scaling of LLaVA-1.5, we conduct additional studies on open problems in LMMs using the model design and data mixture of LLaVA-1.5.

## Data Efficiency

Despite the data efficiency of LLaVA-1.5 when compared with approaches like InstructBLIP , the training of LLaVA-1.5 still doubles when compared with LLaVA. In this section, we conduct experiments for further improving the data efficiency by randomly sub-sampling the training data mixture of LLaVA-1.5, with a sampling ratio ranging from 0.1 to 0.5. We visualize the relative performance of different sampling variants in Figure 4.

First, the full data mixture provides the best knowledge coverage, and allows the model to achieve the best overall performance. To our surprise, with only 50% of the samples, the model still maintains more than 98% of the full dataset performance. This suggests that there is room for further improvements in data efficiency.

Second, when downsampling the dataset to 50%, the model’s performance on MMBench, ScienceQA, and POPE does not decrease at all, and it even slightly improves on MMBench. Similarly, the model’s performance remains steady when further downscaling the data from 50% to 30%. These results show promise of having the less-is-more  benefit for multimodal models as well.

## Rethinking Hallucination in LMMs

Hallucination is an important issue to tackle for LLMs and LMMs. Often in LMMs, we attribute the model’s hallucination to the errors or hallucinations in the training dataset. For example, the detailed descriptions in LLaVA-Instruct  may contain a small amount of hallucinated content, and it is believed that training on such data *may* have caused the model to hallucinate when asked to “describe the image in detail”. However, we find that such hallucination is significantly reduced, when we scale the model’s inputs to higher resolutions like 448$`^2`$.

This finding is interesting as it suggests that the LMMs may be robust to *a few* such errors in the training data. However, when the input resolution is not sufficient for the model to discern all details in the training data, and the amount of data that is at that granularity beyond the model’s capability becomes large enough, the model *learns* to hallucinate. This further suggests that there needs to be a balance between improving the data annotation with more details and the model’s capability to properly process the information at such granularities. We hope this finding provides a reference for future work in terms of dealing with hallucination and the scaling of the models and data.

## Compositional Capabilities

We demonstrate interesting compositional capabilities in LLaVA-1.5: the model trained on a set of tasks independently generalizes to tasks that require a combination of these capabilities without explicit joint training. We note some of the findings below.

First, we observe an improved language capability in visual conversations after including the ShareGPT  data, including the multimodal multilingual capability as discussed in Section 4.3. Moreover, the model is more capable at providing longer and more detailed responses in visual conversations. Second, the additional visual knowledge from the academic-task-oriented datasets, improves the visual groundness of LLaVA-1.5’s responses in visual conversations, as evidenced quantitatively by the improved results on MM-Vet  and LLaVA-Wild  in Table 4.

However, there is still difficulty in achieving ideal performance for some tasks that require a certain combination of capabilities. For example, being able to correctly answer the attribute of a certain object in VQA, does not guarantee an accurate depiction of that object attribute in a detailed description of the whole image. Furthermore, the capability of engaing in conversations with certain foreign languages (Korean) still falls behind. See appendix for examples.

These findings suggest that the compositional capabilities of LMMs can be leveraged to improve the model’s performance without significantly increasing the data by exhaustively including all task combinations. Yet, it can be further investigated, and a deeper understanding of the mechanism behind the compositional capabilities of LMMs can further improve the capability and the data efficiency of LLaVA-1.5.

# Conclusion

In this paper, we take a step towards demystifying the design of large multimodal models, and propose a simple, effective, and data-efficient baseline, LLaVA-1.5, for large multimodal models. In addition, we explore the open problems in visual instruction tuning, scale LMMs to higher resolutions, and present some intriguing findings in terms of model hallucination and compositional capabilities for LMMs. We hope these improved and easily-reproducible baselines as well as the new findings will provide a reference for future research in open-source LMM.

**Limitations.** Despite the promising results demonstrated by LLaVA-1.5, it still has limitations including prolonged training for high-resolution images, lack of multiple-image understanding, limited problem solving capabilities in certain fields. It is not exempt from producing hallucinations, and should be used with caution in critical applications (medical). See appendix for a detailed discussion.

**Acknowledgements.** This work was supported in part by NSF CAREER IIS2150012, and Institute of Information & communications Technology Planning & Evaluation(IITP) grants funded by the Korea government(MSIT) (No. 2022-0-00871, Development of AI Autonomy and Knowledge Enhancement for AI Agent Collaboration) and (No. RS-2022-00187238, Development of Large Korean Language Model Technology for Efficient Pre-training).

# Appendix

This appendix is organized as follows.

- In Section 7, we show implementation details for LLaVA-1.5-HD (Section 7.1), data and prompts (Section 7.2), and hyperparameters (Section 7.3).

- In Section 8, we present more qualitative results for response format prompts (Section 8.1), compositional capabilities (Section 8.2).

- In Section 9, we discuss limitations with more details.

# Implementation Details

## LLaVA-1.5-HD

### Preprocessing

**Overview.** We use CLIP-ViT-L-14 (224$`^2`$) as the base image encoder. We first select and pad the input image to a target resolution that effectively captures its details, and split the image into 224$`^2`$ grids. All 224$`^2`$ image patches are encoded by the CLIP image encoder separately and their features are merged back to a single large feature map. We then post-process the resulting feature map to a flattened list of features. We additionally concatenate the features of a fixed-resolution image to provide the model with a global context.

**Target resolution selection.** We predefine a set of resolutions to support up to six grids (1x1, 1x2, 1x3, 1x4, 1x5, 1x6, 2x2, 2x3, and their transpose). This system allows for a maximum resolution of 672x448 (or 448x672). Two criteria are enforced in the target resolution selection: (1) *Detail preservation*: the selected resolution preserves as much detail from the original image as possible; (2) *Resource efficiency:* the resolution should not be excessively large to avoid unnecessary consumption of pixels and memory (it should not select 448$`^2`$ for a 224$`^2`$ input image).

**Postprocessing.** We perform three steps of postprocessing to ensure that the final features can be processed effectively and efficiently by the language model. (1) *Padding removal.* Features corresponding exclusively to the paddings are discarded. This reduces the number of visual tokens processed by the language model and improves the efficiency. (2) *Row-end Tokens.* We append a special token to the end of each row of features, to provide an explicit indication of the shape of the image. Unlike the original LLaVA and LLaVA-1.5 that uses a fixed resolution, we now use a variable resolution for the image features of LLaVA-1.5-HD, such indication allows the language model to capture the exact shape and the size of the image for each sample. (3) *Flattening.* Finally, we flatten the image feature map and feed it into the language model along with language token features.

### Training

Since we compute the visual features on the original 224$`^2`$ resolution that the vision encoder is trained on, we do not perform additional pretraining. We also do not perform additional high resolution pretraining for the visual projectors, and perform visual instruction tuning directly on the higher-resolution images.

## Data

Our final training data mixture contains a variety of datasets: VQA , OCR , region-level VQA , visual conversation  and language conversation  data. We adopt multiple strategies to reduce training cost and enhance efficiency, detailed as follows:

1.  For all VQA datasets, QA pairs from the same training image are merged into a single conversation.

2.  For ShareGPT , we filter out invalid conversations as . Unlike Vicuna , long conversations that surpass 2048 tokens are truncated rather than splitting to multiple conversations. This results in $`\sim`$<!-- -->40K conversations.

3.  Each QA pair in A-OKVQA  is augmented $`k`$ times, where $`k`$ is the number of choices per question, to counterbalance the lack of multiple-choice data.

4.  80K conversations are sampled from OCRVQA .

5.  For Visual Genome, we sample 10 annotations for images with additional annotations.

6.  For RefCOCO, conversations are dissected into segments, each containing fewer than 10 conversations.

7.  We obverse that language conversations are often longer than visual ones. For each batch, we sample conversations only from a single modality, and this speeds up the training by 25%, and does not affect the final outcome.

All data splits are concatenated together and sampled with the same probability. We present the response formatting prompts of the final instruction-following data mixtures in Table 5 and the response format prompts used for each evaluation benchmark in Table 6.

## Hyperparameters

The latest Vicuna v1.5  is used as the base LLM. LLaVA-1.5 uses the same set of hyperparameters as the original LLaVA, except that we halve the learning rate in pretraining due to the usage of the MLP projection layer instead of the original linear projection layer design. We show the training hyperparameters for both first-stage vision-language alignment pretraining and the second-stage visual instruction tuning in Table 7. We use greedy decoding for evaluation to ensure reproducibility.
**Table 7.** Training hyperparameters for pretraining and visual instruction tuning.

# Qualitative Results

## Response Format Prompts

We show additional examples of LLaVA-1.5 generalizing to different unseen response format prompts.

First, as shown in Table 10, LLaVA-1.5 can provide details at different granularities in response to user’s requests. When requested by the user, it is also capable of switching between response formats within the conversations.
**Table 10.** Qualitative examples of response granularity and format switching.

Second, we provide another example of the constrained prompting to generate the prompts for Stable Diffusion models. We show an example of generating anime prompts in Table 12.
**Table 12.** Example prompts for anime-style constrained generation.

<div class="minipage">

<a id="tab:format_prompt_generalization"></a>

**Table 4.** Auto-restored caption placeholder for `tab:format_prompt_generalization`.

<div class="minipage">

<a id="tab:visual_writing_task"></a>

**Table 5.** Auto-restored caption placeholder for `tab:visual_writing_task`.

<p><img src="../images/Visual%20Instruction%20Tuning_md_images/figs/multilingual.pdf.png"  /><br />
</p>
**Figure 5.** **Compositional capability: multilingual visual conversation.** LLaVA-1.5 generalizes to multilingual visual conversations, when training on visual instruction following data (English-only) together with the text-only ShareGPT data (multilingual). However, there can still be errors in some languages (Korean, errors marked in  red).

## Compositional Capabilities

We present qualitative examples of the compositional capabilities of LLaVA-1.5. As shown in Figure 5, LLaVA-1.5 is capable of participating in multilingual visual conversations and adapting its output language based on the user’s input, even though it has not been trained on multilingual visual instruction data. We hypothesize this emerging bahavior is a compositional capability learned from visual conversations (English-only) and the text-only ShareGPT data (multilingual). However, there can still be errors in some languages (Korean), which could be improved by incorporating more of those language data.

Additionally, in Table 11, we show another observed compositional capability after including the ShareGPT data in training. LLaVA-1.5 is able to produce more detailed and visually-grounded responses in writing tasks with visual inputs than LLaVA.
**Table 11.** Compositional visual writing examples after including ShareGPT data.

<div class="minipage">

<a id="tab:anime_prompt_generation"></a>

**Table 6.** Auto-restored caption placeholder for `tab:anime_prompt_generation`.

# Limitations

Despite the promising results demonstrated by LLaVA-1.5, several limitations must be acknowledged. First, LLaVA-1.5 utilizes full image patches, potentially prolonging each training iteration. While visual resamplers  reduce the number of visual patches in LLMs, they currently cannot achieve convergence as efficiently as LLaVA with a comparable amount of training data, probably due to more trainable parameters in the resamplers. The development of a sample-efficient visual resampler could pave the way for future scaling-up of instruction-following multimodal models. Second, LLaVA-1.5 is not yet capable of processing multiple images due to the lack of such instruction-following data, and the limit of the context length. Third, although LLaVA-1.5 exhibits proficiency in following complex instructions, its problem-solving capabilities can still be limited in certain domains, which could be improved with a more capable language model and with high-quality, targeted visual instruction tuning data. Finally, despite its significantly reduced propensity for hallucination, LLaVA-1.5 is not exempt from producing hallucinations and occasionally disseminating misinformation, and should be used with caution in critical applications (medical).
