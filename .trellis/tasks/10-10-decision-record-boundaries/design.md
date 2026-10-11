# 跨任务决策记录与任务结构校验设计

状态：已按用户批准的方案实现校验模块、三个入口及本地材料，本仓库开关已启用，限定静态核查已完成（结果及未覆盖范围见 implement.md）。任务为 in_progress；GitNexus 不作为实施前提。

## Scope

- 本仓库先行使用独立决策记录，并在任务开始、归档前校验任务文档和相关决策记录。
- 同步直接涉及的 `.trellis/scripts/` 与 `packages/cli/src/templates/trellis/scripts/` Python 副本；只在本仓库配置中启用。不修改 init/update 分发逻辑、平台 hooks、公共 workflow 模板、CI 或测试。
- 新旧未归档任务使用同一规则，下一次开始/归档时按需补齐；不批量迁移历史任务。
- 第一版不提供决策 CRUD CLI、数据库、后台扫描、双语 hash、通用规则 DSL 或自动判断决策优劣的机制。
- 本任务作为一个复杂任务实现：记录格式、相关集合和生命周期前置检查共享同一契约，暂不拆分相互依赖的子任务。

### 纳入独立记录的标准

同时满足“影响后续任务的工程选择”及“保留取舍理由有复用价值”，例如跨任务架构选择、公共接口策略、替换已有方案的重要决定或有明确前提的否决。

一次性变量命名、局部算法细节和本任务内的普通实现选择留在 `design.md`；调研原文留在 `research/`。规范只表达当前有效约束并引用决策，不复制整套论证。并非每个任务都必须创建决策。

## Contracts

### 1. 项目启用与任务分类

在本仓库 `.trellis/config.yaml` 使用一个明确的顶层标量：

```yaml
task_structure_validation: true
```

- 缺少该配置项或明确为 `false` 时，新增检查不启用，既有上下文、分支及归档校验继续按原行为运行。公共模板不写入启用值。
- 对该项只接受 `true` / `false`；显式空值、重复声明、错误类型或不支持的写法报告配置错误，不能降级成关闭。读取失败也不能当作成功。
- 现有 `read_trellis_config()` 遇到读取失败返回空字典，且简单 YAML 解析器会跳过不支持的项，不能直接用其默认值实现上述严格语义。新模块仅对这个顶层配置项做严格的存在性、重复及标量检查，复用现有简单 YAML 的标量解析规则；不改写通用配置加载行为、不引入 YAML 依赖。采用逐行和字段分隔处理，不新增正则。
- 这是项目自愿启用的流程检查，不是权限隔离；有权限修改配置的人仍可明确关闭它。配置文件缺失与明确关闭应在诊断中可区分。

复用现有字符串型任务扩展：

```json
{"meta": {"planning_mode": "complex"}}
```

`planning_mode` 必须明确为 `lightweight` 或 `complex`；缺失/未知值报错，不通过文档缺失、文件数或任务标题猜测类型。使用既有 `create --meta` / `set-meta` 能力维护，不新增顶层任务字段，也不预设默认轻量类型。

人或 AI 在规划时依据现有 workflow 判定类型并提交用户评审；机器只检查声明与材料是否一致，不判断分类是否合理。本任务应在实施获批后、启用检查前补充为 `complex`。

### 2. 任务规划文档

| 文件 | 轻量任务 | 复杂任务 | 必须存在且有内容的二级章节 |
| --- | --- | --- | --- |
| `prd.md` | 必需 | 必需 | `Goal`、`Requirements`、`Acceptance Criteria` |
| `design.md` | 可省略 | 必需 | `Scope`、`Contracts`、`Data Flow`、`Tradeoffs`、`Rollout and Rollback` |
| `implement.md` | 可省略 | 必需 | `Ordered Steps`、`Validation`、`Review Gates`、`Rollback Points` |

