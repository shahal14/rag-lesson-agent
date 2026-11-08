import re
import yaml
from pathlib import Path
from llm import ask_json

ROOT = Path(__file__).parent
RUBRIC = yaml.safe_load((ROOT / "config" / "rubric.yaml").read_text(encoding="utf-8"))
FACTS = (ROOT / "config" / "fact_sheet.md").read_text(encoding="utf-8")

JUDGE_SYSTEM = """You are a strict but fair content reviewer. You judge a beginner lesson against checks.
Rules:
- Judge ONLY the exact wording of each check. Do not fail a check for a problem that belongs to a different check.
- Each check is strictly PASS or FAIL. No partial credit.
- If a check asks for something to be PRESENT (explained, covered, included, stated), FAIL when it is missing or unclear.
- If a check asks for something to be ABSENT (no contradictions, no invented facts, no idioms, nothing used before it is introduced), FAIL only if you can quote the exact words that break it. If you cannot quote a specific violation, PASS.
- For every check give an exact quote copied from the lesson as evidence (use "" only if required content is missing entirely).
- Give a short reason and a concrete suggested_fix.
Return ONLY a JSON array, no other text:
[{"check_id": "A1", "pass": true, "evidence_quote": "...", "reason": "...", "suggested_fix": "..."}]"""


def res(cid, ok, reason, fix="", quote=""):
    return {"check_id": cid, "pass": ok, "evidence_quote": quote,
            "reason": reason, "suggested_fix": fix}


