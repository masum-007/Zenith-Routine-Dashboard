# Zenith Theme Engine: A complete visual overhaul for the Routine Dashboard.

THEME_PALETTES = {
    "dark": {
        "bg-base": "#101014",
        "bg-surface": "#1B1B1F",
        "bg-surface-2": "#2C2C32",
        "text-primary": "#F0F0F5",
        "text-secondary": "#A0A0B0",
        "border": "#3A3A40",
        "accent-primary": "#8A5CF5",
        "accent-secondary": "#3B82F6",
        "accent-hover": "#A07CF8",
        "shadow-color": "rgba(0, 0, 0, 0.5)"
    },
    "light": {
        "bg-base": "#F8F9FA",
        "bg-surface": "#FFFFFF",
        "bg-surface-2": "#F1F5F9",
        "text-primary": "#1E293B",
        "text-secondary": "#64748B",
        "border": "#E2E8F0",
        "accent-primary": "#4F46E5",
        "accent-secondary": "#0EA5E9",
        "accent-hover": "#6366F1",
        "shadow-color": "rgba(100, 116, 139, 0.2)"
    }
}


def get_theme(theme_name="dark"):
    p = THEME_PALETTES.get(theme_name, THEME_PALETTES["dark"])

    return f"""
        /* --- Universal --- */
        * {{ font-family: 'Segoe UI Variable', sans-serif; }}
        QMainWindow, QDialog {{ background-color: {p['bg-base']}; }}
        
        /* --- Labels --- */
        QLabel {{ color: {p['text-secondary']}; background: transparent; }}
        QLabel#headerLabel {{ font-size: 26px; font-weight: 700; color: {p['text-primary']}; }}
        QLabel#dateLabel {{ font-size: 16px; font-weight: 600; color: {p['text-primary']}; }}
        QLabel#progressLabel {{ font-size: 13px; font-weight: 600; text-transform: uppercase; color: {p['text-secondary']}; }}
        QLabel#noTasksLabel {{ font-size: 16px; color: {p['text-secondary']}; font-style: italic; }}
        QLabel#taskNotesLabel {{
            font-size: 13px;
            color: {p['text-secondary']};
            font-style: italic;
            padding-top: 5px;
            border-top: 1px solid {p['border']};
            margin-top: 5px;
        }}
        /* Analytics Dialog Labels */
        QLabel#analyticsHeader {{ font-size: 20px; font-weight: 600; color: {p['text-primary']}; }}
        QLabel#heatmapDayLabel {{
            font-size: 12px;
            font-weight: 600;
            color: {p['text-secondary']};
            background-color: transparent;
            min-width: 30px;
        }}

        /* --- Buttons --- */
        QPushButton {{ border: none; border-radius: 8px; font-weight: 600; font-size: 14px; padding: 10px 16px; }}
        QPushButton#primaryButton, QPushButton#dialogPrimaryButton {{ background-color: {p['accent-primary']}; color: white; }}
        QPushButton#primaryButton:hover, QPushButton#dialogPrimaryButton:hover {{ background-color: {p['accent-hover']}; }}
        QPushButton#secondaryButton, QPushButton#dialogSecondaryButton {{ background-color: {p['bg-surface-2']}; color: {p['text-primary']}; }}
        QPushButton#secondaryButton:hover, QPushButton#dialogSecondaryButton:hover {{ background-color: {p['border']}; }}
        QPushButton#navButton {{ background-color: transparent; padding: 8px; }}
        QPushButton#navButton:hover {{ background-color: {p['bg-surface-2']}; }}
        QPushButton#iconButton {{ background-color: transparent; padding: 8px; border-radius: 18px; }}
        QPushButton#iconButton:hover {{ background-color: {p['bg-surface-2']}; }}
        QPushButton#colorPickerButton {{ padding: 5px; border: 2px solid {p['border']}; }}
        QPushButton#colorPickerButton:hover {{ border: 2px solid {p['accent-primary']}; }}

        /* --- Custom Date Button --- */
        QPushButton#dateSelectorButton {{ background-color: {p['bg-surface']}; border: 1px solid {p['border']}; color: {p['text-primary']}; font-weight: 600; }}
        QPushButton#dateSelectorButton:hover {{ background-color: {p['bg-surface-2']}; }}

        /* --- Calendar Popup --- */
        QCalendarWidget {{ background-color: {p['bg-surface']}; border: 1px solid {p['border']}; }}
        QCalendarWidget QWidget#qt_calendar_navigationbar {{ background-color: {p['bg-surface']}; }}
        QCalendarWidget QToolButton {{ color: {p['text-primary']}; background-color: transparent; font-size: 14px; font-weight: 600; }}
        QCalendarWidget QToolButton:hover {{ background-color: {p['bg-surface-2']}; }}
        QCalendarWidget QMenu {{ background-color: {p['bg-surface']}; color: {p['text-primary']}; }}
        QCalendarWidget QSpinBox {{ background-color: {p['bg-surface-2']}; color: {p['text-primary']}; border: 1px solid {p['border']}; }}
        QCalendarWidget QAbstractItemView:enabled {{ color: {p['text-primary']}; background-color: {p['bg-surface']}; selection-background-color: {p['accent-primary']}; selection-color: white; }}
        QCalendarWidget QAbstractItemView:disabled {{ color: {p['text-secondary']}; }}

        /* --- Progress Bar --- */
        QProgressBar {{ background-color: {p['bg-surface-2']}; color: {p['text-primary']}; border: none; border-radius: 8px; text-align: center; font-weight: 600; }}
        QProgressBar::chunk {{ background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {p['accent-primary']}, stop:1 {p['accent-secondary']}); border-radius: 8px; }}

        /* --- Scroll Area --- */
        QScrollArea {{ border: none; background: transparent; }}
        QWidget#scrollContent {{ background-color: transparent; }}
        QScrollBar:vertical {{ border: none; background: transparent; width: 10px; margin: 0px; }}
        QScrollBar::handle:vertical {{ background-color: {p['border']}; min-height: 25px; border-radius: 5px; }}
        QScrollBar::handle:vertical:hover {{ background-color: {p['text-secondary']}; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}

        /* --- Inputs --- */
        QComboBox, QLineEdit, QTimeEdit, QTextEdit {{
            background-color: {p['bg-surface-2']};
            border: 1px solid {p['border']};
            padding: 8px 12px;
            border-radius: 8px;
            color: {p['text-primary']};
            font-size: 14px;
        }}
        QComboBox:focus, QLineEdit:focus, QTimeEdit:focus, QTextEdit:focus {{ border: 1px solid {p['accent-primary']}; }}
        
        /* --- Table --- */
        QTableWidget {{ background-color: {p['bg-base']}; border: 1px solid {p['border']}; gridline-color: {p['border']}; color: {p['text-primary']}; border-radius: 8px; }}
        QHeaderView::section {{ background-color: {p['bg-surface']}; color: {p['text-primary']}; padding: 10px; border: none; border-bottom: 1px solid {p['border']}; font-weight: 600; }}
        QTableWidget::item {{ padding: 10px; border-bottom: 1px solid {p['border']}; }}
        QTableWidget::item:selected {{ background-color: {p['accent-primary']}; color: white; }}
        QListWidget {{ background-color: {p['bg-surface']}; border: 1px solid {p['border']}; color: {p['text-primary']}; border-radius: 8px; }}
        QListWidget::item {{ padding: 10px; }}
        QListWidget::item:selected {{ background-color: {p['accent-primary']}; color: white; }}

        /* --- Task Card Specific --- */
        QWidget#taskCard {{
            background-color: {p['bg-surface']};
            border-radius: 12px;
            border: 1px solid {p['border']};
        }}
        /* NEW: Color bar on the task card */
        QWidget#categoryColorBar {{
            border-top-left-radius: 12px;
            border-bottom-left-radius: 12px;
        }}
        QWidget#taskCard[completed="true"] {{ background-color: {p['bg-base']}; }}
        QWidget#taskCard[is_current="true"] {{ border: 2px solid {p['accent-secondary']}; }}
        QLabel#taskNameLabel {{ font-weight: 600; font-size: 16px; color: {p['text-primary']}; }}
        QLabel#taskTimeLabel {{ font-size: 13px; color: {p['text-secondary']}; }}
        
        /* --- Analytics Charts --- */
        QChartView {{ background: transparent; }}
        QTabWidget::pane {{ border: 1px solid {p['border']}; border-radius: 8px; padding: 10px; }}
        QTabBar::tab {{
            background: {p['bg-surface-2']};
            color: {p['text-secondary']};
            padding: 10px 20px;
            font-weight: 600;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: 1px solid {p['border']};
            border-bottom: none;
            margin-right: 4px;
        }}
        QTabBar::tab:selected {{
            background: {p['bg-base']};
            color: {p['text-primary']};
            border-bottom: 1px solid {p['bg-base']};
        }}
        QTabBar::tab:!selected:hover {{
            background: {p['border']};
        }}
    """
