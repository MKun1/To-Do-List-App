import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QMenu, QAction,
    QWidget, QLabel, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from ToDoUI import Ui_MainWindow


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class TaskWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.text = text
        self.completed = False
        self.urgent = False
        self.favorite = False

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 2, 5, 2)
        self.layout.setSpacing(8)
        self.setLayout(self.layout)

        self.line_edit = QLineEdit(text)
        self.line_edit.setReadOnly(True)
        self.line_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.line_edit.customContextMenuRequested.connect(self.show_context_menu)
        self.line_edit.setStyleSheet(self.get_style())
        self.layout.addWidget(self.line_edit)

        self.status_icon = QLabel()
        self.status_icon.setFixedSize(20, 20)
        self.status_icon.setPixmap(QPixmap(resource_path("images/iconsandimages/clock.png")).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.status_icon.setAlignment(Qt.AlignVCenter)
        self.layout.addWidget(self.status_icon)

        self.action_icon = QLabel()
        self.action_icon.setFixedSize(20, 20)
        self.action_icon.setPixmap(QPixmap())  # Initially empty
        self.action_icon.setAlignment(Qt.AlignVCenter)
        self.layout.addWidget(self.action_icon)

        self.set_selected(False)

    def show_context_menu(self, pos):
        menu = QMenu(self)

        toggle_complete = QAction("Mark as Completed" if not self.completed else "Mark as Incomplete", self)
        toggle_complete.triggered.connect(self.toggle_completed)
        menu.addAction(toggle_complete)

        toggle_urgent = QAction("Mark as Urgent" if not self.urgent else "Unmark Urgent", self)
        toggle_urgent.triggered.connect(self.toggle_urgent)
        menu.addAction(toggle_urgent)

        toggle_fav = QAction("Mark as Favorite" if not self.favorite else "Unmark Favorite", self)
        toggle_fav.triggered.connect(self.toggle_favorite)
        menu.addAction(toggle_fav)

        menu.exec_(self.line_edit.mapToGlobal(pos))

    def toggle_completed(self):
        self.completed = not self.completed
        icon = "checkmark.png" if self.completed else "clock.png"
        self.status_icon.setPixmap(QPixmap(resource_path(f"images/iconsandimages/{icon}")).scaled(20, 20))
        self.update_style()

    def toggle_urgent(self):
        self.urgent = not self.urgent
        icon = "warning.png" if self.urgent else ("checkmark.png" if self.completed else "clock.png")
        self.status_icon.setPixmap(QPixmap(resource_path(f"images/iconsandimages/{icon}")).scaled(20, 20))
        self.update_style()

    def toggle_favorite(self):
        self.favorite = not self.favorite
        icon = "star.png" if self.favorite else ""
        if icon:
            self.action_icon.setPixmap(QPixmap(resource_path(f"images/iconsandimages/{icon}")).scaled(20, 20))
        else:
            self.action_icon.setPixmap(QPixmap())
        self.update_style()

    def update_style(self):
        font = QFont()
        font.setStrikeOut(self.completed)
        self.line_edit.setFont(font)
        self.line_edit.setStyleSheet(self.get_style())

    def set_selected(self, selected):
        self.line_edit.setProperty("selected", selected)
        self.line_edit.setStyleSheet(self.get_style())

    def get_style(self):
        bg = "#eaf4ff" if self.line_edit.property("selected") else "#f9f9f9"
        border = "2px solid #4A90E2" if self.line_edit.property("selected") else "1px solid #ccc"
        color = "gray" if self.completed else "red" if self.urgent else "black"

        return f"""
            QLineEdit {{
                background-color: {bg};
                border: {border};
                border-radius: 10px;
                padding: 6px;
                font-size: 14px;
                color: {color};
            }}
            QLineEdit:hover {{
                background-color: #f0f8ff;
                font-size: 15px;
            }}
        """


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("QMainWindow { background: transparent; }")

        self._is_dragging = False
        self._drag_position = None

        self.ui.addtaskbutton.clicked.connect(self.add_task)
        self.ui.deletetaskbutton.clicked.connect(self.delete_selected_task)
        self.ui.exitbutton.clicked.connect(self.close)
        self.ui.minimizebutton.clicked.connect(self.showMinimized)

        self.selected_task = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._is_dragging = False

    def add_task(self):
        text = self.ui.inputtask.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty Task", "Please enter a task.")
            return

        task_widget = TaskWidget(text)
        task_widget.mousePressEvent = lambda event, t=task_widget: self.select_task(event, t)
        self.ui.taskListLayout.addWidget(task_widget)
        self.ui.inputtask.clear()

    def select_task(self, event, task_widget):
        if self.selected_task and self.selected_task is not task_widget:
            self.selected_task.set_selected(False)

        self.selected_task = task_widget
        task_widget.set_selected(True)

    def delete_selected_task(self):
        if self.selected_task:
            self.ui.taskListLayout.removeWidget(self.selected_task)
            self.selected_task.deleteLater()
            self.selected_task = None
        else:
            QMessageBox.information(self, "No Selection", "Please select a task to delete.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
