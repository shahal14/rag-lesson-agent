import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from evaluator import evaluate_lesson

for name in ["outputs/final_lesson.md", "tests/bad_lessons/bad_factual.md"]:
    results = evaluate_lesson(Path(name).read_text(encoding="utf-8"))
    print(name, "-> failed:", sorted(r["check_id"] for r in results if not r["pass"]))
    for r in results:
        if not r["pass"] and r["check_id"] in ("A1", "A3"):
            print("   ", r["check_id"], r["reason"])