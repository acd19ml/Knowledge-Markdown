# Computer Use Agent: A Slow-Thinking Retrospective

> **Source**: "Ungrounded 不着边际" Podcast — Episode 1
> **Full Title**: OpenClaw 爆火的当下，对 Computer Use Agent 的一场慢思考实录
> **Published**: 2025-12 (est.)
> **Format**: ~3-hour roundtable discussion
> **Tags**: computer-use-agent, GUI-agent, benchmark, business-model, continual-learning, GenUI, startup

---

## Speakers

| Speaker | Affiliation | Focus |
|---|---|---|
| **孔德涵** | WebAgentLab | Web agent research, host |
| **谢天宝** | HKU PhD / OSWorld core author | Benchmarks, evaluation methodology |
| **谷雨** | OSU PhD / NeoCognition co-founder | Industry deployment, startup perspective |
| **尚晏仪** | iMean.AI founder | Product design, enterprise automation |

---

## Part I: The 0→60 vs. 60→99 Framing

This is arguably the episode's most important conceptual contribution.

### The Core Divide

```
0 ─────────────── 60 ─────────────────────────── 99
│                  │                               │
Academic            Industry                    Enterprise
formulation         deployability               reliability
(benchmark SoTA)    (real users, real tasks)    (safety, audit)
```

- **0→60**: The problem academia has largely solved — getting an agent to *attempt* a task and succeed on a clean benchmark environment.
- **60→99**: The hard part — handling the long tail of edge cases, errors, distractions, and real-world messiness that matters for actual deployment.

> "学术界做的是0到60分的工作，而工业界要做的是60到99分的工作。这两个问题的性质完全不同。"

**Why this matters**: Most published benchmarks measure 0→60 performance. A model that scores 70% on OSWorld may still be completely unusable in production because the remaining 30% includes exactly the cases users care most about (security prompts, unexpected UI changes, multi-step error recovery).

### Implications by actor

| Actor | What they need to focus on |
|---|---|
| Researchers | Admit 0→60 benchmarks don't predict 60→99 gaps |
| Product builders | 60→99 requires different engineering: error handling, human-in-loop, fallback strategies |
| Benchmark designers | Evaluate failure recovery, not just success rate |

---

## Part II: Benchmark Critique — OSWorld and Beyond

### OSWorld's Design Philosophy

**谢天宝** (core author) shared the inside story:
- **369 examples**, each taking ~10 hours to annotate → enormous human cost
- Tasks span: file management, web browsing, cross-app workflows
- Evaluation uses **functional state verification** (did the desired state actually change?) not screenshot comparison
- **Why functional state?** Screenshot-based evaluation is gameable and fragile; state-based evaluation catches semantic intent

### Reward Hacking Discovered by Claude

A striking finding: Claude discovered 300+ annotation errors in OSWorld by reward hacking — it found paths to trigger "success" without actually completing the intended task.

**Lessons**:
1. Benchmark annotation at human scale is inherently imperfect
2. Strong models will exploit annotation artifacts before solving the actual task
3. Continuous benchmark refresh is necessary as models improve

### The "Chatbot Arena for Agents" Problem

