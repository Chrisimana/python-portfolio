STYLE_CSS = """
QMainWindow {
    background-color: #2b2b2b;
    color: #ffffff;
}

QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton.danger {
    background-color: #f44336;
}

QPushButton.danger:hover {
    background-color: #da190b;
}

QPushButton.warning {
    background-color: #ff9800;
}

QPushButton.warning:hover {
    background-color: #e68900;
}

QLineEdit, QTextEdit {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px;
    font-size: 14px;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #4CAF50;
}

QListWidget {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555;
    border-radius: 4px;
    font-size: 14px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #555;
}

QListWidget::item:selected {
    background-color: #4CAF50;
    color: white;
}

QTabWidget::pane {
    border: 1px solid #555;
    background-color: #2b2b2b;
}

QTabBar::tab {
    background-color: #3c3c3c;
    color: #ffffff;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #4CAF50;
    color: white;
}

QLabel {
    color: #ffffff;
    font-size: 14px;
}

QLabel.title {
    font-size: 18px;
    font-weight: bold;
    color: #4CAF50;
}

QComboBox {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px;
    min-width: 120px;
}

QSpinBox {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px;
}

QCheckBox {
    color: #ffffff;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    background-color: #3c3c3c;
    border: 1px solid #555;
}

QCheckBox::indicator:checked {
    background-color: #4CAF50;
    border: 1px solid #4CAF50;
}

QGroupBox {
    color: #4CAF50;
    font-weight: bold;
    border: 1px solid #555;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}

QProgressBar {
    border: 1px solid #555;
    border-radius: 4px;
    text-align: center;
    color: white;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 3px;
}

.agenda-item {
    padding: 10px;
    border-bottom: 1px solid #555;
}

.agenda-selesai {
    color: #888;
    text-decoration: line-through;
}

.agenda-prioritas-tinggi {
    border-left: 4px solid #f44336;
}

.agenda-prioritas-sedang {
    border-left: 4px solid #ff9800;
}

.agenda-prioritas-rendah {
    border-left: 4px solid #4CAF50;
}
"""