## v8 -> v9
- Observed (sabotage run): code J1 rejected "A small piece of text is called a chunk." because
  its definition pattern did not recognise "is called". A false positive in a deterministic check.
- Observed (normal run): AI-judged F2 claimed "LLM" appeared in the hook, quoting a sentence that
  contained no technical term. The evidence check only proves a quote exists, not that it supports the claim.
- Both runs ended NEEDS_HUMAN_REVIEW on false alarms and consumed quota.
- Change: J1 accepts "called / known as / named"; F2 is now a deterministic hook check;
  tests now include good lessons that must PASS, not only bad lessons that must FAIL.
- Change: llm.py skips a model that failed completely for 10 minutes; logger keeps timestamped runs.