import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import TicTacToeWindow

def main():
    app = QApplication(sys.argv)
    window = TicTacToeWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()