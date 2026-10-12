# 决策记录及结构校验实施计划

状态：任务保持 in_progress，meta.planning_mode=complex。原功能已随 `03993303` 提交，GitNexus 规则移除另见 `8bae7c86`。本轮修复配置缺失警告及未启用项目受无关 YAML 阻断的问题，本地 CI 已通过；运行结果、环境差异和日志见 Validation。用户已确认提交本轮修复，任务未归档，未推送。

## Ordered Steps

步骤有顺序依赖；每步沿用当前工作区和暂存区基线，不恢复旧版本以缩小 diff。

### 1. 确认授权与实施前提

- [x] 用户已评审 prd.md、design.md 和本计划并批准实施，无须重复确认。
- [x] 阅读 `.trellis/spec/cli/backend/index.md`、`script-conventions.md` 和 `workflow-state-contract.md`，采用现有 Python 标准库、导入与脚本镜像约定。
- [x] 核对本轮目标文件现有 diff 和直接调用关系，仅补足新证据；不重做已解决的产品讨论。发现必须扩大文件范围时暂停。
- [x] 实施获批后，使用既有元数据能力将本任务标记为 `meta.planning_mode=complex`；确认上下文清单就绪，按流程 `task.py start`，状态成为 in_progress 后再实施。

此处的任务激活是实施流程操作，不等于允许运行测试、编译或运行验证。

### 2. 实现单一只读校验模块

文件：`.trellis/scripts/common/task_validation.py` 及 `packages/cli/src/templates/trellis/scripts/common/task_validation.py`，两份均新增且内容相同。

- [x] 按 design 契约定义 `ValidationIssue` 与 `validate_task_structure(repo_root, task_dir)`，返回诊断，不更改任何持久状态。
- [x] 实现单项配置的严格启用判定；缺项/false 关闭，显式无效配置报错，不改变通用配置解析器的容错行为。
- [x] 严格读取任务 JSON；校验明确的轻量/复杂分类与规划文件，不因缺失 design/implement 推断任务为轻量。
- [x] 使用行级状态解析固定 Markdown 标题，处理代码围栏和 HTML 注释；只检查结构和非空，不增加语义/关键词规则。
- [x] 实现单文件决策元数据、必填正文、状态与文件名 ID 校验；只使用标准库，不添加依赖、字段版本或独立索引。
- [x] 从 relatedFiles 建立根集合，单层枚举元数据并沿重议关系收集相关记录；相关错误阻断，无关损坏警告，保留无法推断未知关联的说明。
- [x] 来源任务仅作精确目录名匹配，覆盖活动/归档目录，拒绝歧义及路径逃逸；不递归要求历史任务补档。
- [x] 检查已定稿前驱、自引用、循环与冲突的已采纳后继；替代状态只派生，不写回旧记录。

### 3. 接入现有命令

以下每个 Python 文件的产品模板副本必须同步，禁止改变一致性断言以容忍漂移。

- [x] `.trellis/scripts/task.py`：在 start 的首次会话或任务状态修改之前前检，普通/degraded 两条分支均覆盖；保留原有上下文检查。
- [x] `.trellis/scripts/common/task_context.py`：validate 汇总旧 JSONL 结果与新诊断；仅有警告不失败，有错误返回 1。
- [x] `.trellis/scripts/common/task_store.py`：在归档状态/亲子关系/会话/目录/Git 修改之前前检，覆盖 task.json 缺失/损坏的原容错分支；不重构归档后半段。
- [x] 保留现有错误语义与专用跳过参数的作用域；不添加结构检查旁路，不修改 after_* hooks、create 默认模板或 finish 恢复路径。
- [x] 仍保持本地启用项未打开，先完成入口与材料，再启用。

### 4. 接入本地工作流程与启用

- [x] 新建 `.trellis/decisions/README.md`：写入纳入标准、单文件模板、检索/关联方法及重议规则；不自动将草案升级为已采纳记录。
- [x] 局部修改 `.trellis/workflow.md`：在相应规划步骤和 planning/in_progress（含 inline）breadcrumb 中提示分类、历史决策检索、relatedFiles 登记和文档要求；引用 README，不重复复制完整字段规范。保持所有既有阶段规则。
- [x] 仅在 `.trellis/spec/cli/backend/script-conventions.md` 补充新增脚本接口、启用及错误处理的实际契约；不整理无关规范。
- [x] 确认当前任务材料符合已批准的固定章节与分类，其他任务不批量修改；不要求本任务必须凭空创建决策。
- [x] 最后在本仓库 `.trellis/config.yaml` 写入 `task_structure_validation: true`；公共配置模板和 init/update 逻辑不变。

### 5. 完成一次静态核查并交付

- [x] 主线程仅对已修改文件做一次结构、语法、类型、明确编译级错误与 diff 格式核查；不派审查子代理，不再次扩大功能调查。
- [x] 核对本次四组 Python 脚本副本逐字节一致；不扫描或修复无关脚本。
- [x] 区分代码改动与已有格式化/用户改动，保留证据；没有运行证据的行为不得标为运行通过。
- [x] 报告改动、静态结果及尚未执行的运行验证。任务归档、Git 提交/推送或关闭检查开关均不从本计划自动获得授权。

## Validation

### 初次交付的静态结果（历史记录）

