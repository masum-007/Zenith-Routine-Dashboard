from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt

# --- Define SVG data directly ---
# We create light (for dark theme) and dark (for light theme) versions

ICON_DATA = {
    "settings_white": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#FFFFFF"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 15.6c1.98 0 3.6-1.62 3.6-3.6s-1.62-3.6-3.6-3.6-3.6 1.62-3.6 3.6 1.62 3.6 3.6 3.6ZM19.14 12.94c.04-.3.06-.61.06-.94s-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96a8.2 8.2 0 0 0-1.62-.94L14.4 2.81c-.04-.24-.24-.41-.48-.41H10.08c-.24 0-.44.17-.48.41L9.2 5.77a8.2 8.2 0 0 0-1.62.94l-2.39-.96c-.22-.07-.47 0-.59.22L2.68 9.29c-.11.2-.06.47.12.61l2.03 1.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.04.24.24.41.48.41h3.84c.24 0 .44-.17.48.41l.36-2.54c.59-.24 1.12-.56 1.62-.94l2.39.96c.22.08.47.01.59-.22l1.92-3.32c.11-.2.06-.47-.12-.61l-2.03-1.58Z"/></svg>',

    "analytics_light": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F0F0F5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>',
    "analytics_dark": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1E293B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>',

    "left-arrow_light": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F0F0F5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>',
    "left-arrow_dark": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1E293B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>',

    "right-arrow_light": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F0F0F5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>',
    "right-arrow_dark": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1E293B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>',

    # Icons for dialogs (can just use one color version)
    "plus_light": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F0F0F5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14m-7-7h14"/></svg>',
    "edit_light": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F0F0F5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
    "delete_light": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F0F0F5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'
}


def get_icon(icon_name: str) -> QIcon:
    """Loads a QIcon directly from predefined SVG data string."""
    svg_data = ICON_DATA.get(icon_name)
    if not svg_data:
        print(f"Warning: Icon data for '{icon_name}' not found.")
        return QIcon()

    # PyQt6 can load icons directly from SVG byte data
    pixmap = QPixmap()
    if pixmap.loadFromData(svg_data.encode('utf-8')):
        # Check if pixmap loaded successfully and has size
        if not pixmap.isNull() and pixmap.width() > 0 and pixmap.height() > 0:
            return QIcon(pixmap)
        else:
            print(
                f"Warning: Pixmap for '{icon_name}' is null or empty after loading SVG data.")
            return QIcon()  # Return empty icon if loading failed or pixmap is invalid
    else:
        print(
            f"Warning: Failed to load pixmap from SVG data for icon '{icon_name}'.")
        return QIcon()  # Return empty icon if loading failed
