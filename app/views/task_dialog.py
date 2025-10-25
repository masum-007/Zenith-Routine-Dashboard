from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTimeEdit, QTextEdit,
    QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QComboBox
)
from PyQt6.QtCore import QTime


class TaskDialog(QDialog):
    def __init__(self, categories: list, task_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Details" if not task_data else "Edit Task")
        self.setMinimumWidth(400)
        self.categories = categories

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(10, 10, 10, 10)

        self.name_input = QLineEdit()
        self.name_input.setObjectName("formInput")

        self.start_time_input = QTimeEdit()
        self.start_time_input.setObjectName("formInput")
        self.start_time_input.setDisplayFormat("h:mm AP")

        self.end_time_input = QTimeEdit()
        self.end_time_input.setObjectName("formInput")
        self.end_time_input.setDisplayFormat("h:mm AP")

        # --- NEW: Category Dropdown ---
        self.category_input = QComboBox()
        self.category_input.setObjectName("formInput")
        for category in self.categories:
            self.category_input.addItem(category['name'], category['id'])

        self.notes_input = QTextEdit()
        self.notes_input.setObjectName("formInput")
        self.notes_input.setPlaceholderText(
            "Add any details or sub-tasks here...")
        self.notes_input.setMinimumHeight(80)

        form_layout.addRow("Task Name:", self.name_input)
        form_layout.addRow("Category:", self.category_input)  # Add new row
        form_layout.addRow("Start Time:", self.start_time_input)
        form_layout.addRow("End Time:", self.end_time_input)
        form_layout.addRow("Notes:", self.notes_input)
        main_layout.addLayout(form_layout)

        # Button Layout
        btn_layout = QHBoxLayout()
        btn_layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("dialogSecondaryButton")
        self.save_button = QPushButton("Save Task")
        self.save_button.setObjectName("dialogPrimaryButton")
        btn_layout.addWidget(self.cancel_button)
        btn_layout.addWidget(self.save_button)
        main_layout.addLayout(btn_layout)

        # Connect signals
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # Populate data
        if task_data:
            self.name_input.setText(task_data.get('name', ''))
            self.start_time_input.setTime(QTime.fromString(
                task_data.get('start_time', '09:00'), "HH:mm"))
            self.end_time_input.setTime(QTime.fromString(
                task_data.get('end_time', '10:00'), "HH:mm"))
            self.notes_input.setText(task_data.get('notes', ''))
            # Set category dropdown
            category_id = task_data.get('category')
            index = self.category_input.findData(category_id)
            if index != -1:
                self.category_input.setCurrentIndex(index)

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "start_time": self.start_time_input.time().toString("HH:mm"),
            "end_time": self.end_time_input.time().toString("HH:mm"),
            "notes": self.notes_input.toPlainText().strip(),
            "category": self.category_input.currentData()  # Get ID from dropdown
        }
