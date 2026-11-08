# Rubric changelog

Every change below came from a real failure seen in a run, a log, or a test.

## v1 -> v2
- Observed: a retry fixed J1 but dropped two glossary terms. J2 only counted entries, so it passed.
- Observed: an average sentence length hid one very long sentence.
- Observed: a memory rule named one specific word, so it would not help other lessons.
- Change: J2 now requires 7 specific glossary terms.
- Change: L1 now also caps the longest sentence at 25 words.
- Change: the judge's evidence quote is checked against the lesson text in code.
- Change: memory rules must be general, and the retry prompt says not to remove other parts of the lesson.

## v2 -> v3
- Observed: a run ended NEEDS_HUMAN_REVIEW. L3 failed 3 times because the judge criticised the exam analogy, but L3 is meant to check English wording. E1 (needs an analogy) and L3 conflicted, so the generator could not fix it. The same analogy had passed L3 earlier.
- Change: L3 now says "judge wording only; analogies are judged elsewhere".
- Change: the judge prompt treats "must be present" checks (fail if missing) differently from "must be absent" checks (fail only with a quotable violation).
- Change: memory cleared, because a failed run had saved a rule from a bad judgment.

## v3 -> v4
- Observed: J1 and F2 failed with quoted evidence. Terms were used before they were defined.
- Root cause: the generator wrote "use the term, then define it".
- Change: generator prompt bans technical terms in the hook, requires "define first, then use" with a correct and a wrong example, and fixes the definition order (LLM, prompt, retrieval).

## v4 -> v5
- Observed: the worked example passed E2 but did not show why RAG is needed (no "without retrieval" case).
- Change: E2 now requires the without-retrieval answer. The generator prompt specifies a five-part example. Conflicting old prompt lines were removed.

## v5 -> v6
- Observed: the AI-judged J1 cited a sentence that did not contain the term, and had passed near-identical text before. Retrying it used up free-tier quota.
- Change: J1 is now a deterministic code check on 7 listed terms. Added check_only.py to test code checks with no API calls.
- Trade-off: J1 covers only the listed terms; the AI version covered any term but was unstable.

## v6 -> v7
- Observed: code J1 flagged three terms that were defined in the sentence right after their first use.
- Decision: max_gap = <0 or 1, as in rubric.yaml> because <your reason>.

## v7 -> v8
- Observed: bad_language.md has an average sentence length of 11.4 (under the limit) but a 41-word sentence. Only the longest-sentence cap caught it.
- Observed: bad files built from an older lesson all failed J2, so the baseline was not clean.
- Change: bad files are rebuilt from the current passing lesson, and every test run includes a control.
- Known limitation: code J1 does not catch jargon outside its 7 listed terms.

## v8 -> v9
- Observed (sabotage run): code J1 rejected "A small piece of text is called a chunk." because its definition pattern did not recognise "is called". A false positive in a deterministic check.
- Observed (normal run): AI-judged F2 claimed "LLM" appeared in the hook, quoting a sentence that contained no technical term. The evidence check proves a quote exists, not that it supports the claim.
- Both runs ended NEEDS_HUMAN_REVIEW on false alarms and used up quota.
- Change: J1 accepts "called / known as / named". F2 is now a deterministic hook check. Tests now include good text that must PASS, not only bad text that must FAIL.
- Change: llm.py skips a model that failed completely for 10 minutes. The logger keeps a timestamped copy of every run.

## v9 -> v10
- Provider switched from Gemini to Groq after an API key problem. The planned judge model (llama-3.1-8b-instant) had been retired, so the judge is now gpt-oss-20b and the generator is gpt-oss-120b.
- Re-ran the tests: the control fails none of the 15 checks. bad_factual.md fails A1 and A3 (the Gemini judge failed only A1).
- Observation: changing the judge model changes verdicts, so re-run the planted-flaw tests whenever the judge changes.
- Note: generator and judge are normally different models, and Groq's limits apply per model. The fallback in llm.py can make them the same model temporarily if one is unavailable.
- Change: output limit lowered to 4000 tokens (Groq's per-minute cap is small), and .env is always trusted over leftover terminal settings (load_dotenv(override=True)).