- 可选文件若存在，也检查其结构；额外章节允许，不要求字段顺序。
- 使用固定英文标题作为机器锚点，正文不限语言。本地 workflow 说明契约；不改其他项目的公共文档模板。
- 每个必填二级章节恰好出现一次，且含至少一行非空、非标题、非纯围栏标记的内容；HTML 注释不计入内容，代码围栏中的伪标题不算章节。未闭合围栏/注释报结构错误。
- 只使用行级 Markdown 子集，不实现通用 Markdown 渲染器或关键词评分。正文中的占位词、论证深度、验收标准质量、勾选状态及用户批准事实不由该检查推断。
- `task.json` 必须可读且是对象，`meta` 必须是对象；`relatedFiles` 若存在必须为字符串数组。只新增直接必要的字段检查，不重做整个任务 schema 校验器。

### 3. 决策记录单一事实源

采用 `.trellis/decisions/<id>.md` 平铺存储，`README.md` 仅存规范及模板，不作为决策。

- 文件名去掉 `.md` 即唯一稳定 ID，不再在元数据中重复保存 ID。ID 是单一路径段；禁止路径分隔符、`.`、`..`、保留名 `README`，并检查大小写折叠后的文件名冲突。
- 首个一级标题后紧接一个 JSON 围栏块（中间仅允许空行），作为唯一元数据。选择 JSON 是为了使用标准库进行严格解析，不给现有宽松 YAML 子集增加前置元数据解析职责。
- 不新增日期、负责人、版本或缓存索引；任务提供来源与实际交付状态，Git 可提供修改历史。

模板形态（示意，不是本轮创建的生产记录）：

````markdown
# 某项跨任务工程决定

```json
{
  "status": "proposed",
  "source_task": "10-10-decision-record-boundaries",
  "reconsiders": null
}
```

## Context
影响与约束。

## Options Considered
备选方案及其取舍。

## Decision
当前建议，或已确认结论及理由。

## Applicability
适用前提，以及哪些变化值得重新评估。
````

元数据三个字段均必需：

| 字段 | 类型与含义 |
| --- | --- |
| `status` | `proposed` / `accepted` / `rejected`；表示结论，不表示代码交付 |
| `source_task` | 来源任务的完整目录名，不是短 slug、不含目录路径 |
| `reconsiders` | `null` 或一个既有决策 ID；第一版只支持一个直接前驱 |

重议记录额外要求有内容的 `## Reconsideration`，说明新证据或适用条件变化。元数据拒绝重复 JSON 键、未知状态、字段缺失、错误类型与额外字段，避免拼写错误被忽略。

### 4. 重议与替代

- `proposed` 可在用户确认后转为 `accepted` 或 `rejected`。已定稿记录的结论及当时理由不原地覆写；重议创建新文件，通过 `reconsiders` 指向已定稿记录。
- 新记录仍为 `proposed` 或变为 `rejected`，都不取消旧结论。新记录成为 `accepted` 才产生替代效果。
- 旧记录保留原来的 `accepted` / `rejected` 状态；是否被替代从后继引用及其状态派生，不写回第二套状态或双向字段。
- 禁止自引用、环路和在同一关联链中出现两个已采纳的直接后继。继续重议时引用链尾；拟议/否决的重议尝试不自动取代当前有效结论。
- AI 查询历史时同时查看原记录及关联后继；被否决不是永久禁止，条件变化可以重新评估。
- 结构检查只校验当前文件快照，不能证明某个合法文本没有被改写，也不能代替用户批准。历史保留由工作流与 Git 审查约束，不添加快照数据库或审批签名。

### 5. 任务关联、扫描范围和归档稳定性

复用 `task.json.relatedFiles` 登记本任务使用/创建的决策路径，例如 `.trellis/decisions/task-validation-policy.md`；普通代码路径的既有用途不变。决策正文提到某个文件，不会自动建立机器关联；漏登记是否构成遗漏仍由 AI 审查。

相关集合的构造：

