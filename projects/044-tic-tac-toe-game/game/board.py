from utils.constants import BOARD_SIZE, EMPTY

class Board:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.grid[row][col] = player
            return True
        return False
    
    def is_valid_move(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.grid[row][col] == EMPTY
    
    def get_empty_cells(self):
        empty = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.grid[i][j] == EMPTY:
                    empty.append((i, j))
        return empty
    
    def is_full(self):
        return len(self.get_empty_cells()) == 0
    
    def check_winner(self):
        # Check rows
        for row in self.grid:
            if row[0] != EMPTY and len(set(row)) == 1:
                return row[0]
        
        # Check columns
        for col in range(BOARD_SIZE):
            if self.grid[0][col] != EMPTY and self.grid[0][col] == self.grid[1][col] == self.grid[2][col]:
                return self.grid[0][col]
        
        # Check diagonals
        if self.grid[0][0] != EMPTY and self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
            return self.grid[0][0]
        
        if self.grid[0][2] != EMPTY and self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
            return self.grid[0][2]
        
        return None
    
    def is_game_over(self):
        return self.check_winner() is not None or self.is_full()