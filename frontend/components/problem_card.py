"""
Problem presentation components for cards and table listings.
Renders difficulty badges, topic tags, and action buttons.
"""

import textwrap
from typing import Any, Dict, List
import streamlit as st


def get_difficulty_badge_html(difficulty: str) -> str:
    """Return styled HTML badge for problem difficulty level."""
    diff_lower = (difficulty or "Easy").strip().lower()
    if diff_lower == "easy":
        return '<span class="tb-badge tb-badge-easy">Easy</span>'
    elif diff_lower == "medium":
        return '<span class="tb-badge tb-badge-medium">Medium</span>'
    elif diff_lower == "hard":
        return '<span class="tb-badge tb-badge-hard">Hard</span>'
    return f'<span class="tb-badge tb-badge-medium">{difficulty}</span>'


def get_tags_html(tags: List[str]) -> str:
    """Return styled HTML tags pills for problem categories."""
    if not tags:
        return '<span style="color: #94A3B8; font-size: 0.78rem;">General</span>'
    pills = [f'<span class="tb-tag">{tag}</span>' for tag in tags[:4]]
    if len(tags) > 4:
        pills.append(f'<span class="tb-tag">+{len(tags) - 4}</span>')
    return "".join(pills)


def render_problem_recommendation_card(problem: Dict[str, Any], key_prefix: str = "rec"):
    """Render an individual problem card on the dashboard or list."""
    p_id = problem.get("id")
    title = problem.get("title", "Untitled Problem")
    difficulty = problem.get("difficulty", "Easy")
    tags = problem.get("tags", [])

    badge_html = get_difficulty_badge_html(difficulty)
    tags_html = get_tags_html(tags)

    card_col, btn_col = st.columns([4, 1.2])

    with card_col:
        card_html = f"""
        <div style="background: #121A18; border: 1px solid #26332F; border-radius: 10px; padding: 14px 18px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-weight: 700; color: #94A3B8; font-size: 0.85rem;">#{p_id}</span>
                    <span style="font-weight: 600; color: #F5F7FA; font-size: 0.98rem;">{title}</span>
                </div>
                {badge_html}
            </div>
            <div>{tags_html}</div>
        </div>
        """
        st.markdown(textwrap.dedent(card_html).strip(), unsafe_allow_html=True)

    with btn_col:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Solve  →", key=f"{key_prefix}_solve_{p_id}", type="primary", use_container_width=True):
            st.session_state["selected_problem_id"] = p_id
            st.session_state["current_page"] = "workspace"
            st.rerun()
