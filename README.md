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
├── Agent_skills/                # Building custom skills for Claude Code
│   ├── The-Complete-Guide-to-Building-Skill-for-Claude.md
│   └── The-Complete-Guide-to-Building-Skill-for-Claude_zh.md
│
├── Agent_Memory/                # Foundation Agent Memory (survey + structured notes)
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
└── Claude_API/                  # Claude API features and best practices
    └── Tool_Use/
        ├── advanced-tool-use-features.md
        └── advanced-tool-use-features_zh.md
```

## Quick Index

| Topic | File | Tags |
|---|---|---|
| The Complete Guide to Building Skills for Claude | [Agent_skills/The-Complete-Guide-to-Building-Skill-for-Claude.md](Agent_skills/The-Complete-Guide-to-Building-Skill-for-Claude.md) | skills, slash-commands, claude-code |
| Advanced Tool Use Features (PTC, Tool Search, Examples, Dynamic Filtering) | [Claude_API/Tool_Use/advanced-tool-use-features.md](Claude_API/Tool_Use/advanced-tool-use-features.md) | api, tool-use, tokens, performance |
| Agent Memory Survey — Overview & Index | [Agent_Memory/README.md](Agent_Memory/README.md) | agent-memory, survey, LLM, research |
| Memory Substrates (External/Internal) | [Agent_Memory/02_taxonomy/2.1_memory-substrates.md](Agent_Memory/02_taxonomy/2.1_memory-substrates.md) | memory, RAG, KV-cache, vector-store |
| Cognitive Mechanisms (5 types) | [Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md](Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md) | episodic, semantic, working, procedural |
| Memory Operations (single & multi-agent) | [Agent_Memory/03_operations/](Agent_Memory/03_operations/) | operations, multi-agent, routing |
| Memory Learning Policy (Prompting/SFT/RL) | [Agent_Memory/04_learning-policy.md](Agent_Memory/04_learning-policy.md) | learning, RL, fine-tuning, prompting |
| Evaluation Benchmarks (30+ annotated) | [Agent_Memory/06_evaluation.md](Agent_Memory/06_evaluation.md) | benchmarks, evaluation, metrics |
| Applications (11 domains) | [Agent_Memory/07_applications.md](Agent_Memory/07_applications.md) | healthcare, robotics, finance, science |
| Future Research Directions (6 challenges) | [Agent_Memory/08_future-directions.md](Agent_Memory/08_future-directions.md) | research, future, open-problems |
