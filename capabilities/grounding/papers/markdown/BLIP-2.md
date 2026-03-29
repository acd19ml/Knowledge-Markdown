# Introduction

<a id="sec:intro"></a>

Vision-language pre-training (VLP) research has witnessed a rapid advancement in the past few years, where pre-trained models with increasingly larger scale have been developed to continuously push the state-of-the-art on various downstream tasks . However, most state-of-the-art vision-language models incur a high computation cost during pre-training, due to end-to-end training using large-scale models and datasets.

<img src="../images/BLIP-2_md_images/image/fig1-example.pdf.png"  />
**Figure 1.** Overview of BLIP-2’s framework. We pre-train a lightweight Querying Transformer following a two-stage strategy to bridge the modality gap. The first stage bootstraps vision-language representation learning from a frozen image encoder. The second stage bootstraps vision-to-language generative learning from a frozen LLM, which enables zero-shot instructed image-to-text generation (see Figure 4 for more examples).

Vision-language research sits at the intersection between vision and language, therefore it is naturally expected that vision-language models can harvest from the readily-available unimodal models from the vision and natural language communities. In this paper, we propose a *generic* and *compute-efficient* VLP method by bootstrapping from off-the-shelf pre-trained vision models and language models. Pre-trained vision models offer high-quality visual representation. Pre-trained language models, in particular *large language models* (LLMs), offer strong language generation and zero-shot transfer abilities. To reduce computation cost and counteract the issue of catastrophic forgetting, the unimodal pre-trained models remain frozen during the pre-training.

In order to leverage pre-trained unimodal models for VLP, it is key to facilitate cross-modal alignment. However, since LLMs have not seen images during their unimodal pre-training, freezing them makes vision-language alignment in particular challenging. In this regard, existing methods (*e*.*g*. Frozen , Flamingo ) resort to an image-to-text generation loss, which we show is insufficient to bridge the modality gap.

To achieve effective vision-language alignment with frozen unimodal models, we propose a Querying Transformer (Q-Former) pre-trained with a new two-stage pre-training strategy. As shown in Figure 1, Q-Former is a lightweight transformer which employs a set of learnable query vectors to extract visual features from the frozen image encoder. It acts as an information bottleneck between the frozen image encoder and the frozen LLM, where it feeds the most useful visual feature for the LLM to output the desired text. In the first pre-training stage, we perform vision-language representation learning which enforces the Q-Former to learn visual representation most relevant to the text. In the second pre-training stage, we perform vision-to-language generative learning by connecting the output of the Q-Former to a frozen LLM, and trains the Q-Former such that its output visual representation can be interpreted by the LLM.

We name our VLP framework as BLIP-2: Bootstrapping Language-Image Pre-training with frozen unimodal models. The key advantages of BLIP-2 include:

- BLIP-2 effectively leverages both frozen pre-trained image models and language models. We bridge the modality gap using a Q-Former pre-trained in two-stages: representation learning stage and generative learning stage. BLIP-2 achieves state-of-the-art performance on various vision-language tasks including visual question answering, image captioning, and image-text retrieval.

- Powered by LLMs (*e*.*g*. OPT , FlanT5 ), BLIP-2 can be prompted to perform zero-shot image-to-text generation that follows natural language instructions, which enables emerging capabilities such as visual knowledge reasoning, visual conversation, etc. (see Figure 4 for examples).

- Due to the use of frozen unimodal models and a lightweight Q-Former, BLIP-2 is more compute-efficient than exisiting state-of-the-arts. For example, BLIP-2 outperforms Flamingo  by 8.7% on zero-shot VQAv2, while using 54$`\times`$ fewer trainable parameters. Furthermore, our results show that BLIP-2 is a generic method that can harvest more advanced unimodal models for better VLP performance.

# Related Work

<a id="sec:related"></a>

## End-to-end Vision-Language Pre-training

