import plotly.graph_objects as go


def create_map_figure(filtered_df):
    fig = go.Figure()

    # Add task markers
    for status in ["Upcoming", "In Progress", "Overdue", "Completed"]:
        status_df = filtered_df[filtered_df["status"] == status]
        if len(status_df) > 0:
            fig.add_trace(
                go.Scatter(
                    x=status_df["x"],
                    y=status_df["y"],
                    mode="markers+text",
                    name=status,
                    marker=dict(
                        size=status_df["size"],
                        color=status_df["color"],
                        symbol="circle",
                        line=dict(color="white", width=2),
                    ),
                    text=status_df["city"],
                    textposition="bottom center",
                    textfont=dict(size=10, color="white"),
                    customdata=status_df[["name", "city", "start_date", "end_date", "days_until", "status"]],
                    hovertemplate="<b>%{customdata[0]}</b><br>"
                    + "Location: %{customdata[1]}<br>"
                    + "Start: %{customdata[2]|%Y-%m-%d}<br>"
                    + "End: %{customdata[3]|%Y-%m-%d}<br>"
                    + "Days Until: %{customdata[4]}<br>"
                    + "Status: %{customdata[5]}<extra></extra>",
                )
            )

    # Update layout
    fig.update_layout(
        height=600,
        plot_bgcolor="#1f2937",
        paper_bgcolor="#111827",
        font=dict(color="white"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", showticklabels=False, range=[-5, 105]),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", showticklabels=False, range=[-5, 105]),
        showlegend=True,
        legend=dict(bgcolor="rgba(31,41,55,0.8)", bordercolor="rgba(255,255,255,0.3)", borderwidth=1),
        hovermode="closest",
    )

    return fig
