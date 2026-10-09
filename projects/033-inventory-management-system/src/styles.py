from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication

def setup_app_style(app):
    # Set modern font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Set modern style
    app.setStyle('Fusion')
    
    # Custom palette for dark/light theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(76, 163, 224))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)

def get_stylesheet():
    return """
    QMainWindow {
        background-color: #f0f0f0;
    }
    
    QGroupBox {
        font-weight: bold;
        border: 2px solid #cccccc;
        border-radius: 8px;
        margin-top: 1ex;
        padding-top: 10px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
        color: #2c3e50;
    }
    
    QPushButton {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 8px 16px;
        text-align: center;
        text-decoration: none;
        font-size: 14px;
        margin: 4px 2px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #45a049;
    }
    
    QPushButton:pressed {
        background-color: #3d8b40;
    }
    
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
    
    QLineEdit, QComboBox, QSpinBox {
        padding: 8px;
        border: 2px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
    }
    
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
        border-color: #4CAF50;
    }
    
    QTableWidget {
        gridline-color: #d0d0d0;
        border: 1px solid #cccccc;
        border-radius: 4px;
    }
    
    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    QTableWidget::item:selected {
        background-color: #4CAF50;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #2c3e50;
        color: white;
        padding: 8px;
        border: none;
        font-weight: bold;
    }
    
    QTabWidget::pane {
        border: 1px solid #cccccc;
        border-radius: 4px;
    }
    
    QTabBar::tab {
        background-color: #e0e0e0;
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    
    QTabBar::tab:selected {
        background-color: #4CAF50;
        color: white;
    }
    """