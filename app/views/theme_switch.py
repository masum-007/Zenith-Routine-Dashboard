from PyQt6.QtWidgets import QAbstractButton
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QRect, QEasingCurve, Qt, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QIcon
from PyQt6.QtSvg import QSvgRenderer


class ThemeSwitch(QAbstractButton):
    toggled = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(64, 32)

        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.setDuration(300)

        self.sun_icon = self._create_icon("sun")
        self.moon_icon = self._create_icon("moon")

        self.clicked.connect(self._on_toggle)
        self.set_mode('dark')

    def _on_toggle(self):
        mode = 'light' if self.isChecked() else 'dark'
        self.toggled.emit(mode)

        self.animation.setStartValue(self.circle_position)
        self.animation.setEndValue(35 if self.isChecked() else 3)
        self.animation.start()

    def set_mode(self, mode):
        is_light = mode == 'light'
        self.setChecked(is_light)
        self.circle_position = 35 if is_light else 3
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # Background
        if self.isChecked():  # Light mode
            bg_color = QColor("#CBD5E1")
        else:  # Dark mode
            bg_color = QColor("#374151")
        painter.setBrush(bg_color)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 16, 16)

        # Circle (Toggle)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(int(self._circle_position), 3, 26, 26)

        # Icon
        icon_rect = QRect(int(self._circle_position) + 4, 7, 18, 18)
        icon = self.sun_icon if self.isChecked() else self.moon_icon
        icon.paint(painter, icon_rect)

    # --- FIX 2: Define a Qt Property for animation ---
    def _get_circle_position(self):
        return self._circle_position

    def _set_circle_position(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = pyqtProperty(
        float, fget=_get_circle_position, fset=_set_circle_position)

    def _create_icon(self, icon_name):
        from PyQt6.QtGui import QPixmap
        svg_paths = {
            "sun": f'<circle cx="12" cy="12" r="5" fill="#F59E0B"></circle><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>',
            "moon": f'<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="#D1D5DB"></path>'
        }
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">{svg_paths[icon_name]}</svg>"""
        renderer = QSvgRenderer(svg.encode('utf-8'))

        pixmap = QPixmap(renderer.defaultSize())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        return QIcon(pixmap)