def plain(md):
    """Remove markdown so readability checks measure real sentences."""
    t = re.sub(r"^#+\s.*$", "", md, flags=re.M)                      # headings
    t = re.sub(r"^\s*(?:[-*\u2022]|\d+[.)])\s+", "", t, flags=re.M)  # list markers
    t = re.sub(r"[*_`>#|]", "", t)                                   # leftover symbols
    lines = [l.strip() for l in t.splitlines() if l.strip()]
    lines = [l if l[-1] in ".!?" else l + "." for l in lines]        # end every line
    return "\n".join(lines)


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[*_`#>]", "", t)).strip().lower()


def count_syllables(word):
    """Simple syllable estimate: count vowel groups, adjust for a silent final 'e'."""
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    n = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and not word.endswith("le") and n > 1:
        n -= 1
    return max(n, 1)


def fk_grade(text):
    """Flesch-Kincaid grade level, computed directly (no external data needed)."""
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    words = re.findall(r"[A-Za-z']+", text)
    if not sents or not words:
        return 0.0
    syllables = sum(count_syllables(w) for w in words)
    return 0.39 * len(words) / len(sents) + 11.8 * syllables / len(words) - 15.59


# ---------------- code checks (deterministic) ----------------
def check_L1(lesson, cfg):
    sents = [s for s in re.split(r"(?<=[.!?])\s+", plain(lesson)) if s.strip()]
    lens = [len(s.split()) for s in sents]
    avg = sum(lens) / max(len(lens), 1)
    longest_len = max(lens) if lens else 0
    longest = max(sents, key=lambda s: len(s.split())) if sents else ""
    ok = avg <= cfg["max_avg_words"] and longest_len <= cfg["max_sentence_words"]
    return res("L1", ok,
               f"Average sentence length is {avg:.1f} words (limit {cfg['max_avg_words']}); "
               f"longest sentence has {longest_len} words (limit {cfg['max_sentence_words']}).",
               "Split long sentences into two or three short ones.",
               longest.strip()[:200])


def check_L2(lesson, cfg):
    grade = fk_grade(plain(lesson))
    ok = grade <= cfg["max_grade"]
    return res("L2", ok,
               f"Readability grade is {grade:.1f} (limit {cfg['max_grade']}).",
               "Use shorter words and shorter sentences.")


def check_J1(lesson, cfg):
    """Each key term must be defined at or before the sentence where it is first used."""
    body = re.split(r"^##\s*Glossary", lesson, flags=re.M)[0]
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", plain(body)) if s.strip()]
    gap = cfg.get("max_gap", 0)   # 0 = definition must come first; 1 = may follow in the next sentence
    problems = []
    for term, stem in cfg["terms"].items():
        use = re.compile(rf"\b{stem}", re.I)
        defn = re.compile(
            rf"\b{stem}\w*\b[^.]{{0,60}}?\b(is|are|means|stands for|refers to)\b"
            rf"|\b(called|known as|named)\s+(?:a |an |the )?{stem}", re.I)
        u = next((i for i, s in enumerate(sents) if use.search(s)), None)
        if u is None:
            continue  # term never used in the body, nothing to define
        d = next((i for i, s in enumerate(sents) if defn.search(s)), None)
        if d is None or d > u + gap:
            problems.append((term, sents[u]))
    if not problems:
        return res("J1", True, "Every key term is defined before (or where) it is first used.")
    shown = "; ".join(f"'{t}' first used in: \"{s[:80]}\"" for t, s in problems[:3])
    return res("J1", False,
               f"{len(problems)} term(s) are used before they are defined: {shown}",
               "Write the definition first (for example 'A chunk is a small piece of text.'), then use the term.",
               problems[0][1][:200])

def check_J2(lesson, cfg):
    m = re.search(r"^##\s*Glossary[^\n]*\n(.*?)(?=^##\s|\Z)", lesson, re.M | re.S)
    section = m.group(1) if m else ""
    n = len([l for l in section.splitlines() if l.strip()])
    missing = [t for t in cfg.get("required_terms", []) if t.lower() not in section.lower()]
    reason = f"Glossary has {n} entries (need {cfg['min_entries']})."
    if missing:
        reason += f" Missing required terms: {missing}."
    return res("J2", n >= cfg["min_entries"] and not missing, reason,
               "Add every required term to the Glossary, one per line.")


def check_F1(lesson, cfg):
    heads = [h.lower() for h in re.findall(r"^##\s+(.*)$", lesson, re.M)]
    order = ["what", "why", "how", "example", "recap", "glossary"]
    pos, missing = 0, []
    for key in order:
        idx = next((i for i in range(pos, len(heads)) if key in heads[i]), None)
        if idx is None:
            missing.append(key)
        else:
            pos = idx + 1
    return res("F1", not missing,
               "Section order is correct." if not missing
               else f"Missing or out-of-order sections: {missing}",
               "Use the required headings in the required order.")

def check_F2(lesson, cfg):
    """The hook (text before the first heading) must not use technical terms."""
    hook = re.split(r"^##\s", lesson, maxsplit=1, flags=re.M)[0]
    found = [t for t in cfg["banned_terms"] if re.search(rf"\b{re.escape(t)}", hook, re.I)]
    return res("F2", not found,
               "The hook uses no technical terms." if not found
               else f"The hook uses technical terms before they are taught: {found}",
               "Rewrite the hook in everyday words only.",
               hook.strip()[:200])
CODE_CHECKS = {"L1": check_L1, "L2": check_L2, "J1": check_J1, "J2": check_J2,
               "F1": check_F1, "F2": check_F2}
# ---------------- main entry ----------------
def evaluate_lesson(lesson):
    results, by_dim = [], {}
    for c in RUBRIC["checks"]:
        if c["type"] == "code":
            results.append(CODE_CHECKS[c["id"]](lesson, c))
        else:
            by_dim.setdefault(c["dimension"], []).append(c)

    for dim, checks in by_dim.items():
        listing = "\n".join(f"- {c['id']}: {c['question']}" for c in checks)
        user = f"FACT SHEET:\n{FACTS}\n\nLESSON:\n{lesson}\n\nCHECKS:\n{listing}"
        got = {r["check_id"]: r for r in ask_json(JUDGE_SYSTEM, user)}
        for c in checks:
            r = got.get(c["id"]) or res(c["id"], False, "Judge gave no verdict.")
            q = r.get("evidence_quote") or ""
            if q and norm(q) not in norm(lesson):
                r["evidence_quote"] = q + "  [UNVERIFIED: not found in lesson]"
            results.append(r)

    order = [c["id"] for c in RUBRIC["checks"]]
    return sorted(results, key=lambda r: order.index(r["check_id"]))