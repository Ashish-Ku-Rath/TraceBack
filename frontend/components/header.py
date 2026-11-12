"""
Top navigation bar component for TraceBack.
Displays breadcrumbs and live backend connectivity status.
"""

import streamlit as st
from frontend.api_client import api_client


def render_header(breadcrumb_title: str = "Dashboard") -> bool:
    """
    Render top navigation bar with live backend status indicator.
    Returns:
        bool: True if backend is healthy, False otherwise.
    """
    # Probe backend health
    is_connected = api_client.check_health()
    st.session_state["backend_connected"] = is_connected

    status_pill_html = (
        '<div class="tb-status-pill tb-status-connected">'
        '<span class="tb-pulse-dot tb-pulse-green"></span>'
        '<span>API Online</span>'
        '</div>'
        if is_connected
        else '<div class="tb-status-pill tb-status-disconnected">'
        '<span class="tb-pulse-dot tb-pulse-red"></span>'
        '<span>API Offline</span>'
        '</div>'
    )

    topbar_html = (
        '<div class="tb-topbar">'
        '<div class="tb-breadcrumb">'
        '<span style="color: #34D399; font-size: 1.0rem;">⚡</span>'
        '<span style="color: #94A3B8;">TraceBack</span>'
        '<span style="color: #26332F;">/</span>'
        f'<span style="color: #F5F7FA; font-weight: 600;">{breadcrumb_title}</span>'
        '</div>'
        f'<div style="display: flex; align-items: center; gap: 12px;">{status_pill_html}</div>'
        '</div>'
    )
    st.markdown(topbar_html, unsafe_allow_html=True)
    return is_connected
