# model.py
import sqlite3

from custom_types import TaskData, Status


class DatabaseModel:
    def __init__(self, db_name="schedule.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Create the Days table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE
            )
        ''')
        # Create the Tasks table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                start_time TEXT,
                task_description TEXT,
                estimated_duration TEXT,
                importance INTEGER,
                urgency INTEGER,
                priority INTEGER,
                status INTEGER,
                FOREIGN KEY(date) REFERENCES Days(date)
            )
        ''')
        self.conn.commit()

    def add_day_if_not_exists(self, date_str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM Days WHERE date = ?", (date_str,))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO Days (date) VALUES (?)", (date_str,))
            self.conn.commit()

    def add_task(self, task: TaskData):
        self.add_day_if_not_exists(task.date)
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO Tasks (date, start_time, task_description, estimated_duration,
                               priority, urgency, importance, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.date, 
            task.start_time, 
            task.task_description, 
            task.estimated_duration,
            task.priority, 
            task.urgency, 
            task.importance,
            task.status.value
        ))
        self.conn.commit()

    def update_task(self, task_id: int, task: TaskData):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE Tasks
            SET date = ?, start_time = ?, task_description = ?, estimated_duration = ?,
                priority = ?, urgency = ?, importance = ?, status = ?
            WHERE id = ?
        ''', (
            task.date, task.start_time, task.task_description, task.estimated_duration,
            task.priority, task.urgency, task.importance, task.status.value, task_id
        ))
        self.conn.commit()
    
    
    def delete_task(self, task_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def get_tasks_by_date(self, date_str):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, task_description, start_time, estimated_duration, importance, urgency, priority, status
            FROM Tasks
            WHERE date = ?
            ORDER BY start_time
        ''', (date_str,))
        return cursor.fetchall()
    
