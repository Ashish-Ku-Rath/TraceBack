"""
Custom CSS stylesheet injection for TraceBack Streamlit UI.
Implements the revised emerald green & dark charcoal design system
(80% black/charcoal, 15% dark green/neutral surfaces, 5% accent).
"""

CUSTOM_CSS = """
<style>
/* Global resets & dark theme application */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #080B0D !important;
    color: #F5F7FA !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

/* Header bar styling */
[data-testid="stHeader"] {
    background-color: #080B0D !important;
    border-bottom: 1px solid #26332F !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0D1211 !important;
    border-right: 1px solid #26332F !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    background-color: #0D1211 !important;
    padding-top: 1.25rem !important;
}

/* Hide default streamlit decorations and multi-page sidebar navigation */
#MainMenu, footer, [data-testid="stSidebarNav"] {
    display: none !important;
    visibility: hidden !important;
}

/* Standard content area max-width & padding */
.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1400px !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: #F5F7FA !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

p, span, label, div {
    color: #F5F7FA;
}

.text-muted {
    color: #94A3B8 !important;
}

/* Modern Card Containers */
.tb-card {
    background: #121A18;
    border: 1px solid #26332F;
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    transition: border-color 0.15s ease;
}

.tb-card:hover {
    border-color: #354742;
}

.tb-card-secondary {
    background: #18221F;
    border: 1px solid #26332F;
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 12px;
}

/* Welcome Section Card */
.tb-welcome-card {
    background: #121A18;
    border: 1px solid #26332F;
    border-left: 4px solid #34D399;
    border-radius: 10px;
    padding: 24px 28px;
    margin-bottom: 20px;
}

/* Metric / Stat Card */
.tb-stat-card {
    background: #121A18;
    border: 1px solid #26332F;
    border-radius: 10px;
    padding: 18px 20px;
    text-align: left;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.tb-stat-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94A3B8;
    margin-bottom: 6px;
}

.tb-stat-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: #F5F7FA;
    line-height: 1.1;
    margin-bottom: 4px;
}

.tb-stat-desc {
    font-size: 0.78rem;
    color: #64748B;
}

/* Difficulty Badges */
.tb-badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.tb-badge-easy {
    background: rgba(16, 185, 129, 0.12);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.tb-badge-medium {
    background: rgba(245, 158, 11, 0.12);
    color: #F59E0B;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.tb-badge-hard {
    background: rgba(239, 68, 68, 0.12);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Topic Tag Pill - Navy Blue (#1E3A5F / #1D4ED8) */
.tb-tag {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 500;
    background: #1E3A5F;
    border: 1px solid #1D4ED8;
    color: #DBEAFE;
    margin-right: 5px;
    margin-bottom: 4px;
}

/* Problem Description Panel (Distraction-free black & white reading experience) */
.tb-problem-panel {
    background: #090B0F;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 24px 26px;
    margin-bottom: 20px;
    color: #F8FAFC;
}

.tb-panel-heading {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #FFFFFF !important;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
}

.tb-code-box {
    background: #000000;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 14px 16px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace;
    font-size: 0.86rem;
    color: #F8FAFC;
    line-height: 1.6;
    margin-top: 8px;
    margin-bottom: 8px;
}

/* Workspace Split-Screen Styles */
.tb-workspace-desc-panel {
    background: #090B0F;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 22px 24px;
    height: 720px;
    max-height: calc(100vh - 170px);
    min-height: 540px;
    overflow-y: auto;
    color: #F8FAFC;
}

.tb-workspace-desc-panel::-webkit-scrollbar {
    width: 6px;
}
.tb-workspace-desc-panel::-webkit-scrollbar-track {
    background: #090B0F;
}
.tb-workspace-desc-panel::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 3px;
}
.tb-workspace-desc-panel::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

.tb-workspace-editor-panel {
    background: #111C2E;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 14px;
}

.tb-editor-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #0B111D;
    border: 1px solid #1E293B;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 8px 14px;
    margin-bottom: 0;
}

.tb-badge-lang {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 0.76rem;
    font-weight: 600;
    background: #1E3A5F;
    color: #93C5FD;
    border: 1px solid #1D4ED8;
}

.tb-tab-container {
    background: #0B111D;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 14px;
    margin-top: 10px;
}

/* Top Navigation Bar */
.tb-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 18px;
    background: #0D1211;
    border: 1px solid #26332F;
    border-radius: 10px;
    margin-bottom: 20px;
}

.tb-breadcrumb {
    font-size: 0.92rem;
    font-weight: 600;
    color: #F5F7FA;
    display: flex;
    align-items: center;
    gap: 8px;
}

.tb-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 16px;
    font-size: 0.75rem;
    font-weight: 600;
}

.tb-status-connected {
    background: rgba(16, 185, 129, 0.12);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.tb-status-disconnected {
    background: rgba(239, 68, 68, 0.12);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.tb-pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
}

.tb-pulse-green {
    background-color: #34D399;
    box-shadow: 0 0 6px rgba(52, 211, 153, 0.6);
}

.tb-pulse-red {
    background-color: #EF4444;
    box-shadow: 0 0 6px rgba(239, 68, 68, 0.6);
}

/* Code block styling */
pre, code {
    background-color: #0D1211 !important;
    border: 1px solid #26332F !important;
    color: #A7F3D0 !important;
    border-radius: 6px;
}

/* Form Controls & Inputs */
input, select, textarea, [data-baseweb="input"] {
    background-color: #121A18 !important;
    border-color: #26332F !important;
    color: #F5F7FA !important;
    border-radius: 6px !important;
}

input:focus, select:focus, textarea:focus {
    border-color: #34D399 !important;
    box-shadow: 0 0 0 1px #34D399 !important;
}

/* Streamlit Button Overrides */
.stButton > button {
    background: #18221F;
    color: #F5F7FA;
    border: 1px solid #26332F;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 0.4rem 1rem;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    background: #202D29;
    border-color: #34D399;
    color: #FFFFFF;
}

.stButton > button[kind="primary"] {
    background: #34D399 !important;
    color: #080B0D !important;
    border: 1px solid #34D399 !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(52, 211, 153, 0.25) !important;
}

.stButton > button[kind="primary"]:hover {
    background: #10B981 !important;
    border-color: #10B981 !important;
    color: #080B0D !important;
    box-shadow: 0 4px 12px rgba(52, 211, 153, 0.35) !important;
}

/* Empty state container */
.tb-empty-state {
    text-align: center;
    padding: 30px 20px;
    background: #121A18;
    border: 1px dashed #26332F;
    border-radius: 8px;
    color: #94A3B8;
}

/* Distribution bar */
.tb-progress-container {
    background: #18221F;
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
    margin-top: 6px;
    margin-bottom: 12px;
    display: flex;
}
.tb-progress-easy {
    background-color: #34D399;
    height: 100%;
}
.tb-progress-med {
    background-color: #F59E0B;
    height: 100%;
}
.tb-progress-hard {
    background-color: #EF4444;
    height: 100%;
}
</style>
"""


def apply_custom_css():
    """Inject custom dark theme CSS into the current Streamlit app page."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
