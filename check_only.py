import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from evaluator import RUBRIC, CODE_CHECKS

path = sys.argv[1] if len(sys.argv) > 1 else "outputs/final_lesson.md"
lesson = Path(path).read_text(encoding="utf-8")
for c in RUBRIC["checks"]:
    if c["type"] == "code":
        r = CODE_CHECKS[c["id"]](lesson, c)
        print("PASS" if r["pass"] else "FAIL", r["check_id"], r["reason"])