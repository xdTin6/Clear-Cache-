#include <gtk/gtk.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>

void clear_cache(GtkWidget *widget, gpointer data) {
    const char *cache_dir = g_get_home_dir();
    char path[512];
    snprintf(path, sizeof(path), "%s/Library/Caches", cache_dir);

    DIR *dir = opendir(path);
    if (!dir) {
        gtk_message_dialog_format_secondary_text(GTK_MESSAGE_DIALOG(data), "Cache directory does not exist.");
        return;
    }

    struct dirent *entry;
    int total_deleted = 0;

    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;

        snprintf(path, sizeof(path), "%s/Library/Caches/%s", cache_dir, entry->d_name);
        struct stat path_stat;
        stat(path, &path_stat);

        if (S_ISDIR(path_stat.st_mode)) {
            char command[600];
            snprintf(command, sizeof(command), "rm -rf '%s'", path);
            system(command);
        } else {
            remove(path);
        }

        total_deleted++;
    }

    closedir(dir);
    gchar *message = g_strdup_printf("Cache cleared. Total items deleted: %d", total_deleted);
    gtk_message_dialog_format_secondary_text(GTK_MESSAGE_DIALOG(data), "%s", message);
    g_free(message);
}

void clear_adobe_cache(GtkWidget *widget, gpointer data) {
    const char *cache_dir = g_get_home_dir();
    const char *adobe_dirs[] = {
        "/Library/Application Support/Adobe/Media Cache",
        "/Library/Application Support/Adobe/Media Cache Files",
        "/Library/Application Support/Adobe/Peak Files"
    };

    int total_deleted = 0;
    char path[512];

    for (int i = 0; i < 3; ++i) {
        snprintf(path, sizeof(path), "%s%s", cache_dir, adobe_dirs[i]);

        DIR *dir = opendir(path);
        if (!dir) continue;

        struct dirent *entry;
        while ((entry = readdir(dir)) != NULL) {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;

            snprintf(path, sizeof(path), "%s%s/%s", cache_dir, adobe_dirs[i], entry->d_name);
            struct stat path_stat;
            stat(path, &path_stat);

            if (S_ISDIR(path_stat.st_mode)) {
                char command[600];
                snprintf(command, sizeof(command), "rm -rf '%s'", path);
                system(command);
            } else {
                remove(path);
            }

            total_deleted++;
        }
        closedir(dir);
    }

    gchar *message = g_strdup_printf("Adobe Media Cache cleared. Total items deleted: %d", total_deleted);
    gtk_message_dialog_format_secondary_text(GTK_MESSAGE_DIALOG(data), "%s", message);
    g_free(message);
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Cache Manager");
    gtk_window_set_default_size(GTK_WINDOW(window), 400, 300);

    GtkWidget *vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    gtk_container_add(GTK_CONTAINER(window), vbox);

    GtkWidget *label = gtk_label_new("Manage your cache below:");
    gtk_box_pack_start(GTK_BOX(vbox), label, FALSE, FALSE, 5);

    GtkWidget *clear_cache_button = gtk_button_new_with_label("Clear System Cache");
    gtk_box_pack_start(GTK_BOX(vbox), clear_cache_button, FALSE, FALSE, 5);

    GtkWidget *clear_adobe_button = gtk_button_new_with_label("Clear Adobe Media Cache");
    gtk_box_pack_start(GTK_BOX(vbox), clear_adobe_button, FALSE, FALSE, 5);

    GtkWidget *dialog = gtk_message_dialog_new(GTK_WINDOW(window), GTK_DIALOG_MODAL, GTK_MESSAGE_INFO, GTK_BUTTONS_OK, "Processing...");

    g_signal_connect(clear_cache_button, "clicked", G_CALLBACK(clear_cache), dialog);
    g_signal_connect(clear_adobe_button, "clicked", G_CALLBACK(clear_adobe_cache), dialog);

    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    gtk_widget_show_all(window);
    gtk_main();

    return 0;
}
