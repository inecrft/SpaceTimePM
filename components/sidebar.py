import streamlit as st

from config import MAX_TIME_RANGE_DAYS


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

    return time_range
