# Interim Survey Draft — GUI Agent × Memory × Self-Evolving

---

## 0. Title

**Experience-Dependent Procedural Knowledge in GUI Agents: A Taxonomy and Research Agenda**

---

## 1. Abstract

LLM-based GUI agents have recently achieved rapid gains in perception, planning, and action execution across mobile, desktop, and web environments. Yet much of this progress still relies on stronger backbones, larger training corpora, longer context windows, or app-specific workflow hints. This survey argues that the next bottleneck is not generic GUI skill, but the lack of a reusable and revisable experience layer: **experience-dependent procedural knowledge** acquired through interaction and applied beyond the current run. We study this problem through a taxonomy that asks **what** is learned, **when** experience is written back, and **how** experience is matched and applied. The taxonomy further separates `Match Operator` from `Application Carrier`, allowing retrieval to be distinguished from enforcement and enabling current systems to be analyzed at the level of capability patterns rather than whole-paper labels. Under this view, existing GUI agents already weakly occupy parts of the `post-task` memory space, especially `post-task / Skills / similarity retrieval × context injection`, but still rarely support rule-level generalization, cross-task procedural reuse, or failure-driven memory rewrite. We then synthesize evidence across GUI-agent, agent-memory, and self-evolving-agent literatures to argue that two gaps now form the most defensible research focus: `A-1 procedural memory for GUI` and `A-4 failure-driven write-back`. Episodic memory is positioned as supporting infrastructure, while user-centric memory remains a confirmed but peripheral extension line. The resulting survey contributes not only a literature organization scheme, but also a methodological agenda: memory units should be structured procedural rules rather than raw trajectories, retrieval and application should be evaluated separately, and write-back should be treated as a first-class design choice rather than an implementation detail. This framing narrows the field's broad memory rhetoric into a more testable target for future GUI-agent research.

---

## 2. Introduction

### 2.1 Why This Problem Matters

Graphical user interfaces remain the dominant interface layer for real-world digital work. A practical agent that can reliably operate software, websites, or mobile applications must therefore reason over GUI state, choose grounded actions, and recover from interface-specific failures. Recent LLM- and VLM-based systems have made clear progress on all three fronts. They can parse screenshots or accessibility trees, decompose tasks into sub-steps, and even exploit auxiliary memory to improve efficiency or robustness. Yet the strongest current systems still exhibit a recurring weakness: once the interface changes, the workflow becomes unfamiliar, or a local mistake reveals a hidden precondition, much of the useful knowledge has to be re-discovered rather than reused.

This weakness is easy to underestimate because it is often masked by gains from stronger backbones, larger context windows, or better training pipelines. But these improvements do not by themselves answer a more structural question: what should the agent remember after acting? Some GUI knowledge is already likely encoded in the base model, such as recognizing a button, a search box, or a common navigation pattern. What remains unstable is the interaction-derived part: knowledge about which submenu usually hides the needed function, which form field must be completed before another becomes active, which recovery action avoids losing state, or which failure pattern indicates that a previously successful tactic no longer applies. This is not generic GUI familiarity. It is experience-dependent procedural knowledge.

The literature reviewed in later sections suggests that this is now the most useful way to state the bottleneck. Existing systems such as AppAgent (Zhang et al., 2023), MobileGPT (Lee et al., 2024), MAGNET (Sun et al., 2026), ActionEngine (Zhong et al., 2026), IntentCUA (Lee et al., 2026), and GUI-Owl-1.5 / MobileAgentV3.5 (Xu et al., 2026) have shown that app-specific knowledge documents, sub-task graphs, workflow memory, structural state graphs, and intent abstractions can all help. They have not yet shown that post-task experience can be consolidated into cross-task reusable rules and revised after failure. The central motivation of this survey is therefore not to ask whether GUI agents have any memory, but whether they can build the right kind of memory: a reusable and revisable experience layer that goes beyond static hints and transient context management.

### 2.2 Scope and Boundary

This survey focuses on LLM-based GUI agents that externalize or operationalize experience reuse. Concretely, it is concerned with memory objects and write-back mechanisms that persist beyond a single run and can influence later task execution. The main emphasis is on the transition from `post-task` experience to `cross-task` reuse, because this is where the current taxonomy reveals the clearest structural gap. The survey therefore prioritizes systems that either already instantiate some form of externalized experience reuse in GUI environments, or provide transferable precedents for how such reuse could be built.

The survey is not mainly about generic prompt engineering, pure training-stage self-evolution, or one-shot improvements that never survive beyond the current episode. Nor is it a general survey of text-only agent memory. Work from adjacent non-GUI domains is included only when it provides a precedent that directly informs the missing GUI capability, such as workflow induction, long-term storage management, experience abstraction, or memory rewrite. This boundary is important because otherwise the discussion quickly collapses into an overly broad claim that "memory helps agents." That statement is true but not discriminative enough to guide methodology.

The key boundary throughout the paper is the following: we distinguish reusable experience-dependent procedural knowledge from generic GUI priors already likely encoded in the base model. This distinction excludes many tempting but unhelpful examples. A model remembering that search bars often appear near the top of a page is not yet evidence of learned experience. A model learning that, in a family of settings pages, the relevant option is often hidden behind a secondary overflow path and that a failed save usually reflects a missing prerequisite field is much closer to the target object of this survey.

### 2.3 Research Question

> **RQ**: How can LLM-based GUI agents represent interaction-derived, experience-dependent procedural knowledge as retrievable, revisable, and cross-task reusable memory, and improve it through failure-aware write-back from post-task experience?

This research question is narrower than a generic "memory for GUI agents" framing and commits the survey to three specific requirements. First, the memory must represent interaction-derived knowledge rather than merely restating generic interface priors. Second, the memory must be retrievable and reusable across future tasks rather than only within the current trajectory. Third, the memory must be revisable, which means failure is treated not just as a runtime event but as a signal for memory maintenance. These three requirements separate the framing adopted here from neighboring but insufficiently aligned lines such as raw trajectory replay, app-specific workflow caching, or stronger training-side data flywheels.

### 2.4 Contributions of This Survey

This survey makes four concrete contributions. First, it proposes an operational taxonomy over `What` is learned, `When` experience is written back, and `How` experience is matched and applied, instead of collapsing GUI skill, memory, and self-improvement into one undifferentiated category. Second, it uses taxonomy occupancy together with counter-evidence analysis to separate valuable blanks from merely unoccupied cells. Third, it argues that `A-1 procedural memory` and `A-4 failure-driven write-back` form the most defensible research focus, while episodic memory and user-centric personalization are better treated as supporting and extension lines, respectively. Fourth, it translates these conclusions into a methodological agenda, so that the survey can serve not only as a related-work chapter but also as a bridge into subsequent method design.

