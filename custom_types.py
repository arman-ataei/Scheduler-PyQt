import datetime

from dataclasses import dataclass
from enum import Enum
# Define the Status enum.
class Status(Enum):
    Not_Started = 0
    In_Progress = 1
    Completed = 2

# Define a dataclass representing a task.
@dataclass
class TaskData:
    date: str = str(datetime.date.today())
    start_time: str = "00:00"
    task_description: str = "Describe the Task"
    estimated_duration: str = "00:30"
    urgency: int = 10
    importance:int=10
    priority:int = urgency + importance
    status: Status = Status.Not_Started