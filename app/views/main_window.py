from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QProgressBar, QGraphicsDropShadowEffect
    # QStyle is no longer needed here
)
from PyQt6.QtCore import QDate, pyqtSignal, Qt, QSize, QTimer, QTime
from PyQt6.QtGui import QColor, QIcon  # Import QIcon
# --- FIX: Import the new get_icon function ---
from ..utils.icons import get_icon
# -------------------------------------------
from ..utils.theme import THEME_PALETTES  # Keep for shadow color if needed
from .theme_switch import ThemeSwitch
from .task_card_widget import TaskCardWidget
from .custom_date_edit import CustomDateEdit


class MainWindow(QMainWindow):
    theme_changed = pyqtSignal(str)
    date_changed = pyqtSignal(QDate)
    manage_routines_requested = pyqtSignal()
    completion_toggled = pyqtSignal(str, bool)
    analytics_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zenith Routine Dashboard")
        self.setMinimumSize(900, 750)
        self.task_widgets = []
        self._setup_ui()

        self.highlight_timer = QTimer(self)
        self.highlight_timer.timeout.connect(
            self._update_current_task_highlight)
        self.highlight_timer.start(30000)

    def set_initial_theme(self, theme_name: str):
        """Sets the initial state of the theme switch and icons."""
        self.theme_switch.set_mode(theme_name)
        # Ensure icons match initial theme
        self.update_theme_elements(theme_name)

    def _setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.main_layout.setSpacing(20)

        # --- Header ---
        header_layout = QHBoxLayout()
        self.header_label = QLabel("Routine Dashboard")
        self.header_label.setObjectName("headerLabel")

        # --- FIX: Use get_icon, icon set in update_theme_elements ---
        self.analytics_button = QPushButton()
        self.analytics_button.setObjectName("iconButton")
        self.analytics_button.setIconSize(QSize(22, 22))
        self.analytics_button.setToolTip("Show Analytics")
        # ---------------------------------------------------------

        self.theme_switch = ThemeSwitch()

        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.analytics_button)
        header_layout.addWidget(self.theme_switch)
        self.main_layout.addLayout(header_layout)

        # --- Sub-Header (Date Navigation) ---
        nav_layout = QHBoxLayout()
        self.date_label = QLabel()
        self.date_label.setObjectName("dateLabel")

        # --- FIX: Use get_icon, icons set in update_theme_elements ---
        self.prev_day_button = QPushButton()
        self.prev_day_button.setObjectName("navButton")
        self.prev_day_button.setIconSize(QSize(18, 18))

        self.date_selector = CustomDateEdit()
        self.date_selector.setObjectName("dateSelectorButton")

        self.next_day_button = QPushButton()
        self.next_day_button.setObjectName("navButton")
        self.next_day_button.setIconSize(QSize(18, 18))
        # ---------------------------------------------------------

        nav_layout.addWidget(self.date_label)
        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_day_button)
        nav_layout.addWidget(self.date_selector)
        nav_layout.addWidget(self.next_day_button)
        self.main_layout.addLayout(nav_layout)

        # --- Progress Bar ---
        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_header_layout = QHBoxLayout()
        progress_label = QLabel("DAILY PROGRESS")
        progress_label.setObjectName("progressLabel")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat("%p%")
        progress_header_layout.addWidget(progress_label)
        progress_layout.addLayout(progress_header_layout)
        progress_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(progress_container)

        # --- Task List Area ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.task_list_layout = QVBoxLayout(self.scroll_content)
        self.task_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.task_list_layout.setContentsMargins(
            5, 5, 5, 5)  # Padding around cards
        self.task_list_layout.setSpacing(12)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)  # Add scroll area

        # --- Bottom Button ---
        self.manage_routines_button = QPushButton("Manage Routines")
        self.manage_routines_button.setObjectName("primaryButton")
        # Settings icon is always white, so load directly
        self.manage_routines_button.setIcon(get_icon("settings_white"))
        self.manage_routines_button.setIconSize(QSize(18, 18))

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(138, 92, 245, 80))  # Example shadow color
        self.manage_routines_button.setGraphicsEffect(shadow)
        self.main_layout.addWidget(
            self.manage_routines_button, 0, Qt.AlignmentFlag.AlignCenter)

        # --- Connect signals ---
        self.date_selector.dateChanged.connect(self._on_date_changed)
        self.prev_day_button.clicked.connect(self.select_prev_day)
        self.next_day_button.clicked.connect(self.select_next_day)
        self.manage_routines_button.clicked.connect(
            self.manage_routines_requested.emit)
        self.theme_switch.toggled.connect(self.theme_changed.emit)
        self.analytics_button.clicked.connect(self.analytics_requested.emit)

        # Set initial date label after widgets are created
        self._on_date_changed(self.date_selector.date())

    def update_theme_elements(self, theme_name: str):
        """Update icons based on the selected theme."""
        # --- FIX: Load the correct icon based on theme name ---
        if theme_name == "dark":
            self.analytics_button.setIcon(get_icon("analytics_light"))
            self.prev_day_button.setIcon(get_icon("left-arrow_light"))
            self.next_day_button.setIcon(get_icon("right-arrow_light"))
        else:  # Light theme
            self.analytics_button.setIcon(get_icon("analytics_dark"))
            self.prev_day_button.setIcon(get_icon("left-arrow_dark"))
            self.next_day_button.setIcon(get_icon("right-arrow_dark"))
        # --------------------------------------------------------

        # Settings icon on the bottom button remains white regardless of theme
        self.manage_routines_button.setIcon(get_icon("settings_white"))

    def _clear_task_list(self):
        # ... (same as before) ...
        self.task_widgets = []
        while self.task_list_layout.count():
            item = self.task_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def display_tasks(self, tasks: list, progress_percent: int):
        # ... (same as before) ...
        self._clear_task_list()
        self.progress_bar.setValue(progress_percent)

        if not tasks:
            no_tasks_label = QLabel("No tasks scheduled for this day.")
            no_tasks_label.setObjectName("noTasksLabel")
            no_tasks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.task_list_layout.addStretch(1)
            self.task_list_layout.addWidget(no_tasks_label)
            self.task_list_layout.addStretch(1)
        else:
            for task_data in tasks:
                card = TaskCardWidget(task_data, self.scroll_content)
                card.completion_toggled.connect(self.completion_toggled.emit)
                self.task_list_layout.addWidget(card)
                self.task_widgets.append(card)
            self.task_list_layout.addStretch(1)  # Add bottom stretch

        self._update_current_task_highlight()

    def _on_date_changed(self, new_date: QDate):
        # ... (same as before) ...
        self.date_label.setText(new_date.toString("dddd, MMMM d, yyyy"))
        self.date_changed.emit(new_date)
        self._update_current_task_highlight()

    def get_current_date(self) -> QDate:
        # ... (same as before) ...
        return self.date_selector.date()

    def select_prev_day(self):
        # ... (same as before) ...
        self.date_selector.setDate(self.date_selector.date().addDays(-1))

    def select_next_day(self):
        # ... (same as before) ...
        self.date_selector.setDate(self.date_selector.date().addDays(1))

    def _update_current_task_highlight(self):
        # ... (same as before) ...
        is_today = (self.get_current_date() == QDate.currentDate())
        current_time_str = QTime.currentTime().toString("HH:mm")

        for card in self.task_widgets:
            is_current = False
            if is_today and not card.checkbox.isChecked():
                if card.start_time and card.end_time:
                    if card.start_time <= current_time_str < card.end_time:
                        is_current = True
            card.set_is_current(is_current)
