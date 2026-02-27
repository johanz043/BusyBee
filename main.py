import sys, json, os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

FILE = "tasks.json"

class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BusyBee 🐝")
        self.resize(800, 600)

        # Layout containers
        page_layout = QVBoxLayout()
        page_layout_without_title = QHBoxLayout()
        task_manipulation_layout = QVBoxLayout()
        add_task_layout = QHBoxLayout()
        task_list_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()

        # =========================
        # TITLE
        # =========================
        title = QLabel("BusyBee 🐝")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        page_layout.addWidget(title)

        # =========================
        # TASK PANEL LEFT
        # =========================
        task_manipulation_layout.addLayout(add_task_layout)
        task_manipulation_layout.addLayout(task_list_layout)
        task_manipulation_layout.addLayout(buttons_layout)

        # INPUT
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter task...")
        self.input_box.returnPressed.connect(self.add_task)
        add_task_layout.addWidget(self.input_box)

        # BUTTONS
        pending_btn = QPushButton("Pending")
        pending_btn.clicked.connect(self.toggle_pending)
        pending_btn.setStyleSheet("background-color: #1E90FF; color: white; font-weight: bold;")
        buttons_layout.addWidget(pending_btn)

        priority_btn = QPushButton("Priority")
        priority_btn.clicked.connect(self.toggle_priority)
        priority_btn.setStyleSheet("background-color: #FFD700; color: black; font-weight: bold;")
        buttons_layout.addWidget(priority_btn)

        completed_btn = QPushButton("Completed")
        completed_btn.clicked.connect(self.toggle_completed)
        completed_btn.setStyleSheet("background-color: #32CD32; color: white; font-weight: bold;")
        buttons_layout.addWidget(completed_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_task)
        delete_btn.setStyleSheet("background-color: #FF4500; color: white; font-weight: bold;")
        buttons_layout.addWidget(delete_btn)

        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self.add_task)
        add_btn.setStyleSheet("background-color: #FFA500; color: white; font-weight: bold;")
        add_task_layout.addWidget(add_btn)

        # TASK LIST
        self.task_list = QListWidget()
        task_list_layout.addWidget(self.task_list)

        # =========================
        # RIGHT PANEL PIE CHART
        # =========================
        right_panel = QVBoxLayout()
        self.figure = Figure(figsize=(4,4))
        self.canvas = FigureCanvas(self.figure)
        right_panel.addWidget(self.canvas)

        # =========================
        # SPLIT PAGE
        # =========================
        page_layout_without_title.addLayout(task_manipulation_layout, 2)
        page_layout_without_title.addLayout(right_panel, 1)
        page_layout.addLayout(page_layout_without_title)

        self.setLayout(page_layout)

        # =========================
        # LOAD TASKS
        # =========================
        self.load_tasks()
        self.update_pie_chart()

    # -----------------------
    # TASK FUNCTIONS
    # -----------------------
    def add_task(self):
        text = self.input_box.text().strip()
        if text:
            self.task_list.addItem(text)
            self.input_box.clear()
            self.save_tasks()
            self.update_pie_chart()

    def delete_task(self):
        row = self.task_list.currentRow()
        if row >= 0:
            self.task_list.takeItem(row)
            self.save_tasks()
            self.update_pie_chart()

    def toggle_priority(self):
        item = self.task_list.currentItem()
        if item:
            text = item.text()
            # Remove other status emojis
            text = text.replace("⏳ ", "").replace("✅ ", "")
            if text.startswith("⭐ "):
                text = text[2:]  # remove star if already priority
            else:
                text = "⭐ " + text
            item.setText(text)
            self.save_tasks()
            self.update_pie_chart()

    def toggle_pending(self):
        item = self.task_list.currentItem()
        if item:
            text = item.text()
            # Remove other status emojis
            text = text.replace("⭐ ", "").replace("✅ ", "")
            if text.startswith("⏳ "):
                text = text[2:]  # remove pending if already pending
            else:
                text = "⏳ " + text
            item.setText(text)
            self.save_tasks()
            self.update_pie_chart()

    def toggle_completed(self):
        item = self.task_list.currentItem()
        if item:
            text = item.text()
            # Remove other status emojis
            text = text.replace("⭐ ", "").replace("⏳ ", "")
            if text.startswith("✅ "):
                text = text[2:]  # unmark completed if already done
            else:
                text = "✅ " + text
            item.setText(text)
            self.save_tasks()
            self.update_pie_chart()

    # -----------------------
    # SAVE / LOAD
    # -----------------------
    def save_tasks(self):
        tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]
        with open(FILE, "w") as f:
            json.dump(tasks, f, indent=4)

    def load_tasks(self):
        if os.path.exists(FILE):
            with open(FILE) as f:
                tasks = json.load(f)
                self.task_list.addItems(tasks)

    # -----------------------
    # PIE CHART
    # -----------------------
    def update_pie_chart(self):
        tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]
        priority = sum(1 for t in tasks if t.startswith("⭐ "))
        pending = sum(1 for t in tasks if t.startswith("⏳ "))
        completed = sum(1 for t in tasks if t.startswith("✅ "))
        none = len(tasks) - priority - pending - completed

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = []
        sizes = []
        colors = []

        if priority:
            labels.append("Priority")
            sizes.append(priority)
            colors.append("#FFD700")  # yellow
        if pending:
            labels.append("Pending")
            sizes.append(pending)
            colors.append("#1E90FF")  # blue
        if completed:
            labels.append("Completed")
            sizes.append(completed)
            colors.append("#32CD32")  # green
        if none:
            labels.append("None")
            sizes.append(none)
            colors.append("#A9A9A9")  # grey

        if not sizes:  # No tasks at all
            # Draw a blank grey circle
            ax.pie([1], colors=['#f0f0f0'])
        else:
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        
        ax.axis('equal')
        self.canvas.draw()


# =========================
# RUN APP
# =========================
app = QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec_())