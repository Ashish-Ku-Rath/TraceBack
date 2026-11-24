"""
Coding Workspace page for TraceBack.
Implements a complete competitive-programming split-screen coding workspace:
- Top Navigation: Back to Problems, Title, Difficulty, Python 3 Indicator, Run Code, Submit.
- Left Panel: Distraction-free problem description, Input/Output format, constraints, examples.
- Right Panel: Monaco editor with client-side model, stable cursor, zero-flashing architecture.
- Bottom Tabs:
  1. Testcase (stdin): custom input, sample input loader, clear input.
  2. Execution Output: live output for Run Code and Submit, verdicts, stdout/stderr, execution stats.
  3. Custom Test Lab: multi-testcase evaluation with expected outputs.
  4. AI Debug Assistant: Gemini-powered error explanations, root causes, and suggested fixes.
"""

import html
from typing import Any, Dict, List, Optional
import streamlit as st
from frontend.api_client import api_client
from frontend.components.cards import render_backend_offline_alert
from frontend.components.monaco_editor import render_monaco_editor
from frontend.components.problem_card import (
    get_difficulty_badge_html,
    get_tags_html,
)
from frontend.starter_templates import (
    get_sample_input,
    get_starter_template,
    is_legacy_template,
)


def clean_html(raw_html: str) -> str:
    """Strip leading and trailing whitespace from each line."""
    return "\n".join(line.strip() for line in raw_html.splitlines() if line.strip())


