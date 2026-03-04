# Knowledge-Markdown

Personal knowledge base — AI engineering notes, API references, and practical guides.

> 中文版目录：[README_zh.md](README_zh.md)

## Bilingual Convention

All notes are maintained in both English and Chinese.

| File | Language |
|------|----------|
| `<name>.md` | English (primary) |
| `<name>_zh.md` | Chinese |

Both files are kept in the same directory for easy side-by-side editing. This index links English files only — see [README_zh.md](README_zh.md) for the Chinese index.

## Directory Structure

```
Knowledge-Markdown/
├── README.md                    # English master index (this file)
├── README_zh.md                 # Chinese master index
│
├── Agent_Skills/                # Building custom skills for Claude Code
│   ├── The-Complete-Guide-to-Building-Skill-for-Claude.md
│   └── The-Complete-Guide-to-Building-Skill-for-Claude_zh.md
│
├── Agent_Memory/                # Foundation Agent Memory — English (survey + structured notes)
│   ├── README.md                # Knowledge base index & navigation
│   ├── 00_survey-overview.md    # Paper metadata, abstract, structure map
│   ├── 01_background.md         # Foundation agents, memory concepts, cognitive science roots
│   ├── 02_taxonomy/             # Three-dimensional memory taxonomy
│   │   ├── README.md
│   │   ├── 2.1_memory-substrates.md      # External vs Internal storage
│   │   ├── 2.2_cognitive-mechanisms.md   # Sensory/Working/Episodic/Semantic/Procedural
│   │   └── 2.3_memory-subjects.md        # User-centric vs Agent-centric
│   ├── 03_operations/           # Memory operations (single & multi-agent)
│   │   ├── single-agent-operations.md
│   │   └── multi-agent-operations.md
│   ├── 04_learning-policy.md    # Prompting / Fine-tuning / RL for memory
│   ├── 05_scaling.md            # Context explosion & real-world scaling
│   ├── 06_evaluation.md         # Metrics + 30+ benchmarks
│   ├── 07_applications.md       # 11 application domains
│   └── 08_future-directions.md  # 6 open challenges
│
├── Agent_Memory_zh/             # Foundation Agent Memory — Chinese translation
│   └── (mirrors Agent_Memory/ structure)
│
├── Self_Evolve/                 # Self-Evolving Agents — English (survey + structured notes)
│   ├── README.md                # Knowledge base index & navigation
│   ├── 00_survey-overview.md    # Paper metadata, taxonomy, key results
│   ├── 01_background.md         # Preliminaries: agent definition, MDP, problem framing
│   ├── 02_model-centric/        # Section III: Model-Centric Self-Evolution
│   │   ├── README.md
│   │   ├── 2.1_inference-based.md  # Parallel sampling, self-correction, structured reasoning
│   │   └── 2.2_training-based.md   # Synthesis-driven offline, exploration-driven online
│   ├── 03_env-centric/          # Section IV: Environment-Centric Self-Evolution
│   │   ├── README.md
│   │   ├── 3.1_static-knowledge.md   # Agentic RAG, Deep Research
│   │   ├── 3.2_dynamic-experience.md # Offline/Online/Lifelong experience evolution
│   │   ├── 3.3_modular-arch.md       # Interaction protocols, memory arch, tool-augmented
│   │   └── 3.4_agentic-topology.md   # Offline search, runtime adaptation, structural state
│   ├── 04_co-evolution.md       # Section V: Model-Environment Co-Evolution
│   ├── 05_applications.md       # Section VI: Science, Software Engineering, Open-World
│   ├── 06_challenges.md         # Section VII: Discussion, Challenges, Future Frontiers
│   └── 07_benchmarks.md         # Sections VIII–IX: Benchmarks + OSS libraries
│
├── Self_Evolve_zh/              # Self-Evolving Agents — Chinese translation
│   └── (mirrors Self_Evolve/ structure)
│
├── GUI_Agent/                   # LLM-based GUI Agent — English (survey + structured notes)
│   ├── README.md                # Knowledge base index & navigation
│   ├── 00_survey-overview.md    # Paper metadata, taxonomy, structure map
│   ├── 01_background.md         # LLM, MLLM, LLM-based Agent concepts
│   ├── 02_capabilities/         # 5 core capabilities of GUI Agent
│   │   ├── README.md
│   │   ├── 2.1_gui-comprehension.md    # Text/Vision/Hybrid GUI understanding
│   │   ├── 2.2_device-control.md       # Code-based vs UI-based control
│   │   ├── 2.3_user-interaction.md     # Single-turn vs task-oriented dialogue
│   │   └── 2.4_advanced-capabilities.md # Personalization + multi-agent synergy
│   ├── 03_task-automation-pipeline.md  # Two-stage pipeline: Exploration → Exploitation
│   ├── 04_evaluation.md         # 24 datasets + evaluation metrics
│   ├── 05_challenges.md         # Cost, feasibility, safety, AIOS connection
│   ├── comparison-matrix.md     # Cross-paper comparison (23 systems)
│   └── gap-tracker.md           # Research gap tracker (5 gaps)
│
├── Claude_API/                  # Claude API features and best practices
│   └── Tool_Use/
│       ├── advanced-tool-use-features.md
│       └── advanced-tool-use-features_zh.md
│
└── Industry_Insights/           # Practitioner perspectives: podcasts, talks, articles
    ├── 2025-12_CUA-Slow-Thinking-Podcast.md     # Computer Use Agent roundtable (Ungrounded Ep.1)
    └── 2025-12_CUA-Slow-Thinking-Podcast_zh.md  # Chinese version
```

