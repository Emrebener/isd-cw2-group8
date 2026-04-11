from tasks import Task, RecurringTask
import datetime
import csv
import pickle


class TaskTestDAO:
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

    def get_all_tasks(self) -> list[Task]:
        task_list = [
            Task("Buy groceries", datetime.datetime.now() - datetime.timedelta(days=4)),
            Task("Do laundry", datetime.datetime.now() - datetime.timedelta(days=-2)),
            Task("Clean room", datetime.datetime.now() + datetime.timedelta(days=-1)),
            Task("Do homework", datetime.datetime.now() + datetime.timedelta(days=3)),
            Task("Walk dog", datetime.datetime.now() + datetime.timedelta(days=5)),
            Task("Do dishes", datetime.datetime.now() + datetime.timedelta(days=6))
        ]

        r_task = RecurringTask("Go to the gym", datetime.datetime.now(), datetime.timedelta(days=7))
        r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=7))
        r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=14))
        r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=22))
        r_task.date_created = datetime.datetime.now() - datetime.timedelta(days=28)

        task_list.append(r_task)

        return task_list

    def save_all_tasks(self, tasks: list[Task]) -> None:
        pass


class TaskCsvDAO:
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path
        self.fieldnames = ["title", "type", "date_due", "completed", "interval", "completed_dates", "date_created"]

    def get_all_tasks(self) -> list[Task]:
        task_list: list[Task] = []
        with open(self.storage_path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                task_type = row["type"]
                task_title = row["title"]
                task_date_due = row["date_due"]
                task_completed = row["completed"]
                task_interval = row["interval"]
                task_date_created = row["date_created"]
                task_completed_dates = row["completed_dates"]

                task: Task | RecurringTask

                if task_type == "RecurringTask":
                    interval_days = int(task_interval.split(" ")[0])
                    task = RecurringTask(task_title, datetime.datetime.strptime(task_date_due, "%Y-%m-%d"), datetime.timedelta(days=interval_days))
                    task.completed_dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in task_completed_dates.split(",")]
                    task.date_created = datetime.datetime.strptime(task_date_created, "%Y-%m-%d")
                else:
                    task = Task(task_title, datetime.datetime.strptime(task_date_due, "%Y-%m-%d"))
                    task.date_created = datetime.datetime.strptime(task_date_created, "%Y-%m-%d")

                task.completed = True if task_completed.lower() == "true" else False

                task_list.append(task)
        return task_list

    def save_all_tasks(self, tasks: list[Task]) -> None:
        with open(self.storage_path, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for task in tasks:
                row = {}

                row["title"] = task.title
                row["type"] = "RecurringTask" if isinstance(task, RecurringTask) else "Task"
                row["date_due"] = task.date_due.strftime("%Y-%m-%d")
                row["completed"] = str(task.completed)
                row["interval"] = str(task.interval) if isinstance(task, RecurringTask) else ""
                row["completed_dates"] = ",".join([date.strftime("%Y-%m-%d") for date in task.completed_dates]) if isinstance(task, RecurringTask) else ""
                row["date_created"] = task.date_created.strftime("%Y-%m-%d")
                writer.writerow(row)


class TaskPickleDAO:
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

    def get_all_tasks(self) -> list[Task]:
        with open(self.storage_path, "rb") as file:
            task_list = pickle.load(file)
        return task_list

    def save_all_tasks(self, tasks: list[Task]) -> None:
        with open(self.storage_path, "wb") as file:
            pickle.dump(tasks, file)