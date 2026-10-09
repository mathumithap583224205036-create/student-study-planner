"""
Reusable UI components for the Student Study Planner Agent.
Includes KPI stat cards, schedule views, quiz cards, and agentic trace audit trails.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
from models.student_models import StudentProfile, StudyPlan, AgentActionTrace


def render_header(model_name: str, has_api_key: bool):
    """Render top application banner with model & agent status."""
    status_label = "Gemini Agentic Engine Active" if has_api_key else "Local High-Reliability Mode"
    status_color = "#34d399" if has_api_key else "#fbbf24"
    dot_color = "#34d399" if has_api_key else "#fbbf24"

    st.markdown(
        f"""
        <div class="agent-header">
            <div>
                <h1 class="agent-title">
                    <span>🎓</span> STUDENT STUDY PLANNER AGENT
                </h1>
                <p class="agent-subtitle">
                    Autonomous Agentic AI for Personalized Study Scheduling, Hour Allocation & Practice Generation
                </p>
            </div>
            <div>
                <div class="status-badge" style="border-color: {status_color}; color: {status_color};">
                    <span class="badge-dot" style="background-color: {dot_color}; box-shadow: 0 0 8px {dot_color};"></span>
                    <span>{status_label} ({model_name})</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi_row(profile: StudentProfile, plan: Optional[StudyPlan]):
    """Render KPI metrics across a 5-column dashboard card row."""
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Days to Exam</div>
                <div class="metric-value">{profile.days_remaining}d</div>
                <div class="metric-subtext">Exam Horizon</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # Check if tomorrow has an override
        tmrw_override = profile.date_overrides.get("tomorrow")
        override_note = f" (Tomorrow: {tmrw_override}h)" if tmrw_override is not None else " Target"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Daily Available</div>
                <div class="metric-value">{profile.daily_available_hours}h</div>
                <div class="metric-subtext">{override_note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        total_hrs = plan.total_available_hours if plan else round(profile.days_remaining * profile.daily_available_hours, 1)
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Study Time</div>
                <div class="metric-value">{total_hrs}h</div>
                <div class="metric-subtext">Allocated Across Days</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        total_topics = max(1, len(profile.completed_topics) + len(profile.pending_topics))
        pct = round(len(profile.completed_topics) / total_topics * 100, 1)
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Syllabus Covered</div>
                <div class="metric-value">{pct}%</div>
                <div class="metric-subtext">{len(profile.completed_topics)}/{total_topics} Topics Done</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        weak_count = len(profile.weak_topics)
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Priority Focus</div>
                <div class="metric-value" style="color: {'#dc2626' if weak_count > 0 else '#16a34a'};">{weak_count}</div>
                <div class="metric-subtext">Weak Areas Remaining</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_priorities(plan: Optional[StudyPlan], profile: StudentProfile):
    """Render topic priority badges and reasons."""
    high_items = plan.priorities.get("High", profile.weak_topics) if plan else profile.weak_topics
    med_items = plan.priorities.get("Medium", profile.subjects) if plan else profile.subjects
    low_items = plan.priorities.get("Low", profile.strong_topics) if plan else profile.strong_topics

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🔴 High Priority (Weak Areas)")
        if high_items:
            for item in high_items:
                st.markdown(f'<span class="pill-high">⚡ {item}</span>', unsafe_allow_html=True)
            if plan and plan.priority_explanations:
                for item in high_items:
                    exp = plan.priority_explanations.get(item)
                    if exp:
                        st.caption(f"💡 *{item}*: {exp}")
        else:
            st.info("No weak topics currently flagged.")

    with col2:
        st.markdown("#### 🟡 Medium Priority (Core Syllabus)")
        if med_items:
            for item in med_items:
                st.markdown(f'<span class="pill-med">📖 {item}</span>', unsafe_allow_html=True)
        else:
            st.write("All core topics reviewed.")

    with col3:
        st.markdown("#### 🟢 Low Priority (Strong Foundations)")
        if low_items:
            for item in low_items:
                st.markdown(f'<span class="pill-low">✓ {item}</span>', unsafe_allow_html=True)
        else:
            st.caption("No strong topics set.")


def render_today_schedule(plan: Optional[StudyPlan]):
    """Render Day 1 / Today's active study timetable."""
    st.markdown("### 📅 Today's Study Roadmap (Day 1)")
    if not plan or not plan.daily_schedule:
        st.info("No active study plan generated yet. Ask the AI Agent to 'Create my study plan' to generate your personalized timetable!")
        return

    day_1_sessions = [s for s in plan.daily_schedule if s.day == 1]
    if not day_1_sessions:
        day_1_sessions = plan.daily_schedule[:4]

    for s in day_1_sessions:
        s_class = "break" if s.session_type.lower() == "break" else ("revision" if s.session_type.lower() == "revision" else "")
        badge = "☕ BREAK" if s.session_type.lower() == "break" else (f"🎯 {s.session_type.upper()}")

        st.markdown(
            f"""
            <div class="session-item {s_class}">
                <div>
                    <strong>{s.time_slot}</strong> &nbsp;|&nbsp; 
                    <span style="font-weight: 600; color: #1e293b;">{s.subject}</span>: {s.topic}
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;">{s.notes}</div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; font-weight: 700; background: #e2e8f0; padding: 4px 8px; border-radius: 6px;">
                        {badge} ({s.duration_hours}h)
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_schedule_table(plan: Optional[StudyPlan]):
    """Render complete interactive tabular schedule with Day filter."""
    if not plan or not plan.daily_schedule:
        st.info("Generate a study plan first to explore the full daily schedule.")
        return

    days_avail = sorted(list(set(s.day for s in plan.daily_schedule)))
    selected_day = st.selectbox("Filter by Day:", ["All Days"] + [f"Day {d}" for d in days_avail])

    rows = []
    for s in plan.daily_schedule:
        if selected_day != "All Days" and f"Day {s.day}" != selected_day:
            continue
        rows.append({
            "Day": f"Day {s.day}",
            "Date": s.date_str,
            "Time Slot": s.time_slot,
            "Subject": s.subject,
            "Topic": s.topic,
            "Duration": f"{s.duration_hours}h",
            "Type": s.session_type,
            "Focus Notes": s.notes
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_agent_traces(traces: List[AgentActionTrace]):
    """Display the Agentic reasoning, decision, and tool execution audit trail."""
    with st.expander(f"🧠 Agent Reasoning & Tool Execution Audit Trail ({len(traces)} Steps)", expanded=False):
        st.markdown(
            """
            *The trail below demonstrates the autonomous agentic loop:  
            **User → Agent → Reason → Decide → Select Tool → Execute Tool → Observe Result → Next Action → Final Response***
            """
        )
        for t in traces:
            tool_info = f" | Tool: `{t.tool_name}`" if t.tool_name else ""
            st.markdown(
                f"""
                <div style="margin-bottom: 12px; padding: 10px 14px; background: #f8fafc; border-left: 3px solid #6366f1; border-radius: 6px;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #1e293b;">
                        Step {t.step_number}: {t.step_name}{tool_info} <span style="font-size: 0.75rem; color: #94a3b8; font-weight: 400;">({t.timestamp})</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #475569; margin-top: 4px;">
                        {t.reasoning}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if t.tool_input or t.tool_output:
                with st.expander("Show Tool I/O Data", expanded=False):
                    if t.tool_input:
                        st.json(t.tool_input)
                    if t.tool_output:
                        st.write(t.tool_output)


def render_practice_interactive(questions: List[Dict[str, Any]]):
    """Render interactive quiz with revealable answers."""
    if not questions:
        st.info("No practice questions currently loaded. Ask the agent: 'Give me practice questions on Java OOP'!")
        return

    for i, q in enumerate(questions, 1):
        with st.container():
            st.markdown(f"#### Q{i}. [{q.get('subject', 'General')}] {q.get('topic', '')}")
            st.markdown(f"**{q.get('question')}**")

            options = q.get("options")
            if options and isinstance(options, list):
                # Interactive radio selection
                user_choice = st.radio(f"Select option for Q{i}:", options, key=f"quiz_opt_{i}")
            
            with st.expander("🔍 Reveal Correct Answer & Conceptual Explanation"):
                st.markdown(f"**Correct Answer:** `{q.get('correct_answer')}`")
                st.markdown(f"**Explanation:** {q.get('explanation')}")
                st.caption(f"Difficulty: {q.get('difficulty', 'Medium')}")
            st.markdown("---")


def render_subject_charts(plan: Optional[StudyPlan]):
    """Render interactive visual charts for subject hours and session type distributions."""
    if not plan or not plan.daily_schedule:
        st.info("Study charts will render once a schedule is generated.")
        return

    # Extract sessions data
    data = []
    for s in plan.daily_schedule:
        data.append({
            "Subject": s.subject,
            "Type": s.session_type,
            "Duration": s.duration_hours,
            "Day": f"Day {s.day}"
        })
    df = pd.DataFrame(data)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 📚 Hours Allocated by Subject")
        # Filter out break for subject hours
        study_df = df[df["Type"] != "Break"]
        if not study_df.empty:
            subj_hours = study_df.groupby("Subject")["Duration"].sum().reset_index()
            subj_hours = subj_hours.sort_values(by="Duration", ascending=False)
            st.bar_chart(subj_hours.set_index("Subject"), color="#6366f1", use_container_width=True)
        else:
            st.write("No core study hours found.")

    with col2:
        st.markdown("##### ⏱️ Workload by Session Type")
        type_hours = df.groupby("Type")["Duration"].sum().reset_index()
        st.bar_chart(type_hours.set_index("Type"), color="#10b981", use_container_width=True)


def render_flashcards_view(questions: List[Dict[str, Any]]):
    """Render spaced repetition flashcards for active recall study."""
    if not questions:
        st.info("No flashcard concepts loaded yet. Generate questions to start flashcard review!")
        return

    if "fc_index" not in st.session_state:
        st.session_state.fc_index = 0
    if "fc_flipped" not in st.session_state:
        st.session_state.fc_flipped = False

    total = len(questions)
    curr_idx = st.session_state.fc_index % total
    q = questions[curr_idx]

    # Navigation bar
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        if st.button("⬅️ Previous Card", use_container_width=True):
            st.session_state.fc_index = (curr_idx - 1) % total
            st.session_state.fc_flipped = False
            st.rerun()
    with nav_col2:
        st.markdown(f"<div style='text-align: center; font-weight: 700; color: #475569;'>Flashcard {curr_idx + 1} of {total}</div>", unsafe_allow_html=True)
    with nav_col3:
        if st.button("Next Card ➡️", use_container_width=True):
            st.session_state.fc_index = (curr_idx + 1) % total
            st.session_state.fc_flipped = False
            st.rerun()

    # Flashcard card UI
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.fc_flipped:
        # Front of card
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); color: #ffffff; border-radius: 16px; padding: 32px; min-height: 220px; box-shadow: 0 10px 25px rgba(49, 46, 129, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);">
                <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">{q.get('subject', 'Subject')} • {q.get('topic', 'Topic')}</span>
                <h3 style="margin-top: 16px; font-size: 1.35rem; color: #f8fafc;">{q.get('question')}</h3>
                <p style="color: #c7d2fe; font-size: 0.85rem; margin-top: 12px;">Difficulty: {q.get('difficulty', 'Medium')} | Click 'Flip Flashcard' below to reveal answer</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🔄 Flip Flashcard (Show Answer)", type="primary", use_container_width=True):
            st.session_state.fc_flipped = True
            st.rerun()
    else:
        # Back of card
        st.markdown(
            f"""
            <div style="background: #f0fdf4; color: #166534; border: 2px solid #bbf7d0; border-radius: 16px; padding: 32px; min-height: 220px; box-shadow: 0 8px 20px rgba(22, 101, 52, 0.08);">
                <span style="background: #dcfce7; padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; color: #15803d;">ANSWER & EXPLANATION</span>
                <h4 style="margin-top: 14px; font-size: 1.2rem; color: #14532d;">{q.get('correct_answer')}</h4>
                <p style="color: #166534; font-size: 0.9rem; margin-top: 10px; line-height: 1.5;">{q.get('explanation')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        c_r1, c_r2, c_r3, c_r4 = st.columns([1, 1, 1, 1])
        with c_r1:
            if st.button("🔄 Flip Back", use_container_width=True):
                st.session_state.fc_flipped = False
                st.rerun()
        with c_r2:
            if st.button("🔴 Hard", use_container_width=True):
                st.session_state.fc_index = (curr_idx + 1) % total
                st.session_state.fc_flipped = False
                st.rerun()
        with c_r3:
            if st.button("🟡 Medium", use_container_width=True):
                st.session_state.fc_index = (curr_idx + 1) % total
                st.session_state.fc_flipped = False
                st.rerun()
        with c_r4:
            if st.button("🟢 Easy", use_container_width=True):
                st.session_state.fc_index = (curr_idx + 1) % total
                st.session_state.fc_flipped = False
                st.rerun()


def render_pomodoro_widget(plan: Optional[StudyPlan], on_complete_topic_cb=None):
    """Render an integrated study timer widget on the dashboard."""
    st.markdown("### ⏱️ Focus Study Session (Pomodoro Mode)")

    if not plan or not plan.daily_schedule:
        st.info("Generate a study plan to activate the Focus Timer.")
        return

    day1 = [s for s in plan.daily_schedule if s.day == 1 and s.session_type != "Break"]
    if not day1:
        day1 = plan.daily_schedule[:3]

    session_labels = [f"{s.time_slot} | {s.subject}: {s.topic}" for s in day1]
    selected_sess_idx = st.selectbox("Current Active Session:", range(len(session_labels)), format_func=lambda i: session_labels[i])
    current_sess = day1[selected_sess_idx]

    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.markdown(
            f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #6366f1; text-transform: uppercase;">ACTIVE FOCUS TARGET</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-top: 4px;">{current_sess.subject} — {current_sess.topic}</div>
                <div style="font-size: 0.85rem; color: #64748b; margin-top: 4px;">Scheduled: {current_sess.time_slot} ({current_sess.duration_hours}h)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_t2:
        interval = st.radio("Focus Interval:", ["25 mins (Pomodoro)", "50 mins (Deep Work)"], horizontal=True)
        if st.button("✅ Mark Session Finished", type="primary", use_container_width=True):
            if on_complete_topic_cb:
                on_complete_topic_cb(current_sess.topic)

