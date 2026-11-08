import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
from evaluator import evaluate_lesson

# bad file -> checks that SHOULD fail because of the planted flaw
EXPECTED = {
    "bad_factual.md":    {"A1"},
    "bad_jargon.md":     {"J2"},
    "bad_language.md":   {"L1"},
    "bad_structure.md":  {"F1"},
    "bad_no_example.md": {"E2", "F1"},
}


def failed_ids(path):
    text = Path(path).read_text(encoding="utf-8")
    return {r["check_id"] for r in evaluate_lesson(text) if not r["pass"]}


control = failed_ids("outputs/final_lesson.md")
print(f"CONTROL (known-good lesson) failed: {sorted(control)} "
      f"-> {'clean baseline' if not control else 'BASELINE NOT CLEAN, fix before trusting results'}\n")

caught = 0
for name, expected in EXPECTED.items():
    failed = failed_ids(Path("tests/bad_lessons") / name)
    ok = expected <= failed
    extra = sorted(failed - expected - control)
    caught += ok
    print(f"{'CAUGHT' if ok else 'MISSED'}  {name:20} expected {sorted(expected)} | "
          f"failed {sorted(failed)} | collateral {extra}")

print(f"\nEvaluator caught {caught}/{len(EXPECTED)} planted flaws")