# Progress Report Draft

这份文件整理的是可直接用于课程 `progress report` 的段落草稿。

写法目标不是“显得做了很多”，而是把当前项目如何从一个较大的问题收缩成一个更可 defend 的实验设计，清楚地写出来。

---

## 1. 摘要段落

当前项目的进展不应仅理解为“完成了多少实验运行”，而应理解为“将一个原本过于宽泛、难以解释的 memory 问题，收缩为一个更可测、更可 defend 的 empirical question”。项目目前已经完成了研究问题的重述、实验约定的冻结、pilot workflow 的搭建，以及第一轮 taxonomy 标注与 source-set feasibility check。基于这些前期工作，项目的中心问题已从宽泛的 memory critique 收缩为：在固定经验预算下，memory 是否支持 `selective transfer`，而不是 `indiscriminate reuse`。当前最重要的进展不是分数本身，而是已经获得了足以指导下一步实验设计的结构性发现。

## 2. 问题收缩与项目重定位

项目最初关心的长期问题不是 benchmark 分数，而是更高层的 memory question：过去经验什么时候只是被存下来，什么时候会进一步变成可复用的知识，甚至成为持续影响后续判断的结构。基于这一长期问题，课程项目并没有直接去追问过大的 memory theory，而是切出一个中间层、可实验的问题：如果 memory 真正有用，它不应只在平均分上看起来有帮助，而应在过去经验与当前任务结构相关时带来正向迁移，并在二者不相关时避免负迁移。这个问题被进一步固定为 `HotpotQA -> 2WikiMultiHopQA` 的 near-transfer setting，从而将讨论收束到 `selective transfer` 这一可测现象上。

## 3. 为什么需要这一轮设计重构

这次设计重构并不是单纯的“换题”，而是对原问题可实验性的修正。原先更大的问题虽然有研究吸引力，但依赖过多潜变量，例如“memory 是否真的相关”“经验是否真的可迁移”“机制是否真的正确工作”。这类问题在课程项目中很难得到干净结论，因为结果可能同时受到 model 能力、prompt、benchmark 结构、annotation 主观性和 system configuration 的影响。当前版本的设计通过固定 benchmark、source-target direction、split 定义和指标，把问题收缩到一个更可解释的层面：我们不直接判断 memory 的本体真假，而先判断它是否表现出选择性的迁移行为。

## 4. 实验约定与 protocol 的建立

为了避免后续实验出现“变量不止一个、结果不可追溯、结论超出 scope”的情况，项目先建立了一套明确的实验约定。当前设计要求每一轮正式比较只改变一个核心变量；benchmark、model、agent scaffold、pairing、max steps 和 metrics 在同一轮内保持固定；`Relevant / Irrelevant` pairing 必须在实验前冻结；memory artifacts 在进入正式运行前必须先经过人工检查；同时，所有结果必须分 split 报告，而不能只看 average gain。这些约定将当前项目从一般性的 exploratory note 收紧成了一个可解释、可追溯、可重复的实验框架。

## 5. 第一轮 taxonomy 标注的当前发现

在第一轮工作中，项目已经对 20 个 sampled tasks 完成了首轮 taxonomy 标注。当前结果显示，这批样本中稳定出现的 dominant reasoning patterns 主要是 `bridge` 和 `comparison`：其中 `bridge = 14`，`comparison = 6`，而 `temporal` 和 `distractor-heavy` 在这一小样本中没有形成足够稳定的实例。这个结果有两个意义。第一，它说明 taxonomy 并非空想规则，而是已经能够与真实 benchmark 样本对接。第二，它也暴露出当前 sample 的结构限制：这一轮更适合作为 `bridge + comparison` 的 pilot subset，而不足以支撑更完整的四类 taxonomy 设计。

## 6. Source set feasibility check 的关键发现

基于当前的 taxonomy 结果，项目继续进行了第一轮 source-set feasibility check。这里出现了一个重要发现：在当前 sample 下，source benchmark `HotpotQA` 只足够构出一个干净的 `bridge` source set，而不足以构出 `comparison` source set。原因很直接：当前 sample 中 `HotpotQA comparison` 只有 2 题，而设计要求每个 source set 固定包含 `N = 5` 个 solved episodes。这意味着当前 20 题 sample 虽然足以支撑 taxonomy rehearsal，也足以证明 source-set construction 不是空转，但还不足以直接进入正式的 full pilot。这个发现非常重要，因为它不是“实验失败”，而是一个真实的 protocol bottleneck。

## 7. 由发现逼出的设计决策

基于上述发现，项目已经做出若干关键决策。首先，不再把当前 `sampled_20` 直接当作正式 source pool，而是把它重新定位为 taxonomy rehearsal 和 source-set feasibility check。其次，保持当前的 source-target setting 不变，即 source benchmark 仍然是 `HotpotQA`，target benchmark 仍然是 `2WikiMultiHopQA`，不通过临时借用 target-side 样本来“补齐” source-side cluster。再次，承认当前 sample 只能先支持一个 `bridge` draft source set，并把 comparison coverage 不足视为协议层面的真实发现，而不是用 ad hoc patch 掩盖掉。换言之，当前项目已经开始从“先跑了再说”的状态，转向“先保证 setup 自身可解释，再决定后续实验如何扩大”的状态。

## 8. 这些进展为什么是有效进展

虽然当前项目还没有进入完整的 pilot run，但这并不意味着没有实质性进展。恰恰相反，当前阶段已经完成了课程项目中最容易被忽视、但对后续结果最关键的一层工作：把 measurement device 本身搭出来，并开始用真实数据检验这把“尺子”是否能用。taxonomy 的首轮标注、source set 的可行性检查、以及由此产生的结构性约束，已经能够帮助项目决定下一步该如何扩大 source pool、如何构造更可 defend 的 pairing，以及什么样的 pilot 才值得真正跑下去。从这个角度看，当前的进展不只是搭文档，而是在缩小问题、识别瓶颈、收紧实验边界。

## 9. 当前阶段最合理的下一步

基于目前已有材料，下一步最重要的工作不是继续扩展理论讨论，也不是急着进入 full run，而是继续把 setup 做稳。具体来说，下一步包括三项互相关联的任务：第一，对已标注的 5 个边界 case 做 delayed re-annotation，以检查 taxonomy 的基本稳定性；第二，扩充 `HotpotQA` source-side candidate pool，专门补足 `comparison` cluster，以便构造至少一个可用的 `comparison` source set；第三，在 source-side cluster 足够支撑后，再进入第一轮正式的 relevant / irrelevant pairing。只有当这几步完成后，后续的 artifact generation 和 pilot run 才真正有解释价值。

## 10. 可直接用于结尾的总结段

总体而言，当前项目最重要的成果不是已经得到了关于 memory 的最终结论，而是已经把一个原本过于宽泛、容易混淆变量的问题，收缩成了一个更清晰的 selective-transfer setup，并通过真实 sample 暴露出关键的 protocol bottleneck。这些发现已经足以支持一个更成熟的后续实验计划：在保持 source-target setting 不变的前提下，补齐 source-side candidate pool，稳定 taxonomy，并在此基础上构造更干净的 source sets 与 pairing。换句话说，当前阶段的价值主要体现在研究设计的澄清与实验边界的收紧，而不是 benchmark 分数本身。
