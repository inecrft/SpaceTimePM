import folium

from config import DEFAULT_MAP_CENTER, DEFAULT_MAP_ZOOM, STATUS_EMOJIS


def calculate_opacity(days_until, max_days=35):
    if days_until <= 3:
        return 1

    normalized = min(max(days_until - 3, 0), max_days - 3) / (max_days - 3)
    opacity = 1 - normalized * 0.9

    return max(opacity, 0.1)


def should_glow(days_until, status):
    if status in ["Overdue", "In Progress"]:
        return True
    if status == "Upcoming" and days_until <= 3:
        return True
    return False


def create_popup_html(task):
    emoji = STATUS_EMOJIS.get(task["status"], "⚪")

    urgent_badge = ""
    if should_glow(task["days_until"], task["status"]):
        urgent_badge = '<span style="background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">⚠️ URGENT</span><br>'

    return f"""
        <div style="font-family: Arial; min-width: 200px;">
            {urgent_badge}
            <h4 style="margin: 5px 0;">{emoji} {task['name']}</h4>
            <hr style="margin: 8px 0;">
            <p style="margin: 5px 0;"><b>📍 Location:</b> {task['city']}</p>
            <p style="margin: 5px 0;"><b>📅 Start:</b> {task['start_date'].strftime('%Y-%m-%d')}</p>
            <p style="margin: 5px 0;"><b>🏁 End:</b> {task['end_date'].strftime('%Y-%m-%d')}</p>
            <p style="margin: 5px 0;"><b>⏰ Days Until:</b> {task['days_until']} days</p>
            <p style="margin: 5px 0;"><b>📊 Status:</b> {task['status']}</p>
        </div>
    """


def create_folium_map(filtered_df):
    # Create base map
    m = folium.Map(
        location=DEFAULT_MAP_CENTER,
        zoom_start=DEFAULT_MAP_ZOOM,
        tiles="OpenStreetMap",
    )

    if len(filtered_df) == 0:
        return m

    # Calculate visual properties
    filtered_df = filtered_df.copy()
    filtered_df["opacity"] = filtered_df["days_until"].apply(calculate_opacity)
    filtered_df["radius"] = 15
    filtered_df["has_glow"] = filtered_df.apply(lambda row: should_glow(row["days_until"], row["status"]), axis=1)

    # Add markers for each task
    for _, task in filtered_df.iterrows():
        # Create glow effect (outer circle)
        if task["has_glow"]:
            folium.CircleMarker(
                location=[task["lat"], task["lng"]],
                radius=task["radius"] + 5,
                color=task["color"],
                fill=True,
                fillColor=task["color"],
                fillOpacity=0.4,
                weight=0,
            ).add_to(m)

        # Main marker
        folium.CircleMarker(
            location=[task["lat"], task["lng"]],
            radius=task["radius"],
            color="white",
            weight=2 if task["has_glow"] else 1,
            fill=True,
            fillColor=task["color"],
            fillOpacity=1 if task["has_glow"] else task["opacity"],
            popup=folium.Popup(create_popup_html(task), max_width=300),
            tooltip=f"{task['name']} - {task['city']} ({task['days_until']}d)",
        ).add_to(m)

    # Fit bounds to show all markers
    if len(filtered_df) > 0:
        bounds = [
            [filtered_df["lat"].min(), filtered_df["lng"].min()],
            [filtered_df["lat"].max(), filtered_df["lng"].max()],
        ]
        m.fit_bounds(bounds, padding=[50, 50])

    return m
