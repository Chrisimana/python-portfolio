import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from database import DatabaseManager
from widgets import MainTabWidget
from styles import STYLESHEET

class InvestasiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Kalkulator Investasi")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(700, 500)
        
        # Set stylesheet
        self.setStyleSheet(STYLESHEET)
        
        # Central widget
        central_widget = QWidget()
        central_widget.setObjectName("mainWidget")
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Main tab widget
        self.tab_widget = MainTabWidget(self.db_manager)
        layout.addWidget(self.tab_widget)
    
    def refresh_history(self):
        """Refresh history tab"""
        self.tab_widget.refresh_history()

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Kalkulator Investasi")
    app.setApplicationVersion("2.0")
    
    window = InvestasiApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()