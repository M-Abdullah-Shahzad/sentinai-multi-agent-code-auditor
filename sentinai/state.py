from typing import TypedDict, List, Dict, Any

class SentinAIState(TypedDict):
    source_files: List[Dict[str, str]]
    parser_data: str
    ner_entities: str
    security_findings: str
    bug_findings: str
    rag_references: str
    documentation: str
    health_score: str
    final_report: str
    final_json: str
    errors: List[str]
