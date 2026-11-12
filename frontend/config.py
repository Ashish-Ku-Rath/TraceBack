"""
Frontend configuration and theme constants for TraceBack.
Updated visual identity: Emerald & dark charcoal/navy palette, clean bold developer typography.
"""

import os

# Backend API endpoint configuration
BACKEND_BASE_URL: str = os.getenv("BACKEND_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

# Design System Colour Palette (Emerald / Dark Charcoal)
COLORS = {
    "main_bg": "#080B0D",
    "sidebar_bg": "#0D1211",
    "card_bg": "#121A18",
    "secondary_card": "#18221F",
    "primary_accent": "#34D399",
    "primary_accent_hover": "#10B981",
    "secondary_accent": "#10B981",
    "blue_accent": "#38BDF8",
    "main_text": "#F5F7FA",
    "secondary_text": "#94A3B8",
    "border": "#26332F",
    "border_subtle": "#1B2623",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "tag_bg": "rgba(52, 211, 153, 0.10)",
    "tag_border": "rgba(52, 211, 153, 0.25)",
}

# Brand identity constants
BRAND_NAME = "TraceBack"
TAGLINE = "The Intelligent Coding & Debugging Assistant"

# Brand Logo: Emerald green brackets, white text, bold minimal typography
LOGO_HTML = """
<div style="display: flex; align-items: center; gap: 8px; font-family: 'JetBrains Mono', 'Fira Code', 'Inter', monospace; user-select: none;">
    <span style="font-size: 1.55rem; font-weight: 800; letter-spacing: -0.5px; line-height: 1;">
        <span style="color: #34D399;">&lt;/</span><span style="color: #F5F7FA;">TraceBack</span><span style="color: #34D399;">&gt;</span>
    </span>
</div>
"""

LOGO_HTML_LARGE = """
<div style="display: inline-flex; align-items: center; gap: 10px; font-family: 'JetBrains Mono', 'Fira Code', 'Inter', monospace; user-select: none;">
    <span style="font-size: 2.1rem; font-weight: 800; letter-spacing: -0.7px; line-height: 1;">
        <span style="color: #34D399;">&lt;/</span><span style="color: #F5F7FA;">TraceBack</span><span style="color: #34D399;">&gt;</span>
    </span>
</div>
"""
