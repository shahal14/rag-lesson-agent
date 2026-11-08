import sys
sys.stdout.reconfigure(encoding="utf-8")

import argparse
from pathlib import Path
from graph import build_graph
from evaluator import evaluate_lesson


def show(results):
    for r in results:
        print(f"{'PASS' if r['pass'] else 'FAIL'}  {r['check_id']}  {r['reason']}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--topic", default="Introduction to LLM")
    p.add_argument("--evaluate-only", help="path to a lesson .md file to judge")
    p.add_argument("--sabotage", action="store_true", help="force a weak first draft (demo)")
    a = p.parse_args()

    if a.evaluate_only:
        show(evaluate_lesson(Path(a.evaluate_only).read_text(encoding="utf-8")))
    else:
        final = build_graph().invoke({
            "topic": a.topic,
            "attempt": 0,
            "rejection_log": [],
            "sabotage": a.sabotage,
        })
        show(final["results"])
        print(f"\n{final['status']} after {final['attempt']} attempt(s)")
        print("Lesson: outputs/final_lesson.md | Log: logs/rejection_log.md")