def render_workspace_page(problem_id: Optional[int] = None):
    """Render the full split-screen coding workspace."""
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
    # Stable Editor State Management
    # -------------------------------------------------------------------------
    code_key = f"code_{p_id}"
    init_key = f"editor_init_{p_id}"
    counter_key = f"reset_counter_{p_id}"
    last_visited_key = "last_visited_problem_id"

    if counter_key not in st.session_state:
        st.session_state[counter_key] = 0

    if code_key not in st.session_state:
        st.session_state[code_key] = ""
        st.session_state[init_key] = ""
    elif is_legacy_template(st.session_state.get(code_key, "")):
        # Safely migrate automatically generated legacy template to empty editor
        st.session_state[code_key] = ""
        st.session_state[init_key] = ""

    if st.session_state.get(last_visited_key) != p_id:
        st.session_state[last_visited_key] = p_id
        st.session_state[init_key] = st.session_state[code_key]
        st.session_state[counter_key] += 1

    # Stdin state tracking
    stdin_key = f"stdin_{p_id}"
    if stdin_key not in st.session_state:
        st.session_state[stdin_key] = get_sample_input(problem)

    # Execution and AI debug result state
    run_result_key = f"run_result_{p_id}"
    submit_result_key = f"submit_result_{p_id}"
    ai_debug_key = f"ai_debug_{p_id}"
    custom_tests_key = f"custom_tests_{p_id}"
    active_tab_key = f"active_tab_{p_id}"

    # Initialize custom test lab items if not present
    if custom_tests_key not in st.session_state:
        st.session_state[custom_tests_key] = [
            {"input": ex.get("input", ""), "expected_output": ex.get("expected_output", "")}
            for ex in examples[:2]
        ] if examples else [{"input": "", "expected_output": ""}]

    # =========================================================================
    # Top Compact Navigation Bar
    # =========================================================================
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1.5, 3.0, 1.8, 1.3, 1.3])
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

    # Action flags
    trigger_run = False
    trigger_submit = False

    with nav_col4:
        if st.button("▶  Run Code", key=f"top_run_{p_id}", type="secondary", use_container_width=True, help="Execute code remotely with custom standard input"):
            trigger_run = True

    with nav_col5:
        if st.button("Submit", key=f"top_submit_{p_id}", type="primary", use_container_width=True, help="Submit solution for official judging against problem test cases"):
            trigger_submit = True

    st.markdown("<hr style='border: none; border-top: 1px solid #1E293B; margin: 4px 0 16px 0;'>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Execute Actions if Triggered
    # -------------------------------------------------------------------------
    current_source = st.session_state.get(code_key, "")
    current_stdin = st.session_state.get(stdin_key, "")

    if trigger_run:
        with st.spinner("Executing Python code remotely..."):
            run_data, run_err = api_client.run_code(
                source_code=current_source,
                stdin=current_stdin,
                language="python",
            )
            if run_err:
                st.session_state[run_result_key] = {"status": "error", "error": run_err}
            else:
                st.session_state[run_result_key] = run_data
                st.session_state["last_action"] = "run"

    if trigger_submit:
        with st.spinner("Judging solution against problem test cases..."):
            submit_data, submit_err = api_client.submit_solution(
                problem_id=p_id,
                source_code=current_source,
                language="python",
            )
            if submit_err:
                st.session_state[submit_result_key] = {"verdict": "error", "error": submit_err}
            else:
                st.session_state[submit_result_key] = submit_data
                st.session_state["last_action"] = "submit"

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
            f"<div style='margin: 0 0 12px 0; line-height: 1.65; color: #F8FAFC; font-size: 0.92rem;'>{html.escape(p).replace(chr(10), '<br>')}</div>"
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
                        <div><strong style="color: #94A3B8;">Input (stdin):</strong><br><pre style="margin: 4px 0; color: #F8FAFC; font-family: monospace;">{html.escape(input_str)}</pre></div>
                        <div style="margin-top: 6px;"><strong style="color: #94A3B8;">Expected Output:</strong><br><span style="color: #34D399; font-weight: 600; font-family: monospace;">{html.escape(output_str)}</span></div>
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
    # RIGHT PANEL: Monaco Editor + Header + Bottom Tabs
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
            if st.button("↺ Reset", key=f"reset_code_{p_id}", type="secondary", use_container_width=True, help="Clear editor completely"):
                st.session_state[code_key] = ""
                st.session_state[init_key] = ""
                st.session_state[counter_key] += 1
                st.rerun()

        if st.session_state.get(f"draft_saved_{p_id}"):
            st.markdown(
                "<div style='font-size: 0.76rem; color: #34D399; margin-bottom: 6px;'>✓ Draft synchronized and saved to session.</div>",
                unsafe_allow_html=True,
            )
            st.session_state[f"draft_saved_{p_id}"] = False

        st.markdown(
            """
            <div style="font-size: 0.80rem; color: #94A3B8; margin: 4px 0 8px 2px; display: flex; align-items: center; gap: 6px;">
                <span>✍️</span>
                <span>Write your complete Python solution here. The editor starts blank.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

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

        if edited_code and edited_code != st.session_state[code_key]:
            st.session_state[code_key] = edited_code

        # ---------------------------------------------------------------------
        # Bottom Tabs: Testcase, Output & Judging, Custom Test Lab, AI Debugger
        # ---------------------------------------------------------------------
        tab_testcase, tab_output, tab_custom, tab_ai = st.tabs([
            "🧪 Testcase (stdin)",
            "📊 Execution Output",
            "🔬 Custom Test Lab",
            "🤖 AI Debug Assistant",
        ])

        # Tab 1: Testcase (stdin)
        with tab_testcase:
            t_col1, t_col2, _ = st.columns([1.5, 1.3, 3])
            with t_col1:
                if st.button("📋 Load Sample Input", key=f"load_sample_{p_id}", use_container_width=True):
                    st.session_state[stdin_key] = get_sample_input(problem)
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
            st.session_state[stdin_key] = user_stdin

            st.markdown(
                "<div style='font-size: 0.76rem; color: #94A3B8; margin-top: 4px;'>In Complete Program Mode, standard input is read directly by <code>sys.stdin.read()</code> or <code>input()</code>.</div>",
                unsafe_allow_html=True,
            )

        # Tab 2: Execution Output (Run Code & Submit Results)
        with tab_output:
            last_action = st.session_state.get("last_action")
            run_res = st.session_state.get(run_result_key)
            submit_res = st.session_state.get(submit_result_key)

            if not run_res and not submit_res:
                st.markdown(
                    """
                    <div style="background: #090B0F; border: 1px dashed #1E293B; border-radius: 8px; padding: 26px; text-align: center; color: #94A3B8;">
                        <div style="font-size: 1.6rem; margin-bottom: 8px;">⚙️</div>
                        <div style="font-size: 0.95rem; font-weight: 600; color: #F8FAFC; margin-bottom: 4px;">
                            Execution Console Ready
                        </div>
                        <div style="font-size: 0.84rem; color: #CBD5E1;">
                            Click <strong>▶ Run Code</strong> to test with standard input, or <strong>Submit</strong> to evaluate against problem test cases.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif last_action == "submit" and submit_res:
                # Render Submit Judging Results
                verdict = submit_res.get("verdict", "error")
                passed = submit_res.get("passed_tests", 0)
                total = submit_res.get("total_tests", 0)
                tests_list = submit_res.get("tests", [])
                provider_name = submit_res.get("provider", "mock")
                is_sim = submit_res.get("is_simulated", True)

                # Verdict styling
                if verdict.lower() == "accepted":
                    v_color = "#10B981"
                    v_text = "ACCEPTED"
                    v_icon = "✓"
                elif verdict.lower() == "wrong_answer":
                    v_color = "#EF4444"
                    v_text = "WRONG ANSWER"
                    v_icon = "✗"
                else:
                    v_color = "#F59E0B"
                    v_text = verdict.upper().replace("_", " ")
                    v_icon = "!"

                sim_tag = "<span style='background: #1E3A5F; color: #93C5FD; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; margin-left: 8px;'>Simulated Execution</span>" if is_sim else "<span style='background: #064E3B; color: #34D399; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; margin-left: 8px;'>Remote Engine</span>"

                st.markdown(
                    f"""
                    <div style="background: #0F172A; border: 1px solid #1E293B; border-left: 4px solid {v_color}; border-radius: 8px; padding: 14px 18px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.15rem; font-weight: 800; color: {v_color}; letter-spacing: 0.03em;">{v_icon} {v_text}</span>
                                {sim_tag}
                            </div>
                            <div style="font-size: 0.85rem; color: #F8FAFC; font-weight: 600;">
                                Passed {passed} / {total} Test Cases
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Individual Test Case breakdown
                for idx, t_res in enumerate(tests_list, start=1):
                    t_verd = t_res.get("verdict", "unknown")
                    is_pass = t_verd.lower() == "accepted"
                    t_badge = "✓ Passed" if is_pass else "✗ Failed"
                    t_badge_col = "#10B981" if is_pass else "#EF4444"

                    with st.expander(f"Test Case #{idx} — {t_badge}", expanded=not is_pass):
                        st.markdown(f"**Input:**\n```text\n{t_res.get('input', '')}\n```")
                        col_exp, col_act = st.columns(2)
                        with col_exp:
                            st.markdown(f"**Expected Output:**\n```text\n{t_res.get('expected_output', '')}\n```")
                        with col_act:
                            st.markdown(f"**Actual Output:**\n```text\n{t_res.get('actual_output') or 'No output'}\n```")
                        if t_res.get("error"):
                            st.error(t_res.get("error"))

                # AI Debug button if submission failed
                if verdict.lower() != "accepted":
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    if st.button("🤖 Diagnose Failure with AI Assistant", key=f"ai_diag_submit_{p_id}", type="secondary"):
                        with st.spinner("AI Assistant analyzing failure..."):
                            ai_resp, ai_err = api_client.request_ai_debug(
                                problem_title=title,
                                problem_description=description,
                                source_code=current_source,
                                error_message=f"Verdict: {verdict}",
                                stdin=tests_list[0].get("input") if tests_list else "",
                                stdout=tests_list[0].get("actual_output") if tests_list else "",
                                stderr=tests_list[0].get("error") if tests_list else "",
                            )
                            st.session_state[ai_debug_key] = ai_resp or {"status": "error", "explanation": ai_err}
                            st.rerun()

            elif run_res:
                # Render Run Code Result
                status_val = run_res.get("status", "unknown")
                stdout_val = run_res.get("stdout", "")
                stderr_val = run_res.get("stderr", "")
                exit_code = run_res.get("exit_code", 0)
                exec_time = run_res.get("execution_time", 0.0)
                mem_kb = run_res.get("memory_kb", 0)
                provider_name = run_res.get("provider", "mock")
                is_sim = run_res.get("is_simulated", True)

                is_ok = status_val.lower() == "success" and exit_code == 0
                badge_bg = "#064E3B" if is_ok else "#7F1D1D"
                badge_fg = "#34D399" if is_ok else "#FCA5A5"
                status_label = "Process Finished Successfully" if is_ok else f"Execution Failed ({status_val.upper()})"

                sim_tag = "<span style='background: #1E3A5F; color: #93C5FD; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; margin-left: 8px;'>Simulated Execution</span>" if is_sim else "<span style='background: #064E3B; color: #34D399; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; margin-left: 8px;'>Remote Engine</span>"

                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #0B111D; border: 1px solid #1E293B; border-radius: 6px; padding: 8px 14px; margin-bottom: 10px;">
                        <div style="font-weight: 600; font-size: 0.88rem; color: {badge_fg};">
                            {status_label} {sim_tag}
                        </div>
                        <div style="font-size: 0.78rem; color: #94A3B8;">
                            ⏱️ {exec_time:.3f}s &nbsp;|&nbsp; 💾 {mem_kb} KB &nbsp;|&nbsp; Exit: {exit_code}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if stdout_val:
                    st.markdown("**Standard Output (stdout):**")
                    st.code(stdout_val, language="text")
                else:
                    st.info("Program completed with no stdout output.")

                if stderr_val:
                    st.markdown("**Standard Error (stderr):**")
                    st.code(stderr_val, language="text")

                # AI Debug button if Run Code failed
                if not is_ok:
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    if st.button("🤖 Diagnose Error with AI Assistant", key=f"ai_diag_run_{p_id}", type="secondary"):
                        with st.spinner("AI Assistant diagnosing error..."):
                            ai_resp, ai_err = api_client.request_ai_debug(
                                problem_title=title,
                                problem_description=description,
                                source_code=current_source,
                                error_message=stderr_val or status_val,
                                stdin=current_stdin,
                                stdout=stdout_val,
                                stderr=stderr_val,
                            )
                            st.session_state[ai_debug_key] = ai_resp or {"status": "error", "explanation": ai_err}
                            st.rerun()

        # Tab 3: Custom Test Lab (Multi-test case evaluation)
        with tab_custom:
            st.markdown(
                "<div style='font-size: 0.84rem; color: #CBD5E1; margin-bottom: 10px;'>"
                "Test your program against multiple custom input/output pairs using our automated remote test runner."
                "</div>",
                unsafe_allow_html=True,
            )

            test_items = st.session_state.get(custom_tests_key, [])

            for idx, item in enumerate(test_items):
                st.markdown(f"**Custom Test #{idx + 1}**")
                col_in, col_out = st.columns(2)
                with col_in:
                    item["input"] = st.text_area(f"Input #{idx + 1}", value=item.get("input", ""), height=70, key=f"ctl_in_{p_id}_{idx}")
                with col_out:
                    item["expected_output"] = st.text_area(f"Expected Output #{idx + 1}", value=item.get("expected_output", ""), height=70, key=f"ctl_out_{p_id}_{idx}")

            btn_col1, btn_col2, _ = st.columns([1.5, 1.3, 3])
            with btn_col1:
                if st.button("▶ Run Custom Tests", key=f"ctl_run_btn_{p_id}", type="primary"):
                    valid_tests = [t for t in test_items if t.get("expected_output")]
                    if not valid_tests:
                        st.warning("Please provide expected output for at least one test case.")
                    else:
                        with st.spinner("Evaluating custom test cases..."):
                            chk_data, chk_err = api_client.check_custom_tests(
                                source_code=current_source,
                                tests=valid_tests,
                                checker="trim",
                            )
                            if chk_err:
                                st.error(chk_err)
                            else:
                                st.session_state[f"ctl_results_{p_id}"] = chk_data
                                st.rerun()

            with btn_col2:
                if st.button("+ Add Testcase", key=f"ctl_add_btn_{p_id}"):
                    test_items.append({"input": "", "expected_output": ""})
                    st.session_state[custom_tests_key] = test_items
                    st.rerun()

            # Display custom test results if available
            ctl_res = st.session_state.get(f"ctl_results_{p_id}")
            if ctl_res:
                c_verdict = ctl_res.get("verdict", "")
                c_passed = ctl_res.get("passed_tests", 0)
                c_total = ctl_res.get("total_tests", 0)
                c_color = "#10B981" if c_verdict.lower() == "accepted" else "#EF4444"

                st.markdown(
                    f"""
                    <div style="background: #0B111D; border-left: 4px solid {c_color}; border-radius: 6px; padding: 10px 14px; margin-top: 14px;">
                        <span style="font-weight: 700; color: {c_color}; font-size: 0.95rem;">VERDICT: {c_verdict.upper()}</span>
                        <span style="color: #94A3B8; margin-left: 12px; font-size: 0.85rem;">Passed {c_passed} / {c_total} custom tests</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                for t_item in ctl_res.get("tests", []):
                    t_idx = t_item.get("test_index", 0) + 1
                    t_v = t_item.get("verdict", "")
                    with st.expander(f"Result #{t_idx} — {t_v.upper()}"):
                        st.markdown(f"**Actual:** `{t_item.get('actual_output')}`")
                        st.markdown(f"**Expected:** `{t_item.get('expected_output')}`")

        # Tab 4: AI Debug Assistant
        # Tab 4: AI Debug Assistant
        with tab_ai:

            st.markdown("### 🤖 TraceBack AI Mentor")
            st.caption("Intelligent programming assistance powered by Google Gemini.")

            # -------------------------------------------------
            # 1. Assistance Mode Selection
            # -------------------------------------------------

            mode_options = {
                "Explain Error": "explain_error",
                "Give Me a Hint": "hint",
                "Explain Algorithm": "explain_algorithm",
                "Find the Bug": "find_bug",
                "Show Corrected Code": "corrected_code",
            }

            selected_mode = st.selectbox(
                "How would you like AI to help?",
                options=list(mode_options.keys()),
                key=f"ai_help_mode_label_{p_id}",
            )

            help_mode = mode_options[selected_mode]

            mode_descriptions = {
                "explain_error": "Understand why your program failed.",
                "hint": "Get clues without revealing the complete solution.",
                "explain_algorithm": "Learn the correct algorithm step by step.",
                "find_bug": "Identify the problematic code and logic.",
                "corrected_code": "Receive a complete corrected Python program.",
            }

            st.info(mode_descriptions[help_mode])

            # -------------------------------------------------
            # 2. Collect Latest Execution Context
            # -------------------------------------------------

            failure_type = "unknown"
            error_message = None
            ai_stdout = ""
            ai_stderr = ""
            ai_stdin = current_stdin
            expected_output = None

            last_action = st.session_state.get("last_action")

            run_res = st.session_state.get(run_result_key)
            submit_res = st.session_state.get(submit_result_key)

            # Context from Submit
            if last_action == "submit" and submit_res:

                verdict = str(
                    submit_res.get("verdict", "")
                ).lower()

                tests_list = submit_res.get("tests", [])

                failed_test = next(
                    (
                        test for test in tests_list
                        if str(test.get("verdict", "")).lower()
                        != "accepted"
                    ),
                    None,
                )

                if failed_test:

                    test_verdict = str(
                        failed_test.get("verdict", "")
                    ).lower()

                    if "runtime" in test_verdict:
                        failure_type = "runtime_error"

                    elif "time_limit" in test_verdict or "tle" in test_verdict:
                        failure_type = "time_limit_exceeded"

                    elif "compil" in test_verdict:
                        failure_type = "compilation_error"

                    else:
                        failure_type = "wrong_answer"

                    ai_stdin = failed_test.get("input", "")
                    ai_stdout = failed_test.get("actual_output") or ""
                    ai_stderr = failed_test.get("error") or ""
                    expected_output = failed_test.get("expected_output")

                    error_message = (
                        f"Submission verdict: {verdict}. "
                        f"Test case verdict: {test_verdict}."
                    )

            # Context from Run Code
            elif last_action == "run" and run_res:

                ai_stdout = run_res.get("stdout", "") or ""
                ai_stderr = run_res.get("stderr", "") or ""

                error_message = (
                    run_res.get("error")
                    or run_res.get("status")
                )

                combined_error = ai_stderr.lower()

                if "syntaxerror" in combined_error or "indentationerror" in combined_error:
                    failure_type = "syntax_error"

                elif "timeout" in combined_error:
                    failure_type = "time_limit_exceeded"

                elif ai_stderr:
                    failure_type = "runtime_error"

            # -------------------------------------------------
            # 3. Show Available Context
            # -------------------------------------------------

            if failure_type != "unknown":
                st.caption(
                    f"Detected execution issue: "
                    f"{failure_type.replace('_', ' ').title()}"
                )
            else:
                st.caption(
                    "You can also ask AI to review your current code "
                    "without an execution error."
                )

            # -------------------------------------------------
            # 4. Analyze Button
            # -------------------------------------------------

            if st.button(
                "🤖 Analyze Current Code with AI",
                key=f"ai_manual_req_{p_id}",
                type="primary",
                use_container_width=True,
            ):

                if not current_source.strip():
                    st.warning("Please write some code before requesting AI assistance.")

                else:
                    with st.spinner(
                        f"TraceBack AI Mentor is preparing: {selected_mode}..."
                    ):

                        ai_res, ai_err = api_client.request_ai_debug(
                            problem_title=title,
                            problem_description=description,
                            source_code=current_source,
                            error_message=error_message,
                            stdout=ai_stdout,
                            stderr=ai_stderr,
                            stdin=ai_stdin,
                            language="python",
                            help_mode=help_mode,
                            failure_type=failure_type,
                            expected_output=expected_output,
                        )

                        if ai_err:
                            st.session_state[ai_debug_key] = {
                                "status": "error",
                                "help_mode": help_mode,
                                "explanation": ai_err,
                            }
                        else:
                            st.session_state[ai_debug_key] = ai_res

                        st.rerun()

            st.markdown("---")

            # -------------------------------------------------
            # 5. Display AI Diagnosis
            # -------------------------------------------------

            ai_data = st.session_state.get(ai_debug_key)

            # Don't display an old response for another mode
            if ai_data and ai_data.get("help_mode", "find_bug") != help_mode:
                st.info(
                    "You've selected a different assistance mode. "
                    "Click Analyze Current Code with AI to generate a new response."
                )
                ai_data = None

            if ai_data:

                ai_status = ai_data.get("status", "success")

                expl = ai_data.get("explanation", "")
                cause = ai_data.get("likely_cause", "")
                code_loc = ai_data.get("responsible_code", "")
                fix = ai_data.get("suggested_fix", "")
                corr = ai_data.get("corrected_code")
                is_mock = ai_data.get("is_mock", False)

                if ai_status == "unconfigured":

                    st.warning(
                        "Gemini API is not configured yet. "
                        "Add your API key to the backend .env file "
                        "to enable live AI debugging."
                    )

                    st.info(expl)

                    st.write("**Configuration guidance:**")
                    st.write(fix)

                elif ai_status == "error":

                    st.error(expl)

                    if fix:
                        st.write(f"Suggestion: {fix}")

                else:

                    if is_mock:
                        st.info("Simulated AI response — Gemini API is not connected yet.")
                    else:
                        st.success("Gemini AI analysis completed successfully.")

                    st.markdown("### 💡 Explanation")
                    st.write(expl)

                    st.markdown("### 🔍 Likely Root Cause")
                    st.write(cause)

                    st.markdown("### 📍 Responsible Code")
                    st.write(code_loc)

                    st.markdown("### 🛠️ Suggested Fix")
                    st.write(fix)

                    if corr:
                        st.markdown("### ✅ Corrected Code")
                        st.code(corr, language="python")

                if st.button(
                    "🔄 Clear Diagnosis",
                    key=f"ai_clear_{p_id}",
                ):
                    st.session_state[ai_debug_key] = None
                    st.rerun()
