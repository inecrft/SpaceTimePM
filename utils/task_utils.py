import pandas as pd

from config import DEFAULT_MARKER_SIZE, STATUS_COLORS


def get_task_status(row, today):
    if row["completed"]:
        return "Completed"
    elif row["end_date"] < today:
        return "Overdue"
    elif row["start_date"] <= today <= row["end_date"]:
        return "In Progress"
    else:
        return "Upcoming"


def get_task_color(status):
    return STATUS_COLORS.get(status, STATUS_COLORS["Upcoming"])


def get_days_until(date, today):
    return (date - today).days


def prepare_task_dataframe(tasks_data, today):
    df = pd.DataFrame(tasks_data)
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])
    df["days_until"] = df["start_date"].apply(lambda x: get_days_until(x, today))
    df["status"] = df.apply(lambda row: get_task_status(row, today), axis=1)
    df["color"] = df["status"].apply(get_task_color)
    df["size"] = DEFAULT_MARKER_SIZE
    return df


def filter_tasks_by_time(df, time_range):
    return df[df["days_until"] <= time_range].copy()


def get_status_counts(df):
    return {
        "Upcoming": len(df[df["status"] == "Upcoming"]),
        "In Progress": len(df[df["status"] == "In Progress"]),
        "Overdue": len(df[df["status"] == "Overdue"]),
        "Completed": len(df[df["status"] == "Completed"]),
    }
