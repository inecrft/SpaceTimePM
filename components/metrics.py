import streamlit as st

from utils import get_status_counts


def render_metrics(filtered_df):
    counts = get_status_counts(filtered_df)

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        st.metric("Upcoming", counts["Upcoming"])

    with col_b:
        st.metric("In Progress", counts["In Progress"])

    with col_c:
        st.metric("Overdue", counts["Overdue"])

    with col_d:
        st.metric("Completed", counts["Completed"])
