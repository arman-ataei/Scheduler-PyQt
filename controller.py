# controller.py
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTime
from model import DatabaseModel # Ensure model.py is in your PYTHONPATH
from custom_types import Status, TaskData
from view import MainView

class MainController:
    def __init__(self, model: DatabaseModel, view: MainView):
        self.model = model
        self.view = view
        self.current_task_id = None  # Holds the ID of the task being edited (None if adding a new task)
        # Connect UI signals to controller methods.
        self.view.submit_button.clicked.connect(self.handle_submit)
        # handle_delete deletes the selected task, refreshes the view, and resets the form.
        self.view.delete_button.clicked.connect(self.handle_delete)
        # handle_cancel clears the form and cancel the update
        self.view.cancel_update_button.clicked.connect(self.handle_cancel)
        # connect the double-click signal from the tasks table to a handler that
        # loads the task into the form.
        self.view.tasks_table.itemDoubleClicked.connect(self.handle_task_selection)
        # Load tasks for the currently selected date.
        self.load_tasks_for_date(self.view.date_edit.date().toString("yyyy-MM-dd"))
        # Reload tasks if the date is changed.
        self.view.date_edit.dateChanged.connect(self.handle_date_change)

    def handle_submit(self):
        # Retrieve and validate input data from the view.
        date_qdate = self.view.date_edit.date()
        date_str = date_qdate.toString("yyyy-MM-dd")

        start_time_str = self.view.start_time_edit.time().toString("HH:mm")
        task_description = self.view.task_description_edit.toPlainText().strip()
        if not task_description:
            self.view.show_message("Validation Error", "Task description cannot be empty.")
            return

        estimated_duration_str = self.view.estimated_duration_edit.time().toString("HH:mm")
        importance = self.view.importance_spin.value()
        urgency = self.view.urgency_spin.value()
        status = self.view.status_combo.currentData()
        if not isinstance(status, Status):
            print(type(status), isinstance(status, Status))
            self.view.show_message("Validation Error", "Invalid status selected.")
            return

        # Create a new TaskData instance.
        new_task = TaskData(
            date=date_str,
            start_time=start_time_str,
            task_description=task_description,
            estimated_duration=estimated_duration_str,
            importance=importance,
            urgency=urgency,
            priority=urgency + importance,
            status=status
        )
        if self.current_task_id is None:
            # Adding a new task
            self.model.add_task(new_task)
            self.view.show_message("Success", "Task added successfully!")
        else:
            # Updating an existing task.
            self.model.update_task(self.current_task_id, new_task)
            self.view.show_message("Success", "Task updated successfully!")
            # Reset update mode.
            self.current_task_id = None
            self.view.submit_button.setText("Add Task")

        # Clear the form and refresh task display.
        self.view.clear_form()
        self.load_tasks_for_date(date_str)
    
    def handle_delete(self):
        if self.current_task_id is None:
            return  # Nothing to delete.
        # Delete the task from the database.
        self.model.delete_task(self.current_task_id)
        self.view.show_message("Success", "Task deleted successfully!")
        self.current_task_id = None
        self.view.clear_form()
        self.load_tasks_for_date(self.view.date_edit.date().toString("yyyy-MM-dd"))

    def handle_cancel(self):
        def yes_handle():
            self.current_task_id = None
            self.view.cancel_update_button.setEnabled(False)
            self.view.delete_button.setEnabled(False)
            self.view.submit_button.setText("Add Task")
            self.view.clear_form()

        def no_handle():
            return
        
        self.view.cancel_confirmed_message(yes_handle, no_handle)
        self.load_tasks_for_date(self.view.date_edit.date().toString("yyyy-MM-dd"))

    def handle_task_selection(self, item):
        row = item.row()
        # Retrieve task ID from the first column.
        task_id_item = self.view.tasks_table.item(row, 0)
        if not task_id_item:
            return
        task_id = int(task_id_item.text())
        self.current_task_id = task_id

        # Load task data from the table row into the form.
        description = self.view.tasks_table.item(row, 1).text()
        start_time = self.view.tasks_table.item(row, 2).text()
        duration = self.view.tasks_table.item(row, 3).text()
        priority_text = self.view.tasks_table.item(row, 6).text()
        importance_text = self.view.tasks_table.item(row, 4).text()
        urgency_text = self.view.tasks_table.item(row, 5).text()
        status_text = self.view.tasks_table.item(row, 7).text()  # e.g., "Not_Started"

        # Set values in the form.
        # Parse time strings into QTime.
        try:
            h, m = map(int, start_time.split(":"))
            self.view.start_time_edit.setTime(QTime(h, m))
        except Exception:
            pass

        try:
            h, m = map(int, duration.split(":"))
            self.view.estimated_duration_edit.setTime(QTime(h, m))
        except Exception:
            pass

        self.view.task_description_edit.setPlainText(description)
        self.view.importance_spin.setValue(int(importance_text))
        self.view.urgency_spin.setValue(int(urgency_text))

        # Convert status_text to Status enum.
        try:
            status_enum = Status[status_text]
            index = self.view.status_combo.findData(status_enum)
            if index != -1:
                self.view.status_combo.setCurrentIndex(index)
        except KeyError:
            pass

        # Change the submit button text to indicate update mode and enable delete.
        self.view.submit_button.setText("Update Task")
        self.view.delete_button.setEnabled(True)
        self.view.cancel_update_button.setEnabled(True)

    def load_tasks_for_date(self, date_str: str):
        tasks = self.model.get_tasks_by_date(date_str)
        self.view.tasks_table.setRowCount(0)
        for row_number, task in enumerate(tasks):
            self.view.tasks_table.insertRow(row_number)
            for col_number, value in enumerate(task):
                # Convert the status integer back to the status name.
                if col_number == 7:
                    value = Status(value).name
                item = QTableWidgetItem(str(value))
                self.view.tasks_table.setItem(row_number, col_number, item)

    def handle_date_change(self):
        date_str = self.view.date_edit.date().toString("yyyy-MM-dd")
        self.load_tasks_for_date(date_str)
