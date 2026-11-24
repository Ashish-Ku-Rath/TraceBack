"""
Problem Library page for TraceBack.
Provides searching, difficulty filtering, topic filtering, and problem listing.
Directly communicates with FastAPI GET /problems endpoint.
"""

from typing import List
import streamlit as st
from frontend.api_client import api_client
from frontend.components.cards import render_backend_offline_alert
from frontend.components.problem_card import (
    get_difficulty_badge_html,
    get_tags_html,
)

AVAILABLE_TAGS = ["All", "Array", "Basic Programming", "Hash Map", "Math", "Stack", "String", "Two Pointers"]
DIFFICULTY_OPTIONS = ["All", "Easy", "Medium", "Hard"]


def render_problems_page():
    """Render the full DSA Problem Library view."""
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h1 style="font-size: 1.85rem; font-weight: 700; margin: 0 0 6px 0; color: #F5F7FA;">Problem Library</h1>
            <p style="font-size: 0.92rem; color: #94A3B8; margin: 0;">
                Practice DSA, strengthen your algorithmic logic, and become a better problem solver.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initial selection from session state if set by quick practice shortcuts
    default_diff = st.session_state.get("filter_difficulty", "All")
    diff_index = DIFFICULTY_OPTIONS.index(default_diff) if default_diff in DIFFICULTY_OPTIONS else 0

    default_tag = st.session_state.get("filter_tag", "All")
    tag_index = AVAILABLE_TAGS.index(default_tag) if default_tag in AVAILABLE_TAGS else 0

    # Filter Controls Bar
    filter_col1, filter_col2, filter_col3 = st.columns([2.2, 1.2, 1.4])

    with filter_col1:
        search_query = st.text_input(
            "Search Problems",
            placeholder="Search by problem title (e.g. Two Sum, String)...",
            label_visibility="collapsed",
            key="library_search_input",
        )

    with filter_col2:
        selected_difficulty = st.selectbox(
            "Difficulty",
            options=DIFFICULTY_OPTIONS,
            index=diff_index,
            label_visibility="collapsed",
            key="library_diff_select",
        )

    with filter_col3:
        selected_tag = st.selectbox(
            "Topic Tag",
            options=AVAILABLE_TAGS,
            index=tag_index,
            label_visibility="collapsed",
            key="library_tag_select",
        )

    # Clear pre-selected filter state after reading
    if "filter_difficulty" in st.session_state:
        st.session_state["filter_difficulty"] = selected_difficulty
    if "filter_tag" in st.session_state:
        st.session_state["filter_tag"] = selected_tag

    # Fetch problems matching criteria from backend
    problems, total_count, error = api_client.get_problems(
        skip=0,
        limit=100,
        difficulty=selected_difficulty,
        tag=selected_tag,
        search=search_query,
    )

    if error:
        render_backend_offline_alert(error)
        return

    # Count indicator bar
    active_filters: List[str] = []
    if search_query:
        active_filters.append(f'Search: "{search_query}"')
    if selected_difficulty != "All":
        active_filters.append(f"Difficulty: {selected_difficulty}")
    if selected_tag != "All":
        active_filters.append(f"Topic: {selected_tag}")

    filters_desc = f" ({', '.join(active_filters)})" if active_filters else ""
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 18px 0 12px 0;">
            <div style="font-size: 0.86rem; font-weight: 500; color: #94A3B8;">
                Showing <span style="color: #F5F7FA; font-weight: 600;">{len(problems)}</span> of <span style="color: #34D399; font-weight: 600;">{total_count}</span> problems{filters_desc}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Empty State Check
    if not problems:
        st.markdown(
            """
            <div class="tb-empty-state" style="margin-top: 20px;">
                <div style="font-size: 2.0rem; margin-bottom: 8px;">🔍</div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #F5F7FA; margin-bottom: 4px;">No Problems Found</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">
                    No algorithmic challenges matched your current search filters. Try clearing your search keyword or switching difficulty/tags.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Table Header
    header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns([0.6, 3.2, 1.2, 2.4, 1.2])
    with header_col1:
        st.markdown("<span style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>ID</span>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("<span style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>Title</span>", unsafe_allow_html=True)
    with header_col3:
        st.markdown("<span style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>Difficulty</span>", unsafe_allow_html=True)
    with header_col4:
        st.markdown("<span style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>Topics</span>", unsafe_allow_html=True)
    with header_col5:
        st.markdown("<span style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>Action</span>", unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #26332F; margin: 4px 0 10px 0;'>", unsafe_allow_html=True)

    # Problem Rows
    for p in problems:
        p_id = p.get("id")
        title = p.get("title", "Untitled")
        difficulty = p.get("difficulty", "Easy")
        tags = p.get("tags", [])

        r_col1, r_col2, r_col3, r_col4, r_col5 = st.columns([0.6, 3.2, 1.2, 2.4, 1.2])

        with r_col1:
            st.markdown(f"<div style='padding-top: 8px; font-weight: 600; color: #94A3B8; font-size: 0.88rem;'>#{p_id}</div>", unsafe_allow_html=True)

        with r_col2:
            st.markdown(f"<div style='padding-top: 8px; font-weight: 600; color: #F5F7FA; font-size: 0.95rem;'>{title}</div>", unsafe_allow_html=True)

        with r_col3:
            st.markdown(f"<div style='padding-top: 6px;'>{get_difficulty_badge_html(difficulty)}</div>", unsafe_allow_html=True)

        with r_col4:
            st.markdown(f"<div style='padding-top: 6px;'>{get_tags_html(tags)}</div>", unsafe_allow_html=True)

        with r_col5:
            if st.button("Solve  →", key=f"lib_solve_{p_id}", type="primary", use_container_width=True):
                st.session_state["selected_problem_id"] = p_id
                st.session_state["current_page"] = "workspace"
                st.rerun()

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(38, 51, 47, 0.6); margin: 6px 0 6px 0;'>", unsafe_allow_html=True)
