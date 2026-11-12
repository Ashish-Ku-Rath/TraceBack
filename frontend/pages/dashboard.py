"""
Dashboard view for TraceBack.
Implements the revised emerald & dark charcoal design system.
Follows the exact visual hierarchy:
- Header & live backend status
- Welcome section with "Explore Problems" primary action
- 4 Genuine KPI metric cards
- Two-column main layout (Left: Continue Practising + Recent Activity; Right: Difficulty Breakdown + Quick Shortcuts + Platform Info)
"""

import textwrap
import streamlit as st
from frontend.api_client import api_client
from frontend.components.cards import (
    render_backend_offline_alert,
    render_difficulty_breakdown,
    render_empty_activity,
    render_platform_info,
    render_stat_card,
)
from frontend.components.problem_card import render_problem_recommendation_card


def render_dashboard_page():
    """Render the revised TraceBack platform dashboard."""
    # A. Header
    header_html = """
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 1.85rem; font-weight: 700; color: #F5F7FA; margin: 0 0 6px 0;">Dashboard</h1>
        <p style="font-size: 0.92rem; color: #94A3B8; margin: 0;">System overview, problem statistics, and personal practice progress.</p>
    </div>
    """
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # Fetch live backend statistics
    stats, error = api_client.get_statistics()
    if error:
        render_backend_offline_alert(error)

    # B. Welcome section
    hero_html = """
    <div class="tb-hero-card">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0 0 8px 0; color: #F5F7FA;">
            Welcome to TraceBack
        </h2>
        <p style="font-size: 0.95rem; color: #94A3B8; margin: 0; max-width: 680px; line-height: 1.5;">
            Your space to practise, debug and improve your coding skills.
        </p>
    </div>
    """
    st.markdown(textwrap.dedent(hero_html).strip(), unsafe_allow_html=True)

    btn_col, _ = st.columns([2, 5])
    with btn_col:
        if st.button("Explore Problems  →", type="primary", use_container_width=True):
            st.session_state["current_page"] = "problems"
            st.session_state["selected_problem_id"] = None
            st.session_state["filter_difficulty"] = "All"
            st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # C. Statistics (Genuine backend-derived statistics)
    total_val = stats.get("total", 0)
    easy_val = stats.get("easy", 0)
    med_val = stats.get("medium", 0)
    hard_val = stats.get("hard", 0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            render_stat_card(
                label="Total Problems",
                value=total_val,
                desc="Curated challenges in database",
                border_color="#34D399",
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_stat_card(
                label="Easy Problems",
                value=easy_val,
                desc="Beginner friendly & warmups",
                border_color="#10B981",
            ),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            render_stat_card(
                label="Medium Problems",
                value=med_val,
                desc="Algorithmic core logic",
                border_color="#F59E0B",
            ),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            render_stat_card(
                label="Hard Problems",
                value=hard_val,
                desc="Advanced data structures",
                border_color="#EF4444",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # D. Main content structure: Two-column layout
    left_col, right_col = st.columns([1.65, 1.0])

    with left_col:
        # Continue Practising section
        section_html = """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="font-size: 1.15rem; font-weight: 600; color: #F5F7FA; margin: 0;">Continue Practising</h3>
            <span style="font-size: 0.78rem; color: #34D399; font-weight: 600;">Available Now</span>
        </div>
        """
        st.markdown(textwrap.dedent(section_html).strip(), unsafe_allow_html=True)

        problems, total, prob_err = api_client.get_problems(skip=0, limit=5)
        if prob_err:
            st.error(prob_err)
        elif not problems:
            empty_html = """
            <div class="tb-empty-state">
                <div>No problems available in the database yet.</div>
                <div style="font-size: 0.8rem; margin-top: 6px;">Run <code>python -m database.seed</code> to populate initial problems.</div>
            </div>
            """
            st.markdown(textwrap.dedent(empty_html).strip(), unsafe_allow_html=True)
        else:
            for p in problems:
                render_problem_recommendation_card(p, key_prefix="dash")

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # Recent Activity section
        render_empty_activity()

    with right_col:
        # Right 1: Problem Difficulty Breakdown
        render_difficulty_breakdown(
            easy=easy_val,
            medium=med_val,
            hard=hard_val,
            total=total_val,
        )

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Right 2: Quick Practice Shortcuts
        shortcuts_html = """
        <div class="tb-card" style="padding-bottom: 14px;">
            <h3 style="font-size: 1.0rem; font-weight: 600; margin-top: 0; margin-bottom: 12px; color: #F5F7FA;">
                ⚡ Quick Practice Shortcuts
            </h3>
            <p style="font-size: 0.82rem; color: #94A3B8; margin: 0 0 12px 0;">Jump directly into filtered challenge sets:</p>
        </div>
        """
        st.markdown(textwrap.dedent(shortcuts_html).strip(), unsafe_allow_html=True)

        qc1, qc2 = st.columns(2)
        with qc1:
            if st.button("🟢 Easy Sets", use_container_width=True, key="qc_easy"):
                st.session_state["filter_difficulty"] = "Easy"
                st.session_state["current_page"] = "problems"
                st.session_state["selected_problem_id"] = None
                st.rerun()
            if st.button("🏷️ Arrays", use_container_width=True, key="qc_arrays"):
                st.session_state["filter_tag"] = "Array"
                st.session_state["current_page"] = "problems"
                st.session_state["selected_problem_id"] = None
                st.rerun()

        with qc2:
            if st.button("🟡 Medium Sets", use_container_width=True, key="qc_medium"):
                st.session_state["filter_difficulty"] = "Medium"
                st.session_state["current_page"] = "problems"
                st.session_state["selected_problem_id"] = None
                st.rerun()
            if st.button("🏷️ Strings", use_container_width=True, key="qc_strings"):
                st.session_state["filter_tag"] = "String"
                st.session_state["current_page"] = "problems"
                st.session_state["selected_problem_id"] = None
                st.rerun()

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Right 3: Platform Information
        render_platform_info()
