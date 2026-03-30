# Hallu-PI: Evaluating Hallucination in Multi-modal Large Language Models within Perturbed Inputs

## Abstract

Multi-modal Large Language Models (MLLMs) have demonstrated remarkable performance on various visual-language understanding and generation tasks. However, MLLMs occasionally generate content inconsistent with the given images, which is known as "hallucination". Prior works primarily center on evaluating hallucination using standard, unperturbed benchmarks, which overlook the prevalent occurrence of perturbed inputs in real-world scenarios—such as image cropping or blurring—that are critical for a comprehensive assessment of MLLMs' hallucination. In this paper, to bridge this gap, we propose **Hallu-PI**, the first benchmark designed to evaluate **Hallu**cination in MLLMs within **P**erturbed **I**nputs. Specifically, Hallu-PI consists of seven perturbed scenarios, containing 1,260 perturbed images from 11 object types. Each image is accompanied by detailed annotations, which include fine-grained hallucination types, such as existence, attribute, and relation. We equip these annotations with a rich set of questions, making Hallu-PI suitable for both discriminative and generative tasks. Extensive experiments on 12 mainstream MLLMs, such as GPT-4V and Gemini-Pro Vision, demonstrate that these models exhibit significant hallucinations on Hallu-PI, which is not observed in unperturbed scenarios. Furthermore, our research reveals a severe bias in MLLMs’ ability to handle different types of hallucinations. We also design two baselines specifically for perturbed scenarios, namely Perturbed-Reminder and Perturbed-ICL. We hope that our study will bring researchers’ attention to the limitations of MLLMs when dealing with perturbed inputs, and spur further investigations to address this issue. Our code and datasets are publicly available at [https://github.com/NJUNLP/Hallu-PI](https://github.com/NJUNLP/Hallu-PI).

![Some examples of hallucinations in MLLMs with perturbed inputs (such as image concatenation, image cropping, and prompt misleading). Text highlighted in green and red represents correct and hallucinatory content, respectively.](../images/Hallu-PI_md_images/figs/figure_1.png)
Figure source: `../sources/Hallu-PI_source/figs/figure_1.pdf`

**Figure 1.** Some examples of hallucinations in MLLMs with perturbed inputs (such as image concatenation, image cropping, and prompt misleading). Text highlighted in green and red represents correct and hallucinatory content, respectively.

# 1. Introduction

Multi-modal Large Language Models (MLLMs) have achieved significant progress in a range of practical applications, such as providing detailed descriptions for user-provided images (i.e., image captioning) (Achiam et al. 2023; Team et al. 2023) and answering specific questions about input images (i.e., visual question answering) (H. Liu, Li, Li, et al. 2023; Zhu et al. 2023). However, these models occasionally exhibit a phenomenon known as "hallucination", where the generated content is inconsistent with the given images (H. Ye et al. 2023; L. Huang et al. 2023).

Previous works have sought to investigate the hallucinations in MLLMs by utilizing a large language model like GPT-4 (Achiam et al. 2023), or by employing humans as annotators (Zhou et al. 2023; Zhai et al. 2023). Alternatively, some studies focus on developing detection models to scrutinize the hallucinations exhibited by MLLMs. (Gunjal et al. 2023; Y. Li et al. 2023). More recently,  (J. Wang, Wang, et al. 2023) introduce AMBER, a LLM-free benchmark designed to examine MLLM hallucinations in both discriminative and generative tasks across dimensions like existence, attribute, and relation.

Despite these efforts, existing researches primarily focus on conducting evaluations by sampling images from available image datasets, such as MSCOCO (Y. Li et al. 2023; Qiu et al. 2023; Yin et al. 2023; Gunjal et al. 2023; J. Wang, Zhou, et al. 2023; Zhai et al. 2023). However, in real-world scenarios, inputs fed to MLLMs frequently encounter a variety of perturbations (e.g., noise and cropping) (Geirhos et al. 2018). Overlooking such perturbations could lead MLLMs to produce incorrect answers or judgments, potentially causing serious accidents in certain applications (e.g., medical diagnosis, industrial automation and autonomous driving) (Q. Huang et al. 2023). Figure 2 illustrates the hallucinations of several MLLMs before and after image concatenation perturbation. The inconsistent performance trends indicate that relying solely on existing unperturbed benchmarks is insufficient for a comprehensive and precise evaluation of hallucinations in MLLMs.

![The hallucinatory performance of various MLLMs before (blue bars) and after (orange bars) input perturbation. Inconsistent performance trends show that relying solely on unperturbed benchmarks is insufficient for a complete and precise evaluation of hallucinations in MLLMs.](../images/Hallu-PI_md_images/figs/combined_bar_line_chart_final.png)
Figure source: `../sources/Hallu-PI_source/figs/combined_bar_line_chart_final.pdf`

**Figure 2.** The hallucinatory performance of various MLLMs before (blue bars) and after (orange bars) input perturbation. Inconsistent performance trends show that relying solely on unperturbed benchmarks is insufficient for a complete and precise evaluation of hallucinations in MLLMs.

In order to bridge this gap, we introduce **Hallu-PI**, a benchmark designed to evaluate the **Hallu**cination performance of MLLMs within **P**erturbed **I**nputs. Followed by (Hendrycks and Dietterich 2019; Geirhos et al. 2018), we first categorize the image perturbations into four types: noise, blur, weather, and digital. Additionally, we meticulously propose three distinct types of perturbations: image concatenation, image cropping, and prompt misleading. These perturbations are considered at both the image level and the prompt level. Annotators are instructed to carefully manipulate the perturbations and provide corresponding annotations. Evaluations of 12 mainstream MLLMs conducted on Hallu-PI reveal significant hallucinations of leading MLLMs (e.g., GPT-4V and Gemini-Pro Vision) when dealing with perturbed scenarios.

To comprehensively understand the hallucination of MLLMs to perturbed inputs, we conduct a detailed analysis of the experimental results. We find that most models exhibit significant bias towards specific types of perturbations, particularly image concatenation, image cropping, and prompt misleading (see Figure 1). Furthermore, to mitigate the hallucination of MLLMs in response to perturbed inputs, we draw inspiration from the defensive strategies adopted by text LLMs against jailbreak attacks (Ding et al. 2023; Wu et al. 2023) and designed two baselines: Perturbed-Reminder and Perturbed-ICL. Experiments conducted on GPT-4V show that these strategies effectively reduce hallucinations. We hope our work can prompts MLLM researchers and developers to address hallucinations from perturbed inputs.

In summary, the contributions of our work are as follows:

- We construct Hallu-PI, the first freely available multi-modal hallucination benchmark with perturbed inputs. Hallu-PI encompasses 7 perturbed scenarios, a total of 1,260 images, and 11 distinct object categories to evaluate hallucinations in MLLMs across both generative and discriminative tasks.

- We conduct extensive experiments with Hallu-PI to evaluate multi-modal hallucinations in 12 state-of-the-art MLLMs under perturbed inputs. The results unveil the limitations of MLLMs when dealing with perturbed inputs, as well as their specific bias towards certain types of hallucinations.

- To mitigate the hallucinations of MLLMs on Hallu-PI, we introduce two baselines: Perturbed-Reminder and Perturbed-ICL. Experimental results on GPT-4V indicate that our methods are effective and can reduce the model’s hallucinations in response to perturbed inputs to a certain extent.

# 2. Related Work

## 2.1 Multimodal Large Language Models

