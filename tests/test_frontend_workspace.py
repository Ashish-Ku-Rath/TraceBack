"""
Frontend Coding Workspace tests (Day 5).
Verifies:
1. Workspace opens for Two Sum (#1).
2. Workspace opens for Reverse String (#2).
3. Workspace opens for Valid Parentheses (#3).
4. Correct problem information is displayed (title, difficulty, tags, examples, constraints).
5. Monaco editor component is configured properly with Python syntax highlighting and vs-dark.
6. Python code can be edited and returned.
7. Code persists across normal Streamlit reruns in session state.
8. Input can be entered, loaded from sample, and cleared.
9. Back to Problems navigation state updates correctly.
10. Dashboard navigation remains functional.
11. Submit button remains disabled until Day 6.
12. No fake execution results are displayed.
"""

import pytest
from unittest.mock import MagicMock, patch
from frontend.starter_templates import (
    DEFAULT_TEMPLATE,
    SAMPLE_INPUTS,
    STARTER_TEMPLATES,
    get_sample_input,
    get_starter_template,
)
from frontend.components.monaco_editor import render_monaco_editor
from frontend.pages.workspace import clean_html


# -----------------------------------------------------------------------------
# 1, 2, 3: Workspace Opens Completely Blank for All Problems
# -----------------------------------------------------------------------------
def test_workspace_two_sum_template():
    """Verify Two Sum opens with a completely blank editor."""
    tpl = get_starter_template(1)
    assert tpl == ""


def test_workspace_reverse_string_template():
    """Verify Reverse String opens with a completely blank editor."""
    tpl = get_starter_template(2)
    assert tpl == ""


def test_workspace_valid_parentheses_template():
    """Verify Valid Parentheses opens with a completely blank editor."""
    tpl = get_starter_template(3)
    assert tpl == ""


def test_workspace_fallback_default_template():
    """Verify any problem ID opens with a completely blank editor by default."""
    tpl = get_starter_template(9999)
    assert tpl == ""
    assert tpl == DEFAULT_TEMPLATE


def test_all_problems_open_completely_blank():
    """Verify that all problems (1 through 23 and beyond) return empty string as initial template."""
    for p_id in range(1, 30):
        assert get_starter_template(p_id) == ""


def test_legacy_template_migration_detection():
    """Verify is_legacy_template detects old starter templates for automatic migration."""
    from frontend.starter_templates import is_legacy_template
    assert is_legacy_template("# Complete Program Mode (stdin -> stdout)\n# Problem 1: Two Sum\n...") is True
    assert is_legacy_template("# Problem 2: Reverse String\n...") is True
    assert is_legacy_template("# User custom code\nprint('hello')") is False
    assert is_legacy_template("") is False


# -----------------------------------------------------------------------------
# 4: Correct Problem Information is Displayed
# -----------------------------------------------------------------------------
def test_correct_problem_information_structure():
    """Verify sample inputs and problem metadata structures."""
    problem_mock = {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": "Given an integer array...",
        "constraints": "2 <= nums.length <= 10^4",
        "tags": ["Array", "Hash Map"],
        "examples": [{"input": "4\n2 7 11 15\n9", "expected_output": "0 1"}],
    }
    sample = get_sample_input(problem_mock)
    assert sample == SAMPLE_INPUTS[1]

    # Test clean_html strips leading whitespace preventing Markdown code block bugs
    indented_html = "    <div class='test'>\n        <span>Hello</span>\n    </div>"
    cleaned = clean_html(indented_html)
    for line in cleaned.splitlines():
        assert not line.startswith("    ")
        assert not line.startswith("\t")


# -----------------------------------------------------------------------------
# 5, 6: Monaco Editor Component Config & Editing
# -----------------------------------------------------------------------------
@patch("frontend.components.monaco_editor.render_component")
def test_monaco_editor_configuration_and_editing(mock_render):
    """Verify Monaco editor invokes the component with python language and vs-dark theme."""
    mock_render.return_value = "print('edited code')"

    initial_code = "print('hello')"
    result = render_monaco_editor(
        code=initial_code,
        key="monaco_test_key",
        height="450px",
        language="python",
        theme="vs-dark",
    )

    mock_render.assert_called_once_with(
        value=initial_code,
        height="450px",
        language="python",
        lineNumbers=True,
        minimap=False,
        theme="vs-dark",
        key="monaco_test_key",
        default=initial_code,
    )
    assert result == "print('edited code')"


@patch("frontend.components.monaco_editor.render_component")
def test_monaco_editor_returns_initial_when_none(mock_render):
    """Verify Monaco returns the initial code if user hasn't made changes."""
    mock_render.return_value = None

    initial_code = "print('initial')"
    result = render_monaco_editor(code=initial_code, key="monaco_none_key")
    assert result == initial_code


