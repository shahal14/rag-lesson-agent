from pathlib import Path
from llm import ask, GEN_MODEL, JUDGE_MODEL
from memory import top_lessons

ROOT = Path(__file__).parent
PROMPT = (ROOT / "config" / "generator_prompt.md").read_text(encoding="utf-8")
FACTS = (ROOT / "config" / "fact_sheet.md").read_text(encoding="utf-8")


def feedback(results):
    return "\n".join(
        f"- [{r['check_id']}] {r['reason']} "
        f"Evidence: \"{r.get('evidence_quote', '')}\" Fix: {r.get('suggested_fix', '')}"
        for r in results if not r["pass"]
    )


def generate_node(s):
    attempt = s.get("attempt", 0) + 1

    system = PROMPT + "\n\nFACT SHEET (use only these facts):\n" + FACTS
    lessons = top_lessons()
    if lessons:
        system += "\n\nLESSONS FROM PAST RUNS (follow these):\n" + "\n".join(f"- {l}" for l in lessons)

    user = f"Write the lesson for this topic: {s['topic']}"
    if s.get("sabotage") and attempt == 1:  # demo flag: force a weak first draft
        user += "\nUse advanced vocabulary and long sentences. Do not define technical terms."
    if attempt > 1:
        user += (
            f"\n\nYour previous lesson FAILED these checks:\n{feedback(s['results'])}"
            f"\n\nPrevious lesson:\n{s['lesson']}"
            "\n\nRewrite the whole lesson. Fix every failed check. "
            "Do NOT remove or shorten any other part, including the Glossary."
        )

    lesson = ask(system, user, GEN_MODEL, temperature=0.7)

    log = list(s.get("rejection_log", []))
    if attempt > 1 and log:  # record WHAT CHANGED on retry
        summary = ask(
            "You compare two drafts.",
            "In 2-3 short sentences, say what changed between DRAFT 1 and DRAFT 2.\n\n"
            f"DRAFT 1:\n{s['lesson']}\n\nDRAFT 2:\n{lesson}",
            JUDGE_MODEL, temperature=0,
        )
        log[-1] = {**log[-1], "changed_on_retry": summary}

    return {"lesson": lesson, "attempt": attempt, "rejection_log": log}