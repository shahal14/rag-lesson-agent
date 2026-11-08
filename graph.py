from langgraph.graph import StateGraph, END
from state import State
from generator import generate_node
from evaluator import evaluate_lesson
from memory import reflect_and_save
from logger import write_outputs

MAX_ATTEMPTS = 3  # 1 first try + 2 retries -> the loop always ends


def evaluate_node(s):
    results = evaluate_lesson(s["lesson"])
    failed = [r for r in results if not r["pass"]]
    log = list(s.get("rejection_log", []))
    if failed:
        log.append({"attempt": s["attempt"], "failed": failed, "changed_on_retry": None})
    return {"results": results, "rejection_log": log}


def route(s):
    if all(r["pass"] for r in s["results"]):
        return "finalize"
    return "flag" if s["attempt"] >= MAX_ATTEMPTS else "retry"


def finalize_node(s):
    return {"status": "PASSED"}


def flag_node(s):
    return {"status": "NEEDS_HUMAN_REVIEW"}


def reflect_node(s):
    write_outputs(s)
    reflect_and_save(s)
    return {"status": s["status"]}


def build_graph():
    g = StateGraph(State)
    g.add_node("generate", generate_node)
    g.add_node("evaluate", evaluate_node)
    g.add_node("finalize", finalize_node)
    g.add_node("flag", flag_node)
    g.add_node("reflect", reflect_node)

    g.set_entry_point("generate")
    g.add_edge("generate", "evaluate")
    g.add_conditional_edges(
        "evaluate", route,
        {"finalize": "finalize", "flag": "flag", "retry": "generate"},
    )
    g.add_edge("finalize", "reflect")
    g.add_edge("flag", "reflect")
    g.add_edge("reflect", END)
    return g.compile()