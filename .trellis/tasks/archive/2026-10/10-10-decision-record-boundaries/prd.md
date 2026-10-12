# Trellis 决策记录职责边界与升级规划

## Goal

在已批准范围内实施跨任务决策记录与确定性结构校验，减少重复论证和多份文档重复维护。校验模块、命令接入和本地材料已实现并随 `03993303` 提交，本仓库配置已启用。用户后续授权运行验证、安装必要依赖、构建、本地 CI 审查及缺陷修复；本轮修复已通过本地 CI，结果和验证边界见 implement.md。

## Background and Confirmed Facts

- 用户指定以 `/Users/admin/Coding/VibeCoding/DSH-C/trellis-upgrade-handover.md` 作为讨论起点，并同意创建规划任务；开发者标识为 `zzr-pi`。
- 交接文档提出三个候选方向：决策/否决生命周期、确定性结构校验、双语分节 hash 配对。第一版的用户选择见下方 Requirements；除下列已核查入口外，交接文档中的其他源码行为尚未重新核实。
- 当前 [workflow.md](../../workflow.md) 的 Planning Artifacts 已将需求、技术设计和执行计划分别分配给 `prd.md`、`design.md` 和 `implement.md`；`design.md` 明确包含 tradeoffs。
- 当前 [任务系统说明](../../../.pi/skills/trellis-meta/references/local-architecture/task-system.md) 将 `research/` 定位为研究材料，任务归档后仍保留在 `tasks/archive/`。不能把任务归档等同于决策材料被删除。
- 当前 [trellis-update-spec](../../../.pi/skills/trellis-update-spec/SKILL.md) 已要求把重要设计决定写入相关 spec 的 Design Decisions，模板含 Context、Options Considered、Decision。Trellis 并非没有记录决策理由的机制。
- 当前 [规范系统说明](../../../.pi/skills/trellis-meta/references/local-architecture/spec-system.md) 将 spec 定位为项目工程约定和实现契约。
- 规划初查时静态核对 [cmd_validate](../../scripts/common/task_context.py)：157–198 行只汇总 `implement.jsonl` / `check.jsonl` 校验结果，另对失效分支给出警告；当时尚未接入决策记录校验。
- 规划初查时静态核对 [cmd_start](../../scripts/task.py)：171–281 行在写入会话指针和任务启动状态前检查上下文清单；`after_start` 在状态更新之后调用。该入口没有自动调用完整的 `cmd_validate`。
- 规划初查时静态核对 [cmd_archive](../../scripts/common/task_store.py)：1257–1458 行包含归档前置检查，随后更新状态、移动目录，并可能自动提交；`after_archive` 在这些操作之后才调用。
- 规划初查时静态核对 [run_task_hooks](../../scripts/common/task_utils.py)：381–485 行从项目 `config.yaml` 读取 hooks，失败或超时只警告，不使生命周期操作失败。因此若要求结构错误阻止开始/归档，需要在状态和目录变更前校验，不能仅接入现有 `after_*` hooks。
- 已确认的脚本同步约束：[脚本规范](../../spec/cli/backend/script-conventions.md) 的 Two script trees, one content 要求 `.trellis/scripts/**/*.py` 与 `packages/cli/src/templates/trellis/scripts/**/*.py` 的路径集合和文件内容完全一致；已静态核对 [现有断言](../../../packages/cli/test/regression.test.ts) 11755–11817 行确实检查这两点，规划时未执行测试；后续运行结果见 implement.md。本仓库 `.trellis/scripts` 是产品脚本的自用副本，不能按普通使用项目的独立本地脚本处理。
- 已核查 [任务元数据与默认 PRD](../../scripts/common/task_store.py)：280–323 行支持字符串型 `meta` 与默认 PRD 骨架，1890–1930 行提供 `set-meta`；规划初查时当前任务的 `meta` 为空；实施激活时已设置 `meta.planning_mode=complex`，限定检索 `.trellis/scripts` 未找到现成的 `complexity` / `task_size` / `planning_mode` 分类约定。既有任务接入方式已获用户确认；明确分类的技术方案见已批准的 design.md。

## Requirements

### Confirmed

