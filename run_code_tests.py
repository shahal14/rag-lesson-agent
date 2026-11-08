import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
from evaluator import RUBRIC, CODE_CHECKS


def failed(path):
    text = Path(path).read_text(encoding="utf-8")
    return {c["id"] for c in RUBRIC["checks"]
            if c["type"] == "code" and not CODE_CHECKS[c["id"]](text, c)["pass"]}


# flaw -> code check that should catch it (bad_factual needs the AI judge, so it is not here)
EXPECTED = {
    "bad_jargon.md":     {"J2"},
    "bad_language.md":   {"L1"},
    "bad_structure.md":  {"F1"},
    "bad_no_example.md": {"F1"},
}

control = failed("outputs/final_lesson.md")
print(f"CONTROL (current lesson) failed code checks: {sorted(control)} "
      f"-> {'clean baseline' if not control else 'NOT CLEAN, fix first'}\n")

caught = 0
for name, expected in EXPECTED.items():
    f = failed(Path("tests/bad_lessons") / name)
    ok = expected <= f
    caught += ok
    print(f"{'CAUGHT' if ok else 'MISSED'}  {name:20} expected {sorted(expected)} | failed {sorted(f)} "
          f"| collateral {sorted(f - expected - control)}")

print(f"\nCode checks caught {caught}/{len(EXPECTED)} planted flaws (no API calls used)")
print("bad_factual.md needs the AI judge: run run_tests.py when quota is available")