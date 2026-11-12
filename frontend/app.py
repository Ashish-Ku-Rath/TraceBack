"""
TraceBack — The Intelligent Coding & Debugging Assistant
Streamlit Frontend Application Entrypoint.
"""

import streamlit as st
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.pages.dashboard import render_dashboard_page
from frontend.pages.problem_detail import render_problem_detail_page
from frontend.pages.problems import render_problems_page
from frontend.pages.workspace import render_workspace_page
from frontend.styles import apply_custom_css

# Configure main browser window & layout
st.set_page_config(
    page_title="TraceBack — The Intelligent Coding & Debugging Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize global session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "dashboard"
if "selected_problem_id" not in st.session_state:
    st.session_state["selected_problem_id"] = None
if "backend_connected" not in st.session_state:
    st.session_state["backend_connected"] = False

# Inject custom design system stylesheet
apply_custom_css()

# Render minimal dark sidebar navigation
active_page = render_sidebar()

# Page title mapping for header breadcrumbs
BREADCRUMB_MAP = {
    "dashboard": "Dashboard",
    "problems": "Problem Library",
    "workspace": "Coding Workspace",
    "problem_detail": "Problem Details",
}

breadcrumb_title = BREADCRUMB_MAP.get(active_page, "Dashboard")

# Render top header bar with live API connection indicator
render_header(breadcrumb_title=breadcrumb_title)

# Route to active page controller
if active_page == "dashboard":
    render_dashboard_page()
elif active_page == "problems":
    render_problems_page()
elif active_page == "workspace":
    render_workspace_page(problem_id=st.session_state.get("selected_problem_id"))
elif active_page == "problem_detail":
    render_problem_detail_page(problem_id=st.session_state.get("selected_problem_id"))
else:
    st.session_state["current_page"] = "dashboard"
    render_dashboard_page()
