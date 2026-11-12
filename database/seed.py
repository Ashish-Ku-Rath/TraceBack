"""
Initial problem seed data for TraceBack.
Provides an idempotent seed mechanism that populates the database with initial DSA problems.
"""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from backend.models.problem import Problem, ProblemExample
from database.connection import SessionLocal, init_db

# Initial problem definitions with original descriptions and sample examples
INITIAL_PROBLEMS: List[Dict[str, Any]] = [
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Map"],
        "description": (
            "Given an integer array `nums` and an integer `target`, determine and return "
            "the 0-based indices of the two elements whose sum equals `target`.\n\n"
            "Assumptions:\n"
            "- Exactly one valid solution exists for each input test case.\n"
            "- You cannot use the same array element twice.\n"
            "- The answer indices can be returned in any order."
        ),
        "constraints": (
            "2 <= nums.length <= 10^4\n"
            "-10^9 <= nums[i] <= 10^9\n"
            "-10^9 <= target <= 10^9\n"
            "Exactly one valid solution exists."
        ),
        "examples": [
            {
                "input": "nums = [2, 7, 11, 15], target = 9",
                "expected_output": "[0, 1]",
                "explanation": "Because nums[0] + nums[1] == 2 + 7 == 9, return [0, 1].",
            },
            {
                "input": "nums = [3, 2, 4], target = 6",
                "expected_output": "[1, 2]",
                "explanation": "Because nums[1] + nums[2] == 2 + 4 == 6, return [1, 2].",
            },
            {
                "input": "nums = [3, 3], target = 6",
                "expected_output": "[0, 1]",
                "explanation": "Because nums[0] + nums[1] == 3 + 3 == 6, return [0, 1].",
            },
        ],
    },
    {
        "title": "Reverse String",
        "slug": "reverse-string",
        "difficulty": "Easy",
        "tags": ["String", "Two Pointers"],
        "description": (
            "Write a function that reverses an input string represented as an array of characters `s`.\n\n"
            "Requirements:\n"
            "- Perform the reversal in-place by mutating the original array directly.\n"
            "- Do not allocate extra memory for another array (O(1) auxiliary space)."
        ),
        "constraints": (
            "1 <= s.length <= 10^5\n"
            "s[i] consists of printable ASCII characters."
        ),
        "examples": [
            {
                "input": 's = ["h", "e", "l", "l", "o"]',
                "expected_output": '["o", "l", "l", "e", "h"]',
                "explanation": "The array of characters is inverted completely in-place.",
            },
            {
                "input": 's = ["H", "a", "n", "n", "a", "h"]',
                "expected_output": '["h", "a", "n", "n", "a", "H"]',
                "explanation": "Case is preserved and all characters are reversed.",
            },
        ],
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "difficulty": "Medium",
        "tags": ["String", "Stack"],
        "description": (
            "Given a string `s` containing only the characters '(', ')', '{', '}', '[' and ']', "
            "determine whether the bracket sequence is structurally valid.\n\n"
            "A bracket sequence is valid if and only if:\n"
            "1. Every open bracket is closed by a matching bracket of the identical type.\n"
            "2. Open brackets are closed in the exact order of their nesting.\n"
            "3. Every closing bracket matches a previously opened bracket."
        ),
        "constraints": (
            "1 <= s.length <= 10^4\n"
            "s consists exclusively of parentheses: '()[]{}'."
        ),
        "examples": [
            {
                "input": 's = "()[]{}"',
                "expected_output": "true",
                "explanation": "All three bracket pairs open and close in correct sequence.",
            },
            {
                "input": 's = "(]"',
                "expected_output": "false",
                "explanation": "The open parenthesis '(' is incorrectly closed by a square bracket ']'.",
            },
            {
                "input": 's = "([)]"',
                "expected_output": "false",
                "explanation": "The parentheses and brackets interleave out of order.",
            },
        ],
    },
]


def seed_problems(db: Optional[Session] = None) -> List[Problem]:
    """
    Idempotently insert initial DSA problems into the database.
    Checks each problem by slug and skips existing records to avoid duplicates.
    Never truncates or overwrites existing user data.
    """
    should_close = False
    session = db
    if session is None:
        init_db()
        session = SessionLocal()
        should_close = True

    seeded_records: List[Problem] = []

    try:
        for p_data in INITIAL_PROBLEMS:
            slug = p_data["slug"]
            existing = session.query(Problem).filter(Problem.slug == slug).first()

            if existing is not None:
                seeded_records.append(existing)
                continue

            # Create new Problem
            problem = Problem(
                title=p_data["title"],
                slug=p_data["slug"],
                description=p_data["description"],
                difficulty=p_data["difficulty"],
                constraints=p_data.get("constraints", ""),
                tags=p_data.get("tags", []),
            )
            session.add(problem)
            session.flush()  # Flush to obtain problem.id

            # Create associated public sample examples
            for ex in p_data.get("examples", []):
                example = ProblemExample(
                    problem_id=problem.id,
                    input=ex["input"],
                    expected_output=ex["expected_output"],
                    explanation=ex.get("explanation"),
                )
                session.add(example)

            session.commit()
            session.refresh(problem)
            seeded_records.append(problem)

        return seeded_records
    finally:
        if should_close:
            session.close()


if __name__ == "__main__":
    print("[*] Initializing database and running idempotent seed...")
    results = seed_problems()
    print(f"[+] Seeding complete. Total available seed problems: {len(results)}")
    for p in results:
        print(f"    - [{p.id}] {p.title} ({p.difficulty}) | slug: {p.slug} | examples: {len(p.examples)}")

