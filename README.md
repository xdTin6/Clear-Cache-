import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPixmap
import sys

def greet_user():
    """Return the username for greeting."""
    return os.path.expanduser("~").split("/")[-1]

def clear_cache():
    """Clear cache files in ~/Library/Caches."""
    cache_dir = os.path.expanduser("~/Library/Caches")
    total_deleted = 0

    if not os.path.exists(cache_dir):
        return "Cache directory does not exist."

    for item in os.listdir(cache_dir):
        item_path = os.path.join(cache_dir, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            total_deleted += 1
        except Exception as e:
            return f"Failed to delete {item_path}: {e}"

    return f"Cache cleared. Total items deleted: {total_deleted}"

def delete_app_folder(selected_folder):
    """Delete a selected app folder."""
    try:
        shutil.rmtree(selected_folder)
        return f"Deleted: {selected_folder}"
    except Exception as e:
        return f"Failed to delete {selected_folder}: {e}"

def clear_adobe_media_cache():
    """Clear Adobe media cache in specific folders."""
    adobe_dirs = [
        os.path.expanduser("~/Library/Application Support/Adobe/Media Cache"),
        os.path.expanduser("~/Library/Application Support/Adobe/Media Cache Files"),
        os.path.expanduser("~/Library/Application Support/Adobe/Peak Files")
    ]

    total_deleted = 0
    for adobe_dir in adobe_dirs:
        if os.path.exists(adobe_dir):
            for item in os.listdir(adobe_dir):
                item_path = os.path.join(adobe_dir, item)
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    total_deleted += 1
                except Exception as e:
                    return f"Failed to clear {adobe_dir}: {e}"

    return f"Adobe Media Cache cleared. Total items deleted: {total_deleted}"

class CacheManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cache Manager")
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

        # Clear cache button
        self.clear_cache_button = QPushButton("Clear System Cache")
        self.clear_cache_button.clicked.connect(self.clear_cache_action)
        layout.addWidget(self.clear_cache_button)

        # Delete app folder button
        self.delete_folder_button = QPushButton("Delete App Folder")
        self.delete_folder_button.clicked.connect(self.delete_folder_action)
        layout.addWidget(self.delete_folder_button)

        # Clear Adobe cache button
        self.clear_adobe_button = QPushButton("Clear Adobe Media Cache")
        self.clear_adobe_button.clicked.connect(self.clear_adobe_action)
        layout.addWidget(self.clear_adobe_button)

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
            """)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(self.current_theme)
        self.settings.setValue("theme", self.current_theme)

    def clear_cache_action(self):
        result = clear_cache()
        QMessageBox.information(self, "Clear Cache", result)

    def delete_folder_action(self):
        base_dir = os.path.expanduser("~/Library/Application Support")
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
                result = delete_app_folder(folder_path)
                QMessageBox.information(self, "Delete Folder", result)
            dialog.close()

        dialog.itemClicked.connect(on_item_selected)

    def clear_adobe_action(self):
        result = clear_adobe_media_cache()
        QMessageBox.information(self, "Clear Adobe Media Cache", result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CacheManagerApp()
    window.show()
    sys.exit(app.exec_())
