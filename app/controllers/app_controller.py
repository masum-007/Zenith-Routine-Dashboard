from app.views.routine_editor_dialog import RoutineEditorDialog
from app.views.analytics_view_dialog import AnalyticsViewDialog
from app.utils.theme import get_theme, THEME_PALETTES
from datetime import date
from PyQt6.QtWidgets import QMessageBox  # Import QMessageBox here


class AppController:
    """The Controller, connecting the View and the Model."""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        """Connects signals from the view to controller methods."""
        self.view.date_changed.connect(self.update_task_list)
        self.view.manage_routines_requested.connect(self.show_routine_editor)
        self.view.completion_toggled.connect(self.toggle_completion)
        self.view.theme_changed.connect(self.handle_theme_change)
        self.view.analytics_requested.connect(self.show_analytics_dialog)

    def init_app(self):
        """Loads initial settings and populates the view."""
        initial_theme = self.model.load_settings().get("theme", "dark")
        # Apply theme stylesheet FIRST
        stylesheet = get_theme(initial_theme)
        self.view.setStyleSheet(stylesheet)
        # THEN set the switch state and update dynamic elements (icons)
        self.view.set_initial_theme(initial_theme)
        # THEN load the initial tasks
        self.update_task_list()

    def handle_theme_change(self, theme_name: str):
        """Applies the selected theme stylesheet and updates dynamic elements."""
        stylesheet = get_theme(theme_name)
        self.view.setStyleSheet(stylesheet)  # Apply the main stylesheet
        # --- FIX: Re-enabled update_theme_elements ---
        # Update icons based on the new theme
        self.view.update_theme_elements(theme_name)
        self.model.save_settings({"theme": theme_name})  # Save preference

    def update_task_list(self):
        # ... (same as before) ...
        current_date = self.view.get_current_date().toPyDate()
        tasks = self.model.get_tasks_for_display(current_date)

        completed_count = sum(1 for task in tasks if task.get('completed'))
        total_tasks = len(tasks)
        progress = int((completed_count / total_tasks * 100)
                       ) if total_tasks > 0 else 0

        self.view.display_tasks(tasks, progress)

    def show_routine_editor(self):
        # ... (same as before) ...
        routines_copy = self.model.get_all_routines().copy()
        categories = self.model.get_categories()
        uncat_id = self.model.get_uncategorized_id()

        dialog = RoutineEditorDialog(
            routines_data=routines_copy,
            categories=categories,
            uncategorized_id=uncat_id,
            parent=self.view
        )
        dialog.controller = self

        if dialog.exec():
            updated_routines = dialog.get_updated_routines()
            routines_changed = False
            for day_name, tasks in updated_routines.items():
                if self.model.routines.get(day_name) != tasks:
                    self.model.save_routine_for_day(day_name, tasks)
                    routines_changed = True
            if routines_changed:
                self.update_task_list()

    def save_categories_and_update(self, categories: list):
        # ... (same as before) ...
        self.model.save_categories(categories)
        self.update_task_list()

    def toggle_completion(self, task_id: str, is_completed: bool):
        # ... (same as before) ...
        current_date = self.view.get_current_date().toPyDate()
        self.model.toggle_task_completion(current_date, task_id)
        self.update_task_list()

    def show_analytics_dialog(self):
        # ... (same as before, including error handling) ...
        try:
            today = date.today()
            weekly_progress = self.model.get_progress_for_date_range(today, 7)
            category_allocation = self.model.get_allocated_time_by_category()
            heatmap_progress = self.model.get_progress_for_date_range(
                today, 35)
            current_theme_name = self.model.load_settings().get("theme", "dark")
            theme_palette = THEME_PALETTES.get(current_theme_name)
            categories = self.model.get_categories()

            dialog = AnalyticsViewDialog(
                weekly_data=weekly_progress,
                category_data=category_allocation,
                heatmap_data=heatmap_progress,
                categories=categories,
                theme_palette=theme_palette,
                parent=self.view
            )
            dialog.setStyleSheet(get_theme(current_theme_name))
            dialog.exec()
        except ImportError:
            QMessageBox.critical(self.view, "Error",
                                 "PyQt6-Charts library is required for analytics but not found.\n"
                                 "Please install it using: pip install PyQt6-Charts")
        except Exception as e:
            print(f"Error opening analytics dialog: {e}")
            QMessageBox.critical(self.view, "Error",
                                 f"Could not open analytics window:\n{e}")
