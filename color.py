import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)



# Custom widget that displays a background color
class Color(QWidget):
    def __init__(self, color):
        super().__init__()

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To Do List")

        # Layout containers
        page_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        page_layout.addLayout(button_layout)
        page_layout.addLayout(self.stacklayout)

        # Button + page setup helper
        self.add_page("red", 0, button_layout)
        self.add_page("green", 1, button_layout)
        self.add_page("yellow", 2, button_layout)

        # Central widget
        container = QWidget()
        container.setLayout(page_layout)
        self.setCentralWidget(container)

    # Helper to reduce repeated code
    def add_page(self, color, index, layout):
        btn = QPushButton(color)
        btn.clicked.connect(lambda: self.stacklayout.setCurrentIndex(index))
        layout.addWidget(btn)
        self.stacklayout.addWidget(Color(color))


# Run app
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
