import json
from .agents import sentinai_graph, get_llm
from .parsers import parse_uploaded_file
from .rag import ReferenceRetriever


class SentinAICore:
    def __init__(self):
        self.retriever = ReferenceRetriever()

    def validate(self):
        # We can do a quick check to see if the LLM provider can be initialized
        try:
            get_llm()
            return None
        except Exception as e:
            raise RuntimeError(f"LLM initialization failed: {e}")

    def analyze(self, source_files):
        # We can still parse locally, though the Master Prompt asks the LLM to act as a Parser Agent too.
        # We'll pass the files as requested.
        initial_state = {
            "source_files": source_files,
            "errors": []
        }
        
        try:
            # Run the LangGraph workflow
            result_state = sentinai_graph.invoke(initial_state)
            
            if result_state.get("errors"):
                raise RuntimeError("Graph execution errors: " + ", ".join(result_state["errors"]))
                
            # Parse the JSON if it exists
            final_json = {}
            if result_state.get("final_json"):
                final_json = json.loads(result_state["final_json"])
                
            return {
                "final_report": result_state.get("final_report", ""),
                "final_json": final_json,
                "files": source_files,
                "llm_fallback_reason": None,
            }
        except Exception as exc:
            raise RuntimeError(f"Analysis failed: {str(exc)}")
