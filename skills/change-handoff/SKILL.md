---
name: change-handoff
description: On first use, offer manual invocation or project AGENTS.md integration, then keep lightweight task notes and commit checkpoints in the selected mode. Generate an evidence-based handoff only when review is requested. Use for tracking AI coding changes and preparing review reports. Does not replace code review, install Git hooks, or reconstruct unavailable history.
---

# Change handoff

Keep development lightweight: maintain local notes without requesting routine
input, and generate a human-facing report only when review is requested. Match
the user's language and repository conventions. Record facts, material decisions,
and evidence, not private reasoning, raw transcripts, or a tool-by-tool diary.

## First use: offer a mode

Before task recording, read project instructions and `.change-handoff/config.json`
if present. Reuse a valid saved mode or an existing explicit project/user choice.
Notes files alone do not establish a mode. For an unconfigured project, proactively
ask once, in the user's language, with these two choices:

> How should this project use change-handoff?
> 1. Automatic (recommended): add a rule to this project's AGENTS.md; agents keep
>    local notes and commit checkpoints without repeated invocation.
> 2. Manual: record only when you explicitly invoke change-handoff; leave AGENTS.md unchanged.

Use a supported choice UI when available, otherwise ask in chat. Wait for the
answer before saving a mode or editing project rules. Do not default to automatic
because time passed or the user did not answer. Independent requested work may
continue. An explicit mode choice already given in the request needs no repeat.

After selection, ensure the local directory is ignored as described below and
save `.change-handoff/config.json` with `schema_version: 1` and `mode: "manual"`
or `mode: "agent"`. Preserve unrelated settings. In automatic mode, also save
`agent_file: "AGENTS.md"` only after the project rule is successfully written.
Use [the project rule](assets/agents-rule.md), replacing its path prompt with the
verified installed skill's absolute SKILL.md path. Merge one marked block into
the repository-root AGENTS.md; create the file if absent. Preserve all unrelated
instructions and update an existing matching block instead of appending duplicates.
The user's automatic choice authorizes this project-scoped edit; no second
confirmation is needed. Do not edit global instructions or commit/push settings.

On later invocations, do not ask again unless the user requests a mode change or
saved settings conflict with project rules. Manual mode must not start recording
merely because the skill was implicitly selected: require explicit invocation or
an ongoing explicitly enabled task. Automatic mode follows the project rule.
If setup cannot persist settings or write its rule, disclose the failure and do
not claim automatic setup succeeded. If the referenced installation later moves
or disappears, report it and repair only from a verified skill location.

When switching to manual, remove only this skill's marked automatic rule and
save manual mode; preserve other instructions. An unmarked existing rule that
still requires automatic tracking needs reconciliation, not a conflicting setting.
Report setup completion once, then keep normal recording unobtrusive. Installation
alone cannot offer this prompt: it appears when the skill first runs in a project.

## Establish scope and destination

Read repository instructions and any existing notes or report for this task first.
Determine the task/PR identifier, requested behavior, relevant starting state,
and destination from the conversation and repository. Ask only when ambiguity
would mix unrelated work or select the wrong comparison base.

- Keep one notes file per task/PR across commits, not one file per commit or push.
  Reuse the stable task identifier; separate unrelated tasks on the same branch.
- Default notes: `.change-handoff/tasks/<stable-task-slug>.md`. Reuse an existing
  configured local location when present. Before writing, ensure Git ignores it.
  On initial setup, add only `/.change-handoff/` to the repository .gitignore if
  necessary, preserving existing rules. This is a Git rule, not an `.ignore` rule.
  Check whether files are already tracked: do not automatically untrack them or
  claim the ignore rule hides them. If ignore-file edits are prohibited, use an
  existing ignored location or conversation and disclose the persistence limit.
- Default review report: `.change-handoff/reports/<stable-task-slug>.md`, produced
  only on request. Honor a requested chat-only, tracked-document, or PR destination.
  Preserve unrelated PR text and use authorized tools; otherwise keep a local
  draft and state that remote delivery remains outstanding.
- Do not create a PR, publish, commit notes, install hooks, edit agent settings
  beyond the chosen project setup, or delete historical notes as a side effect.
  External actions follow the user's authorization. Automatic mode relies on
  the host loading and following AGENTS.md; it is not a Git event listener.

Use [task notes](assets/task-notes-template.md) during development and
[the report template](assets/handoff-template.md) at review time. Fill only
applicable sections, remove placeholder prompts, and explicitly retain material
unknowns. Read [examples and review cases](references/examples.md) when choosing
between ongoing tracking, late reconstruction, or updating a stale handoff.

## Start or resume

Capture the request, acceptance criteria, consequential inferred requirements,
and a stable base commit before implementation when possible. Select the base
from the actual task boundary; do not guess `main`, `HEAD~1`, or a merge base.

