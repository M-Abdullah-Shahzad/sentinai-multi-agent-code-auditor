import json

from .agents import get_llm, sentinai_graph
from .rag import ReferenceRetriever


class SentinAICore:
    def __init__(self):
        self.retriever = ReferenceRetriever()

    def validate(self):
        try:
            get_llm()
            return None
        except Exception as exc:
            raise RuntimeError(f"LLM initialization failed: {exc}") from exc

    def analyze(self, source_files):
        if not source_files:
            raise RuntimeError("Upload at least one supported Python or JavaScript file.")

        query = "\n\n".join(
            f"{item.get('name', '')}\n{str(item.get('content', ''))[:1200]}"
            for item in source_files
        )[:8000]

        retrieval_warning = None
        try:
            references = self.retriever.retrieve(query, k=4)
        except Exception as exc:
            references = []
            retrieval_warning = (
                "Local reference retrieval was unavailable; specialist agents continued "
                f"without retrieved references ({type(exc).__name__})."
            )

        try:
            result_state = sentinai_graph.invoke({
                "source_files": source_files,
                "rag_references": references,
                "errors": [],
            })
            final_json = json.loads(result_state.get("final_json", "{}"))
            return {
                "final_report": result_state.get("final_report", ""),
                "final_json": final_json,
                "files": source_files,
                "llm_fallback_reason": retrieval_warning,
            }
        except Exception as exc:
            raise RuntimeError(f"Analysis failed: {exc}") from exc