Multi-modal Large Language Models (MLLMs) are currently achieving significant improvements by combining the advanced capabilities of Large Language Models (LLMs) with visual processing (Achiam et al. 2023; Alayrac et al. 2022; Team et al. 2023; Driess et al. 2023; J. Li et al. 2023). These MLLMs show great potential in a variety of applications, such as visual question answering (VQA) (Fu et al. 2023), image captioning (Y. Liu et al. 2023), and video understanding (B. Li et al. 2023). Representative MLLMs, such as CogVLM (W. Wang et al. 2023), LLaVA1.5 (H. Liu, Li, Li, et al. 2023), InternLM-XComposer (Zhang et al. 2023), MiniGPT-4 (Chen et al. 2023), mPLUG-Owl2 (Q. Ye et al. 2023), Qwen-VL (Bai et al. 2023), and the latest GPT-4V (Achiam et al. 2023), and Google Gemini-Pro Vision (Team et al. 2023), have achieved impressive performance across various multi-modal tasks.

## 2.2 Hallucination in MLLMs

While MLLMs have exhibited excellent performance on multi-modal tasks, we are still facing the challenge that MLLMs often generate content unfaithful to the given images, which is called "hallucination" (F. Liu et al. 2023; Li et al. 2024; Tong et al. 2024; Chen et al. 2024; Ji et al. 2023).

Currently, many researchers focus on evaluating the hallucination in MLLMs. LURE (Zhou et al. 2023) and HallE-Switch (Zhai et al. 2023) rely on human evaluations or GPT-4. While this method is relatively reliable, it is also expensive. HaELM (J. Wang, Zhou, et al. 2023) and FDPO (Gunjal et al. 2023) are based on hallucinatory detection models. However, the performance of these models is highly dependent on hallucinatory data and incurs substantial training costs. POPE (Y. Li et al. 2023) is based on object detection but is only applicable to discriminative tasks and evaluates existence-type hallucinations. Recently, (J. Wang, Wang, et al. 2023) introduce AMBER, which assesses hallucinations across multiple dimensions, such as existence, attribute, and relation. Despite these efforts, they do not explore hallucinations in the perturbed scenarios commonly encountered in real-life situations. To bridge this gap, we propose Hallu-PI, the first benchmark designed to evaluate the hallucination of MLLMs with perturbed inputs. Table 1 presents a detailed comparison between Hallu-PI and other hallucination benchmarks.

**Table 1.** Comparison with existing hallucination evaluation benchmarks. "Sample" means sampling from an existing dataset.

| Benchmark | Discriminative | Generative | Existence | Attribute | Relation | Perturbation | Baseline | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| POPE | Yes | No | Yes | No | No | No | No | Sample |
| M-HalDetect | No | Yes | No | No | No | No | Yes | Sample |
| HaELM | No | Yes | No | No | No | No | No | Sample |
| Halle-Switch | No | Yes | No | No | No | No | No | Sample |
| AMBER | Yes | Yes | Yes | Yes | Yes | No | No | Manual |
| **Hallu-PI (ours)** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Manual** |

## 2.3 Image Perturbation

To simulate real-world perturbation scenarios, previous works adopt various perturbation strategies such as ImageNet-C (Hendrycks and Dietterich 2019) and Stylize-ImageNet (Geirhos et al. 2018; Michaelis et al. 2019; Qiu et al. 2023). The perturbations are grouped into five primary categories: noise, blur, weather, digital, and stylize. Specifically, these can be further subdivided into the following 17 image perturbation techniques: (1) Noise: Adding noise to the images, such as gaussian noise, shot noise, impulse noise, and speckle noise. (2) Blur: Blurring the images, including defocus blur, frosted glass blur, motion blur, and zoom blur. (3) Weather: Adding environmental effects such as snow, frost, fog, and brightness adjustments. (4) Digital: Manipulating images through contrast enhancement, elastic transformation, pixelation, and JPEG compression. and (5) Stylize: Applying artistic styles and transformations to images.

Compared to existing benchmarks that only consider hallucination assessment in unperturbed scenarios, Hallu-PI further takes into account perturbations that frequently occur in real-world applications. Therefore, it serves as a complement to existing benchmarks and provides a more comprehensive and accurate evaluation of hallucinations in MLLMs.

![(a) Overview of Hallu-PI pipeline for image annotation and perturbation. (b) An illustration of evaluation pipeline of Hallu-PI, including both generative and discriminative tasks.](../images/Hallu-PI_md_images/figs/Hallu-PI_final.png)
Figure source: `../sources/Hallu-PI_source/figs/Hallu-PI_final.pdf`

**Figure 3.** (a) Overview of Hallu-PI pipeline for image annotation and perturbation. (b) An illustration of evaluation pipeline of Hallu-PI, including both generative and discriminative tasks.

# 3. Hallu-PI Benchmark

In this section, we introduce the process of constructing our Hallu-PI benchmark which primarily encompasses three aspects: (1) Image Collection, (2) Image Perturbation and Annotation, and (3) Designing Prompt Query Templates.

## 3.1 Image Collection

To ensure the diversity of the dataset, we identify 11 different object types and require annotators to collect images for each category. In the image selection process, we primarily consider (1) image copyright and (2) image quality. We provide annotators with several websites offering free copyright images and instruct them to search for images using specific object keywords. Annotators are asked to select images where the object is complete and the image is of high quality for downloading.

## 3.2 Image Perturbation and Annotation

Following previous work (Qiu et al. 2023), we first consider four primary types of perturbation: noise, blur, weather, and digital. Stylize is not included because the stylized images are too blurred to recognize the objects and attributes within them. To construct a more comprehensive set of perturbation scenarios, we meticulously propose three additional perturbations: image concatenation, image cropping, and prompt misleading. The first two are considered because they are commonly used by users in real life to edit their images, while prompt misleading ensures that Hallu-PI can evaluate hallucinations at both the image level and the prompt level.

For noise, blur, weather, and digital perturbations, we reuse the code from (Qiu et al. 2023) to generate the perturbed images. For image concatenation, we require our well-trained annotators to combine every four individual images previously collected into a single four-grid image, ensuring that the objects in the concatenated image are complete. For image cropping, we primarily focus on images containing English letters. Annotators are instructed to crop these images and provide corresponding questions and answers for both the original and cropped images. For prompt misleading, annotators need to select an image and provide a prompt that could potentially induce hallucinations. Figure 1 provides some examples of these perturbations. Annotators are required to provide detailed annotations for perturbed images. These annotations include Existence, Number, Color, Relation, and Hal-object, as shown in Figure 3.

In Figure 4, we present the distribution of perturbation types and the distribution of object categories included in Hallu-PI.

![The data distribution of Hallu-PI.](../images/Hallu-PI_md_images/figs/statistic.png)
Figure source: `../sources/Hallu-PI_source/figs/statistic.pdf`

**Figure 4.** The data distribution of Hallu-PI.

## 3.3 Designing Prompt Query Templates

**Table 2.** The results under noise, blur, weather, and digital perturbations. Before/After means before/after perturbation.

| Model | Before ACC+ | Before CHAIR | Noise ACC+ | Noise CHAIR | Blur ACC+ | Blur CHAIR | Weather ACC+ | Weather CHAIR | Digital ACC+ | Digital CHAIR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CogVLM | 49.0 | 62.0 | 48.5 | 68.2 | 47.4 | 68.6 | 42.8 | 67.9 | 48.4 | 69.8 |
| Multi-GPT | 13.3 | 73.5 | 9.6 | 73.6 | 12.8 | 76.1 | 11.2 | 73.4 | 9.2 | 77.8 |
| LLaVA | 6.3 | 68.5 | 4.33 | 67.7 | 5.0 | 70.6 | 4.17 | 69.8 | 3.6 | 74.2 |
| LLaVA1.5 | 43.0 | 68.9 | 42.6 | 70.1 | 42.4 | 68.7 | 43.3 | 68.0 | 36.8 | 74.5 |
| MiniGPT-4 | 16.0 | 72.4 | 15.8 | 70.2 | 15.9 | 72.1 | 14.5 | 72.6 | 13.8 | 73.9 |
| MiniGPT4-v2 | 28.3 | 72.1 | 26.7 | 74.7 | 28.8 | 74.0 | 28.2 | 72.8 | 27.1 | 74.9 |
| mPLUG2 | 38.0 | 65.0 | 33.3 | 67.6 | 33.1 | 69.1 | 35.3 | 66.9 | 32.3 | 73.6 |
| Gemini | 46.0 | 57.3 | 44.2 | 60.0 | 45.1 | 59.7 | 44.8 | 58.5 | 37.5 | 61.3 |
| GPT-4V | 47.3 | 66.1 | 42.3 | 66.9 | 41.8 | 68.4 | 47.8 | 60.9 | 34.0 | 65.4 |

