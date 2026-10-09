import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QPushButton, QLabel, QComboBox)
from PyQt5.QtCore import Qt
from game.game_logic import GameLogic
from ui.styles import apply_styles
from utils.constants import MODE_2_PLAYER, MODE_AI_EASY, MODE_AI_MEDIUM, MODE_AI_HARD

class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = GameLogic()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.is_ai_thinking = False  # Flag untuk mencegah AI bergerak saat masih berpikir
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Tic Tac Toe')
        self.setFixedSize(500, 600)
        self.setStyleSheet(apply_styles())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel('Tic Tac Toe')
        title_label.setObjectName('title')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel('Mode Game:')
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([MODE_2_PLAYER, MODE_AI_EASY, MODE_AI_MEDIUM, MODE_AI_HARD])
        self.mode_combo.currentTextChanged.connect(self.reset_game)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)
        
        # Status label
        self.status_label = QLabel('Giliran Pemain X')
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Game board
        board_widget = QWidget()
        board_layout = QGridLayout(board_widget)
        board_layout.setSpacing(10)
        
        for i in range(3):
            for j in range(3):
                button = QPushButton('')
                button.setObjectName('cell')
                button.setFixedSize(120, 120)
                button.clicked.connect(lambda checked, x=i, y=j: self.on_cell_click(x, y))
                board_layout.addWidget(button, i, j)
                self.buttons[i][j] = button
        
        main_layout.addWidget(board_widget, alignment=Qt.AlignCenter)
        
        # Reset button
        reset_button = QPushButton('Game Baru')
        reset_button.setObjectName('reset')
        reset_button.clicked.connect(self.reset_game)
        main_layout.addWidget(reset_button, alignment=Qt.AlignCenter)
        
        main_layout.addStretch()
    
    def on_cell_click(self, row, col):
        # Cegah klik jika game sudah selesai atau AI sedang berpikir
        if self.game.is_game_over() or self.is_ai_thinking:
            return
        
        if self.game.make_move(row, col):
            self.update_board()
            
            if self.game.is_game_over():
                self.show_game_over()
                return
            
            self.update_status()
            
            # PENTING: Hanya jalankan AI jika mode adalah VS AI (bukan 2 Player)
            current_mode = self.mode_combo.currentText()
            is_ai_mode = current_mode != MODE_2_PLAYER
            
            if is_ai_mode and not self.game.is_game_over():
                self.ai_move_with_delay()
    
    def ai_move_with_delay(self):
        self.is_ai_thinking = True
        self.status_label.setText('AI sedang berpikir...')
        
        # Gunakan QTimer untuk delay tanpa memblock UI
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(300, self.perform_ai_move)
    
    def perform_ai_move(self):
        # Double check apakah masih mode AI dan game belum selesai
        current_mode = self.mode_combo.currentText()
        is_ai_mode = current_mode != MODE_2_PLAYER
        
        if is_ai_mode and not self.game.is_game_over():
            ai_move = self.game.ai_move()
            if ai_move:
                self.update_board()
                
                if self.game.is_game_over():
                    self.show_game_over()
                else:
                    self.update_status()
        
        self.is_ai_thinking = False
    
    def update_board(self):
        for i in range(3):
            for j in range(3):
                symbol = self.game.board.grid[i][j]
                self.buttons[i][j].setText(symbol)
                
                if symbol != ' ':
                    self.buttons[i][j].setEnabled(False)
                else:
                    # Hanya enable jika game belum selesai dan AI tidak sedang berpikir
                    self.buttons[i][j].setEnabled(not self.game.is_game_over() and not self.is_ai_thinking)
    
    def update_status(self):
        if not self.game.is_game_over():
            current_mode = self.mode_combo.currentText()
            is_ai_mode = current_mode != MODE_2_PLAYER
            
            if is_ai_mode and self.game.get_current_player() == 'O':
                # Giliran AI, status akan di-update saat AI bergerak
                pass
            else:
                self.status_label.setText(f'Giliran Pemain {self.game.get_current_player()}')
    
    def show_game_over(self):
        if self.game.winner:
            if self.game.winner == 'X':
                self.status_label.setText('Pemain X menang!')
            else:
                # Cek apakah ini mode AI atau 2 Player
                current_mode = self.mode_combo.currentText()
                if current_mode != MODE_2_PLAYER:
                    self.status_label.setText('AI menang!')
                else:
                    self.status_label.setText('Pemain O menang!')
        else:
            self.status_label.setText("Hasil Seri!")
    
    def reset_game(self):
        # Reset flag AI thinking
        self.is_ai_thinking = False
        
        mode = self.mode_combo.currentText()
        self.game.new_game(mode)
        
        # Reset buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText('')
                self.buttons[i][j].setEnabled(True)
        
        self.update_status()
        
        # Reset status label
        self.status_label.setText('Giliran Pemain X')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TicTacToeWindow()
    window.show()
    sys.exit(app.exec_())