---

## 3. Background and Problem Formulation

### 3.1 Three Source Threads

The problem studied in this survey sits at the intersection of three research threads that are often discussed separately. GUI-agent work contributes the grounded task setting, memory research contributes the storage and retrieval vocabulary, and self-evolving-agent work contributes the mechanisms for turning experience into future improvement. The central research focus only becomes clear when these three threads are read together.

#### 3.1.1 GUI Agents

The GUI-agent literature establishes the practical environment in which the problem matters. These systems must perceive a screen, infer the relevant task state, and choose actions that remain grounded under interface variation, multi-step dependencies, and partial observability. The strongest recent systems show that meaningful progress is possible through app-specific knowledge documents, hierarchical sub-task memory, workflow memory, structural state graphs, and intent-level planning abstractions, as illustrated by AppAgent (Zhang et al., 2023), MobileGPT (Lee et al., 2024), MobileAgent-v2 (Wang, J. et al., 2024), MAGNET (Sun et al., 2026), ActionEngine (Zhong et al., 2026), and IntentCUA (Lee et al., 2026). This body of work therefore proves that GUI agents do not fail only because of weak perception. They also fail because the environment reveals interaction-specific regularities that are hard to retain and reuse.

At the same time, GUI-native work also exposes the current limits of memory design. Many systems still store either app-bound semantic artifacts, transient working summaries, workflow templates, or structural priors. These are all useful, but they answer different questions. Some help an agent become familiar with a single app. Others help it finish the current run more reliably. Fewer address whether experience can survive as a revisable cross-task asset. This is why the GUI thread provides the task pressure and the failure modes, but not yet a complete answer to the current research question.

#### 3.1.2 Agent Memory

The agent-memory literature contributes a more precise language for talking about what is being stored and why. It shows that memory is not a single object but a family of functions: episodic memory preserves past events, semantic memory stores relatively stable world knowledge, procedural memory supports action selection, and user-centric memory tracks preference or personalization signals. It also provides concrete mechanisms such as selective retrieval, reflection-triggered abstraction, long-term storage management, and explicit memory evolution, as seen in Generative Agents (Park et al., 2023), MemGPT (Packer et al., 2023), and A-MEM (Xu et al., 2025). Without this literature, GUI memory discussions tend to stay at the level of "the agent remembers something." With it, the survey can ask sharper questions about whether a given GUI artifact is serving as working memory, semantic documentation, procedural reuse, or only a loose prompt aid.

This thread also matters because it removes a recurring conceptual objection. Long-term memory is not just a larger prompt. Text-domain systems such as Generative Agents (Park et al., 2023), MemGPT (Packer et al., 2023), and A-MEM (Xu et al., 2025) show that memory can be externally stored, selectively retrieved, reorganized, and even rewritten in response to new evidence. None of these methods directly solves GUI interaction, because their memory substrates are mostly textual and their actions are not visually grounded. But they establish that retrieval, reflection, storage management, and write-back are not speculative ideas. They are already viable memory primitives that GUI-agent research can adapt.

#### 3.1.3 Self-Evolving Agents

The self-evolving-agent literature contributes the missing dynamic piece: how experience is turned into improved future behavior. This thread is especially important because it shifts the question from storage to transformation. AWM (Wang, Z. Z. et al., 2024) shows that trajectories can be distilled into reusable workflows instead of being replayed verbatim. ExpeL (Zhao et al., 2024) shows how success-failure contrasts can maintain an editable pool of insights. SkillRL (Xia et al., 2026) shows that failures can be distilled into generalized skills rather than left as raw cautionary traces. AgentKB (Tang et al., 2025) shows that experience can transfer across heterogeneous agent frameworks when retrieval is filtered and interference is controlled. These works collectively demonstrate that "learning from experience" can be implemented as a memory pipeline without continual backbone retraining.

In this review, this thread matters less as direct GUI evidence than as methodological precedent. It shows that workflow induction, experience abstraction, and failure-aware refinement are feasible in neighboring environments. The unresolved issue is therefore not whether such mechanisms can exist at all, but whether they can be grounded in multimodal GUI settings where failure often depends on visual ambiguity, hidden state, or app-specific control logic. This is the bridge between self-evolving agents and the present `A-1/A-4` research focus.

### 3.2 Key Definitions

To keep the rest of the survey precise, four terms need to be used in an explicitly operational sense.

**Experience-dependent procedural knowledge** refers to action-guiding knowledge that is revealed through interaction and is not adequately explained by generic model prior alone. It is not the fact that buttons are clickable or that a save action often appears near the top of a page. It is the knowledge that, under a certain interface pattern, the effective route is usually hidden behind a secondary menu, that a field activation depends on an unstated prerequisite, or that a certain recovery action prevents state loss after a failed submission.

**Memory unit** refers to the smallest experience artifact worth retrieving and revising. In the framing adopted here, a memory unit is not a raw action trace, but a structured procedural rule with trigger, procedure, constraint, failure signal, revision cue, and scope. This definition matters because it excludes two common but insufficient extremes: verbatim trajectory replay on one side and over-general prompt advice on the other.

**Write-back** refers to the act of consolidating post-task evidence into the long-term memory store so that future behavior can change. Write-back may add a new memory unit, edit an existing one, split an over-broad rule, downweight a memory whose scope was overestimated, or rewrite a previously stored policy. The key point is that write-back is about memory maintenance after task outcome is known, not merely about using memory during inference.

**Cross-task reuse** refers to any reuse setting in which memory created from one task instance influences another task instance beyond literal replay. The most important levels here are repeated-task reuse, same-app cross-task reuse, and near-domain app-family transfer. The definition is intentionally narrower than open-world generalization, because the present argument does not require fully unrestricted transfer in order to be meaningful.

### 3.3 Common Confusions to Eliminate

Four confusions repeatedly blur the literature and need to be eliminated before the taxonomy is applied.

**Confusion 1: workflow cache != procedural memory.** A cached workflow or approved plan may be highly useful, but it is not automatically a procedural memory unit in the sense used here. A workflow cache typically stores a successful route through a task. Procedural memory, by contrast, should capture the transferable local rule inside that route, together with the conditions under which it applies and fails. This distinction is what separates systems such as MobileGPT, MAGNET, and IntentCUA from the stronger target posed by A-1.

