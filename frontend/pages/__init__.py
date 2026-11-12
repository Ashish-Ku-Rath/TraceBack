"""
Page views package for TraceBack frontend.
"""

from frontend.pages.coming_soon import render_coming_soon_page
from frontend.pages.dashboard import render_dashboard_page
from frontend.pages.problem_detail import render_problem_detail_page
from frontend.pages.problems import render_problems_page

__all__ = [
    "render_dashboard_page",
    "render_problems_page",
    "render_problem_detail_page",
    "render_coming_soon_page",
]
