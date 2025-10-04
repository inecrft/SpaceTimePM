import streamlit as st

from utils import create_map_figure


def render_map_view(filtered_df, total_tasks):
    st.subheader("🗺️ Task Map")

    if len(filtered_df) > 0:
        fig = create_map_figure(filtered_df)

        # Display the map
        st.plotly_chart(fig, use_container_width=True, key="map", on_select="rerun")

        # Show count
        st.caption(f"Showing {len(filtered_df)} of {total_tasks} tasks")
    else:
        st.warning("No tasks in the selected time range. Adjust the time filter.")
