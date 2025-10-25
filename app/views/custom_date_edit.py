from PyQt6.QtWidgets import QPushButton, QCalendarWidget, QWidget
from PyQt6.QtCore import pyqtSignal, QDate, Qt, QPoint
from PyQt6.QtGui import QGuiApplication


class CustomDateEdit(QPushButton):
    """
    A custom, fully stylable date selector button that behaves like a
    standard dropdown menu and stays within the screen bounds.
    """
    dateChanged = pyqtSignal(QDate)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._current_date = QDate.currentDate()
        self.setText(self._current_date.toString("MM/dd/yyyy"))
        self.clicked.connect(self._show_calendar)
        self._calendar_widget = None

    def date(self) -> QDate:
        """Returns the currently selected date."""
        return self._current_date

    def setDate(self, date: QDate):
        """Sets the date and updates the button's text."""
        if self._current_date != date:
            self._current_date = date
            self.setText(self._current_date.toString("MM/dd/yyyy"))
            self.dateChanged.emit(self._current_date)

    def _show_calendar(self):
        """
        Creates, positions, and shows a styled QCalendarWidget that closes
        automatically and stays within the screen boundaries.
        """
        if self._calendar_widget is None or not self._calendar_widget.isVisible():
            self._calendar_widget = QCalendarWidget(self.window())
            self._calendar_widget.setWindowFlags(Qt.WindowType.Popup)
            self._calendar_widget.setSelectedDate(self._current_date)
            self._calendar_widget.selectionChanged.connect(
                self._on_date_selected)

            # --- FIX: Calculate position to stay within the screen ---
            screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
            calendar_size = self._calendar_widget.sizeHint()
            global_pos = self.mapToGlobal(QPoint(0, self.height()))

            # Adjust horizontally if it goes off the right edge
            if global_pos.x() + calendar_size.width() > screen_geometry.right():
                global_pos.setX(self.mapToGlobal(
                    QPoint(self.width() - calendar_size.width(), 0)).x())

            # Adjust vertically if it goes off the bottom edge
            if global_pos.y() + calendar_size.height() > screen_geometry.bottom():
                global_pos.setY(self.mapToGlobal(
                    QPoint(0, -calendar_size.height())).y())

            self._calendar_widget.move(global_pos)
            self._calendar_widget.show()

    def _on_date_selected(self):
        """Handles date selection from the calendar popup."""
        if self._calendar_widget:
            new_date = self._calendar_widget.selectedDate()
            self.setDate(new_date)
            self._calendar_widget.close()
            self._calendar_widget = None