**Confusion 2: context compression != cross-session episodic memory.** Summarizing the current trajectory can stabilize long-horizon execution, but that does not imply the agent now has an episodic memory architecture. In-task compression is a working-memory function. Episodic memory requires persistence, retrieval across sessions or tasks, and some principle for selecting or consolidating prior episodes. Treating these two as equivalent risks overstating what current long-horizon systems actually achieve.

**Confusion 3: stronger training pipeline != deployment-stage write-back.** Synthetic trajectory generation, post-training, and training-time self-evolution can all improve GUI agents, but they do not by themselves create a runtime loop in which failure revises long-term memory. This distinction is central to A-4. If deployment-stage memory never changes after a failure, then the system may be self-improving in a broad engineering sense while still lacking failure-driven write-back in the specific sense that matters here.

**Confusion 4: user profile concept != validated user-centric memory mechanism.** A paper may acknowledge that user history or preference information matters without providing a mature user-centric memory loop. This is the current status of much of the personalization line. Recognizing the object is not the same as showing how it should be stored, updated, retrieved, and evaluated over time. The distinction matters because A-3 is confirmed as a direction, but still not as a solved mechanism.

---

## 4. Taxonomy

### 4.1 Dimension I: What Is Learned

The first dimension asks what kind of experience is being accumulated. This question matters because not every useful artifact should be treated as the same memory object. In the current taxonomy, four categories are needed.

**Skills** refer to reusable local action policies, exception-handling patterns, and task-relevant procedures. This is the category most closely aligned with the present argument, because it is where experience-dependent procedural knowledge should appear if the field is truly learning from interaction. A typical GUI example would be a rule that, in a certain settings layout, the relevant control is often reached by opening an overflow menu before the visible option list becomes useful.

**World** refers to relatively stable environment knowledge such as app structure, UI semantics, and interface regularities. This category includes knowledge such as which navigation tabs exist, which screen regions are functionally stable, or how a site organizes states and transitions. World knowledge is useful, but it is not automatically procedural. It helps the agent orient itself; it does not by itself specify which action policy should be taken under failure or partial observability.

**Episodes** refer to concrete past task histories, including successful and failed trajectories. This category is important because many systems begin by storing or compressing episodes before they can abstract rules from them. But episodic storage should be treated as a substrate rather than as the final answer to procedural reuse. A past trajectory may be worth retrieving without yet being the right memory unit.

**User** refers to user-specific preferences, habits, and personalized operating tendencies. This category matters because some GUI tasks are underdetermined without user history. Yet it remains peripheral to the present argument because the best available evidence still concerns access to preference history more than mature user-memory maintenance.

This first dimension therefore separates four different reasons to store experience. The distinction is not merely descriptive. It prevents the survey from labeling every external artifact as "procedural memory" and clarifies why the present argument is specifically centered on `Skills`, with `Episodes` as supporting substrate, `World` as structural context, and `User` as a separate extension line.

### 4.2 Dimension II: When Is Experience Written Back

The second dimension asks when experience is written back or consolidated. Four stages are needed here as well: `pre-task`, `in-task`, `post-task`, and `cross-task`.

`Pre-task` learning refers to exploration or preparation before the target task is executed. App exploration and app-specific knowledge construction belong here. This stage is already well represented in GUI agents and explains why systems such as AppAgent and MobileGPT can outperform purely stateless prompting. But pre-task learning often remains app-bound and does not guarantee that later task outcomes will revise the memory itself.

`In-task` learning refers to real-time reflection, compression, or correction while the task is unfolding. This includes working-memory updates, step-level verification, and local replanning. The field is increasingly competent at this stage, especially in long-horizon agents. Still, in-task adjustment is not yet the same as durable experience accumulation because the updated state often disappears when the episode ends.

`Post-task` learning refers to the period after a task outcome is known, when successful or failed trajectories can be summarized, abstracted, filtered, or written back. This stage is crucial because it is the first point at which the agent can compare expected and actual outcome and decide whether a memory artifact should be added or revised. MAGNET and related systems provide the clearest GUI-side weak occupancies here, but the literature still rarely reaches rule-level generalization or failure-driven revision.

`Cross-task` learning refers to the persistent maintenance and reuse of experience across later tasks. This is where the present argument becomes most demanding. The central bottleneck is not whether any learning occurs at all, but whether post-task evidence can be consolidated into cross-task reusable memory. This is the exact bridge the field still lacks: many systems can explore, reflect, or summarize, but far fewer can preserve the resulting knowledge in a form that remains retrievable, revisable, and useful later.

For this reason, the survey's main stance is not that pre-task or in-task learning are unimportant. It is that the decisive missing link lies between `post-task` and `cross-task`. A system that cannot cross that boundary may still be adaptive in the short term, but it does not yet solve the experience-reuse problem targeted in this survey.

### 4.3 Dimension III: How Is Experience Reused

#### 4.3.1 Match Operator

The third dimension asks how experience is reused, and here the taxonomy must be explicitly split into two layers. The first layer is the **Match Operator**, which describes how the system finds relevant prior experience.

`Exact match` refers to direct reuse when the current task, screen pattern, or sub-task closely matches a previously stored case. This is common in task recall and app-internal reuse settings. It is often the easiest form of memory reuse to validate, but it also has the weakest transfer potential.

`Similarity retrieval` refers to retrieving prior experience based on approximate semantic, structural, or multimodal similarity. This is more flexible than exact match and already appears in workflow and insight retrieval systems. However, it introduces the classic problem of interference: retrieved memories may look relevant while encoding the wrong abstraction or the wrong scope.

`Rule generalization` refers to reusing an abstract procedural rule that is no longer tied to one exact past instance. This is the most important operator in the present framing because it is what separates reusable procedural memory from replay or nearest-neighbor recall. If the field cannot support rule-level generalization, then cross-task reuse will remain largely equivalent to better cache lookup.

#### 4.3.2 Application Carrier

The second layer is the **Application Carrier**, which describes how the retrieved experience actually influences behavior.

`Context injection` means inserting the retrieved artifact into the planner or actor context. This is the most common carrier in current systems because it is easy to implement and compatible with prompt-based agents. But it is also the easiest to overuse, and it often blurs the difference between passive reminder and operational constraint.

`External tool call` means using memory as a callable module, retriever, or workflow executor rather than as plain prompt context. This carrier is rare in current GUI memory work but conceptually important because it creates a clearer separation between long-term experience and the main reasoning prompt.

