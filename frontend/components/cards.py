"""
Card and widget UI components for TraceBack frontend.
Includes statistics cards, difficulty breakdown, activity feed, and alerts.
Uses textwrap.dedent to ensure Markdown does not misinterpret indented HTML as code blocks.
"""

import textwrap
import streamlit as st


def render_stat_card(label: str, value: str | int, desc: str = "", border_color: str = "#26332F") -> str:
    """Generate HTML markup for a KPI metric card."""
    html = f"""
    <div class="tb-stat-card" style="border-top: 3px solid {border_color};">
        <div>
            <div class="tb-stat-label">{label}</div>
            <div class="tb-stat-value">{value}</div>
        </div>
        <div class="tb-stat-desc">{desc}</div>
    </div>
    """
    return textwrap.dedent(html).strip()


def render_difficulty_breakdown(easy: int, medium: int, hard: int, total: int):
    """Render difficulty distribution progress bars with genuine statistics."""
    easy_pct = (easy / total * 100) if total > 0 else 0
    med_pct = (medium / total * 100) if total > 0 else 0
    hard_pct = (hard / total * 100) if total > 0 else 0

    html = f"""
    <div class="tb-card">
        <h3 style="font-size: 1.0rem; font-weight: 600; margin-top: 0; margin-bottom: 16px; color: #F5F7FA;">
            📊 Difficulty Breakdown
        </h3>
        <div style="display: flex; flex-direction: column; gap: 14px;">
            <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 6px;">
                    <span style="color: #34D399; font-weight: 600;">Easy</span>
                    <span style="color: #94A3B8;">{easy} ({easy_pct:.0f}%)</span>
                </div>
                <div class="tb-progress-container">
                    <div class="tb-progress-bar tb-bar-easy" style="width: {easy_pct}%;"></div>
                </div>
            </div>
            <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 6px;">
                    <span style="color: #F59E0B; font-weight: 600;">Medium</span>
                    <span style="color: #94A3B8;">{medium} ({med_pct:.0f}%)</span>
                </div>
                <div class="tb-progress-container">
                    <div class="tb-progress-bar tb-bar-medium" style="width: {med_pct}%;"></div>
                </div>
            </div>
            <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 6px;">
                    <span style="color: #EF4444; font-weight: 600;">Hard</span>
                    <span style="color: #94A3B8;">{hard} ({hard_pct:.0f}%)</span>
                </div>
                <div class="tb-progress-container">
                    <div class="tb-progress-bar tb-bar-hard" style="width: {hard_pct}%;"></div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


def render_platform_info():
    """Render platform architecture and metadata panel."""
    html = """
    <div class="tb-card">
        <h3 style="font-size: 1.0rem; font-weight: 600; margin-top: 0; margin-bottom: 14px; color: #F5F7FA;">
            ℹ️ Platform Information
        </h3>
        <div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.82rem;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #18221F; padding-bottom: 8px;">
                <span style="color: #94A3B8;">Backend</span>
                <span style="color: #34D399; font-weight: 600;">FastAPI (Async)</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #18221F; padding-bottom: 8px;">
                <span style="color: #94A3B8;">Database</span>
                <span style="color: #F5F7FA; font-weight: 500;">SQLite + SQLAlchemy 2.x</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #18221F; padding-bottom: 8px;">
                <span style="color: #94A3B8;">Execution Core</span>
                <span style="color: #F5F7FA; font-weight: 500;">Provider Factory</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #94A3B8;">Frontend Tier</span>
                <span style="color: #10B981; font-weight: 600;">Streamlit Native</span>
            </div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


def render_empty_activity():
    """Render genuine empty state for user activity."""
    html = """
    <div class="tb-card" style="text-align: center; padding: 28px 20px;">
        <div style="font-size: 1.8rem; margin-bottom: 8px; opacity: 0.85;">📝</div>
        <div style="font-size: 0.95rem; font-weight: 600; color: #F5F7FA; margin-bottom: 4px;">Recent Activity</div>
        <div style="font-size: 0.84rem; color: #94A3B8; max-width: 420px; margin: 0 auto; line-height: 1.5;">
            Your coding activity will appear here once you start solving problems.
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


def render_backend_offline_alert(error_msg: str):
    """Render an alert card when backend communication fails."""
    html = f"""
    <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 18px; margin-bottom: 20px;">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <div style="font-size: 1.3rem;">⚠️</div>
            <div>
                <div style="font-weight: 600; color: #EF4444; font-size: 1.0rem; margin-bottom: 4px;">
                    Backend Server Unavailable
                </div>
                <div style="font-size: 0.85rem; color: #F5F7FA; line-height: 1.5; margin-bottom: 8px;">
                    {error_msg}
                </div>
                <div style="font-size: 0.8rem; color: #94A3B8;">
                    Start backend server:
                    <code style="background: #080B0D; color: #34D399; padding: 2px 6px; border-radius: 4px; border: 1px solid #26332F;">
                        .\\.venv\\Scripts\\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
                    </code>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)