## Quick Index

### Agent Skills

| Topic | File | Tags |
|---|---|---|
| The Complete Guide to Building Skills for Claude | [Agent_Skills/The-Complete-Guide-to-Building-Skill-for-Claude.md](Agent_Skills/The-Complete-Guide-to-Building-Skill-for-Claude.md) | skills, slash-commands, claude-code |

### Claude API

| Topic | File | Tags |
|---|---|---|
| Advanced Tool Use Features (PTC, Tool Search, Examples, Dynamic Filtering) | [Claude_API/Tool_Use/advanced-tool-use-features.md](Claude_API/Tool_Use/advanced-tool-use-features.md) | api, tool-use, tokens, performance |

### Agent Memory (English)

| Topic | File | Tags |
|---|---|---|
| Agent Memory Survey — Overview & Index | [Agent_Memory/README.md](Agent_Memory/README.md) | agent-memory, survey, LLM, research |
| Memory Substrates (External/Internal) | [Agent_Memory/02_taxonomy/2.1_memory-substrates.md](Agent_Memory/02_taxonomy/2.1_memory-substrates.md) | memory, RAG, KV-cache, vector-store |
| Cognitive Mechanisms (5 types) | [Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md](Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md) | episodic, semantic, working, procedural |
| Memory Subjects (User-centric / Agent-centric) | [Agent_Memory/02_taxonomy/2.3_memory-subjects.md](Agent_Memory/02_taxonomy/2.3_memory-subjects.md) | user-memory, agent-memory, personalization |
| Memory Operations (single & multi-agent) | [Agent_Memory/03_operations/](Agent_Memory/03_operations/) | operations, multi-agent, routing |
| Memory Learning Policy (Prompting/SFT/RL) | [Agent_Memory/04_learning-policy.md](Agent_Memory/04_learning-policy.md) | learning, RL, fine-tuning, prompting |
| Scaling Challenges | [Agent_Memory/05_scaling.md](Agent_Memory/05_scaling.md) | scaling, context, multi-agent |
| Evaluation Benchmarks (30+ annotated) | [Agent_Memory/06_evaluation.md](Agent_Memory/06_evaluation.md) | benchmarks, evaluation, metrics |
| Applications (11 domains) | [Agent_Memory/07_applications.md](Agent_Memory/07_applications.md) | healthcare, robotics, finance, science |
| Future Research Directions (6 challenges) | [Agent_Memory/08_future-directions.md](Agent_Memory/08_future-directions.md) | research, future, open-problems |

### Self-Evolving Agents (English)

