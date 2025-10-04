import streamlit as st

from config import MAX_TIME_RANGE_DAYS, STATUS_EMOJI


def render_sidebar(today):
    st.header("⚙️ Controls")

    # Current date
    st.info(f"📅 Current Date: {today.strftime('%Y-%m-%d')}")

    # Time filter slider
    st.subheader("🕐 Time Filter")
    time_range = st.slider(
        "Show tasks within next X days:",
        min_value=0,
        max_value=MAX_TIME_RANGE_DAYS,
        value=MAX_TIME_RANGE_DAYS,
        help="Filter tasks by how many days in the future to show",
    )

    st.markdown("---")

    st.subheader("📊 Status Filter")
    all_statuses = ['Upcoming', 'In Progress', 'Overdue', 'Completed']
    select_all = st.checkbox("Select All", value=True, key="select_all_status")
    if select_all:
        status_filter = all_statuses.copy()
        for status in all_statuses:
            st.checkbox(
                f"{STATUS_EMOJI[status]} {status}",
                value=True,
                disabled=True,
                key=f"status_{status}"
            )
    else:
        status_filter = []
        for status in all_statuses:
            if st.checkbox(
                f"{STATUS_EMOJI[status]} {status}",
                value=True,
                key=f"status_{status}"
            ):
                status_filter.append(status)
    
    st.markdown("---")

    # Legend
    st.subheader("📊 Status Legend")
    st.markdown(
        """
    🔵 **Upcoming** - Not started yet  
    🟡 **In Progress** - Currently active  
    🔴 **Overdue** - Past due date  
    🟢 **Completed** - Finished
    """
    )

    return time_range, status_filter