The optional read-only helper needs Python 3.10+ and Git:

```sh
python <skill-dir>/scripts/collect_context.py --repo <repo> --base <base-ref>
```

It resolves refs to full commit IDs and lists committed, staged, unstaged, and
untracked paths separately. It does not read untracked content, inspect diffs for
semantics, run tests, fetch, or write repository files. Its JSON is a local aid,
not a second permanent report. Inspect relevant code and diffs yourself.

Record pre-existing staged, unstaged, and untracked work as a boundary, not as
your contribution. Preserve an existing task base when resuming; HEAD moving
does not start a new task. If base history is missing, report the limitation
instead of claiming a complete comparison. A new repository without HEAD can
still have a handoff based on its visible files, with commit coverage unavailable.

When invoked late, label the record **reconstructed** and identify its sources
(current request, available conversation, final diff). Do not invent earlier
decisions, intermediate states, original intent, or commands that were not seen.

## Maintain during work and commits

Update the same notes file when requirements, approach, scope, or verification
materially change; do not wait until commit to remember a critical decision.
No formal report or routine progress announcement is needed for note updates.
Keep only decisions relevant to the final change; preserve an
abandoned approach only when it explains a remaining tradeoff. Distinguish:

- explicit user requirements from assumptions awaiting confirmation;
- observed behavior from inferred behavior;
- checks actually run from proposed checks;
- changes belonging to this task from pre-existing or concurrent work.

For a decision, give the chosen approach, practical reason, and consequence.
Do not expose chain-of-thought or record every alternative considered. Avoid
credentials, personal data, full prompts, raw logs, and large binary evidence.
Summarize sanitized evidence and link to existing accessible artifacts if useful.

When the agent makes an authorized commit, capture the relevant facts before
committing, then checkpoint the actual resulting full SHA and verification state
after success. Do not commit merely to create a checkpoint. Failed commits do
not get successful checkpoints. Update an existing checkpoint rather than
duplicating it when no new commit exists. Keep checkpoints short (SHA, behavior
delta, check result/unknown); do not copy whole diffs or repeatedly copy the notes.

Push is a sync point: check for missing checkpoints using available evidence;
do not create another record or generate a report. Manual commits made outside
the agent are not guaranteed to trigger this skill. On resume, reconcile history,
including amended/rebased commits, with existing notes; mark unrecoverable
context missing rather than fabricating it. Preserve the original task boundary
or explain when rewritten history makes the comparison unavailable.

## Generate a report when review is requested

A request such as "prepare review", "generate a handoff", or an explicit report
request activates this phase. Finishing coding, committing, or pushing alone
does not. Read this task's notes, then independently reconcile them with code;
do not concatenate checkpoints and call that a report.

1. Re-read the actual final diff and relevant code, including staged, unstaged,
   and task-owned untracked files. Reconcile each material claim with the code.
   A list of filenames alone does not explain behavior.
2. Explain meaningful changes as trigger -> previous behavior -> new behavior.
   Map them to verified paths and symbols; add line numbers only when checked.
   Separate observed defects from plausible risks.
3. State each executed check with its command or manual procedure, result, and
   code state tested. A passing test does not prove uncovered behavior. Preserve
   failures and skipped checks that affect confidence. Mark earlier checks stale
   after relevant edits unless rerun, or explain why the edits do not affect them.
4. Refresh coverage: full base commit, observed HEAD, whether task code has
   uncommitted/untracked changes, and exclusions or pre-existing work. HEAD alone
   does not identify a dirty working tree. Avoid claiming an exact reproducible
   revision for unsaved, untracked, or uncommitted content.
5. Surface unresolved business assumptions, compatibility risks, and specific
   reviewer decisions. State unverified behavior explicitly. Do not turn missing
   evidence into a positive assurance.

Keep the report out of its own code coverage claim: record observed code HEAD
and say whether the handoff itself is pending. Do not repeatedly commit a new
report just to insert that report's own commit SHA. If only the report changes,
the code comparison remains valid. If code changes after finalization, update
the notes and mark the existing report stale. Regenerate it on the next review
request before calling it current.

## Retention and completion

Keep lightweight notes locally between sessions; generate only the requested
concise report in its chosen destination. Do not read all
historical reports by default; search by task/PR, path, or topic when history is
needed. Historical handoffs describe their own change, not current system truth.
Link a later task to a relevant older record instead of rewriting past decisions.
Propose updating existing durable architecture documentation when appropriate,
but do not create a new documentation program as a side effect.

At review delivery, report where the handoff was saved, what code state it covers,
and material limits. During ordinary development, mention recording only if
setup, missing history, or a persistence failure requires attention. The skill
does not guarantee invocation, truthfulness, freshness, or review completeness.
