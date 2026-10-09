from game.board import Board
from game.ai_player import AIPlayer
from utils.constants import X, O, MODE_AI_EASY, MODE_AI_MEDIUM, MODE_AI_HARD

class GameLogic:
    def __init__(self):
        self.board = Board()
        self.current_player = X
        self.game_mode = None
        self.ai_player = None
        self.winner = None
        self.is_draw = False
    
    def new_game(self, mode):
        self.board.reset()
        self.current_player = X
        self.game_mode = mode
        self.winner = None
        self.is_draw = False
        
        if mode in [MODE_AI_EASY, MODE_AI_MEDIUM, MODE_AI_HARD]:
            difficulty = mode.split('(')[1].rstrip(')')
            self.ai_player = AIPlayer(difficulty)
        else:
            self.ai_player = None
    
    def make_move(self, row, col):
        if not self.board.is_valid_move(row, col):
            return False
        
        self.board.make_move(row, col, self.current_player)
        
        winner = self.board.check_winner()
        if winner:
            self.winner = winner
            return True
        elif self.board.is_full():
            self.is_draw = True
            return True
        
        self._switch_player()
        return True
    
    def _switch_player(self):
        self.current_player = O if self.current_player == X else X
    
    def ai_move(self):
        if not self.ai_player or self.current_player == X:
            return None
        
        move = self.ai_player.get_move(self.board, self.current_player)
        if move:
            row, col = move
            self.make_move(row, col)
            return (row, col)
        return None
    
    def is_game_over(self):
        return self.winner is not None or self.is_draw
    
    def get_current_player(self):
        return self.current_player