Vision-language pre-training aims to learn multimodal foundation models with improved performance on various vision-and-language tasks. Depending on the downstream task, different model architectures have been proposed, including the dual-encoder architecture , the fusion-encoder architecture , the encoder-decoder architecture , and more recently, the unified transformer architecture . Various pre-training objectives have also been proposed over the years, and have progressively converged to a few time-tested ones: image-text contrastive learning , image-text matching , and (masked) language modeling .

Most VLP methods perform end-to-end pre-training using large-scale image-text pair datasets. As the model size keeps increasing, the pre-training can incur an extremely high computation cost. Moreover, it is inflexible for end-to-end pre-trained models to leverage readily-available unimodal pre-trained models, such as LLMs .

## Modular Vision-Language Pre-training

More similar to us are methods that leverage off-the-shelf pre-trained models and keep them frozen during VLP. Some methods freeze the image encoder, including the early work which adopts a frozen object detector to extract visual features , and the recent LiT  which uses a frozen pre-trained image encoder for CLIP  pre-training. Some methods freeze the language model to use the knowledge from LLMs for vision-to-language generation tasks . The key challenge in using a frozen LLM is to align visual features to the text space. To achieve this, Frozen  finetunes an image encoder whose outputs are directly used as soft prompts for the LLM. Flamingo  inserts new cross-attention layers into the LLM to inject visual features, and pre-trains the new layers on billions of image-text pairs. Both methods adopt the language modeling loss, where the language model generates texts conditioned on the image.

Different from existing methods, BLIP-2 can effectively and efficiently leverage both frozen image encoders and frozen LLMs for various vision-language tasks, achieving stronger performance at a lower computation cost.

# Method

<img src="../images/BLIP-2_md_images/image/fig2-v5.pdf.png"  />
**Figure 2.** (**Left**) Model architecture of Q-Former and BLIP-2’s first-stage vision-language representation learning objectives. We jointly optimize three objectives which enforce the queries (a set of learnable embeddings) to extract visual representation most relevant to the text. (**Right**) The self-attention masking strategy for each objective to control query-text interaction.

We propose BLIP-2, a new vision-language pre-training method that bootstraps from frozen pre-trained unimodal models. In order to bridge the modality gap, we propose a Querying Transformer (Q-Former) pre-trained in two stages: (1) vision-language representation learning stage with a frozen image encoder and (2) vision-to-language generative learning stage with a frozen LLM. This section first introduces the model architecture of Q-Former, and then delineates the two-stage pre-training procedures.

## Model Architecture

We propose Q-Former as the trainable module to bridge the gap between a frozen image encoder and a frozen LLM. It extracts a fixed number of output features from the image encoder, independent of input image resolution. As shown in Figure 2, Q-Former consists of two transformer submodules that share the same self-attention layers: (1) an image transformer that interacts with the frozen image encoder for visual feature extraction, (2) a text transformer that can function as both a text encoder and a text decoder. We create a set number of learnable query embeddings as input to the image transformer. The queries interact with each other through self-attention layers, and interact with frozen image features through cross-attention layers (inserted every other transformer block). The queries can additionally interact with the text through the same self-attention layers. Depending on the pre-training task, we apply different self-attention masks to control query-text interaction. We initialize Q-Former with the pre-trained weights of BERT$`_\text{base}`$ , whereas the cross-attention layers are randomly initialized. In total, Q-Former contains 188M parameters. Note that the queries are considered as model parameters.

In our experiments, we use 32 queries where each query has a dimension of 768 (same as the hidden dimension of the Q-Former). We use $`Z`$ to denote the output query representation. The size of $`Z`$ ($`32\times768`$) is much smaller than the size of frozen image features (*e*.*g*. $`257\times1024`$ for ViT-L/14). This bottleneck architecture works together with our pre-training objectives into forcing the queries to extract visual information that is most relevant to the text.

## Bootstrap Vision-Language Representation Learning from a Frozen Image Encoder