**Table 3.** The results under image concatenation, image cropping, and prompt misleading perturbations.

| MLLM | Concat Before PI-Score | Concat After PI-Score | Cropping Before PI-Score | Cropping After PI-Score | Prompt Mislead Before PI-Score | Prompt Mislead After PI-Score |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CogVLM | 45.4 | 22.5 | 10.0 | 5.0 | 39.6 | 11.4 |
| Multi-GPT | 8.3 | 15.0 | 11.7 | 0.0 | 18.9 | 7.2 |
| LLaVA | 6.5 | 2.2 | 3.4 | 6.7 | 14.4 | 5.2 |
| LLaVA1.5 | 32.4 | 5.9 | 10.0 | 8.4 | 26.4 | 8.1 |
| MiniGPT-4 | 8.9 | 5.9 | 10.0 | 8.4 | 18.5 | 7.0 |
| MiniGPT-v2 | 15.8 | 12.3 | 16.7 | 15.0 | 26.4 | 11.3 |
| mPLUG2 | 25.7 | 18.9 | 10.0 | 8.3 | 29.7 | 15.7 |
| InternLM | 38.3 | 37.3 | 8.3 | 10.0 | 34.4 | 28.0 |
| Qwen-VL | 46.3 | 19.6 | 20.0 | 11.7 | 53.2 | 38.2 |
| VisualGLM | 6.8 | 0.6 | 34.0 | 0.0 | 21.2 | 11.3 |
| Gemini | 44.6 | 21.4 | 45.0 | 26.7 | 59.2 | 39.4 |
| GPT-4V | 42.0 | 18.0 | 43.4 | 30.0 | 61.4 | 48.2 |

To ensure a more comprehensive evaluation of hallucinations, we design both generative and discriminative prompt templates for each perturbation scenario. For the perturbations such as noise, blur, weather, digital, and image concatenation, we pose questions regarding each specific annotation field. For instance, for the image concatenation perturbation, the generative prompt for the "Existence" field before perturbation is: "Please describe the *existing objects* in the image." After perturbation, the prompt becomes: "Please describe the *existing objects* in the *top-left* image." with "*existing objects*" and "*top-left*" being flexible and variable. For the design of discriminative prompts, we consider that merely calculating accuracy might be insufficient. Following previous work (Fu et al. 2023), we design Yes_Q and No_Q, representing questions with the single-word answers "Yes" or "No," respectively. This allows for the calculation of Acc+, which further enhances the accuracy of hallucination assessment, as shown in Figure 3.

For the image cropping and prompt misleading perturbations, the generative and discriminative prompts are meticulously designed by the annotators and reviewed by two experts. We present the detailed prompt templates in the supplementary materials.

# 4. Experiments

In this section, we conduct extensive experiments to evaluate the performance of different state-of-the-art MLLMs on our Hallu-PI benchmark. We introduce the primary setup of our experiments, including baseline models (Sec. 4.1), response processing (Sec. 4.2), and evaluation metrics (Sec. 4.3).

## 4.1 Baseline Models

We select multiple mainstream state-of-the-art MLLMs for evaluation, including GPT-4V (Achiam et al. 2023), Google Gemini-Pro Vision (Team et al. 2023), InternLM-XComposer-VL (Zhang et al. 2023), QWen-VL-Chat (Bai et al. 2023), VisualGLM (Du et al. 2021), mPLUG-Owl-2 (Q. Ye et al. 2023), MininGPT4-v2 (Chen et al. 2023), MiniGPT-4 (Zhu et al. 2023), LLaVA1.5 (H. Liu, Li, Li, et al. 2023), LLaVA (H. Liu, Li, Wu, et al. 2023), CogVLM (W. Wang et al. 2023), and MultimodalGPT (Gong et al. 2023)). All models have been fine-tuned on their instruction tuning datasets. To ensure optimal performance, we use the hyper-parameters provided in the official code repositories of the models to generate responses. More details about these MLLMs are in supplementary materials.

## 4.2 Response Processing

The input for Hallu-PI is defined as: $`Input=\{Img,Ins\}`$, where $`Img`$ represents the image, and $`Ins`$ refers to the prompt. As shown in Figure 3, we obtain an initial response $`Res`$ by inputting $`Input`$ into a specific MLLM and extracting key elements for computing metrics.

For the generative task, we use the natural language toolkit (NLTK) (Bird et al. 2009) as an answer extractor to obtain the initial prediction’s result $`R'_{obj} = \{R_1, R_2,..., R_n\}`$. Then, we construct an objects list $`X_{obj} = \{X_1,X_2,...,X_n\}`$ consisting of all annotated objects in Hallu-PI. $`X_{obj}`$ is used to filter out unnecessary objects in $`R'_{obj}`$ such as "picture," "distance," and "side." Finally, we obtain the final objects $`R_{obj}`$ by using $`R_{obj} = R'_{obj}\cap X_{obj}`$.

For the discriminative task, owing to our prompt template design, "Please answer with ’Yes’ or ’No’," we can easily perform quantitative statistics based on the "Yes" or "No" responses included in the MLLM outputs, which is both accurate and objective.

## 4.3 Evaluation Metrics

We first introduce the metrics used for generative task and discriminative task. Then, we present our proposed PI-Score metric, which is a comprehensive metric for evaluating both tasks. 

**Table 4.** The results of generative task on image concatenation, cropping, and prompt misleading.

| MLLM | Concat CHAIR Before | Concat CHAIR After | Concat Cover Before | Concat Cover After | Concat Hal Before | Concat Hal After | Concat Cog Before | Concat Cog After | Cropping Hal Before | Cropping Hal After | Prompt Misleading Hal Before | Prompt Misleading Hal After |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CogVLM | 62.0 | 69.0 | 55.3 | 48.3 | 58.3 | 97.1 | 4.3 | 5.9 | 80.0 | 90.0 | 36.7 | 93.3 |
| Multi-GPT | 73.5 | 97.5 | 22.5 | 2.0 | 96.7 | 86.3 | 30.8 | 77.1 | 76.7 | 100.0 | 63.3 | 93.3 |
| LLaVA | 68.5 | 92.3 | 38.8 | 7.4 | 93.3 | 96.7 | 4.3 | 14.9 | 93.3 | 86.7 | 66.7 | 93.3 |
| LLaVA1.5 | 68.9 | 76.1 | 43.8 | 25.0 | 78.3 | 96.3 | 3.4 | 5.7 | 86.7 | 90.0 | 63.3 | 90.0 |
| MiniGPT-4 | 72.4 | 89.3 | 46.5 | 24.8 | 98.3 | 95.8 | 5.1 | 8.2 | 80.0 | 83.3 | 63.3 | 93.3 |
| MiniGPT-v2 | 72.1 | 88.9 | 49.6 | 32.5 | 100.0 | 96.7 | 4.0 | 7.1 | 93.3 | 93.3 | 53.3 | 93.3 |
| mPLUG2 | 65.0 | 82.3 | 44.6 | 14.3 | 86.7 | 89.6 | 6.2 | 6.4 | 93.3 | 96.7 | 46.7 | 80.0 |
| InternLM | 58.4 | 79.2 | 16.3 | 9.5 | 71.7 | 62.5 | 18.8 | 16.7 | 86.7 | 86.7 | 43.3 | 63.3 |
| Qwen-VL | 58.2 | 56.3 | 35.8 | 32.3 | 46.7 | 79.2 | 9.8 | 11.1 | 83.3 | 93.3 | 6.7 | 16.7 |
| VisualGLM | 76.9 | 89.1 | 45.0 | 29.6 | 100.0 | 99.2 | 4.4 | 9.2 | 93.3 | 100.0 | 46.7 | 66.7 |
| Gemini | 57.3 | 63.4 | 50.2 | 43.7 | 56.7 | 90.8 | 3.6 | 4.5 | 26.7 | 56.7 | 12.1 | 30.0 |
| GPT-4V | 66.1 | 63.6 | 66.6 | 53.6 | 63.3 | 98.3 | 1.6 | 1.9 | 33.3 | 73.3 | 1.1 | 3.3 |

