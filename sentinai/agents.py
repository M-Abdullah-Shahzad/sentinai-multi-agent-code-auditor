import json
import re
from typing import Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from .state import SentinAIState
from .prompts import MASTER_SYSTEM_PROMPT
from .config import SENTINAI_LLM_PROVIDER, GROQ_API_KEY, OPENAI_API_KEY, DEFAULT_MODEL, OPENAI_DEFAULT_MODEL


def get_llm():
    if SENTINAI_LLM_PROVIDER == "groq":
        return ChatGroq(model=DEFAULT_MODEL, api_key=GROQ_API_KEY, temperature=0.2)
    else:
        return ChatOpenAI(model=OPENAI_DEFAULT_MODEL, api_key=OPENAI_API_KEY, temperature=0.2)


def analyzer_node(state: SentinAIState) -> Dict[str, Any]:
    llm = get_llm()
    
    # Prepare the source files context
    source_context = ""
    for file in state.get("source_files", []):
        source_context += f"\n--- File: {file['name']} ---\n{file['content']}\n"
        
    messages = [
        SystemMessage(content=MASTER_SYSTEM_PROMPT),
        HumanMessage(content=f"Please analyze the following source code and provide both the Markdown report and JSON output as requested.\n\n"
                             f"For the JSON output, please strictly use the following keys so our UI can render it properly:\n"
                             f"- \"health_score\": (integer 0-100)\n"
                             f"- \"security_findings\": list of objects with keys title, description, severity, file, reference\n"
                             f"- \"bug_findings\": list of objects with keys title, description, severity, file, recommendation\n"
                             f"- \"documentation\": list of objects with keys file, type, content\n"
                             f"- \"references\": list of objects with keys title, snippet\n\n"
                             f"SOURCE CODE:\n{source_context}")
    ]
    
    try:
        response = llm.invoke(messages)
        content = response.content
        
        # Parse JSON and Markdown from the response
        # We expect the LLM to provide a JSON block and a Markdown report.
        json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
        if json_match:
            try:
                parsed_json = json.loads(json_match.group(1))
                final_json = json.dumps(parsed_json)
            except json.JSONDecodeError:
                final_json = "{}"
        else:
            final_json = "{}"
            
        return {
            "final_report": content,
            "final_json": final_json,
        }
    except Exception as e:
        return {"errors": [str(e)]}

# Build the LangGraph workflow
workflow = StateGraph(SentinAIState)
workflow.add_node("analyzer", analyzer_node)
workflow.add_edge(START, "analyzer")
workflow.add_edge("analyzer", END)

# Compile the graph
sentinai_graph = workflow.compile()
