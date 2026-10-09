"""UI components package."""

from .styles import get_custom_css
from .components import (
    render_header,
    render_kpi_row,
    render_priorities,
    render_today_schedule,
    render_schedule_table,
    render_agent_traces,
    render_practice_interactive,
    render_subject_charts,
    render_flashcards_view,
    render_pomodoro_widget,
)

__all__ = [
    "get_custom_css",
    "render_header",
    "render_kpi_row",
    "render_priorities",
    "render_today_schedule",
    "render_schedule_table",
    "render_agent_traces",
    "render_practice_interactive",
    "render_subject_charts",
    "render_flashcards_view",
    "render_pomodoro_widget",
]
