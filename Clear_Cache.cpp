#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLabel>
#include <QListWidget>
#include <QMessageBox>
#include <QFile>
#include <QDir>
#include <QSettings>
#include <QString>
#include <QStringList>
#include <QStandardPaths>
#include <QFileInfo>

QString greetUser() {
    return QDir::home().dirName();
}

QString clearCache() {
    QString cacheDir = QDir::homePath() + "/Library/Caches";
    QDir dir(cacheDir);
    if (!dir.exists()) {
        return "Cache directory does not exist.";
    }

    int totalDeleted = 0;
    foreach (const QString &entry, dir.entryList(QDir::NoDotAndDotDot | QDir::AllEntries)) {
        QFileInfo fileInfo(dir.absoluteFilePath(entry));
        if (fileInfo.isDir()) {
            QDir(fileInfo.absoluteFilePath()).removeRecursively();
        } else {
            QFile::remove(fileInfo.absoluteFilePath());
        }
        totalDeleted++;
    }

    return QString("Cache cleared. Total items deleted: %1").arg(totalDeleted);
}

QString deleteAppFolder(const QString &folderPath) {
    QDir dir(folderPath);
    if (!dir.exists()) {
        return "Folder does not exist.";
    }

    if (dir.removeRecursively()) {
        return QString("Deleted: %1").arg(folderPath);
    } else {
        return QString("Failed to delete: %1").arg(folderPath);
    }
}

QString clearAdobeMediaCache() {
    QStringList adobeDirs = {
        QDir::homePath() + "/Library/Application Support/Adobe/Media Cache",
        QDir::homePath() + "/Library/Application Support/Adobe/Media Cache Files",
        QDir::homePath() + "/Library/Application Support/Adobe/Peak Files"
    };

    int totalDeleted = 0;
    for (const QString &path : adobeDirs) {
        QDir dir(path);
        if (dir.exists()) {
            foreach (const QString &entry, dir.entryList(QDir::NoDotAndDotDot | QDir::AllEntries)) {
                QFileInfo fileInfo(dir.absoluteFilePath(entry));
                if (fileInfo.isDir()) {
                    QDir(fileInfo.absoluteFilePath()).removeRecursively();
                } else {
                    QFile::remove(fileInfo.absoluteFilePath());
                }
                totalDeleted++;
            }
        }
    }

    return QString("Adobe Media Cache cleared. Total items deleted: %1").arg(totalDeleted);
}

class CacheManagerApp : public QMainWindow {
    Q_OBJECT

public:
    CacheManagerApp(QWidget *parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("Cache Manager");
        resize(400, 300);

        QVBoxLayout *layout = new QVBoxLayout();
        QWidget *container = new QWidget();
        setCentralWidget(container);
        container->setLayout(layout);

        // Persistent settings
        settings = new QSettings("CacheManagerApp", "Settings", this);
        currentTheme = settings->value("theme", "light").toString();
        applyTheme(currentTheme);

        // Greeting label
        QLabel *greetingLabel = new QLabel(QString("Hello, %1! Manage your cache below:").arg(greetUser()));
        greetingLabel->setAlignment(Qt::AlignCenter);
        layout->addWidget(greetingLabel);

        // Clear cache button
        QPushButton *clearCacheButton = new QPushButton("Clear System Cache");
        layout->addWidget(clearCacheButton);
        connect(clearCacheButton, &QPushButton::clicked, this, &CacheManagerApp::clearCacheAction);

        // Delete app folder button
        QPushButton *deleteFolderButton = new QPushButton("Delete App Folder");
        layout->addWidget(deleteFolderButton);
        connect(deleteFolderButton, &QPushButton::clicked, this, &CacheManagerApp::deleteFolderAction);

        // Clear Adobe cache button
        QPushButton *clearAdobeButton = new QPushButton("Clear Adobe Media Cache");
        layout->addWidget(clearAdobeButton);
        connect(clearAdobeButton, &QPushButton::clicked, this, &CacheManagerApp::clearAdobeCacheAction);

        // Theme toggle button
        QPushButton *themeToggleButton = new QPushButton("Toggle Theme");
        layout->addWidget(themeToggleButton);
        connect(themeToggleButton, &QPushButton::clicked, this, &CacheManagerApp::toggleTheme);
    }

private slots:
    void clearCacheAction() {
        QMessageBox::information(this, "Clear Cache", clearCache());
    }

    void deleteFolderAction() {
        QString baseDir = QDir::homePath() + "/Library/Application Support";
        QDir dir(baseDir);
        if (!dir.exists()) {
            QMessageBox::warning(this, "Error", "Base directory does not exist.");
            return;
        }

        QListWidget *dialog = new QListWidget(this);
        dialog->setWindowTitle("Select Folder to Delete");
        dialog->setMinimumSize(300, 400);

        foreach (const QString &entry, dir.entryList(QDir::NoDotAndDotDot | QDir::Dirs)) {
            dialog->addItem(entry);
        }

        connect(dialog, &QListWidget::itemClicked, this, [this, dialog, baseDir](QListWidgetItem *item) {
            QString folderPath = baseDir + "/" + item->text();
            QMessageBox::StandardButton reply = QMessageBox::question(
                this, "Confirm Deletion",
                QString("Are you sure you want to delete %1?").arg(folderPath),
                QMessageBox::Yes | QMessageBox::No
            );

            if (reply == QMessageBox::Yes) {
                QMessageBox::information(this, "Delete Folder", deleteAppFolder(folderPath));
            }
            dialog->close();
        });

        dialog->show();
    }

    void clearAdobeCacheAction() {
        QMessageBox::information(this, "Clear Adobe Media Cache", clearAdobeMediaCache());
    }

    void toggleTheme() {
        currentTheme = (currentTheme == "light") ? "dark" : "light";
        applyTheme(currentTheme);
        settings->setValue("theme", currentTheme);
    }

private:
    void applyTheme(const QString &theme) {
        if (theme == "light") {
            setStyleSheet(
                "QMainWindow { background-color: white; }"
                "QPushButton { background-color: #0078D7; color: white; border-radius: 5px; padding: 5px; }"
                "QPushButton:hover { background-color: #005EA6; }"
                "QLabel { color: black; }"
            );
        } else if (theme == "dark") {
            setStyleSheet(
                "QMainWindow { background-color: #2B2B2B; }"
                "QPushButton { background-color: #444; color: white; border-radius: 5px; padding: 5px; }"
                "QPushButton:hover { background-color: #666; }"
                "QLabel { color: white; }"
            );
        }
    }

    QString currentTheme;
    QSettings *settings;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    CacheManagerApp window;
    window.show();

    return app.exec();
}
