from evaluator import check_J1, check_F2, RUBRIC

cfg = {c["id"]: c for c in RUBRIC["checks"]}

good = ("Imagine a helper who forgets new facts.\n\n## What is RAG?\n\n"
        "A confident answer that is wrong is called a hallucination. "
        "A small piece of text is called a chunk. A storage system is called a vector database.\n\n"
        "## Glossary\n- x\n")
bad = ("The LLM forgets new facts.\n\n## What is RAG?\n\n"
       "The model can hallucinate. It makes many mistakes.\n\n## Glossary\n- x\n")

print("J1 good ->", check_J1(good, cfg["J1"])["pass"], "(expect True)")
print("J1 bad  ->", check_J1(bad, cfg["J1"])["pass"], "(expect False)")
print("F2 good ->", check_F2(good, cfg["F2"])["pass"], "(expect True)")
print("F2 bad  ->", check_F2(bad, cfg["F2"])["pass"], "(expect False)")