### Metrics on Generative Task

#### **CHAIR**

CHAIR evaluates the frequency of hallucinatory objects appearing in the responses, which is the most commonly used metric for evaluating hallucinations in MLLMs on generative tasks. With a provided annotated ground truth list $`A_{obj} = \{A_1, A_2,...,A_n\}`$, the calculation formula is as follows:
``` math
\begin{equation}
    \textbf{CHAIR}(Res) = 1 - \frac{len(R_{obj}\cap A_{obj})}{len(R_{obj})} 
\end{equation}
```

#### **Cover**

Cover quantifies the degree of correspondence between responses and the image description. Precisely, its value indicates the coverage of objects mentioned in response $`R_{obj}`$ relative to manually annotated objects $`A_{obj}`$:
``` math
\begin{equation}
    \textbf{Cover}(Res) = \frac{len(R_{obj}\cap A_{obj})}{len(A_{obj})} 
\end{equation}
```

#### **Hal**

Hal represents the proportion of responses with hallucinations. For a MLLM’s response $`Res`$, if its $`\textbf{CHAIR}(Res) \neq 0`$, then $`Res`$ is considered to contain hallucinations:
``` math
\begin{equation}
    \textbf{Hal}(Res)=
    \begin{cases}
        1, \quad \text{if} \quad \textbf{CHAIR}(Res) \neq 0 
        \\0, \quad \text{if} \quad \textbf{CHAIR}(Res) =0
    \end{cases}
\end{equation}
```

#### **Cog**

Cog aims to measure the ratio between hallucinations produced by MLLMs and those annotated by humans. Similar to \[31\], we use the hallucinatory target list $`H_{obj} = \{H_1, H_2,...,H_n\}`$ (corresponding to Hal-object in Figure 3) to calculate Cog:

``` math
\begin{equation}
    \textbf{Cog}(Res) = \frac{len(R_{obj}\cap H_{obj})}{len(R_{obj})} 
\end{equation}
```

### Metrics on Discriminative Task

#### **Accuracy/Precision/Recall/F1 Score**

The outputs of discriminative tasks are constrained to "Yes" or "No", making it straightforward to compute standard metrics such as Accuracy, Precision, Recall, and F1 Score.

***Accuracy+***. Following previous work (Fu et al. 2023), to avoid bias in MLLMs’ responses to "Yes" and "No" and to prevent inaccuracies from random guessing, we calculate Accuracy+ in addition to Accuracy. As described in Sec.  3.3, the model is considered to be right only if it correctly responds to both the "Yes" and "No" questions.

### Metrics on Both Generative and Discriminative Task

#### **PI-Score**.

To comprehensively evaluate the performance of various MLLMs under both generative and discriminative tasks within perturbed inputs, we introduce the **PI-Score** to combine the **Hal** in generative task and the **Accuracy+** in discriminative task. We use $`\alpha`$ as a dynamic weight to balance the importance between generative and discriminative tasks ($`\alpha=0.5`$ in our experiments):
``` math
\begin{equation}
    \textbf{PI-Score} = Avg(\alpha(1-\textbf{Hal}),(1-\alpha)\textbf{Accuarcy+})
\end{equation}
```

# 5. Results

In this section, we first report the overall hallucinations of MLLMs across all perturbation scenarios in Hallu-PI. Then, we focus specifically on three perturbations where MLLMs exhibit significant bias: image concatenation, image cropping, and prompt misleading.

## 5.1 Overall Results

Table 2 and Table 3 demonstrate that all MLLMs show decreased performance under the seven perturbations, with lower **ACC+**, higher **CHAIR** and lower **PI-Score** indicating increased hallucinations. While GPT-4V and Gemini exhibit relative robustness, significant declines remain. Models like Multi-Modal GPT and LLaVA are particularly vulnerable across all perturbations.

## 5.2 Uncovering of Hallucination Bias

Our experiments reveal that MLLMs exhibit more severe hallucinations in *image concatenation*, *image cropping*, and *prompt misleading* perturbation scenarios. Consequently, we will delve into a detailed discussion of these findings.

**Generative Task Results**. Table 4 reveals that MLLMs frequently generate increased hallucinatory content under image concatenation, cropping, and prompt misleading perturbations. Most models show higher CHAIR scores, notably LLaVA rising from 68.5 to 92.3 under concatenation. Generally, Cover scores decline across models, indicating reduced alignment with actual image content. Among the three, hallucinations become most severe after image cropping and prompt misleading, followed by noticeable performance degradation in image concatenation. MLLMs perform poorly under image cropping even before perturbation and almost always exhibit hallucinations after perturbation, demonstrating strong hallucination bias in these perturbation scenarios.

**Table 5.** The results of discriminative task on image concatenation, cropping, and prompt misleading.

| MLLM | Concat ACC Before | Concat ACC+ Before | Concat F1 Before | Concat ACC After | Concat ACC+ After | Concat F1 After | Cropping ACC Before | Cropping ACC+ Before | Cropping F1 Before | Cropping ACC After | Cropping ACC+ After | Cropping F1 After | Prompt Misleading ACC After | Prompt Misleading ACC+ After | Prompt Misleading F1 After |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CogVLM | 69.9 | 49.0 | 74.4 | 67.2 | 42.0 | 73.1 | 50.0 | 0.0 | 66.7 | 50.0 | 0.0 | 66.7 | 56.7 | 33.3 | 51.9 |
| Multi-GPT | 46.8 | 13.3 | 52.4 | 41.8 | 16.3 | 48.9 | 48.3 | 0.0 | 65.2 | 45.0 | 0.0 | 62.1 | 28.3 | 6.7 | 41.1 |
| LLava | 51.5 | 6.3 | 57.2 | 50.3 | 1.0 | 54.0 | 50.0 | 0.0 | 66.7 | 50.0 | 0.0 | 66.7 | 1.7 | 0.0 | 3.2 |
| LLava1.5 | 70.5 | 43.0 | 76.1 | 51.7 | 8.0 | 61.7 | 51.7 | 6.7 | 56.7 | 48.3 | 6.7 | 45.6 | 40.0 | 3.3 | 5.2 |
| MiniGPT-4 | 43.0 | 16.0 | 47.6 | 30.2 | 7.7 | 25.4 | 38.3 | 0.0 | 55.4 | 30.0 | 0.0 | 46.2 | 20.0 | 0.0 | 33.4 |
| MiniGPT-v2 | 55.8 | 28.3 | 56.4 | 48.2 | 21.3 | 41.3 | 55.0 | 26.7 | 62.0 | 48.3 | 23.3 | 47.5 | 88.3 | 80.0 | 88.8 |
| mPLUG2 | 62.3 | 38.0 | 68.3 | 51.5 | 27.3 | 54.5 | 50.0 | 13.3 | 62.5 | 48.3 | 13.3 | 59.7 | 43.3 | 13.3 | 34.6 |
| InternLM | 68.2 | 48.3 | 70.8 | 61.2 | 37.0 | 55.9 | 50.0 | 3.3 | 60.5 | 51.7 | 6.7 | 61.3 | 75.0 | 50.0 | 68.1 |
| Qwen-VL | 62.5 | 39.3 | 62.0 | 55.7 | 18.3 | 52.4 | 58.3 | 23.3 | 65.7 | 48.3 | 16.7 | 53.7 | 93.3 | 86.7 | 92.9 |
| VisualGLM | 46.3 | 5.3 | 50.9 | 43.3 | 0.3 | 45.0 | 50.0 | 0.0 | 66.7 | 50.0 | 0.0 | 66.7 | 30.0 | 13.3 | 36.3 |
| Gemini | 65.7 | 46.0 | 64.1 | 60.0 | 33.7 | 63.2 | 56.7 | 16.7 | 67.5 | 53.3 | 10.0 | 66.7 | 53.3 | 13.3 | 33.3 |
| GPT-4V | 66.7 | 47.3 | 66.1 | 59.8 | 34.3 | 55.8 | 61.7 | 33.3 | 66.7 | 53.3 | 20.0 | 62.5 | 95.0 | 90.0 | 94.7 |

