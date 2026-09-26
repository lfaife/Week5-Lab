# Week5 Lab Notes
## CLI structure and environments
Question: The python -m knight_tasks.cli list --sort priority or the one with python -m knight_tasks.cli add "Email TA" --priority medium. What do these commands do, and is it only specific to the cli file? Are the knight_tasks commands ideal for every environment? Does it have a play in TDD or characterization testing?

  ## What role would it play in different environments, and how would you recreate it if its useful.

  Constraints: Search feeds related to topic, no academic journals / peer-reviews.

## Answer: 

Beyond CLI: A Generalized Design Pattern

The knight_tasks structure is not specific to the CLI file—it's a separation of concerns pattern that applies across any entry point. The three-layer design lets you:

- Reuse service.py in a web API, background task, or Slack bot without duplicating logic
- Test service.py independently (no mocking file I/O needed)
- Swap storage backends (JSON → SQLite → cloud) without touching service logic


# Is It Ideal for Every Environment?

Not universally, but widely applicable:

| Environment | Fit | Notes |
|-------------|-----|-------|
| CLI tasks | ✅ Excellent | Pure argparse design, no dependencies |
| Web API | ✅ Good | Reuse service layer for endpoints |
| Embedded/constrained | ⚠️ Moderate | JSON works; consider binary storage for size constraints |
| High-throughput | ⚠️ Requires change | JSON file I/O isn't concurrent-safe; need SQLite or async persistence |
| Distributed | ❌ Poor | File-based persistence doesn't work across machines |

The pattern scales; the implementation (JSON files) is the bottleneck.

# Advantages of this structure:
- ✅ Easy to test (Service has zero dependencies)
- ✅ Easy to extend (swap storage; add new CLI commands)
- ✅ Easy to debug (pure functions; no hidden state)
- ✅ Works across entry points (CLI, API, cron jobs all use same Service)

# When NOT to use:
- Simple scripts (overhead > benefit)
- Throwaway prototypes
- Single-file utilities

---

# Key References

- Layered Architecture & Separation of Concerns
- Service Layer Design Pattern
- Testing Argparse with Pytest
- Characterization Tests for Legacy Code

# Plan mode and strong prompts
Statements:
- The strong prompt has five parts: symptom, evidence, target, constraint, proof. 
- Before multi-file feature, do "Plan Mode: Read a Plan, Not a Wrong Diff.
- Creating plans avoids cheap mistakes by viewing a noisy patch, rewriting tests, and another agent pass. 
With the plan those issues were  a paragraph of feedback; without it, they become commits and rework.

# Why auto-accept was reasonable here—and when it isn’t:
Reasonable: scope was already decided (layers, today param, no new deps, parsing in cli.py); the change was small and local; tests were part of the plan; you could verify with pytest plus a quick manual check. 

Auto-accept is for “execute the approved plan,” not “invent the design.”

# Not reasonable: 
Vague prompts (“make it better”), auth/payments/migrations unfamiliar code, anything that deletes
tests or adds deps, or when you haven’t read what will change. Then approve edits one file at a time—or stay in plan mode.

Human-team equivalent of “plan is free to read and cheap to change”
A design review / RFC / tech design doc (or a short PR description and checklist before code): 
peers catch layering, compatibility, and testability in comments. Rewriting a section costs minutes; 
rewriting a merged PR costs days. Same idea as your class checklist before anyone approved the agent’s plan.

# Permissions and prompt injection
## Part 5: Permissions and Prompt Injection: 5a. Turn a rule into a guarantee:

Despite commands run Claude.md which is the base the codebase should read,
you should place permissions in .claude settings.json to create a deny rule.

## 5b. Attack your own agent (6 minutes):

Placing HTML comment in .md files can cause hidden instructions to AI 
to run commands without notifying you. 

Prevent by activating permission rules in .claude 

# Undo and recovery
## Part 6: Undo and Recovery:

After you commit latest change, use /rewind to revert to last commit to delete changes.
(Options to refresh code / convo or both)

