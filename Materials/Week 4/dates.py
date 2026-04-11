import datetime

date = datetime.datetime(2021, 1, 1, 12, 0)
date = datetime.datetime.strptime("2021-01-01 12:00", "%Y-%m-%d %H:%M")

def __init__(self, title, date_due):
    self.title = title
    self.date_created = datetime.datetime.now()
    self.completed = False
    self.date_due = date_due