`Policy constraint` means using memory to shape action selection more directly, for example as a verifier prior, reranking signal, or decision constraint. This carrier is especially relevant when the goal is not merely to remind the agent of prior experience, but to make that experience consistently affect execution.

`Memory rewrite` means that experience is not only applied to the current task but also used to modify the memory store itself. This is the carrier most relevant to A-4. It captures the fact that memory maintenance is itself a mechanism of reuse: the system uses current evidence to decide how the next use of memory should change.

We separate matching from application because prior taxonomies often conflate how experience is found with how it is enforced. This distinction is necessary here because `similarity retrieval × context injection` and `rule generalization × policy constraint` may both be called "memory use," yet they represent very different capability levels.

### 4.4 ME/CE Result

This taxonomy is intended as a diagnostic framework rather than a one-label database schema, so its validity depends on a clear ME/CE interpretation. At the level of `memory unit` or `capability pattern`, the taxonomy passes the relevant test. `What` and `When` are sufficiently distinct to classify what kind of experience is being stored and at what stage it is being consolidated. The earlier one-layer version of `How` does not pass this test because it mixes matching strategies with application mechanisms. Once `How` is split into `Match Operator × Application Carrier`, the categories become internally coherent enough to support a stable analysis.

The main caveat is that system-level mapping is not single-label. One GUI agent may contain multiple memory units, and those units may occupy different cells of the taxonomy. This does not invalidate the taxonomy. It simply means the right object of analysis is the capability pattern rather than the whole paper taken as one atomic category. Under that interpretation, the framework is both mutually discriminative enough to be useful and collectively complete enough for the present argument.

### 4.5 Occupancy Summary

When current systems are mapped into this taxonomy, three conclusions emerge immediately. First, `post-task / Skills / similarity retrieval × context injection` is no longer empty. It is weakly occupied by systems such as MAGNET (Sun et al., 2026), which shows that GUI agents can indeed summarize successful experience after a task and reuse it later. Second, `post-task / Skills / rule generalization` remains sparse. Current systems still struggle to turn task-completion experience into compact procedural rules that generalize beyond the original workflow instance. Third, `cross-task / Skills` and especially the `memory rewrite` carrier remain the most structurally underdeveloped parts of the space.

This occupancy pattern is exactly what justifies the survey's central argument. The field no longer needs a generic argument that memory is useful. It needs a sharper argument that the dominant current solutions stop at weak occupancy: they retrieve similar successful experience, often inject it into context, and sometimes maintain workflow-level artifacts, but they rarely generalize those artifacts into revisable cross-task rules. The taxonomy therefore does more than organize the literature. It identifies where the literature is already credible, where it is only weakly occupied, and where the most defensible next contribution lies.

---

## 5. Related Work Through the Taxonomy

Rather than reviewing GUI memory systems as a flat list, we organize prior work by the role memory plays in the agent loop. This matters because different systems externalize very different kinds of experience. Some help the agent become familiar with an app before acting; some stabilize the current trajectory; some store workflows, plan templates, or structural graphs; and only a very small subset begins to approach post-task consolidation. Seen through this taxonomy, the literature already contains several strong partial solutions, but they occupy different slots and should not be collapsed into a single notion of "agent memory."

### 5.1 Pre-Task Exploration and App-Bound Knowledge

Early GUI memory systems primarily use memory to support environment familiarization. AppAgent (Zhang et al., 2023) is the clearest instance of this pattern. It explores an app, compiles discovered action effects into a per-app knowledge document, and then reuses that document during deployment. This is already an important departure from purely stateless operation: the system proves that lightweight exploration can create useful external memory without fine-tuning. However, the stored object remains an app-bound semantic artifact. The document captures which elements tend to do what inside one app, but it does not yet encode a revisable procedural rule with explicit trigger conditions, constraints, failure signals, or scope beyond that app.

MobileGPT (Lee et al., 2024) pushes this line further by turning memory into a hierarchical graph over tasks, sub-tasks, and actions. This is one of the earliest GUI-native examples where past experience is clearly reused as procedural structure rather than as flat notes. Crucially, sub-task knowledge can be shared across tasks within the same app, which makes MobileGPT a strong precursor to procedural memory. Yet its memory remains per-app and per-device, and its repair loop still relies on human intervention rather than autonomous consolidation. Relative to AppAgent, MobileGPT raises the level of abstraction from knowledge documents to reusable sub-task schemas; relative to the present argument, it still stops before `post-task -> cross-task` rule abstraction and failure-driven write-back. The broader lesson from this group is that early GUI memory work is not memory-free. The field has already learned how to externalize app knowledge and app-internal skills. What remains open is whether these app-bound artifacts can be turned into compact, revisable, and transferable procedural units.

### 5.2 In-Task Reflection, Compression, and Local Repair

Another major line improves long-horizon execution not by storing reusable rules, but by making the current run more manageable. MobileAgent-v2 (Wang, J. et al., 2024) is representative here. Its memory unit is explicitly scoped to the current task and works together with planning and reflection agents to preserve relevant context, track progress, and classify errors. This is highly effective for multi-step execution because it reduces drift and supports local recovery, but the memory disappears with the task. The paper is therefore useful precisely because it clarifies the boundary: in-task working memory and reflection can substantially improve execution, yet they do not automatically create a durable experience layer for future tasks.

This distinction becomes even clearer in later long-horizon augmentation systems such as GUI-Owl-1.5 / MobileAgentV3.5 (Xu et al., 2026) and M2 (Yan et al., 2026). Both show that context compression and retrieval can materially improve practical performance. M2 is especially informative because it combines recursive trajectory summarization with external insight retrieval and demonstrates that high-level experience can help without retraining the backbone. Yet its external memory is still an insight bank derived mainly from successful trajectories, not a deployment-generated memory that is continuously revised after failure. These methods therefore provide strong evidence that experience representation matters, but they mainly solve context management and retrieval-time augmentation rather than the full write-back lifecycle. Once temporary compression is separated from persistent procedural accumulation, it becomes easier to see why current long-horizon gains still leave the main research problem unresolved.

### 5.3 Post-Task Workflow Memory as the Current Best GUI-Side Partial Solution

