import os, json, re, time
from openai import OpenAI, RateLimitError, APIConnectionError, APIStatusError
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("PROVIDER_API_KEY")
if not API_KEY:
    raise SystemExit("PROVIDER_API_KEY is empty. Open .env, paste your real key, and press Ctrl+S.")

client = OpenAI(api_key=API_KEY, base_url=os.getenv("BASE_URL"), timeout=90, max_retries=0)
GEN_MODEL = os.getenv("GEN_MODEL")
JUDGE_MODEL = os.getenv("JUDGE_MODEL") or GEN_MODEL

COOLDOWN = 600          # seconds to avoid a model after it failed completely
_blocked_until = {}     # model -> time when we may try it again


def _is_daily(err):
    t = str(err).lower()
    return "perday" in t or "per day" in t or "daily" in t


def ask(system, user, model, temperature=0.7, max_tokens=4000):
    """Call the model. Retries on rate limits and busy servers, then uses the other model."""
    backup = JUDGE_MODEL if model == GEN_MODEL else GEN_MODEL
    models = [model] + ([backup] if backup and backup != model else [])
    live = [m for m in models if _blocked_until.get(m, 0) <= time.time()] or models

    for m in live:
        for attempt in range(5):
            try:
                r = client.chat.completions.create(
                    model=m, temperature=temperature, max_tokens=max_tokens,
                    messages=[{"role": "system", "content": system},
                              {"role": "user", "content": user}],
                )
                text = r.choices[0].message.content or ""
                if text.strip():
                    return text
            except RateLimitError as e:
                if _is_daily(e):
                    print(f"[{m}] daily quota used up, switching model.")
                    break
                wait = 15 * (attempt + 1)
                print(f"[{m}] Rate limit reached, waiting {wait}s...")
                time.sleep(wait)
            except APIStatusError as e:
                if e.status_code >= 500:          # server busy: try again shortly
                    wait = 10 * (attempt + 1)
                    print(f"[{m}] Server busy (error {e.status_code}), waiting {wait}s...")
                    time.sleep(wait)
                else:                              # 400/401/404: our mistake, stop clearly
                    raise
            except APIConnectionError as e:
                print(f"[{m}] Connection problem: {e}")
                time.sleep(5)
        _blocked_until[m] = time.time() + COOLDOWN
        print(f"[{m}] keeps failing, using the other model for the next 10 minutes.")

    raise RuntimeError("LLM call failed after retries (check internet, key, model names, or daily quota)")


def ask_json(system, user, model=None):
    """Ask the judge for JSON. Retries once if the JSON is broken."""
    model = model or JUDGE_MODEL
    for _ in range(2):
        text = ask(system, user, model, temperature=0)
        text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            continue
    raise ValueError("Judge did not return valid JSON")