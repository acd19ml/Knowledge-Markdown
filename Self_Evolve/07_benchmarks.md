# Benchmarks and Open Source Libraries

> Paper Sections VIII–IX (pages 13–18) | Tables IV–V in paper

---

## Overview

The paper categorizes benchmarks into two dimensions:

1. **Intrinsic Capability Benchmarks** — assess base model reasoning/coding proficiency → primarily for evaluating **Model-Centric** methods
2. **Agentic Reasoning Capabilities Benchmarks** — evaluate evolution through interaction with external worlds → for **Environment-Centric and Co-Evolution** methods

---

## A. Intrinsic Capability Benchmarks

> "These benchmarks primarily evaluate the effectiveness of Model-Centric Self-Evolution methods, focusing on static datasets requiring complex reasoning."

### 1. General Knowledge

| Benchmark | Key Feature | Task Format | Why It Matters |
|---|---|---|---|
| **MMLU-Pro** | 12,000 questions across 14 domains, 10 answer choices (vs 4 in MMLU) | MCQ | Discriminates advanced reasoning; low noise |
| **HotpotQA** | Multi-hop reasoning over Wikipedia | Extractive QA | Requires reasoning across multiple documents + supporting facts |
| **LongBench** | 21 datasets, up to 2M word contexts | Mixed | Tests long-context understanding, extended reasoning |
| **AGIEval** | 20 high-standard admission exams (SAT, LSAT, etc.) | MCQ | Measures human-level cognitive ability |
| **ARC** | Grid-based visual puzzles | Visual grid | Abstract reasoning with minimal examples; fluid intelligence |
| **ARC-AGI** | Grid transformation tasks | Visual | AI-hard but human-easy; measures general intelligence |

### 2. Scientific Reasoning

| Benchmark | Domain | Key Feature |
|---|---|---|
| **GPQA** | Biology, Physics, Chemistry | Google-proof: non-expert + search = 34%; expert = 65% |
| **SuperGPQA** | 285 graduate disciplines | Light industry + agriculture included |
| **SciBench** | Physics/Chemistry/Math | ~700 problems from textbooks; multi-step calculation |
| **ChemBench** | Chemistry | Autonomous lab focus |

### 3. Mathematical Reasoning

| Benchmark | Level | Key Feature |
|---|---|---|
| **MATH** | High school competition | Multi-step; LaTeX format |
| **AIME** | Pre-olympiad competition | Long-chain logical deduction |
| **OlympiadBench** | International olympiad | Bilingual + multimodal (images + text) |
| **GSM8K** | Grade school | Chain-of-thought focus; wide baseline |

### 4. Code Generation

| Benchmark | Key Feature | Evaluation Metric |
|---|---|---|
| **LiveCodeBench** | Contamination-free; live problems from LeetCode/AtCoder | Self-repair, execution, output prediction |
| **BigCodeBench** | 1,140 tasks; 139 libraries across 7 domains | Real-world software development |
| **HumanEval** | 164 hand-written problems with unit tests | pass@k metric |
| **MBPP** | Basic programming semantic understanding | pass@k |
| **EvalPlus** | 80× more test cases than HumanEval | Rigorous correctness |
| **MultiPL-E** | 18+ programming languages | Polyglot evaluation |

---

## B. Agentic Reasoning Capabilities Benchmarks

> "These benchmarks provide dynamic environments for Environment-Centric and Co-Evolution paradigms — they function as gyms providing observations, actions, and feedback signals essential for RL and lifelong evolution."

### Web Navigation and Tool Use

| Benchmark | Key Feature | Agent Capability Tested |
|---|---|---|
| **WebArena** | Fully functional web ecosystem; 800+ long-horizon tasks | Cross-site planning, real web interaction |
| **WebShop** | E-commerce simulation | Decision making, product search |
| **WebVoyager** | End-to-end web agent; screenshot-based | Visual navigation + text interaction |
| **VisualWebArena** | Visual + HTML hybrid interaction | Multimodal web agents |
| **Mind2Web** | Real DOM from 2000+ real-world websites | Generalist web agent |
| **MT-Mind2Web** | Multi-turn instruction following | Conversational web agents |
| **ToolLLM** | 16,000+ real-world APIs | Large-scale API mastery |

### Unified Evaluation Frameworks

