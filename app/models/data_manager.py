import json
import os
import uuid
from datetime import date, timedelta


class DataManager:
    """Handles loading/saving all app data."""

    DEFAULT_CATEGORIES = [
        {"id": "cat-001", "name": "Uncategorized", "color": "#A0A0B0"},
        {"id": "cat-002", "name": "Study", "color": "#3B82F6"},
        {"id": "cat-003", "name": "Work", "color": "#10B981"},
        {"id": "cat-004", "name": "Health", "color": "#F59E0B"},
        {"id": "cat-005", "name": "Spiritual", "color": "#8A5CF5"}
    ]
    UNCATEGORIZED_ID = DEFAULT_CATEGORIES[0]["id"]

    def __init__(self, routines_file, progress_file, categories_file, settings_file):
        self.routines_file = routines_file
        self.progress_file = progress_file
        self.categories_file = categories_file
        self.settings_file = settings_file

        self._ensure_data_dir_exists()

        self.routines = self._load_json(
            self.routines_file, default={"default": []})
        self.progress = self._load_json(self.progress_file, default={})
        self.categories = self._load_json(
            self.categories_file, default=self.DEFAULT_CATEGORIES)
        self.settings = self._load_json(
            self.settings_file, default={"theme": "dark"})

    def _ensure_data_dir_exists(self):
        os.makedirs(os.path.dirname(self.routines_file), exist_ok=True)

    def _load_json(self, filepath, default):
        if not os.path.exists(filepath):
            if callable(default):
                return default()
            return default
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            if callable(default):
                return default()
            return default

    # --- Routines ---
    def _save_routines(self):
        with open(self.routines_file, 'w', encoding='utf-8') as f:
            json.dump(self.routines, f, indent=4)

    def get_routine_for_day(self, day_name: str):
        return self.routines.get(day_name, self.routines.get("default", []))

    def get_all_routines(self):
        return self.routines

    def save_routine_for_day(self, day_name: str, tasks: list):
        for task in tasks:
            if 'id' not in task or not task['id']:
                task['id'] = str(uuid.uuid4())
            if 'category' not in task:
                # Ensure category exists
                task['category'] = self.UNCATEGORIZED_ID
        self.routines[day_name] = tasks
        self._save_routines()

    # --- Progress ---
    def _save_progress(self):
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=4)

    def get_tasks_for_display(self, target_date: date):
        day_name = target_date.strftime('%A')
        date_str = target_date.isoformat()

        tasks_template = self.get_routine_for_day(day_name)
        completed_ids = set(self.progress.get(date_str, []))

        # Get a quick lookup map for category colors
        category_map = {cat['id']: cat for cat in self.categories}
        uncategorized = category_map.get(
            self.UNCATEGORIZED_ID, {"name": "Uncategorized", "color": "#A0A0B0"})

        display_tasks = []
        for task_template in tasks_template:
            task = task_template.copy()
            task_id = task.get('id')

            # Get category info
            category_id = task.get('category', self.UNCATEGORIZED_ID)
            category_info = category_map.get(category_id, uncategorized)

            task['completed'] = task_id in completed_ids
            task['category_name'] = category_info['name']
            task['category_color'] = category_info['color']

            display_tasks.append(task)

        return sorted(display_tasks, key=lambda x: x.get('start_time', '00:00'))

    def toggle_task_completion(self, target_date: date, task_id: str):
        date_str = target_date.isoformat()
        if date_str not in self.progress:
            self.progress[date_str] = []

        if task_id in self.progress[date_str]:
            self.progress[date_str].remove(task_id)
        else:
            self.progress[date_str].append(task_id)
        self._save_progress()

    # --- Categories ---
    def get_categories(self):
        return self.categories

    def save_categories(self, categories: list):
        self.categories = categories
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            json.dump(self.categories, f, indent=4)

    def get_uncategorized_id(self):
        return self.UNCATEGORIZED_ID

    # --- Settings ---
    def load_settings(self):
        return self.settings

    def save_settings(self, settings: dict):
        self.settings = settings
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)

    # --- Analytics Data ---
    def get_progress_for_date_range(self, end_date: date, days: int):
        """Returns progress data for the last 'days' ending at 'end_date'."""
        progress_map = {}
        for i in range(days):
            target_date = end_date - timedelta(days=i)
            date_str = target_date.isoformat()

            tasks = self.get_tasks_for_display(target_date)
            total_tasks = len(tasks)

            if total_tasks == 0:
                progress_map[date_str] = -1  # -1 indicates a day with no tasks
                continue

            completed_count = sum(1 for task in tasks if task.get('completed'))
            percentage = int((completed_count / total_tasks * 100))
            progress_map[date_str] = percentage

        return progress_map

    def get_allocated_time_by_category(self):
        """Calculates total time (in hours) allocated per category in routines."""
        from datetime import datetime
        category_time = {}

        routines = self.get_all_routines()
        category_map = {cat['id']: cat for cat in self.categories}
        uncategorized_name = category_map.get(
            self.UNCATEGORIZED_ID, {"name": "Uncategorized"})['name']

        all_tasks = []
        for day, tasks in routines.items():
            all_tasks.extend(tasks)

        for task in all_tasks:
            category_id = task.get('category', self.UNCATEGORIZED_ID)
            category_name = category_map.get(
                category_id, {"name": uncategorized_name})['name']

            try:
                t1 = datetime.strptime(
                    task.get('start_time', '00:00'), '%H:%M')
                t2 = datetime.strptime(task.get('end_time', '00:00'), '%H:%M')
                duration_hours = (t2 - t1).total_seconds() / 3600
                if duration_hours < 0:  # Handle overnight tasks simply
                    duration_hours += 24
            except ValueError:
                duration_hours = 0

            if category_name not in category_time:
                category_time[category_name] = 0
            category_time[category_name] += duration_hours

        return category_time