The strongest GUI-side partial solutions emerge when experience is lifted from local interaction history into workflow, structure, or intent-level memory. MAGNET (Sun et al., 2026) is currently the clearest representative of this transition. By introducing stationary memory for stable functional UI semantics and procedural memory for abstract workflows, it shows that GUI agents can benefit from memory objects richer than app notes or transient summaries. More importantly, it demonstrates that memory can help cope with UI drift and app-version changes, which directly targets a central weakness of app-bound prompt-only agents. However, MAGNET still relies mainly on successful trajectories for memory construction, and its procedural memory remains largely workflow-level and per-app in practice. It therefore occupies an important slot in the taxonomy, but still only a weak one relative to the present argument.

ActionEngine (Zhong et al., 2026) and IntentCUA (Lee et al., 2026) extend this shift in two different directions. ActionEngine turns memory into a state-machine graph that supports one-shot program synthesis and deterministic execution. This is a strong example of structural memory for planning, but the stored object is still primarily topology and executable template rather than revisable experience-delta rules. IntentCUA instead abstracts traces into intent groups, subgroup skills, and shared plan memory. Its contribution is to show that GUI memory can operate above the atomic-action level, which is conceptually close to procedural abstraction. Yet the resulting memory is still closer to approved plan cache and skill hints than to an open-ended long-term memory that can be rewritten after failure. Taken together, these systems confirm that the field has already started moving toward more structured and reusable external memory, but that the dominant forms remain workflow-level, app-bound, or success-biased. The remaining gap is therefore no longer whether memory helps, but whether it can support finer-grained rule abstraction and principled revision.

### 5.4 Transferable Precedents from Memory and Self-Evolving Agents

Many of the strongest design precedents for the missing GUI capability currently come from adjacent fields rather than from GUI-native systems. On the memory side, Generative Agents (Park et al., 2023) and MemGPT (Packer et al., 2023) establish two complementary lessons: raw experience must be selectively retrieved and often reflected upon, and long-term memory requires explicit management rather than blind context accumulation. A-MEM (Xu et al., 2025) extends this argument by showing that memory need not be append-only; later evidence can revise earlier memory objects. These systems do not yet solve GUI procedural reuse because their substrates are mostly textual and their actions are not grounded in dynamic interfaces. Still, they remove several conceptual objections. They show that persistent retrieval, reflection-triggered abstraction, self-directed memory operations, and even memory rewrite are all technically viable.

On the self-evolving side, AWM (Wang, Z. Z. et al., 2024), ExpeL (Zhao et al., 2024), SkillRL (Xia et al., 2026), and AgentKB (Tang et al., 2025) provide even stronger precedents for the present argument. AWM demonstrates that historical trajectories can be abstracted into reusable workflows rather than replayed verbatim. ExpeL shows how success-failure contrasts can maintain an editable insight pool. SkillRL goes one step further by extracting generalizable skills from successes and failures and co-evolving them with policy. AgentKB shows that transferable experience can improve heterogeneous agents when retrieval is filtered and disagreement is controlled. None of these papers directly answers the GUI problem, because they are validated mainly in textual or web settings and do not address grounded visual interaction, interface drift, or app-family transfer. But together they make the main conclusion difficult to avoid: the strongest ingredients for reusable experience already exist, just not yet in a GUI-grounded form.

### 5.5 User-Centric Personalization as a Peripheral but Confirmed Line

User-centric memory remains peripheral to the present argument, but it is no longer a speculative direction. OS-Copilot / FRIDAY (Wu et al., 2024) already make room for user profile information inside a broader memory architecture, which is important because it shows that system designers recognize user history as a distinct memory object rather than merely another prompt field. At the same time, these systems do not yet provide a cleanly validated user-centric write-back loop. Their procedural memory is primarily tool-centric, and their evidence for personalization remains indirect.

Persona2Web (Kim et al., 2026) makes the missing piece explicit by showing that current web agents fail catastrophically on ambiguous personalized tasks when user history is absent, and still perform poorly even when history is accessible. The benchmark therefore sharpens the problem: having a history store is not the same as using it effectively, and using it effectively is not the same as maintaining it over time. For this survey, user-centric memory should be treated as a confirmed extension line with important evaluation implications, but not as the most feasible or best-evidenced centerpiece of the present research agenda.

---

## 6. Gap Analysis

### 6.1 Main Gap A-1: Procedural Memory for GUI

Current GUI agents still lack a reusable procedural memory that can transform post-task experience into cross-task applicable rules. This claim does not mean the field lacks memory altogether. The progression from AppAgent (Zhang et al., 2023) to MobileGPT (Lee et al., 2024) to MAGNET (Sun et al., 2026), ActionEngine (Zhong et al., 2026), and IntentCUA (Lee et al., 2026) shows that GUI systems have already learned to externalize app knowledge, sub-task structure, workflows, intent abstractions, and structural state graphs. The problem is that these artifacts are usually tied to a specific app, site, workflow family, or cached plan regime. Their memory objects remain either too coarse, too local, or too rigid to serve as general `experience-delta` rules that can be retrieved and reused across future tasks with clear triggers, constraints, and scope boundaries.

This is why the current best partial solutions do not yet close the gap. MobileGPT (Lee et al., 2024) demonstrates app-internal procedural reuse, but its memory is explicitly per-app and per-device. MAGNET (Sun et al., 2026) demonstrates workflow-level procedural memory and dynamic evolution, but its memory still depends on successful trajectories and remains constrained by per-app workflow abstraction. ActionEngine (Zhong et al., 2026) proves that structural memory can dramatically improve planning, yet its graph stores site topology and executable templates rather than revisable experiential rules. IntentCUA (Lee et al., 2026) shows that skill abstraction can rise above atomic action traces, but its memory is still closer to user-approved plan cache and subgroup hints than to continuously consolidated procedural memory. These systems collectively show that the field has reached the edge of the problem, not its solution.

The importance of A-1 becomes even clearer once adjacent precedents are considered. AWM (Wang, Z. Z. et al., 2024) and related self-evolving systems already demonstrate that trajectories can be distilled into reusable workflow knowledge in textual or web domains. The unresolved jump is therefore not conceptual feasibility but GUI grounding: how to represent procedural knowledge that is abstract enough to transfer beyond one exact screen flow, yet grounded enough to remain operational under visual variation, hidden preconditions, and layout drift. This is precisely why A-1 remains the central gap. It sits at the intersection of what GUI-native systems have almost achieved and what adjacent fields have already partially validated.

### 6.2 Main Gap A-4: Failure-Driven Write-Back