![The performance variation (before and after image concatenation) in five annotated attributes.](../images/Hallu-PI_md_images/figs/five_aspects_2.png)
Figure source: `../sources/Hallu-PI_source/figs/five_aspects_2.pdf`

**Figure 5.** The performance variation (before and after image concatenation) in five annotated attributes.

**Discriminative Task Results**. Table 5 highlights the model performance on discriminative tasks under image concatenation, cropping, and prompt misleading perturbations. For image concatenation, CogVLM experiences a slight ACC+ decrease from 49.0 to 42.0, while LLaVA1.5 drops drastically from 43.0 to 8.0, indicating high sensitivity. For image cropping, most models, including LLaVA, MiniGPT-4, and mPLUG2, exhibit random guessing ACC (around 50.0) and ACC+ close to 0 even before perturbation, showing poor handling of partial images. Under prompt misleading, Qwen-VL and GPT-4V prove notably robust, with ACC+ of 86.7 and 90.0, respectively, and F1 scores above 90, while LLaVA1.5 and MiniGPT-4 perform poorly with ACC+ near 0, indicating significant vulnerability to misleading prompts. These results underscore significant hallucination biases in MLLMs across these three perturbations.

![We explore two baselines for Hallu-PI: (a) Perturbed-Reminder, which increases the focus of MLLMs on the image content itself by injecting a perturbation reminder into the prompt. (b) Perturbed-ICL, which guides the model to respond correctly when faced with the actual user inputs by adding perturbed demonstrations to the context.](../images/Hallu-PI_md_images/figs/perturbed_baseline.png)
Figure source: `../sources/Hallu-PI_source/figs/perturbed_baseline.pdf`

**Figure 6.** We explore two baselines for Hallu-PI: (a) Perturbed-Reminder, which increases the focus of MLLMs on the image content itself by injecting a perturbation reminder into the prompt. (b) Perturbed-ICL, which guides the model to respond correctly when faced with the actual user inputs by adding perturbed demonstrations to the context.

|   | Noise | Noise | Blur | Blur | Weather | Weather | Digital | Digital | Concat | Concat | Crop | Crop | Mislead | Mislead |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   | ACC+ ↑ | Hal ↓ | ACC+ ↑ | Hal ↓ | ACC+ ↑ | Hal ↓ | ACC+ ↑ | Hal ↓ | ACC+ ↑ | Hal ↓ | ACC+ ↑ | Hal ↓ | ACC+ ↑ | Hal ↓ |   |
| w/o | 42.3 | 54.2 | 41.8 | 54.6 | 40.1 | 56.7 | 34.0 | 61.7 | 34.3 | 98.3 | 20.0 | 73.3 | 90.0 | 3.3 |   |
| ICL | 47.6 | 54.2 | 47.8 | 56.2 | 48.2 | 57.5 | 44.5 | 59.6 | 43.0 | 65.0 | 30.0 | 67.0 | 93.3 | 0.0 |   |
| Reminder | 49.0 | 51.2 | 49.3 | 46.7 | 50.5 | 49.6 | 42.2 | 54.6 | 46.0 | 40.0 | 36.6 | 70.0 | 96.6 | 1.1 |   |

## 5.3 Experimental Analysis

**Analysis of perturbation scenarios**. The PI-Score results presented in Table 3 reveal that under the three constructed scenarios, the performance of most MLLMs experiences a decline when the inputs are perturbed. Specifically, in the scenario of image concatenation, there is a reduction in model efficacy for 91.7% (11 out of 12). For image cropping, this figure stands at 83.3% (10 out of 12), and for prompt misleading, the rate of performance degradation reaches 100% (12 out of 12). Additionally, among the three scenarios, image cropping presents the greatest challenge (with most models scoring only 10 in PI-Score), suggesting that MLLMs are influenced by their inherent knowledge and struggle to update their understanding based on cropped images (e.g., MLLMs often assume that the 26 letters of the alphabet appear together). Prompt misleading is the scenario where the performance drop before and after perturbation is most significant (e.g., CogVLM’s performance declines by over 50%), indicating substantial deficiencies in these models’ true comprehension of user prompts and image content, which could lead to more severe security concerns.

**Analysis of specific attribute performance**. Figure 5 illustrates the performance change of MLLMs on each annotated attribute before and after perturbation in the image concatenation scenario. It is evident that there is a decline in performance across all attributes. Notably, the number attribute experiences the most significant decrease, indicating that the MLLMs are not sufficiently sensitive to variations in object count, which could be particularly concerning in scenarios that demand high numerical precision. Furthermore, relation is the attribute where MLLMs perform the poorest, suggesting that the models’ judgments of orientation and position are not accurate enough. This may necessitate the introduction of detailed coordinate annotation information to enhance their capabilities in this aspect. See supplementary material for further analysis.

## 5.4 How to Mitigate Hallucinations Induced by Hallu-PI?

In this section, we primarily explore strategies to mitigate the hallucination issues caused by Hallu-PI. We posit that hallucinations in MLLMs also constitute a safety concern, which could lead to severe hazards in specific contexts, such as autonomous driving (Q. Huang et al. 2023). Therefore, drawing inspiration from works on jailbreaking and securing text LLMs (Ding et al. 2023; Wu et al. 2023), we design two specific baselines for perturbed scenarios, namely Perturbed-Reminder and Perturbed-ICL, which we detail in the subsequent sections.

**Perturbed-Reminder**. Previous works have demonstrated that appending a specific safety-reminder prompt (Wu et al. 2023) to the prefix of user requests can effectively defend against jailbreak attacks targeting text LLMs. This is because such safety reminders cause the model to pay closer attention to specific parts of the user input, thereby more accurately filtering out harmful requests (Ding et al. 2023). Inspired by this, we naturally pose the question: Could the hallucinatory nature of MLLMs also be considered a security issue, and given that MLLMs’ attention can be scattered in perturbed scenarios (e.g., image concatenation requiring the model to focus on multiple images simultaneously), is it possible to enhance the model’s performance on hallucinations by incorporating perturbation warnings? Consequently, we introduce the concept of Perturbed-Reminder, as shown in Figure 6 (a), where we prepend a hallucination reminder to the user’s prompt, thereby explicitly directing the model’s focus and attention towards the images themselves.

