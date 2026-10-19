# Change handoff: initial change-handoff skill

- Task: develop the skill discussed with the user and connect the supplied GitHub repository.
- Capture: 2026-10-19, reconstructed at delivery from this conversation, tool results, and final files. The baseline and clean working state were observed before implementation; no continuous process diary was maintained.
- Base: `a058e0a05a050eb938f67f8f5aad99c0d7750250`.
- Observed code HEAD: `314bf57128c62bbf6ed7be737c77252ae5ab7e26`.
- Working state at verification: implementation files were uncommitted when tests ran; those same contents were subsequently committed as the observed code HEAD. No pre-existing local edits were present.
- Handoff state: repository record; the subsequent commit adds only this report and does not change tested implementation files. The report's own SHA is intentionally not embedded here.

## Intent and boundaries

The user wants reviewers to understand AI coding work beyond commit messages,
and asked how records should scale as commits accumulate. The requested repository
initialization uses project-agent-init. Chosen implementation: a task/PR handoff
skill, a compact template, realistic examples, a read-only Git helper, and a
Chinese usage guide. No application framework, service, hooks, transcript capture,
global installation, or external evidence storage was added.

## Behavior and implementation

| Trigger | Before -> after | Code location | Evidence / limitation |
| --- | --- | --- | --- |
| Agent prepares a change for review | A one-line repository description -> instructions connecting intent, behavior, code, and verification | `skills/change-handoff/SKILL.md` | Workflow inspected; real agent compliance is not guaranteed |
| More commits land for the same task | No persistence convention -> update one task/PR record while retaining its initial base | SKILL.md, `assets/handoff-template.md` | Multi-commit Git comparison tested; long-running agent behavior not tested |
| Skill is invoked after implementation | No reconstruction policy -> label reconstruction and missing historical evidence | SKILL.md, `references/examples.md` | Fictional scenarios inspected, not live task simulations |
| Reviewer needs repository state | No helper -> separate committed, staged, unstaged, untracked, and conflict paths | `scripts/collect_context.py`: `collect`, `resolve_commit`, `changes` | Nine standard-library tests pass |
| Contributor changes the skill | No project guide -> scope and verification commands available | `AGENTS.md`, `tests/test_collect_context.py`, README.md | No stack profile applies to this Python/Markdown skill repository |

## Material decisions

- Use one final record per task/PR to reduce duplication. Prefer an existing
  editable PR description, with a repository Markdown fallback and explicit
  chat-only support. PR integration is instruction-based, not a GitHub API client.
- Git helper reports facts about revisions and paths only. It cannot establish
  authorship, business semantics, test execution, or exact dirty-tree contents.
- Avoid automatic base inference: missing base means no committed comparison;
  invalid explicit refs fail. Unborn HEAD is represented as unavailable.
- Python standard library and Git are enough for runtime and tests. Temporary
  PyYAML was used outside the repository solely for the skill-creator validator;
  it is not a runtime or repository dependency.

## Verification

Commands below use `python` as shorthand for the bundled Python 3.12 executable
available in this development environment.

| Executed command / procedure | Result | Coverage / limitation |
| --- | --- | --- |
| `python -m unittest discover -s tests -v` | PASS, 9 tests | Multi-commit base, staged/unstaged split, unicode/spaces, read-only index and HEAD, absent/invalid base, unborn HEAD, ignores, deletion/nested invocation, conflicts, CLI JSON/errors |
| `python skills/change-handoff/scripts/collect_context.py --repo . --base a058e0a05a050eb938f67f8f5aad99c0d7750250` | PASS | Actual implementation worktree; task edits listed, no fabricated semantic claims |
| skill-creator `quick_validate.py skills/change-handoff` with temporary PyYAML | PASS | Frontmatter/name/scaffold checks; does not validate agent behavior |
| Parse `agents/openai.yaml`, check UI description length and skill prompt, resolve relative Markdown links | PASS | UI metadata and six existing local documentation links |
| `git diff --check` and staged equivalent | PASS | Changed-file whitespace |
| Manual inspection of lifecycle examples and destination rules | Completed | No independent agent simulation, GitHub PR edit, or cross-client discovery test |

## Reviewer attention

- Records can still be omitted, misleading, or stale; no mechanical enforcement
  or independent code review is provided.
- The helper does not inspect ignored files, untracked contents, unsaved editor
  buffers, or submodule internals. Collection is not atomic.
- The helper requires Python 3.10+ and Git; behavior was executed on Windows with
  Python 3.12, not on other operating systems or the minimum Python version.
- The installed workflow is intentionally portable; automatic discovery and
  invocation remain host-dependent and unverified here.
- GitHub push delivery is verified outside this historical code report in the
  user-facing completion message; this record does not claim a remote PR update.