Current GUI agents may accumulate successful traces or benefit from stronger training flywheels, yet they still lack a deployment-stage mechanism that rewrites memory based on failure. This is a distinct problem from merely having memory. AppAgent (Zhang et al., 2023) and MobileGPT (Lee et al., 2024) demonstrate memory construction, but neither provides autonomous failure-driven revision. MobileAgent-v2 (Wang, J. et al., 2024) is especially revealing because it explicitly classifies erroneous and ineffective operations during execution, yet this signal is not consolidated into persistent memory. MAGNET (Sun et al., 2026) goes further by evolving memory over time, but still requires successful trajectories for memory construction and therefore leaves failure as mostly a filtering condition rather than a source of learnable correction.

The gap is further sharpened by recent training-oriented self-evolution work. Systems such as GUI-Owl-1.5 / MobileAgentV3.5 (Xu et al., 2026) and related training-side flywheels show that GUI agents can improve through synthetic data, trajectory refinement, and stronger post-training pipelines. But these improvements primarily happen before deployment or outside the runtime memory loop. They do not answer whether a deployed agent can observe that a previously stored rule no longer works, diagnose why it failed, and then edit, split, downweight, or rewrite that rule for future tasks. Training-time evolution and deployment-time write-back should therefore be treated as related but non-equivalent capabilities.

Adjacent fields again provide the strongest precedents without yet closing the GUI gap. AWM (Wang, Z. Z. et al., 2024) and ExpeL (Zhao et al., 2024) show that success-failure contrasts can yield reusable experience abstractions. SkillRL (Xia et al., 2026) shows that failures can be distilled into generalized corrective skills rather than stored as raw cautionary traces. A-MEM (Xu et al., 2025) shows that memory can be revised rather than merely appended. Yet none of these systems addresses the grounded GUI problem where failures arise from visual ambiguity, hidden interface state, transient pop-ups, or app-specific control logic. This is why A-4 remains a main-line gap rather than an implementation detail of A-1. Without failure-driven write-back, even a good procedural memory will tend to degenerate into a success-case cache.

### 6.3 Supporting Gap A-2: Episodic Memory for GUI

Episodic memory is best treated as supporting infrastructure for retrieval and evaluation, rather than the central object of the present argument. Generative Agents (Park et al., 2023) and MemGPT (Packer et al., 2023) already show why long-term storage, selective retrieval, and memory management matter, while GUI-side results such as M2 (Yan et al., 2026) suggest that summarized history and insight retrieval can materially improve long-horizon performance. But episodic memory alone does not automatically produce reusable procedural knowledge. Raw history helps preserve context; it does not by itself explain which local strategies should transfer, when a previously successful tactic has become invalid, or how a failure should modify an existing rule. For this reason, A-2 is better positioned as an enabling layer beneath A-1 and A-4 than as the survey's central research object.

### 6.4 Extension Gap A-3: User-Centric Memory

User-centric memory is a high-value extension line, but it currently sits outside the most feasible and best-evidenced contribution path. OS-Copilot / FRIDAY (Wu et al., 2024) show that user information can be acknowledged as part of an agent memory architecture, and Persona2Web (Kim et al., 2026) demonstrates that history-dependent personalization is a real and difficult capability gap rather than a product nicety. However, the available evidence still mostly concerns access to history and use of preference signals, not a mature loop for maintaining, revising, and safely deploying user-centric GUI memory over time. The direction is therefore confirmed, but still not strong enough to displace the procedural-memory focus adopted here.

### 6.5 Why These Gaps Matter More Than Other Blanks

Not every empty cell in the taxonomy deserves equal attention. The reason A-1 and A-4 matter more than other blanks is not simply that they are empty, but that they satisfy four stronger conditions simultaneously. They are technically plausible because adjacent fields have already validated major sub-components such as workflow abstraction, editable experience pools, and memory rewrite. They align directly with the current research question because they target the missing `post-task -> cross-task` experience layer rather than peripheral capabilities. They are experimentally tractable because repeated-task, same-app transfer, and near-domain app-family transfer already offer realistic validation settings. And they carry higher explanatory value than many alternative blanks because solving them would clarify whether GUI agents need more model capacity, better prompts, or a genuinely new memory mechanism.

By contrast, some other blanks are either too weakly evidenced, too far from current feasibility, or too indirect relative to the central argument. This is why the survey should not present the taxonomy as an invitation to fill every vacancy. Its value is diagnostic: it helps separate structural bottlenecks from merely unoccupied possibilities. On the current evidence base, reusable procedural memory and failure-driven write-back remain the two most defensible targets.

---

## 7. Methodological Implications

### 7.1 What Should Be Stored

The literature reviewed so far suggests that the target memory object should not be a raw trajectory and should not simply restate generic GUI priors. Raw trajectories are too verbose, too noisy, and too brittle: they preserve local detail but do not directly explain what should transfer. Generic priors, on the other hand, do not justify an external memory mechanism at all, because the model should already know many of them. What should be stored instead is a compact procedural rule that captures the part of the experience that was revealed only through interaction and is likely to matter again.

At minimum, such a memory unit should encode a trigger, a recommended procedure, the relevant constraints or preconditions, a failure signal indicating when the stored strategy has become unreliable, and a scope statement describing where the rule is expected to transfer. This is the smallest representation that remains faithful to the current gap analysis. It is richer than app notes, more abstract than raw action traces, and more editable than frozen workflows. It also directly answers a recurring objection from the related-work section: if the stored object cannot specify when it should fail or be revised, it will likely collapse back into either case-based retrieval or static workflow caching.

### 7.2 How Memory Should Be Retrieved and Applied

The survey also suggests that retrieval and application should be treated as separate design decisions rather than a single mechanism. On the retrieval side, the natural comparison is among raw trajectory retrieval, coarse workflow memory, and fine-grained delta procedural memory. These baselines correspond to three different assumptions about what makes past experience useful: exact recall of prior episodes, reuse of higher-level workflows, or reuse of compact procedural deltas. A convincing follow-on method should show not only that memory helps, but that the finer-grained representation is the right unit of reuse.

On the application side, the literature strongly suggests that context injection alone is not enough. Many current systems prepend retrieved memory to the prompt, which is often the simplest starting point, but this makes it hard to distinguish between memory as actionable guidance and memory as passive reminder. The taxonomy therefore motivates evaluating multiple application carriers: prompt-level context injection, tool-mediated retrieval, policy-level constraint or reranking, and memory rewrite as a maintenance carrier. This separation is not cosmetic. It determines whether the system merely sees prior experience or can actually let that experience shape planning, execution, and revision in a stable way.

### 7.3 Why Failure Must Trigger Memory Revision

