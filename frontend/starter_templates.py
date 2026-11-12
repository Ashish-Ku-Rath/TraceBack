"""
Starter code templates and sample inputs for TraceBack coding workspace.
All templates follow Complete Program Mode (Codeforces / CodeChef style)
where solutions read from stdin and write to stdout.
"""

from typing import Any, Dict

# Pre-configured Complete Program templates tailored to each problem
STARTER_TEMPLATES: Dict[int, str] = {
    1: """# Complete Program Mode (stdin -> stdout)
# Problem 1: Two Sum
# Input format:
#   Line 1: n (number of elements)
#   Line 2: space-separated integers (nums)
#   Line 3: target integer
# Output format:
#   Indices of the two numbers separated by space (e.g. 0 1)

import sys

def solve():
    lines = sys.stdin.read().split()
    if not lines:
        return
    n = int(lines[0])
    nums = [int(x) for x in lines[1:n+1]]
    target = int(lines[n+1])
    
    # Write your solution below
    pass

if __name__ == "__main__":
    solve()
""",
    2: """# Complete Program Mode (stdin -> stdout)
# Problem 2: Reverse String
# Input format:
#   Line 1: string s to reverse
# Output format:
#   Reversed string

import sys

def solve():
    s = sys.stdin.readline().rstrip("\\r\\n")
    if not s:
        return
        
    # Write your solution below
    pass

if __name__ == "__main__":
    solve()
""",
    3: """# Complete Program Mode (stdin -> stdout)
# Problem 3: Valid Parentheses
# Input format:
#   Line 1: string s containing brackets '(', ')', '{', '}', '[', ']'
# Output format:
#   true or false

import sys

def solve():
    s = sys.stdin.readline().rstrip("\\r\\n")
    if not s:
        return
        
    # Write your solution below
    pass

if __name__ == "__main__":
    solve()
""",
}

DEFAULT_TEMPLATE = """# Complete Program Mode (stdin -> stdout)
# Read input from standard input (sys.stdin or input())
# Print solution output to standard output (print() or sys.stdout)

import sys

def solve():
    # Read input from stdin
    pass

if __name__ == "__main__":
    solve()
"""

# Default sample stdin for testing in the Testcase tab
SAMPLE_INPUTS: Dict[int, str] = {
    1: "4\n2 7 11 15\n9",
    2: "hello",
    3: "()[]{}",
}


def get_starter_template(problem_id: int) -> str:
    """Return the Complete Program starter template for the given problem ID."""
    return STARTER_TEMPLATES.get(problem_id, DEFAULT_TEMPLATE)


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

