---
name: change-handoff
description: Keep lightweight local task notes during coding, checkpoint them at commits, and generate an evidence-based handoff only when review is requested. Use for tracking AI coding changes, commit handoff checkpoints, and preparing review reports. Does not replace code review, install Git hooks, or reconstruct unavailable history.
---

# Change handoff

Keep development lightweight: maintain local notes without requesting routine
input, and generate a human-facing report only when review is requested. Match
the user's language and repository conventions. Record facts, material decisions,
and evidence, not private reasoning, raw transcripts, or a tool-by-tool diary.

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
- Do not create a PR, publish, commit notes, install hooks, edit agent settings,
  or delete historical notes as a side effect. External actions follow the user's
  authorization. Installation alone does not guarantee automatic invocation.

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
