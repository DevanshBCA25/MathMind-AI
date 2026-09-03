from __future__ import annotations

import streamlit as st

from src.analytics.analytics_engine import (
    AnalyticsEngine,
)


def show():

    st.title(
        "📊 MathMind AI — Analytics"
    )

    st.caption(
        "Application usage and performance overview."
    )

    analytics = AnalyticsEngine()

    # ========================================================
    # SUMMARY
    # ========================================================

    summary = analytics.get_summary()

    st.subheader(
        "📈 System Summary"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Total Events",
            summary[
                "total_events"
            ],
        )

    with col2:

        st.metric(
            "Successful",
            summary[
                "successful_events"
            ],
        )

    with col3:

        st.metric(
            "Errors",
            summary[
                "error_events"
            ],
        )

    with col4:

        st.metric(
            "Success Rate",
            f'{summary["success_rate"]}%',
        )

    st.divider()

    # ========================================================
    # MODULE STATISTICS
    # ========================================================

    st.subheader(
        "🧩 Module Usage"
    )

    module_stats = (
        analytics.module_statistics()
    )

    if module_stats:

        st.bar_chart(
            module_stats
        )

    else:

        st.info(
            "No module usage data available yet."
        )

    st.divider()

    # ========================================================
    # STATUS
    # ========================================================

    st.subheader(
        "📋 Status Distribution"
    )

    status_stats = (
        analytics.status_statistics()
    )

    if status_stats:

        st.bar_chart(
            status_stats
        )

    else:

        st.info(
            "No status data available yet."
        )

    st.divider()

    # ========================================================
    # EVENT TYPES
    # ========================================================

    st.subheader(
        "⚡ Event Types"
    )

    event_stats = (
        analytics.event_statistics()
    )

    if event_stats:

        st.bar_chart(
            event_stats
        )

    else:

        st.info(
            "No event data available yet."
        )

    st.divider()

    # ========================================================
    # RAW EVENTS
    # ========================================================

    with st.expander(
        "🔧 Raw Analytics Events"
    ):

        events = analytics.get_events()

        if events:

            st.json(
                events
            )

        else:

            st.info(
                "No events recorded."
            )

    st.divider()

    # ========================================================
    # CLEAR DATA
    # ========================================================

    st.subheader(
        "🗑 Analytics Management"
    )

    if st.button(
        "Clear Analytics Data",
        use_container_width=True,
    ):

        analytics.clear_events()

        st.success(
            "Analytics data cleared successfully."
        )

        st.rerun()