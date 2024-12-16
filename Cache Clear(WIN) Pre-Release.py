import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox
from PyQt5.QtCore import Qt, QSettings
import sys

def greet_user():
    """Return the username for greeting."""
    return os.getlogin()

def clear_temp_files():
    """Clear files in the Windows temp folders."""
    temp_dirs = [
        os.getenv('TEMP'),
        os.getenv('TMP'),
        os.path.join(os.getenv('SystemRoot'), 'Temp')
    ]
    total_deleted = 0

    for temp_dir in temp_dirs:
        if temp_dir and os.path.exists(temp_dir):
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    total_deleted += 1
                except Exception as e:
                    return f"Failed to delete {item_path}: {e}"

    return f"Temporary files cleared. Total items deleted: {total_deleted}"

def delete_app_residual(selected_folder):
    """Delete a selected application residual folder."""
    try:
        shutil.rmtree(selected_folder)
        return f"Deleted: {selected_folder}"
    except Exception as e:
        return f"Failed to delete {selected_folder}: {e}"

def clear_windows_update_cache():
    """Clear Windows Update cache."""
    update_cache_dir = os.path.join(os.getenv('SystemRoot'), 'SoftwareDistribution', 'Download')
    total_deleted = 0

    if os.path.exists(update_cache_dir):
        for item in os.listdir(update_cache_dir):
            item_path = os.path.join(update_cache_dir, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                total_deleted += 1
            except Exception as e:
                return f"Failed to clear {item_path}: {e}"

    return f"Windows Update Cache cleared. Total items deleted: {total_deleted}"

def clear_prefetch():
    """Clear Prefetch files."""
    prefetch_dir = os.path.join(os.getenv('SystemRoot'), 'Prefetch')
    total_deleted = 0

    if os.path.exists(prefetch_dir):
        for item in os.listdir(prefetch_dir):
            item_path = os.path.join(prefetch_dir, item)
            try:
                os.remove(item_path)
                total_deleted += 1
            except Exception as e:
                return f"Failed to delete {item_path}: {e}"

    return f"Prefetch files cleared. Total items deleted: {total_deleted}"

def clear_browser_cache():
    """Clear browser cache for common browsers."""
    browser_dirs = [
        os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache')
    ]

    total_deleted = 0
    for browser_dir in browser_dirs:
        if os.path.exists(browser_dir):
            for item in os.listdir(browser_dir):
                item_path = os.path.join(browser_dir, item)
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    total_deleted += 1
                except Exception as e:
                    return f"Failed to clear {browser_dir}: {e}"

    return f"Browser cache cleared. Total items deleted: {total_deleted}"

class CacheManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows Cache Manager")
        self.setGeometry(200, 200, 400, 300)

        # Persistent settings
        self.settings = QSettings("CacheManagerApp", "Settings")

        # Load theme
        self.current_theme = self.settings.value("theme", "light")
        self.apply_theme(self.current_theme)

        # Main layout
        layout = QVBoxLayout()

        # Greeting label
        user_name = greet_user()
        self.greeting_label = QLabel(f"Hello, {user_name}! Manage your cache below:")
        self.greeting_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.greeting_label)

        # Clear temp files button
        self.clear_temp_button = QPushButton("Clear Temporary Files")
        self.clear_temp_button.clicked.connect(self.clear_temp_action)
        layout.addWidget(self.clear_temp_button)

        # Delete app residuals button
        self.delete_folder_button = QPushButton("Delete App Residual Folder")
        self.delete_folder_button.clicked.connect(self.delete_folder_action)
        layout.addWidget(self.delete_folder_button)

        # Clear Windows update cache button
        self.clear_update_button = QPushButton("Clear Windows Update Cache")
        self.clear_update_button.clicked.connect(self.clear_update_action)
        layout.addWidget(self.clear_update_button)

        # Clear Prefetch files button
        self.clear_prefetch_button = QPushButton("Clear Prefetch Files")
        self.clear_prefetch_button.clicked.connect(self.clear_prefetch_action)
        layout.addWidget(self.clear_prefetch_button)

        # Clear browser cache button
        self.clear_browser_button = QPushButton("Clear Browser Cache")
        self.clear_browser_button.clicked.connect(self.clear_browser_action)
        layout.addWidget(self.clear_browser_button)

        # Theme toggle button
        self.theme_toggle_button = QPushButton("Toggle Theme")
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_toggle_button)

        # Set layout
        container = self.centralWidget()
        if not container:
            from PyQt5.QtWidgets import QWidget
            container = QWidget()
            self.setCentralWidget(container)
        container.setLayout(layout)

    def apply_theme(self, theme):
        """Apply the selected theme."""
        if theme == "light":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: white;
                }
                QPushButton {
                    background-color: #0078D7;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #005EA6;
                }
                QLabel {
                    color: black;
                }
            """)
        elif theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2B2B2B;
                }
                QPushButton {
                    background-color: #444;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
                QLabel {
                    color: white;
                }
            """)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(self.current_theme)
        self.settings.setValue("theme", self.current_theme)

    def clear_temp_action(self):
        result = clear_temp_files()
        QMessageBox.information(self, "Clear Temporary Files", result)

    def delete_folder_action(self):
        base_dir = os.getenv('APPDATA')
        if not os.path.exists(base_dir):
            QMessageBox.warning(self, "Error", "Base directory does not exist.")
            return

        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
        if not folders:
            QMessageBox.information(self, "Delete Folder", "No folders found to delete.")
            return

        # Create a dialog to list folders for deletion
        dialog = QListWidget(self)
        dialog.addItems(folders)
        dialog.setWindowTitle("Select Folder to Delete")
        dialog.setMinimumSize(300, 400)
        dialog.show()

        def on_item_selected(item):
            folder_name = item.text()
            folder_path = os.path.join(base_dir, folder_name)
            reply = QMessageBox.question(
                self, "Confirm Deletion",
                f"Are you sure you want to delete {folder_path}?",
                                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                result = delete_app_residual(folder_path)
                QMessageBox.information(self, "Delete Folder", result)
            dialog.close()

        dialog.itemClicked.connect(on_item_selected)

    def clear_update_action(self):
        result = clear_windows_update_cache()
        QMessageBox.information(self, "Clear Windows Update Cache", result)

    def clear_prefetch_action(self):
        result = clear_prefetch()
        QMessageBox.information(self, "Clear Prefetch Files", result)

    def clear_browser_action(self):
        result = clear_browser_cache()
        QMessageBox.information(self, "Clear Browser Cache", result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CacheManagerApp()
    window.show()
    sys.exit(app.exec_())

