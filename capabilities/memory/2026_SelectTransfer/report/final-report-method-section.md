# Final Report — Method Section

> **Support**
> - Main Round 1 narrative: [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
> - Claim traceability: [round1-evidence-map.md](./round1-evidence-map.md)
> - Case-level raw evidence: [round1-case-appendix.md](./round1-case-appendix.md)

## 1. Task Framing

This project does not evaluate memory by asking whether memory increases average benchmark performance. Instead, it studies **selective transfer**:

> Under a fixed experience budget, does a memory mechanism help on structurally matched target tasks while avoiding harm on mismatched target tasks?

The goal of the experiment is therefore methodological as well as empirical. We aim to distinguish genuine memory effects from artifacts introduced by coarse pairing, insensitive evaluation, or non-executable memory abstractions.

## 2. Experimental Setting

The benchmark setting is a near-transfer configuration:

- **Source benchmark:** HotpotQA
- **Target benchmark:** 2WikiMultiHopQA
- **Model:** `Qwen/Qwen3.5-9B`
- **Experience budget:** `N = 5` source episodes per source set

We compare three memory conditions:

1. **No Memory**
2. **Episodic Trace**
3. **Cross-Episode Consolidation**

The source/target setting, model, budget, and decoding scaffold are fixed within each controlled sub-round. When the experiment later introduces repairs, each sub-round changes only one variable, consistent with the project's [experiment contract](../design/experiment-contract.md).

## 3. Source Pool Construction

The source side is not treated as an arbitrary retrieval pool. We first construct explicit source sets from annotated source episodes.

The early workflow includes:

- task sampling and task-pool construction
- taxonomy annotation
- source-set construction
- matched/mismatched pairing
- artifact generation and review

This pipeline is documented operationally in [pilot/README.md](../pilot/README.md) and [protocol/README.md](../protocol/README.md), but the methodological point is simple: `Relevant / Irrelevant` is defined **before** running the model, not after observing the outcome.

## 4. Evaluation Protocol

### 4.1 Why Naive Aggregate Was Rejected

The initial smoke subset showed that a flat average over all target cases was misleading. Different cases served different methodological roles:

- some were useful only as **process sanity** checks
- some were true **diagnostic** cases
- some were **audit / boundary** cases dominated by scoring or format effects

After Round 1c, mixed-role aggregation was explicitly banned. Cases had to be classified before entering any summary table.

### 4.2 Pairing Granularity

The original `bridge` cluster was later found to be too coarse. In particular, the experiment had conflated:

- `attribute_bridge`
- `relation_chain_bridge`

This matters because a coarse-grained "relevant" label can still be structurally mismatched at the subtype level. Round 1d–1g therefore redefined relevance at the subtype level and rerouted the most important diagnostic case (`wiki_dev_2639`) to a subtype-matched source set.

### 4.3 Executable Abstraction Requirement

For `Cross-Episode Consolidation`, topical relevance alone was insufficient. The memory artifact also had to preserve the target task's **operator structure** in an executable form.

This distinction became crucial for relation-chain cases involving kinship operators such as `sibling-in-law`. A natural-language summary of the relation pattern was not enough; the memory artifact had to encode candidate operator branches explicitly enough for the model to execute them.

## 5. Observability and Parsing

Round 1b introduced a structured response scaffold:

- `## Reasoning`
- `## Final Answer`

This change was necessary because the original pilot mostly produced short, opaque answers. Once the scaffold was added, all smoke runs became parseable, and process-level behaviors such as **explicit memory use** and **explicit memory rejection** became observable in the raw outputs.

This made it possible to separate:

- outcome-level change
- process-level selectivity
- scoring-boundary artifacts

## 6. Controlled Repair Strategy

Round 1 was not a single run but a sequence of tightly controlled sub-rounds. Each repair targeted exactly one layer:

- prompt scaffold
- case-role discipline
- pairing granularity
- source-side subtype feasibility
- routing
- consolidation formatting
- kinship-operator execution
- final patchback synthesis

This design is central to the method. The project is not claiming that memory "worked" after arbitrary iterative tuning. It is claiming that each suspected confound was isolated, repaired, and traced forward to its effect on interpretation.

## 7. What the Method Section Establishes

The methodological contribution of Round 1 is the following protocol claim:

- selective-transfer evaluation requires pre-frozen pairing
- case roles must be assigned before aggregation
- relevance must be defined at the right structural granularity
- consolidation artifacts must preserve executable operator structure

Without these constraints, the experiment risks measuring its own setup artifacts rather than the phenomenon of interest.