| Topic | File | Tags |
|---|---|---|
| Self-Evolving Agents Survey — Overview & Index | [Self_Evolve/README.md](Self_Evolve/README.md) | self-evolution, survey, LLM, agents |
| Inference-Based Evolution (Test-Time Scaling) | [Self_Evolve/02_model-centric/2.1_inference-based.md](Self_Evolve/02_model-centric/2.1_inference-based.md) | inference, CoT, tree-search, self-correction |
| Training-Based Evolution (SFT/RL) | [Self_Evolve/02_model-centric/2.2_training-based.md](Self_Evolve/02_model-centric/2.2_training-based.md) | self-instruct, STaR, GRPO, WebRL |
| Environment-Centric Evolution | [Self_Evolve/03_env-centric/](Self_Evolve/03_env-centric/) | RAG, experience, memory-arch, MAS-topology |
| Model-Environment Co-Evolution | [Self_Evolve/04_co-evolution.md](Self_Evolve/04_co-evolution.md) | co-evolution, adaptive-curriculum, MARL |
| Applications (Science, SWE, Open-World) | [Self_Evolve/05_applications.md](Self_Evolve/05_applications.md) | science, software-engineering, gaming |
| Challenges & Future Frontiers | [Self_Evolve/06_challenges.md](Self_Evolve/06_challenges.md) | challenges, model-collapse, future-work |
| Benchmarks (40+ annotated) | [Self_Evolve/07_benchmarks.md](Self_Evolve/07_benchmarks.md) | benchmarks, evaluation, SWE-bench, WebArena |

### GUI Agent (English)

| Topic | File | Tags |
|---|---|---|
| GUI Agent Survey — Overview & Index | [GUI_Agent/README.md](GUI_Agent/README.md) | GUI-agent, survey, LLM, task-automation |
| Background: LLM, MLLM, Agent Concepts | [GUI_Agent/01_background.md](GUI_Agent/01_background.md) | LLM, MLLM, transformer, CogAgent |
| GUI Environment Comprehension (3 paradigms) | [GUI_Agent/02_capabilities/2.1_gui-comprehension.md](GUI_Agent/02_capabilities/2.1_gui-comprehension.md) | GUI-understanding, VH, DOM, vision, hybrid |
| Device Control (Code-based vs UI-based) | [GUI_Agent/02_capabilities/2.2_device-control.md](GUI_Agent/02_capabilities/2.2_device-control.md) | device-control, action-space, automation |
| User Interaction (Single-turn vs Dialogue) | [GUI_Agent/02_capabilities/2.3_user-interaction.md](GUI_Agent/02_capabilities/2.3_user-interaction.md) | dialogue, task-oriented, user-interaction |
| Personalization + Multi-Agent Synergy | [GUI_Agent/02_capabilities/2.4_advanced-capabilities.md](GUI_Agent/02_capabilities/2.4_advanced-capabilities.md) | personalization, memory, multi-agent, UFO |
| Task Automation Pipeline (Explore → Exploit) | [GUI_Agent/03_task-automation-pipeline.md](GUI_Agent/03_task-automation-pipeline.md) | two-stage, exploration, exploitation, AppAgent |
| Evaluation: 24 Datasets + Metrics | [GUI_Agent/04_evaluation.md](GUI_Agent/04_evaluation.md) | benchmarks, Mind2Web, WebArena, success-rate |
| Challenges: Cost, Safety, AIOS | [GUI_Agent/05_challenges.md](GUI_Agent/05_challenges.md) | cost, hallucination, security, AIOS |
| Cross-Paper Comparison Matrix (23 systems) | [GUI_Agent/comparison-matrix.md](GUI_Agent/comparison-matrix.md) | comparison, survey, systems |
| Research Gap Tracker (5 gaps) | [GUI_Agent/gap-tracker.md](GUI_Agent/gap-tracker.md) | research-gap, memory, self-evolving |

### Industry Insights

| Topic | File | Tags |
|---|---|---|
| Computer Use Agent: Slow-Thinking Roundtable (Ungrounded Ep.1) | [Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast.md](Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast.md) | CUA, GUI-agent, benchmark, business-model, GenUI, continual-learning, startup |
| Computer Use Agent: Slow-Thinking Roundtable — Chinese | [Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast_zh.md](Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast_zh.md) | CUA, GUI-agent, benchmark, business-model, GenUI, continual-learning, startup |
