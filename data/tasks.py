import pandas as pd


class TaskManager:
    def __init__(self, tasks_data):
        self.tasks_data = tasks_data

    def get_all_tasks(self):
        return self.tasks_data

    def add_task(self, task):
        self.tasks_data.append(task)

    def update_task(self, task_id, updates):
        for task in self.tasks_data:
            if task["id"] == task_id:
                task.update(updates)
                return True
        return False

    def delete_task(self, task_id):
        self.tasks_data = [t for t in self.tasks_data if t["id"] != task_id]

    @classmethod
    def from_csv(cls, filepath):
        df = pd.read_csv(filepath)
        return cls(df.to_dict(orient="records"))

    def to_csv(self, filepath):
        df = pd.DataFrame(self.tasks_data)
        df.to_csv(filepath, index=False)
