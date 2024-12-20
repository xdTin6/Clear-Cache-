import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QTabWidget, QWidget, QProgressBar, QMessageBox, QListWidget
)
from PyQt5.QtCore import Qt, QSettings
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
        self.setGeometry(200, 200, 400, 400)

        # Persistent settings
        self.settings = QSettings("CacheManagerApp", "Settings")

        # Load theme
        self.current_theme = self.settings.value("theme", "light")
        self.apply_theme(self.current_theme)

        # Tabs Setup
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Dashboard Tab
        self.dashboard_tab = QWidget()
        self.setup_dashboard_tab()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        # Cache Management Tab
        self.cache_tab = QWidget()
        self.setup_cache_tab()
        self.tabs.addTab(self.cache_tab, "Manage Cache")

        # Adobe Cache Tab
        self.adobe_tab = QWidget()
        self.setup_adobe_tab()
        self.tabs.addTab(self.adobe_tab, "Adobe Cache")

        # Delete App Folder Tab
        self.delete_app_tab = QWidget()
        self.setup_delete_app_tab()
        self.tabs.addTab(self.delete_app_tab, "Delete App Folder")

        # Theme Tab
        self.theme_tab = QWidget()
        self.setup_theme_tab()
        self.tabs.addTab(self.theme_tab, "Theme")

    def setup_dashboard_tab(self):
        """Setup dashboard tab with basic information and cache scanning."""
        self.scan_button = QPushButton("Scan Cache")
        self.scan_button.clicked.connect(self.scan_cache)
        self.summary_label = QLabel("Cache sizes will appear here.")
        
        layout = QVBoxLayout()
        layout.addWidget(self.scan_button)
        layout.addWidget(self.summary_label)
        self.dashboard_tab.setLayout(layout)

    def setup_cache_tab(self):
        """Setup cache management controls."""
        self.cache_progress = QProgressBar()
        self.cache_progress.setRange(0, 100)

        self.clear_cache_button = QPushButton("Clear System Cache")
        self.clear_cache_button.clicked.connect(self.clear_system_cache)

        layout = QVBoxLayout()
        layout.addWidget(self.cache_progress)
        layout.addWidget(self.clear_cache_button)
        self.cache_tab.setLayout(layout)

    def setup_adobe_tab(self):
        """Setup Adobe cache management controls."""
        self.adobe_progress = QProgressBar()
        self.adobe_progress.setRange(0, 100)

        self.clear_adobe_button = QPushButton("Clear Adobe Cache")
        self.clear_adobe_button.clicked.connect(self.clear_adobe_cache)

        layout = QVBoxLayout()
        layout.addWidget(self.adobe_progress)
        layout.addWidget(self.clear_adobe_button)
        self.adobe_tab.setLayout(layout)

    def setup_delete_app_tab(self):
        """Setup delete app folder controls."""
        self.delete_folder_button = QPushButton("Scan & Select App Folder to Delete")
        self.delete_folder_button.clicked.connect(self.scan_and_show_app_folders)

        layout = QVBoxLayout()
        layout.addWidget(self.delete_folder_button)
        self.delete_app_tab.setLayout(layout)

    def setup_theme_tab(self):
        """Setup theme tab with options to toggle between themes."""
        self.light_theme_button = QPushButton("Light Theme")
        self.light_theme_button.clicked.connect(self.set_light_theme)

        self.dark_theme_button = QPushButton("Dark Theme")
        self.dark_theme_button.clicked.connect(self.set_dark_theme)

        layout = QVBoxLayout()
        layout.addWidget(self.light_theme_button)
        layout.addWidget(self.dark_theme_button)
        self.theme_tab.setLayout(layout)

    def apply_theme(self, theme):
        """Apply the selected theme."""
        if theme == "light":
            self.setStyleSheet("""
                QMainWindow { background-color: white; }
                QPushButton { background-color: #0078D7; color: white; border-radius: 5px; padding: 5px; }
                QPushButton:hover { background-color: #005EA6; }
                QLabel { color: black; }
                QTabWidget::tab { color: black; }
                QTabBar::tab:selected { background-color: #0078D7; color: white; }
            """)
        elif theme == "dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #2B2B2B; }
                QPushButton { background-color: #444; color: white; border-radius: 5px; padding: 5px; }
                QPushButton:hover { background-color: #666; }
                QLabel { color: white; }
                QTabWidget::tab { color: white; }
                QTabBar::tab:selected { background-color: #444; color: white; }
            """)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(self.current_theme)
        self.settings.setValue("theme", self.current_theme)

    def set_light_theme(self):
        """Set to light theme."""
        self.apply_theme("light")
        self.settings.setValue("theme", "light")

    def set_dark_theme(self):
        """Set to dark theme."""
        self.apply_theme("dark")
        self.settings.setValue("theme", "dark")

    def clear_system_cache(self):
        result = clear_cache()
        QMessageBox.information(self, "Clear Cache", result)

    def clear_adobe_cache(self):
        result = clear_adobe_media_cache()
        QMessageBox.information(self, "Clear Adobe Media Cache", result)

    def scan_cache(self):
        """Scan cache sizes and update the summary label."""
        system_cache_dir = os.path.expanduser("~/Library/Caches")
        adobe_dirs = [
            os.path.expanduser("~/Library/Application Support/Adobe/Media Cache"),
            os.path.expanduser("~/Library/Application Support/Adobe/Media Cache Files"),
            os.path.expanduser("~/Library/Application Support/Adobe/Peak Files")
        ]

        system_cache_size = 0
        adobe_cache_size = 0

        # Calculate system cache size
        if os.path.exists(system_cache_dir):
            system_cache_size = self.get_folder_size(system_cache_dir)

        # Calculate Adobe cache size
        for adobe_dir in adobe_dirs:
            if os.path.exists(adobe_dir):
                adobe_cache_size += self.get_folder_size(adobe_dir)

        # Update summary
        self.summary_label.setText(
            f"\nSystem Cache: {self.human_readable_size(system_cache_size)}\n"
            f"Adobe Cache: {self.human_readable_size(adobe_cache_size)}\n"
        )

    def scan_and_show_app_folders(self):
        """Scan and list the app folders in ~/Library/Application Support for deletion."""
        base_dir = os.path.expanduser("~/Library/Application Support")
        if not os.path.exists(base_dir):
            QMessageBox.warning(self, "Error", "Base directory does not exist.")
            return

        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
        if not folders:
            QMessageBox.information(self, "Delete Folder", "No app folders found to delete.")
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
            result = delete_app_folder(folder_path)
            QMessageBox.information(self, "Delete App Folder", result)
            dialog.close()

        dialog.itemClicked.connect(on_item_selected)

    def get_folder_size(self, folder_path):
        """Recursively calculate folder size."""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        return total_size

    def human_readable_size(self, size):
        """Convert size in bytes to human-readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CacheManagerApp()
    main_window.show()
    sys.exit(app.exec_())
