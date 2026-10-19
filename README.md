# change-handoff

开发时轻量记录，commit 时更新，需要 review 时再生成报告。

每个任务维护一份本地记录，不写流水账，不为每次 commit 或 push 生成文档。

## 安装

将仓库里的 `skills/change-handoff/` 文件夹复制到你的技能目录，例如 `~/.codex/skills/change-handoff/`。已存在时先合并自定义内容，避免直接覆盖。

## 日常开发

任务开始时说：

```text
使用 $change-handoff 跟踪这个任务，平时只记录，需要 review 时再生成报告。
```

想减少手动调用，可把下面这句话加入项目的 `AGENTS.md`：

```text
编码任务使用 change-handoff：维护本地过程记录，成功 commit 后更新检查点，仅在要求 review 时生成报告。
```

| 时机 | 动作 |
| --- | --- |
| 开始任务 | 记录需求、代码基线和已有改动 |
| 重要变化 | 记录关键决策、假设和实际验证结果 |
| Commit 成功 | 更新同一份记录，关联 commit SHA |
| Push | 检查漏记，不生成新文档 |
| 需要 review | 对照最终代码，生成交接报告 |

普通记录不需要开发者逐条确认。安装 skill 本身不保证自动执行；手动 commit 可能不会触发，下次调用时会根据可用证据补录，缺失信息会标明。

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
  tasks/<task>.md      # 过程记录，跨 commit 更新
  reports/<task>.md    # review 时生成
```

首次使用会确保 `.gitignore` 包含 `/.change-handoff/`。已被 Git 跟踪的文件不会自动取消跟踪；项目禁止修改忽略规则时，会改用已有忽略目录或说明记录限制。

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
