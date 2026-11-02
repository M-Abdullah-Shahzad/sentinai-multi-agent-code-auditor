from typing import Any, TypedDict


class SentinAIState(TypedDict, total=False):
    source_files: list[dict[str, str]]
    parser_data: list[dict[str, Any]]
    rag_references: list[dict[str, str]]
    security_findings: list[dict[str, Any]]
    bug_findings: list[dict[str, Any]]
    documentation: list[dict[str, Any]]
    health_score: int
    final_report: str
    final_json: str
    errors: list[str]