Failure-driven revision emerges from the survey not as an optional enhancement, but as a core methodological requirement. Without a write-back path, even a good memory store tends to become a success-case cache. This is already visible in current GUI systems that benefit from successful workflows or approved plans but have little principled way to revise those artifacts when the environment changes or when an old strategy begins to fail. The consequence is not just stagnation. It is miscalibrated reuse: the system continues to retrieve an experience artifact whose original conditions no longer hold.

This is why rewrite operations such as `edit`, `split`, `downweight`, or `rewrite` should be treated as first-class design choices rather than implementation detail. Each operation corresponds to a different hypothesis about why the prior memory failed. An edit assumes the memory was mostly right but incompletely specified. A split assumes two contexts were previously conflated. A downweight assumes the memory remains valid but should be trusted less broadly. A rewrite assumes the previously stored policy is no longer the right abstraction. A subsequent method need not commit to the final write-back policy at the outset, but it should inherit from this review the principle that failure must be able to change memory, not merely trigger another attempt.

### 7.4 Minimum Evaluation Package

The minimum evaluation package follows directly from the main-line argument. At a baseline level, a future method should be compared against `no memory`, `raw trajectory retrieval`, `success-only memory`, `failure-aware memory update`, `coarse workflow memory`, and `fine-grained delta procedural memory`. These comparisons are necessary because each baseline eliminates a different alternative explanation. If the full method only beats `no memory`, it may simply be exploiting any added context. If it fails to beat workflow memory, then fine-grained procedural abstraction may not be justified. If it fails to beat success-only memory, then the write-back argument remains unproven.

Evaluation should also be staged across three transfer boundaries: repeated-task reuse, same-app cross-task reuse, and near-domain app-family transfer. This order matters. Repeated-task improvement tests whether the system can learn from experience at all. Same-app transfer tests whether the stored memory generalizes beyond literal task replay. Near-domain app-family transfer tests whether the learned unit is more than an app-specific cache. Open cross-app transfer may still be worth reporting, but the survey suggests it should be treated as a bonus rather than a precondition for the main contribution. The main empirical question is not whether memory solves all GUI generalization, but whether it produces measurable experience gain beyond what the base model already knows.

---

## 8. Discussion

### 8.1 What Would Count as Real Memory Gain

The central evaluation risk for this line of work is that apparent memory gains may be misattributed. A system may improve because it has more context, because it cached a repeated task template, or because the backbone was already strong enough and simply benefited from better prompt organization. For this reason, real memory gain in the sense used by this survey should satisfy three stronger conditions. First, the gain should exceed what can plausibly be explained by generic base-model prior alone. The strongest evidence here is not absolute success rate but selective improvement on cases where the model initially fails or behaves unstably and later improves after accumulating experience. Second, the gain should be more than literal cache reuse. If a method succeeds only when the future task nearly duplicates a stored workflow, then it has not yet shown that it learned a transferable procedural rule. Third, the gain should remain revisable under failure. If a memory artifact can only help when previously successful but cannot be corrected when wrong, then the system is still closer to a success-case repository than to an evolving experience layer.

These criteria imply that the strongest future evidence will likely come from controlled comparisons rather than from one headline benchmark number. A persuasive system should show repeated-task improvement, some degree of same-app cross-task transfer, and a measurable advantage for failure-aware update over success-only accumulation. In the context of this survey, that is what would justify the claim that memory is functioning as reusable procedural knowledge rather than as extra prompt budget.

### 8.2 Limits of the Current Survey

This survey also has several deliberate limits. First, the evidence base is uneven across sub-lines. `A-1` and `A-4` are comparatively well supported because they can draw on both GUI-native systems and adjacent precedents from memory and self-evolving agents. `A-3 user-centric memory`, by contrast, remains evidence-limited and should still be discussed in B-level language. Second, several peripheral or recently emerging systems remain only partially integrated into the current cross-topic synthesis. Their absence does not overturn the core argument, but it does mean that the occupancy map should still be read as a strong draft rather than a final census of the field.

Third, the survey intentionally does not require fully open cross-app generalization as a precondition for significance. This is a methodological choice rather than a claim that open-world transfer is unimportant. The current evidence suggests that repeated-task reuse, same-app transfer, and near-domain app-family transfer are already meaningful and experimentally tractable boundaries. Requiring unrestricted cross-app transfer too early would risk turning a concrete and testable problem into a vague benchmark ideal. Finally, the survey remains stronger as a taxonomy-and-gap document than as a comprehensive field census.

### 8.3 Outlook

The main practical value of this survey is that it converts a broad topic area into a narrower research program. Instead of asking whether GUI agents need memory in general, it argues that the most promising next target is `experience-dependent procedural memory` linked to `failure-driven write-back`. The result is not only a literature summary, but a structured bridge toward subsequent methodological development: a taxonomy that localizes the missing capability, an evidence-backed gap analysis that prioritizes `A-1 + A-4`, and a methodological agenda that already constrains what should be stored, how it should be reused, and how it should be evaluated. The next step is to compress this research agenda into a concrete method and experimental package, not to reopen the problem framing at a broader and less testable level.

---

## 9. Conclusion

This survey argues that the next bottleneck for LLM-based GUI agents is not simply stronger perception, larger models, or longer context, but a missing experience layer: reusable, revisable procedural knowledge acquired through interaction. By organizing the field through `What` is learned, `When` experience is written back, and `How` it is matched and applied, we show that current systems have already moved beyond purely stateless execution, but have done so unevenly. App-bound knowledge documents, working-memory compression, workflow memory, structural state graphs, and intent abstractions all provide useful partial solutions. Yet these solutions remain concentrated in weakly occupied parts of the taxonomy and still rarely deliver rule-level generalization, persistent cross-task reuse, or principled memory rewrite after failure.

This diagnosis leads to a more focused research agenda than the broad claim that "GUI agents need memory." The most defensible research focus is the combination of `A-1 procedural memory for GUI` and `A-4 failure-driven write-back`. In this framing, episodic memory serves mainly as supporting substrate and evaluation infrastructure, while user-centric memory remains an important but still peripheral extension line. The resulting shift is significant because it turns the problem from an abstract capability wish into a more testable target: can a GUI agent store interaction-derived procedural rules, retrieve them beyond literal replay, and revise them when they fail?