In the representation learning stage, we connect Q-Former to a frozen image encoder and perform pre-training using image-text pairs. We aim to train the Q-Former such that the queries can learn to extract visual representation that is most informative of the text. Inspired by BLIP , we jointly optimize three pre-training objectives that share the same input format and model parameters. Each objective employs a different attention masking strategy between queries and text to control their interaction (see Figure 2).

**Image-Text Contrastive Learning** (ITC) learns to align image representation and text representation such that their mutual information is maximized. It achieves so by contrasting the image-text similarity of a positive pair against those of negative pairs. We align the output query representation $`Z`$ from the image transformer with the text representation $`t`$ from the text transformer, where $`t`$ is the output embedding of the `[CLS]` token. Since $`Z`$ contains multiple output embeddings (one from each query), we first compute the pairwise similarity between each query output and $`t`$, and then select the highest one as the image-text similarity. To avoid information leak, we employ a unimodal self-attention mask, where the queries and text are not allowed to see each other. Due to the use of a frozen image encoder, we can fit more samples per GPU compared to end-to-end methods. Therefore, we use in-batch negatives instead of the momentum queue in BLIP.

**Image-grounded Text Generation** (ITG) loss trains the Q-Former to generate texts, given input images as the condition. Since the architecture of Q-Former does not allow direct interactions between the frozen image encoder and the text tokens, the information required for generating the text must be first extracted by the queries, and then passed to the text tokens via self-attention layers. Therefore, the queries are forced to extract visual features that capture all the information about the text. We employ a multimodal causal self-attention mask to control query-text interaction, similar to the one used in UniLM . The queries can attend to each other but not the text tokens. Each text token can attend to all queries and its previous text tokens. We also replace the `[CLS]` token with a new `[DEC]` token as the first text token to signal the decoding task.

**Image-Text Matching** (ITM) aims to learn fine-grained alignment between image and text representation. It is a binary classification task where the model is asked to predict whether an image-text pair is positive (matched) or negative (unmatched). We use a bi-directional self-attention mask where all queries and texts can attend to each other. The output query embeddings $`Z`$ thus capture multimodal information. We feed each output query embedding into a two-class linear classifier to obtain a logit, and average the logits across all queries as the output matching score. We adopt the hard negative mining strategy from  to create informative negative pairs.

<img src="../images/BLIP-2_md_images/image/fig3-v3.pdf.png" style="width:90.0%"  />
**Figure 3.** BLIP-2’s second-stage vision-to-language generative pre-training, which bootstraps from frozen large language models (LLMs). (**Top**) Bootstrapping a decoder-based LLM (e.g. OPT). (**Bottom**) Bootstrapping an encoder-decoder-based LLM (e.g. FlanT5). The fully-connected layer adapts from the output dimension of the Q-Former to the input dimension of the chosen LLM.

## Bootstrap Vision-to-Language Generative Learning from a Frozen LLM

In the generative pre-training stage, we connect Q-Former (with the frozen image encoder attached) to a frozen LLM to harvest the LLM’s generative language capability. As shown in Figure 3, we use a fully-connected (FC) layer to linearly project the output query embeddings $`Z`$ into the same dimension as the text embedding of the LLM. The projected query embeddings are then prepended to the input text embeddings. They function as *soft visual prompts* that condition the LLM on visual representation extracted by the Q-Former. Since the Q-Former has been pre-trained to extract language-informative visual representation, it effectively functions as an information bottleneck that feeds the most useful information to the LLM while removing irrelevant visual information. This reduces the burden of the LLM to learn vision-language alignment, thus mitigating the catastrophic forgetting problem.

We experiment with two types of LLMs: decoder-based LLMs and encoder-decoder-based LLMs. For decoder-based LLMs, we pre-train with the language modeling loss, where the frozen LLM is tasked to generate the text conditioned on the visual representation from Q-Former. For encoder-decoder-based LLMs, we pre-train with the prefix language modeling loss, where we split a text into two parts. The prefix text is concatenated with the visual representation as input to the LLM’s encoder. The suffix text is used as the generation target for the LLM’s decoder.

## Model Pre-training

