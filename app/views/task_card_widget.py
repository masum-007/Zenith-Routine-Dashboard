from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox
from PyQt6.QtCore import pyqtSignal, Qt, QTime


class TaskCardWidget(QWidget):
    completion_toggled = pyqtSignal(str, bool)

    def __init__(self, task_info: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("taskCard")

        self.task_id = task_info.get('id')
        self.start_time = task_info.get('start_time', '')
        self.end_time = task_info.get('end_time', '')
        is_completed = task_info.get('completed', False)

        name = task_info.get('name', 'Unnamed Task')
        notes = task_info.get('notes', '')
        category_color = task_info.get('category_color', '#A0A0B0')

        start_time_12h = QTime.fromString(
            self.start_time, "HH:mm").toString("h:mm AP")
        end_time_12h = QTime.fromString(
            self.end_time, "HH:mm").toString("h:mm AP")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 20, 0)  # No left margin
        main_layout.setSpacing(15)

        # --- NEW: Category Color Bar ---
        self.color_bar = QWidget()
        self.color_bar.setObjectName("categoryColorBar")
        self.color_bar.setFixedWidth(6)
        self.color_bar.setStyleSheet(f"background-color: {category_color};")
        main_layout.addWidget(self.color_bar)

        # --- Checkbox ---
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(is_completed)
        main_layout.addWidget(self.checkbox)

        # --- Text Content ---
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 15, 0, 15)  # Vertical padding
        text_layout.setSpacing(2)
        self.name_label = QLabel(name)
        self.name_label.setObjectName("taskNameLabel")
        self.time_label = QLabel(f"{start_time_12h} - {end_time_12h}")
        self.time_label.setObjectName("taskTimeLabel")

        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.time_label)

        if notes:
            self.notes_label = QLabel(notes)
            self.notes_label.setObjectName("taskNotesLabel")
            self.notes_label.setWordWrap(True)
            self.notes_label.setMaximumWidth(400)
            text_layout.addSpacing(10)
            text_layout.addWidget(self.notes_label)

        main_layout.addLayout(text_layout)
        main_layout.addStretch()

        # --- Connect Signals ---
        self.checkbox.stateChanged.connect(self._on_toggle)
        self.set_completed_style(is_completed)

    def _on_toggle(self, state):
        is_checked = state == Qt.CheckState.Checked.value
        self.set_completed_style(is_checked)
        self.completion_toggled.emit(self.task_id, is_checked)
        if self.parent() and self.parent().window():
            self.parent().window()._update_current_task_highlight()

    def set_completed_style(self, is_completed):
        self.setProperty("completed", is_completed)
        self.style().polish(self)

    def set_is_current(self, is_current):
        self.setProperty("is_current", is_current)
        self.style().polish(self)
