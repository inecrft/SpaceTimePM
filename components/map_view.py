import streamlit as st
from streamlit_folium import st_folium

from utils import create_folium_map


def render_map_view(filtered_df, total_tasks):
    st.subheader("🗺️ Task Map")

    if len(filtered_df) > 0:
        folium_map = create_folium_map(filtered_df)

        # Display the map
        st_folium(folium_map, width=None, height=600, returned_objects=[])

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
