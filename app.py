from datetime import date

import pandas as pd
import streamlit as st

from components import render_map_view, render_metrics, render_sidebar, render_task_list
from data import TaskManager
from utils import filter_tasks_by_time, prepare_task_dataframe, filter_tasks_by_status

# Page config
st.set_page_config(page_title="Spatio-Temporal Project Manager", layout="wide")


@st.cache_resource
def get_task_manager():
    return TaskManager.from_csv("./data/sample_tasks.csv")


# Initialize
task_manager = get_task_manager()
today = pd.Timestamp(date.today())

# Title and description
st.title("🗺️ Space Time Project Manager")
st.markdown("*Visualizing tasks across space and time*")

# Sidebar for controls
with st.sidebar:
    time_range, status_filter = render_sidebar(today)

# Prepare data
df = prepare_task_dataframe(task_manager.get_all_tasks(), today)

filtered_df = filter_tasks_by_time(df, time_range)
filtered_df = filter_tasks_by_status(filtered_df, status_filter)

if status_filter:
    filter_summary = f"**Filters Active** Time ≤ {time_range} days | Status: {', '.join(status_filter)}"
else:
    filter_summary = "**⚠️ No status selected** - Please select at least one status to view tasks"
st.caption(filter_summary)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    render_map_view(filtered_df, len(df))

with col2:
    render_task_list(filtered_df)

# Footer with stats
st.markdown("---")

st.subheader("📊 Overall Task Statistics")
render_metrics(df)

if len(filtered_df) < len(df):
    st.subheader("📋 Filtered Task Statistics")
    render_metrics(filtered_df)
