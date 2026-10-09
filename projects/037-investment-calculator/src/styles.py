STYLESHEET = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                stop: 0 #667eea, stop: 1 #764ba2);
}

QWidget#mainWidget {
    background: white;
    border-radius: 15px;
    margin: 10px;
}

QTabWidget::pane {
    border: 2px solid #C2C7CB;
    border-radius: 10px;
    background-color: white;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    background-color: #E1E1E1;
    border: 2px solid #C4C4C3;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-width: 8ex;
    padding: 8px 16px;
    margin: 2px;
}

QTabBar::tab:selected {
    background-color: #4CAF50;
    color: white;
}

QLineEdit {
    padding: 8px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 14px;
    background-color: #f9f9f9;
}

QLineEdit:focus {
    border-color: #4CAF50;
    background-color: white;
}

QPushButton {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    font-size: 14px;
    margin: 4px 2px;
    border-radius: 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton#secondary {
    background-color: #2196F3;
}

QPushButton#secondary:hover {
    background-color: #1976D2;
}

QPushButton#danger {
    background-color: #f44336;
}

QPushButton#danger:hover {
    background-color: #d32f2f;
}

QLabel#title {
    font-size: 24px;
    font-weight: bold;
    color: #333;
    padding: 10px;
}

QLabel#result {
    font-size: 18px;
    font-weight: bold;
    color: #4CAF50;
    padding: 15px;
    background-color: #f8fff8;
    border: 2px solid #4CAF50;
    border-radius: 10px;
}

QTableWidget {
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: white;
    gridline-color: #ddd;
}

QHeaderView::section {
    background-color: #4CAF50;
    color: white;
    padding: 8px;
    border: none;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #ddd;
}

QTableWidget::item:selected {
    background-color: #E3F2FD;
}
"""