# Discuss:

/rewind and checkpoints are in the same family: 
they restore local files / session state the agent touched, not the outside world.

They do not undo side effects outside that:

a database migration (DB already changed)
a deleted branch (git ref gone)
a sent email (already left the machine)
a pushed commit (remote already has it)

--

# Context and new sessions
Continuing after two failed corrects causes answers to become worse because the context is the problem.

Switch to a new session when the conversation itself is hurting you more than helping—i.e. the context window is full of noise, not useful state.

# Do it when:

Two failed fixes in a row on the same bug (Monday’s rule)—wrong code, bad theories, and error spam are now in the prompt.

The agent contradicts itself, re-applies a bad patch, or “fixes” things that aren’t broken.

You’re starting a different task (due dates done → permissions → unrelated feature) and the old thread adds no signal.

The thread is huge—long tool dumps, many rewrites—and answers get vaguer or ignore recent instructions.

You rewound/restored files to a clean commit but the chat still “remembers” the broken approach.

# Don’t bother when:

You’re mid-plan with a clear next step and the agent is still on track.

You only need a small follow-up that depends on what was just decided.

Practice: commit (or rewind) so the repo is clean, then open a fresh session so the context matches that clean tree. New session resets judgment; it doesn’t undo pushes, migrations, or emails.

# Headless mode and CI
## Part 7: Headless Mode:

claude -p "List the public functions in knight_tasks/service.py, one line each." 
(The first command needs only file functions)

claude -p "Run the test suite and report only the pass and fail counts." \
--allowedTools "Bash(python -m pytest:*)"

(The second needs to run a command. Nobody is there to approve it, so the permission must be
granted up front with --allowedTools. Your settings.json allow rule also covers it. Simply allows the "allow" values)

claude -p "Summarize the last 3 commits as release notes." --output-format json
(The third returns JSON with the result plus metadata such as cost and duration, ready for a
script to parse.) ^ 3rd is good for showing cost / duration?

3rd command = observability + machine-readable output; improvement comes from what you do with those numbers.

--

# Discuss
## Where in a CI pipeline would one of these be useful? Where would it be dangerous?

Where headless -p is useful in CI

| Job | Why it fits |
|-----|-------------|
| Report-only — “run pytest, print pass/fail counts” | Deterministic, read-ish, fail the job on red tests |
| Summarize — last N commits → release notes / changelog draft | Output to artifact or PR comment; no repo mutation |
| Review assist — list APIs, describe diff (read tools only) | Extra signal for humans; doesn’t merge itself |

Best as a side step: produce text/JSON metrics, never as the thing that deploys or pushes.

Where it’s dangerous

| Situation | Risk |
|-----------|------|
| Agent can write files / commit / push on a stranger’s PR | Prompt injection + egress (Monday’s triangle) |
| Secrets in the env and broad Bash/network allow | Leak via logs, curl, or “helpful” debug prints |
| Auto-merge / deploy driven by model output | Hallucinated “all good” ships bad code |
| --allowedTools too wide (Bash(*), unrestricted Write) | Same as unsupervised root on the runner |

## In headless mode no human approves each step. What does that do to the permissions you would grant?

CI at 3 a.m. = no permission prompts. Untrusted PR + secrets + outbound = full attack surface.

No human approvals → what permissions you grant

Tighten hard. Interactive “I’ll click Deny if it looks weird” is gone.

- Prefer deny by default; allow only the exact tool patterns the job needs (like your Bash(python -m pytest:*)).
- Prefer --allowedTools on the command so the job is self-describing and minimal.
- Keep settings.json deny for .env, git push, rm, etc., and load that same config in CI.
- Don’t grant Write/network/push “just in case.”
- If the step only needs to read code, don’t allow Bash at all.

Rule of thumb: grant the smallest toolkit that can’t exfiltrate or mutate, then measure with --output-format json—don’t widen tools to make the agent “more helpful.”