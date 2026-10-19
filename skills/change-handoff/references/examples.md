# Examples and review cases

These are fictional examples, not executed checks or evidence for a real task.

## First-use choices

In a new project, the user says "Use change-handoff" without a mode. Offer
automatic/manual choices before changing AGENTS.md or persisting a preference.
No answer means no chosen mode, not consent to automatic setup.

If automatic is selected, merge the marked rule with the verified installed skill
path, preserve existing project instructions, then save agent mode. Repeating
setup must not duplicate the rule. If manual is selected, save manual mode and
leave AGENTS.md unchanged; future implicit selection must not enable recording.
Either mode records normal coding without generating a review report.

On a new session, reuse the valid saved choice without asking again. A project
already explicitly requiring automatic use also has a choice; notes without a
mode or rule do not. If writing AGENTS.md fails, do not save successful automatic
setup or claim it works. Report the incomplete setup.

Switching from the marked automatic rule to manual removes only that block and
preserves other project rules. If an unmarked rule still requires automatic use,
resolve the conflict rather than claiming manual mode overrides it silently.

## Ongoing task with many commits

Request: prevent duplicate order submission from rapid clicks. The task starts
at commit A, advances through B and C, and ends with uncommitted error handling.

Maintain one local notes file with base A and observed HEAD C, with short
checkpoints for successful commits B and C. Push creates no extra file or report.
Generate the report only when review is requested. State that the working tree
also contains task-owned error handling. Explain the button lock at the submit
handler, its release on failure, and the limitation that this does not establish
server-side idempotency. If a double-click check ran at B, do not present it as a
check of the final error handling. After committing, update observed code HEAD;
do not move the task base to the previous commit.

## Late reconstruction

Request: "Explain this branch for review." Only the final diff is available.

State that the report is reconstructed from the request and diff. Describe the
observable behavior and code locations. The original reason for an architectural
choice is unknown unless evidence is available. Write "not run in this session"
for verification; tests present in the diff are not proof that they passed.
If the branch comparison target is ambiguous, establish it before declaring
coverage. Continue inspecting visible code while that question is unresolved.

## Existing work and ambiguous ownership

At task start a payment module is already staged; the requested task concerns a
form label. Preserve the staged work and list it as pre-existing. Do not claim it
as the skill user's change or stage it along with the report. If both changes
touch the same file and cannot be separated from evidence, mark attribution
uncertain. Git status establishes file state, not authorship.

## Finalized handoff becomes stale

A report says timeout recovery passed at C. A later code edit changes timeout
handling. Update the notes and mark the existing report and earlier result stale.
Rerun the relevant check and regenerate the report on the next review request.
A correction only to report wording does not by
itself invalidate code tests. A new unrelated task gets its own report even if
it starts on the same branch.

## No history or destination access

If HEAD does not exist, describe new files and explicitly report unavailable
commit coverage. If the requested base is absent in a shallow clone, do not
silently substitute HEAD or fetch without considering network authorization.
If PR editing is unavailable, save a local draft and report that delivery to the
PR is outstanding. Never claim a PR update because a draft was produced.

## Confidential or large evidence

An error log contains an access token. Record the sanitized error category and
the relevant outcome, not the log. Keep video, screenshots, transcripts, and
context JSON out of the permanent report by default. A link's availability and
retention are limitations; do not imply linked evidence is permanently stored.

## Setup and manual commits

On first use, ensure `/.change-handoff/` is ignored before writing local notes.
Already-tracked notes are not hidden by adding the rule; disclose that condition
and do not remove them from Git automatically. If rule edits are forbidden, use
an existing ignored location or state that notes are limited to the conversation.

If a developer manually creates two commits, the skill may not have run. At the
next invocation, reconcile both commits from available history and notes. Label
unknown test execution as unknown. If one commit was amended, replace its old
checkpoint identity when established, preserving still-valid decision evidence;
do not silently treat the old SHA as reachable or reset the task base.
