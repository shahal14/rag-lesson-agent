import re
from pathlib import Path

src = Path("outputs/final_lesson.md").read_text(encoding="utf-8")
out = Path("tests/bad_lessons")
out.mkdir(parents=True, exist_ok=True)


def remove_section(text, keyword):
    pattern = rf"^##\s+[^\n]*{keyword}[^\n]*\n.*?(?=^##\s|\Z)"
    return re.sub(pattern, "", text, flags=re.M | re.S | re.I)


def must_change(new, old, name):
    if new == old:
        raise SystemExit(f"Could not create {name}: the lesson headings differ from expected.")
    return new


# 1. Wrong fact: says RAG retrains the model
bad = must_change(
    src.replace("## Why does RAG matter?",
                "RAG retrains the model on your documents every time you ask a question.\n\n## Why does RAG matter?", 1),
    src, "bad_factual.md")
(out / "bad_factual.md").write_text(bad, encoding="utf-8")

# 2. Jargon: remove the glossary and add undefined technical terms
bad = remove_section(src, "Glossary")
bad = bad.replace("## Quick recap",
                  "The retriever uses cosine similarity over dense vectors with an ANN index and a reranker.\n\n## Quick recap", 1)
(out / "bad_jargon.md").write_text(must_change(bad, src, "bad_jargon.md"), encoding="utf-8")

# 3. Language: merge sentences into very long ones and add idioms
lines = []
for line in src.splitlines():
    if line.lstrip().startswith(("#", "-", "*")) or re.match(r"\s*\d+[.)]", line):
        lines.append(line)
    else:
        lines.append(re.sub(r"\.\s+", ", and then ", line))
bad = "\n".join(lines).replace(
    "## Quick recap",
    "In a nutshell, RAG is a piece of cake once you get the hang of it.\n\n## Quick recap", 1)
(out / "bad_language.md").write_text(must_change(bad, src, "bad_language.md"), encoding="utf-8")

# 4. Structure: remove the "why" section
bad = remove_section(src, "Why does RAG matter")
(out / "bad_structure.md").write_text(must_change(bad, src, "bad_structure.md"), encoding="utf-8")

# 5. No example: remove the worked example section
bad = remove_section(src, "worked example")
(out / "bad_no_example.md").write_text(must_change(bad, src, "bad_no_example.md"), encoding="utf-8")

print("Created 5 bad lessons in tests/bad_lessons/")