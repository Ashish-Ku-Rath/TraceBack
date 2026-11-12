"""
UI components package for TraceBack frontend.
"""

from frontend.components.cards import (
    render_backend_offline_alert,
    render_difficulty_breakdown,
    render_empty_activity,
    render_platform_info,
    render_stat_card,
)
from frontend.components.header import render_header
from frontend.components.problem_card import (
    get_difficulty_badge_html,
    get_tags_html,
    render_problem_recommendation_card,
)
from frontend.components.sidebar import render_sidebar

__all__ = [
    "render_sidebar",
    "render_header",
    "render_stat_card",
    "render_difficulty_breakdown",
    "render_platform_info",
    "render_empty_activity",
    "render_backend_offline_alert",
    "get_difficulty_badge_html",
    "get_tags_html",
    "render_problem_recommendation_card",
]