**Perturbed-ICL**. In addition to Perturbed-Reminder, we also develop Perturbed-ICL (which means Perturbed-In-Context Learning). In-context learning (Dong et al. 2022) has been proven to enhance the capabilities of LLMs (such as reasoning abilities). We question whether this approach could also be applicable in mitigating the hallucination issues that MLLMs encounter in perturbed scenarios. Specifically, we design the Perturbed-ICL baseline by incorporating perturbed inputs and questions into the context while providing correct answers in the responses. (see Figure 6 (b)). The objective is to determine if the model can learn from contextual demonstrations (explicitly informing MLLMs of input perturbations) when faced with actual user inputs, thereby mitigating the effects of these perturbations.

**Table 6.** The results of Perturbed-ICL and Perturbed-Reminder on GPT-4V. `w/o` represents without baseline improvement.

The results in Table 6 suggest that both Perturbed-Reminder and Perturbed-ICL baselines are effective to some extent in reducing hallucinations in GPT-4V under perturbed scenarios. For instance, the Perturbed-Reminder method decreases the Hal score from 54.6% to 46.7% in the Blur scenario. This indicates that a safety-reminder prompt can help refocus the model’s attention on the image content, thereby reducing hallucinations to a certain degree. Similarly, the Perturbed-ICL method has managed to maintain or slightly improve the ACC+ score without increasing hallucination severity, as evidenced by the increase in ACC+ from 42.3% to 47.6% in the Noise scenario. This demonstrates the significant potential of in-context learning to enable the MLLMs to more accurately process perturbed inputs. Despite these methods showing effectiveness, results in Table 6 indicate that mitigating hallucinations in MLLMs within perturbed inputs remains a persistent and challenging issue.

| Method | Noise ACC+ | Noise Hal | Blur ACC+ | Blur Hal | Weather ACC+ | Weather Hal | Digital ACC+ | Digital Hal | Concat ACC+ | Concat Hal | Crop ACC+ | Crop Hal | Mislead ACC+ | Mislead Hal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| w/o | 42.3 | 54.2 | 41.8 | 54.6 | 40.1 | 56.7 | 34.0 | 61.7 | 34.3 | 98.3 | 20.0 | 73.3 | 90.0 | 3.3 |
| ICL | 47.6 | 54.2 | 47.8 | 56.2 | 48.2 | 57.5 | 44.5 | 59.6 | 43.0 | 65.0 | 30.0 | 67.0 | 93.3 | 0.0 |
| Reminder | 49.0 | 51.2 | 49.3 | 46.7 | 50.5 | 49.6 | 42.2 | 54.6 | 46.0 | 40.0 | 36.6 | 70.0 | 96.6 | 1.1 |

# 6. Conclusion

In this paper, we introduce Hallu-PI, the first benchmark designed to evaluate hallucination in MLLMs within perturbed inputs. Hallu-PI consists of seven perturbed scenarios, containing 1,260 perturbed images from 11 object types. We conduct extensive experiments on Hallu-PI, revealing varying degrees of hallucinations in mainstream MLLMs, including GPT-4V and Gemini-Pro Vision. Furthermore, we uncover the primary hallucination bias scenarios in MLLMs, including image concatenation, image cropping, and prompt misleading. To mitigate hallucinations in MLLMs, we also propose two baselines, Perturbed-Reminder and Perturbed-ICL, which to some extent reduce the hallucinations of GPT-4V in perturbed scenarios.

We would like to thank the anonymous reviewers for their insightful comments. Shujian Huang is the corresponding author. This work is supported by National Science Foundation of China(No. 62376116, 62176120).

# 7. More Details of Hallu-PI

**Image Sources**. We ask annotators to download images from the following websites, which offer high-quality images that are free to download, available for commercial use, and do not require any licensing fees. (1) <https://www.pexels.com/zh-cn> (2) <https://pixabay.com/zh/images/search> (3) <https://www.hippopx.com> (4) <https://stocksnap.io>

**Annotation for Image Cropping Scenario**. For image cropping scenario, we primarily investigate the robustness in MLLMs ability to count the letters number within cropped images. Therefore, we have annotators collect images containing common English words, crop them, and annotate the number of English letters present before and after cropping. Subsequently, we obtain responses from MLLMs through the prompt, “*How many English letters are there in the image?*"

**Annotation for Prompt Misleading Scenario**. For prompt misleading scenario, we ask annotators to manually craft prompts intended to induce MLLMs to generate content that does not align with the given images. For example, given an image containing only apples and bananas, a misleading prompt might be: “*Besides apples and bananas, there are two other types of fruit in the image. What are they?*"

![Examples of images with noise, blur, weather, and digital perturbations.](../images/Hallu-PI_md_images/figs/other_perturbation.png)
Figure source: `../sources/Hallu-PI_source/figs/other_perturbation.pdf`

**Figure 7.** Examples of images with noise, blur, weather, and digital perturbations.

**Other Perturbation Examples**. In Figure 7, we provide four additional examples of perturbations in Hallu-PI, including noise, blur, weather, and digital.

**Prompt Templates**. In Figure 10, we provide the prompt templates used in Hallu-PI.

**Details about the MLLMs used in Hallu-PI**. We provide a detailed introduction of the MLLMs evaluated by Hallu-PI in Table 9, including model parameters and architectures.

# 8. Experimental Details

## 8.1 Perturbation Intensity Selection

Real-world perturbations can manifest themselves at varying intensities. In previous work (Qiu et al. 2023), they designed five levels of severity for each perturbation scenario. Hallu-PI, however, focuses more on the specific perturbation itself rather than its intensity. Therefore, we randomly select an intensity level between 1 and 5 for noise, blur, weather, and digital perturbations. We will leave the discussion and analysis of different perturbation intensities for future work.

## 8.2 Specific Perturbation Method Selection

As introduced in Section 3.2 of our paper, we follow (Qiu et al. 2023) and reuse the four types of perturbation scenarios from their paper: noise, blur, weather, and digital. The specific algorithms for these perturbation scenarios are detailed in Section 2.3 (Related Work) of our paper. During our experiments, we chose the most representative perturbation algorithms for the Hallu-PI scenarios. Specifically, we select gaussian noise, defocus blur, fog weather perturbation, and pixelation for the digital perturbation. Similarly, we will further explore the impact of different perturbation algorithms on hallucination in MLLMs in future work.

## 8.3 Improvement in Metrics Post-Perturbation

It is worth noting that some metrics in our paper exhibit a slight improvement post-perturbation compared to pre-perturbation. These are rare occurrences and usually appear in simple perturbation scenarios, as exemplified in Figure 7, where the images undergo minimal changes after perturbation. However, for more complex perturbations such as image concatenation, image cropping, and prompt misleading, the metrics generally tend to deteriorate.

# 9. Additional Analysis

## 9.1 Analysis of Cropping and Misleading

Figure 8 illustrates the comparative performance of MLLMs before and after image cropping. GPT-4V (Achiam et al. 2023) and Google Gemini-Pro Vision (Team et al. 2023) exhibit better performance compared to other models. However, all models, including GPT-4V and Gemini, exhibit a significant performance decline when evaluated on cropped images.

Figure 9 depicts the robustness of MLLMs under the prompt misleading scenario. A higher score indicates better robustness of the model. It is observed that GPT-4V, Qwen-VL-Chat (Bai et al. 2023), and Gemini exhibit higher robustness compared to other MLLMs. However, it is concerning that a greater number of models struggle to identify misleading prompts, which could lead to more severe hallucinations during multi-turn dialogues.

![Performance of MLLMs before and after Cropping.](../images/Hallu-PI_md_images/figs/cropping_comparison.png)
Figure source: `../sources/Hallu-PI_source/figs/cropping_comparison.pdf`

**Figure 8.** Performance of MLLMs before and after Cropping.

