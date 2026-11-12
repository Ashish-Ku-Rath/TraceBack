"""
Sidebar navigation component for TraceBack.
Displays brand logo, minimal navigation menu, and platform version.
"""

import streamlit as st
from frontend.config import LOGO_HTML, TAGLINE

# Minimal navigation: only live implemented features
NAV_ITEMS = [
    ("Dashboard", "dashboard", "📊"),
    ("Problems", "problems", "🧩"),
]


def render_sidebar() -> str:
    """
    Render the minimal dark sidebar with active navigation items.
    Returns the selected page identifier.
    """
    with st.sidebar:
        # Brand Logo and Tagline
        st.markdown(LOGO_HTML, unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size: 0.72rem; color: #94A3B8; margin-top: 4px; margin-bottom: 24px; font-weight: 500; line-height: 1.3;'>{TAGLINE}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='border: none; border-top: 1px solid #26332F; margin: 0 0 16px 0;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.08em; margin-bottom: 8px;'>Platform</div>", unsafe_allow_html=True)

        current_page = st.session_state.get("current_page", "dashboard")

        # Render navigation options
        for label, page_key, icon in NAV_ITEMS:
            is_active = (current_page == page_key) or (current_page in ("problem_detail", "workspace") and page_key == "problems")
            btn_label = f"{icon}  {label}"

            if is_active:
                st.button(
                    btn_label,
                    key=f"nav_{page_key}",
                    type="primary",
                    use_container_width=True,
                )
            else:
                if st.button(
                    btn_label,
                    key=f"nav_{page_key}",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.session_state["current_page"] = page_key
                    if page_key != "problems":
                        st.session_state["selected_problem_id"] = None
                    st.rerun()

        st.markdown("<div style='flex-grow: 1; min-height: 200px;'></div>", unsafe_allow_html=True)
        st.markdown("<hr style='border: none; border-top: 1px solid #26332F; margin: 24px 0 12px 0;'>", unsafe_allow_html=True)

        # Bottom System Info
        st.markdown(
            """
            <div style="font-size: 0.72rem; color: #94A3B8; display: flex; justify-content: space-between; align-items: center;">
                <span>TraceBack v0.5.0</span>
                <span style="color: #34D399; font-weight: 600;">Day 5 Workspace</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.get("current_page", "dashboard")
