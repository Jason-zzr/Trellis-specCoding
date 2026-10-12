# 第一版实施计划

状态：2026-10-11 用户已批准本仓库 + Pi 试点计划，进入实施；实际结果记录在本文末尾。

## Ordered Steps

1. **评审并激活**
   - 用户已确认第一版四项措施及本仓库 + Pi 试点边界。
   - 已执行 `python3 ./.trellis/scripts/task.py start .trellis/tasks/10-11-workflow-lightweight-v1`，状态已由 planning 转为 in_progress。
   - 执行前读取八个目标文件的当前内容与 diff，保留届时新增的用户改动，不重新调查已经解决的问题。
2. **调整本地工作流默认行为**
   - 修改 `.trellis/workflow.md` 的 Request Triage、相关状态块及 1.1/1.4/2.1/2.2/3.3/3.4 对应说明。
   - 小请求直接处理；任务规划保留一次批准；Pi 默认主线程；知识判断一次；复用有效验证结果。
   - 同步修改与新行为冲突的强制说明，保留标记、阶段编号、复杂任务三文档和 JSONL 就绪要求。
3. **对齐四个 start/continue 入口**
   - `.pi/prompts/trellis-start.md`、`.pi/prompts/trellis-continue.md`。
   - `.agents/skills/trellis-start/SKILL.md`、`.agents/skills/trellis-continue/SKILL.md`。
   - 入口引用 workflow；避免小请求建任务询问、无关请求绑定旧任务和重复实施审批。保留适用平台的上下文读取方式。
4. **对齐三个直接消费 skills**
   - `.pi/skills/trellis-brainstorm/SKILL.md`：合并独立问题，按结论更新材料，区分方向同意与最终实施批准。
   - `.pi/skills/trellis-before-dev/SKILL.md`：允许无任务的直接处理路径，保留相关规范读取。
   - `.pi/skills/trellis-check/SKILL.md`：主线程检查、验证证据有效性与完整范围、一次 spec 判断。
   - 不修改代理角色、update-spec 内容模板或 finish-work；按需调用已有能力。
5. **集中静态核查与交付**
   - 主线程只对本次八个变更文件做一次结构、Markdown/frontmatter、标记配对及 diff 格式核查；对照已确定的验收场景静态确认文案是否有相反要求。
   - 更新本任务实施结果，报告实际改动和未执行的运行验证；不追加审查代理，不自动提交、推送或归档。

## Validation

本次及计划默认均为静态核查：不新增、修改、安装或执行测试，不运行构建、CI 或真实 agent 场景；未来用户另行授权运行验证时再明确范围。

可用的只读命令：

```bash
git diff --check -- .trellis/workflow.md .pi/prompts/trellis-start.md .pi/prompts/trellis-continue.md .agents/skills/trellis-start/SKILL.md .agents/skills/trellis-continue/SKILL.md .pi/skills/trellis-brainstorm/SKILL.md .pi/skills/trellis-before-dev/SKILL.md .pi/skills/trellis-check/SKILL.md
git diff --stat -- .trellis/workflow.md .pi/prompts .agents/skills/trellis-start .agents/skills/trellis-continue .pi/skills/trellis-brainstorm .pi/skills/trellis-before-dev .pi/skills/trellis-check
```

静态验收对照（不是已运行的测试）：

| 场景 | 预期规则 |
| --- | --- |
| 无任务的解释问题/只读调查 | 直接响应，不询问建任务 |
| 当前任务中的无关问答 | 不改任务指针、状态或材料 |
| 明确低风险小修改 | 使用现有修改授权、主线程完成获准工作 |
| 用户只要计划 | 停留 planning，不运行 start |
| 复杂计划已批准且范围不变 | 复用批准，不重复询问 |
| 出现权限/迁移/跨包契约或新风险 | 停止扩大范围，重新规划或确认 |
| 原检查覆盖相同输入与环境 | 复用；覆盖不足或输入变化则不可声称已通过 |
| 无新增工程知识 | spec 判断一次；出现新契约则按需更新 |

静态结果只证明规则文档的一致性，不能证明 agent 真实执行次数、耗时或多平台行为改善。

## Review Gates

- 当前已确认：整体诊断与第一批四项优化方向。
- 2026-10-11 用户已明确批准本仓库 + Pi 的试点边界及这版设计、实施计划，无需重复确认。
- 实施若需扩大到脚本、公共模板、其他平台、测试或全局配置，报告必要证据并重新取得相应授权。
- 不把本版目标扩成“所有材料与收尾全面重做”。现有结构校验与 Git 权限边界不变。