**Pre-training data.** We use the same pre-training dataset as BLIP with 129M images in total, including COCO , Visual Genome , CC3M , CC12M , SBU , and 115M images from the LAION400M dataset . We adopt the CapFilt method  to create synthetic captions for the web images. Specifically, we generate 10 captions using the BLIP$`_\mathrm{large}`$ captioning model, and rank the synthetic captions along with the original web caption based on the image-text similarity produced by a CLIP ViT-L/14 model. We keep top-two captions per image as training data and randomly sample one at each pre-training step.

**Pre-trained image encoder and LLM.** For the frozen image encoder, we explore two state-of-the-art pre-trained vision transformer models: (1) ViT-L/14 from CLIP  and (2) ViT-g/14 from EVA-CLIP . We remove the last layer of the ViT and uses the second last layer’s output features, which leads to slightly better performance. For the frozen language model, we explore the unsupervised-trained OPT model family  for decoder-based LLMs, and the instruction-trained FlanT5 model family  for encoder-decoder-based LLMs.

<img src="../images/BLIP-2_md_images/image/examples.pdf.png"  />
**Figure 4.** Selected examples of **instructed zero-shot image-to-text generation** using a BLIP-2 model w/ ViT-g and FlanT5<sub>XXL</sub>, where it shows a wide range of capabilities including visual conversation, visual knowledge reasoning, visual commensense reasoning, storytelling, personalized image-to-text generation, etc.

**Pre-training settings.** We pre-train for 250k steps in the first stage and 80k steps in the second stage. We use a batch size of 2320/1680 for ViT-L/ViT-g in the first stage and a batch size of 1920/1520 for OPT/FlanT5 in the second stage. During pre-training, we convert the frozen ViTs’ and LLMs’ parameters into FP16, except for FlanT5 where we use BFloat16. We found no performance degradation compared to using 32-bit models. Due to the use of frozen models, our pre-training is more computational friendly than existing large-scale VLP methods. For example, using a single 16-A100(40G) machine, our largest model with ViT-g and FlanT5-XXL requires less than 6 days for the first stage and less than 3 days for the second stage.

The same set of pre-training hyper-parameters are used for all models. We use the AdamW  optimizer with $`\beta_1=0.9`$, $`\beta_1=0.98`$, and a weight decay of 0.05. We use a cosine learning rate decay with a peak learning rate of 1e-4 and a linear warmup of 2k steps. The minimum learning rate at the second stage is 5e-5. We use images of size 224$`\times`$<!-- -->224, augmented with random resized cropping and horizontal flipping.

# Experiment

<a id="sec:experiment"></a>
<a id="tbl:vqa_zeroshot"></a>

**Table 1.** Auto-restored caption placeholder for `tbl:vqa_zeroshot`.

Table 1 provides an overview of the performance of BLIP-2 on various zero-shot vision-language tasks. Compared to previous state-of-the-art models, BLIP-2 achieves improved performance while requiring substantially fewer number of trainable parameters during vision-language pre-training.

## Instructed Zero-shot Image-to-Text Generation

BLIP-2 effectively enables a LLM to understand images while preserving its capability in following text prompts, which allows us to control image-to-text generation with instructions. We simply append the text prompt after the visual prompt as input to the LLM. Figure 4 shows examples to demonstrate a wide range of zero-shot image-to-text capabilities including visual knowledge reasoning, visual commensense reasoning, visual conversation, personalized image-to-text generation, etc.

**Zero-shot VQA**. We perform quantitative evaluation on the zero-shot visual question answering task. For OPT models, we use the prompt “Question: {} Answer:”. For FlanT5 models, we use the prompt “Question: {} Short answer:”. During generation, we use beam search with a beam width of 5. We also set the length-penalty to -1 which encourages shorter answers that align better with human annotation.

