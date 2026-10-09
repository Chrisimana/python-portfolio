import random
from game.board import Board
from utils.constants import BOARD_SIZE, X, O

class AIPlayer:
    def __init__(self, difficulty='Medium'):
        self.difficulty = difficulty
    
    def get_move(self, board, ai_symbol):
        empty_cells = board.get_empty_cells()
        
        if self.difficulty == 'Easy':
            return random.choice(empty_cells) if empty_cells else None
        
        elif self.difficulty == 'Medium':
            # 70% chance of smart move, 30% random
            if random.random() < 0.7:
                return self._get_best_move(board, ai_symbol)
            else:
                return random.choice(empty_cells) if empty_cells else None
        
        elif self.difficulty == 'Hard':
            return self._get_best_move(board, ai_symbol)
        
        return None
    
    def _get_best_move(self, board, ai_symbol):
        human_symbol = O if ai_symbol == X else X
        best_score = -float('inf')
        best_move = None
        
        for row, col in board.get_empty_cells():
            board.make_move(row, col, ai_symbol)
            score = self._minimax(board, 0, False, ai_symbol, human_symbol)
            board.grid[row][col] = ' '  
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move
    
    def _minimax(self, board, depth, is_maximizing, ai_symbol, human_symbol):
        winner = board.check_winner()
        
        if winner == ai_symbol:
            return 10 - depth
        elif winner == human_symbol:
            return -10 + depth
        elif board.is_full():
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for row, col in board.get_empty_cells():
                board.make_move(row, col, ai_symbol)
                score = self._minimax(board, depth + 1, False, ai_symbol, human_symbol)
                board.grid[row][col] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in board.get_empty_cells():
                board.make_move(row, col, human_symbol)
                score = self._minimax(board, depth + 1, True, ai_symbol, human_symbol)
                board.grid[row][col] = ' '
                best_score = min(score, best_score)
            return best_score