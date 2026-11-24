"""
Starter code templates and sample inputs for TraceBack coding workspace.
All problems now open with a completely blank editor by default.
"""

from typing import Any, Dict

# Blank starter template for all problems
DEFAULT_TEMPLATE = ""

# Pre-configured templates map (empty to ensure completely blank editor)
STARTER_TEMPLATES: Dict[int, str] = {}

# Legacy starter templates kept strictly to identify and migrate legacy session states
_LEGACY_SNIPPETS = [
    "# Problem 1: Two Sum",
    "# Problem 2: Reverse String",
    "# Problem 3: Valid Parentheses",
    "# Complete Program Mode (stdin -> stdout)\n# Read input from standard input",
]


def is_legacy_template(code: str) -> bool:
    """Return True if code is an automatically generated legacy starter template."""
    if not code or not isinstance(code, str):
        return False
    trimmed = code.strip()
    for snippet in _LEGACY_SNIPPETS:
        if snippet in trimmed:
            return True
    return False


# Default sample stdin for testing in the Testcase tab
SAMPLE_INPUTS: Dict[int, str] = {
    1: "4\n2 7 11 15\n9",
    2: "hello",
    3: "()[]{}",
}


def get_starter_template(problem_id: int) -> str:
    """
    Return the starter template for the given problem ID.
    Always returns empty string so that the editor opens completely blank.
    """
    return ""


def get_sample_input(problem: Dict[str, Any]) -> str:
    """
    Extract sample stdin from problem metadata or pre-configured defaults.
    """
    p_id = problem.get("id", 0)
    if p_id in SAMPLE_INPUTS:
        return SAMPLE_INPUTS[p_id]

    # Fallback to first example's input if available
    examples = problem.get("examples", [])
    if examples and isinstance(examples, list):
        return str(examples[0].get("input", ""))

    return ""