As shown in Table 1. BLIP-2 achieves state-of-the-art result on the VQAv2  and GQA  datasets. It outperforms Flamingo80B by 8.7% on VQAv2, despite having 54x fewer trainable parameters. On the OK-VQA  dataset, BLIP-2 comes secondary to Flamingo80B. We hypothesis that this is because OK-VQA focuses more on open-world knowledge than visual understanding, and the 70B Chinchilla  language model from Flamingo80B possesses more knowledge than the 11B FlanT5$`_\text{XXL}`$.

We make a promising observation from Table 1: **a stronger image encoder or a stronger LLM both lead to better performance.** This observation is supported by several facts: (1) ViT-g outperforms ViT-L for both OPT and FlanT5. (2) Within the same LLM family, larger models outperform smaller ones. (3) FlanT5, an instruction-tuned LLM, outperforms the unsupervised-trained OPT on VQA. This observation validates BLIP-2 as a **generic vision-language pre-training method** that can efficiently harvest the rapid advances in vision and natural language communities.

**Effect of Vision-Language Representation Learning.**

<div class="minipage">
<img src="../images/BLIP-2_md_images/image/opt.pdf.png"  />
**Figure 5.** <div class="minipage">
<img src="../images/BLIP-2_md_images/image/flant5.pdf.png"  />
**Figure 6.** Effect of vision-language representation learning on vision-to-language generative learning. Without representation learning, the Q-Former fails the bridge the modality gap, leading to significantly lower performance on zero-shot VQA.

The first-stage representation learning pre-trains the Q-Former to learn visual features relevant to the text, which reduces the burden of the LLM to learn vision-language alignment. Without the representation learning stage, Q-Former relies solely on the vision-to-language generative learning to bridge the modality gap, which is similar to the Perceiver Resampler in Flamingo. Figures 5 and 6 show the effect of representation learning on generative learning. Figure 5 summarizes the OPT trend, and Figure 6 shows the FlanT5 trend. Without representation learning, both types of LLMs give substantially lower performance on zero-shot VQA. In particular, OPT suffers from catastrophic forgetting where performance drastically degrades as training proceeds.
<a id="tbl:caption"></a>

**Table 2.** Auto-restored caption placeholder for `tbl:caption`.

<a id="tbl:vqa_finetune"></a>

**Table 3.** Auto-restored caption placeholder for `tbl:vqa_finetune`.


## Image Captioning

We finetune BLIP-2 models for the image captioning task, which asks the model to generate a text description for the image’s visual content. We use the prompt “a photo of” as an initial input to the LLM and trains the model to generate the caption with the language modeling loss. We keep the LLM frozen during finetuning, and updates the parameters of the Q-Former together with the image encoder. We experiment with ViT-g and various LLMs. Detailed hyperparameters can be found in the appendix. We perform finetuning on COCO, and evaluate on both COCO test set and zero-shot transfer to NoCaps  validation set.

The results are shown in Table 2. BLIP-2 achieves state-of-the-art performance with significant improvement on NoCaps over existing methods, demonstrating strong generalization ability to out-domain images.

## Visual Question Answering

Given annotated VQA data, we finetune the parameters of the Q-Former and the image encoder while keeping the LLM frozen. We finetune with the open-ended answer generation loss, where the LLM receives Q-Former’s output and the question as input, and is asked to generate the answer. In order to extract image features that are more relevant to the question, we additionally condition Q-Former on the question. Specifically, the question tokens are given as input to the Q-Former and interact with the queries via the self-attention layers, which can guide the Q-Former’s cross-attention layers to focus on more informative image regions.

Following BLIP, our VQA data includes the training and validation splits from VQAv2, as well as training samples from Visual Genome. Table 3 demonstrates the state-of-the-art results of BLIP-2 among open-ended generation models.

## Image-Text Retrieval
Since image-text retrieval does not involve language generation, we directly finetune the first-stage-pretrained model w/o LLM. Specifically, we finetune the image encoder together with Q-Former on COCO using the same objectives (*i*.*e*. ITC, ITM, and ITG) as pre-training. We then evaluate the model for both image-to-text retrieval and text-to-image retrieval on COCO and Flickr30K  datasets. During inference, we follow  which first select $`k=128`$ candidates based on the image-text feature similarity, followed by a re-ranking based on pairwise ITM scores. We experiment with both ViT-L and ViT-g as the image encoder. Detailed hyperparameters can be found in the appendix.

