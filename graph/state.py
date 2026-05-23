from typing import TypedDict, List


class ResearchState(TypedDict):
    query: str
    subquestions: List[str]
    search_results: List[str]
    critique: str
    final_report: str