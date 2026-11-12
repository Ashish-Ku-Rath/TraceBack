"""
Polished Coming Soon placeholder view for future TraceBack platform modules.
"""

import streamlit as st

MODULE_INFO = {
    "workspace": {
        "title": "Interactive Monaco Code Workspace",
        "icon": "💻",
        "milestone": "Day 5 — Code Editor & Execution Lab",
        "desc": (
            "The in-browser Monaco code editor with syntax highlighting, indentation, "
            "and live sandboxed execution against custom test cases will be integrated in Day 5."
        ),
    },
    "ai_assistant": {
        "title": "AI Debugging & AST Reasoning",
        "icon": "✨",
        "milestone": "Day 6 — Gemini AI Integration",
        "desc": (
            "Google Gemini API integration with Python AST static analysis to diagnose "
            "logic flaws, runtime errors, and off-by-one edge cases without revealing the full answer."
        ),
    },
    "submissions": {
        "title": "Submission History & Benchmarks",
        "icon": "📋",
        "milestone": "Day 7 — Submissions & Tracking",
        "desc": (
            "Complete submission archives, historical runtimes, memory charts, "
            "and pass/fail verification across all solved problems."
        ),
    },
    "progress": {
        "title": "DSA Mastery & Progress Analytics",
        "icon": "📈",
        "milestone": "Day 8 — Analytics & Profiles",
        "desc": (
            "Radar charts covering algorithm categories (Arrays, Dynamic Programming, Graphs), "
            "solving streaks, and mastery progression levels."
        ),
    },
    "profile": {
        "title": "Developer Profile & Credentials",
        "icon": "👤",
        "milestone": "Day 8 — User Management",
        "desc": (
            "Personalized developer profile, solved challenge badges, and settings."
        ),
    },
}


def render_coming_soon_page(module_key: str):
    """Render a polished preview banner for upcoming platform features."""
    info = MODULE_INFO.get(
        module_key,
        {
            "title": "Coming Soon",
            "icon": "⏳",
            "milestone": "Upcoming Milestone",
            "desc": "This platform module is currently under development according to our engineering roadmap.",
        },
    )

    st.markdown(
        f"""
        <div class="tb-card" style="text-align: center; padding: 60px 30px; margin-top: 20px;">
            <div style="font-size: 3.5rem; margin-bottom: 16px;">{info['icon']}</div>
            <div style="display: inline-block; padding: 4px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; background: rgba(139, 92, 246, 0.15); color: #DDD6FE; border: 1px solid rgba(139, 92, 246, 0.35); margin-bottom: 14px;">
                {info['milestone']}
            </div>
            <h1 style="font-size: 2rem; font-weight: 800; margin: 0 0 14px 0; color: #F8FAFC;">
                {info['title']}
            </h1>
            <p style="font-size: 1.05rem; color: #94A3B8; max-width: 580px; margin: 0 auto 28px auto; line-height: 1.6;">
                {info['desc']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col2:
        if st.button("← Return to Dashboard", type="primary", use_container_width=True):
            st.session_state["current_page"] = "dashboard"
            st.rerun()