## Rollback Points

- 步骤 2 前记录目标文件原有 diff；只撤销本任务引入的局部修改，不覆盖基线。
- 工作流与入口必须作为一致集合保留或回退，不能只留一半新规则。
- 不通过 trellis update 覆盖定制，不改模板 hash，不改旧任务状态。

## Implementation Result — 2026-10-11

- 已完成八个目标文件的第一版修改：小请求直达；Pi 主线程实施与检查；独立问题合并、授权复用；有效检查证据复用、一次 spec 判断。start/continue 和直接消费 skills 已对齐。
- Pi 使用现有普通状态及独立平台段；原有六个 workflow-state 标记、阶段/步骤标题、JSONL 准备、任务/决策校验和 Git 收尾机制保持不变。公共模板、其他平台文件、运行时脚本和本机安装配置未改。
- 主线程已完成一次集中静态核查：八个流程文件及四个 Markdown 规划/交接文件共 12 份文件的 UTF-8、代码围栏、frontmatter/空白格式未发现错误；workflow 的 23 组块标记配对，六个状态块和阶段/步骤标题与基线一致；task JSON/JSONL 可解析，上下文引用存在。
- 定向 `git diff --check` 通过；跟踪文件 diff 严格为约定八个文件（165 行新增、125 行删除），暂存区为空。核查时未发现目标文案中的相反要求。
- 验收边界：AC1–AC8 对应规则已做静态文案对照；没有运行真实 agent 场景、任务运行验收、测试、构建或 CI，不将静态结果当作行为或性能验证。PRD 的场景清单不据此冒充运行通过。
- 本次 spec 判断：提示策略已记录在 workflow 及其入口；未增加运行时状态、解析或生命周期契约，不另建重复规范或决策条目。后续收尾复用本结论，除非出现新的契约或发现。
- 未提交、推送、归档或改动原决策记录任务；本任务保持 in_progress。

## Review Fix — 轻量化审查修复

- 用户已授权修复审查发现的两处问题，沿用本仓库 + Pi、仅静态核查的范围；上节为初版实施记录，不代表后续语义审查无问题。
- 收尾条件：Pi continue、check skill、workflow 状态提示和 2.2 对齐为实施完成、当前全范围证据满足约定交付标准、无阻塞发现或必需检查失败，才进入 Phase 3。部分实施、失败结果和未验证的必需验收项均留在 Phase 2；未获授权的检查不运行，也不当作通过。
- 平台边界：共享 start/continue 在 Pi 下转用仓库内 `.pi/prompts/` 对应入口，非 Pi 正文恢复原流程；workflow 的分流、状态提示、澄清与批准复用、检查复用和 spec 去重均明确 Pi 条件，保留其他平台原规则。未修改其他平台文件、公共模板、运行时脚本或本机配置。
- 本轮范围：五个流程文件（workflow、共享 start/continue、Pi continue、Pi check）及本文；其余初版改动保留。不运行测试、构建或真实 agent 场景，不提交、推送或归档。
- 静态核查：六份本轮文件的 UTF-8、空白、代码围栏及适用 frontmatter 检查完成；Pi prompt 原本无 frontmatter，已对照 HEAD 确认沿用原格式，无需添加。workflow 仍有 23 组配对标记，六个状态块名称及阶段/步骤标题保留。共享 start/continue 的非 Pi 步骤正文与 HEAD 一致，Pi 入口引用存在。未执行行为验证；diff 格式检查结果在本轮交付中报告。

## Planning Handoff

- 完整诊断：`trellis-workflow-lightweight-handover.md`。
- 当前任务：`.trellis/tasks/10-11-workflow-lightweight-v1/`，`in_progress`，`meta.planning_mode=complex`。
- 计划批准与仓库内八个流程文件的修改已完成；静态核查结果记录在下节。未运行测试或真实 agent 场景，也未提交、推送或归档。
- 用户明确要求只改仓库；目标路径已解析确认均位于 `/Users/admin/Coding/VibeCoding/Trellis-specCoding/` 内。不修改本机安装配置、`~/.pi/` 或全局目录，不安装更新或全局同步。
- start 提示 branch 与 base_branch 同为 main，归档将被拒绝；本轮不归档、不切换分支，后续 Git 操作另行授权。