- 用户选择方案 A：第一版新增独立决策记录，只收跨任务的重要决策及否决记录；普通实现细节仍留在任务内。
- 用户选择在本仓库试点，并进一步批准为满足脚本同步约束，同步直接涉及的 `.trellis/scripts` 及 `packages/cli/src/templates/trellis/scripts` 副本；新增校验仅在本仓库启用。不修改 `init/update` 分发逻辑或 DSH-C 项目，不扩大到其他无关模板。
- 职责边界：`research/` 保存研究证据；`design.md` 保存本任务技术方案与局部取舍；`spec/` 保存当前有效工程契约及必要理由；独立决策记录保存跨任务的重要选择、否决理由、适用条件和后续替代关系。
- 不要求同一份详细论证在多处重复维护；design.md 的具体纳入标准、字段、章节和关联范围已随整体方案获批。
- 用户要求第一版同时纳入自动结构校验，并已明确批准实施。
- 用户选择扩大校验覆盖面：除决策记录及本任务关联外，第一版还检查 `prd.md`、`design.md`、`implement.md` 的存在性与必填章节，并区分轻量和复杂任务；任务规划文档的结构错误也纳入上述前置阻断。
- 用户选择阻断策略：当前任务涉及的决策记录若有结构错误，在开始实施和归档前自动校验并拒绝操作，列出具体错误和修复提示，保持原状态；不是仅警告后继续。
- 用户选择新旧任务统一校验：启用后，未归档任务在下一次开始或归档时接受相同检查，并按需补齐分类及必要文档；不批量修改历史任务或已归档文档，不为旧任务保留豁免通道。
- 用户选择结论型生命周期：`待决 → 已采纳 / 已否决`，实际交付由任务追踪；“已采纳”不等于已实施，不再采用交接文档中以实现、归档表达决策状态的方案。
- 条件变化后的重新评估新建关联记录；新结论确认后才建立替代关系，保留旧记录及其当时的理由，不覆盖历史结论。

### Approved Design

- 用户已批准 [design.md](design.md) 与 [implement.md](implement.md) 的整体方案；初次交付仅静态核查，后续明确授权运行验证、依赖安装、构建、提交、本地 CI 审查及本轮修复。已执行范围和结果见 implement.md；用户已单独确认提交本轮修复，未授权推送或归档。
- 用户明确不再使用 GitNexus；取消相关工具前置要求及阻塞，不增加替代工具或额外审批流程。
- 双语配对未纳入本轮范围；内容 hash 不能代替翻译语义审查。

## Acceptance Criteria

### Planning

- [x] 用户确认采用方案 A：独立管理跨任务的重要决策及否决记录。
- [x] 用户确认在本仓库试点、允许同步直接涉及的脚本模板副本；新增校验仅本仓库启用，`init/update` 分发逻辑不改。
- [x] 已提出哪些决定需要长期保存、哪些留在任务设计或研究材料中的具体标准，见 design.md；已随整体方案获批。
- [x] 用户确认结论型生命周期，以及新建记录重议、确认后替代并保留历史的规则。
- [x] 用户确认第一版包含自动结构校验。
- [x] 用户确认校验同时覆盖任务规划文档，并区分轻量和复杂任务。
- [x] 用户确认本任务相关记录结构错误时阻断开始实施和归档，并保持原状态。
- [x] 用户确认新旧任务同一规则、按下一次开始/归档接入，不批量修改历史资料。
- [x] 已明确建议的校验对象、关联范围及未覆盖的判断能力，见 design.md；已随整体方案获批。
- [x] 已补齐 design.md、implement.md 及非空的 implement.jsonl / check.jsonl。
- [x] 用户完成整体规划评审，并单独批准实施；不重复请求相同批准。

### Capability — Implemented

以下勾选表示实现已落地；实际执行的静态检查、测试、构建及环境边界见 implement.md，不把通过 CI 等同于证明全部业务语义。

- [x] 跨任务重要选择可独立检索，来源、备选方案、结论、理由和适用条件可追溯，任务内资料无须重复完整论证。
- [x] 采用待决/已采纳/已否决的结论状态，重议新建关联记录，仅已采纳的新结论产生替代效果，历史理由保留。
- [x] 轻量/复杂任务有明确分类，并按分类检查必要文档的存在性、必填章节和内容；分类缺失不能静默按轻量处理。
- [x] 本任务相关决策的元数据、章节、状态、唯一标识和来源/重议引用接受结构检查；无关历史错误不阻断本任务。
- [x] 开始或归档前发现错误，列出可定位的诊断及修复提示，返回失败，任务、会话指针、亲子关系、目录及 Git 索引保持调用前状态。
- [x] 来源任务归档后，决策仍可解析其来源，不要求已归档文档补齐新规则。
- [x] 新旧任务按同一标准检查；仅本仓库启用，直接涉及的脚本副本保持一致，未启用项目保留原流程。
- [x] 交付明确结构校验不能证明论证合理、分类正确或用户已批准，也不将静态证据当作运行通过。

## Out of Scope for This Stage

已批准的实施范围以 design.md 的拟改文件表为准；停用 GitNexus 不扩大功能范围。

- 修改该表之外的产品代码、平台 skills/hooks、其他模板、CI 或无关工程规范。
- 新增未获批准的生产决策、字段、CLI 命令或其他数据契约。
- 新增或修改测试资产、fixture、测试依赖或 CI 定义；未获授权的额外安装、运行验证、提交、推送或归档。已获授权的现有 CI 检查可执行。
- 初始化全局开发者身份；当前任务通过 `--assignee zzr-pi` 指定创建者和负责人。

## Open Questions

- 无待确认的 GitNexus 能力或替代授权事项；原有工具阻塞已取消。
- 本轮修复已通过本地 CI；详细结果、已有警告和与远程 CI 的环境差异见 implement.md。用户已确认提交本轮修复，任务未归档、未推送。
