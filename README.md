# change-handoff

开发时轻量记录，commit 时更新，需要 review 时再生成报告。

每个任务维护一份本地记录，不写流水账，不为每次 commit 或 push 生成文档。

## 安装

将仓库里的 `skills/change-handoff/` 文件夹复制到你的技能目录，例如 `~/.codex/skills/change-handoff/`。已存在时先合并自定义内容，避免直接覆盖。

## 首次使用

安装后，在项目里调用一次：

```text
使用 $change-handoff
```

Skill 会主动让你选择：

| 模式 | 后续怎么用 |
| --- | --- |
| 自动（推荐） | Skill 写入项目 `AGENTS.md`，后续开发由 agent 自动记录 |
| 手动 | 不修改 `AGENTS.md`，需要记录时自己调用 `$change-handoff` |

选择保存在本地，后续不重复询问。自动模式不需要你自己复制规则；想切换时说“改成手动模式”或“改成自动模式”。

## 日常开发

| 时机 | 动作 |
| --- | --- |
| 开始任务 | 记录需求、代码基线和已有改动 |
| 重要变化 | 记录关键决策、假设和实际验证结果 |
| Commit 成功 | 更新同一份记录，关联 commit SHA |
| Push | 检查漏记，不生成新文档 |
| 需要 review | 对照最终代码，生成交接报告 |

普通记录不需要逐条确认。自动模式依赖 agent 读取项目规则；手动 commit 不保证触发，下次调用时补录可确认的信息。

## 开始 review

```text
使用 $change-handoff，基于这个任务的记录和最终代码生成 review 报告。
```

报告包含：需求与假设、行为变化、关键决策、代码位置、验证结果和需要关注的问题。已有报告会更新，不重复创建。代码变化后，旧报告和相关验证会标记为过时。

交接报告是审查材料；继续检查代码时说：

```text
结合这份报告 review 实际 diff，找出错误、回归和需求遗漏，不要直接采信报告结论。
```

没有过程记录也能生成报告，但会标为补录，不编造历史决策或测试结果。

## 存储

默认保存在本地：

```text
.change-handoff/
  config.json         # 首次选择的使用模式
  tasks/<task>.md      # 过程记录，跨 commit 更新
  reports/<task>.md    # review 时生成
```

选好模式后会确保 `.gitignore` 包含 `/.change-handoff/`。已被 Git 跟踪的文件不会自动取消跟踪；无法保存配置或写入规则时会明确说明。

需要共享时，可明确要求把报告放到 PR 描述或 `docs/changes/`。只忽略过程记录、提交最终报告也可以。不会默认保存完整对话、日志或截图，也不会自动删除历史记录。

## 开发与检查

项目规则见 [AGENTS.md](AGENTS.md)，流程见 [SKILL.md](skills/change-handoff/SKILL.md)，[案例](skills/change-handoff/references/examples.md)覆盖补录、原有改动和记录过时等情形。

Python 3.10+ 和 Git，无第三方运行依赖：

```sh
python -m unittest discover -s tests -v
python skills/change-handoff/scripts/collect_context.py --repo . --base <任务起点SHA>
git diff --check
```

采集器只读 Git 版本和路径状态，不运行测试、不判断业务语义，也不读取未跟踪文件正文。基线固定为任务起点，不随 commit 移动。
