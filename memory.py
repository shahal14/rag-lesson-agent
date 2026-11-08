import json
from pathlib import Path
from datetime import datetime
from llm import ask_json

MEM = Path(__file__).parent / "memory"
LESSONS = MEM / "lessons_learned.json"
HISTORY = MEM / "run_history.jsonl"


def _load():
    return json.loads(LESSONS.read_text(encoding="utf-8")) if LESSONS.exists() else {}


def top_lessons(n=5):
    """The most frequently repeated lessons, injected into the generator prompt."""
    items = sorted(_load().values(), key=lambda x: -x["count"])[:n]
    return [i["instruction"] for i in items]


def reflect_and_save(s):
    MEM.mkdir(exist_ok=True)
    log = s.get("rejection_log", [])

    if log:
        reasons = {r["check_id"]: r["reason"] for e in log for r in e["failed"]}
        new = ask_json("For each failed check, write ONE short GENERAL instruction (max 25 words) for a "
            "lesson-writing AI that would prevent this failure in ANY lesson. "
            "Do not mention specific words from this lesson. "
            "Return ONLY a JSON object: {\"CHECK_ID\": \"instruction\"}.",
            json.dumps(reasons),
        )
        if isinstance(new, dict):
            data = _load()
            for cid, instruction in new.items():
                count = data.get(cid, {"count": 0})["count"] + 1
                data[cid] = {"instruction": str(instruction), "count": count}
                if count >= 3:
                    print(f"NOTE: check {cid} has failed in {count} runs -> review the rubric or prompt.")
            LESSONS.write_text(json.dumps(data, indent=2), encoding="utf-8")

    with HISTORY.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "time": datetime.now().isoformat(timespec="seconds"),
            "topic": s["topic"],
            "attempts": s["attempt"],
            "status": s["status"],
            "failed_checks": sorted({r["check_id"] for e in log for r in e["failed"]}),
        }) + "\n")