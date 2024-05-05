from constants import *

class Chessboard:
    def __init__(self):
        self.table = [[None] * SIZE for _ in range (SIZE)]

    def initialize(self):
        self.table[0] = ["8", B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING, B_BISHOP, B_KNIGHT, B_ROOK]
        self.table[1] = ["7"] + [B_PAWN] * 8
        for i in range(2, 6):
            self.table[i] = [str(8-i)] + [" "] * 8
        self.table[6] = ["2"] + [W_PAWN] * 8
        self.table[7] = ["1", W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING, W_BISHOP, W_KNIGHT, W_ROOK]
        self.table[8] = [" ", "A", "B", "C", "D", "E", "F", "G", "H"]
    
    def draw(self):
        for i, row in enumerate(self.table):
            for j, piece in enumerate(row):
                if (i + j) % 2 == 0 and i != 8 and j != 0: 
                    print(BROWN, end="")  
                elif i != 8 and j != 0:
                    print(BEIJE, end="") 
                print(piece, end=" ")
            print(RESET_COLOR)
        print()
    
    
    
