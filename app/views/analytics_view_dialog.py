from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QWidget, QTabWidget, QLabel, QGridLayout, QSizePolicy
)
# Ensure all necessary Chart components are imported
from PyQt6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet, QPieSeries, QPieSlice,
    QBarCategoryAxis, QValueAxis
)
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt6.QtCore import Qt, QDate
from datetime import timedelta


class AnalyticsViewDialog(QDialog):
    def __init__(self, weekly_data, category_data, heatmap_data, categories, theme_palette, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analytics Dashboard")
        # Increased size slightly for better chart display
        self.setMinimumSize(850, 700)

        # Store data passed from controller
        self.weekly_data = weekly_data
        self.category_data = category_data
        self.heatmap_data = heatmap_data
        self.categories = categories  # Needed for pie chart colors
        self.theme = theme_palette  # The dictionary with theme colors

        # --- Refactor: Define theme colors explicitly ---
        self.text_color = QColor(self.theme['text-primary'])
        self.secondary_text_color = QColor(self.theme['text-secondary'])
        self.accent_color = QColor(self.theme['accent-primary'])
        self.secondary_accent_color = QColor(self.theme['accent-secondary'])
        self.bg_color = QColor(self.theme['bg-base'])
        self.surface_color = QColor(self.theme['bg-surface'])
        self.border_color = QColor(self.theme['border'])
        # -----------------------------------------------

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Use a more prominent title
        title = QLabel("Productivity Analytics")
        title.setObjectName("analyticsHeader")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        main_layout.addSpacing(15)

        # Use tabs for different views
        tabs = QTabWidget()
        tabs.addTab(self._create_weekly_chart_tab(), "Weekly Completion")
        tabs.addTab(self._create_category_chart_tab(), "Time Allocation")
        tabs.addTab(self._create_heatmap_tab(), "Progress Heatmap")

        main_layout.addWidget(tabs)

    def _apply_chart_theme(self, chart: QChart):
        """Applies common theme elements to a QChart."""
        chart.setTitleFont(QFont("Segoe UI Variable", 16, QFont.Weight.Bold))
        chart.setTitleBrush(QBrush(self.text_color))
        # Use surface color for chart BG
        chart.setBackgroundBrush(QBrush(self.surface_color))
        chart.legend().setLabelColor(self.text_color)
        chart.legend().setFont(QFont("Segoe UI Variable", 10))

    def _create_weekly_chart_tab(self) -> QWidget:
        """Creates the tab containing the 7-day completion bar chart."""
        bar_set = QBarSet("Completion")
        bar_set.setColor(self.accent_color)  # Use theme accent
        bar_set.setLabelColor(self.text_color)  # Label on top of bar

        dates = []
        categories = []  # For x-axis labels
        today = QDate.currentDate()
        for i in range(6, -1, -1):  # Iterate from 6 days ago up to today
            date = today.addDays(-i)
            date_str = date.toString("yyyy-MM-dd")
            categories.append(date.toString("ddd d"))  # e.g., "Sat 26"
            progress = self.weekly_data.get(date_str, 0)
            # Use 0 for days with no tasks, visually cleaner than gaps
            bar_set.append(max(progress, 0))  # Ensure non-negative value

        series = QBarSeries()
        series.append(bar_set)
        series.setLabelsVisible(True)  # Show percentage on top of bars
        series.setLabelsFormat("@value%")  # Format label as percentage

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Last 7 Days Completion")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # X-Axis (Categories for days)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        # Use secondary color for axes
        axis_x.setLabelsColor(self.secondary_text_color)
        axis_x.setLabelsFont(QFont("Segoe UI Variable", 10))
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        # Y-Axis (Value Axis for percentage)
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTickCount(6)  # 0, 20, 40, 60, 80, 100
        axis_y.setLabelFormat("%d%%")
        axis_y.setLabelsColor(self.secondary_text_color)
        axis_y.setLabelsFont(QFont("Segoe UI Variable", 10))
        axis_y.setGridLineVisible(True)  # Show subtle grid lines
        axis_y.setGridLineColor(self.border_color)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(False)  # Hide legend for single series
        self._apply_chart_theme(chart)  # Apply common styling

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chart_view

    def _create_category_chart_tab(self) -> QWidget:
        """Creates the tab containing the category time allocation pie chart."""
        series = QPieSeries()
        series.setHoleSize(0.35)  # Make it a donut chart

        total_hours = sum(self.category_data.values())
        if total_hours <= 0:  # Handle case with no data
            # Optionally return a widget showing "No data"
            no_data_label = QLabel("No time allocation data available.")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return no_data_label

        # Map category names to colors from the loaded categories
        color_map = {cat['name']: QColor(cat['color'])
                     for cat in self.categories}
        default_color = QColor(self.theme['text-secondary'])

        # Sort data for consistent slice order (optional but nice)
        sorted_categories = sorted(
            self.category_data.items(), key=lambda item: item[1], reverse=True)

        for name, hours in sorted_categories:
            if hours <= 0:
                continue
            percentage = (hours / total_hours) * 100
            # Label format: Category Name (X.Yh, Z.Z%)
            label = f"{name}\n({hours:.1f}h, {percentage:.1f}%)"
            slice_ = QPieSlice(label, percentage)
            slice_.setColor(color_map.get(name, default_color))
            slice_.setLabelFont(
                QFont("Segoe UI Variable", 9, QFont.Weight.Bold))
            # Use primary text for labels
            slice_.setLabelColor(self.text_color)
            # Explode slice on hover for interactivity
            slice_.hovered.connect(
                lambda state, s=slice_: s.setExploded(state))

            series.append(slice_)

        # Labels outside the slices
        series.setLabelsPosition(QPieSlice.LabelPosition.LabelOutside)
        series.setLabelsVisible(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Weekly Time Allocation by Category")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        chart.legend().setVisible(False)  # Labels on slices are sufficient
        self._apply_chart_theme(chart)  # Apply common styling
        # Specific styling for pie chart labels
        for s in series.slices():
            s.setLabelBrush(QBrush(self.text_color))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chart_view

    def _create_heatmap_tab(self) -> QWidget:
        """Creates the tab containing the 35-day calendar heatmap."""
        container = QWidget()
        layout = QGridLayout(container)
        layout.setSpacing(4)  # Tighter spacing for heatmap cells

        today = QDate.currentDate()
        # Calculate start date: Go back to the Sunday before the date 34 days ago
        start_date_calc = today.addDays(-34)
        day_of_week_start = start_date_calc.dayOfWeek() % 7  # 0=Sun, 6=Sat
        start_date = start_date_calc.addDays(-day_of_week_start)

        # Add day labels (Mon-Sun or Sun-Sat based on locale preference?)
        # Let's use Mon-Sun common in many places
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days):
            label = QLabel(day)
            label.setObjectName("heatmapDayLabel")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label, 0, col)

        # Create 5 rows x 7 columns grid
        num_rows = 5
        for i in range(num_rows * 7):  # 35 days total
            current_date = start_date.addDays(i)
            date_str = current_date.toString("yyyy-MM-dd")
            # Use -2 for dates outside range
            progress = self.heatmap_data.get(date_str, -2)

            day_cell = QLabel(current_date.toString("d"))  # Day number
            day_cell.setFixedSize(45, 45)  # Slightly larger cells
            day_cell.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Determine color and tooltip based on progress
            tooltip_text = f"{current_date.toString('MMM d, yyyy')}: "
            # Date outside the 35-day range (e.g., future dates if start wasn't Sunday)
            if progress == -2:
                # Use base background
                color_hex = QColor(self.theme['bg-base']).name()
                tooltip_text += "N/A"
            elif progress == -1:  # No tasks scheduled
                color_hex = self.theme['bg-surface-2']  # Use input background
                tooltip_text += "No tasks"
            else:  # Valid progress day
                color_hex = self._get_color_for_progress(progress)
                tooltip_text += f"{progress}% completed"

            # Apply style and tooltip
            day_cell.setStyleSheet(f"""
                background-color: {color_hex};
                color: {self.theme['text-primary']};
                border: 1px solid {self.theme['border']};
                border-radius: 6px;
                font-weight: 600;
            """)
            day_cell.setToolTip(tooltip_text)

            row = i // 7
            col = i % 7
            layout.addWidget(day_cell, row + 1, col)  # +1 for header row

        # Add stretchers to push grid to top-left if needed
        layout.setRowStretch(num_rows + 1, 1)
        layout.setColumnStretch(7, 1)

        # Optionally add a color scale legend here

        return container

    def _get_color_for_progress(self, progress: int) -> str:
        """Returns a hex color string for the heatmap based on progress %."""
        if progress < 0:
            return self.theme['bg-surface-2']  # No tasks
        if progress == 0:
            return self.theme['border']  # Zero completion

        # Create a gradient using the secondary accent color for heatmap
        base_color = QColor(self.theme['accent-secondary'])
        # Alpha from 0.1 (low) to 1.0 (high)
        alpha = 0.1 + (progress / 100.0) * 0.9
        base_color.setAlphaF(alpha)

        # Return in #AARRGGBB format for QSS
        return base_color.name(QColor.NameFormat.HexArgb)
