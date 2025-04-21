# view.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFormLayout, QTextEdit, QSpinBox, QComboBox,
    QPushButton, QMessageBox, QVBoxLayout,  QHBoxLayout, QLabel, QDateEdit, QTimeEdit,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QDate, QTime
from enum import Enum

from custom_types import Status

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Schedule App")
        self.setGeometry(100, 100, 600, 500)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a form layout for task entry.
        self.form_layout = QFormLayout()

        # Date input.
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.form_layout.addRow("Date:", self.date_edit)

        # Start time input.
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime(0, 0))
        self.form_layout.addRow("Start Time:", self.start_time_edit)

        # Task description input.
        self.task_description_edit = QTextEdit()
        self.form_layout.addRow("Task Description:", self.task_description_edit)

        # Estimated duration input.
        self.estimated_duration_edit = QTimeEdit()
        self.estimated_duration_edit.setTime(QTime(0, 30))
        self.form_layout.addRow("Estimated Duration:", self.estimated_duration_edit)

        # Importance input.
        self.importance_spin = QSpinBox()
        self.importance_spin.setRange(0, 11)
        self.importance_spin.setValue(10)
        self.form_layout.addRow("Importance (0-10):", self.importance_spin)

        # Urgency input.
        self.urgency_spin = QSpinBox()
        self.urgency_spin.setRange(0, 11)
        self.urgency_spin.setValue(10)
        self.form_layout.addRow("Urgency (0-10):", self.urgency_spin)

        # Status input.
        self.status_combo = QComboBox()
        self.status_combo.addItem("Not Started", Status.Not_Started)
        self.status_combo.addItem("In Progress", Status.In_Progress)
        self.status_combo.addItem("Completed", Status.Completed)
        self.form_layout.addRow("Status:", self.status_combo)

        # Create a horizontal layout for the Add/Update and Delete buttons.
        btn_layout = QHBoxLayout()
        self.submit_button = QPushButton("Add Task")
        btn_layout.addWidget(self.submit_button)
        
        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setEnabled(False)  # Disabled by default.
        btn_layout.addWidget(self.delete_button)
        
        self.cancel_update_button = QPushButton("Cancel")
        self.cancel_update_button.setEnabled(False)
        btn_layout.addWidget(self.cancel_update_button)

        self.form_layout.addRow(btn_layout)

        # Table widget to display tasks.
        self.tasks_table = QTableWidget(0,8)
        self.tasks_table.setHorizontalHeaderLabels(
            ["id","Description","Start Time", "E-End Time", "Importance", "Urgency","Priority", "Status"]
        )
        self.tasks_table.hideColumn(0)

        # Combine the layouts.
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(QLabel("Tasks:"))
        main_layout.addWidget(self.tasks_table)
        central_widget.setLayout(main_layout)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
    
    def cancel_confirmed_message(self, yes_handle, no_handle):
        # Create a QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)  # Set the icon as a question mark
        msg_box.setWindowTitle("Confirmation")  # Set the window title
        msg_box.setText("Do you want to Cancel Changes?")  # Set the message
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # Add Yes and No buttons

        # Execute the message box and capture the user's response
        response = msg_box.exec()

        # Check which button was clicked
        if response == QMessageBox.Yes:
            # print("User selected Yes.")
            yes_handle()

        elif response == QMessageBox.No:
            # print("User selected No.")
            no_handle()

    def clear_form(self):
        self.task_description_edit.clear()
        self.start_time_edit.setTime(QTime(0, 0))
        self.estimated_duration_edit.setTime(QTime(0, 30))
        self.importance_spin.setValue(0)
        self.urgency_spin.setValue(0)
        self.status_combo.setCurrentIndex(0)
        # Reset the buttons.
        self.submit_button.setText("Add Task")
        self.delete_button.setEnabled(False)
        self.cancel_update_button.setEnabled(False)