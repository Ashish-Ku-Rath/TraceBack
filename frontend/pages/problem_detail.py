"""
Problem Detail view for TraceBack.
Implements the distraction-free black-and-white reading panel design rule:
- Background: #090B0F
- Main text: #F8FAFC, Secondary text: #CBD5E1
- Problem title & Section headings (Problem Description, Examples, Constraints): White (#FFFFFF)
- Topic tags: Navy blue badges (#1E3A5F, border #1D4ED8)
- Difficulty badges: Green (Easy), Amber (Medium), Red (Hard)
- Code examples: Black background (#000000) with readable syntax highlighting
- Zero markdown indentation bugs via clean_html line-stripping
"""

import html
from typing import Optional
import streamlit as st
from frontend.api_client import api_client
from frontend.components.cards import render_backend_offline_alert
from frontend.components.problem_card import (
    get_difficulty_badge_html,
    get_tags_html,
)


def clean_html(raw_html: str) -> str:
    """
    Strip leading and trailing whitespace from each line.
    Guarantees no line starts with 4+ spaces, preventing Markdown from
    falsely interpreting HTML fragments as indented code blocks.
    """
    return "\n".join(line.strip() for line in raw_html.splitlines() if line.strip())


def render_problem_detail_page(problem_id: Optional[int] = None):
    """Render the full single problem detail view."""
    # Top Action Bar with Back button and Workspace launcher
    top_bar_col, action_col = st.columns([6, 2])
    with top_bar_col:
        if st.button("←  Back to Problems", key="back_to_problems_btn", type="secondary"):
            st.session_state["current_page"] = "problems"
            st.session_state["selected_problem_id"] = None
            st.rerun()

    # Determine ID to fetch
    target_id = problem_id or st.session_state.get("selected_problem_id", 1)

    with action_col:
        if st.button("🚀  Open Workspace", key="open_workspace_btn", type="primary", use_container_width=True):
            st.session_state["selected_problem_id"] = target_id
            st.session_state["current_page"] = "workspace"
            st.rerun()

    # Fetch problem details from backend
    problem, error = api_client.get_problem_by_id(target_id)

    if error:
        render_backend_offline_alert(error)
        return

    if not problem:
        st.error(f"Problem #{target_id} could not be found.")
        return

    title = problem.get("title", "Untitled Problem")
    slug = problem.get("slug", "")
    difficulty = problem.get("difficulty", "Easy")
    description = problem.get("description", "")
    constraints = problem.get("constraints", "")
    tags = problem.get("tags", [])
    examples = problem.get("examples", [])

    # Main Two-Column Layout
    col_content, col_meta = st.columns([2.6, 1.0])

    with col_content:
        # Build description paragraphs HTML
        paragraphs = [p.strip() for p in description.split("\n\n") if p.strip()]
        desc_paragraphs_html = "".join(
            f"<p style='margin: 0 0 14px 0; line-height: 1.65; color: #F8FAFC; font-size: 0.95rem;'>{html.escape(p)}</p>"
            for p in paragraphs
        ) if paragraphs else f"<p style='color: #F8FAFC; font-size: 0.95rem;'>{html.escape(description)}</p>"

        # Build examples HTML
        examples_html_list = []
        if not examples:
            examples_html_list.append(
                "<div style='color: #CBD5E1; font-size: 0.88rem; font-style: italic;'>No sample test cases configured.</div>"
            )
        else:
            for idx, ex in enumerate(examples, start=1):
                input_str = ex.get("input", "")
                output_str = ex.get("expected_output", "")
                explanation = ex.get("explanation")

                explanation_html = (
                    f"<div style='margin-top: 8px; font-size: 0.86rem; color: #CBD5E1; line-height: 1.5;'>"
                    f"<strong style='color: #F8FAFC;'>Explanation: </strong>{html.escape(explanation)}"
                    f"</div>"
                    if explanation
                    else ""
                )

                ex_box = f"""
                <div style="margin-bottom: 18px;">
                    <div style="font-size: 0.88rem; font-weight: 600; color: #FFFFFF; margin-bottom: 6px;">
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

        # Build constraints HTML
        lines = [c.strip() for c in constraints.split("\n") if c.strip()]
        if lines:
            c_items = "".join(
                f"<li style='margin-bottom: 6px;'>"
                f"<code style='background: #000000; color: #E2E8F0; padding: 2px 7px; border-radius: 4px; border: 1px solid #1E293B; font-family: monospace; font-size: 0.85rem;'>"
                f"{html.escape(line)}"
                f"</code>"
                f"</li>"
                for line in lines
            )
            constraints_html = f"<ul style='padding-left: 20px; margin: 0; font-size: 0.88rem; color: #CBD5E1; line-height: 1.6;'>{c_items}</ul>"
        else:
            constraints_html = "<div style='color: #CBD5E1; font-size: 0.88rem;'>Standard algorithmic constraints apply.</div>"

        # Complete Left-side Problem Description Panel (Clean Black & White Reading Experience)
        panel_html = f"""
        <div class="tb-problem-panel">
            <div style="margin-bottom: 16px;">
                <div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 8px;">
                    <span style="font-size: 1.35rem; font-weight: 700; color: #CBD5E1;">#{problem.get('id')}</span>
                    <h1 style="font-size: 1.85rem; font-weight: 700; margin: 0; color: #FFFFFF; display: inline;">{title}</h1>
                </div>
                <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                    {get_difficulty_badge_html(difficulty)}
                    <span style="color: #334155;">|</span>
                    <div>{get_tags_html(tags)}</div>
                </div>
            </div>

            <hr style="border: none; border-top: 1px solid #1E293B; margin: 18px 0 20px 0;">

            <div class="tb-panel-heading">Problem Description</div>
            <div style="margin-bottom: 24px;">
                {desc_paragraphs_html}
            </div>

            <div class="tb-panel-heading">Examples</div>
            <div style="margin-bottom: 24px;">
                {rendered_examples}
            </div>

            <div class="tb-panel-heading">Constraints</div>
            <div>
                {constraints_html}
            </div>
        </div>
        """
        st.markdown(clean_html(panel_html), unsafe_allow_html=True)

    with col_meta:
        # Problem Metadata Panel
        meta_html = f"""
        <div class="tb-card">
            <div style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; color: #FFFFFF; letter-spacing: 0.06em; margin-bottom: 14px;">
                Problem Details
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.82rem;">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #1E293B; padding-bottom: 8px;">
                    <span style="color: #CBD5E1;">ID</span>
                    <span style="color: #F8FAFC; font-weight: 600;">#{problem.get('id')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #1E293B; padding-bottom: 8px;">
                    <span style="color: #CBD5E1;">Slug</span>
                    <code style="background: #000000; color: #93C5FD; padding: 2px 6px; border-radius: 4px; border: 1px solid #1E293B;">{slug}</code>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #1E293B; padding-bottom: 8px;">
                    <span style="color: #CBD5E1;">Difficulty</span>
                    <span style="font-weight: 600;">{difficulty}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #CBD5E1;">Judging</span>
                    <span style="color: #34D399; font-weight: 600;">Sandboxed</span>
                </div>
            </div>
        </div>
        """
        st.markdown(clean_html(meta_html), unsafe_allow_html=True)
