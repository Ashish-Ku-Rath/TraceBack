"""
Monaco Editor component wrapper for TraceBack coding workspace.
Integrates the Microsoft Monaco Editor with Python syntax highlighting,
line numbers, and the 'vs-dark' professional code theme.

ARCHITECTURE & FLICKER PREVENTION:
- Monaco maintains editor state locally in the client browser.
- Typing does NOT fire Streamlit.setComponentValue() or trigger app reruns.
- State synchronizes with Python on deliberate actions:
  * Blur (clicking outside, switching tabs, clicking Run Code / Save Draft)
  * Ctrl+S / Cmd+S shortcut
  * Explicit sync_trigger
"""

from pathlib import Path
from typing import Optional
import streamlit as st
from streamlit.components.v1 import declare_component

MONACO_BUILD_DIR = Path(__file__).resolve().parent / "monaco_build"
render_component = declare_component("traceback_monaco", path=str(MONACO_BUILD_DIR))


def render_monaco_editor(
    code: str,
    key: str = "monaco_editor",
    height: str = "450px",
    language: str = "python",
    theme: str = "vs-dark",
    line_numbers: bool = True,
    minimap: bool = False,
    sync_trigger: Optional[int] = None,
) -> str:
    """
    Render the Monaco code editor inside the Streamlit UI.
    
    Args:
        code: Initial or current code string.
        key: Unique Streamlit component key for state tracking.
        height: CSS height of the editor container.
        language: Programming language for syntax highlighting (default 'python').
        theme: Monaco theme ('vs-dark' for standard professional dark mode).
        line_numbers: Whether to display editor line numbers.
        minimap: Whether to show code minimap.
        sync_trigger: Optional trigger counter to force editor sync to Python.
        
    Returns:
        str: Current code string after user edits, or initial code if untouched.
    """
    kwargs = {
        "value": code,
        "height": height,
        "language": language,
        "lineNumbers": line_numbers,
        "minimap": minimap,
        "theme": theme,
        "key": key,
        "default": code,
    }
    if sync_trigger is not None:
        kwargs["sync_trigger"] = sync_trigger

    edited_code = render_component(**kwargs)

    if edited_code is not None and isinstance(edited_code, str):
        return edited_code
    return code
