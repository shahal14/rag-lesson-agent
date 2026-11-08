# Rejection log

Final status: **PASSED** after 3 attempt(s)


## Attempt 1 - REJECTED
- **L1** failed: Average sentence length is 10.8 words (limit 15); longest sentence has 32 words (limit 25).
  - Evidence: "(3) What the LLM would answer WITHOUT retrieval: "I am not sure about your office furniture schedule." (It has never seen the document, so it guesses or says it does not know)."
  - Fix requested: Split long sentences into two or three short ones.
- **What changed on retry:** Between DRAFT 1 and DRAFT 2, the only change is in the "A worked example" section under point (3). The simulated LLM response without retrieval was rewritten to remove the quoted example answer ("I am not sure about your office furniture schedule.") and replaced with a direct descriptive explanation of the model's behavior.

## Attempt 2 - REJECTED
- **L1** failed: Average sentence length is 10.5 words (limit 15); longest sentence has 27 words (limit 25).
  - Evidence: "RAG is Retrieval-Augmented Generation, which finds relevant information in external documents at question time, adds it to the prompt, and the LLM writes the answer using it."
  - Fix requested: Split long sentences into two or three short ones.
- **What changed on retry:** Draft 2 breaks down several long, compound sentences into shorter, simpler sentences to improve readability. It also removes a duplicate definition of "hallucination" in the "Why does RAG matter?" section.