- 8 个修改/新增 Python 文件经 `ast.parse(..., feature_version=(3, 9))` 解析通过，未导入或执行产品模块。
- 本次 4 组本地/模板脚本逐字节一致。
- 目标文件的工作区和暂存区 `git diff --check` 均返回 0；本次目标文件在改动前无暂存/未暂存修改，既有规则清理及其他目录改动保持原状。
- `task.json` 及两个 JSONL 清单解析有效；任务为 `in_progress`，`planning_mode=complex`。`task.json` 延续现有写入器不带末尾换行的格式。
- Ruff LSP 对 8 个文件返回 32 条 warning、无 error，包含新校验模块的 TRY004 异常类型建议及入口导入排序建议；未据此扩展格式整理或改动错误语义。Ruff 不等于专门类型检查，未运行额外类型检查器。
- 初次交付未执行新增校验器、start/archive 运行验证、测试、编译或安装，也未创建/修改测试资产；后续运行授权及结果见下文。
- 初次静态交付时保留 in_progress，未自动归档或提交；后续已获用户批准完成两组提交。本轮修复后用户另行确认提交。启动时已有 `branch=main` 与 `base_branch=main` 相同的警告，归档前需由用户处理。

### 后续授权与本轮 CI 结果

- 用户后续依次授权运行验证、安装 pnpm/项目依赖、构建、提交原功能、本地 CI 审查与本轮修复；随后单独确认提交本轮修复，不包含推送或归档。
- 已确认的历史提交：`8bae7c86` 移除 GitNexus 强制流程，`03993303` 实现任务/决策结构校验并注册模板模块。
- 修复前本地 CI：Core 399 通过、1 跳过；CLI 1901 通过、4 失败。新增的配置缺失警告导致 1 项回归，继承 Pi 会话环境导致 1 项失败，未初始化 marketplace 导致 2 项文件缺失失败。初次 CI 日志位于 `/tmp/trellis-ci.0KQPZN/`。
- 本轮代码修复：配置文件缺失时静默关闭；不再因无关 flow/merge YAML 形式产生结构校验错误。保留已识别开关声明的格式/重复检查，以及损坏符号链接、读取失败的错误处理；本地和模板副本同步。
- marketplace 已初始化至仓库锁定提交 `7d5298d16e07c328c09493eed1f0652571744b17`；未更改 gitlink，也未初始化无关 docs-site 子模块。
- 检查子进程清除 `PI_SESSION_ID`、`PI_SESSIONID`、`PI_SESSION_FILE`，使用独立临时目录及 `LC_ALL=C / LANG=C / LANGUAGE=C`；不改变宿主环境、全局 Git 配置或测试文件。
- 75 个已跟踪 Python 文件通过 Python 3.9 语法 AST 检查及本机解释器 py_compile；`pnpm typecheck`、`pnpm --filter @mindfoldhq/trellis lint:py`、`pnpm lint`、`pnpm build` 均 exit 0。Python 类型检查保留 68 条 warning，0 errors。
- Core 与 CLI 分别执行现有 `vitest run --maxWorkers=2`（default + JSON reporter），范围不加过滤：Core **399 通过、1 跳过**；CLI **1905 通过、0 失败**。两包合计 **2304 通过、1 跳过**。CI 所列构建产物及分发后的 `common/task_validation.py` 存在。
- 本轮 8 个检查阶段均 exit 0。日志和退出码：`/tmp/trellis-ci-fix.DoZo13/status.tsv`；机器报告：同目录 `test-core.json`、`test-cli.json`。
- 环境边界：本机 macOS / Node 24 / Python 3.14，不是 CI 的 Ubuntu / Node 20 / Python 3.9。AST 检查不能替代 Python 3.9 运行；未触发远程 GitHub Actions。本轮没有新增或修改测试资产、依赖清单、锁文件、CI 或全局配置。

### 静态证据边界

| 范围 | 静态证据 | 不能据此声称 |
| --- | --- | --- |
| 本轮规划文件 | Markdown 结构、JSON/JSONL 解析、引用存在性、明确分类与当前 in_progress 状态 | 产品功能已实现 |
| 修改后的 Python | 源码语法/类型诊断，不导入或执行业务模块；有配置时用 LSP | 程序运行正确、测试通过 |
| 双份脚本 | 仅本次四组对应文件的字节比较 | 全仓库无漂移 |
| 修改范围 | 定向 git diff / git diff --check，分开观察暂存与工作区 | 无关既有改动由本任务产生 |
| 配置和文档 | 仅已修改文件的格式、键值、章节与链接结构 | 真正 start/archive 已受保护 |

可使用的只读 Git 命令（执行时限定为本次实际修改文件）：

```bash
git diff --check -- <modified-files>
git diff --cached --check -- <modified-files>
git diff -- <modified-files>
git diff --cached -- <modified-files>
```

初次交付仅执行静态解析；本轮已按用户授权执行上述运行检查。各类证据仅证明对应范围，不将一次 CI 通过表述为所有平台或所有行为均已验证，也不为获得通过而修改测试资产。

## Review Gates

1. **规划评审**：用户确认设计的纳入标准、字段/章节、关联集合和局限，并单独批准实施。此前只允许修改本任务规划产物。
2. **启用次序**：脚本及本地材料先完整，开关最后写入；不以默认关闭掩盖未完成实现。
3. **完成判定**：按当前已获授权的范围核验。本轮完成现有 CI 检查及主线程一次限定静态检查，记录结果和环境限制；未完成或阻塞项保持未完成。新增提交、推送和归档不自动执行。

现有清单供上下文读取，不授权派生审查子代理。不得在收尾阶段重新进行功能、业务或风险复核。

## Rollback Points

- 步骤 1 未满足：保持 planning，不写产品代码，也不启用配置。
- 步骤 2–3 出现阻塞：保持检查未启用，记录未完成项并报告；需要撤销时只撤销本任务修改，两份脚本同步处理。
- 本地启用导致现有任务缺材料：默认补齐被点名任务，不批量迁移、不放宽规则。若用户明确要求操作性回退，可关闭本地开关，并说明因此恢复无新增结构阻断的旧行为。
- 不删除决策库、任务文档或历史理由来回退；不 reset 工作区、清理目录或覆盖用户改动。
