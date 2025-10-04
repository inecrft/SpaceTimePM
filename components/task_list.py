import streamlit as st

from config import STATUS_EMOJIS


def render_task_list(filtered_df):
    st.subheader("📋 Task List")

    if len(filtered_df) > 0:
        # Sort by days until
        display_df = filtered_df.sort_values("days_until")

        for _, task in display_df.iterrows():
            with st.container():
                st.markdown(f"**{STATUS_EMOJIS[task['status']]} {task['name']}**")
                st.caption(f"📍 {task['city']} | 📅 {task['days_until']}d")

                # Expandable details
                with st.expander("View Details"):
                    st.write(f"**Status:** {task['status']}")
                    st.write(f"**Location:** {task['city']}")
                    st.write(f"**Start Date:** {task['start_date'].strftime('%Y-%m-%d')}")
                    st.write(f"**End Date:** {task['end_date'].strftime('%Y-%m-%d')}")
                    st.write(f"**Days Until Start:** {task['days_until']} days")

                st.divider()
    else:
        st.warning("⚠️ No tasks match the current filters. Try adjusting your filter settings.")
        st.info("💡 Tip: Enable more statuses or increase the time range to see more tasks.")
