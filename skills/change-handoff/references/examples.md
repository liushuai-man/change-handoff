# Examples and review cases

These are fictional examples, not executed checks or evidence for a real task.

## Ongoing task with many commits

Request: prevent duplicate order submission from rapid clicks. The task starts
at commit A, advances through B and C, and ends with uncommitted error handling.

Maintain one record with base A and observed HEAD C. State that the working tree
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
handling. Update the same task report and mark the earlier result stale until
the relevant check is rerun. A correction only to report wording does not by
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
