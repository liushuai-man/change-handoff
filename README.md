# change-handoff

用于记录每次 agent 具体怎么 coding 的 skill：把需求、关键决策、行为变化、代码位置和验证证据对应起来，帮助 code review 判断这次工作是否解决了问题。

一份任务或 PR 维护一份交接说明，跨 commit 更新。它记录可核查的结论和证据，不保存完整对话、内部推理或工具流水账，也不替代独立代码审查。

## 安装

可安装内容在 `skills/change-handoff/`，不需要安装 Python 依赖。把这个文件夹复制到你的技能目录；例如在 PowerShell 中，从仓库根目录执行：

```powershell
# 默认 Codex 技能位置；如果配置了 CODEX_HOME，请使用对应位置。
$skillDestination = Join-Path $env:USERPROFILE '.codex/skills/change-handoff'
if (Test-Path -LiteralPath $skillDestination) {
    throw '目标已存在，请先检查并合并已有自定义内容。'
}
New-Item -ItemType Directory -Path (Split-Path $skillDestination) -Force | Out-Null
Copy-Item -LiteralPath './skills/change-handoff' -Destination $skillDestination -Recurse
```

安装只复制 skill，不修改全局 agent 规则或添加 hooks。其他支持同类 SKILL.md 的工具，可使用其技能目录；未验证各工具的自动发现行为。

## 使用

最好在开始任务时调用，并在同一任务中持续维护：

```text
使用 $change-handoff 跟踪这次修改：修复订单页面连续点击产生重复请求的问题。
以当前 HEAD 为任务基线，交付时生成交接说明。
```

也支持结束时补录：

```text
使用 $change-handoff，为当前分支准备 review 交接说明。
比较基线是 <实际的任务起点 commit>，请明确标注无法追溯的决策和未执行的验证。
```

已有交接说明时继续更新同一份，不因新增 commit 重建报告。自动选择 skill 只是辅助；要明确要求记录时，请显式调用。仅安装 skill 不保证每次编码都会运行它。

## 交接说明包含什么

- 用户要求、验收条件，以及 agent 自行推断的业务规则。
- 触发条件下，行为从什么变成什么，对应哪些代码。
- 影响最终实现的关键决策及取舍。
- 实际执行的检查、结果、覆盖的代码状态和未验证部分。
- 明确的 review 关注点、兼容性风险和待确认假设。
- 完整基线 commit、观察到的代码 HEAD、尚未提交的任务改动及原有改动边界。

补录会标为 reconstructed，不能从最终 diff 杜撰开发历史。代码更新后，旧验证证据可能失效；skill 会要求刷新记录或标为过时。报告本身的提交不需要反复把自己的 SHA 写进报告。

## 存在哪里，怎么控制增长

优先沿用已有且有权限编辑的 PR 描述；没有可用 PR 流程时，保存到 `docs/changes/YYYY/MM/<task-slug>.md`。明确要求只在聊天输出时，不创建文件。无法更新远端 PR 时交付本地草稿，并说明远端尚未更新。

一个任务的多次 commit 只维护一份最终说明。临时过程留在会话或已有的忽略目录，不默认写进 Git。截图、视频、完整日志和 Git 采集 JSON 不默认归档。不会自动删除历史、修改忽略规则或建立外部存储。

历史说明只描述当时那次变更；后续任务引用它，不把旧说明改成当前系统文档。长期有效的设计理由适合进入已有架构文档。查历史按任务、PR 或代码位置检索，不默认把所有历史加载进上下文。

## Git 信息采集器

可选 helper 使用 Python 3.10+ 和 Git，只执行本地只读查询，不依赖 GitHub CLI 或联网：

```sh
python skills/change-handoff/scripts/collect_context.py --repo . --base HEAD
```

`--base HEAD` 适用于刚开始的新任务。后续继续使用最初记录的完整基线 SHA，不能每次都用移动后的 HEAD。已完成分支的比较起点应来自实际任务边界，脚本不会猜 main 或 HEAD~1。

输出 JSON 分别列出 base→HEAD 的已提交变更、暂存、未暂存、未跟踪路径和冲突路径。不指定 `--base` 时已提交比较为 `null`，不是“没有改动”。无初始 commit 时 HEAD 为 `null`；显式指定不存在的 base 会报错，不会静默替换。

脚本只提供版本和路径状态，不能判断业务语义、改动归属或测试是否通过。它不读取未跟踪文件正文、忽略文件、编辑器未保存内容和子模块内部状态；采集也不是原子快照。未提交代码不能仅用 HEAD 精确标识。

## 项目规则与验证

- [AGENTS.md](AGENTS.md)：开发边界和验证命令。
- [SKILL.md](skills/change-handoff/SKILL.md)：唯一的工作流程入口。
- [模板](skills/change-handoff/assets/handoff-template.md)：交接说明的起点，可按实际改动缩减。
- [案例](skills/change-handoff/references/examples.md)：多 commit、补录、原有改动、过时记录等情形。
- `tests/`：标准库 unittest 测试；不需要网络或第三方包。

在仓库根目录执行：

```sh
python -m unittest discover -s tests -v
python skills/change-handoff/scripts/collect_context.py --repo . --base HEAD
git diff --check
```

测试验证 Git 采集的实际行为，包括不改变索引和 HEAD。案例需人工核对；Markdown 指令和路径采集不能保证记录真实、完整或持续更新。
