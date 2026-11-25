"""
TraceBack — Premium Animated Developer Dashboard & Landing Experience.
Implements the revised visual identity: modern dark charcoal/navy canvas,
emerald & electric blue accents, floating coding workspace illustration,
smooth entrance animations, quick action cards, 3-step workflow,
feature highlights, genuine live problem metrics, and a developer-platform footer.
"""

import textwrap
import streamlit as st
from frontend.api_client import api_client
from frontend.components.cards import render_backend_offline_alert
from frontend.config import BRAND_NAME, LOGO_HTML_LARGE, TAGLINE


def render_dashboard_page():
    """Render the premium animated developer landing page and dashboard."""

    # Fetch live backend statistics from SQLite database
    stats, error = api_client.get_statistics()
    if error:
        render_backend_offline_alert(error)

    total_problems = stats.get("total", 23)
    easy_problems = stats.get("easy", 17)
    med_problems = stats.get("medium", 6)
    hard_problems = stats.get("hard", 0)

    # =========================================================================
    # 1. TOP NAVIGATION BAR
    # =========================================================================
    st.markdown('<div id="top"></div>', unsafe_allow_html=True)
    nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([3.0, 1.2, 1.2, 1.2, 1.8])

    with nav_c1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; padding-top: 4px;">
                <span style="font-size: 1.45rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; letter-spacing: -0.5px;">
                    <span style="color: #34D399;">&lt;/</span><span style="color: #F8FAFC;">TraceBack</span><span style="color: #34D399;">&gt;</span>
                </span>
                <span style="font-size: 0.72rem; color: #64748B; background: #0F172A; border: 1px solid #1E293B; padding: 2px 7px; border-radius: 4px; font-weight: 600;">v0.5</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with nav_c2:
        if st.button("🏠 Home", key="topnav_home", use_container_width=True, type="secondary"):
            st.session_state["current_page"] = "dashboard"
            st.rerun()

    with nav_c3:
        if st.button("🧩 Problems", key="topnav_problems", use_container_width=True, type="secondary"):
            st.session_state["current_page"] = "problems"
            st.session_state["selected_problem_id"] = None
            st.rerun()

    with nav_c4:
        if st.button("🤖 AI Debugger", key="topnav_ai", use_container_width=True, type="secondary"):
            st.session_state["current_page"] = "workspace"
            st.session_state["selected_problem_id"] = 1
            st.rerun()

    with nav_c5:
        if st.button("🚀 Start Coding", key="topnav_start", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "workspace"
            st.session_state["selected_problem_id"] = 1
            st.rerun()

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 2. HERO SECTION WITH ANIMATED CODING WORKSPACE ILLUSTRATION
    # =========================================================================
    hero_col_left, hero_col_right = st.columns([1.15, 1.15], gap="large")

    with hero_col_left:
        hero_left_html = (
            '<div style="animation: tbFadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);">'
            '<div class="tb-hero-pill">'
            '<span>⚡</span>'
            '<span>Next-Gen Coding & AI Debugging Platform</span>'
            '</div>'
            '<h1 class="tb-hero-h1">Every Bug Leaves a Trace.</h1>'
            '<div class="tb-hero-h2">Code. Test. Debug. Learn.</div>'
            '<p class="tb-hero-desc">'
            'Your personal coding workspace powered by AI. Practise programming problems, '
            'execute your solutions, understand errors, and improve with intelligent debugging assistance.'
            '</p>'
            '</div>'
        )
        st.markdown(hero_left_html, unsafe_allow_html=True)

        cta_col1, cta_col2, _ = st.columns([1.35, 1.45, 1.0])
        with cta_col1:
            if st.button("▶  Start Coding", key="hero_cta_start", type="primary", use_container_width=True):
                st.session_state["current_page"] = "workspace"
                st.session_state["selected_problem_id"] = 1
                st.rerun()
        with cta_col2:
            if st.button("🧩  Explore Problems", key="hero_cta_explore", type="secondary", use_container_width=True):
                st.session_state["current_page"] = "problems"
                st.session_state["selected_problem_id"] = None
                st.rerun()

        st.markdown(
            '<div style="display: flex; align-items: center; gap: 16px; margin-top: 24px; font-size: 0.82rem; color: #64748B;">'
            '<span>✓ Complete Program Mode</span>'
            '<span>•</span>'
            '<span>✓ 5 AI Debug Modes</span>'
            '<span>•</span>'
            '<span>✓ OnlineCompiler Sandbox</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    with hero_col_right:
        # Floating Coding Workspace Composition (Single-line concatenation prevents Markdown code-block parsing)
        hero_visual_html = (
            '<div class="tb-hero-visual-wrapper">'
            '<!-- Satellite Card 1: AI Debug Mentor -->'
            '<div class="tb-float-card tb-float-ai">'
            '<div class="tb-float-ai-header">'
            '<span>🤖</span>'
            '<span>AI Debug Mentor</span>'
            '<span style="color: #38BDF8; font-size: 0.65rem; background: rgba(56, 189, 248, 0.15); padding: 1px 5px; border-radius: 3px;">Active</span>'
            '</div>'
            '<div class="tb-float-ai-text">'
            '"Optimized from O(n²) to O(n) using a hash map lookup."'
            '</div>'
            '</div>'
            '<!-- Central Floating Code Window -->'
            '<div class="tb-window-frame">'
            '<div class="tb-window-header">'
            '<div class="tb-window-dots">'
            '<span class="tb-window-dot tb-dot-red"></span>'
            '<span class="tb-window-dot tb-dot-yellow"></span>'
            '<span class="tb-window-dot tb-dot-green"></span>'
            '</div>'
            '<div class="tb-window-filename">'
            '<span>solution.py</span>'
            '</div>'
            '<div class="tb-window-lang">Python</div>'
            '</div>'
            '<div class="tb-window-body">'
            '<div class="tb-code-line"><span class="tb-line-num">1</span><span class="tb-line-content"><span class="tb-syntax-kw">def</span> <span class="tb-syntax-fn">find_sum</span>(numbers, target):</span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">2</span><span class="tb-line-content">    seen = {}</span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">3</span><span class="tb-line-content"></span></div>'
            '<div class="tb-code-line active-line"><span class="tb-line-num">4</span><span class="tb-line-content">    <span class="tb-syntax-kw">for</span> i, num <span class="tb-syntax-kw">in</span> <span class="tb-syntax-fn">enumerate</span>(numbers):</span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">5</span><span class="tb-line-content">        diff = target - num</span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">6</span><span class="tb-line-content"></span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">7</span><span class="tb-line-content">        <span class="tb-syntax-kw">if</span> diff <span class="tb-syntax-kw">in</span> seen:</span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">8</span><span class="tb-line-content">            <span class="tb-syntax-kw">return</span> [seen[diff], i]<span class="tb-cursor"></span></span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">9</span><span class="tb-line-content">        seen[num] = i</span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">10</span><span class="tb-line-content"></span></div>'
            '<div class="tb-code-line"><span class="tb-line-num">11</span><span class="tb-line-content">    <span class="tb-syntax-kw">return</span> []</span></div>'
            '</div>'
            '</div>'
            '<!-- Satellite Card 2: Test Result Panel -->'
            '<div class="tb-float-card tb-float-test">'
            '<div class="tb-float-test-header">'
            '<span>✓</span>'
            '<span>Test Suite Passed</span>'
            '<span style="color: #34D399; font-size: 0.68rem; margin-left: 6px;">ACCEPTED</span>'
            '</div>'
            '<div class="tb-float-test-detail">'
            '3 / 3 Cases Passed • 0.04s Execution • 8.1MB'
            '</div>'
            '</div>'
            '<!-- Satellite Card 3: Diagnostic Indicator -->'
            '<div class="tb-float-card tb-float-diag">'
            '<span>⚡</span>'
            '<span>Trace Resolved: Index Bounds Verified</span>'
            '</div>'
            '</div>'
        )
        st.markdown(hero_visual_html, unsafe_allow_html=True)

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 3. SECTION A: QUICK ACTIONS
    # =========================================================================
    st.markdown(
        """
        <div class="tb-section-header">
            <div class="tb-section-pill">Action Hub</div>
            <h2 class="tb-section-title">Jump Straight Into Coding</h2>
            <p class="tb-section-subtitle">Pick an activity to sharpen your problem-solving skills with immediate execution and guidance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    act_col1, act_col2, act_col3 = st.columns(3, gap="medium")

    with act_col1:
        st.markdown(
            """
            <div class="tb-quick-action-box">
                <div>
                    <div class="tb-action-icon">🧩</div>
                    <div class="tb-action-title">Start Practising</div>
                    <div class="tb-action-desc">
                        Explore 23 curated programming problems across Easy and Medium levels.
                        Improve algorithmic logic and coding discipline.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Problems  →", key="act_btn_prob", type="primary", use_container_width=True):
            st.session_state["current_page"] = "problems"
            st.session_state["selected_problem_id"] = None
            st.rerun()

    with act_col2:
        st.markdown(
            """
            <div class="tb-quick-action-box">
                <div>
                    <div class="tb-action-icon">🤖</div>
                    <div class="tb-action-title">AI Debug Mentor</div>
                    <div class="tb-action-desc">
                        Stuck on a tricky error? Receive Socratic hints, algorithm breakdowns,
                        bug detection, and minimal surgical corrections powered by Gemini.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open AI Debugger  →", key="act_btn_ai", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "workspace"
            st.session_state["selected_problem_id"] = 1
            st.rerun()

    with act_col3:
        st.markdown(
            """
            <div class="tb-quick-action-box">
                <div>
                    <div class="tb-action-icon">🔬</div>
                    <div class="tb-action-title">Custom Test Lab</div>
                    <div class="tb-action-desc">
                        Validate edge cases and test your complete Python programs against
                        custom inputs and expected outputs in a safe remote runner.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Test Lab  →", key="act_btn_ctl", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "workspace"
            st.session_state["selected_problem_id"] = 1
            st.rerun()

    st.markdown("<div style='height: 52px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 4. SECTION B: HOW TRACEBACK WORKS
    # =========================================================================
    st.markdown(
        """
        <div class="tb-section-header">
            <div class="tb-section-pill">Workflow</div>
            <h2 class="tb-section-title">How TraceBack Works</h2>
            <p class="tb-section-subtitle">A seamless 3-step loop designed to make you a more resilient, analytical software engineer.</p>
        </div>
        <div class="tb-timeline-grid">
            <div class="tb-step-card">
                <div class="tb-step-badge">01</div>
                <div class="tb-step-title">Choose a Problem</div>
                <p class="tb-step-desc">
                    Browse our curated catalog of 23 DSA problems spanning arrays, strings, math,
                    and number theory with clear input/output requirements.
                </p>
            </div>
            <div class="tb-step-card">
                <div class="tb-step-badge">02</div>
                <div class="tb-step-title">Write & Execute</div>
                <p class="tb-step-desc">
                    Code from scratch in the distraction-free Monaco editor. Run your solution
                    with custom stdin or submit against automated judge test suites.
                </p>
            </div>
            <div class="tb-step-card">
                <div class="tb-step-badge">03</div>
                <div class="tb-step-title">Debug & Improve</div>
                <p class="tb-step-desc">
                    When tests fail or runtime exceptions occur, activate the Gemini AI Debug Mentor
                    for Socratic guidance, bug pinpointing, and algorithmic insights.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 56px;' id='features'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 5. SECTION C: PLATFORM FEATURES
    # =========================================================================
    st.markdown(
        """
        <div class="tb-section-header">
            <div class="tb-section-pill">Capabilities</div>
            <h2 class="tb-section-title">Engineered for Deliberate Practice</h2>
            <p class="tb-section-subtitle">TraceBack combines essential developer tooling into one cohesive, distraction-free environment.</p>
        </div>
        <div class="tb-features-grid">
            <div class="tb-feature-card">
                <div class="tb-feature-icon">📚</div>
                <div class="tb-feature-title">23 Curated Problems</div>
                <p class="tb-feature-desc">Graded challenges covering Arrays, Two Pointers, Strings, Math, and Number Theory.</p>
            </div>
            <div class="tb-feature-card">
                <div class="tb-feature-icon">💻</div>
                <div class="tb-feature-title">Monaco Code Editor</div>
                <p class="tb-feature-desc">VS Code editor engine with zero-rerun stability, syntax highlighting, and Ctrl+S drafts.</p>
            </div>
            <div class="tb-feature-card">
                <div class="tb-feature-icon">⚡</div>
                <div class="tb-feature-title">Dual Execution Engine</div>
                <p class="tb-feature-desc">Cloud execution via OnlineCompiler REST API alongside safe, deterministic offline simulation.</p>
            </div>
            <div class="tb-feature-card">
                <div class="tb-feature-icon">🔬</div>
                <div class="tb-feature-title">Custom Test Lab</div>
                <p class="tb-feature-desc">Evaluate custom edge-case test pairs simultaneously with detailed pass/fail feedback.</p>
            </div>
            <div class="tb-feature-card">
                <div class="tb-feature-icon">🤖</div>
                <div class="tb-feature-title">5-Mode AI Debugger</div>
                <p class="tb-feature-desc">Error explanation, hint delivery, algorithm walk-throughs, bug isolation, and code fixes.</p>
            </div>
            <div class="tb-feature-card">
                <div class="tb-feature-icon">⚖️</div>
                <div class="tb-feature-title">Automated Submission Judge</div>
                <p class="tb-feature-desc">Rigorous test evaluations returning instant Accepted, Wrong Answer, and Runtime Error verdicts.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 56px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 6. SECTION D: PROBLEM DISCOVERY & LIVE STATISTICS
    # =========================================================================
    st.markdown(
        """
        <div class="tb-section-header">
            <div class="tb-section-pill">Problem Discovery</div>
            <h2 class="tb-section-title">Explore Problem Catalog</h2>
            <p class="tb-section-subtitle">Real-time statistics queried directly from the SQLite database.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.markdown(
            f"""
            <div class="tb-stat-card" style="border-top: 3px solid #34D399;">
                <div>
                    <div class="tb-stat-label">Total Challenges</div>
                    <div class="tb-stat-value">{total_problems}</div>
                </div>
                <div class="tb-stat-desc">Curated in database</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with stat_col2:
        st.markdown(
            f"""
            <div class="tb-stat-card" style="border-top: 3px solid #10B981;">
                <div>
                    <div class="tb-stat-label">Easy Tier</div>
                    <div class="tb-stat-value">{easy_problems}</div>
                </div>
                <div class="tb-stat-desc">Core fundamentals & math</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with stat_col3:
        st.markdown(
            f"""
            <div class="tb-stat-card" style="border-top: 3px solid #F59E0B;">
                <div>
                    <div class="tb-stat-label">Medium Tier</div>
                    <div class="tb-stat-value">{med_problems}</div>
                </div>
                <div class="tb-stat-desc">Algorithmic complexity</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with stat_col4:
        st.markdown(
            f"""
            <div class="tb-stat-card" style="border-top: 3px solid #EF4444;">
                <div>
                    <div class="tb-stat-label">Hard Tier</div>
                    <div class="tb-stat-value">{hard_problems}</div>
                </div>
                <div class="tb-stat-desc">Advanced graph & DP</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    disc_btn_col, _ = st.columns([2.5, 5])
    with disc_btn_col:
        if st.button("Browse Full Problem Library  →", key="disc_browse_btn", type="primary", use_container_width=True):
            st.session_state["current_page"] = "problems"
            st.session_state["selected_problem_id"] = None
            st.rerun()

    st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 7. SECTION E: FINAL CTA BANNER
    # =========================================================================
    cta_banner_html = """
    <div class="tb-cta-banner">
        <div style="font-size: 0.80rem; font-weight: 700; color: #34D399; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">
            Get Started Now
        </div>
        <h2 class="tb-cta-h2">Your Next Solution Starts Here.</h2>
        <p class="tb-cta-desc">
            Write your code, find your mistakes, and take the next step in your programming journey
            with TraceBack's intelligent execution and debugging workspace.
        </p>
    </div>
    """
    st.markdown(textwrap.dedent(cta_banner_html).strip(), unsafe_allow_html=True)

    final_c1, final_c2, final_c3 = st.columns([2.5, 2.5, 2.5])
    with final_c2:
        if st.button("💻  Enter Workspace", key="final_cta_btn", type="primary", use_container_width=True):
            st.session_state["current_page"] = "workspace"
            st.session_state["selected_problem_id"] = 1
            st.rerun()

    # =========================================================================
    # 8. FOOTER
    # =========================================================================
    footer_html = """
    <footer class="tb-footer">
        <div class="tb-footer-content">
            <div class="tb-footer-brand">
                <span style="font-size: 1.4rem; font-weight: 800; font-family: 'JetBrains Mono', monospace;">
                    <span style="color: #34D399;">&lt;/</span><span style="color: #F8FAFC;">TraceBack</span><span style="color: #34D399;">&gt;</span>
                </span>
                <p class="tb-footer-tagline">
                    Making coding practice smarter through intelligent debugging and AI-powered learning.
                </p>
            </div>
            <div>
                <div class="tb-footer-col-title">Product</div>
                <ul class="tb-footer-list">
                    <li class="tb-footer-item">Problem Library (23 Problems)</li>
                    <li class="tb-footer-item">Monaco Code Editor</li>
                    <li class="tb-footer-item">AI Debug Mentor (Gemini)</li>
                    <li class="tb-footer-item">Custom Test Lab</li>
                </ul>
            </div>
            <div>
                <div class="tb-footer-col-title">Platform</div>
                <ul class="tb-footer-list">
                    <li class="tb-footer-item">FastAPI REST Backend</li>
                    <li class="tb-footer-item">Streamlit Native UI</li>
                    <li class="tb-footer-item">OnlineCompiler Remote Engine</li>
                    <li class="tb-footer-item">SQLite Database</li>
                </ul>
            </div>
            <div>
                <div class="tb-footer-col-title">Information</div>
                <ul class="tb-footer-list">
                    <li class="tb-footer-item">Complete Program Mode</li>
                    <li class="tb-footer-item">5 AI Assistance Modes</li>
                    <li class="tb-footer-item">74 Automated Tests</li>
                </ul>
            </div>
        </div>
        <div class="tb-footer-bottom">
            <span>© 2026 TraceBack. Built for developers.</span>
            <span>An Intelligent Coding, Execution and AI-Powered Debugging Platform.</span>
        </div>
    </footer>
    """
    st.markdown(textwrap.dedent(footer_html).strip(), unsafe_allow_html=True)
