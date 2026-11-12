"""
Coding Workspace page for TraceBack (Day 5).
Implements a professional split-screen coding workspace:
- Top Navigation: Back to Problems, Title, Python 3 indicator, Run Code (Day 6 disabled), Submit (Day 6 disabled).
- Left Panel: Distraction-free problem description with independent scrolling.
- Right Panel: Monaco editor with Python 3 syntax highlighting, stable cursor state management,
  and Complete Program Mode (stdin -> stdout).
- Testcase & Test Result tabs with custom stdin input and sample input helper.
"""

import html
from typing import Optional
import streamlit as st
from frontend.api_client import api_client
from frontend.components.cards import render_backend_offline_alert
from frontend.components.monaco_editor import render_monaco_editor
from frontend.components.problem_card import (
    get_difficulty_badge_html,
    get_tags_html,
)
from frontend.starter_templates import get_sample_input, get_starter_template


def clean_html(raw_html: str) -> str:
    """
    Strip leading and trailing whitespace from each line.
    Prevents Markdown from interpreting indented HTML fragments as code blocks.
    """
    return "\n".join(line.strip() for line in raw_html.splitlines() if line.strip())


def render_workspace_page(problem_id: Optional[int] = None):
    """Render the full split-screen coding workspace."""
    # Target problem ID
    target_id = problem_id or st.session_state.get("selected_problem_id", 1)

    # Fetch problem details from backend
    problem, error = api_client.get_problem_by_id(target_id)
    if error:
        render_backend_offline_alert(error)
        if st.button("← Back to Problems", key="ws_err_back_btn"):
            st.session_state["current_page"] = "problems"
            st.session_state["selected_problem_id"] = None
            st.rerun()
        return

    if not problem:
        st.error(f"Problem #{target_id} could not be loaded from database.")
        if st.button("← Back to Problems", key="ws_notfound_back_btn"):
            st.session_state["current_page"] = "problems"
            st.session_state["selected_problem_id"] = None
            st.rerun()
        return

    p_id = problem.get("id", target_id)
    title = problem.get("title", "Untitled Problem")
    difficulty = problem.get("difficulty", "Easy")
    description = problem.get("description", "")
    constraints = problem.get("constraints", "")
    tags = problem.get("tags", [])
    examples = problem.get("examples", [])

    # -------------------------------------------------------------------------
    # Stable Editor State Management (Prevents Cursor Jumping)
    # -------------------------------------------------------------------------
    code_key = f"code_{p_id}"
    init_key = f"editor_init_{p_id}"
    counter_key = f"reset_counter_{p_id}"
    last_visited_key = "last_visited_problem_id"

    if counter_key not in st.session_state:
        st.session_state[counter_key] = 0

    # If this problem has never been initialized in session state, set starter template
    if code_key not in st.session_state:
        st.session_state[code_key] = get_starter_template(p_id)
        st.session_state[init_key] = st.session_state[code_key]

    # Detect if user just navigated back to this problem from another problem
    if st.session_state.get(last_visited_key) != p_id:
        st.session_state[last_visited_key] = p_id
        # Mount editor with current persisted code for this problem
        st.session_state[init_key] = st.session_state[code_key]
        st.session_state[counter_key] += 1

    # Stdin state tracking
    stdin_key = f"stdin_{p_id}"
    if stdin_key not in st.session_state:
        st.session_state[stdin_key] = get_sample_input(problem)

    # =========================================================================
    # Top Compact Navigation Bar (Section 6 Requirement)
    # =========================================================================
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1.5, 3.2, 1.8, 1.3, 1.3])
    with nav_col1:
        if st.button("←  Back to Problems", key="ws_nav_back", type="secondary"):
            st.session_state["current_page"] = "problems"
            st.session_state["selected_problem_id"] = None
            st.rerun()

    with nav_col2:
        topbar_info_html = f"""
        <div style="display: flex; align-items: center; gap: 8px; padding-top: 5px;">
            <span style="font-weight: 700; color: #94A3B8; font-size: 0.92rem;">#{p_id}</span>
            <span style="font-weight: 700; color: #FFFFFF; font-size: 1.05rem;">{title}</span>
            <span style="color: #334155;">|</span>
            {get_difficulty_badge_html(difficulty)}
        </div>
        """
        st.markdown(clean_html(topbar_info_html), unsafe_allow_html=True)

    with nav_col3:
        badge_html = """
        <div style="display: flex; justify-content: flex-end; align-items: center; padding-top: 5px;">
            <span class="tb-badge-lang">🐍 Python 3 (Complete Program)</span>
        </div>
        """
        st.markdown(clean_html(badge_html), unsafe_allow_html=True)

    with nav_col4:
        st.button(
            "▶  Run Code",
            key=f"top_run_{p_id}",
            disabled=True,
            use_container_width=True,
            help="Code execution will be available in Day 6.",
        )

    with nav_col5:
        st.button(
            "Submit",
            key=f"top_submit_{p_id}",
            disabled=True,
            use_container_width=True,
            help="Automated judging will be available in Day 6.",
        )

    # Sub-navigation informational banner for Day 6
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end; font-size: 0.74rem; color: #94A3B8; margin-top: -6px; margin-bottom: 6px;">
            <span>ℹ️ Code execution will be available in Day 6.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border: none; border-top: 1px solid #1E293B; margin: 4px 0 16px 0;'>", unsafe_allow_html=True)

    # =========================================================================
    # Split-Screen Layout: Left Panel (Description) & Right Panel (Editor)
    # =========================================================================
    left_col, right_col = st.columns([1.05, 1.25])

    # -------------------------------------------------------------------------
    # LEFT PANEL: Problem Description (Independent Scroll)
    # -------------------------------------------------------------------------
    with left_col:
        # Format description paragraphs
        paragraphs = [p.strip() for p in description.split("\n\n") if p.strip()]
        desc_paragraphs_html = "".join(
            f"<p style='margin: 0 0 12px 0; line-height: 1.65; color: #F8FAFC; font-size: 0.92rem;'>{html.escape(p)}</p>"
            for p in paragraphs
        ) if paragraphs else f"<p style='color: #F8FAFC; font-size: 0.92rem;'>{html.escape(description)}</p>"

        # Format examples
        examples_html_list = []
        if not examples:
            examples_html_list.append(
                "<div style='color: #CBD5E1; font-size: 0.85rem; font-style: italic;'>No sample test cases configured.</div>"
            )
        else:
            for idx, ex in enumerate(examples, start=1):
                input_str = ex.get("input", "")
                output_str = ex.get("expected_output", "")
                explanation = ex.get("explanation")

                explanation_html = (
                    f"<div style='margin-top: 8px; font-size: 0.84rem; color: #CBD5E1; line-height: 1.5;'>"
                    f"<strong style='color: #F8FAFC;'>Explanation: </strong>{html.escape(explanation)}"
                    f"</div>"
                    if explanation
                    else ""
                )

                ex_box = f"""
                <div style="margin-bottom: 16px;">
                    <div style="font-size: 0.85rem; font-weight: 600; color: #FFFFFF; margin-bottom: 6px;">
                        Example {idx}:
                    </div>
                    <div class="tb-code-box">
                        <div><strong style="color: #94A3B8;">Input:</strong> <span style="color: #F8FAFC;">{html.escape(input_str)}</span></div>
                        <div style="margin-top: 4px;"><strong style="color: #94A3B8;">Output:</strong> <span style="color: #34D399; font-weight: 600;">{html.escape(output_str)}</span></div>
                    </div>
                    {explanation_html}
                </div>
                """
                examples_html_list.append(ex_box)

        rendered_examples = "".join(examples_html_list)

        # Format constraints
        lines = [c.strip() for c in constraints.split("\n") if c.strip()]
        if lines:
            c_items = "".join(
                f"<li style='margin-bottom: 6px;'>"
                f"<code style='background: #000000; color: #E2E8F0; padding: 2px 7px; border-radius: 4px; border: 1px solid #1E293B; font-family: monospace; font-size: 0.84rem;'>"
                f"{html.escape(line)}"
                f"</code>"
                f"</li>"
                for line in lines
            )
            constraints_html = f"<ul style='padding-left: 20px; margin: 0; font-size: 0.85rem; color: #CBD5E1; line-height: 1.6;'>{c_items}</ul>"
        else:
            constraints_html = "<div style='color: #CBD5E1; font-size: 0.85rem;'>Standard algorithmic constraints apply.</div>"

        # Complete Left Panel HTML
        left_panel_html = f"""
        <div class="tb-workspace-desc-panel">
            <div style="margin-bottom: 14px;">
                <h2 style="font-size: 1.6rem; font-weight: 700; margin: 0 0 8px 0; color: #FFFFFF;">
                    #{p_id} {title}
                </h2>
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    {get_difficulty_badge_html(difficulty)}
                    <span style="color: #334155;">|</span>
                    <div>{get_tags_html(tags)}</div>
                </div>
            </div>

            <hr style="border: none; border-top: 1px solid #1E293B; margin: 14px 0 16px 0;">

            <div class="tb-panel-heading">Problem Description</div>
            <div style="margin-bottom: 22px;">
                {desc_paragraphs_html}
            </div>

            <div class="tb-panel-heading">Examples</div>
            <div style="margin-bottom: 22px;">
                {rendered_examples}
            </div>

            <div class="tb-panel-heading">Constraints</div>
            <div>
                {constraints_html}
            </div>
        </div>
        """
        st.markdown(clean_html(left_panel_html), unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # RIGHT PANEL: Monaco Editor + Header + Testcase / Test Result Tabs
    # -------------------------------------------------------------------------
    with right_col:
        # Editor Tab Header Bar
        hdr_c1, hdr_c2, hdr_c3 = st.columns([2.6, 1.3, 1.1])
        with hdr_c1:
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 8px; height: 38px;">
                    <span style="font-size: 1.0rem;">💻</span>
                    <span style="font-weight: 600; font-size: 0.88rem; color: #F8FAFC;">Solution.py</span>
                    <span style="font-size: 0.72rem; color: #64748B; background: #0F172A; padding: 2px 6px; border-radius: 4px; border: 1px solid #1E293B;">Ctrl+S to save</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with hdr_c2:
            if st.button("💾 Save Draft", key=f"save_draft_{p_id}", type="secondary", use_container_width=True, help="Synchronize and save draft to session (or press Ctrl+S)"):
                st.session_state[f"draft_saved_{p_id}"] = True
                st.rerun()

        with hdr_c3:
            if st.button("↺ Reset", key=f"reset_code_{p_id}", type="secondary", use_container_width=True, help="Reset to initial starter template"):
                template = get_starter_template(p_id)
                st.session_state[code_key] = template
                st.session_state[init_key] = template
                st.session_state[counter_key] += 1
                st.rerun()

        if st.session_state.get(f"draft_saved_{p_id}"):
            st.markdown(
                "<div style='font-size: 0.76rem; color: #34D399; margin-bottom: 6px;'>✓ Draft synchronized and saved to session.</div>",
                unsafe_allow_html=True,
            )
            st.session_state[f"draft_saved_{p_id}"] = False

        # Monaco Editor Component with Stable Key and Initial Code
        editor_key = f"monaco_{p_id}_{st.session_state[counter_key]}"
        edited_code = render_monaco_editor(
            code=st.session_state[init_key],
            key=editor_key,
            height="440px",
            language="python",
            theme="vs-dark",
            line_numbers=True,
            minimap=False,
        )

        # Update persisted code in session state without modifying init_key
        # This prevents React prop updates from forcing Monaco executeEdits / cursor jumping
        if edited_code and edited_code != st.session_state[code_key]:
            st.session_state[code_key] = edited_code

        # ---------------------------------------------------------------------
        # Bottom Tabs: Testcase & Test Result
        # ---------------------------------------------------------------------
        tab_testcase, tab_result = st.tabs(["🧪 Testcase", "📊 Test Result"])

        # Tab 1: Testcase
        with tab_testcase:
            t_col1, t_col2, _ = st.columns([1.5, 1.3, 3])
            with t_col1:
                if st.button("📋 Load Sample Input", key=f"load_sample_{p_id}", use_container_width=True):
                    sample_in = get_sample_input(problem)
                    st.session_state[stdin_key] = sample_in
                    st.rerun()

            with t_col2:
                if st.button("🗑️ Clear Input", key=f"clear_stdin_{p_id}", use_container_width=True):
                    st.session_state[stdin_key] = ""
                    st.rerun()

            user_stdin = st.text_area(
                "Standard Input (stdin)",
                value=st.session_state.get(stdin_key, ""),
                height=110,
                key=f"ta_stdin_{p_id}",
                help="Input provided to the program via sys.stdin / input()",
                label_visibility="collapsed",
            )
            # Synchronize custom stdin input
            st.session_state[stdin_key] = user_stdin

            st.markdown(
                "<div style='font-size: 0.76rem; color: #94A3B8; margin-top: 4px;'>In Complete Program Mode, standard input is read directly by <code>sys.stdin.read()</code> or <code>input()</code>.</div>",
                unsafe_allow_html=True,
            )

        # Tab 2: Test Result
        with tab_result:
            code_preview = st.session_state.get(code_key, "")
            num_lines = len(code_preview.splitlines())
            char_count = len(code_preview)
            stdin_preview = st.session_state.get(stdin_key, "")

            st.markdown(
                f"""
                <div style="background: #090B0F; border: 1px dashed #1E293B; border-radius: 8px; padding: 20px; text-align: center; color: #94A3B8;">
                    <div style="font-size: 1.5rem; margin-bottom: 6px;">⚙️</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #F8FAFC; margin-bottom: 6px;">
                        Code Execution Engine (Day 6)
                    </div>
                    <div style="font-size: 0.84rem; line-height: 1.5; color: #CBD5E1; max-width: 500px; margin: 0 auto 12px auto;">
                        Code execution will be available in Day 6.<br>
                        Your program is written in Complete Program Mode. Use the Testcase tab to prepare and inspect custom test inputs.
                    </div>
                    <div style="display: inline-flex; gap: 16px; font-size: 0.78rem; background: #000000; border: 1px solid #1E293B; border-radius: 6px; padding: 6px 14px; color: #94A3B8;">
                        <span>Source: <strong style="color: #F8FAFC;">{num_lines} lines ({char_count} chars)</strong></span>
                        <span>Stdin: <strong style="color: #F8FAFC;">{len(stdin_preview.splitlines())} lines</strong></span>
                        <span>Target: <strong style="color: #34D399;">Python 3 (CPython 3.10)</strong></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
