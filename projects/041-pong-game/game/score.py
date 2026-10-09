class Score:
    def __init__(self):
        self.left = 0
        self.right = 0
    
    def add_left(self):
        self.left += 1
    
    def add_right(self):
        self.right += 1
    
    def reset(self):
        self.left = 0
        self.right = 0