1. 从目标任务的 `relatedFiles` 提取决策文件作为根节点；登记的文件缺失、越界或不可解析，阻断。
2. 只枚举 `.trellis/decisions/*.md` 的元数据建立临时名称和重议引用索引，不递归扫描项目，不持久化另一份索引。
3. 沿有效 `reconsiders` 的前驱和后继取得相关连通集合，检查其中记录的完整结构、引用和替代链一致性。不能只读旧记录而漏掉已采纳的后继。
4. 无关记录的损坏仅作为警告，不阻断本任务。无法解析元数据的未登记文件，其关联关系不可确定；报告该限制，不声称校验已覆盖未知关联。没有决策根节点的任务可以不创建任何决策。

来源任务通过完整目录名，精确查找 `.trellis/tasks/<name>` 和 `.trellis/tasks/archive/*/<name>`，不作 suffix 猜测；零个结果为失效引用，多个为歧义。复用 `resolve_task_dir()` 对最终候选作目录边界检查。现有 `find_task_by_name()` 不扫描归档，因此不直接拿它作为历史来源解析器，也不扩大其所有调用方的行为。

只检查来源任务 `task.json` 的可读性及身份，不递归校验来源任务文档，避免要求历史任务补档。归档移动后按目录名重新解析，无须修改决策文件。决策路径解析以实际 `.trellis/decisions` 目录为边界，拒绝符号链接逃逸；保留 `.trellis` 整体指向共享存储的既有场景。

## Data Flow

### 单一校验实现

新增 `common/task_validation.py`，由三个现有入口直接调用，不借用失败只警告的 `after_*` hooks。

- `ValidationIssue`：记录 `path: Path`、`line: int | None`、`message: str`、`hint: str`、`severity: Literal["error", "warning"]`。
- `validate_task_structure(repo_root: Path, task_dir: Path) -> list[ValidationIssue]`：读取启用配置、目标任务和相关材料，返回稳定排序的诊断；不写任何任务、会话、目录或 Git 状态。
- 配置未启用时不扫描新增材料；显式配置错误返回 error。可预期的读取/解析错误转为诊断；不吞掉程序缺陷并返回“通过”。
- 模块依赖现有 paths/io/配置标量解析和 task_utils 的边界解析，不导入 `task.py`、`task_store.py`、`task_context.py`，避免循环依赖。不改通用 hook 或配置语义。

### 接入位置

| 入口 | 新增位置与行为 |
| --- | --- |
| `cmd_validate` | 汇总现有 JSONL 结果与新增结构诊断；存在任一 error 则返回 1，原警告仍为警告 |
| `cmd_start` | 在目录合法性检查之后、`set_active_task()` 和 `_record_start_state()` 之前执行；普通和 degraded 分支共用同一次前检 |
| `cmd_archive` | 在目录/归档目标碰撞检查之后、任务状态写入及亲子/会话/目录/Git 修改之前执行；即使 task.json 缺失或损坏也必须先拒绝，不能进入原先“警告后继续归档”分支 |

`--allow-empty-context` 仅控制原有上下文检查；`--skip-branch-validation` 仅控制原分支检查，都不能跳过新增结构检查。不新增忽略结构错误的参数。创建任务、检索、编辑、设置元数据和 `finish` 等恢复路径不受新前检阻断。

输出包含文件、能确定时的行号、错误项与修复提示；失败返回 1，状态/当前会话指针/亲子关系/目录/索引保持调用前状态。不宣称后续归档 I/O 具有新增事务保证，也不把直接编辑文件视为受该 CLI 检查保护。

### 工作流使用

本地 workflow 的规划步骤提示：明确类型，检索既有决定，把相关记录登记到 `relatedFiles`，补齐相应文档后请求用户批准；开始和归档前的脚本检查只保证结构。规划与实施阶段的本地 breadcrumb 说明该契约并引用 `.trellis/decisions/README.md`。

不修改平台 skills/hooks，不把“检查通过”替换为“用户已批准”，不自动将本任务本轮的规划讨论升级成生产决策记录。

## Tradeoffs

