import sys, json, os # Import core Python libraries
from PyQt5.QtCore import Qt # Import PyQt5 core functionality
from PyQt5.QtWidgets import ( # Import PyQt5 widgets for building the GUI
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # Import Matplotlib components to embed charts
from matplotlib.figure import Figure

FILE = "tasks.json" # File used for storing tasks

# Main application window
class Main(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("BusyBee 🐝")
        self.resize(800, 600)

        # Layout containers
        page_layout = QVBoxLayout() # Main vertical layout (entire page, splits between the title and the rest of the program)
        page_layout_without_title = QHBoxLayout() # Layout below the title (splits between the graph and the task section)
        task_manipulation_layout = QVBoxLayout() # The left side of page_layout_without_title spitting task controls
        # Sub layouts
        add_task_layout = QHBoxLayout() # input + add button
        task_list_layout = QVBoxLayout() # task list display
        buttons_layout = QHBoxLayout() # action buttons

        # TITLE
        title = QLabel("BusyBee 🐝")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        page_layout.addWidget(title)

        # TASKS LAYOUT (Left Panel)
        task_manipulation_layout.addLayout(add_task_layout) # Puts all the sub layouts inside task_manipulation_layout
        task_manipulation_layout.addLayout(task_list_layout) 
        task_manipulation_layout.addLayout(buttons_layout)

        # Creates input box to add tasks
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter task...") # Text input field for user to type tasks
        self.input_box.returnPressed.connect(self.add_task) # Placeholder text
        add_task_layout.addWidget(self.input_box) # Add input box to add_task_layout

        # BUTTONS
        pending_btn = QPushButton("Pending") # Create button labeled "Pending"
        pending_btn.clicked.connect(self.toggle_pending) # On click, call toggle_pending()
        pending_btn.setStyleSheet("background-color: #1E90FF; color: white; font-weight: bold;")
        buttons_layout.addWidget(pending_btn) # Add button to buttons_layout

        priority_btn = QPushButton("Priority")  # Create "Priority" button
        priority_btn.clicked.connect(self.toggle_priority) # Connect to toggle_priority()
        priority_btn.setStyleSheet("background-color: #FFD700; color: black; font-weight: bold;")
        buttons_layout.addWidget(priority_btn) # Add to buttons_layout

        completed_btn = QPushButton("Completed")
        completed_btn.clicked.connect(self.toggle_completed)
        completed_btn.setStyleSheet("background-color: #32CD32; color: white; font-weight: bold;")
        buttons_layout.addWidget(completed_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_task)
        delete_btn.setStyleSheet("background-color: #FF4500; color: white; font-weight: bold;")
        buttons_layout.addWidget(delete_btn)

        add_btn = QPushButton("Add Task") # Create "Add Task" button
        add_btn.clicked.connect(self.add_task) # Connect to add_task()
        add_btn.setStyleSheet("background-color: #FFA500; color: white; font-weight: bold;")
        add_task_layout.addWidget(add_btn) # Add next to input box in add_task_layout

        # TASK LIST
        self.task_list = QListWidget() # Create list widget to display tasks
        task_list_layout.addWidget(self.task_list) # Add list to task_list_layout

        # RIGHT PANEL PIE CHART
        right_panel = QVBoxLayout() # Layout for right side (chart)
        self.figure = Figure(figsize=(4,4)) # Create matplotlib figure (size 4x4)
        self.canvas = FigureCanvas(self.figure) # Convert figure into a widget for PyQt5
        right_panel.addWidget(self.canvas) # Add chart canvas to layout

        # SPLITTING THE PAGE
        page_layout_without_title.addLayout(task_manipulation_layout, 2) # The task_manipulation layout goes into page_layout_without_title on the left taking up more space 
        page_layout_without_title.addLayout(right_panel, 1) # right_panel fits into page_layout_without_title on the right
        page_layout.addLayout(page_layout_without_title) # Add both panels below title

        self.setLayout(page_layout) # Apply main layout to window

        # LOADING TASKS
        self.load_tasks() # Load tasks from JSON file (if exists)
        self.update_pie_chart()

    # FUNCTIONS
    def add_task(self):# Function to add a new task to the list
        text = self.input_box.text().strip() # Get input text
        if text: # Ensure input is not empty
            self.task_list.addItem(text) # Add task to the list widget
            self.input_box.clear() # Clear input field after adding
            self.save_tasks() # Save updated task list to file
            self.update_pie_chart() # Refresh chart to show new task

    def delete_task(self): # Function to delete a selected task
        row = self.task_list.currentRow() # Get index of currently selected task
        if row >= 0: # Check if the selected item exists
            self.task_list.takeItem(row) # Remove task from the list
            self.save_tasks() # Save updated list
            self.update_pie_chart() # Update chart

    def toggle_priority(self): # Function to toggle "priority" status
        item = self.task_list.currentItem() # Get currently selected task
        if item: # Ensure a task is selected
            text = item.text() # Get task text
            text = text.replace("⏳ ", "").replace("✅ ", "") # Remove other status emojis
            # Toggle priority status
            if text.startswith("⭐ "): # If already marked as priority
                text = text[2:]  # Unmark it (deprioritise)
            else: # If not prioritised
                text = "⭐ " + text # Add the emoji to prioritise
            item.setText(text) # Update task text in UI
            self.save_tasks() # Save changes to the file
            self.update_pie_chart() # Update chart

    def toggle_pending(self): # Function to toggle "pending" status
        # Its basically the same as toggle_priority
        item = self.task_list.currentItem()
        if item:
            text = item.text()s
            text = text.replace("⭐ ", "").replace("✅ ", "")
            if text.startswith("⏳ "):
                text = text[2:]  
            else:
                text = "⏳ " + text
            item.setText(text)
            self.save_tasks()
            self.update_pie_chart()

    def toggle_completed(self): # Function to toggle "completed" status
        # The same as the previous two
        item = self.task_list.currentItem()
        if item:
            text = item.text()
            text = text.replace("⭐ ", "").replace("⏳ ", "")
            if text.startswith("✅ "):
                text = text[2:] 
            else:
                text = "✅ " + text
            item.setText(text)
            self.save_tasks()
            self.update_pie_chart()

    # SAVING AND LOADING
    def save_tasks(self): # Save all tasks to a JSON file
        tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())] # Convert QListWidget items into a Python list
        with open(FILE, "w") as f: # Open file in write mode and save tasks as JSON
            json.dump(tasks, f, indent=4)

    def load_tasks(self):  # Load tasks from JSON file
        if os.path.exists(FILE): # Check if file exists
            with open(FILE) as f: # Open file in read mode
                tasks = json.load(f) # Load JSON data into Python list
                self.task_list.addItems(tasks)  # Fill task list in UI

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
