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

/* ==========================================================================
   PREMIUM ANIMATED DEVELOPER DASHBOARD & LANDING PAGE STYLES
   ========================================================================== */

/* Keyframe Animations */
@keyframes tbFloat {
    0% {
        transform: translateY(0px) rotate(0deg);
    }
    50% {
        transform: translateY(-8px) rotate(0.4deg);
    }
    100% {
        transform: translateY(0px) rotate(0deg);
    }
}

@keyframes tbBadgeFloat1 {
    0% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-6px);
    }
    100% {
        transform: translateY(0px);
    }
}

@keyframes tbBadgeFloat2 {
    0% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(6px);
    }
    100% {
        transform: translateY(0px);
    }
}

@keyframes tbPulseGlow {
    0%, 100% {
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.15), 0 20px 40px rgba(0, 0, 0, 0.6);
        border-color: rgba(52, 211, 153, 0.28);
    }
    50% {
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.25), 0 25px 50px rgba(0, 0, 0, 0.7);
        border-color: rgba(56, 189, 248, 0.4);
    }
}

@keyframes tbCursorBlink {
    0%, 49% {
        opacity: 1;
    }
    50%, 100% {
        opacity: 0;
    }
}

@keyframes tbFadeInUp {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Top Navigation Bar on Homepage */
.tb-landing-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 24px;
    background: rgba(13, 21, 36, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(34, 51, 78, 0.8);
    border-radius: 12px;
    margin-bottom: 28px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.tb-nav-links {
    display: flex;
    align-items: center;
    gap: 24px;
}

.tb-nav-link {
    color: #94A3B8;
    font-size: 0.88rem;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.15s ease;
    cursor: pointer;
}

.tb-nav-link:hover, .tb-nav-link.active {
    color: #F8FAFC;
}

/* Hero Section */
.tb-hero-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
    padding: 24px 0 48px 0;
    animation: tbFadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.tb-hero-left {
    flex: 1 1 540px;
}

.tb-hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 20px;
    background: rgba(52, 211, 153, 0.08);
    border: 1px solid rgba(52, 211, 153, 0.28);
    font-size: 0.80rem;
    font-weight: 600;
    color: #34D399;
    letter-spacing: 0.02em;
    margin-bottom: 20px;
    box-shadow: 0 0 12px rgba(52, 211, 153, 0.15);
}

.tb-hero-h1 {
    font-size: 3.1rem;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.03em;
    color: #FFFFFF !important;
    margin: 0 0 10px 0;
}

.tb-hero-h2 {
    font-size: 1.65rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #34D399 0%, #38BDF8 60%, #818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 18px 0;
}

.tb-hero-desc {
    font-size: 1.05rem;
    line-height: 1.65;
    color: #94A3B8;
    max-width: 540px;
    margin: 0 0 28px 0;
}

/* Hero Right: Animated Floating Coding Workspace Illustration */
.tb-hero-visual-wrapper {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
    max-width: 560px;
    margin: 0 auto;
    overflow: visible;
}

.tb-window-frame {
    position: relative;
    width: 100%;
    max-width: 520px;
    background: #0B111E;
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 12px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7), 0 0 24px rgba(52, 211, 153, 0.1);
    animation: tbFloat 6s ease-in-out infinite, tbPulseGlow 6s ease-in-out infinite;
    z-index: 2;
    overflow: hidden;
}

.tb-window-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 14px;
    background: #080D17;
    border-bottom: 1px solid rgba(30, 41, 59, 0.8);
}

.tb-window-dots {
    display: flex;
    align-items: center;
    gap: 6px;
}

.tb-window-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
}

