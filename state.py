from typing import TypedDict, List


class State(TypedDict, total=False):
    topic: str
    lesson: str
    attempt: int
    results: List[dict]
    rejection_log: List[dict]
    status: str
    sabotage: bool