from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLineEdit, QColorDialog, QWidget, QLabel,
    QMessageBox
)
from PyQt6.QtGui import QColor, QPixmap, QPainter, QIcon
from PyQt6.QtCore import QSize, Qt
# --- FIX: Import the correct function name 'get_icon' ---
from ..utils.icons import get_icon
# -------------------------------------------------------
import uuid


class CategoryManagerDialog(QDialog):

    PRESET_COLORS = [
        "#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8A5CF5",
        "#EC4899", "#0EA5E9", "#6D28D9", "#F97316", "#A0A0B0"
    ]

    def __init__(self, categories: list, uncategorized_id: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Categories")
        self.setMinimumWidth(500)

        self.categories = categories  # Working copy
        self.uncategorized_id = uncategorized_id
        # Default to last preset (grey)
        self.current_color = self.PRESET_COLORS[-1]

        self._setup_ui()
        self._connect_signals()
        self._load_categories_list()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # List of existing categories
        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)

        # --- Form for editing/adding ---
        edit_widget = QWidget()
        edit_widget.setObjectName("editWidget")  # For potential styling
        edit_layout = QVBoxLayout(edit_widget)
        edit_layout.setContentsMargins(0, 10, 0, 0)
        edit_layout.setSpacing(10)

        # Name Input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Select or add new category name...")
        edit_layout.addWidget(self.name_input)

        # Color Selection Area
        color_area_layout = QHBoxLayout()
        color_area_layout.addWidget(QLabel("Color:"))

        # Preset Color Buttons
        for color in self.PRESET_COLORS:
            btn = QPushButton()
            btn.setObjectName("colorPickerButton")
            btn.setFixedSize(28, 28)
            btn.setStyleSheet(
                f"background-color: {color}; border-radius: 6px;")
            btn.clicked.connect(lambda checked=False,
                                c=color: self.set_color(c))
            color_area_layout.addWidget(btn)

        # Custom Color Picker Button
        self.custom_color_btn = QPushButton("...")
        self.custom_color_btn.setObjectName("colorPickerButton")
        self.custom_color_btn.setFixedSize(28, 28)
        self.custom_color_btn.setStyleSheet(
            f"background-color: {self.current_color}; border-radius: 6px;")
        self.custom_color_btn.setToolTip("Pick custom color")
        self.custom_color_btn.clicked.connect(self.pick_custom_color)
        color_area_layout.addWidget(self.custom_color_btn)
        color_area_layout.addStretch()
        edit_layout.addLayout(color_area_layout)

        main_layout.addWidget(edit_widget)

        # --- Action buttons ---
        btn_layout = QHBoxLayout()
        # --- FIX: Use the correct function name 'get_icon' ---
        icon_color = "#FFFFFF"
        secondary_icon_color = "#F0F0F5"  # Adjust if theme changes

        self.add_btn = QPushButton("Add New")
        self.add_btn.setObjectName("dialogPrimaryButton")
        self.add_btn.setIcon(get_icon("plus_light"))  # Use get_icon
        self.add_btn.setIconSize(QSize(16, 16))

        self.update_btn = QPushButton("Update Selected")
        self.update_btn.setObjectName("dialogSecondaryButton")
        self.update_btn.setIcon(get_icon("edit_light"))  # Use get_icon
        self.update_btn.setIconSize(QSize(16, 16))

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setObjectName("dialogSecondaryButton")
        self.delete_btn.setIcon(get_icon("delete_light"))  # Use get_icon
        self.delete_btn.setIconSize(QSize(16, 16))
        # -----------------------------------------------

        btn_layout.addStretch()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        main_layout.addLayout(btn_layout)

    def _connect_signals(self):
        self.list_widget.currentItemChanged.connect(self.on_item_selected)
        self.add_btn.clicked.connect(self.add_category)
        self.update_btn.clicked.connect(self.update_category)
        self.delete_btn.clicked.connect(self.delete_category)

    def _create_color_icon(self, color_str: str) -> QIcon:
        size = 16
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(color_str))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawRoundedRect(0, 0, size, size, 3, 3)
        painter.end()
        return QIcon(pixmap)

    def _load_categories_list(self):
        self.list_widget.clear()
        sorted_categories = sorted(
            [c for c in self.categories if c['id'] != self.uncategorized_id],
            key=lambda x: x['name'].lower()
        )
        uncategorized = next(
            (c for c in self.categories if c['id'] == self.uncategorized_id), None)
        if uncategorized:
            sorted_categories.insert(0, uncategorized)

        for category in sorted_categories:
            item = QListWidgetItem(category['name'])
            item.setData(Qt.ItemDataRole.UserRole, category)
            item.setIcon(self._create_color_icon(category['color']))
            if category['id'] == self.uncategorized_id:
                item.setFlags(
                    item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
                item.setText(f"{category['name']} (Default)")
            self.list_widget.addItem(item)
        self._clear_form()

    def _clear_form(self):
        self.list_widget.setCurrentItem(None)
        self.name_input.clear()
        self.set_color(self.PRESET_COLORS[-1])

    def on_item_selected(self, current_item: QListWidgetItem, previous_item):
        if not current_item:
            self._clear_form()
            return

        category_data = current_item.data(Qt.ItemDataRole.UserRole)
        if category_data:
            self.name_input.setText(category_data['name'])
            self.set_color(category_data['color'])
            is_uncategorized = (category_data['id'] == self.uncategorized_id)
            self.name_input.setEnabled(not is_uncategorized)

    def set_color(self, color_str: str):
        self.current_color = color_str
        self.custom_color_btn.setStyleSheet(
            f"background-color: {color_str}; border-radius: 6px;")

    def pick_custom_color(self):
        initial_color = QColor(self.current_color)
        color = QColorDialog.getColor(
            initial_color, self, "Pick a Custom Category Color")
        if color.isValid():
            self.set_color(color.name())

    def add_category(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error",
                                "Category name cannot be empty.")
            return

        if any(cat['name'].lower() == name.lower() for cat in self.categories):
            QMessageBox.warning(self, "Input Error",
                                f"A category named '{name}' already exists.")
            return

        new_category = {"id": f"cat-{uuid.uuid4()}", "name": name,
                        "color": self.current_color}
        self.categories.append(new_category)
        self._load_categories_list()

    def update_category(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.information(
                self, "Selection Required", "Please select a category to update.")
            return

        original_data = current_item.data(Qt.ItemDataRole.UserRole)
        original_id = original_data['id']

        if original_id == self.uncategorized_id:
            QMessageBox.warning(
                self, "Cannot Edit", "The default 'Uncategorized' category cannot be modified.")
            return

        new_name = self.name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Input Error",
                                "Category name cannot be empty.")
            return

        if any(cat['name'].lower() == new_name.lower() and cat['id'] != original_id for cat in self.categories):
            QMessageBox.warning(
                self, "Input Error", f"Another category named '{new_name}' already exists.")
            return

        for i, category in enumerate(self.categories):
            if category['id'] == original_id:
                self.categories[i]['name'] = new_name
                self.categories[i]['color'] = self.current_color
                break
        self._load_categories_list()

    def delete_category(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.information(
                self, "Selection Required", "Please select a category to delete.")
            return

        category_data = current_item.data(Qt.ItemDataRole.UserRole)
        category_id = category_data['id']
        category_name = category_data['name']

        if category_id == self.uncategorized_id:
            QMessageBox.warning(
                self, "Cannot Delete", "The default 'Uncategorized' category cannot be deleted.")
            return

        reply = QMessageBox.question(self, 'Confirm Deletion',
                                     f"Are you sure you want to delete the category '{category_name}'?\n"
                                     f"(Tasks using this category will be moved to 'Uncategorized')",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.categories = [
                cat for cat in self.categories if cat['id'] != category_id]
            self._load_categories_list()

    def get_categories(self) -> list:
        return self.categories
