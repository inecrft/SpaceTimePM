import streamlit as st

from utils import create_map_figure


def render_map_view(filtered_df, total_tasks):
    st.subheader("🗺️ Task Map")

    if len(filtered_df) > 0:
        fig = create_map_figure(filtered_df)

        # Display the map
        st.plotly_chart(fig, use_container_width=True, key="map", on_select="rerun")

        # Show count
        if len(filtered_df) < total_tasks:
            st.caption(
                f"Showing {len(filtered_df)} of {total_tasks} tasks"
                f"({(len(filtered_df) / total_tasks * 100):.1f}% visible)"
            )
        else:
            st.caption(f"Showing all {len(filtered_df)} tasks")
    else:
        st.warning("⚠️ No tasks match the current filters. Try adjusting your filter settings.")
        st.info("💡 Tip: Enable more statuses or increase the time range to see more tasks.")
