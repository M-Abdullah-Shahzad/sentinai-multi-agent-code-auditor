import ast
import json
import os
import subprocess
from typing import Any, Dict


def parse_python_code(source: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(source)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        return {"functions": functions, "classes": classes, "ast": tree}
    except SyntaxError as exc:
        return {"error": str(exc)}


def parse_javascript_code(source: str) -> Dict[str, Any]:
    script = os.path.join(os.path.dirname(__file__), "js_parser.js")
    try:
        process = subprocess.run(["node", script], input=source, capture_output=True, text=True, check=True)
        return json.loads(process.stdout)
    except FileNotFoundError:
        return {"error": "Node.js not installed. Install Node.js and npm to use JavaScript parsing."}
    except subprocess.CalledProcessError as exc:
        return {"error": exc.stderr or exc.stdout}


def parse_uploaded_file(file_data: Dict[str, str]) -> Dict[str, Any]:
    if file_data["language"] == "python":
        return parse_python_code(file_data["content"])
    return parse_javascript_code(file_data["content"])