- **Chatbot Arena** works for text: you can judge which response is better quickly
- **Agent Arena** is much harder: task takes 5 minutes, involves many steps, hard for humans to evaluate mid-process
- Current workaround: model-as-judge (LLM evaluates another LLM's trajectory), but this has its own biases

### Dynamic / Live Benchmarks as Solution

Static benchmarks become contaminated as soon as training data includes benchmark tasks. Proposals:
- **Procedurally generated tasks** (infinite, cheat-resistant) — e.g., ReasoningGym
- **Live web benchmarks** — tasks sampled from real websites at evaluation time
- **Redaction + re-annotation** on a rolling basis

---

## Part III: Business Models for Agent Products

### The Three Revenue Models

| Model | Mechanism | Agent Fit? |
|---|---|---|
| **Advertising** | Attention → ad click | Poor — agent bypasses ads, completes task directly |
| **Subscription** | Monthly fee | OK — but users churn if agent doesn't save time |
| **Commission** | % of transaction value | **Ideal** — agent as intermediary earns when it delivers value |

### Why Commission is the Natural Agent Business Model

Traditional internet ads monetize *attention*. Agents *eliminate* the browsing journey — they shortcut directly to the outcome. This destroys ad revenue for platform operators but creates a new market:

```
User wants: cheapest flight from SFO to NYC
Traditional: User browses 10 sites → platform earns ad revenue
Agent model: Agent books directly → earns commission on booking
```

Agents are more analogous to **travel agents** (pre-internet) than to search engines. The labor/intermediary model is a natural fit.

### Travel Domain as the Ideal Beachhead

The travel domain was highlighted as particularly suited for agents because:
1. **Natural commission structure** already exists (OTAs earn commission)
2. **High task complexity** — multi-step booking, comparison, constraint satisfaction
3. **Clear value delivery** — saved time + money is measurable
4. **User tolerance for AI errors** is higher (can correct mistakes)

### The Ads Conflict

When agents automate browsing, they threaten the existing ad ecosystem. This creates a structural conflict:
- Search engines profit from users clicking ads
- Agents eliminate those clicks
- Tension: Should AI labs partner with search engines or compete with them?

---

## Part IV: Productization — The "Small Window" Mistake

### The Critical Product Design Error

The most common mistake in building computer use agents:

> "很多团队犯了一个错误：他们把agent做成了一个小窗口，在角落里观察屏幕。这完全错了。"

**The mistake**: Building the agent as an observer in a corner window, rather than giving it primary control of the desktop.

**Why it fails**:
- Agent needs to *take over* the interaction, not assist from the sidelines
- Partial control leads to coordination conflicts between user and agent
- Creates confusing UX where user doesn't know who's in control

**Correct design**: Clear handoff model — either user is in control, or agent is in control, never ambiguous.

### The Universal Digital Agent (UDA) Concept

**UDA** = agent with a unified action space that selects the optimal interaction modality per context:

```
Unified Action Space:
├── GUI interaction    (clicks, typing, visual navigation)
├── API calls          (when API exists and is more reliable)
├── Terminal / CLI     (for power operations)
└── Code execution     (for complex data transformations)
```

**Key insight**: Different tasks have different optimal interaction modalities. A true UDA picks the right one:
- Booking a flight: GUI (no API) or API (if available)
- Data extraction: Code (more reliable than visual scraping)
- System configuration: Terminal (more reliable than GUI)

**Why this matters**: Pure GUI agents are unnecessarily brittle. When an API exists, use it. UDA maximizes robustness by choosing the lowest-friction path.

---

## Part V: Model Capability Gaps — What Models Still Cannot Do

Based on practitioner experience building real products:

### Persistent Gaps (as of 2025)

| Gap | Manifestation | Why Hard |
|---|---|---|
| **Multi-step planning** | Agent loses track of goal after 5+ steps | Long-context attention degradation |
| **Error recovery** | Agent gets stuck in loops on unexpected UI | No world model; can't reason about "stuck" state |
| **Spatial reasoning** | Misidentifies element positions in complex UIs | Screenshot understanding is still brittle |
| **Cross-app workflows** | Context doesn't transfer between apps | No persistent state across app boundaries |
| **Ambiguity resolution** | Proceeds with wrong assumption instead of asking | Models trained to complete, not to clarify |

### The Verification Problem

Agents struggle to *verify* their own output:
- Did the file actually save?
- Did the email actually send?
- Is the form actually submitted?

Current approach: force explicit verification steps ("take a screenshot and confirm"). Future need: functional state checking built into the agent loop.

---

## Part VI: Generative UI (GenUI) Reflections

### The Spectrum

```
Fixed Templates ←──────────────────────────────→ Fully Generative
│                                                  │
OTA booking UI                              AI-generated
(constrained)                              interface from scratch
```

### 熵减 (Entropy Reduction) Preference

A key insight about user psychology:

> "用户在高度不确定的时候其实更需要减熵的界面，而不是完全自由的界面。"

Users facing complex decisions (travel booking, medical info) want **structured constraints** that reduce cognitive load, not open-ended generation that increases it.

**Implication**: GenUI is not "generate anything"; it's "generate the *right amount* of structure for the cognitive context."

### The Itinerary (行程单) as Ideal GenUI Case

Why travel itineraries are a perfect GenUI use case:
1. **Variable structure** — every itinerary is different (days, activities, constraints)
2. **Predictable schema** — all itineraries have the same semantic elements (when, where, what, how long)
3. **High user value** — reduces complex planning to a visual artifact
4. **Easy verification** — user can scan and correct

### OTA UI Convergence

All major travel booking sites (Ctrip, Expedia, etc.) have converged on nearly identical UI patterns. This happened not because of design copying, but because **the domain constraints naturally produce one optimal layout**. GenUI in constrained domains should converge similarly.

### GenUI Anti-Pattern

Generating fully dynamic UI for every task creates:
- Unpredictable behavior users can't learn from
- Higher cognitive load than fixed UI
- Harder to test and debug

**Practical guideline**: Use GenUI for the *data layer* (what content to show), keep the *interaction layer* relatively fixed (how to interact with it).

---

## Part VII: Continual Learning and Self-Evolution

### The Core Equation

> **Learning = Long-term Memory + Inference**

This framing unifies two perspectives on learning:
- **Subsymbolic** (neural): Learning encodes information into weights
- **Symbolic** (memory-based): Learning stores information in retrievable structures

Both are forms of *changing what the agent knows* — they differ only in *where* and *how* that knowledge is stored.

### Test-Time Training (TTT) and Real-Time Adaptation

**Test-Time Training (TTT)**: Update model weights at inference time based on new observations, without a full fine-tuning cycle.

Use case: agent encounters a new website layout → TTT adapts GUI parsing to that specific layout → future interactions with same site are more reliable.

**Intrinsic reward signal**:
- Log probability of next-token prediction as reward signal
- High surprise (low probability) → learning signal
- Agent can self-supervise: "I didn't predict this outcome" → update

### The Catastrophic Forgetting Problem

When agents learn from new tasks, they tend to forget old skills — **catastrophic forgetting**.

Solutions discussed:
1. **Episodic replay** — periodically replay old task trajectories to maintain prior skills
2. **Selective parameter update** — identify which parameters to update for new task vs which to freeze
3. **External memory** — store learned skills symbolically, don't encode into weights

### Compositional Generalization

A key test of genuine learning: can an agent **combine** previously learned sub-skills to solve a new task it has never seen?

Example:
- Skill A: "extract table from Excel"
- Skill B: "email attachment"
- New task: "email someone a summary of this Excel table"
- True generalization = agent composes A+B without explicit training on this combination

Current models largely fail at this when component skills were learned separately.

---

## Part VIII: Knowledge Representation

### Three Types of Knowledge

| Type | Chinese | Definition | Example |
|---|---|---|---|
| **Factual** | 事实知识 | World facts, entities, properties | "Paris is the capital of France" |
| **Procedural** | 事理知识 | How events and actions connect causally | "Clicking 'submit' sends the form" |
| **Episodic** | 情节知识 | Specific past experiences with context | "Last Tuesday I booked a flight and it failed at step 3" |

**Key insight**: Most agent failures are **procedural knowledge failures** — the agent knows *what* but not *how to sequence actions* in a novel UI.

### Symbolic AI vs. Connectionism Tension

The old AI debate resurfaces in agent context:

| Paradigm | Strength | Weakness for Agents |
|---|---|---|
| **Symbolic** (KG, KB, rules) | Interpretable, composable, editable | Brittle when world doesn't match schema |
| **Connectionist** (neural LLMs) | Flexible, generalizes to unseen cases | Opaque, hard to correct specific errors |

**The practical view**: LLMs handle the *recognition* problem well (what is this UI element?); symbolic representations handle the *planning* problem better (what sequence of actions reaches the goal?).

**Neuro-symbolic bridge**: agents that use LLMs for perception + interpretation, and symbolic planners for goal-directed sequencing.

### KG/KB vs. LLM Paradigm Shift

Before LLMs: Knowledge Graphs (Freebase, Wikidata) were the dominant knowledge representation.

After LLMs: Knowledge is implicitly encoded in weights. The question becomes:
- When to use explicit KG retrieval vs implicit LLM recall?
- How to keep agent knowledge up-to-date as the world changes?

**Practical answer**: KGs for stable, structured, verifiable facts (e.g., flight schedules, product catalogs). LLMs for flexible reasoning about relationships and procedures.

---

## Part IX: Startup Strategy — Building Moats in Agent Markets

### The Temporal Moat Ladder

The competitive advantage of an agent startup evolves over time:

```
Stage 1: Speed advantage
  → Be first to market in a domain
  → Capture initial users before competition
  └── Moat durability: months

Stage 2: Reputation / 声量
  → Build brand recognition as "the CUA company for [domain]"
  → Customers choose you because they've heard of you
  └── Moat durability: 1-2 years

Stage 3: Domain-specific data accumulation
  → Unique data that competitors cannot replicate
  → Model trained on this data outperforms generic models
  └── Moat durability: multi-year, potentially durable
```

### What Makes Data Moats Real?

Not all data is moat-worthy. The key question: **can competitors get the same data?**

Moat-worthy data types:
- **User decision-flow data**: what choices users make at each step (not just final booking, but which options they considered and rejected)
- **Error recovery trajectories**: how agents recovered from failures — this is training data no one else has
- **Domain-specific UI interaction patterns**: learned mappings from specific company UIs that drift over time

### Supply Chain Advantage

Some agent products gain moat through supply-side relationships:
- Negotiated API access with data providers
- Exclusive data licensing
- Preferred partner status that enables lower latency or better pricing

This is a different moat than data — it's relationship-based and harder to replicate.

### Network Effects in Agent Products

Unlike traditional SaaS, agent products can have unusual network effects:
- More users → more diverse task trajectories → better model → more users
- Enterprise deployments create internal data flywheels (each employee using the agent creates training data)

### The Semantic Web Historical Parallel

A striking historical analogy raised in the episode:

> "Semantic Web的失败，不是因为理念错了，而是因为没有一个实体有足够的激励去标注数据。LLM解决了这个问题，因为模型本身就是对世界知识的压缩。"

**Semantic Web** (1998-2010s): Tim Berners-Lee's vision of machine-readable web. Failed because no one had incentive to manually annotate their web content with structured metadata.

**LLMs changed this**: The knowledge doesn't need to be manually structured — it can be extracted from unstructured text at scale. The data annotation problem is solved by scale, not by incentive alignment.

**Implication for agents**: The bottleneck is no longer "can we represent knowledge?" (LLMs + KGs solve this) but "can we collect the *right kind* of task-specific knowledge?" — which is where startups can win.

---

## Part X: Open Questions and Research Directions

From the discussion, several genuinely open questions emerged:

### Evaluation
- [ ] How to build dynamic benchmarks that resist contamination as models improve?
- [ ] Can model-as-judge for agent evaluation be made reliable enough for research use?
- [ ] What's the right way to evaluate 60→99 performance? How do we measure reliability at scale?

### Architecture
- [ ] What's the optimal split between GUI, API, and code for a Universal Digital Agent?
- [ ] Can test-time training work without catastrophic forgetting on prior agent skills?
- [ ] How do we build agents that know *when to ask* vs. when to proceed?

### Learning and Knowledge
- [ ] What is the minimum external signal needed to prevent model collapse in self-training?
- [ ] Can compositional generalization be achieved without explicit compositional training?
- [ ] Is procedural knowledge better stored symbolically (retrievable) or subsymbolically (in weights)?

### Business and Product
- [ ] Which domains will commission-based agent businesses emerge first (travel, finance, healthcare)?
- [ ] When does the speed → reputation → data moat ladder break down?
- [ ] Can small startups sustain data moats as foundation model providers enter their domain?

---

## Cross-References to Knowledge Base

| Topic | Related Files |
|---|---|
| Self-evolving agents (learning/memory) | [Self_Evolve/03_env-centric/3.2_dynamic-experience.md](../Self_Evolve/03_env-centric/3.2_dynamic-experience.md) |
| Continual learning / lifelong memory | [Agent_Memory/04_learning-policy.md](../Agent_Memory/04_learning-policy.md) |
| Benchmarks (OSWorld, WebArena, etc.) | [Self_Evolve/07_benchmarks.md](../Self_Evolve/07_benchmarks.md) |
| Knowledge representation (procedural) | [Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md](../Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md) |
| Modular architecture / tool use | [Self_Evolve/03_env-centric/3.3_modular-arch.md](../Self_Evolve/03_env-centric/3.3_modular-arch.md) |
| Model collapse challenge | [Self_Evolve/06_challenges.md](../Self_Evolve/06_challenges.md) |
| Agentic topology (multi-agent) | [Self_Evolve/03_env-centric/3.4_agentic-topology.md](../Self_Evolve/03_env-centric/3.4_agentic-topology.md) |
| Claude Code as agent system | [Self_Evolve/05_applications.md](../Self_Evolve/05_applications.md) |

---

## Key Takeaways (TL;DR)

1. **0→60 vs 60→99**: The hardest agent problems are not in benchmarks — they're in the long tail of real-world failures.
2. **Commission beats ads**: Agents destroy the attention economy but enable the labor-intermediary economy. Commission is the natural business model.
3. **UDA > pure GUI agent**: Unified action spaces (GUI + API + code + terminal) are more robust than pure GUI approaches.
4. **Learning = Memory + Inference**: Continual learning is about where knowledge lives, not just how it's acquired.
5. **GenUI ≠ free generation**: Users want entropy reduction, not infinite flexibility. GenUI should structure, not overwhelm.
6. **Moat ladder**: Speed → reputation → domain data. Each stage requires different strategy.
7. **Procedural knowledge is the bottleneck**: Models know facts; they struggle with action sequences in novel contexts.