![The hallucination of MLLMs under the prompt misleading scenario, the smaller the score, the more severe the hallucination.](../images/Hallu-PI_md_images/figs/misleading_comparison.png)
Figure source: `../sources/Hallu-PI_source/figs/misleading_comparison.pdf`

**Figure 9.** The hallucination of MLLMs under the prompt misleading scenario, the smaller the score, the more severe the hallucination.

## 9.2 Analysis of PI-Score

To validate the effectiveness of our proposed PI-Score, we sample 100 images from Hallusionbench (Guan et al. 2024) and calculate the PI-Score on 5 representative MLLMs (see Table 7, left). We extend our findings to Hallusionbench and observe consistent results with those obtained on Hallu-PI, demonstrating the model’s vulnerability in perturbed scenarios and the effectiveness of the PI-Score.

## 9.3 Analysis of Additional Perturbation

To further enhance the generalizability of Hallu-PI, we add a common image augmentation perturbation, "shearing" (Cubuk et al. 2020) (see Table 7, right), applied to a sample of 100 CIFAR-10 images. We observe that several representative MLLMs exhibit more severe hallucinations after the perturbation.

## 9.4 Results Before Perturbation for Prompt Misleading

In our paper, we present the results of the prompt misleading discriminative task post-perturbation, aimed at revealing the severe hallucinations it induces. To better illustrate this effect, we also design pre-perturbation prompts (see Figure 10). The experimental results are shown in Table 8: LLaVA-1.5 experiences the most significant performance decline, while GPT-4V shows more robustness and achieves the highest scores. This, in combination with the results in Table 5 of our paper, more clearly demonstrates the hallucination biases of MLLMs in prompt misleading scenarios.

**Table 7.** PI-Score on HallusionBench (left) and Top-1 error of "shearing" perturbation (right).

| Models | Hallusionbench-PI score ↑ | Hallusionbench-PI score ↑ | Shearing-Top 1 error ↓ | Shearing-Top 1 error ↓ |
| --- | --- | --- | --- | --- |
| 2-5 | Before | After | Before | After |
| LLaVA | 29.0 | 18.0 | 13.0 | 25.0 |
| LLaVA-1.5 | 30.5 | 23.4 | 9.0 | 20.0 |
| Qwen-VL | 43.0 | 19.4 | 18.0 | 38.0 |
| Gemini | 37.5 | 18.6 | 12.0 | 33.0 |
| GPT-4V | 40.7 | 21.9 | 8.0 | 31.0 |

**Table 8.** The before and after results of prompt misleading.

| Models | Prompt Misleading | Prompt Misleading | Prompt Misleading | Prompt Misleading | Prompt Misleading | Prompt Misleading |
| --- | --- | --- | --- | --- | --- | --- |
| 2-7 | Before | Before | Before | After | After | After |
| 2-7 | ACC ↑ | ACC+ ↑ | F1 ↑ | ACC ↑ | ACC+ ↑ | F1 ↑ |
| LLaVA | 60.0 | 26.7 | 70.2 | 1.7 | 0.0 | 3.2 |
| LLaVA-1.5 | 98.3 | 96.7 | 98.3 | 40.0 | 3.3 | 5.2 |
| Qwen-VL | 96.7 | 93.3 | 96.8 | 93.3 | 86.7 | 92.9 |
| Gemini | 98.3 | 96.7 | 98.3 | 53.3 | 13.3 | 33.3 |
| GPT-4V | 98.3 | 96.7 | 98.3 | 95.0 | 90.0 | 94.7 |

**Table 9.** The architecture and parameters of MLLMs evaluated by Hallu-PI.

| MLLMs | Vision Encoder (VE) | Parameters of VE | Language Model (LM) | Parameters of LM | Source |
|:---|:---|:---|:---|:---|:--:|
| CogVLM | EVA2-CLIP-E | 4.7B | Vicuna-v1.5 | 7B | Official Code |
| InternLM-Xcomposer-VL | EVA-CLIP-G | 1.1B | InternLM | 7B | Official Code |
| LLaVA | ViT-L/14 | 0.4B | LLaMA-2-Chat-13B | 13B | Official Code |
| LLaVA1.5 | ViT-L/14-336px | 0.4B | Vicuna-v1.5 | 7B | Official Code |
| MiniGPT-4 | BLIP2-Qformer | 1.9B | Vicuna-v0 | 7B | Official Code |
| MiniGPT-v2 | EVA-CLIP-G | 1.1B | LLaMA-2-Chat-7B | 7B | Official Code |
| mPLUG-Owl-2 | ViT-L/14 | 0.4B | LLaMA-2-Chat-7B | 7B | Official Code |
| MultimodalGPT | ViT-L/14 | 0.4B | LLaMA-13B | 13B | Official Code |
| Qwen-VL-Chat | ViT-G/14 | 1.9B | Qwen-7B | 7.7B | Official Code |
| VisualGLM | BLIP2-Qformer | 1.9B | ChatGLM-6B | 6B | Official Code |
| Google Gemini-Pro Vision | Unknown | Unknown | Gemini-Pro | Unknown | API |
| GPT-4V | Unknown | Unknown | GPT4 | Unknown | API |

![The prompt templates used in Hallu-PI include those for generative task and discriminative task, as well as prompts before and after perturbations.](../images/Hallu-PI_md_images/figs/prompt_templates.png)
Figure source: `../sources/Hallu-PI_source/figs/prompt_templates.pdf`

**Figure 10.** The prompt templates used in Hallu-PI include those for generative task and discriminative task, as well as prompts before and after perturbations.