The results are shown in Table. BLIP-2 achieves state-of-the-art performance with significant improvement over existing methods on zero-shot image-text retrieval.

<a id="tbl:retrieval_ablation"></a>

**Table 4.** Auto-restored caption placeholder for `tbl:retrieval_ablation`.


The ITC and ITM losses are essential for image-text retrieval as they directly learn image-text similarity. In Table 4, we show that the ITG (image-grounded text generation) loss is also beneficial for image-text retrieval. This result supports our intuition in designing the representation learning objectives: the ITG loss enforces the queries to extract visual features most relevant to the text, thus improving vision-language alignment.

# Limitation

Recent LLMs can perform in-context learning given few-shot examples. However, our experiments with BLIP-2 do not observe an improved VQA performance when providing the LLM with in-context VQA examples. We attribute the lack of in-context learning capability to our pre-training dataset, which only contains a single image-text pair per sample. The LLMs cannot learn from it the correlation among multiple image-text pairs in a single sequence. The same observation is also reported in the Flamingo paper, which uses a close-sourced interleaved image and text dataset (M3W) with multiple image-text pairs per sequence. We aim to create a similar dataset in future work.

BLIP-2’s image-to-text generation could have unsatisfactory results due to various reasons including inaccurate knowledge from the LLM, activating the incorrect reasoning path, or not having up-to-date information about new image content (see Figure 7). Furthermore, due to the use of frozen models, BLIP-2 inherits the risks of LLMs, such as outputting offensive language, propagating social bias, or leaking private information. Remediation approaches include using instructions to guide model’s generation or training on a filtered dataset with harmful content removed.

# Conclusion

<a id="sec:conclusion"></a> We propose BLIP-2, a generic and compute-efficient method for vision-language pre-training that leverages frozen pre-trained image encoders and LLMs. BLIP-2 achieves state-of-the-art performance on various vision-language tasks while having a small amount of trainable parameters during pre-training. BLIP-2 also demonstrates emerging capabilities in zero-shot instructed image-to-text generation. We consider BLIP-2 as an important step towards building a multimodal conversational AI agent.

<thead>
<tr>
<th style="text-align: left;">LLM</th>
<th style="text-align: center;">FlanT5<sub>XL</sub></th>
<th style="text-align: center;">OPT<sub>2.7B</sub></th>
<th style="text-align: center;">OPT<sub>6.7B</sub></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Fine-tuning epochs</td>
<td colspan="3" style="text-align: center;">5</td>
</tr>
<tr>
<td style="text-align: left;">Warmup steps</td>
<td colspan="3" style="text-align: center;">1000</td>
</tr>
<tr>
<td style="text-align: left;">Learning rate</td>
<td colspan="3" style="text-align: center;">1e-5</td>
</tr>
<tr>
<td style="text-align: left;">Batch size</td>
<td colspan="3" style="text-align: center;">256</td>
</tr>
<tr>
<td style="text-align: left;">AdamW *β*</td>
<td colspan="3" style="text-align: center;">(0.9,0.999)</td>
</tr>
<tr>
<td style="text-align: left;">Weight decay</td>
<td colspan="3" style="text-align: center;">0.05</td>
</tr>
<tr>
<td style="text-align: left;">Drop path</td>
<td colspan="3" style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: left;">Image resolution</td>
<td colspan="3" style="text-align: center;">364</td>
</tr>
<tr>
<td style="text-align: left;">Prompt</td>
<td colspan="3" style="text-align: center;">“a photo of”</td>
</tr>
<tr>
<td style="text-align: left;">Inference beam size</td>
<td colspan="3" style="text-align: center;">5</td>
</tr>
<tr>
<td style="text-align: left;">Layer-wise learning rate decay for ViT</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">0.95</td>
</tr>
</tbody>