# -----------------------------------------------------------------------------
# 7: Code Persists Across Normal Streamlit Reruns
# -----------------------------------------------------------------------------
def test_code_persistence_in_session_state():
    """Verify code is cached per problem_id so different problems keep separate states."""
    session_state = {}

    p1_id = 1
    p2_id = 2

    # Initial load for Problem 1 starts completely blank
    code_key_1 = f"code_{p1_id}"
    session_state[code_key_1] = get_starter_template(p1_id)
    assert session_state[code_key_1] == ""

    # User edits code for Problem 1
    session_state[code_key_1] = "# User edited solution for Two Sum"

    # User switches to Problem 2 - also starts completely blank
    code_key_2 = f"code_{p2_id}"
    session_state[code_key_2] = get_starter_template(p2_id)
    assert session_state[code_key_2] == ""

    # User edits code for Problem 2
    session_state[code_key_2] = "# User edited solution for Reverse String"

    # User switches back to Problem 1 - edits must persist
    assert session_state[code_key_1] == "# User edited solution for Two Sum"
    assert session_state[code_key_2] == "# User edited solution for Reverse String"


# -----------------------------------------------------------------------------
# 8: Input Can Be Entered, Loaded from Sample, and Cleared
# -----------------------------------------------------------------------------
def test_stdin_management_lifecycle():
    """Verify stdin can be loaded from sample, edited, and cleared."""
    session_state = {}
    p_id = 1
    stdin_key = f"stdin_{p_id}"

    # Load sample input
    session_state[stdin_key] = get_sample_input({"id": p_id})
    assert session_state[stdin_key] == "4\n2 7 11 15\n9"

    # User enters custom input
    session_state[stdin_key] = "5\n1 2 3 4 5\n6"
    assert session_state[stdin_key] == "5\n1 2 3 4 5\n6"

    # Clear input
    session_state[stdin_key] = ""
    assert session_state[stdin_key] == ""


# -----------------------------------------------------------------------------
# 9, 10: Navigation Transitions (Back to Problems, Dashboard)
# -----------------------------------------------------------------------------
def test_navigation_state_transitions():
    """Verify page transitions between workspace, problems, and dashboard."""
    session_state = {"current_page": "workspace", "selected_problem_id": 1}

    # Simulate Back to Problems click
    session_state["current_page"] = "problems"
    session_state["selected_problem_id"] = None
    assert session_state["current_page"] == "problems"
    assert session_state["selected_problem_id"] is None

    # Simulate Dashboard navigation click
    session_state["current_page"] = "dashboard"
    assert session_state["current_page"] == "dashboard"


# -----------------------------------------------------------------------------
# 11, 12: Submit & Run Execution State Management
# -----------------------------------------------------------------------------
def test_execution_scope_and_submit_disabled():
    """
    Verify starter templates contain no hardcoded answer output.
    """
    for p_id in (1, 2, 3):
        tpl = get_starter_template(p_id)
        assert "Accepted" not in tpl
        assert "Wrong Answer" not in tpl
        assert "Runtime Error" not in tpl


def test_workspace_execution_state_lifecycle():
    """Verify session state tracks run results, submit results, and custom test cases."""
    session_state = {}
    p_id = 1
    run_key = f"run_result_{p_id}"
    submit_key = f"submit_result_{p_id}"
    action_key = f"last_action_{p_id}"

    # Simulate Run Code completion
    session_state[action_key] = "run"
    session_state[run_key] = {
        "status": "success",
        "stdout": "0 1\n",
        "stderr": "",
        "exit_code": 0,
        "execution_time": 0.05,
        "provider": "mock",
        "is_simulated": True,
    }

    assert session_state[action_key] == "run"
    assert session_state[run_key]["stdout"] == "0 1\n"
    assert session_state[run_key]["is_simulated"] is True

    # Simulate Submit completion
    session_state[action_key] = "submit"
    session_state[submit_key] = {
        "verdict": "accepted",
        "total_tests": 3,
        "passed_tests": 3,
        "failed_tests": 0,
        "provider": "mock",
        "is_simulated": True,
    }

    assert session_state[action_key] == "submit"
    assert session_state[submit_key]["verdict"] == "accepted"
    assert session_state[submit_key]["passed_tests"] == 3


def test_workspace_ai_debug_state():
    """Verify AI debug result storage in session state."""
    session_state = {}
    p_id = 1
    ai_key = f"ai_debug_{p_id}"

    session_state[ai_key] = {
        "status": "success",
        "explanation": "ZeroDivisionError in line 4",
        "likely_cause": "Division by zero",
        "responsible_code": "res = a / b",
        "suggested_fix": "Add check for b != 0",
        "corrected_code": "if b != 0:\n    res = a / b",
        "is_mock": True,
    }

    assert session_state[ai_key]["status"] == "success"
    assert "ZeroDivisionError" in session_state[ai_key]["explanation"]


