---
name: change-handoff
description: Maintain an evidence-based task or PR handoff during coding and prepare a review-ready explanation of requirements, decisions, behavior changes, code locations, and actual verification. Use when asked to track AI coding changes, explain a change for review, or maintain a change handoff across commits. Does not replace code review or reconstruct unavailable development history.
---

# Change handoff

Give the reviewer a checkable connection from user intent to behavior, code, and
verification. Record conclusions, material assumptions, and evidence, not private
reasoning, raw transcripts, or a tool-by-tool diary. Match the user's language and
the repository's conventions. Scale detail to the change; a small fix needs only
a short record.

## Establish scope and destination

Read repository instructions and any existing handoff for this task first.
Determine the task/PR identifier, requested behavior, relevant starting state,
and destination from the conversation and repository. Ask only when ambiguity
would mix unrelated work or select the wrong comparison base.

- Keep one record for one task/PR, updating it across commits. Separate unrelated
  tasks even when they share a branch. Do not generate a report per commit.
- Prefer an existing PR description when a PR workflow and authorized editing
  tools are available. Preserve unrelated PR text. Otherwise write
  `docs/changes/YYYY/MM/<stable-task-slug>.md`, using the user's local date.
  An explicitly requested chat-only handoff stays in chat.
- Draft locally if a PR destination cannot be edited. Do not create a PR, publish,
  install hooks, change retention rules, or modify agent configuration merely
  to deliver a handoff. External updates follow the user's actual authorization.
- Keep working notes in an existing ignored scratch location or conversation;
  do not change .gitignore or create permanent scratch logs just for this skill.

Use [the template](assets/handoff-template.md) as a starting point. Fill only
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

## Maintain during work

Update the same record when requirements, approach, scope, or verification
materially change. Keep only decisions relevant to the final change; preserve an
abandoned approach only when it explains a remaining tradeoff. Distinguish:

- explicit user requirements from assumptions awaiting confirmation;
- observed behavior from inferred behavior;
- checks actually run from proposed checks;
- changes belonging to this task from pre-existing or concurrent work.

For a decision, give the chosen approach, practical reason, and consequence.
Do not expose chain-of-thought or record every alternative considered. Avoid
credentials, personal data, full prompts, raw logs, and large binary evidence.
Summarize sanitized evidence and link to existing accessible artifacts if useful.

## Finalize against the code

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
the existing report and its verification status before calling it current.

## Retention and completion

Save only the final concise handoff in the chosen destination. Do not read all
historical reports by default; search by task/PR, path, or topic when history is
needed. Historical handoffs describe their own change, not current system truth.
Link a later task to a relevant older record instead of rewriting past decisions.
Propose updating existing durable architecture documentation when appropriate,
but do not create a new documentation program as a side effect.

Report where the handoff was delivered, what code state it covers, and material
limits. The skill guides agent behavior; it does not guarantee invocation,
truthfulness, freshness, or review completeness.
