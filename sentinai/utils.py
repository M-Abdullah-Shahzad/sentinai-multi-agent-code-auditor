import re

SECRET_PATTERNS = [
    r'(?i)api[_-]?key\s*=\s*["\']?([A-Za-z0-9-_]{20,})["\']?',
    r'(?i)secret[_-]?key\s*=\s*["\']?([A-Za-z0-9-_]{20,})["\']?',
    r'(?i)password\s*=\s*["\'](.+?)["\']',
    r'(?i)authorization\s*[:=]\s*["\']?Bearer\s+([A-Za-z0-9-_.]+)["\']?',
]

SQL_KEYWORDS = ["SELECT", "INSERT", "UPDATE", "DELETE", "EXEC", "DROP", "UNION", "WHERE"]

XSS_PATTERNS = [
    r"document\.write\(",
    r"innerHTML\s*=",
    r"outerHTML\s*=",
    r"eval\(",
    r"setTimeout\(.*document\.",
]


def find_secret_patterns(code: str):
    findings = []
    for pattern in SECRET_PATTERNS:
        for match in re.finditer(pattern, code):
            findings.append(match.group(0))
    return findings


def is_potential_sql_injection(code: str):
    if any(keyword in code.upper() for keyword in SQL_KEYWORDS) and "+" in code:
        return True
    return False


def is_potential_xss(code: str):
    return any(re.search(pattern, code) for pattern in XSS_PATTERNS)


def sanitize_text(text: str):
    return text.strip()