The practical value of this survey is therefore twofold. As a literature contribution, it provides a taxonomy and gap analysis that make the current field easier to read without collapsing distinct memory functions into a single category. As a research transition document, it narrows subsequent method design toward a concrete implementation and evaluation package: structured procedural memory units, explicit separation between retrieval and application, and write-back mechanisms that treat failure as a source of memory maintenance rather than only as a runtime error. If this framing is correct, the next substantive advance in GUI-agent research will come less from scaling model capacity alone and more from building a grounded experience layer that can persist, transfer, and be corrected over time.

---

## 10. Section-Level Evidence Map


| Section          | Claim                                                                            | Evidence Source                              | Current Strength | Status             |
| ---------------- | -------------------------------------------------------------------------------- | -------------------------------------------- | ---------------- | ------------------ |
| Introduction     | GUI agents still need interaction-derived knowledge beyond base-model priors     | Zhang et al. (2023); Lee et al. (2024); Xu et al. (2026); cross-topic gap synthesis | A                | Ready              |
| Introduction     | The real bottleneck is reusable procedural experience rather than generic memory | Taxonomy occupancy synthesis + procedural-memory gap evidence from Lee et al. (2024), Sun et al. (2026), and adjacent precedents | A | Ready |
| Taxonomy         | `How` must be split into match vs application                                    | Taxonomy synthesis from cross-topic comparison and capability-pattern analysis | A | Ready |
| Related Work 5.1 | Early GUI memory is mainly app-bound exploration support                         | Zhang et al. (2023); Lee et al. (2024)       | A-B              | Ready              |
| Related Work 5.2 | In-task reflection rarely becomes revisable long-term memory                     | Wang, J. et al. (2024); Xu et al. (2026); Yan et al. (2026) | A-B | Ready |
| Related Work 5.3 | Current best GUI-side memory remains workflow-level and weak in rule abstraction | Sun et al. (2026); Zhong et al. (2026); Lee et al. (2026) | A | Ready |
| Related Work 5.4 | Adjacent fields provide the strongest precedents for reusable experience         | Wang, Z. Z. et al. (2024); Zhao et al. (2024); Packer et al. (2023); Xu et al. (2025); Tang et al. (2025); Xia et al. (2026) | A | Ready |
| Gap 6.1          | GUI agents lack cross-task reusable procedural memory                            | Lee et al. (2024); Sun et al. (2026); Zhong et al. (2026); Lee et al. (2026); Wang, Z. Z. et al. (2024) | A | Ready |
| Gap 6.2          | GUI agents lack failure-driven write-back at deployment time                     | Wang, J. et al. (2024); Sun et al. (2026); Xu et al. (2026); Zhao et al. (2024); Xia et al. (2026); Xu et al. (2025) | A | Ready |
| Gap 6.3          | Episodic memory is supporting infrastructure, not current core object            | Park et al. (2023); Packer et al. (2023); Yan et al. (2026) | A | Ready |
| Gap 6.4          | User-centric memory is confirmed but still peripheral                            | Wu et al. (2024); Kim et al. (2026)          | B                | Ready with caution |
| Methodology      | Memory unit should be a revisable procedural rule, not a raw trace               | Cross-topic synthesis from Lee et al. (2024), Sun et al. (2026), Wang, J. et al. (2024), and Xu et al. (2025) | A-B | Ready |
| Evaluation       | Success-only memory is insufficient; failure-aware update must be tested         | Cross-topic synthesis from Wang, J. et al. (2024), Sun et al. (2026), Xu et al. (2026), and Zhao et al. (2024) | A | Ready |

---

## 11. References

Kim, S. et al. (2026) 'Persona2Web: Benchmarking Personalized Web Agents for Contextual Reasoning with User History'. *Proceedings of the International Conference on Machine Learning (ICML 2026)*. arXiv:2602.17003.

Lee, S. et al. (2024) 'MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation'. *Proceedings of the 30th Annual International Conference on Mobile Computing and Networking (MobiCom 2024)*. arXiv:2312.10190.

Lee, S. et al. (2026) 'IntentCUA: Learning Intent-level Representations for Skill Abstraction and Multi-Agent Planning in Computer-Use Agents'. *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2026)*. arXiv:2602.17049.

Packer, C. et al. (2023) 'MemGPT: Towards LLMs as Operating Systems'. *arXiv preprint*, arXiv:2310.08560.

Park, J. S. et al. (2023) 'Generative Agents: Interactive Simulacra of Human Behavior'. *Proceedings of the ACM Symposium on User Interface Software and Technology (UIST 2023)*. arXiv:2304.03442.

Sun, L. et al. (2026) 'MAGNET: Towards Adaptive GUI Agents with Memory-Driven Knowledge Evolution'. *arXiv preprint*, arXiv:2601.19992.

Tang, X. et al. (2025) 'AGENT KB: Leveraging Cross-Domain Experience for Agentic Problem Solving'. *arXiv preprint*, arXiv:2507.06229.

Wang, J. et al. (2024) 'Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration'. *arXiv preprint*, arXiv:2406.01014.

Wang, Z. Z. et al. (2024) 'Agent Workflow Memory'. *arXiv preprint*, arXiv:2409.07429.

Wu, Z. et al. (2024) 'OS-Copilot: Towards Generalist Computer Agents with Self-Improvement'. *Proceedings of the International Conference on Learning Representations (ICLR 2024)*. arXiv:2402.07456.

Xia, P. et al. (2026) 'SKILLRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning'. *arXiv preprint*, arXiv:2602.08234.

Xu, H. et al. (2026) 'Mobile-Agent-v3.5: Multi-platform Fundamental GUI Agents'. *arXiv preprint*, arXiv:2602.16851.

Xu, W. et al. (2025) 'A-Mem: Agentic Memory for LLM Agents'. *arXiv preprint*, arXiv:2502.12110.

Yan, D. et al. (2026) 'M^2: Dual-Memory Augmentation for Long-Horizon Web Agents via Trajectory Summarization and Insight Retrieval'. *arXiv preprint*, arXiv:2603.00503.

Zhang, C. et al. (2023) 'AppAgent: Multimodal Agents as Smartphone Users'. *arXiv preprint*, arXiv:2312.11190. Published in *Proceedings of the ACM CHI Conference on Human Factors in Computing Systems (CHI 2025)*.

Zhao, A. et al. (2024) 'ExpeL: LLM Agents Are Experiential Learners'. *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2024)*. arXiv:2308.10144.

Zhong, H. et al. (2026) 'ActionEngine: From Reactive to Programmatic GUI Agents via State Machine Memory'. *arXiv preprint*, arXiv:2602.20502.