- 保留单文件记录和现有任务关联字段，避免 task.json 新顶层 schema、独立数据库及双份索引。
- 使用结论状态而非 implemented/archived，避免与任务进度重复；生效关系需要查看重议链。
- 采用固定标题和显式分类，错误更可复核；旧任务需要按触达补档，非标准标题需人工整理。
- 校验边界为相关记录，不让其他历史错误阻断本任务；代价是无法从未登记且元数据损坏的文件推断隐含关联。
- 原地启用优于为旧任务设计豁免/版本标记；不批量重写既有资料。
- 不采用 after-hook 阻断、不更改现有通用配置解析器的容错策略、不添加新依赖。
- 当前源码取证足以确定入口位置；未做编译、测试或运行验证，失败前无副作用与模板同步仍需实施后的静态证据，实际运行事实不能预先保证。

## Rollout and Rollback

1. 在获得整体方案和实施批准后，按项目要求激活任务；先明确本任务为 complex，并保留规划材料及上下文清单。
2. 保持新配置项未启用，完成校验模块与三个入口的双份脚本修改。
3. 完成本地记录 README、workflow/breadcrumb 提示及必要的本地 spec 契约记录；补齐本任务材料。
4. 最后只在本仓库配置写入启用值，再由主线程对本次修改文件做一次结构、语法、类型和 diff 静态核查，不运行程序、测试、构建或安装。
5. 其他任务由其负责人在下次开始/归档时按错误提示补齐；不批量迁移。运行验证留给用户，未验证的事实在交付中明确列出。

若实现前核查发现必须修改上述范围之外的模板、调用方或配置，暂停报告，不自行扩展。操作性回退先经用户确认明确关闭本地开关，保留所有记录和任务材料；若需撤销代码，仅撤销本任务引入的修改并保持脚本镜像同步，不覆盖其他工作区改动。

### 拟改文件

| 文件 | 用途 |
| --- | --- |
| `.trellis/scripts/common/task_validation.py`（新增）及同路径模板副本 | 集中结构校验与只读诊断 |
| `.trellis/scripts/task.py` 及模板副本 | start 前置检查 |
| `.trellis/scripts/common/task_context.py` 及模板副本 | validate 汇总 |
| `.trellis/scripts/common/task_store.py` 及模板副本 | archive 前置检查，不改 create 默认模板 |
| `.trellis/config.yaml` | 只在本仓库显式启用 |
| `.trellis/decisions/README.md`（新增） | 记录规范、模板、检索与重议操作 |
| `.trellis/workflow.md` | 本地分类、检索、登记和材料要求；相关 breadcrumb |
| `.trellis/spec/cli/backend/script-conventions.md` | 仅补充本次新增检查的实际脚本契约及镜像要求 |
| 当前任务 `task.json` 与规划材料 | 分类和上下文；保持现有无关字段 |

模板副本前缀统一为 `packages/cli/src/templates/trellis/scripts/`。不改其他模板、DSH-C、测试、依赖和 CI。

## Evidence

- `common/task_store.py:280–323,1890–1930`：字符串 meta、默认 PRD 与 set-meta。
- `common/task_utils.py:62–111,117–173,195–278`：名称查找仅活动目录，归档目录形态，路径 containment。
- `common/trellis_config.py:212–247`：简单 YAML 值为字符串，读取失败退回空对象。
- `task.py:195–275`：空清单检查、degraded 状态写入与会话指针写入顺序。
- `common/task_store.py:1257–1370`：归档碰撞检查、损坏 JSON 警告路径以及状态写入位置。
- `common/task_context.py:115–118,157–198`：JSONL 的 file/reason 契约与现有 validate。
- `.trellis/workflow.md:167–185,205–228`：规划产物职责及 planning breadcrumb。
- `packages/cli/test/regression.test.ts:11755–11817`：只读确认脚本路径集合/字节一致性断言；没有运行或改动该测试。

本节缩写的 Python 路径均相对 `.trellis/scripts/`。以上为静态证据，不能代表新增方案已运行通过。