| Benchmark | Key Feature | Scope |
|---|---|---|
| **AgentGym** | 14 environments, 89 tasks; unified interface; enables self-evolution via RL | Multi-domain |
| **AgentBoard** | Fine-grained progress feedback; interaction visualization | Partially observable envs |
| **ReasoningGym** | Algorithmic tasks; dynamic generation; cheat-resistant | Logic/reasoning |
| **ALFWorld** | Text-based household tasks; aligns text and embodied envs | Embodied + text |
| **AgentBench** | Comprehensive multi-environment evaluation | Multi-domain |
| **GAIA** | 466 real-world questions; requires multi-capability reasoning + tools | General AI assistant |
| **DeepResearchBench** | Long-form web research + citation evaluation | Research agents |

### Software Engineering and OS Operations

| Benchmark | Key Feature | Task Format |
|---|---|---|
| **SWE-bench** | 2,294 real GitHub issues across 12 Python repos; patch generation | Real codebase navigation |
| **SWE-bench Verified** | 500 human-validated high-quality samples (filtered) | Higher reliability |
| **Terminal-Bench** | Linux terminal tasks (server config, kernel compilation); Docker sandbox | OS-level autonomy |
| **OSWorld** | Cross-app full OS control; GUI interaction | Multi-app desktop tasks |

---

## C. Open Source Libraries (Table V)

> "To facilitate future research and deployment of Self-Evolving Agents, key open-source libraries are summarized by category."

### Foundational Agent Orchestration

| Library | Key Features |
|---|---|
| **LangGraph** | Multi-actor applications with cyclic graphs (overcomes DAG limitations); enables loops, persistent memory, human-in-the-loop |
| **LlamaIndex** | Context-augmented LLM applications; data connectors, index structures, query engines for RAG |
| **AutoGen** | Multi-agent conversations; customizable agents integrating LLMs, tools, human inputs |
| **MetaGPT** | SOPs encoded into LLMs; role-based (PM, Architect, Engineer) software development lifecycle |

### Distributed Training

| Library | Key Features |
|---|---|
| **Megatron-LM** | Ultra-large-scale training; tensor, pipeline, sequence, expert parallelism; FP8 mixed precision |
| **DeepSpeed** | ZeRO Redundancy Optimizer; trains 100B+ parameter models on limited hardware |

### Post-Training and Alignment

| Library | Key Features |
|---|---|
| **slime** | Async RL training framework; server-based rollout; decoupled rollout and training engines across GPUs |
| **VeRL** | ByteDance's HybridFlow-based RL; supports PPO and GRPO; 3D-HybridEngine eliminates memory redundancy |
| **OpenRLHF** | Ray + vLLM based RLHF; supports PPO, DPO, KTO, Rejection Sampling; scales to 70B+ models |
| **TRL** | Hugging Face's full-stack library; SFT, Reward Modeling, PPO, DPO, KTO, GRPO |

### Efficient Fine-tuning

| Library | Key Features |
|---|---|
| **LLaMA Factory** | Code-free WebUI (LlamaBoard); 100+ models; LoRA, QLoRA, PPO, DPO; FlashAttention-2 integration |
| **Unsloth** | 2× faster training; 80% memory reduction for Llama, Mistral, Phi, Gemma; manually derived backprop |

### Inference and Serving

| Library | Key Features |
|---|---|
| **vLLM** | PagedAttention for KV cache; continuous batching, speculative decoding, prefix caching |
| **SGLang** | RadixAttention for aggressive KV cache reuse; structured generation language; fast multi-turn |

---

## Benchmark Selection Guide

### For evaluating Model-Centric methods:
- Reasoning: GPQA, MATH, AIME, OlympiadBench
- Code: LiveCodeBench, BigCodeBench, SWE-bench
- General: MMLU-Pro, HotpotQA, LongBench

### For evaluating Environment-Centric methods:
- Web: WebArena, WebVoyager, Mind2Web
- Tool use: ToolLLM, AgentBench
- Multi-domain: AgentGym, GAIA

### For evaluating Co-Evolution methods:
- Long-horizon: SWE-bench, OSWorld, Terminal-Bench
- Open-world: Custom environments (Minecraft, virtual towns)
- Adaptive: AgentGym (self-evolution via RL support)
