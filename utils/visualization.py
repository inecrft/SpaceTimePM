import folium

from config import DEFAULT_MAP_CENTER, DEFAULT_MAP_ZOOM, STATUS_EMOJIS


def calculate_opacity(days_until, max_days=35):
    if days_until <= 3:
        return 1

    normalized = min(max(days_until - 3, 0), max_days - 3) / (max_days - 3)
    opacity = 1 - normalized * 0.9

    return max(opacity, 0.1)


def calculate_radius(days_until, status, base_size=15):
    if status == "Overdue":
        return base_size + 10

    if days_until <= 3:
        return base_size + 5

    return base_size


def should_pulse(days_until, status):
    if status in ["Overdue", "In Progress"]:
        return True
    if status == "Upcoming" and days_until <= 3:
        return True
    return False


def create_custom_icon(color, pulsing=False):
    pulse_animation = (
        """
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 {color}80; }
            50% { box-shadow: 0 0 0 10px {color}00; }
            100% { box-shadow: 0 0 0 0 {color}80; }
        }
    """.format(
            color=color
        )
        if pulsing
        else ""
    )

    animation_style = "animation: pulse 2s infinite;" if pulsing else ""

    return f"""
        <style>
            {pulse_animation}
            .custom-marker {{
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background-color: {color};
                border: 3px solid white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                {animation_style}
            }}
        </style>
        <div class="custom-marker"></div>
    """


def create_popup_html(task):
    emoji = STATUS_EMOJIS.get(task["status"], "⚪")

    urgent_badge = ""
    if should_pulse(task["days_until"], task["status"]):
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
            <div style="background-color: #f0f0f0; border-radius: 10px; height: 20px; margin-top: 10px;">
                <div style="background-color: {task['color']}; width: {task['progress']}%; height: 100%; border-radius: 10px; transition: width 0.3s;"></div>
            </div>
            <p style="margin: 5px 0; font-size: 11px; color: #666;">Progress: {task['progress']}%</p>
        </div>
    """


def create_folium_map(filtered_df):
    # Create base map
    m = folium.Map(
        location=DEFAULT_MAP_CENTER,
        zoom_start=DEFAULT_MAP_ZOOM,
        tiles="OpenStreetMap",  # Options: 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'CartoDB positron'
    )

    if len(filtered_df) == 0:
        return m

    # Calculate visual properties
    filtered_df = filtered_df.copy()
    filtered_df["opacity"] = filtered_df["days_until"].apply(calculate_opacity)
    filtered_df["radius"] = filtered_df.apply(lambda row: calculate_radius(row["days_until"], row["status"]), axis=1)
    filtered_df["pulsing"] = filtered_df.apply(lambda row: should_pulse(row["days_until"], row["status"]), axis=1)

    # Add markers for each task
    for _, task in filtered_df.iterrows():
        # Create glow effect for pulsing tasks (outer circle)
        if task["pulsing"]:
            folium.Circle(
                location=[task["lat"], task["lng"]],
                radius=task["radius"] * 100,  # Convert to meters (approximate)
                color=task["color"],
                fill=True,
                fillColor=task["color"],
                fillOpacity=0.15,
                weight=0,
            ).add_to(m)

        # Main marker (CircleMarker for consistent size)
        folium.CircleMarker(
            location=[task["lat"], task["lng"]],
            radius=task["radius"],
            color="white",
            weight=3 if task["pulsing"] else 2,
            fill=True,
            fillColor=task["color"],
            fillOpacity=task["opacity"],
            popup=folium.Popup(create_popup_html(task), max_width=300),
            tooltip=f"{task['name']} - {task['city']} ({task['days_until']}d)",
        ).add_to(m)

    # Add layer control (optional - allows switching map styles)
    folium.TileLayer("Stamen Terrain").add_to(m)
    folium.TileLayer("CartoDB positron").add_to(m)
    folium.LayerControl().add_to(m)

    # Fit bounds to show all markers
    if len(filtered_df) > 0:
        bounds = [
            [filtered_df["lat"].min(), filtered_df["lng"].min()],
            [filtered_df["lat"].max(), filtered_df["lng"].max()],
        ]
        m.fit_bounds(bounds, padding=[50, 50])

    return m
