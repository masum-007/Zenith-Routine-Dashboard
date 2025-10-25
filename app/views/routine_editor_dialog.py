from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QTableWidget,
    QPushButton, QHeaderView, QAbstractItemView,
    QTableWidgetItem, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, QTime
# --- FIX: Import the correct function name ---
from ..utils.icons import get_icon
# ------------------------------------------
from .task_dialog import TaskDialog
from .category_manager_dialog import CategoryManagerDialog
import uuid


class RoutineEditorDialog(QDialog):
    # Keep track of the controller to call back for saving categories
    controller = None

    def __init__(self, routines_data: dict, categories: list, uncategorized_id: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Routine Templates")
        self.setMinimumSize(800, 600)

        self.routines = routines_data  # Working copy
        self.categories = categories  # Keep local ref for task dialog
        self.uncategorized_id = uncategorized_id
        self.current_day = "default"

        self._setup_ui()
        self._connect_signals()
        self.day_selector.setCurrentText("default")  # Trigger initial load

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # --- Top controls ---
        top_layout = QHBoxLayout()
        self.day_selector = QComboBox()
        self.day_selector.addItems([
            "default", "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ])
        top_layout.addWidget(self.day_selector)

        self.manage_categories_btn = QPushButton("Manage Categories")
        self.manage_categories_btn.setObjectName("secondaryButton")
        # Can add category icon later if needed
        top_layout.addWidget(self.manage_categories_btn)

        top_layout.addSpacerItem(QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # --- FIX: Use the correct function name 'get_icon' ---
        icon_color = "#FFFFFF"  # Icons on primary buttons are white
        secondary_icon_color = "#F0F0F5"  # Icons on secondary match text

        self.add_task_btn = QPushButton("Add Task")
        self.add_task_btn.setObjectName("dialogPrimaryButton")
        self.add_task_btn.setIcon(get_icon("plus_light"))  # Use get_icon
        self.add_task_btn.setIconSize(QSize(16, 16))

        self.edit_task_btn = QPushButton("Edit")
        self.edit_task_btn.setObjectName("dialogSecondaryButton")
        self.edit_task_btn.setIcon(get_icon("edit_light"))  # Use get_icon
        self.edit_task_btn.setIconSize(QSize(16, 16))

        self.delete_task_btn = QPushButton("Delete")
        self.delete_task_btn.setObjectName("dialogSecondaryButton")
        self.delete_task_btn.setIcon(get_icon("delete_light"))  # Use get_icon
        self.delete_task_btn.setIconSize(QSize(16, 16))
        # -----------------------------------------------

        top_layout.addWidget(self.add_task_btn)
        top_layout.addWidget(self.edit_task_btn)
        top_layout.addWidget(self.delete_task_btn)
        layout.addLayout(top_layout)

        # --- Task table ---
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(
            ["Task Name", "Category", "Start Time", "End Time"])
        self.task_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch)
        self.task_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.task_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setAlternatingRowColors(True)  # Improves readability
        layout.addWidget(self.task_table)

        # --- Bottom buttons ---
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("primaryButton")  # Use primary style
        bottom_layout.addWidget(self.close_button)
        layout.addLayout(bottom_layout)

    def _connect_signals(self):
        self.close_button.clicked.connect(
            self.accept)  # Close dialog on accept
        self.day_selector.currentTextChanged.connect(
            self.day_selection_changed)
        self.manage_categories_btn.clicked.connect(self.open_category_manager)
        self.add_task_btn.clicked.connect(self.add_task)
        self.edit_task_btn.clicked.connect(self.edit_task)
        self.delete_task_btn.clicked.connect(self.delete_task)
        self.task_table.doubleClicked.connect(
            self.edit_task)  # Double-click to edit

    def day_selection_changed(self, day):
        """Loads tasks when a different day template is selected."""
        self.current_day = day
        self.load_tasks_for_selected_day()

    def load_tasks_for_selected_day(self):
        """Refreshes the table with tasks for the currently selected day template."""
        self.task_table.setRowCount(0)  # Clear existing rows
        tasks = self.routines.get(self.current_day, [])
        # Sort tasks by start time before displaying
        sorted_tasks = sorted(
            tasks, key=lambda x: x.get('start_time', '00:00'))

        category_map = {cat['id']: cat['name'] for cat in self.categories}
        uncategorized_name = category_map.get(
            self.uncategorized_id, "Uncategorized")

        # Disable sorting during population
        self.task_table.setSortingEnabled(False)
        for row, task in enumerate(sorted_tasks):
            self.task_table.insertRow(row)

            # Task Name (with ID stored as data)
            name_item = QTableWidgetItem(task.get('name', ''))
            name_item.setData(Qt.ItemDataRole.UserRole,
                              task.get('id', ''))  # Store ID
            self.task_table.setItem(row, 0, name_item)

            # Category Name
            category_id = task.get('category', self.uncategorized_id)
            category_name = category_map.get(category_id, uncategorized_name)
            category_item = QTableWidgetItem(category_name)
            # Make category column read-only in table view
            category_item.setFlags(category_item.flags()
                                   & ~Qt.ItemFlag.ItemIsEditable)
            self.task_table.setItem(row, 1, category_item)

            # Start Time (formatted)
            start_time_str = QTime.fromString(
                task.get('start_time', ''), "HH:mm").toString("h:mm AP")
            start_item = QTableWidgetItem(start_time_str)
            start_item.setFlags(start_item.flags() & ~
                                Qt.ItemFlag.ItemIsEditable)
            self.task_table.setItem(row, 2, start_item)

            # End Time (formatted)
            end_time_str = QTime.fromString(
                task.get('end_time', ''), "HH:mm").toString("h:mm AP")
            end_item = QTableWidgetItem(end_time_str)
            end_item.setFlags(end_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.task_table.setItem(row, 3, end_item)

        self.task_table.setSortingEnabled(True)  # Re-enable sorting

    def add_task(self):
        """Opens the TaskDialog to add a new task to the current template."""
        # Smart Time Suggestion Logic
        default_task_data = {}
        tasks_on_current_day = self.routines.get(self.current_day, [])
        if tasks_on_current_day:
            try:
                latest_task = max(tasks_on_current_day, key=lambda x: QTime.fromString(
                    x.get('end_time', '00:00'), "HH:mm"))
                last_end_time = QTime.fromString(
                    latest_task.get('end_time', '00:00'), "HH:mm")
                default_task_data['start_time'] = last_end_time.toString(
                    "HH:mm")
                default_task_data['end_time'] = last_end_time.addSecs(
                    3600).toString("HH:mm")
                default_task_data['category'] = latest_task.get(
                    'category', self.uncategorized_id)
            except Exception as e:
                print(f"Error suggesting time: {e}")

        if 'start_time' not in default_task_data:
            default_task_data['start_time'] = "09:00"
            default_task_data['end_time'] = "10:00"
        if 'category' not in default_task_data:
            default_task_data['category'] = self.uncategorized_id

        dialog = TaskDialog(categories=self.categories,
                            task_data=default_task_data, parent=self)
        if dialog.exec():
            new_task_data = dialog.get_data()
            if not new_task_data.get('name'):
                QMessageBox.warning(self, "Input Error",
                                    "Task name cannot be empty.")
                return

            new_task_data['id'] = f"task-{uuid.uuid4()}"
            if self.current_day not in self.routines:
                self.routines[self.current_day] = []
            self.routines[self.current_day].append(new_task_data)
            self.load_tasks_for_selected_day()

    def edit_task(self):
        """Opens the TaskDialog to edit the selected task."""
        selected_row = self.task_table.currentRow()
        if selected_row < 0:
            QMessageBox.information(
                self, "Selection Required", "Please select a task to edit.")
            return

        task_id = self.task_table.item(
            selected_row, 0).data(Qt.ItemDataRole.UserRole)
        tasks_on_current_day = self.routines.get(self.current_day, [])
        task_to_edit = next(
            (t for t in tasks_on_current_day if t.get('id') == task_id), None)

        if not task_to_edit:
            QMessageBox.critical(
                self, "Error", "Could not find the selected task data.")
            return

        dialog = TaskDialog(categories=self.categories,
                            task_data=task_to_edit, parent=self)
        if dialog.exec():
            updated_task_data = dialog.get_data()
            if not updated_task_data.get('name'):
                QMessageBox.warning(self, "Input Error",
                                    "Task name cannot be empty.")
                return

            for i, task in enumerate(tasks_on_current_day):
                if task.get('id') == task_id:
                    tasks_on_current_day[i].update(updated_task_data)
                    break
            self.load_tasks_for_selected_day()

    def delete_task(self):
        """Deletes the selected task from the current template."""
        selected_row = self.task_table.currentRow()
        if selected_row < 0:
            QMessageBox.information(
                self, "Selection Required", "Please select a task to delete.")
            return

        task_id = self.task_table.item(
            selected_row, 0).data(Qt.ItemDataRole.UserRole)
        task_name = self.task_table.item(selected_row, 0).text()

        reply = QMessageBox.question(self, 'Confirm Deletion',
                                     f"Are you sure you want to delete the task '{task_name}' from the '{self.current_day}' template?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.routines[self.current_day] = [
                task for task in self.routines.get(self.current_day, []) if task.get('id') != task_id
            ]
            self.load_tasks_for_selected_day()

    def open_category_manager(self):
        """Opens the dialog for managing categories."""
        categories_copy = [cat.copy() for cat in self.categories]
        cat_dialog = CategoryManagerDialog(
            categories_copy, self.uncategorized_id, parent=self)

        if cat_dialog.exec():
            updated_categories = cat_dialog.get_categories()
            if updated_categories != self.categories:
                self.categories = updated_categories
                if self.controller:
                    self.controller.save_categories_and_update(self.categories)
                self.load_tasks_for_selected_day()

    def get_updated_routines(self) -> dict:
        """Returns the modified routines dict when the dialog is accepted."""
        return self.routines