![Some case studies of perturbation scenarios include image concatenation, image cropping, and prompt misleading. MLLMs adopt CogVLM2-Chat-En (W. Wang et al. 2023), which can be accessed at http://36.103.203.44:7861.](../images/Hallu-PI_md_images/figs/case_study.png)
Figure source: `../sources/Hallu-PI_source/figs/case_study.pdf`

Representative case studies for these perturbation scenarios are shown in Figure 11.

**Figure 11.** Some case studies of perturbation scenarios include image concatenation, image cropping, and prompt misleading. MLLMs adopt CogVLM2-Chat-En (W. Wang et al. 2023), which can be accessed at http://36.103.203.44:7861.

Achiam, Josh, Steven Adler, Sandhini Agarwal, et al. 2023. “Gpt-4 Technical Report.” *arXiv Preprint arXiv:2303.08774*.

Alayrac, Jean-Baptiste, Jeff Donahue, Pauline Luc, et al. 2022. “Flamingo: A Visual Language Model for Few-Shot Learning.” *Advances in Neural Information Processing Systems* 35: 23716–36.

Bai, Jinze, Shuai Bai, Shusheng Yang, et al. 2023. “Qwen-Vl: A Frontier Large Vision-Language Model with Versatile Abilities.” *arXiv Preprint arXiv:2308.12966*.

Bird, Steven, Ewan Klein, and Edward Loper. 2009. *Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit*. " O’Reilly Media, Inc.".

Chen, Jun, Deyao Zhu, Xiaoqian Shen, et al. 2023. “Minigpt-V2: Large Language Model as a Unified Interface for Vision-Language Multi-Task Learning.” *arXiv Preprint arXiv:2310.09478*.

Chen, Shuo, Zhen Han, Bailan He, et al. 2024. “Red Teaming GPT-4V: Are GPT-4V Safe Against Uni/Multi-Modal Jailbreak Attacks?” *arXiv Preprint arXiv:2404.03411*.

Cubuk, Ekin D, Barret Zoph, Jonathon Shlens, and Quoc V Le. 2020. “Randaugment: Practical Automated Data Augmentation with a Reduced Search Space.” *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops*, 702–3.

Ding, Peng, Jun Kuang, Dan Ma, et al. 2023. “A Wolf in Sheep’s Clothing: Generalized Nested Jailbreak Prompts Can Fool Large Language Models Easily.” *arXiv Preprint arXiv:2311.08268*.

Dong, Qingxiu, Lei Li, Damai Dai, et al. 2022. “A Survey on in-Context Learning.” *arXiv Preprint arXiv:2301.00234*.

Driess, Danny, Fei Xia, Mehdi SM Sajjadi, et al. 2023. “Palm-e: An Embodied Multimodal Language Model.” *arXiv Preprint arXiv:2303.03378*.

Du, Zhengxiao, Yujie Qian, Xiao Liu, et al. 2021. “Glm: General Language Model Pretraining with Autoregressive Blank Infilling.” *arXiv Preprint arXiv:2103.10360*.

Fu, Chaoyou, Peixian Chen, Yunhang Shen, et al. 2023. “Mme: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models.” *arXiv Preprint arXiv:2306.13394*.

Geirhos, Robert, Patricia Rubisch, Claudio Michaelis, Matthias Bethge, Felix A Wichmann, and Wieland Brendel. 2018. “ImageNet-Trained CNNs Are Biased Towards Texture; Increasing Shape Bias Improves Accuracy and Robustness.” *arXiv Preprint arXiv:1811.12231*.

Gong, Tao, Chengqi Lyu, Shilong Zhang, et al. 2023. “Multimodal-Gpt: A Vision and Language Model for Dialogue with Humans.” *arXiv Preprint arXiv:2305.04790*.

Guan, Tianrui, Fuxiao Liu, Xiyang Wu, et al. 2024. “HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models.” *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 14375–85.

Gunjal, Anisha, Jihan Yin, and Erhan Bas. 2023. “Detecting and Preventing Hallucinations in Large Vision Language Models.” *arXiv Preprint arXiv:2308.06394*.

Hendrycks, Dan, and Thomas Dietterich. 2019. “Benchmarking Neural Network Robustness to Common Corruptions and Perturbations.” *arXiv Preprint arXiv:1903.12261*.

Huang, Lei, Weijiang Yu, Weitao Ma, et al. 2023. “A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions.” *arXiv Preprint arXiv:2311.05232*.

Huang, Qidong, Xiaoyi Dong, Pan Zhang, et al. 2023. “OPERA: Alleviating Hallucination in Multi-Modal Large Language Models via over-Trust Penalty and Retrospection-Allocation.” *arXiv Preprint arXiv:2311.17911*.

Ji, Ziwei, Nayeon Lee, Rita Frieske, et al. 2023. “Survey of Hallucination in Natural Language Generation.” *ACM Computing Surveys* 55 (12): 1–38.

Li, Bohao, Rui Wang, Guangzhi Wang, Yuying Ge, Yixiao Ge, and Ying Shan. 2023. “Seed-Bench: Benchmarking Multimodal Llms with Generative Comprehension.” *arXiv Preprint arXiv:2307.16125*.

Li, Junnan, Dongxu Li, Silvio Savarese, and Steven Hoi. 2023. “Blip-2: Bootstrapping Language-Image Pre-Training with Frozen Image Encoders and Large Language Models.” *arXiv Preprint arXiv:2301.12597*.

Li, Junyi, Jie Chen, Ruiyang Ren, et al. 2024. “The Dawn After the Dark: An Empirical Study on Factuality Hallucination in Large Language Models.” *arXiv Preprint arXiv:2401.03205*.

Li, Yifan, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin Zhao, and Ji-Rong Wen. 2023. “Evaluating Object Hallucination in Large Vision-Language Models.” *arXiv Preprint arXiv:2305.10355*.

Liu, Fuxiao, Kevin Lin, Linjie Li, Jianfeng Wang, Yaser Yacoob, and Lijuan Wang. 2023. “Aligning Large Multi-Modal Model with Robust Instruction Tuning.” *arXiv Preprint arXiv:2306.14565*.

Liu, Haotian, Chunyuan Li, Yuheng Li, and Yong Jae Lee. 2023. “Improved Baselines with Visual Instruction Tuning.” *arXiv Preprint arXiv:2310.03744*.

Liu, Haotian, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. 2023. “Visual Instruction Tuning.” *arXiv Preprint arXiv:2304.08485*.

Liu, Yuan, Haodong Duan, Yuanhan Zhang, et al. 2023. “Mmbench: Is Your Multi-Modal Model an All-Around Player?” *arXiv Preprint arXiv:2307.06281*.

Michaelis, Claudio, Benjamin Mitzkus, Robert Geirhos, et al. 2019. “Benchmarking Robustness in Object Detection: Autonomous Driving When Winter Is Coming.” *arXiv Preprint arXiv:1907.07484*.

Qiu, Jielin, Yi Zhu, Xingjian Shi, et al. 2023. “Benchmarking Robustness of Multimodal Image-Text Models Under Distribution Shift.” *Journal of Data-Centric Machine Learning Research*.

Team, Gemini, Rohan Anil, Sebastian Borgeaud, et al. 2023. “Gemini: A Family of Highly Capable Multimodal Models.” *arXiv Preprint arXiv:2312.11805*.

Tong, Shengbang, Zhuang Liu, Yuexiang Zhai, Yi Ma, Yann LeCun, and Saining Xie. 2024. “Eyes Wide Shut? Exploring the Visual Shortcomings of Multimodal Llms.” *arXiv Preprint arXiv:2401.06209*.

Wang, Junyang, Yuhang Wang, Guohai Xu, et al. 2023. “An Llm-Free Multi-Dimensional Benchmark for Mllms Hallucination Evaluation.” *arXiv Preprint arXiv:2311.07397*.

Wang, Junyang, Yiyang Zhou, Guohai Xu, et al. 2023. “Evaluation and Analysis of Hallucination in Large Vision-Language Models.” *arXiv Preprint arXiv:2308.15126*.

Wang, Weihan, Qingsong Lv, Wenmeng Yu, et al. 2023. “Cogvlm: Visual Expert for Pretrained Language Models.” *arXiv Preprint arXiv:2311.03079*.

Wu, Fangzhao, Yueqi Xie, Jingwei Yi, et al. 2023. *Defending Chatgpt Against Jailbreak Attack via Self-Reminder*.

Ye, Hongbin, Tong Liu, Aijia Zhang, Wei Hua, and Weiqiang Jia. 2023. “Cognitive Mirage: A Review of Hallucinations in Large Language Models.” *arXiv Preprint arXiv:2309.06794*.

Ye, Qinghao, Haiyang Xu, Jiabo Ye, et al. 2023. “Mplug-Owl2: Revolutionizing Multi-Modal Large Language Model with Modality Collaboration.” *arXiv Preprint arXiv:2311.04257*.

Yin, Shukang, Chaoyou Fu, Sirui Zhao, et al. 2023. “Woodpecker: Hallucination Correction for Multimodal Large Language Models.” *arXiv Preprint arXiv:2310.16045*.

Zhai, Bohan, Shijia Yang, Xiangchen Zhao, et al. 2023. “HallE-Switch: Rethinking and Controlling Object Existence Hallucinations in Large Vision Language Models for Detailed Caption.” *arXiv Preprint arXiv:2310.01779*.

Zhang, Pan, Xiaoyi Dong Bin Wang, Yuhang Cao, et al. 2023. “Internlm-Xcomposer: A Vision-Language Large Model for Advanced Text-Image Comprehension and Composition.” *arXiv Preprint arXiv:2309.15112*.

Zhou, Yiyang, Chenhang Cui, Jaehong Yoon, et al. 2023. “Analyzing and Mitigating Object Hallucination in Large Vision-Language Models.” *arXiv Preprint arXiv:2310.00754*.

Zhu, Deyao, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. 2023. “Minigpt-4: Enhancing Vision-Language Understanding with Advanced Large Language Models.” *arXiv Preprint arXiv:2304.10592*.
