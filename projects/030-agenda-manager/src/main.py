import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import logging

# Setup logging configuration
def setup_logging():
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    # Setup logging first
    setup_logging()
    
    # Buat folder struktur jika belum ada
    folders = ['data', 'data/backup', 'logs', 'exports']
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Agenda Manager Pro")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("AgendaPro")
    
    # Load style
    try:
        from styles import STYLE_CSS
        app.setStyleSheet(STYLE_CSS)
    except Exception as e:
        logging.warning(f"Gagal memuat stylesheet: {e}")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    try:
        from controller import ControllerAgenda
        controller = ControllerAgenda()
        controller.jalankan()
        
        logging.info("Agenda Manager berhasil dijalankan")
        
        return app.exec_()
        
    except Exception as e:
        logging.error(f"Error menjalankan aplikasi: {e}")
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Error", 
                           f"Gagal menjalankan aplikasi:\n{str(e)}\n\n"
                           f"Pastikan semua file dependencies tersedia.")
        return 1

if __name__ == "__main__":
    sys.exit(main())