<thead>
<tr>
<th style="text-align: left;">LLM</th>
<th style="text-align: center;">FlanT5<sub>XL</sub></th>
<th style="text-align: center;">OPT<sub>2.7B</sub></th>
<th style="text-align: center;">OPT<sub>6.7B</sub></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Fine-tuning epochs</td>
<td colspan="3" style="text-align: center;">5</td>
</tr>
<tr>
<td style="text-align: left;">Warmup steps</td>
<td colspan="3" style="text-align: center;">1000</td>
</tr>
<tr>
<td style="text-align: left;">Learning rate</td>
<td colspan="3" style="text-align: center;">1e-5</td>
</tr>
<tr>
<td style="text-align: left;">Batch size</td>
<td colspan="3" style="text-align: center;">128</td>
</tr>
<tr>
<td style="text-align: left;">AdamW *β*</td>
<td colspan="3" style="text-align: center;">(0.9,0.999)</td>
</tr>
<tr>
<td style="text-align: left;">Weight decay</td>
<td colspan="3" style="text-align: center;">0.05</td>
</tr>
<tr>
<td style="text-align: left;">Drop path</td>
<td colspan="3" style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: left;">Image resolution</td>
<td colspan="3" style="text-align: center;">490</td>
</tr>
<tr>
<td style="text-align: left;">Prompt</td>
<td colspan="3" style="text-align: center;">“Question: {} Answer:”</td>
</tr>
<tr>
<td style="text-align: left;">Inference beam size</td>
<td colspan="3" style="text-align: center;">5</td>
</tr>
<tr>
<td style="text-align: left;">Layer-wise learning rate decay for ViT</td>
<td style="text-align: center;">0.95</td>
<td style="text-align: center;">0.95</td>
<td style="text-align: center;">0.9</td>
</tr>
</tbody>


<thead>
<tr>
<th style="text-align: left;">Image Encoder</th>
<th style="text-align: center;">ViT-L/14</th>
<th style="text-align: center;">ViT-g/14</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Fine-tuning epochs</td>
<td colspan="2" style="text-align: center;">5</td>
</tr>
<tr>
<td style="text-align: left;">Warmup steps</td>
<td colspan="2" style="text-align: center;">1000</td>
</tr>
<tr>
<td style="text-align: left;">Learning rate</td>
<td style="text-align: center;">5e-6</td>
<td style="text-align: center;">1e-5</td>
</tr>
<tr>
<td style="text-align: left;">Batch size</td>
<td colspan="2" style="text-align: center;">224</td>
</tr>
<tr>
<td style="text-align: left;">AdamW *β*</td>
<td style="text-align: center;">(0.9,0.98)</td>
<td style="text-align: center;">(0.9,0.999)</td>
</tr>
<tr>
<td style="text-align: left;">Weight decay</td>
<td colspan="2" style="text-align: center;">0.05</td>
</tr>
<tr>
<td style="text-align: left;">Drop path</td>
<td colspan="2" style="text-align: center;">0</td>
</tr>
<tr>
<td style="text-align: left;">Image resolution</td>
<td colspan="2" style="text-align: center;">364</td>
</tr>
<tr>
<td style="text-align: left;">Layer-wise learning rate decay for ViT</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">0.95</td>
</tr>
</tbody>

<img src="../images/BLIP-2_md_images/image/examples_limitation.pdf.png"  />
**Figure 7.** Incorrect output examples for instructed zero-shot image-to-text generation using a BLIP-2 model w/ ViT-g and FlanT5<sub>XXL</sub>.

<img src="../images/BLIP-2_md_images/image/fig-vqa.pdf.png" style="width:48.0%"  />
**Figure 8.** Model architecture for VQA finetuning, where the LLM receives Q-Former’s output and the question as input, then predicts answers. We also provide the question as a condition to Q-Former, such that the extracted image features are more relevant to the question.

We use Figure 8 when describing the VQA finetuning setup in the appendix.