.tb-dot-red { background: #EF4444; }
.tb-dot-yellow { background: #F59E0B; }
.tb-dot-green { background: #10B981; }

.tb-window-filename {
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 0.76rem;
    font-weight: 600;
    color: #94A3B8;
    display: flex;
    align-items: center;
    gap: 6px;
}

.tb-window-lang {
    font-size: 0.70rem;
    color: #38BDF8;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.25);
    padding: 1px 6px;
    border-radius: 4px;
    font-weight: 600;
}

.tb-window-body {
    padding: 14px 16px;
    font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
    font-size: 0.80rem;
    line-height: 1.55;
    background: #0B111E;
    max-height: 290px;
    overflow-x: auto;
    overflow-y: hidden;
}

.tb-code-line {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1px;
}

.tb-line-num {
    width: 24px;
    color: #475569;
    user-select: none;
    font-size: 0.74rem;
    flex-shrink: 0;
}

.tb-line-content {
    color: #E2E8F0;
    white-space: pre;
    font-size: 0.78rem;
}

.tb-code-line.active-line {
    background: rgba(56, 189, 248, 0.08);
    border-left: 2px solid #38BDF8;
    margin-left: -16px;
    padding-left: 14px;
}

.tb-syntax-kw { color: #F472B6; font-weight: 600; }
.tb-syntax-fn { color: #60A5FA; font-weight: 600; }
.tb-syntax-param { color: #FBBF24; }
.tb-syntax-str { color: #34D399; }
.tb-syntax-comment { color: #64748B; font-style: italic; }
.tb-syntax-num { color: #A78BFA; }

.tb-cursor {
    display: inline-block;
    width: 2px;
    height: 1.1em;
    background: #38BDF8;
    margin-left: 2px;
    vertical-align: middle;
    animation: tbCursorBlink 1s infinite;
}

/* Floating Satellite Cards */
.tb-float-card {
    position: absolute;
    background: rgba(13, 22, 38, 0.94);
    backdrop-filter: blur(12px);
    border-radius: 8px;
    padding: 10px 14px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
    z-index: 3;
    pointer-events: none;
}

.tb-float-ai {
    top: -8px;
    right: -8px;
    border: 1px solid rgba(56, 189, 248, 0.45);
    animation: tbBadgeFloat1 5s ease-in-out infinite;
    max-width: 250px;
}

.tb-float-ai-header {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.74rem;
    font-weight: 700;
    color: #38BDF8;
    margin-bottom: 3px;
}

.tb-float-ai-text {
    font-size: 0.74rem;
    color: #E2E8F0;
    line-height: 1.35;
}

.tb-float-test {
    bottom: -10px;
    left: -8px;
    border: 1px solid rgba(52, 211, 153, 0.45);
    animation: tbBadgeFloat2 5.5s ease-in-out infinite;
    max-width: 260px;
}

.tb-float-test-header {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.76rem;
    font-weight: 700;
    color: #34D399;
    margin-bottom: 2px;
}

.tb-float-test-detail {
    font-size: 0.70rem;
    color: #94A3B8;
}

.tb-float-diag {
    bottom: 40px;
    right: -10px;
    border: 1px solid rgba(167, 139, 250, 0.45);
    animation: tbBadgeFloat1 6s ease-in-out infinite 0.5s;
    font-size: 0.70rem;
    color: #C4B5FD;
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 6px 10px;
}

/* Section Common Styling */
.tb-landing-section {
    margin-bottom: 56px;
}

.tb-section-header {
    margin-bottom: 28px;
}

.tb-section-pill {
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #38BDF8;
    margin-bottom: 6px;
}

.tb-section-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #FFFFFF !important;
    margin: 0 0 8px 0;
    letter-spacing: -0.02em;
}

.tb-section-subtitle {
    font-size: 0.95rem;
    color: #94A3B8;
    margin: 0;
    max-width: 650px;
}

/* Quick Actions Cards */
.tb-quick-action-box {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 24px 22px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s ease;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
}

.tb-quick-action-box:hover {
    border-color: #38BDF8;
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(56, 189, 248, 0.15);
}

.tb-action-icon {
    font-size: 1.8rem;
    margin-bottom: 12px;
    display: inline-block;
}

.tb-action-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 8px;
}

.tb-action-desc {
    font-size: 0.88rem;
    color: #94A3B8;
    line-height: 1.5;
    margin-bottom: 18px;
    flex-grow: 1;
}

/* How TraceBack Works: 3-Step Timeline */
.tb-timeline-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    position: relative;
}

.tb-step-card {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 26px 22px;
    position: relative;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

.tb-step-card:hover {
    border-color: #34D399;
    transform: translateY(-2px);
}

.tb-step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: rgba(52, 211, 153, 0.12);
    border: 1px solid rgba(52, 211, 153, 0.3);
    color: #34D399;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 14px;
}

.tb-step-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 8px;
}

.tb-step-desc {
    font-size: 0.88rem;
    color: #94A3B8;
    line-height: 1.55;
    margin: 0;
}

/* Platform Features Grid (6 Cards) */
.tb-features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.tb-feature-card {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 22px 20px;
    transition: all 0.2s ease;
}

.tb-feature-card:hover {
    border-color: #38BDF8;
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.tb-feature-icon {
    font-size: 1.6rem;
    margin-bottom: 12px;
}

.tb-feature-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 6px;
}

.tb-feature-desc {
    font-size: 0.85rem;
    color: #94A3B8;
    line-height: 1.5;
    margin: 0;
}

/* Final CTA Banner */
.tb-cta-banner {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 14px;
    padding: 44px 36px;
    text-align: center;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(56, 189, 248, 0.1);
    margin: 40px 0 50px 0;
}

.tb-cta-h2 {
    font-size: 2.1rem;
    font-weight: 800;
    color: #FFFFFF !important;
    margin: 0 0 10px 0;
    letter-spacing: -0.02em;
}

.tb-cta-desc {
    font-size: 1.05rem;
    color: #94A3B8;
    max-width: 600px;
    margin: 0 auto 26px auto;
    line-height: 1.6;
}

/* Modern Developer Footer */
.tb-footer {
    border-top: 1px solid #1E293B;
    padding: 40px 0 24px 0;
    margin-top: 50px;
}

.tb-footer-content {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 36px;
    margin-bottom: 32px;
}

.tb-footer-brand {
    max-width: 320px;
}

.tb-footer-tagline {
    font-size: 0.85rem;
    color: #94A3B8;
    line-height: 1.5;
    margin-top: 10px;
}

.tb-footer-col-title {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #CBD5E1;
    letter-spacing: 0.06em;
    margin-bottom: 14px;
}

.tb-footer-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 9px;
}

.tb-footer-item {
    font-size: 0.84rem;
    color: #94A3B8;
}

.tb-footer-bottom {
    border-top: 1px solid rgba(30, 41, 59, 0.6);
    padding-top: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.78rem;
    color: #64748B;
}

/* Responsive Breakpoints */
@media (max-width: 992px) {
    .tb-hero-section {
        flex-direction: column;
        align-items: stretch;
        gap: 32px;
    }
    .tb-hero-h1 {
        font-size: 2.2rem;
    }
    .tb-hero-visual-wrapper {
        max-width: 100%;
        padding: 10px 0;
    }
    .tb-window-frame {
        max-width: 100%;
    }
    .tb-timeline-grid, .tb-features-grid {
        grid-template-columns: 1fr;
    }
    .tb-float-card {
        display: none;
    }
}

/* Accessibility: Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
    .tb-window-frame, .tb-float-card, .tb-cursor {
        animation: none !important;
    }
}
</style>

"""


def apply_custom_css():
    """Inject custom dark theme CSS into the current Streamlit app page."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
