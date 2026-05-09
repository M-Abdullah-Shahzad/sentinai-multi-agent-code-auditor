from typing import Dict, List


def build_summary_report(analysis):
    report = {
        "summary": {
            "health_score": analysis["health_score"],
            "security_issues": len(analysis["security_findings"]),
            "bug_issues": len(analysis["bug_findings"]),
            "documentation_items": len(analysis["documentation"]),
        },
        "security": analysis["security_findings"],
        "bugs": analysis["bug_findings"],
        "documentation": analysis["documentation"],
        "references": analysis["references"],
    }
    return report
