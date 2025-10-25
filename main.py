import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from app.views.main_window import MainWindow
from app.models.data_manager import DataManager
from app.controllers.app_controller import AppController
from app.utils.theme import get_theme


def main():
    """The main entry point for the application."""

    app = QApplication(sys.argv)

    # --- FIX: Removed the two lines causing the AttributeError ---
    # High-DPI scaling is handled automatically by default in most
    # modern Qt versions, so these lines are not essential.
    # -------------------------------------------------------------

    # Initialize model, view, controller
    data_manager = DataManager(
        routines_file='data/routines.json',
        progress_file='data/progress.json',
        categories_file='data/categories.json',
        settings_file='data/settings.json'
    )

    main_view = MainWindow()
    controller = AppController(model=data_manager, view=main_view)

    controller.init_app()
    main_view.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
