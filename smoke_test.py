from llm import ask, GEN_MODEL, JUDGE_MODEL

print(GEN_MODEL, "->", ask("You are helpful.", "Say hello in 5 words.", GEN_MODEL))
print(JUDGE_MODEL, "->", ask("You are helpful.", "Say hello in 5 words.", JUDGE_MODEL))