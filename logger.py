from pathlib import Path

ROOT = Path(__file__).parent


def write_outputs(s):
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "final_lesson.md").write_text(s["lesson"], encoding="utf-8")

    lines = [f"# Rejection log\n\nFinal status: **{s['status']}** after {s['attempt']} attempt(s)\n"]
    if not s["rejection_log"]:
        lines.append("No rejections: the first draft passed every check.")
    for e in s["rejection_log"]:
        lines.append(f"\n## Attempt {e['attempt']} - REJECTED")
        for r in e["failed"]:
            lines.append(f"- **{r['check_id']}** failed: {r['reason']}")
            if r.get("evidence_quote"):
                lines.append(f"  - Evidence: \"{r['evidence_quote']}\"")
            lines.append(f"  - Fix requested: {r.get('suggested_fix', '')}")
        lines.append(f"- **What changed on retry:** {e.get('changed_on_retry') or 'n/a (no retry left)'}")

    (ROOT / "logs" / "rejection_log.md").write_text("\n".join(lines), encoding="utf-8")
    from datetime import datetime
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    (ROOT / "logs" / f"rejection_log_{stamp}_{s['status']}.md").write_text("\n".join(lines), encoding="utf-8")
    (ROOT / "outputs" / f"lesson_{stamp}_{s['status']}.md").write_text(s["lesson"], encoding="utf-8")