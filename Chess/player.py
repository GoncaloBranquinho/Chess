from constants import *

class Player:
    def __init__(self, color):
        self.color = color
    # convert user input to its respective matrix indexes
    def convert(self, coor):
        if (coor[0] > 'Z'):
            coor = chr(ord(coor[0]) - 32) + coor[1] 
        x1 = 7 - (ord(coor[1]) - ord('1'))
        y1 = ord(coor[0]) - ord('A') + 1
        return (x1, y1)
    
    
    def get_input(self, table):
        flag = True
        while flag:
            print("  Player %s's turn." % self.color)
            userInput = input("  Enter your move: ")
            splitInTwo = userInput.split()
            if len(splitInTwo) == 2 and len(splitInTwo[0]) == 2 and len(splitInTwo[1]) == 2:
                flag = False
            if flag == False:
                toMove = splitInTwo[0]
                toGo = splitInTwo[1]
                x1, y1 = self.convert(toMove)
                x2, y2 = self.convert(toGo)
                # see if the input is valid
                if self.is_in_board(x1, y1, x2, y2) and self.is_player_turn(x1, y1, table):
                    return (x1,y1,x2,y2)
                else:
                    flag = True
            print("  Invalid move please try again: ")
                    
        

    def getPieceColor(self, piece, table):
        
        if piece in [W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING, W_PAWN]:
            return "White"
        elif piece in [B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING, B_PAWN]:
            return "Black"
        elif piece == " ":
            return " "
        return "None"
    
    def is_in_board(self, x1, y1, x2, y2):
        if x1 >= 0 and x2 >= 0 and x1 < 8 and x2 < 8 and y1 > 0 and y2 > 0 and y1 < 9 and y2 < 9:
            return True
        return False   
        
    def is_player_turn(self, x1, y1, table):
        return self.getPieceColor(table[x1][y1], table) ==  self.color
