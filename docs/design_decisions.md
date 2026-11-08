# Design decisions

## Goal
Build the loop that decides, without a human, whether generated learning content is good enough
to ship: generate, evaluate against hard checks, regenerate with reasons, stop safely.

## Architecture
- **LangGraph state machine.** The loop (generate, evaluate, conditional retry) is the product,
  and a graph makes the branches explicit and testable.
- **Hard retry cap (3 attempts).** The loop always terminates. After the cap, the lesson is
  flagged NEEDS_HUMAN_REVIEW instead of silently shipped.
- **Separate generator and judge prompts and models.** A model grading its own draft is biased
  toward approval. (Caveat: a fallback can make both the same model during outages.)
- **Feedback carries reason, quoted evidence and a fix**, so retries are targeted, not "try again".
  The log also records what changed between drafts.

## Rubric
- **Binary checks only.** Each check passes or fails, which makes failures auditable and usable
  as retry feedback.
- **Hybrid evaluation.** Anything measurable is code (sentence length, readability, glossary
  terms, section order, definition-before-use). Meaning-based checks (accuracy, analogy quality,
  coverage) use an LLM judge.
- **Grounding via a fact sheet.** 12 verified facts. Accuracy is judged against them, not against
  the judge's own memory.
- **Judge hygiene.** Strict JSON output, a required evidence quote (verified against the lesson text
  in code, so invented evidence is labeled), and separate rules for "must be present" checks
  (fail if missing) and "must be absent" checks (fail only with a quotable violation).

## What the logs taught me (rubric changelog in docs/rubric_changelog.md)
1. A retry fixed one failure but silently dropped glossary terms. J2 only counted entries, so it
   passed. J2 now requires specific terms.
2. An average sentence length hid a 41-word sentence. L1 now also caps the longest sentence.
3. L3 (idioms) and E1 (needs an analogy) deadlocked: the judge criticized the exam analogy under
   L3. L3 now says "judge wording only".
4. The AI-judged "define terms before use" check was unstable (quoted a sentence without the
   term, and passed near-identical text before). It is now a deterministic code check.
5. The worked example passed E2 but did not show why RAG is needed. E2 now requires the
   "without retrieval" case.

## Memory and self-evolution
- Every run appends to `run_history.jsonl`.
- After a run, a reflect step turns each failed check into one general instruction, counted by how often
  it recurs. The top 5 are injected into the next generator prompt (capped to avoid prompt bloat).
- Rubric changes are made by a human after reading logs, not automatically, so the system
  cannot lower its own standards. A check failing in 3+ runs is flagged for review.

## Test strategy
- A known-good control lesson must fail no checks.
- Planted-flaw lessons (wrong fact, missing glossary, long sentences, missing sections, missing example)
  must each be caught by the intended check.
- Code checks are testable with no API calls (`run_code_tests.py`).

## Trade-offs and limitations
- The LLM judge can vary between runs. Mitigation so far: stricter rules and evidence checks.
  Next: run each check several times and take a majority vote.
- Code J1 covers only 7 listed terms. The earlier AI version covered any term but was unstable.
- F1 checks headings, not section content.
- The syllable counter is a simple estimate, and the readability formula is English-centric.
- Memory rules come from judge feedback, so a wrong judgment can pollute memory. Next: human
  approval before a rule enters memory.
- Free-tier rate limits make runs slow (retries and a fallback model are built in).

## Next steps
Majority-vote judging, a human-labelled calibration set, a Hindi/Malayalam version of the lesson,
and a check that the learner can answer the "Check yourself" questions from the lesson alone.