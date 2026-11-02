from sentinai.agents import (
    _health_score,
    _parse_json_response,
    static_parser_node,
)


def test_parse_json_response_from_markdown_fence():
    result = _parse_json_response('Result:\n```json\n{"findings": []}\n```')
    assert result == {"findings": []}


def test_parse_json_response_rejects_invalid_content():
    assert _parse_json_response("not json") == {}


def test_health_score_applies_documented_severity_penalties():
    score = _health_score(
        [{"severity": "High"}, {"severity": "Medium"}],
        [{"severity": "Low"}],
    )
    assert score == 80


def test_static_parser_extracts_python_structure():
    result = static_parser_node({
        "source_files": [{
            "name": "sample.py",
            "language": "python",
            "content": "class Example:\n    def run(self):\n        return 1\n",
        }]
    })
    summary = result["parser_data"][0]
    assert summary["file"] == "sample.py"
    assert "Example" in summary["analysis"]["classes"]
    assert "run" in summary["analysis"]["functions"]
    assert "ast" not in summary["analysis"]
