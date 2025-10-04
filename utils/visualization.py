import plotly.graph_objects as go


def calculate_opacity(days_until, max_days=35):
    if days_until <= 3:
        return 1

    normalized = min(max(days_until - 3, 0), max_days - 3) / (max_days - 3)
    opacity = 1 - normalized * 0.9

    return max(opacity, 0.1)


def calculate_marker_size(days_until, status, base_size=30):
    if status == "Overdue":
        return base_size + 10

    if days_until <= 3:
        return base_size + 5

    return base_size


def should_pulse(days_until, status):
    if status == "Overdue" or status == "In Progress":
        return True
    if status == "Upcoming" and days_until <= 3:
        return True
    return False


def create_map_figure(filtered_df):
    fig = go.Figure()

    # Add task markers
    filtered_df = filtered_df.copy()
    filtered_df["opacity"] = filtered_df["days_until"].apply(calculate_opacity)
    filtered_df["marker_size"] = filtered_df.apply(
        lambda row: calculate_marker_size(row["days_until"], row["status"]), axis=1
    )
    filtered_df["should_pulse"] = filtered_df.apply(lambda row: should_pulse(row["days_until"], row["status"]), axis=1)
    for status in ["Upcoming", "In Progress", "Overdue", "Completed"]:
        status_df = filtered_df[filtered_df["status"] == status]
        if len(status_df) > 0:
            pulsing_df = status_df[status_df["should_pulse"]]
            non_pulsing_df = status_df[~status_df["should_pulse"]]

            if len(non_pulsing_df) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=non_pulsing_df["x"],
                        y=non_pulsing_df["y"],
                        mode="markers+text",
                        name=status,
                        marker=dict(
                            size=non_pulsing_df["size"],
                            color=non_pulsing_df["color"],
                            opacity=non_pulsing_df["opacity"],
                            symbol="circle",
                            line=dict(color="white", width=2),
                        ),
                        text=non_pulsing_df["city"],
                        textposition="bottom center",
                        textfont=dict(size=10, color="white"),
                        customdata=non_pulsing_df[["name", "city", "start_date", "end_date", "days_until", "status"]],
                        hovertemplate="<b>%{customdata[0]}</b><br>"
                        + "Location: %{customdata[1]}<br>"
                        + "Start: %{customdata[2]|%Y-%m-%d}<br>"
                        + "End: %{customdata[3]|%Y-%m-%d}<br>"
                        + "Days Until: %{customdata[4]}<br>"
                        + "Status: %{customdata[5]}<extra></extra>",
                        showlegend=True if len(pulsing_df) == 0 else False,
                    )
                )

            if len(pulsing_df) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=pulsing_df["x"],
                        y=pulsing_df["y"],
                        mode="markers",
                        name=status + " (Urgent)",
                        marker=dict(
                            size=pulsing_df["marker_size"] + 20,
                            color=pulsing_df["color"],
                            opacity=0.2,
                            symbol="circle",
                            line=dict(width=0),
                        ),
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=pulsing_df["x"],
                        y=pulsing_df["y"],
                        mode="markers",
                        marker=dict(
                            size=pulsing_df["marker_size"] + 10,
                            color=pulsing_df["color"],
                            opacity=0.4,
                            symbol="circle",
                            line=dict(width=0),
                        ),
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=pulsing_df["x"],
                        y=pulsing_df["y"],
                        mode="markers+text",
                        name=status,
                        marker=dict(
                            size=pulsing_df["marker_size"],
                            color=pulsing_df["color"],
                            opacity=1.0,
                            symbol="circle",
                            line=dict(color="white", width=3),
                        ),
                        text=pulsing_df["city"],
                        textposition="bottom center",
                        textfont=dict(size=10, color="white", family="Arial Black"),
                        customdata=pulsing_df[["name", "city", "start_date", "end_date", "days_until", "status"]],
                        hovertemplate="<b>"
                        + ("⚠️ URGENT: " if status == "Overdue" else "")
                        + "%{customdata[0]}</b><br>"
                        + "Location: %{customdata[1]}<br>"
                        + "Start: %{customdata[2]|%Y-%m-%d}<br>"
                        + "End: %{customdata[3]|%Y-%m-%d}<br>"
                        + "Days Until: %{customdata[4]}<br>"
                        + "Status: %{customdata[5]}<extra></extra>",
                        showlegend=True if len(non_pulsing_df) == 0 else False,
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
